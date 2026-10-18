<a id="ECPG-SQL-PREPARE"></a>

## PREPARE

PREPARE — 準備陳述式以供執行

## 語法

```

PREPARE prepared_name FROM string
```

<a id="id-1.7.5.20.13.3"></a>

## 說明

`PREPARE` 會準備一個以字串動態指定的陳述式以供執行。這與直接 SQL 陳述式 [PREPARE](../../reference/sql-commands/sql-prepare.md) 不同，後者也可以在嵌入式程式中使用。兩種預備陳述式都是以 [EXECUTE](../../reference/sql-commands/sql-execute.md) 命令執行。

<a id="id-1.7.5.20.13.4"></a>

## 參數

<a id="ECPG-SQL-PREPARE-PREPARED-NAME"></a>

*`prepared_name`* [#](#ECPG-SQL-PREPARE-PREPARED-NAME)
:   預備查詢的識別字。
<a id="ECPG-SQL-PREPARE-STRING"></a>

*`string`* [#](#ECPG-SQL-PREPARE-STRING)
:   包含可預備之 SQL 陳述式（SELECT、INSERT、UPDATE 或 DELETE 其中之一）的字串常值或主機變數。要在執行時提供的參數值，請以問號（`?`）表示。

<a id="id-1.7.5.20.13.5"></a>

## 注意事項

一般使用時，*`string`* 是一個主機變數參照，指向包含動態建構之 SQL 陳述式的字串。使用字串常值的情況用處不大；你還不如就寫一個直接 SQL 的 `PREPARE` 陳述式。

若你確實使用字串常值，請記住，你可能想在 SQL 陳述式中加入的任何雙引號，都必須寫成八進位跳脫序列（`\042`），而不是一般 C 慣用的 `\"`。這是因為該字串位於 `EXEC SQL` 區段內，因此 ECPG 詞法分析器會依 SQL 規則而非 C 規則來剖析它。任何內嵌的反斜線稍後會依 C 規則處理；但 `\"` 會被視為常值的結尾，因而立即造成語法錯誤。

<a id="id-1.7.5.20.13.6"></a>

## 範例

```

char *stmt = "SELECT * FROM test1 WHERE a = ? AND b = ?";

EXEC SQL ALLOCATE DESCRIPTOR outdesc;
EXEC SQL PREPARE foo FROM :stmt;

EXEC SQL EXECUTE foo USING SQL DESCRIPTOR indesc INTO SQL DESCRIPTOR outdesc;
```

<a id="id-1.7.5.20.13.7"></a>

## 相容性

SQL 標準規定了 `PREPARE`。

<a id="id-1.7.5.20.13.8"></a>

## 另請參閱

[EXECUTE](../../reference/sql-commands/sql-execute.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-prepare.html)（原文版本：18.6；核對日期：2026-10-18）
