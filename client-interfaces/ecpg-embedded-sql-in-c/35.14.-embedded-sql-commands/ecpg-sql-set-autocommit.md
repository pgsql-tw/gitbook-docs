<a id="ECPG-SQL-SET-AUTOCOMMIT"></a>

# SET AUTOCOMMIT

SET AUTOCOMMIT — 設定目前工作階段的自動提交行為

## 語法

```

SET AUTOCOMMIT { = | TO } { ON | OFF }
```

<a id="id-1.7.5.20.14.3"></a>

## 說明

`SET AUTOCOMMIT` 設定目前資料庫工作階段的自動提交行為。預設情況下，嵌入式 SQL 程式<em>不會</em>處於自動提交模式，因此需要時必須明確發出 `COMMIT`。此命令可將工作階段切換為自動提交模式，讓每個個別陳述式隱含地提交。

<a id="id-1.7.5.20.14.4"></a>

## 相容性

`SET AUTOCOMMIT` 是 PostgreSQL ECPG 的擴充功能。

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-set-autocommit.html)
