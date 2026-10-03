<a id="SQL-DROPEXTENSION"></a><a id="id-1.9.3.111.1"></a>

## DROP EXTENSION

DROP EXTENSION — 移除擴充功能

<a id="id-1.9.3.111.4"></a>

## 語法

```

DROP EXTENSION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.111.5"></a>

## 說明

`DROP EXTENSION` 會從資料庫中移除擴充功能。移除擴充功能時，它的成員物件以及其他明確相依於它的常式（請參閱 [ALTER ROUTINE](sql-alterroutine.md) 的 `DEPENDS ON EXTENSION extension_name` 動作）也會一併被移除。

您必須擁有該擴充功能才能使用 `DROP EXTENSION`。

<a id="id-1.9.3.111.6"></a>

## 參數

`IF EXISTS`
:   擴充功能不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   已安裝擴充功能的名稱。

`CASCADE`
:   自動移除相依於擴充功能的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若除了這些擴充功能本身、其成員物件以及明確相依於它們的常式之外，還有其他物件相依於它們，此選項會阻止移除指定的擴充功能。這是預設行為。

<a id="id-1.9.3.111.7"></a>

## 範例

若要從目前的資料庫中移除擴充功能 `hstore`：

```

DROP EXTENSION hstore;
```

若資料庫中有任何 `hstore` 的物件正在使用中，例如有任何資料表含有 `hstore` 型別的欄位，此命令就會失敗。加上 `CASCADE` 選項即可將這些相依物件也一併強制移除。

<a id="id-1.9.3.111.8"></a>

## 相容性

`DROP EXTENSION` 是 PostgreSQL 對 SQL 標準的擴充語法。

<a id="id-1.9.3.111.9"></a>

## 另請參閱

[CREATE EXTENSION](sql-createextension.md), [ALTER EXTENSION](sql-alterextension.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropextension.html)（原文版本：18.6；核對日期：2026-10-03）
