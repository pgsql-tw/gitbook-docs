---
description: 版本：11
---

# DO

DO — 執行匿名的程式區塊

### 語法

```text
DO [ LANGUAGE lang_name ] code
```

### 說明

DO 執行匿名的程式區塊，換句話說，在程序語言中執行短暫的匿名函數。

程式區塊被視為沒有參數的函數，回傳 void。它被解譯並只執行一次。

可以在程式區塊之前或之後寫入選擇性的 LANGUAGE 子句。

### 參數

_`code`_

要執行的程序語言程式。必須將其指定為字串，就像在 CREATE FUNCTION 中一樣。建議使用錢字號引用的文字。

_`lang_name`_

程式碼的程序語言名稱。如果省略，則預設為 plpgsql。

### 注意

要使用的程序語言必須已透過 CREATE LANGUAGE 安裝到目前資料庫中。plpgsql 預設會安裝，但其他語言則沒有。

使用者必須具有程序語言的 USAGE 權限，如果語言是 untrusted，則必須是超級使用者。這與在語言中建立函數的權限要求相同。

### 範例

將綱要 public 中所有檢視表的所有權限授予角色webuser：

```text
DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT table_schema, table_name FROM information_schema.tables
             WHERE table_type = 'VIEW' AND table_schema = 'public'
    LOOP
        EXECUTE 'GRANT ALL ON ' || quote_ident(r.table_schema) || '.' || quote_ident(r.table_name) || ' TO webuser';
    END LOOP;
END$$;
```

### 相容性

SQL 標準中沒有 DO 語句。

### 參閱

[CREATE LANGUAGE](create-language.md)

