## DESCRIBE

DESCRIBE — 取得備妥陳述式或結果集的資訊

## 語法

```

DESCRIBE [ OUTPUT ] prepared_name USING [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO sqlda_name
```

<a id="id-1.7.5.20.8.3"></a>

## 說明

`DESCRIBE` 取得備妥陳述式所含結果欄位的中繼資料資訊，而不會實際擷取資料列。

<a id="id-1.7.5.20.8.4"></a>

## 參數

<a id="ECPG-SQL-DESCRIBE-PREPARED-NAME"></a>

*`prepared_name`* [#](#ECPG-SQL-DESCRIBE-PREPARED-NAME)
:   備妥陳述式的名稱。可以是 SQL 識別字或主機變數。
<a id="ECPG-SQL-DESCRIBE-DESCRIPTOR-NAME"></a>

*`descriptor_name`* [#](#ECPG-SQL-DESCRIBE-DESCRIPTOR-NAME)
:   描述區名稱，區分大小寫。可以是 SQL 識別字或主機變數。
<a id="ECPG-SQL-DESCRIBE-SQLDA-NAME"></a>

*`sqlda_name`* [#](#ECPG-SQL-DESCRIBE-SQLDA-NAME)
:   SQLDA 變數名稱。

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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-describe.html)（英文原文，待翻譯）
