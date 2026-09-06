<a id="ECPG-SQL-ALLOCATE-DESCRIPTOR"></a>

# ALLOCATE DESCRIPTOR

ALLOCATE DESCRIPTOR — 配置 SQL 描述區

## 語法

```

ALLOCATE DESCRIPTOR name
```

<a id="id-1.7.5.20.3.3"></a>

## 說明

`ALLOCATE DESCRIPTOR` 配置新的具名 SQL 描述區，可用於 PostgreSQL 伺服器與主機程式之間交換資料。

使用完畢後，應使用 `DEALLOCATE DESCRIPTOR` 命令釋放描述區。

<a id="id-1.7.5.20.3.4"></a>

## 參數

<em class="replaceable"><code>name</code></em>

SQL 描述區的名稱，區分大小寫。可以是 SQL 識別字或主機變數。

<a id="id-1.7.5.20.3.5"></a>

## 範例

```

EXEC SQL ALLOCATE DESCRIPTOR mydesc;
```

<a id="id-1.7.5.20.3.6"></a>

## 相容性

SQL 標準規定了 `ALLOCATE DESCRIPTOR`。

<a id="id-1.7.5.20.3.7"></a>

## 另請參閱

[DEALLOCATE DESCRIPTOR](ecpg-sql-deallocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md), [SET DESCRIPTOR](ecpg-sql-set-descriptor.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-allocate-descriptor.html)
