<a id="SQL-DROPTABLESPACE"></a><a id="id-1.9.3.135.1"></a>

## DROP TABLESPACE

DROP TABLESPACE — 移除資料表空間

<a id="id-1.9.3.135.4"></a>

## 語法

```

DROP TABLESPACE [ IF EXISTS ] name
```

<a id="id-1.9.3.135.5"></a>

## 說明

`DROP TABLESPACE` 會從系統中移除資料表空間。

資料表空間只能由其擁有者或超級使用者移除。
資料表空間必須清空所有資料庫物件後才能移除。即使目前資料庫中沒有任何物件正在使用該資料表空間，其他資料庫中的物件仍可能存放在該資料表空間中。此外，若該資料表空間列於任何作用中工作階段的 [temp_tablespaces](../../server-administration/runtime-config/runtime-config-client.md#GUC-TEMP-TABLESPACES) 設定中，`DROP` 可能因為存放在該資料表空間中的暫存檔而失敗。

<a id="id-1.9.3.135.6"></a>

## 參數

`IF EXISTS`
:   資料表空間不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   資料表空間的名稱。

<a id="id-1.9.3.135.7"></a>

## 注意事項

`DROP TABLESPACE` 不能在交易區塊內執行。

<a id="id-1.9.3.135.8"></a>

## 範例

若要從系統中移除資料表空間 `mystuff`：

```

DROP TABLESPACE mystuff;
```

<a id="id-1.9.3.135.9"></a>

## 相容性

`DROP TABLESPACE` 是 PostgreSQL 擴充功能。

<a id="id-1.9.3.135.10"></a>

## 另請參閱

[CREATE TABLESPACE](sql-createtablespace.md), [ALTER TABLESPACE](sql-altertablespace.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptablespace.html)（原文版本：18.6；核對日期：2026-10-03）
