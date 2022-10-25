# ALTER TABLESPACE

ALTER TABLESPACE — 變更資料表空間的定義

### 語法

```
ALTER TABLESPACE name RENAME TO new_name
ALTER TABLESPACE name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
ALTER TABLESPACE name SET ( tablespace_option = value [, ... ] )
ALTER TABLESPACE name RESET ( tablespace_option [, ... ] )
```

### 說明

ALTER TABLESPACE 可用於變更資料表空間的定義。

您必須擁有該資料表空間才能變更資料表空間的定義。要改變擁有者，您還必須是新角色的直接或間接成員。（請注意，超級使用者自動擁有這些權限。）

### 參數

_`name`_

現有資料表空間的名稱。

_`new_name`_

資料表空間的新名稱。新名稱不能以「pg\_」開頭，因為這些名稱是為系統資料表空間保留的。

_`new_owner`_

資料表空間的新擁有者。

_`tablespace_option`_

要設定或重置的資料表空間參數。目前，唯一可用的參數是 seq\_page\_cost，random\_page\_cost 和 effective\_io\_concurrency。為特定資料表空間設定任一值將覆蓋查詢規劃器一般從該資料表空間中的資料表中讀取頁面成本的估計值，這由相同名稱的配置參數（請參閱 [seq\_page\_cost，random\_page\_cost，effective\_io\_concurrency](../../server-administration/server-configuration/resource-consumption.md#19-4-6-asynchronous-behavior)）所決定。如果一個資料表空間位於比一般 I/O 子系統更快或更慢的磁碟上，這可能很有用。

### 範例

將資料表空間 index\_space 重新命名為 fast\_raid：

```
ALTER TABLESPACE index_space RENAME TO fast_raid;
```

變更資料表空間 index\_space 的擁有者：

```
ALTER TABLESPACE index_space OWNER TO mary;
```

### 相容性

SQL 標準中沒有 ALTER TABLESPACE 語句。

### 參閱

[CREATE TABLESPACE](create-tablespace.md), [DROP TABLESPACE](drop-tablespace.md)
