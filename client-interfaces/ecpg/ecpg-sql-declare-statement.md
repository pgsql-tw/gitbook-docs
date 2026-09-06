## DECLARE STATEMENT

DECLARE STATEMENT — 宣告 SQL 陳述式識別字

## 語法

```

EXEC SQL [ AT connection_name ] DECLARE statement_name STATEMENT
```

<a id="id-1.7.5.20.7.3"></a>

## 說明

`DECLARE STATEMENT` 宣告 SQL 陳述式識別字。SQL 陳述式識別字可與連線相關聯；動態 SQL 陳述式使用該識別字時，會使用相關聯的連線執行。宣告的命名空間是預編譯單元，不允許對同一 SQL 陳述式識別字進行多次宣告。請注意，若預編譯器以 Informix 相容模式執行且已宣告 SQL 陳述式，便不能將 `database` 用作游標名稱。

<a id="id-1.7.5.20.7.4"></a>

## 參數

<a id="ECPG-SQL-DECLARE-STATEMENT-CONNECTION-NAME"></a>

*`connection_name`* [#](#ECPG-SQL-DECLARE-STATEMENT-CONNECTION-NAME)
:   由 `CONNECT` 命令建立的資料庫連線名稱。

    可省略 `AT` 子句，但這樣的陳述式沒有意義。

<a id="ECPG-SQL-DECLARE-STATEMENT-STATEMENT-NAME"></a>

*`statement_name`* [#](#ECPG-SQL-DECLARE-STATEMENT-STATEMENT-NAME)
:   SQL 陳述式識別字名稱，可以是 SQL 識別字或主機變數。

<a id="id-1.7.5.20.7.5"></a>

## 注意事項

只有在宣告實際放在動態陳述式之前時，此關聯才有效。

<a id="id-1.7.5.20.7.6"></a>

## 範例

```

EXEC SQL CONNECT TO postgres AS con1;
EXEC SQL AT con1 DECLARE sql_stmt STATEMENT;
EXEC SQL DECLARE cursor_name CURSOR FOR sql_stmt;
EXEC SQL PREPARE sql_stmt FROM :dyn_string;
EXEC SQL OPEN cursor_name;
EXEC SQL FETCH cursor_name INTO :column1;
EXEC SQL CLOSE cursor_name;
```

<a id="id-1.7.5.20.7.7"></a>

## 相容性

`DECLARE STATEMENT` 是 SQL 標準的擴充功能，但可用於知名的資料庫管理系統。

<a id="id-1.7.5.20.7.8"></a>

## 另請參閱

[CONNECT](ecpg-sql-connect.md), [DECLARE](ecpg-sql-declare.md), [OPEN](ecpg-sql-open.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-declare-statement.html)（英文原文，待翻譯）
