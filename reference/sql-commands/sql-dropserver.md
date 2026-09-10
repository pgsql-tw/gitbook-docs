<a id="id-1.9.3.131.1"></a>

## DROP SERVER

DROP SERVER — 移除外部伺服器描述器

## 語法

```

DROP SERVER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.131.5"></a>

## 說明

`DROP SERVER` 會移除現有外部伺服器描述器。若要執行此命令，目前使用者必須是該伺服器的擁有者。

<a id="id-1.9.3.131.6"></a>

## 參數

`IF EXISTS`
:   伺服器不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有伺服器名稱。

`CASCADE`
:   自動移除相依於伺服器的物件（例如使用者對應），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有物件相依於伺服器則拒絕移除。這是預設行為。

<a id="id-1.9.3.131.7"></a>

## 範例

若伺服器 `foo` 存在則移除它：

```

DROP SERVER IF EXISTS foo;
```

<a id="id-1.9.3.131.8"></a>

## 相容性

`DROP SERVER` 符合 ISO/IEC 9075-9（SQL/MED）。`IF EXISTS` 子句是 PostgreSQL 擴充功能。

<a id="id-1.9.3.131.9"></a>

## 另請參閱

[CREATE SERVER](sql-createserver.md), [ALTER SERVER](sql-alterserver.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropserver.html)（原文版本：18.6；核對日期：2026-09-11）
