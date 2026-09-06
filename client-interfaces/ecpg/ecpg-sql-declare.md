## DECLARE

DECLARE — 定義游標

## 語法

```

DECLARE cursor_name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ] CURSOR [ { WITH | WITHOUT } HOLD ] FOR prepared_name
DECLARE cursor_name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ] CURSOR [ { WITH | WITHOUT } HOLD ] FOR query
```

<a id="id-1.7.5.20.6.3"></a>

## 說明

`DECLARE` 宣告游標，以走訪備妥陳述式的結果集。此命令與直接 SQL 命令 `DECLARE` 的語意稍有不同：後者會執行查詢並準備結果集以供擷取；此嵌入式 SQL 命令只會宣告一個名稱作為走訪查詢結果集的「迴圈變數」，實際執行會在以 `OPEN` 命令開啟游標時發生。

<a id="id-1.7.5.20.6.4"></a>

## 參數

<a id="ECPG-SQL-DECLARE-CURSOR-NAME"></a>

*`cursor_name`* [#](#ECPG-SQL-DECLARE-CURSOR-NAME)
:   游標名稱，區分大小寫。可以是 SQL 識別字或主機變數。
<a id="ECPG-SQL-DECLARE-PREPARED-NAME"></a>

*`prepared_name`* [#](#ECPG-SQL-DECLARE-PREPARED-NAME)
:   備妥查詢的名稱，可以是 SQL 識別字或主機變數。
<a id="ECPG-SQL-DECLARE-QUERY"></a>

*`query`* [#](#ECPG-SQL-DECLARE-QUERY)
:   提供游標要傳回資料列的 [SELECT](../../reference/sql-commands/sql-select.md) 或 [VALUES](../../reference/sql-commands/sql-values.md) 命令。

游標選項的意義請參閱 [DECLARE](../../reference/sql-commands/sql-declare.md)。

<a id="id-1.7.5.20.6.5"></a>

## 範例

以下範例為查詢宣告游標：

```

EXEC SQL DECLARE C CURSOR FOR SELECT * FROM My_Table;
EXEC SQL DECLARE C CURSOR FOR SELECT Item1 FROM T;
EXEC SQL DECLARE cur1 CURSOR FOR SELECT version();
```

以下範例為備妥陳述式宣告游標：

```

EXEC SQL PREPARE stmt1 AS SELECT version();
EXEC SQL DECLARE cur1 CURSOR FOR stmt1;
```

<a id="id-1.7.5.20.6.6"></a>

## 相容性

SQL 標準規定了 `DECLARE`。

<a id="id-1.7.5.20.6.7"></a>

## 另請參閱

[OPEN](ecpg-sql-open.md), [CLOSE](../../reference/sql-commands/sql-close.md), [DECLARE](../../reference/sql-commands/sql-declare.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-declare.html)（英文原文，待翻譯）
