<a id="PGVISIBILITY"></a>

## F.36. pg_visibility — 可見性對應表資訊與工具 [#](#pgvisibility) <a href="#pgvisibility" id="pgvisibility"></a>

[F.36.1. 函式](pgvisibility.md#PGVISIBILITY-FUNCS)

[F.36.2. 作者](pgvisibility.md#PGVISIBILITY-AUTHOR)

<a id="id-1.11.7.46.2"></a>

`pg_visibility` 模組提供檢視資料表的可見性對應表（VM）與頁面層級可見性資訊的方法。它也提供檢查可見性對應表完整性以及強制重建可見性對應表的函式。

頁面層級的可見性資訊以三個不同的位元儲存。可見性對應表中的全部可見（all-visible）位元表示關聯中對應頁面裡的每個元組，對目前與未來的每個交易都可見。可見性對應表中的全部凍結（all-frozen）位元表示該頁面中的每個元組都已凍結；也就是說，在該頁面上有元組被插入、更新、刪除或鎖定之前，未來的任何清理都不需要修改該頁面。
頁面標頭的 `PD_ALL_VISIBLE` 位元與可見性對應表中的全部可見位元意義相同，但它儲存在資料頁面本身，而不是獨立的資料結構中。
這兩個位元通常一致，但在當機復原之後，有時可能出現頁面的全部可見位元已設定、可見性對應表的位元卻已清除的情況。若在 `pg_visibility` 檢查可見性對應表之後、檢查資料頁面之前發生變更，回報的值也可能不一致。任何造成資料毀損的事件也都可能使這兩個位元不一致。

顯示 `PD_ALL_VISIBLE` 位元資訊的函式，成本遠高於只查閱可見性對應表的函式，因為它們必須讀取關聯的資料區塊，而不只是（小得多的）可見性對應表。檢查關聯資料區塊的函式同樣成本高昂。

<a id="PGVISIBILITY-FUNCS"></a>

### F.36.1. 函式 [#](#PGVISIBILITY-FUNCS)

`pg_visibility_map(relation regclass, blkno bigint, all_visible OUT boolean, all_frozen OUT boolean) returns record`
:   傳回可見性對應表中，指定關聯之指定區塊的全部可見與全部凍結位元。

`pg_visibility(relation regclass, blkno bigint, all_visible OUT boolean, all_frozen OUT boolean, pd_all_visible OUT boolean) returns record`
:   傳回可見性對應表中，指定關聯之指定區塊的全部可見與全部凍結位元，以及該區塊的
    `PD_ALL_VISIBLE` 位元。

`pg_visibility_map(relation regclass, blkno OUT bigint, all_visible OUT boolean, all_frozen OUT boolean) returns setof record`
:   傳回可見性對應表中，指定關聯之每個區塊的全部可見與全部凍結位元。

`pg_visibility(relation regclass, blkno OUT bigint, all_visible OUT boolean, all_frozen OUT boolean, pd_all_visible OUT boolean) returns setof record`
:   傳回可見性對應表中，指定關聯之每個區塊的全部可見與全部凍結位元，以及每個區塊的 `PD_ALL_VISIBLE`
    位元。

`pg_visibility_map_summary(relation regclass, all_visible OUT bigint, all_frozen OUT bigint) returns record`
:   依據可見性對應表，傳回關聯中全部可見頁面的數量與全部凍結頁面的數量。

`pg_check_frozen(relation regclass, t_ctid OUT tid) returns setof tid`
:   傳回儲存在可見性對應表中標記為全部凍結之頁面裡、但尚未凍結的元組 TID。若此函式傳回非空的 TID 集合，表示可見性對應表已毀損。

`pg_check_visible(relation regclass, t_ctid OUT tid) returns setof tid`
:   傳回儲存在可見性對應表中標記為全部可見之頁面裡、但並非全部可見的元組 TID。若此函式傳回非空的 TID 集合，表示可見性對應表已毀損。

`pg_truncate_visibility_map(relation regclass) returns void`
:   截斷指定關聯的可見性對應表。若你認為該關聯的可見性對應表已毀損，並希望強制重建它，此函式很有用。執行此函式之後，在該關聯上執行的第一次 `VACUUM`
    會掃描關聯中的每個頁面並重建可見性對應表。（在此之前，查詢會將可見性對應表視為全部為零。）

預設情況下，這些函式只有超級使用者與具有 `pg_stat_scan_tables` 角色權限的角色可以執行，唯一的例外是
`pg_truncate_visibility_map(relation regclass)`，它只有超級使用者可以執行。

<a id="PGVISIBILITY-AUTHOR"></a>

### F.36.2. 作者 [#](#PGVISIBILITY-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgvisibility.html)（原文版本：18.6；核對日期：2026-10-23）
