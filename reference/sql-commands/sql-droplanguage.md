<a id="SQL-DROPLANGUAGE"></a><a id="id-1.9.3.117.1"></a>

## DROP LANGUAGE

DROP LANGUAGE — 移除程序語言

<a id="id-1.9.3.117.4"></a>

## 語法

```

DROP [ PROCEDURAL ] LANGUAGE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.117.5"></a>

## 說明

`DROP LANGUAGE` 會移除先前註冊之程序語言的定義。你必須是超級使用者或該語言的擁有者，才能使用 `DROP LANGUAGE`。

### 注意

自 PostgreSQL 9.1 起，大多數程序語言都已改為「擴充功能」，因此應該使用 [`DROP EXTENSION`](sql-dropextension.md) 而非 `DROP LANGUAGE` 來移除。

<a id="id-1.9.3.117.6"></a>

## 參數

`IF EXISTS`
:   語言不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有程序語言的名稱。

`CASCADE`
:   自動移除相依於該語言的物件（例如以該語言撰寫的函式），以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於該語言則拒絕移除。這是預設行為。

<a id="id-1.9.3.117.7"></a>

## 範例

此命令會移除程序語言 `plsample`：

```

DROP LANGUAGE plsample;
```

<a id="id-1.9.3.117.8"></a>

## 相容性

SQL 標準中沒有 `DROP LANGUAGE` 陳述式。

<a id="id-1.9.3.117.9"></a>

## 另請參閱

[ALTER LANGUAGE](sql-alterlanguage.md), [CREATE LANGUAGE](sql-createlanguage.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droplanguage.html)（原文版本：18.6；核對日期：2026-10-03）
