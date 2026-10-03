<a id="SQL-CREATETABLESPACE"></a><a id="id-1.9.3.87.1"></a>

## CREATE TABLESPACE

CREATE TABLESPACE — 定義新的資料表空間

<a id="id-1.9.3.87.4"></a>

## 語法

```

CREATE TABLESPACE tablespace_name
    [ OWNER { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER } ]
    LOCATION 'directory'
    [ WITH ( tablespace_option = value [, ... ] ) ]
```

<a id="id-1.9.3.87.5"></a>

## 說明

`CREATE TABLESPACE` 會註冊一個新的、整個叢集共用的資料表空間。資料表空間名稱必須與資料庫叢集中任何現有資料表空間的名稱不同。

資料表空間讓超級使用者可以在檔案系統上定義另一個位置，用來存放包含資料庫物件（例如資料表與索引）的資料檔案。

具有適當權限的使用者可以將 *`tablespace_name`* 傳給 `CREATE DATABASE`、`CREATE TABLE`、`CREATE INDEX` 或 `ADD CONSTRAINT`，讓這些物件的資料檔案存放在指定的資料表空間中。

### 警告

資料表空間無法脫離定義它的叢集而獨立使用；請參閱[第 22.6 節](../../server-administration/managing-databases/manage-ag-tablespaces.md)。

<a id="id-1.9.3.87.6"></a>

## 參數

*`tablespace_name`*
:   要建立之資料表空間的名稱。名稱不能以 `pg_` 開頭，因為這類名稱保留給系統資料表空間使用。

*`user_name`*
:   將擁有該資料表空間之使用者的名稱。若省略，預設為執行此命令的使用者。只有超級使用者可以建立資料表空間，但他們可以將資料表空間的擁有權指派給非超級使用者。

*`directory`*
:   將用於該資料表空間的目錄。此目錄必須已存在（`CREATE TABLESPACE` 不會建立它）、應該是空的，而且必須由 PostgreSQL 系統使用者擁有。此目錄必須以絕對路徑名稱指定。

*`tablespace_option`*
:   要設定或重設的資料表空間參數。目前唯一可用的參數是 `seq_page_cost`、`random_page_cost`、`effective_io_concurrency` 與 `maintenance_io_concurrency`。為特定資料表空間設定這些值，將會覆寫規劃器對於從該資料表空間中的資料表讀取頁面之成本的一般估計，以及發出多少並行 I/O；這些原本是由同名的組態參數所設定（請參閱 [seq_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-SEQ-PAGE-COST)、[random_page_cost](../../server-administration/runtime-config/runtime-config-query.md#GUC-RANDOM-PAGE-COST)、[effective_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY)、[maintenance_io_concurrency](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)）。若某個資料表空間位於比 I/O 子系統其餘部分更快或更慢的磁碟上，這可能會很有用。

<a id="id-1.9.3.87.7"></a>

## 注意事項

`CREATE TABLESPACE` 不能在交易區塊內執行。

<a id="id-1.9.3.87.8"></a>

## 範例

若要在檔案系統位置 `/data/dbs` 建立資料表空間 `dbspace`，請先使用作業系統的工具建立該目錄，並設定正確的擁有權：

```

mkdir /data/dbs
chown postgres:postgres /data/dbs
```

接著在 PostgreSQL 中執行建立資料表空間的命令：

```

CREATE TABLESPACE dbspace LOCATION '/data/dbs';
```

若要建立由另一個資料庫使用者擁有的資料表空間，請使用類似這樣的命令：

```

CREATE TABLESPACE indexspace OWNER genevieve LOCATION '/data/indexes';
```

<a id="id-1.9.3.87.9"></a>

## 相容性

`CREATE TABLESPACE` 是 PostgreSQL 擴充功能。

<a id="id-1.9.3.87.10"></a>

## 另請參閱

[CREATE DATABASE](sql-createdatabase.md), [CREATE TABLE](sql-createtable.md), [CREATE INDEX](sql-createindex.md), [DROP TABLESPACE](sql-droptablespace.md), [ALTER TABLESPACE](sql-altertablespace.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtablespace.html)（原文版本：18.6；核對日期：2026-10-03）
