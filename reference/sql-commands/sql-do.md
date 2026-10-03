<a id="SQL-DO"></a><a id="id-1.9.3.102.1"></a><a id="id-1.9.3.102.2"></a>

## DO

DO — 執行匿名程式碼區塊

<a id="id-1.9.3.102.5"></a>

## 語法

```

DO [ LANGUAGE lang_name ] code
```

<a id="id-1.9.3.102.6"></a>

## 說明

`DO` 會執行一個匿名程式碼區塊，換句話說，也就是以程序語言撰寫的一個暫時性匿名函式。

此程式碼區塊會被視為一個沒有參數、傳回 `void` 的函式主體來處理。它只會被剖析並執行一次。

選用的 `LANGUAGE` 子句可以寫在程式碼區塊之前或之後。

<a id="id-1.9.3.102.7"></a>

## 參數

*`code`*
:   要執行的程序語言程式碼。這必須指定為字串常數，就如同在 `CREATE FUNCTION` 中一樣。建議使用錢號引用的字串常數。

*`lang_name`*
:   撰寫該程式碼所用的程序語言名稱。若省略，預設為 `plpgsql`。

<a id="id-1.9.3.102.8"></a>

## 注意事項

要使用的程序語言必須已經透過 `CREATE EXTENSION` 安裝到目前的資料庫中。`plpgsql` 預設已安裝，但其他語言則沒有。

使用者必須擁有該程序語言的 `USAGE` 權限；若該語言是不受信任的語言，則必須是超級使用者。這與在該語言中建立函式的權限要求相同。

若 `DO` 是在交易區塊中執行，則該程序程式碼不能執行交易控制陳述式。只有當 `DO` 在其自身的交易中執行時，才允許使用交易控制陳述式。

<a id="SQL-DO-EXAMPLES"></a>

## 範例

將綱要 `public` 中所有檢視表的所有權限授予角色 `webuser`：

```

DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT table_schema, table_name FROM information_schema.tables
             WHERE table_type = 'VIEW' AND table_schema = 'public'
    LOOP
        EXECUTE 'GRANT ALL ON ' || quote_ident(r.table_schema) || '.' || quote_ident(r.table_name) || ' TO webuser';
    END LOOP;
END$$;
```

<a id="id-1.9.3.102.10"></a>

## 相容性

SQL 標準中沒有 `DO` 陳述式。

<a id="id-1.9.3.102.11"></a>

## 另請參閱

[CREATE LANGUAGE](sql-createlanguage.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-do.html)（原文版本：18.6；核對日期：2026-10-03）
