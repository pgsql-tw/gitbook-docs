<a id="SQL-CREATEUSERMAPPING"></a><a id="id-1.9.3.96.1"></a>

## CREATE USER MAPPING

CREATE USER MAPPING — 定義使用者到外部伺服器的新對應

<a id="id-1.9.3.96.4"></a>

## 語法

```

CREATE USER MAPPING [ IF NOT EXISTS ] FOR { user_name | USER | CURRENT_ROLE | CURRENT_USER | PUBLIC }
    SERVER server_name
    [ OPTIONS ( option 'value' [ , ... ] ) ]
```

<a id="id-1.9.3.96.5"></a>

## 說明

`CREATE USER MAPPING` 會定義使用者到外部伺服器的對應。使用者對應通常封裝了連線資訊，外部資料包裝器會將這些資訊連同外部伺服器所封裝的資訊一起使用，以存取外部資料來源。

外部伺服器的擁有者可以為任何使用者建立該伺服器的使用者對應。此外，若使用者已被授予該伺服器的 `USAGE` 權限，該使用者也可以為自己的使用者名稱建立使用者對應。

<a id="id-1.9.3.96.6"></a>

## 參數

`IF NOT EXISTS`
:   若指定使用者到指定外部伺服器的對應已存在，則不擲出錯誤；此情況會發出 notice。請注意，並不保證現有的使用者對應與原本會建立的對應有任何相似之處。

*`user_name`*
:   對應到外部伺服器的現有使用者名稱。`CURRENT_ROLE`、`CURRENT_USER` 與 `USER` 均符合目前使用者的名稱。指定 `PUBLIC` 時，會建立所謂的公用對應，在沒有適用的使用者專屬對應時使用。

*`server_name`*
:   要為其建立使用者對應的現有伺服器名稱。

`OPTIONS ( option 'value' [, ... ] )`
:   此子句指定使用者對應的選項。這些選項通常定義該對應實際使用的使用者名稱與密碼。選項名稱必須是唯一的。允許的選項名稱與值，取決於該伺服器的外部資料包裝器。

<a id="id-1.9.3.96.7"></a>

## 範例

為使用者 `bob`、伺服器 `foo` 建立使用者對應：

```

CREATE USER MAPPING FOR bob SERVER foo OPTIONS (user 'bob', password 'secret');
```

<a id="id-1.9.3.96.8"></a>

## 相容性

`CREATE USER MAPPING` 符合 ISO/IEC 9075-9（SQL/MED）。

<a id="id-1.9.3.96.9"></a>

## 另請參閱

[ALTER USER MAPPING](sql-alterusermapping.md), [DROP USER MAPPING](sql-dropusermapping.md), [CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md), [CREATE SERVER](sql-createserver.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createusermapping.html)（原文版本：18.6；核對日期：2026-10-03）
