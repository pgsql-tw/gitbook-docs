<a id="ECPG-SQL-DESCRIBE"></a>

## DESCRIBE

DESCRIBE — 取得預備陳述式或結果集的相關資訊

## 語法

```

DESCRIBE [ OUTPUT ] prepared_name USING [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO sqlda_name
```

<a id="id-1.7.5.20.8.3"></a>

## 說明

`DESCRIBE` 會取得預備陳述式所含結果欄位的中繼資料資訊，而不實際擷取任何資料列。

<a id="id-1.7.5.20.8.4"></a>

## 參數

<a id="ECPG-SQL-DESCRIBE-PREPARED-NAME"></a>

### *`prepared_name`* [#](#ecpg-sql-describe-prepared-name) <a href="#ecpg-sql-describe-prepared-name" id="ecpg-sql-describe-prepared-name"></a>

預備陳述式的名稱。可以是 SQL 識別字或主機變數。

<a id="ECPG-SQL-DESCRIBE-DESCRIPTOR-NAME"></a>

### *`descriptor_name`* [#](#ecpg-sql-describe-descriptor-name) <a href="#ecpg-sql-describe-descriptor-name" id="ecpg-sql-describe-descriptor-name"></a>

描述區名稱。區分大小寫。可以是 SQL 識別字或主機變數。

<a id="ECPG-SQL-DESCRIBE-SQLDA-NAME"></a>

### *`sqlda_name`* [#](#ecpg-sql-describe-sqlda-name) <a href="#ecpg-sql-describe-sqlda-name" id="ecpg-sql-describe-sqlda-name"></a>

SQLDA 變數的名稱。

<a id="id-1.7.5.20.8.5"></a>

## 範例

```

EXEC SQL ALLOCATE DESCRIPTOR mydesc;
EXEC SQL PREPARE stmt1 FROM :sql_stmt;
EXEC SQL DESCRIBE stmt1 INTO SQL DESCRIPTOR mydesc;
EXEC SQL GET DESCRIPTOR mydesc VALUE 1 :charvar = NAME;
EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

<a id="id-1.7.5.20.8.6"></a>

## 相容性

SQL 標準規定了 `DESCRIBE`。

<a id="id-1.7.5.20.8.7"></a>

## 另請參閱

[ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-describe.html)（原文版本：18.6；核對日期：2026-10-18）
