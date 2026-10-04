<a id="SQL-CREATESERVER"></a><a id="id-1.9.3.82.1"></a>

## CREATE SERVER

CREATE SERVER — 定義新的外部伺服器

<a id="id-1.9.3.82.4"></a>

## 語法

```

CREATE SERVER [ IF NOT EXISTS ] server_name [ TYPE 'server_type' ] [ VERSION 'server_version' ]
    FOREIGN DATA WRAPPER fdw_name
    [ OPTIONS ( option 'value' [, ... ] ) ]
```

<a id="id-1.9.3.82.5"></a>

## 說明

`CREATE SERVER` 會定義一個新的外部伺服器。定義該伺服器的使用者會成為其擁有者。

外部伺服器通常封裝了外部資料包裝器用來存取外部資料資源的連線資訊。額外的使用者特定連線資訊可以透過使用者對應來指定。

伺服器名稱在資料庫內必須是唯一的。

建立伺服器需要所使用之外部資料包裝器的 `USAGE` 權限。

<a id="id-1.9.3.82.6"></a>

## 參數

`IF NOT EXISTS`
:   若已存在同名的伺服器，不擲出錯誤；此情況會發出 notice。請注意，不保證現有的伺服器與原本要建立的伺服器有任何相似之處。

*`server_name`*
:   要建立的外部伺服器名稱。

*`server_type`*
:   選用的伺服器類型，可能對外部資料包裝器有用。

*`server_version`*
:   選用的伺服器版本，可能對外部資料包裝器有用。

*`fdw_name`*
:   管理該伺服器的外部資料包裝器名稱。

`OPTIONS ( option 'value' [, ... ] )`
:   此子句指定伺服器的選項。這些選項通常定義伺服器的連線細節，但實際的名稱與值取決於該伺服器的外部資料包裝器。

<a id="id-1.9.3.82.7"></a>

## 注意事項

使用 [dblink](../../appendixes/contrib/dblink.md) 模組時，外部伺服器的名稱可以作為 [dblink_connect](../../appendixes/contrib/contrib-dblink-connect.md) 函式的引數，用來指示連線參數。要以這種方式使用外部伺服器，必須擁有該外部伺服器的 `USAGE` 權限。

若外部伺服器支援排序下推（sort pushdown），它必須與本地伺服器具有相同的排序順序。

<a id="id-1.9.3.82.8"></a>

## 範例

建立一個使用外部資料包裝器 `postgres_fdw` 的伺服器 `myserver`：

```

CREATE SERVER myserver FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'foo', dbname 'foodb', port '5432');
```

更多細節請參閱 [postgres_fdw](../../appendixes/contrib/postgres-fdw.md)。

<a id="id-1.9.3.82.9"></a>

## 相容性

`CREATE SERVER` 符合 ISO/IEC 9075-9（SQL/MED）。

<a id="id-1.9.3.82.10"></a>

## 另請參閱

[ALTER SERVER](sql-alterserver.md), [DROP SERVER](sql-dropserver.md), [CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md), [CREATE FOREIGN TABLE](sql-createforeigntable.md), [CREATE USER MAPPING](sql-createusermapping.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createserver.html)（原文版本：18.6；核對日期：2026-10-04）
