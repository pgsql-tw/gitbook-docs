<a id="id-1.9.3.105.1"></a>

## DROP CAST

DROP CAST — 移除型別轉換

## 語法

```

DROP CAST [ IF EXISTS ] (source_type AS target_type) [ CASCADE | RESTRICT ]
```

<a id="SQL-DROPCAST-DESCRIPTION"></a>

## 說明

`DROP CAST` 會移除先前定義的型別轉換。

若要移除型別轉換，你必須擁有來源或目標資料型別。這與建立型別轉換所需的權限相同。

<a id="id-1.9.3.105.6"></a>

## 參數

`IF EXISTS`
:   型別轉換不存在時不會擲出錯誤；此情況會發出 notice。

*`source_type`*
:   型別轉換的來源資料型別名稱。

*`target_type`*
:   型別轉換的目標資料型別名稱。

`CASCADE`<br>`RESTRICT`
:   這些關鍵字沒有作用，因為型別轉換沒有相依性。

<a id="SQL-DROPCAST-EXAMPLES"></a>

## 範例

若要移除從型別 `text` 到型別 `int` 的型別轉換：

```

DROP CAST (text AS int);
```

<a id="SQL-DROPCAST-COMPAT"></a>

## 相容性

`DROP CAST` 命令符合 SQL 標準。

<a id="id-1.9.3.105.9"></a>

## 另請參閱

[CREATE CAST](sql-createcast.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropcast.html)（原文版本：18.6；核對日期：2026-09-10）
