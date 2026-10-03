<a id="SQL-DROPDATABASE"></a><a id="id-1.9.3.108.1"></a>

## DROP DATABASE

DROP DATABASE — 移除資料庫

<a id="id-1.9.3.108.4"></a>

## 語法

```

DROP DATABASE [ IF EXISTS ] name [ [ WITH ] ( option [, ...] ) ]

where option can be:

    FORCE
```

<a id="id-1.9.3.108.5"></a>

## 說明

`DROP DATABASE` 會移除資料庫。它會移除該資料庫的系統目錄項目，並刪除存放資料的目錄。此命令只能由資料庫擁有者執行。當您連線到目標資料庫時，無法執行此命令。（請連線到 `postgres` 或任何其他資料庫來下達此命令。）此外，若有其他任何人連線到目標資料庫，除非您使用下文所述的 `FORCE` 選項，否則此命令將會失敗。

`DROP DATABASE` 無法復原。請謹慎使用！

<a id="id-1.9.3.108.6"></a>

## 參數

`IF EXISTS`
:   資料庫不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除的資料庫名稱。

`FORCE`
:   嘗試終止所有連到目標資料庫的現有連線。
    若目標資料庫中存在已準備交易、作用中的邏輯複寫插槽或訂閱，則不會終止連線。

    這會終止背景工作程序的連線，以及目前使用者有權限以
    `pg_terminate_backend` 終止的連線；該函式說明於
    [第 9.28.2 節](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)。若仍有連線殘留，
    此命令將會失敗。

<a id="id-1.9.3.108.7"></a>

## 注意事項

`DROP DATABASE` 不能在交易區塊內執行。

連線到目標資料庫時無法執行此命令。因此，改用 [dropdb](../reference-client/app-dropdb.md) 程式可能會更方便，它是包裝此命令的程式。

<a id="id-1.9.3.108.8"></a>

## 相容性

SQL 標準中沒有 `DROP DATABASE` 陳述式。

<a id="id-1.9.3.108.9"></a>

## 另請參閱

[CREATE DATABASE](sql-createdatabase.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropdatabase.html)（原文版本：18.6；核對日期：2026-10-03）
