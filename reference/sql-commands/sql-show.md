<a id="id-1.9.3.179.1"></a>

## SHOW

SHOW — 顯示執行期參數的值

## 語法

```

SHOW name
SHOW ALL
```

<a id="id-1.9.3.179.5"></a>

## 說明

`SHOW` 會顯示執行期參數目前的設定值。這些變數可以透過
`SET` 陳述式設定，也可以編輯 `postgresql.conf`
組態檔、透過 `PGOPTIONS` 環境變數
（當使用 libpq 或以 libpq
為基礎的應用程式時）設定，或是在啟動 `postgres`
伺服器時透過命令列旗標設定。詳情請參閱[第 19 章](../../server-administration/runtime-config/README.md)。

<a id="id-1.9.3.179.6"></a>

## 參數

*`name`*
:   執行期參數的名稱。可用的參數記載於[第 19 章](../../server-administration/runtime-config/README.md)以及[SET](sql-set.md)參考頁面中。
    此外，還有少數幾個參數只能顯示、不能設定：

    `SERVER_VERSION`
    :   顯示伺服器的版本號碼。

    `SERVER_ENCODING`
    :   顯示伺服器端的字元集編碼。目前這個參數只能顯示、不能設定，
        因為編碼是在建立資料庫時就決定的。

    `IS_SUPERUSER`
    :   若目前角色具有超級使用者權限，則為真。

`ALL`
:   顯示所有組態參數的值，並附上說明。

<a id="id-1.9.3.179.7"></a>

## 注意事項

函式 `current_setting` 會產生相同的輸出；請參閱
[9.28.1 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SET)。
此外，
[`pg_settings`](../../internals/views/view-pg-settings.md)
系統檢視表也會產生相同的資訊。

<a id="id-1.9.3.179.8"></a>

## 範例

顯示參數 `DateStyle` 目前的設定：

```

SHOW DateStyle;
 DateStyle
-----------
 ISO, MDY
(1 row)
```

顯示參數 `geqo` 目前的設定：

```

SHOW geqo;
 geqo
------
 on
(1 row)
```

顯示所有設定：

```

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

<a id="id-1.9.3.179.9"></a>

## 相容性

`SHOW` 命令是 PostgreSQL 的擴充功能。

<a id="id-1.9.3.179.10"></a>

## 另請參閱

[SET](sql-set.md)、[RESET](sql-reset.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-show.html)（原文版本：18.6；核對日期：2026-09-28）
