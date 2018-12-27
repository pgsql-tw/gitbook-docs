---
description: 版本：11
---

# SHOW

SHOW — 顯示執行時期參數的值

### 語法

```text
SHOW name
SHOW ALL
```

### 說明

SHOW 將顯示執行時期參數的目前設定。可以使用 SET 語句、編輯postgresql.conf 組態檔案、透過 PGOPTIONS 環境變數（使用 libpq 或基於 libpq 的應用程式）或啟動 postgres 伺服器時以命令列選項來設定這些變數。詳細訊息請參閱[第 19 章](../../server-administration/server-configuration/)。

### 參數

_`name`_

執行時期參數的名稱。可用參數列在[第 19 章](../../server-administration/server-configuration/)和 [SET](set.md) 參考頁面中。此外，還有一些參數可以顯示但不能設定：

`SERVER_VERSION`

顯示伺服器的版本號碼。

`SERVER_ENCODING`

顯示伺服器端字元集編碼。目前，此參數可以顯示但不能設定，因為編碼是在資料庫建立時決定的。

`LC_COLLATE`

顯示資料庫的 collation 設定（文字排序方式）。目前，此參數可以顯示但不能設定，因為此設定是在資料庫建立時決定的。

`LC_CTYPE`

顯示資料庫的字元分類區域設定。目前，此參數可以顯示但不能設定，因為此設定是在資料庫建立時決定的。

`IS_SUPERUSER`

如果目前角色具有超級使用者權限，則為 True。

`ALL`

顯示所有組態參數的值和說明。

### 注意

函數 current\_setting 可以產生相同的輸出；詳見 [9.26 節](../../the-sql-language/functions-and-operators/system-administration.md)。此外， [pg\_settings ](../../internals/system-catalogs/pg_settings.md)系統檢視表也產出相同的資訊。

### 範例

顯示參數 DateStyle 目前的設定：

```text
SHOW DateStyle;
 DateStyle
-----------
 ISO, MDY
(1 row)
```

顯示參數 geqo 目前的設定：

```text
SHOW geqo;
 geqo
------
 on
(1 row)
```

顯示所有設定：

```text
SHOW ALL;
            name         | setting |                description                                                          
-------------------------+---------+-------------------------------------------------
 allow_system_table_mods | off     | Allows modifications of the structure of ...
    .
    .
    .
 xmloption               | content | Sets whether XML data in implicit parsing ...
 zero_damaged_pages      | off     | Continues processing past damaged page headers.
(196 rows)
```

### 相容性

SHOW 指令是 PostgreSQL 的延伸功能。

### 參閱

[SET](set.md), [RESET](reset.md)

