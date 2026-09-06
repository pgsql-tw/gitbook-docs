<a id="id-1.9.3.143.1"></a>

## DROP USER

DROP USER — 移除資料庫角色

## 語法

```

DROP USER [ IF EXISTS ] name [, ...]
```

<a id="id-1.9.3.143.5"></a>

## 說明

`DROP USER` 只是 [`DROP ROLE`](sql-droprole.md) 的另一種寫法。

<a id="id-1.9.3.143.6"></a>

## 相容性

`DROP USER` 陳述式是 PostgreSQL 的擴充功能。SQL 標準將使用者的定義方式留給各實作決定。

<a id="id-1.9.3.143.7"></a>

## 另請參閱

[DROP ROLE](sql-droprole.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-dropuser.html)（原文版本：18.6；核對日期：2026-09-07）
