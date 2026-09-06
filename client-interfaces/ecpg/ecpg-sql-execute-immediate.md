## EXECUTE IMMEDIATE

EXECUTE IMMEDIATE — 動態備妥並執行陳述式

## 語法

```

EXECUTE IMMEDIATE string
```

<a id="id-1.7.5.20.10.3"></a>

## 說明

`EXECUTE IMMEDIATE` 立即備妥並執行動態指定的 SQL 陳述式，但不擷取結果資料列。

<a id="id-1.7.5.20.10.4"></a>

## 參數

<a id="ECPG-SQL-EXECUTE-IMMEDIATE-STRING"></a>

*`string`* [#](#ECPG-SQL-EXECUTE-IMMEDIATE-STRING)
:   包含要執行 SQL 陳述式的字串常值或主機變數。

<a id="id-1.7.5.20.10.5"></a>

## 注意事項

一般使用時，*`string`* 是指向含有動態建構 SQL 陳述式之字串的主機變數參照。字串常值的情況用途不大；不如直接寫 SQL 陳述式，無須額外輸入 `EXECUTE IMMEDIATE`。

若確實使用字串常值，請注意想在 SQL 陳述式中加入的任何雙引號，都必須寫成八進位跳脫字元（`\042`），而不是一般 C 慣用的 `\"`。這是因為該字串位於 `EXEC SQL` 區段內，ECPG 詞法分析器會依 SQL 規則而非 C 規則解析它。任何內嵌反斜線稍後仍會依 C 規則處理；但 `\"` 會被視為結束常值，立即造成語法錯誤。

<a id="id-1.7.5.20.10.6"></a>

## 範例

以下範例使用 `EXECUTE IMMEDIATE` 及名為 `command` 的主機變數執行 `INSERT` 陳述式：

```

sprintf(command, "INSERT INTO test (name, amount, letter) VALUES ('db: ''r1''', 1, 'f')");
EXEC SQL EXECUTE IMMEDIATE :command;
```

<a id="id-1.7.5.20.10.7"></a>

## 相容性

SQL 標準規定了 `EXECUTE IMMEDIATE`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-execute-immediate.html)（英文原文，待翻譯）
