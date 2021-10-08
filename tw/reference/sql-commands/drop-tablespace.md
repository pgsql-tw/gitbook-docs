# DROP TABLESPACE

DROP TABLESPACE — 移除一個資料表空間

## 語法

```text
DROP TABLESPACE [ IF EXISTS ] name
```

## 說明

DROP TABLESPACE 從系統中移除資料表空間。

資料表空間只能由其所有者或超級使用者移除。資料表空間在移除之前必須清空所有的資料庫物件。即使目前資料庫中沒有物件正在使用資料表空間，其他資料庫中的物件仍可能仍駐留在資料表空間中。另外，如果資料表空間在任何連線中的 [temp\_tablespaces](../../server-administration/server-configuration/client-connection-defaults.md#19-11-1-cha-ju-de-hang) 設定列表上，則 DROP 可能會因臨時檔案駐留在資料表空間中而失敗。

## 參數

`IF EXISTS`

如果資料表空間不存在，請不要拋出錯誤。在這種情況下發布通知。

_`name`_

資料表空間的名稱。

## 注意

DROP TABLESPACE 不能在交易事務內執行。

## 範例

從系統中移除資料表空間 mystuff：

```text
DROP TABLESPACE mystuff;
```

## 相容性

DROP TABLESPACE 是 PostgreSQL 的延伸功能。

## 參閱

[CREATE TABLESPACE](create-tablespace.md), [ALTER TABLESPACE](alter-tablespace.md)

