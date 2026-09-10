<a id="id-1.9.3.110.1"></a>

## DROP EVENT TRIGGER

DROP EVENT TRIGGER — 移除事件觸發器

## 語法

```

DROP EVENT TRIGGER [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.110.5"></a>

## 說明

`DROP EVENT TRIGGER` 會移除現有事件觸發器。若要執行此命令，目前使用者必須是事件觸發器擁有者。

<a id="id-1.9.3.110.6"></a>

## 參數

`IF EXISTS`
:   事件觸發器不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   要移除的事件觸發器名稱。

`CASCADE`
:   自動移除相依於觸發器的物件，以及相依於這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有物件相依於觸發器則拒絕移除。這是預設行為。

<a id="SQL-DROPEVENTTRIGGER-EXAMPLES"></a>

## 範例

移除觸發器 `snitch`：

```

DROP EVENT TRIGGER snitch;
```

<a id="SQL-DROPEVENTTRIGGER-COMPATIBILITY"></a>

## 相容性

SQL 標準中沒有 `DROP EVENT TRIGGER` 陳述式。

<a id="id-1.9.3.110.9"></a>

## 另請參閱

[CREATE EVENT TRIGGER](sql-createeventtrigger.md), [ALTER EVENT TRIGGER](sql-altereventtrigger.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropeventtrigger.html)（原文版本：18.6；核對日期：2026-09-11）
