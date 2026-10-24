<a id="ECPG-TRANSACTIONS"></a>

## 34.3.3. 管理交易 [#](#ecpg-transactions) <a href="#ecpg-transactions" id="ecpg-transactions"></a>

在預設模式下，陳述式只有在發出 `EXEC SQL COMMIT` 時才會提交。嵌入式 SQL 介面也支援交易的自動提交（類似 psql 的預設行為），可以透過 `ecpg` 的 `-t` 命令列選項（請參閱 [ecpg](../../reference/reference-client/app-ecpg.md)），或透過 `EXEC SQL SET AUTOCOMMIT TO
ON` 陳述式啟用。在自動提交模式下，除非命令位於明確的交易區塊內，否則每個命令都會自動提交。此模式可以使用 `EXEC
SQL SET AUTOCOMMIT TO OFF` 明確關閉。

可以使用下列交易管理命令：

<a id="ECPG-TRANSACTIONS-EXEC-SQL-COMMIT"></a>

### `EXEC SQL COMMIT` [#](#ecpg-transactions-exec-sql-commit) <a href="#ecpg-transactions-exec-sql-commit" id="ecpg-transactions-exec-sql-commit"></a>

提交進行中的交易。

<a id="ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK"></a>

### `EXEC SQL ROLLBACK` [#](#ecpg-transactions-exec-sql-rollback) <a href="#ecpg-transactions-exec-sql-rollback" id="ecpg-transactions-exec-sql-rollback"></a>

回復進行中的交易。

<a id="ECPG-TRANSACTIONS-EXEC-SQL-PREPARE-TRANSACTION"></a>

### `EXEC SQL PREPARE TRANSACTION` *`transaction_id`* [#](#ecpg-transactions-exec-sql-prepare-transaction) <a href="#ecpg-transactions-exec-sql-prepare-transaction" id="ecpg-transactions-exec-sql-prepare-transaction"></a>

為兩階段提交準備目前的交易。

<a id="ECPG-TRANSACTIONS-EXEC-SQL-COMMIT-PREPARED"></a>

### `EXEC SQL COMMIT PREPARED` *`transaction_id`* [#](#ecpg-transactions-exec-sql-commit-prepared) <a href="#ecpg-transactions-exec-sql-commit-prepared" id="ecpg-transactions-exec-sql-commit-prepared"></a>

提交處於已準備狀態的交易。

<a id="ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK-PREPARED"></a>

### `EXEC SQL ROLLBACK PREPARED` *`transaction_id`* [#](#ecpg-transactions-exec-sql-rollback-prepared) <a href="#ecpg-transactions-exec-sql-rollback-prepared" id="ecpg-transactions-exec-sql-rollback-prepared"></a>

回復處於已準備狀態的交易。

<a id="ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-ON"></a>

### `EXEC SQL SET AUTOCOMMIT TO ON` [#](#ecpg-transactions-exec-sql-autocommit-on) <a href="#ecpg-transactions-exec-sql-autocommit-on" id="ecpg-transactions-exec-sql-autocommit-on"></a>

啟用自動提交模式。

<a id="ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-OFF"></a>

### `EXEC SQL SET AUTOCOMMIT TO OFF` [#](#ecpg-transactions-exec-sql-autocommit-off) <a href="#ecpg-transactions-exec-sql-autocommit-off" id="ecpg-transactions-exec-sql-autocommit-off"></a>

停用自動提交模式。這是預設行為。

[返回 34.3. 執行 SQL 命令](ecpg-commands.md#ecpg-commands)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-commands.html)（原文版本：18.6；核對日期：2026-10-22）
