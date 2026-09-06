## DEALLOCATE DESCRIPTOR

DEALLOCATE DESCRIPTOR — 釋放 SQL 描述區

## 語法

```

DEALLOCATE DESCRIPTOR name
```

<a id="id-1.7.5.20.5.3"></a>

## 說明

`DEALLOCATE DESCRIPTOR` 釋放具名 SQL 描述區。

<a id="id-1.7.5.20.5.4"></a>

## 參數

<a id="ECPG-SQL-DEALLOCATE-DESCRIPTOR-NAME"></a>

*`name`* [#](#ECPG-SQL-DEALLOCATE-DESCRIPTOR-NAME)
:   即將釋放的描述區名稱。此名稱區分大小寫，可以是 SQL 識別字或主機變數。

<a id="id-1.7.5.20.5.5"></a>

## 範例

```

EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

<a id="id-1.7.5.20.5.6"></a>

## 相容性

SQL 標準規定了 `DEALLOCATE DESCRIPTOR`。

<a id="id-1.7.5.20.5.7"></a>

## 另請參閱

[ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md), [SET DESCRIPTOR](ecpg-sql-set-descriptor.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-deallocate-descriptor.html)（英文原文，待翻譯）
