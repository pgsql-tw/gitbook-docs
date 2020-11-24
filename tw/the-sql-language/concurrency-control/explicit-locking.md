# 13.3. 鎖定模式

PostgreSQL provides various lock modes to control concurrent access to data in tables. These modes can be used for application-controlled locking in situations where MVCC does not give the desired behavior. Also, most PostgreSQL commands automatically acquire locks of appropriate modes to ensure that referenced tables are not dropped or modified in incompatible ways while the command executes. \(For example, `TRUNCATE` cannot safely be executed concurrently with other operations on the same table, so it obtains an exclusive lock on the table to enforce that.\)

To examine a list of the currently outstanding locks in a database server, use the [`pg_locks`](https://www.postgresql.org/docs/12/view-pg-locks.html) system view. For more information on monitoring the status of the lock manager subsystem, refer to [Chapter 27](https://www.postgresql.org/docs/12/monitoring.html).

## 13.3.1. Table-Level Locks

The list below shows the available lock modes and the contexts in which they are used automatically by PostgreSQL. You can also acquire any of these locks explicitly with the command [LOCK](https://www.postgresql.org/docs/12/sql-lock.html). Remember that all of these lock modes are table-level locks, even if the name contains the word “row”; the names of the lock modes are historical. To some extent the names reflect the typical usage of each lock mode — but the semantics are all the same. The only real difference between one lock mode and another is the set of lock modes with which each conflicts \(see [Table 13.2](https://www.postgresql.org/docs/12/explicit-locking.html#TABLE-LOCK-COMPATIBILITY)\). Two transactions cannot hold locks of conflicting modes on the same table at the same time. \(However, a transaction never conflicts with itself. For example, it might acquire `ACCESS EXCLUSIVE` lock and later acquire `ACCESS SHARE` lock on the same table.\) Non-conflicting lock modes can be held concurrently by many transactions. Notice in particular that some lock modes are self-conflicting \(for example, an `ACCESS EXCLUSIVE` lock cannot be held by more than one transaction at a time\) while others are not self-conflicting \(for example, an `ACCESS SHARE` lock can be held by multiple transactions\).

**Table-Level Lock Modes**

`ACCESS SHARE`

Conflicts with the `ACCESS EXCLUSIVE` lock mode only.

The `SELECT` command acquires a lock of this mode on referenced tables. In general, any query that only _reads_ a table and does not modify it will acquire this lock mode.

`ROW SHARE`

Conflicts with the `EXCLUSIVE` and `ACCESS EXCLUSIVE` lock modes.

The `SELECT FOR UPDATE` and `SELECT FOR SHARE` commands acquire a lock of this mode on the target table\(s\) \(in addition to `ACCESS SHARE` locks on any other tables that are referenced but not selected `FOR UPDATE/FOR SHARE`\).

`ROW EXCLUSIVE`

Conflicts with the `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE`, and `ACCESS EXCLUSIVE` lock modes.

The commands `UPDATE`, `DELETE`, and `INSERT` acquire this lock mode on the target table \(in addition to `ACCESS SHARE` locks on any other referenced tables\). In general, this lock mode will be acquired by any command that _modifies data_ in a table.

`SHARE UPDATE EXCLUSIVE`

與 SHARE UPDATE EXCLUSIVE、SHARE、SHARE ROW EXCLUSIVE，EXCLUSIVE 和 ACCESS EXCLUSIVE 鎖定模式衝突。此模式可防止資料表發生同時間的資料庫結構變更及 VACUUM 執行。

由 VACUUM（非 FULL）取用，ANALYZE，CREATE INDEX CONCURRENTLY、REINDEX CONCURRENTLY、CREATE STATISTICS 以及某些 ALTER INDEX 和 ALTER TABLE 的指令（有關詳細資訊，請參閱 [ALTER INDEX](../../reference/sql-commands/alter-index.md) 和 [ALTER TABLE](../../reference/sql-commands/alter-table.md)）。

`SHARE`

Conflicts with the `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE`, and `ACCESS EXCLUSIVE` lock modes. This mode protects a table against concurrent data changes.

Acquired by `CREATE INDEX` \(without `CONCURRENTLY`\).

`SHARE ROW EXCLUSIVE`

Conflicts with the `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE`, and `ACCESS EXCLUSIVE` lock modes. This mode protects a table against concurrent data changes, and is self-exclusive so that only one session can hold it at a time.

Acquired by `CREATE TRIGGER` and some forms of `ALTER TABLE` \(see [ALTER TABLE](https://www.postgresql.org/docs/12/sql-altertable.html)\).

`EXCLUSIVE`

Conflicts with the `ROW SHARE`, `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE`, and `ACCESS EXCLUSIVE` lock modes. This mode allows only concurrent `ACCESS SHARE` locks, i.e., only reads from the table can proceed in parallel with a transaction holding this lock mode.

Acquired by `REFRESH MATERIALIZED VIEW CONCURRENTLY`.

`ACCESS EXCLUSIVE`

Conflicts with locks of all modes \(`ACCESS SHARE`, `ROW SHARE`, `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE`, and `ACCESS EXCLUSIVE`\). This mode guarantees that the holder is the only transaction accessing the table in any way.

Acquired by the `DROP TABLE`, `TRUNCATE`, `REINDEX`, `CLUSTER`, `VACUUM FULL`, and `REFRESH MATERIALIZED VIEW` \(without `CONCURRENTLY`\) commands. Many forms of `ALTER INDEX` and `ALTER TABLE` also acquire a lock at this level. This is also the default lock mode for `LOCK TABLE` statements that do not specify a mode explicitly.

{% hint style="info" %}
僅 ACCESS EXCLUSIVE 鎖定會阻擋 SELECT（無 FOR UPDATE / SHARE）語句。
{% endhint %}

Once acquired, a lock is normally held until the end of the transaction. But if a lock is acquired after establishing a savepoint, the lock is released immediately if the savepoint is rolled back to. This is consistent with the principle that `ROLLBACK` cancels all effects of the commands since the savepoint. The same holds for locks acquired within a PL/pgSQL exception block: an error escape from the block releases locks acquired within it.

#### **Table 13.2.  Conflicting Lock Modes**

| Requested Lock Mode | Current Lock Mode |  |  |  |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ACCESS SHARE | ROW SHARE | ROW EXCLUSIVE | SHARE UPDATE EXCLUSIVE | SHARE | SHARE ROW EXCLUSIVE | EXCLUSIVE | ACCESS EXCLUSIVE |  |
| ACCESS SHARE |  |  |  |  |  |  |  | X |
| ROW SHARE |  |  |  |  |  |  | X | X |
| ROW EXCLUSIVE |  |  |  |  | X | X | X | X |
| SHARE UPDATE EXCLUSIVE |  |  |  | X | X | X | X | X |
| SHARE |  |  | X | X |  | X | X | X |
| SHARE ROW EXCLUSIVE |  |  | X | X | X | X | X | X |
| EXCLUSIVE |  | X | X | X | X | X | X | X |
| ACCESS EXCLUSIVE | X | X | X | X | X | X | X | X |

## 13.3.2. Row-Level Locks

除資料表層級的鎖定外，還有資料列層級的鎖定，下面列出了這些資料列層級的鎖定以及 PostgreSQL 自動使用它們的情形。有關資料列層級鎖衝突的完整列表，請參閱 [Table 13.3](explicit-locking.md#table-13-3-conflicting-row-level-locks)。請注意，即使在不同的子事務中，事務也可以在同一筆資料上上持有相衝突的鎖定。但是除此之外，兩個事務永遠不能在同一筆資料上持有相衝突的鎖定。資料列層級的鎖定不會影響資料查詢。它們只是阻止同一筆資料的寫入和鎖定。資料列層級的鎖定會在事務結束時或在保存點回溯期間釋放，就像資料表層級的鎖定一樣。

**Row-Level Lock Modes**

`FOR UPDATE`

FOR UPDATE 會使 SELECT 語句所檢索到的資料被鎖定，就像是要進行更新一樣。這樣可以防止它們被其他事務鎖定，修改或刪除，直到目前的事務結束為止。也就是說，將阻止其他想要嘗試對於這些資料進行 UPDATE，DELETE，SELECT FOR UPDATE，SELECT FOR NO KEY UPDATE，SELECT FOR SHARE 或 SELECT FOR KEY SHARE 的事務，直到目前事務結束為止。相反地，SELECT FOR UPDATE 將等待在同一筆資料上已經執行了以上這些命令的線上事務，然後將鎖定並回傳更新的資料（如果刪除了該筆資料，則不回傳任何資料）。 但是，在 REPEATABLE READ 或 SERIALIZABLE 事務中，如果從事務起始以來要鎖定的資料已被修改，則將引發錯誤。有關更多討論，請參閱[第 13.4 節](data-consistency-checks-at-the-application-level.md)。

資料列上的任何 DELETE 以及修改某些欄位值的 UPDATE 也會獲取 FOR UPDATE 鎖定模式。目前在UPDATE情況下考慮使用的欄位集合是可以在外部鍵上使用的唯一索引（因此不考慮部分索引和表式式索引），但是將來可能會有所改變。

`FOR NO KEY UPDATE`

行為與 FOR UPDATE 類似，除了獲取的鎖定較弱勢之外：此鎖定不會阻止試圖獲取同一筆資料上鎖定的 SELECT FOR KEY SHARE 指令。任何不會取得 FOR UPDATE 鎖定的 UPDATE 也會取得此鎖定模式。

`FOR SHARE`

行為類似於 FOR NO KEY UPDATE，不同之處在於它在每筆檢索到的資料上取得一個共享鎖定，而不是互斥鎖定。共享鎖定可以阻止其他事務在這些資料上執行 UPDATE，DELETE，SELECT FOR UPDATE 或 SELECT FOR NO KEY UPDATE，但不會阻止它們執行 SELECT FOR SHARE 或 SELECT FOR KEY SHARE。

`FOR KEY SHARE`

行為與 FOR SHARE 類似，除了鎖定較弱勢之外：SELECT FOR UPDATE 被阻擋，但 SELECT FOR NO KEY UPDATE 不會。 SELECT FOR NO KEY 鎖定會阻止其他事務執行 DELETE 或任何變更鍵值的 UPDATE 操作，但不會阻止其他 UPDATE 操作，也不會阻止 SELECT FOR NO KEY UPDATE，SELECT FOR SHARE 或 SELECT FOR KEY SHARE。

PostgreSQL 不會去記住記憶體中已修改資料的任何資訊，因此一次鎖定的資料筆數沒有限制。但是，鎖定一筆資料就可能會導致磁碟寫入行為。例如，SELECT FOR UPDATE 會修改所選資料以將其標記為已鎖定，因此將產生磁碟寫入行為。

#### **Table 13.3. Conflicting Row-Level Locks**

| Requested Lock Mode | Current Lock Mode |  |  |  |
| :--- | :--- | :--- | :--- | :--- |
| FOR KEY SHARE | FOR SHARE | FOR NO KEY UPDATE | FOR UPDATE |  |
| FOR KEY SHARE |  |  |  | X |
| FOR SHARE |  |  | X | X |
| FOR NO KEY UPDATE |  | X | X | X |
| FOR UPDATE | X | X | X | X |

## 13.3.3. Page-Level Locks

除了資料表和資料列層級的鎖定之外，頁面層級共享/獨占鎖定用於控制對共享緩衝區中資料表頁面的讀寫存取。在取得或更新一筆資料後，就會立即釋放這些鎖定。應用程序開發人員通常不必關心頁面層級的鎖定，但是出於說明完整性的考量，還是在此稍作說明。

## 13.3.4. Deadlocks

The use of explicit locking can increase the likelihood of _deadlocks_, wherein two \(or more\) transactions each hold locks that the other wants. For example, if transaction 1 acquires an exclusive lock on table A and then tries to acquire an exclusive lock on table B, while transaction 2 has already exclusive-locked table B and now wants an exclusive lock on table A, then neither one can proceed. PostgreSQL automatically detects deadlock situations and resolves them by aborting one of the transactions involved, allowing the other\(s\) to complete. \(Exactly which transaction will be aborted is difficult to predict and should not be relied upon.\)

Note that deadlocks can also occur as the result of row-level locks \(and thus, they can occur even if explicit locking is not used\). Consider the case in which two concurrent transactions modify a table. The first transaction executes:

```text
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 11111;
```

This acquires a row-level lock on the row with the specified account number. Then, the second transaction executes:

```text
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 22222;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 11111;
```

The first `UPDATE` statement successfully acquires a row-level lock on the specified row, so it succeeds in updating that row. However, the second `UPDATE` statement finds that the row it is attempting to update has already been locked, so it waits for the transaction that acquired the lock to complete. Transaction two is now waiting on transaction one to complete before it continues execution. Now, transaction one executes:

```text
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 22222;
```

Transaction one attempts to acquire a row-level lock on the specified row, but it cannot: transaction two already holds such a lock. So it waits for transaction two to complete. Thus, transaction one is blocked on transaction two, and transaction two is blocked on transaction one: a deadlock condition. PostgreSQL will detect this situation and abort one of the transactions.

The best defense against deadlocks is generally to avoid them by being certain that all applications using a database acquire locks on multiple objects in a consistent order. In the example above, if both transactions had updated the rows in the same order, no deadlock would have occurred. One should also ensure that the first lock acquired on an object in a transaction is the most restrictive mode that will be needed for that object. If it is not feasible to verify this in advance, then deadlocks can be handled on-the-fly by retrying transactions that abort due to deadlocks.

只要未檢測到死鎖情況，尋求資料表層級或資料列層級鎖定的事務將無限期地等待衝突的鎖定被釋放。 對於應用程序來說，長時間保持事務處於打開狀態（例如，在等待使用者輸入時）不是一件好事。

## 13.3.5. Advisory Locks

PostgreSQL 提供了一種建立具有應用程式定義的鎖定方法。 這些被稱為 advisory lock，因為系統不會強制使用它們-取決於應用程式是否正確地使用它們。Advisory lock 對於不適用於 MVCC 模型的鎖定策略很有用。例如，Advisory lock 常見的用法是模擬所謂的「flat file」資料管理系統特有的悲觀鎖定策略。雖然儲存在資料表中的識別內容可以用於相同的目的，但 Advisory lock 更快，可以避免資料表膨脹，並在連線結束時由伺服器自動清除。

There are two ways to acquire an advisory lock in PostgreSQL: at session level or at transaction level. Once acquired at session level, an advisory lock is held until explicitly released or the session ends. Unlike standard lock requests, session-level advisory lock requests do not honor transaction semantics: a lock acquired during a transaction that is later rolled back will still be held following the rollback, and likewise an unlock is effective even if the calling transaction fails later. A lock can be acquired multiple times by its owning process; for each completed lock request there must be a corresponding unlock request before the lock is actually released. Transaction-level lock requests, on the other hand, behave more like regular lock requests: they are automatically released at the end of the transaction, and there is no explicit unlock operation. This behavior is often more convenient than the session-level behavior for short-term usage of an advisory lock. Session-level and transaction-level lock requests for the same advisory lock identifier will block each other in the expected way. If a session already holds a given advisory lock, additional requests by it will always succeed, even if other sessions are awaiting the lock; this statement is true regardless of whether the existing lock hold and new request are at session level or transaction level.

Like all locks in PostgreSQL, a complete list of advisory locks currently held by any session can be found in the [`pg_locks`](https://www.postgresql.org/docs/12/view-pg-locks.html) system view.

Both advisory locks and regular locks are stored in a shared memory pool whose size is defined by the configuration variables [max\_locks\_per\_transaction](https://www.postgresql.org/docs/12/runtime-config-locks.html#GUC-MAX-LOCKS-PER-TRANSACTION) and [max\_connections](https://www.postgresql.org/docs/12/runtime-config-connection.html#GUC-MAX-CONNECTIONS). Care must be taken not to exhaust this memory or the server will be unable to grant any locks at all. This imposes an upper limit on the number of advisory locks grantable by the server, typically in the tens to hundreds of thousands depending on how the server is configured.

In certain cases using advisory locking methods, especially in queries involving explicit ordering and `LIMIT` clauses, care must be taken to control the locks acquired because of the order in which SQL expressions are evaluated. For example:

```text
SELECT pg_advisory_lock(id) FROM foo WHERE id = 12345; -- ok
SELECT pg_advisory_lock(id) FROM foo WHERE id > 12345 LIMIT 100; -- danger!
SELECT pg_advisory_lock(q.id) FROM
(
  SELECT id FROM foo WHERE id > 12345 LIMIT 100
) q; -- ok
```

In the above queries, the second form is dangerous because the `LIMIT` is not guaranteed to be applied before the locking function is executed. This might cause some locks to be acquired that the application was not expecting, and hence would fail to release \(until it ends the session\). From the point of view of the application, such locks would be dangling, although still viewable in `pg_locks`.

The functions provided to manipulate advisory locks are described in [Section 9.26.10](https://www.postgresql.org/docs/12/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS).

