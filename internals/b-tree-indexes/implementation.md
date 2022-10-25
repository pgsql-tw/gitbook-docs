# 64.4. Implementation

This section covers B-Tree index implementation details that may be of use to advanced users. See `src/backend/access/nbtree/README` in the source distribution for a much more detailed, internals-focused description of the B-Tree implementation.

## 64.4.1. B-Tree Structure

PostgreSQL B-Tree indexes are multi-level tree structures, where each level of the tree can be used as a doubly-linked list of pages. A single metapage is stored in a fixed position at the start of the first segment file of the index. All other pages are either leaf pages or internal pages. Leaf pages are the pages on the lowest level of the tree. All other levels consist of internal pages. Each leaf page contains tuples that point to table rows. Each internal page contains tuples that point to the next level down in the tree. Typically, over 99% of all pages are leaf pages. Both internal pages and leaf pages use the standard page format described in [Section 70.6](https://www.postgresql.org/docs/14/storage-page-layout.html).

New leaf pages are added to a B-Tree index when an existing leaf page cannot fit an incoming tuple. A _page split_ operation makes room for items that originally belonged on the overflowing page by moving a portion of the items to a new page. Page splits must also insert a new _downlink_ to the new page in the parent page, which may cause the parent to split in turn. Page splits “cascade upwards” in a recursive fashion. When the root page finally cannot fit a new downlink, a _root page split_ operation takes place. This adds a new level to the tree structure by creating a new root page that is one level above the original root page.

## 64.4.2. Bottom-up Index Deletion

B-Tree 索引並不直接考慮 MVCC，同一個邏輯資料表的每筆資料可能存在多個版本；對於索引，每個 tuple 都是一個獨立的物件，需要自己的索引項目。 「Version churn」tuple 有時可能會累積並對查詢延遲和輸出量產生不利影響。這通常發生在 UPDATE 繁重的工作負載中，其中大多數單個更新無法運用 HOT 的最佳化。在 UPDATE 期間只變更一個索引覆寫的一個欄位的值還是需要一組新的索引 tuple — 每一個用於資料表上的索引。請特別注意，這包括未被 UPDATE 「logically modified」的索引。 所有索引都需要一個指向資料表中最新版本的接續實體索引 tuple。每個索引中的每個新 tuple 通常需要與原始「updated」tuple 共存一小段時間（通常直到 UPDATE 交易確認完成之後）。

B-Tree 索引透過執行由下而上的索引刪除程序來逐步刪除 version churn 索引 tuple。每次刪除過程都會被觸發以響應預期的「version churn page split」。這只發生在沒有被 UPDATE 語句邏輯修改的索引，否則會在特定頁面中集中建構過時的版本。通常會避免頁面拆分，儘管某些實作上的啟發式方法可能無法識別和刪除甚至一個垃圾索引元組（在這種情況下，頁面拆分或重複資料刪除傳遞解決了傳入的新 tuple 不適合 leaf tuple）。任何索引掃描必須遍歷的最壞情況版本數量（對於每一單筆邏輯資料）是對整體系統回應能力和輸出量的重要貢獻者。自下而上的索引刪除程序基於涉及邏輯資料列和版本的定性區別針對單個 leaf tuple 中可疑的垃圾元 tuple。這與 autovacuum 工作程序執行的「由上而下」索引清理形成對比，後者在超過某些定量資料表級門檻值時觸發（[請參閱第 25.1.6 節](../../server-administration/routine-database-maintenance-tasks/routine-vacuuming.md#24-1-6-autovacuum-bei-jing-cheng-xu)）。

#### Note

Not all deletion operations that are performed within B-Tree indexes are bottom-up deletion operations. There is a distinct category of index tuple deletion: _simple index tuple deletion_. This is a deferred maintenance operation that deletes index tuples that are known to be safe to delete (those whose item identifier's `LP_DEAD` bit is already set). Like bottom-up index deletion, simple index deletion takes place at the point that a page split is anticipated as a way of avoiding the split.

Simple deletion is opportunistic in the sense that it can only take place when recent index scans set the `LP_DEAD` bits of affected items in passing. Prior to PostgreSQL 14, the only category of B-Tree deletion was simple deletion. The main differences between it and bottom-up deletion are that only the former is opportunistically driven by the activity of passing index scans, while only the latter specifically targets version churn from `UPDATE`s that do not logically modify indexed columns.

Bottom-up index deletion performs the vast majority of all garbage index tuple cleanup for particular indexes with certain workloads. This is expected with any B-Tree index that is subject to significant version churn from `UPDATE`s that rarely or never logically modify the columns that the index covers. The average and worst case number of versions per logical row can be kept low purely through targeted incremental deletion passes. It's quite possible that the on-disk size of certain indexes will never increase by even one single page/block despite _constant_ version churn from `UPDATE`s. Even then, an exhaustive “clean sweep” by a `VACUUM` operation (typically run in an autovacuum worker process) will eventually be required as a part of _collective_ cleanup of the table and each of its indexes.

Unlike `VACUUM`, bottom-up index deletion does not provide any strong guarantees about how old the oldest garbage index tuple may be. No index can be permitted to retain “floating garbage” index tuples that became dead prior to a conservative cutoff point shared by the table and all of its indexes collectively. This fundamental table-level invariant makes it safe to recycle table TIDs. This is how it is possible for distinct logical rows to reuse the same table TID over time (though this can never happen with two logical rows whose lifetimes span the same `VACUUM` cycle).

## 64.4.3. Deduplication

A duplicate is a leaf page tuple (a tuple that points to a table row) where _all_ indexed key columns have values that match corresponding column values from at least one other leaf page tuple in the same index. Duplicate tuples are quite common in practice. B-Tree indexes can use a special, space-efficient representation for duplicates when an optional technique is enabled: _deduplication_.

Deduplication works by periodically merging groups of duplicate tuples together, forming a single _posting list_ tuple for each group. The column key value(s) only appear once in this representation. This is followed by a sorted array of TIDs that point to rows in the table. This significantly reduces the storage size of indexes where each value (or each distinct combination of column values) appears several times on average. The latency of queries can be reduced significantly. Overall query throughput may increase significantly. The overhead of routine index vacuuming may also be reduced significantly.

{% hint style="info" %}
B-Tree 的去重複化對於包含 NULL 值的「duplicates」同樣有效，即使根據任何 B-Tree 運算元的 = 成員，NULL 值也永遠不會彼此相等。 就理解磁碟上 B-Tree 結構實作的任何方面來說，NULL 也只是索引值的一個值的內容罷了。
{% endhint %}

The deduplication process occurs lazily, when a new item is inserted that cannot fit on an existing leaf page, though only when index tuple deletion could not free sufficient space for the new item (typically deletion is briefly considered and then skipped over). Unlike GIN posting list tuples, B-Tree posting list tuples do not need to expand every time a new duplicate is inserted; they are merely an alternative physical representation of the original logical contents of the leaf page. This design prioritizes consistent performance with mixed read-write workloads. Most client applications will at least see a moderate performance benefit from using deduplication. Deduplication is enabled by default.

`CREATE INDEX` and `REINDEX` apply deduplication to create posting list tuples, though the strategy they use is slightly different. Each group of duplicate ordinary tuples encountered in the sorted input taken from the table is merged into a posting list tuple _before_ being added to the current pending leaf page. Individual posting list tuples are packed with as many TIDs as possible. Leaf pages are written out in the usual way, without any separate deduplication pass. This strategy is well-suited to `CREATE INDEX` and `REINDEX` because they are once-off batch operations.

Write-heavy workloads that don't benefit from deduplication due to having few or no duplicate values in indexes will incur a small, fixed performance penalty (unless deduplication is explicitly disabled). The `deduplicate_items` storage parameter can be used to disable deduplication within individual indexes. There is never any performance penalty with read-only workloads, since reading posting list tuples is at least as efficient as reading the standard tuple representation. Disabling deduplication isn't usually helpful.

It is sometimes possible for unique indexes (as well as unique constraints) to use deduplication. This allows leaf pages to temporarily “absorb” extra version churn duplicates. Deduplication in unique indexes augments bottom-up index deletion, especially in cases where a long-running transactions holds a snapshot that blocks garbage collection. The goal is to buy time for the bottom-up index deletion strategy to become effective again. Delaying page splits until a single long-running transaction naturally goes away can allow a bottom-up deletion pass to succeed where an earlier deletion pass failed.

#### Tip

A special heuristic is applied to determine whether a deduplication pass in a unique index should take place. It can often skip straight to splitting a leaf page, avoiding a performance penalty from wasting cycles on unhelpful deduplication passes. If you're concerned about the overhead of deduplication, consider setting `deduplicate_items = off` selectively. Leaving deduplication enabled in unique indexes has little downside.

Deduplication cannot be used in all cases due to implementation-level restrictions. Deduplication safety is determined when `CREATE INDEX` or `REINDEX` is run.

Note that deduplication is deemed unsafe and cannot be used in the following cases involving semantically significant differences among equal datums:

* `text`, `varchar`, and `char` cannot use deduplication when a _nondeterministic_ collation is used. Case and accent differences must be preserved among equal datums.
* `numeric` cannot use deduplication. Numeric display scale must be preserved among equal datums.
* `jsonb` cannot use deduplication, since the `jsonb` B-Tree operator class uses `numeric` internally.
* `float4` and `float8` cannot use deduplication. These types have distinct representations for `-0` and `0`, which are nevertheless considered equal. This difference must be preserved.

There is one further implementation-level restriction that may be lifted in a future version of PostgreSQL:

* Container types (such as composite types, arrays, or range types) cannot use deduplication.

There is one further implementation-level restriction that applies regardless of the operator class or collation used:

* `INCLUDE` indexes can never use deduplication.
