<a id="id-1.9.3.107.1"></a>

## DROP CONVERSION

DROP CONVERSION — 移除轉換

## 語法

```

DROP CONVERSION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPCONVERSION-DESCRIPTION"></a>

## 說明

`DROP CONVERSION` 會移除先前定義的轉換。若要移除轉換，你必須擁有該轉換。

<a id="id-1.9.3.107.6"></a>

## 參數

`IF EXISTS`
:   轉換不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   轉換名稱。轉換名稱可使用 schema 限定。

`CASCADE`<br>`RESTRICT`
:   這些關鍵字沒有作用，因為轉換沒有相依性。

<a id="SQL-DROPCONVERSION-EXAMPLES"></a>

## 範例

若要移除名為 `myname` 的轉換：

```

DROP CONVERSION myname;
```

<a id="SQL-DROPCONVERSION-COMPAT"></a>

## 相容性

SQL 標準中沒有 `DROP CONVERSION` 陳述式，但有與 `CREATE TRANSLATION` 陳述式搭配的 `DROP TRANSLATION` 陳述式；它類似 PostgreSQL 的 `CREATE CONVERSION` 陳述式。

<a id="id-1.9.3.107.9"></a>

## 另請參閱

[ALTER CONVERSION](sql-alterconversion.md), [CREATE CONVERSION](sql-createconversion.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropconversion.html)（原文版本：18.6；核對日期：2026-09-11）
