<a id="SQL-DROPUSERMAPPING"></a><a id="id-1.9.3.144.1"></a>

## DROP USER MAPPING

DROP USER MAPPING — 移除外部伺服器的使用者對應

<a id="id-1.9.3.144.4"></a>

## 語法

```

DROP USER MAPPING [ IF EXISTS ] FOR { user_name | USER | CURRENT_ROLE | CURRENT_USER | PUBLIC } SERVER server_name
```

<a id="id-1.9.3.144.5"></a>

## 說明

`DROP USER MAPPING` 會從外部伺服器移除現有的使用者對應。

外部伺服器的擁有者可以為任何使用者移除該伺服器的使用者對應。此外，若使用者已被授予該伺服器的 `USAGE` 權限，則該使用者可以移除其自身使用者名稱的使用者對應。

<a id="id-1.9.3.144.6"></a>

## 參數

`IF EXISTS`
:   使用者對應不存在時不擲出錯誤；此情況會發出 notice。

*`user_name`*
:   該對應的使用者名稱。`CURRENT_ROLE`、`CURRENT_USER`
    與 `USER` 會比對目前使用者的名稱。`PUBLIC` 用來比對系統中所有現有及未來的使用者名稱。

*`server_name`*
:   該使用者對應的伺服器名稱。

<a id="id-1.9.3.144.7"></a>

## 範例

若存在，則移除伺服器 `foo` 上的使用者對應 `bob`：

```

DROP USER MAPPING IF EXISTS FOR bob SERVER foo;
```

<a id="id-1.9.3.144.8"></a>

## 相容性

`DROP USER MAPPING` 符合 ISO/IEC 9075-9
（SQL/MED）。`IF EXISTS` 子句是 PostgreSQL 擴充功能。

<a id="id-1.9.3.144.9"></a>

## 另請參閱

[CREATE USER MAPPING](sql-createusermapping.md), [ALTER USER MAPPING](sql-alterusermapping.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropusermapping.html)（原文版本：18.6；核對日期：2026-10-03）
