# 13.3.1. 資料表層級鎖定

<a id="LOCKING-TABLES"></a>

## 13.3.1. 資料表層級鎖定 [#](#locking-tables) <a href="#locking-tables" id="locking-tables"></a>

<a id="id-1.5.12.6.5.2"></a>

下列清單列出可用的鎖定模式，以及 PostgreSQL 自動使用它們的情境。你也可以使用 [LOCK](../../../reference/sql-commands/sql-lock.md) 命令明確取得這些鎖定中的任何一種。請記住，這些鎖定模式全都是資料表層級的鎖定，即使名稱中含有「row」一詞也一樣；鎖定模式的名稱是沿襲歷史而來的。在某種程度上，這些名稱反映了每種鎖定模式的典型用途——但它們的語意全都相同。一種鎖定模式與另一種之間唯一真正的差別，在於各自會與哪些鎖定模式衝突（請參閱[表 13.2](#table-lock-compatibility)）。兩個交易不能同時在同一個資料表上持有互相衝突之模式的鎖定。（不過，交易永遠不會與自己衝突。例如，它可以先取得 `ACCESS EXCLUSIVE` 鎖定，之後再在同一個資料表上取得 `ACCESS SHARE` 鎖定。）不會衝突的鎖定模式可以由許多交易同時持有。特別要注意的是，有些鎖定模式會與自己衝突（例如，`ACCESS EXCLUSIVE` 鎖定同一時間只能由一個交易持有），而其他鎖定模式則不會與自己衝突（例如，`ACCESS SHARE` 鎖定可以由多個交易持有）。

**資料表層級鎖定模式**

`ACCESS SHARE` (`AccessShareLock`)

只與 `ACCESS EXCLUSIVE` 鎖定模式衝突。

`SELECT` 命令會在被參照的資料表上取得這種模式的鎖定。一般而言，任何只*讀取*資料表而不修改它的查詢，都會取得這種鎖定模式。

`ROW SHARE` (`RowShareLock`)

與 `EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。

`SELECT` 命令會在所有指定了 `FOR UPDATE`、`FOR NO KEY UPDATE`、`FOR SHARE` 或 `FOR KEY SHARE` 選項之一的資料表上，取得這種模式的鎖定（此外，對於任何其他未指定明確 `FOR ...` 鎖定選項而被參照的資料表，則會取得 `ACCESS SHARE` 鎖定）。

`ROW EXCLUSIVE` (`RowExclusiveLock`)

與 `SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。

`UPDATE`、`DELETE`、`INSERT` 與 `MERGE` 命令會在目標資料表上取得這種鎖定模式（此外，對任何其他被參照的資料表則會取得 `ACCESS SHARE` 鎖定）。一般而言，任何會*修改資料表中資料*的命令，都會取得這種鎖定模式。

`SHARE UPDATE EXCLUSIVE` (`ShareUpdateExclusiveLock`)

與 `SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式可以保護資料表，避免並行的綱要變更與 `VACUUM` 執行。

由 `VACUUM`（不含 `FULL`）、`ANALYZE`、`CREATE INDEX CONCURRENTLY`、`CREATE STATISTICS`、`COMMENT ON`、`REINDEX CONCURRENTLY`，以及某些 [`ALTER INDEX`](../../../reference/sql-commands/sql-alterindex.md) 與 [`ALTER TABLE`](../../../reference/sql-commands/sql-altertable.md) 的變化形式取得（完整細節請參閱這些命令的說明文件）。

`SHARE` (`ShareLock`)

與 `ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式可以保護資料表，避免並行的資料變更。

由 `CREATE INDEX`（不含 `CONCURRENTLY`）取得。

`SHARE ROW EXCLUSIVE` (`ShareRowExclusiveLock`)

與 `ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式可以保護資料表，避免並行的資料變更，而且它會與自己互斥，因此同一時間只能有一個工作階段持有它。

由 `CREATE TRIGGER` 以及某些形式的 [`ALTER TABLE`](../../../reference/sql-commands/sql-altertable.md) 取得。

`EXCLUSIVE` (`ExclusiveLock`)

與 `ROW SHARE`、`ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE` 鎖定模式衝突。這種模式只允許並行的 `ACCESS SHARE` 鎖定，也就是說，在交易持有這種鎖定模式時，只有對該資料表的讀取可以同時進行。

由 `REFRESH MATERIALIZED VIEW CONCURRENTLY` 取得。

`ACCESS EXCLUSIVE` (`AccessExclusiveLock`)

與所有模式的鎖定衝突（`ACCESS SHARE`、`ROW SHARE`、`ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 及 `ACCESS EXCLUSIVE`）。這種模式保證持有者是唯一以任何方式存取該資料表的交易。

由 `DROP TABLE`、`TRUNCATE`、`REINDEX`、`CLUSTER`、`VACUUM FULL` 以及 `REFRESH MATERIALIZED VIEW`（不含 `CONCURRENTLY`）命令取得。許多形式的 `ALTER INDEX` 與 `ALTER TABLE` 也會取得這個層級的鎖定。對於沒有明確指定模式的 `LOCK TABLE` 陳述式，這也是預設的鎖定模式。

### 提示

只有 `ACCESS EXCLUSIVE` 鎖定會阻擋 `SELECT`（不含 `FOR UPDATE/SHARE`）陳述式。

鎖定一旦取得，通常會一直持有到交易結束。但如果鎖定是在建立交易儲存點之後才取得的，那麼在回復到該交易儲存點時，這個鎖定會立即被釋放。這與 `ROLLBACK` 會取消自交易儲存點以來所有命令之效果的原則一致。在 PL/pgSQL 例外處理區塊中取得的鎖定也是如此：因錯誤而跳出該區塊時，會釋放在其中取得的鎖定。

<a id="TABLE-LOCK-COMPATIBILITY"></a>

### 表 13.2. 互相衝突的鎖定模式 [#](#table-lock-compatibility) <a href="#table-lock-compatibility" id="table-lock-compatibility"></a>

<table border="1" class="table" summary="Conflicting Lock Modes"><colgroup><col/><col class="lockst"/><col/><col/><col/><col/><col/><col/><col class="lockend"/></colgroup><thead><tr><th rowspan="2">要求的鎖定模式</th><th align="center" colspan="8">既有的鎖定模式</th></tr><tr><th><code class="literal">ACCESS SHARE</code></th><th><code class="literal">ROW SHARE</code></th><th><code class="literal">ROW EXCL.</code></th><th><code class="literal">SHARE UPDATE EXCL.</code></th><th><code class="literal">SHARE</code></th><th><code class="literal">SHARE ROW EXCL.</code></th><th><code class="literal">EXCL.</code></th><th><code class="literal">ACCESS EXCL.</code></th></tr></thead><tbody><tr><td><code class="literal">ACCESS SHARE</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td></tr><tr><td><code class="literal">ROW SHARE</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">ROW EXCL.</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">SHARE UPDATE EXCL.</code></td><td align="center"> </td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">SHARE</code></td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">SHARE ROW EXCL.</code></td><td align="center"> </td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">EXCL.</code></td><td align="center"> </td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr><tr><td><code class="literal">ACCESS EXCL.</code></td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td><td align="center">X</td></tr></tbody></table>

<br>

[返回 13.3. 明確鎖定](../explicit-locking.md#explicit-locking)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/explicit-locking.html)（原文版本：18.6；核對日期：2026-09-11）
