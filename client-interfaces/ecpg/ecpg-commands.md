<a id="ECPG-COMMANDS"></a>

## 34.3. 執行 SQL 命令 [#](#ECPG-COMMANDS)

[34.3.1. 執行 SQL 陳述式](ecpg-commands.md#ECPG-EXECUTING)

[34.3.2. 使用游標](ecpg-commands.md#ECPG-CURSORS)

[34.3.3. 管理交易](ecpg-commands.md#ECPG-TRANSACTIONS)

[34.3.4. 預備陳述式](ecpg-commands.md#ECPG-PREPARED)

任何 SQL 命令都可以在嵌入式 SQL 應用程式中執行。以下是幾個執行方式的範例。

<a id="ECPG-EXECUTING"></a>

### 34.3.1. 執行 SQL 陳述式 [#](#ECPG-EXECUTING)

建立資料表：

```

EXEC SQL CREATE TABLE foo (number integer, ascii char(16));
EXEC SQL CREATE UNIQUE INDEX num1 ON foo(number);
EXEC SQL COMMIT;
```

插入資料列：

```

EXEC SQL INSERT INTO foo (number, ascii) VALUES (9999, 'doodad');
EXEC SQL COMMIT;
```

刪除資料列：

```

EXEC SQL DELETE FROM foo WHERE number = 9999;
EXEC SQL COMMIT;
```

更新：

```

EXEC SQL UPDATE foo
    SET ascii = 'foobar'
    WHERE number = 9999;
EXEC SQL COMMIT;
```

傳回單一結果資料列的 `SELECT` 陳述式，也可以直接使用 `EXEC SQL` 執行。若要處理含有多個資料列的結果集，應用程式必須使用游標；請參閱下方的[第 34.3.2 節](ecpg-commands.md#ECPG-CURSORS)。（作為特例，應用程式可以一次將多個資料列擷取到陣列主機變數中；請參閱[第 34.4.4.3.1 節](ecpg-variables.md#ECPG-VARIABLES-ARRAYS)。）

單列查詢：

```

EXEC SQL SELECT foo INTO :FooBar FROM table1 WHERE ascii = 'doodad';
```

此外，也可以使用 `SHOW` 命令取得設定參數的值：

```

EXEC SQL SHOW search_path INTO :var;
```

形式為 `:something` 的語彙單元就是*主機變數*，也就是說，它們參照 C 程式中的變數。[第 34.4 節](ecpg-variables.md)會說明主機變數。

<a id="ECPG-CURSORS"></a>

### 34.3.2. 使用游標 [#](#ECPG-CURSORS)

若要取得含有多個資料列的結果集，應用程式必須宣告游標，並從游標逐一擷取每個資料列。使用游標的步驟如下：宣告游標、開啟游標、從游標擷取一個資料列、重複擷取，最後關閉游標。

使用游標查詢：

```

EXEC SQL DECLARE foo_bar CURSOR FOR
    SELECT number, ascii FROM foo
    ORDER BY ascii;
EXEC SQL OPEN foo_bar;
EXEC SQL FETCH foo_bar INTO :FooBar, DooDad;
...
EXEC SQL CLOSE foo_bar;
EXEC SQL COMMIT;
```

關於宣告游標的更多細節，請參閱 [DECLARE](ecpg-sql-declare.md)；關於從游標擷取資料列的更多細節，請參閱 [FETCH](../../reference/sql-commands/sql-fetch.md)。

譯註：上方範例程式碼依原文保留；其中 FETCH 的 INTO 清單第二個目標 DooDad 少了主機變數必須有的冒號前綴，正確寫法應為 :DooDad。

### 注意

ECPG 的 `DECLARE` 命令實際上並不會把陳述式送到 PostgreSQL 後端。游標是在執行 `OPEN` 命令的時候，才（使用後端的 `DECLARE` 命令）在後端開啟。

<a id="ECPG-TRANSACTIONS"></a>

### 34.3.3. 管理交易 [#](#ECPG-TRANSACTIONS)

在預設模式下，陳述式只有在發出 `EXEC SQL COMMIT` 時才會提交。嵌入式 SQL 介面也支援交易的自動提交（類似 psql 的預設行為），可以透過 `ecpg` 的 `-t` 命令列選項（請參閱 [ecpg](../../reference/reference-client/app-ecpg.md)），或透過 `EXEC SQL SET AUTOCOMMIT TO
ON` 陳述式啟用。在自動提交模式下，除非命令位於明確的交易區塊內，否則每個命令都會自動提交。此模式可以使用 `EXEC
SQL SET AUTOCOMMIT TO OFF` 明確關閉。

可以使用下列交易管理命令：

<a id="ECPG-TRANSACTIONS-EXEC-SQL-COMMIT"></a>

`EXEC SQL COMMIT` [#](#ECPG-TRANSACTIONS-EXEC-SQL-COMMIT)
:   提交進行中的交易。
<a id="ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK"></a>

`EXEC SQL ROLLBACK` [#](#ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK)
:   回復進行中的交易。
<a id="ECPG-TRANSACTIONS-EXEC-SQL-PREPARE-TRANSACTION"></a>

`EXEC SQL PREPARE TRANSACTION` *`transaction_id`* [#](#ECPG-TRANSACTIONS-EXEC-SQL-PREPARE-TRANSACTION)
:   為兩階段提交準備目前的交易。
<a id="ECPG-TRANSACTIONS-EXEC-SQL-COMMIT-PREPARED"></a>

`EXEC SQL COMMIT PREPARED` *`transaction_id`* [#](#ECPG-TRANSACTIONS-EXEC-SQL-COMMIT-PREPARED)
:   提交處於已準備狀態的交易。
<a id="ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK-PREPARED"></a>

`EXEC SQL ROLLBACK PREPARED` *`transaction_id`* [#](#ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK-PREPARED)
:   回復處於已準備狀態的交易。
<a id="ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-ON"></a>

`EXEC SQL SET AUTOCOMMIT TO ON` [#](#ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-ON)
:   啟用自動提交模式。
<a id="ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-OFF"></a>

`EXEC SQL SET AUTOCOMMIT TO OFF` [#](#ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-OFF)
:   停用自動提交模式。這是預設行為。

<a id="ECPG-PREPARED"></a>

### 34.3.4. 預備陳述式 [#](#ECPG-PREPARED)

當要傳給 SQL 陳述式的值在編譯時期還不知道，或同一個陳述式將被使用很多次時，預備陳述式就很有用。

陳述式以 `PREPARE` 命令來準備。對於尚未知道的值，請使用預留位置「`?`」：

```

EXEC SQL PREPARE stmt1 FROM "SELECT oid, datname FROM pg_database WHERE oid = ?";
```

若陳述式傳回單一資料列，應用程式可以在 `PREPARE` 之後呼叫 `EXECUTE` 來執行該陳述式，並以 `USING` 子句提供預留位置的實際值：

```

EXEC SQL EXECUTE stmt1 INTO :dboid, :dbname USING 1;
```

若陳述式傳回多個資料列，應用程式可以使用以該預備陳述式為基礎宣告的游標。若要繫結輸入參數，必須以 `USING` 子句開啟游標：

```

EXEC SQL PREPARE stmt1 FROM "SELECT oid,datname FROM pg_database WHERE oid > ?";
EXEC SQL DECLARE foo_bar CURSOR FOR stmt1;

/* when end of result set reached, break out of while loop */
EXEC SQL WHENEVER NOT FOUND DO BREAK;

EXEC SQL OPEN foo_bar USING 100;
...
while (1)
{
    EXEC SQL FETCH NEXT FROM foo_bar INTO :dboid, :dbname;
    ...
}
EXEC SQL CLOSE foo_bar;
```

不再需要該預備陳述式時，你應該將它釋放：

```

EXEC SQL DEALLOCATE PREPARE name;
```

關於 `PREPARE` 的更多細節，請參閱 [PREPARE](ecpg-sql-prepare.md)。關於使用預留位置與輸入參數的更多細節，另請參閱[第 34.5 節](ecpg-dynamic.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-commands.html)（原文版本：18.6；核對日期：2026-10-22）
