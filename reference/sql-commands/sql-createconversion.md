<a id="SQL-CREATECONVERSION"></a><a id="id-1.9.3.60.1"></a>

## CREATE CONVERSION

CREATE CONVERSION — 定義新的編碼轉換

<a id="id-1.9.3.60.4"></a>

## 語法

```

CREATE [ DEFAULT ] CONVERSION name
    FOR source_encoding TO dest_encoding FROM function_name
```

<a id="SQL-CREATECONVERSION-DESCRIPTION"></a>

## 說明

`CREATE CONVERSION` 會定義兩種字元集編碼之間的新轉換。

標記為 `DEFAULT` 的轉換可用於用戶端與伺服器之間的自動編碼轉換。為了支援這種用法，必須定義兩個轉換：從編碼 A 到 B，*以及*從編碼 B 到 A。

要建立轉換，你必須擁有該函式的 `EXECUTE` 權限，以及目的綱要的 `CREATE` 權限。

<a id="id-1.9.3.60.6"></a>

## 參數

`DEFAULT`
:   `DEFAULT` 子句表示此轉換是這組特定來源編碼到目的編碼的預設轉換。在一個綱要中，同一組編碼配對應該只有一個預設轉換。

*`name`*
:   轉換的名稱。轉換名稱可以用綱要限定。若未以綱要限定，轉換會定義在目前的綱要中。轉換名稱在綱要內必須是唯一的。

*`source_encoding`*
:   來源編碼名稱。

*`dest_encoding`*
:   目的編碼名稱。

*`function_name`*
:   用來執行轉換的函式。函式名稱可以用綱要限定。若未以綱要限定，則會在搜尋路徑中查找該函式。

    此函式必須具有下列簽章：

    ```

    conv_proc(
        integer,  -- source encoding ID
        integer,  -- destination encoding ID
        cstring,  -- source string (null terminated C string)
        internal, -- destination (fill with a null terminated C string)
        integer,  -- source string length
        boolean   -- if true, don't throw an error if conversion fails
    ) RETURNS integer;
    ```

    傳回值是成功轉換的來源位元組數。若最後一個引數為 false，函式必須在輸入無效時擲出錯誤，且傳回值一律等於來源字串長度。

<a id="SQL-CREATECONVERSION-NOTES"></a>

## 注意事項

來源編碼與目的編碼都不能是 `SQL_ASCII`，因為伺服器在涉及 `SQL_ASCII`「編碼」之情況下的行為是寫死在程式中的。

請使用 `DROP CONVERSION` 移除使用者定義的轉換。

建立轉換所需的權限可能會在未來的版本中變更。

<a id="SQL-CREATECONVERSION-EXAMPLES"></a>

## 範例

使用 `myfunc` 建立從編碼 `UTF8` 到 `LATIN1` 的轉換：

```

CREATE CONVERSION myconv FOR 'UTF8' TO 'LATIN1' FROM myfunc;
```

<a id="SQL-CREATECONVERSION-COMPAT"></a>

## 相容性

`CREATE CONVERSION` 是 PostgreSQL 的擴充語法。SQL 標準中沒有 `CREATE CONVERSION` 陳述式，但有一個在用途與語法上都非常相似的 `CREATE TRANSLATION` 陳述式。

<a id="SQL-CREATECONVERSION-SEEALSO"></a>

## 另請參閱

[ALTER CONVERSION](sql-alterconversion.md), [CREATE FUNCTION](sql-createfunction.md), [DROP CONVERSION](sql-dropconversion.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createconversion.html)（原文版本：18.6；核對日期：2026-10-04）
