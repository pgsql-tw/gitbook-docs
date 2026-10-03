<a id="SQL-DROPTRANSFORM"></a><a id="id-1.9.3.140.1"></a>

## DROP TRANSFORM

DROP TRANSFORM — 移除轉換

<a id="id-1.9.3.140.4"></a>

## 語法

```

DROP TRANSFORM [ IF EXISTS ] FOR type_name LANGUAGE lang_name [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPTRANSFORM-DESCRIPTION"></a>

## 說明

`DROP TRANSFORM` 會移除先前定義的轉換（transform）。

要能移除轉換，您必須擁有該型別與該語言。這與建立轉換所需的權限相同。

<a id="id-1.9.3.140.6"></a>

## 參數

`IF EXISTS`
:   轉換不存在時不擲出錯誤；此情況會發出 notice。

*`type_name`*
:   轉換的資料型別名稱。

*`lang_name`*
:   轉換的語言名稱。

`CASCADE`
:   自動移除相依於轉換的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於轉換則拒絕移除。這是預設行為。

<a id="SQL-DROPTRANSFORM-EXAMPLES"></a>

## 範例

若要移除型別 `hstore` 與語言 `plpython3u` 的轉換：

```

DROP TRANSFORM FOR hstore LANGUAGE plpython3u;
```

<a id="SQL-DROPTRANSFORM-COMPAT"></a>

## 相容性

這種形式的 `DROP TRANSFORM` 是 PostgreSQL 擴充功能。詳細資訊請參閱 [CREATE TRANSFORM](sql-createtransform.md)。

<a id="id-1.9.3.140.9"></a>

## 另請參閱

[CREATE TRANSFORM](sql-createtransform.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptransform.html)（原文版本：18.6；核對日期：2026-10-03）
