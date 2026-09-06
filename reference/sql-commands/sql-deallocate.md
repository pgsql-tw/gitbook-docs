<a id="id-1.9.3.98.1"></a><a id="id-1.9.3.98.2"></a>

## DEALLOCATE

DEALLOCATE — 釋放預備陳述式

## 語法

```

DEALLOCATE [ PREPARE ] { name | ALL }
```

<a id="id-1.9.3.98.6"></a>

## 說明

`DEALLOCATE` 用來釋放先前準備的 SQL 陳述式。若未明確釋放預備陳述式，它會在工作階段結束時釋放。

預備陳述式的更多資訊，請參閱 [PREPARE](sql-prepare.md)。

<a id="id-1.9.3.98.7"></a>

## 參數

`PREPARE`
:   此關鍵字會被忽略。

*`name`*
:   要釋放的預備陳述式名稱。

`ALL`
:   釋放所有預備陳述式。

<a id="id-1.9.3.98.8"></a>

## 相容性

SQL 標準包含 `DEALLOCATE` 陳述式，但僅供嵌入式 SQL 使用。

<a id="id-1.9.3.98.9"></a>

## 另請參閱

[EXECUTE](sql-execute.md), [PREPARE](sql-prepare.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-deallocate.html)（原文版本：18.6；核對日期：2026-09-07）
