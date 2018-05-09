---
description: CREATE TABLESPACE — 定義一個新的資料表空間
---

# CREATE TABLESPACE

### 語法

```text
CREATE TABLESPACE tablespace_name
    [ OWNER { new_owner | CURRENT_USER | SESSION_USER } ]
    LOCATION 'directory'
    [ WITH ( tablespace_option = value [, ... ] ) ]
```

### 說明

CREATE TABLESPACE 註冊一個新的叢集範圍的資料表空間。資料表空間名稱必須與資料庫叢集中任何現有資料表空間的名稱不同。

資料表空間允許超級使用者為資料庫物件（如資料表和索引）的資料檔案可以駐留的檔案系統上定義備用位置。

具有適當權限的使用者可以將 tablespace\_name 傳遞給 CREATE DATABASE、CREATE TABLE、CREATE INDEX 或 ADD CONSTRAINT，以將這些物件的資料檔案儲存在指定的資料表空間中。

#### 警告

資料表空間不能獨立於定義它的叢集使用，請參見[第 22.6 節](../../server-administration/managing-databases/manage-ag-tablespaces.md)。

### 參數

_`tablespace_name`_

要建立的資料表空間名稱。該名稱不能以 pg\_ 開頭，因為這些名稱是為系統資料表空間。

_`user_name`_

將擁有資料表空間的使用者的名稱。如果省略，則預設為執行該命令的使用者。只有超級使用者可以建立資料表空間，但他們可以將資料表空間的所有權分配給非超級使用者。

_`directory`_

將用於資料表空間的目錄。該目錄應該是空的，並且必須由 PostgreSQL 的作業系統使用者所擁有。該目錄必須以絕對路徑指定。

_`tablespace_option`_

要設定或重置的資料表空間參數。目前，唯一可用的參數是 seq\_page\_cost，random\_page\_cost 和 effective\_io\_concurrency。為特定資料表空間設定任一值將覆寫查詢規劃器通常從該資料表空間中的資料表中讀取成本的估計值，這由相同名稱的配置參數（請參閱 [seq\_page\_cost](../../server-administration/runtime-config/query-planning.md#19-7-2-planner-cost-constants)、[random\_page\_cost](../../server-administration/runtime-config/query-planning.md#19-7-2-planner-cost-constants)、[effective\_io\_concurrency](../../server-administration/runtime-config/query-planning.md#19-7-2-planner-cost-constants)）確定。如果一個資料表空間位於比一般 I/O 子系統更快或更慢的磁碟上，這些參數可能會很有用。

### 注意

資料表空間僅在支持符號連接的檔案系統上支援。

CREATE TABLESPACE 不能在交易事務內執行。

### 範例

在 /data/dbs 建立一個資料表空間 dbspace：

```text
CREATE TABLESPACE dbspace LOCATION '/data/dbs';
```

在 /data/indexes 處建立一個資料表空間索引空間，並指定 genevieve 為擁有者：

```text
CREATE TABLESPACE indexspace OWNER genevieve LOCATION '/data/indexes';
```

### 相容性

`CREATE TABLESPACE 是一個 PostgreSQL 延伸功能。`

### 參閱

[CREATE DATABASE](create-database.md), [CREATE TABLE](create-table.md), [CREATE INDEX](create-index.md), [DROP TABLESPACE](drop-tablespace.md), [ALTER TABLESPACE](alter-tablespace.md)



