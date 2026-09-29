<a id="id-1.9.3.163.1"></a>

## REINDEX

REINDEX — 重建索引

<a id="id-1.9.3.163.2"></a>

## 語法

```

REINDEX [ ( option [, ...] ) ] { INDEX | TABLE | SCHEMA } [ CONCURRENTLY ] name
REINDEX [ ( option [, ...] ) ] { DATABASE | SYSTEM } [ CONCURRENTLY ] [ name ]

where option can be one of:

    CONCURRENTLY [ boolean ]
    TABLESPACE new_tablespace
    VERBOSE [ boolean ]
```

<a id="id-1.9.3.163.5"></a>

## 說明

`REINDEX` 會使用索引所屬資料表中儲存的資料，重建該索引，取代舊有的索引副本。以下是幾種需要使用
`REINDEX` 的情境：

* 索引已損毀，不再包含有效資料。雖然理論上這種情況不該發生，但實際上索引確實可能因軟體錯誤或硬體故障而損毀。
  `REINDEX` 提供了一種復原方法。
* 索引已變得「膨脹」，也就是包含許多空的或近乎空的頁面。在
  PostgreSQL 中，B-tree 索引在某些不常見的存取模式下可能發生這種情況。
  `REINDEX` 提供了一種做法，可透過寫入一份不含死亡頁面的新版索引，來降低該索引的空間佔用。更多資訊請參閱[第 24.2 節](../../server-administration/maintenance/routine-reindex.md)。
* 你變更了某個索引的儲存參數（例如 fillfactor），並希望確保該變更已完全生效。
* 如果使用 `CONCURRENTLY` 選項的索引建置失敗，該索引會被留在「invalid」狀態。這類索引雖然沒有用處，但使用
  `REINDEX` 來重建它們相當方便。請注意，只有
  `REINDEX INDEX` 才能對無效索引執行並行建置。

<a id="id-1.9.3.163.6"></a>

## 參數

`INDEX`
:   重新建立指定的索引。這種形式的 `REINDEX`
    在用於分割索引時，不能在交易區塊內執行。

`TABLE`
:   重新建立指定資料表的所有索引。如果該資料表有次要的「TOAST」資料表，也會一併重新建立索引。這種形式的
    `REINDEX` 在用於分割資料表時，不能在交易區塊內執行。

`SCHEMA`
:   重新建立指定綱要中的所有索引。如果此綱要中某個資料表有次要的「TOAST」資料表，也會一併重新建立索引。共享系統目錄上的索引也會一併處理。
    這種形式的 `REINDEX` 不能在交易區塊內執行。

`DATABASE`
:   重新建立目前資料庫內的所有索引，系統目錄除外。
    系統目錄上的索引不會被處理。
    這種形式的 `REINDEX` 不能在交易區塊內執行。

`SYSTEM`
:   重新建立目前資料庫內、系統目錄上的所有索引，包含共享系統目錄上的索引。
    使用者資料表上的索引不會被處理。
    這種形式的 `REINDEX` 不能在交易區塊內執行。

*`name`*
:   要重新建立索引的特定索引、資料表或資料庫名稱。索引與資料表名稱可加上綱要限定。
    目前 `REINDEX DATABASE` 與 `REINDEX SYSTEM`
    只能對目前的資料庫重建索引。其參數為可省略，若指定則必須與目前資料庫的名稱相符。

`CONCURRENTLY`
:   使用此選項時，PostgreSQL 會在不持有會阻擋資料表上並行插入、更新或刪除之鎖定的情況下重建索引；相對地，標準的索引重建則會鎖定資料表的寫入（但不鎖定讀取），直到重建完成為止。
    使用此選項時有幾點需要注意
    ——請參閱下方的[並行重建索引](sql-reindex.md#SQL-REINDEX-CONCURRENTLY)。

    對於暫存資料表，`REINDEX` 一律採非並行方式進行，因為其他工作階段無法存取它們，而非並行的重新建立索引成本較低。

`TABLESPACE`
:   指定索引將在新的資料表空間上重建。

`VERBOSE`
:   在重建每個索引時，以
    `INFO` 層級印出進度報告。

*`boolean`*
:   指定所選選項應開啟或關閉。
    你可以寫 `TRUE`、`ON` 或
    `1` 來啟用此選項，或寫 `FALSE`、
    `OFF` 或 `0` 來停用它。
    *`boolean`* 值也可以
    省略，此時會視為 `TRUE`。

*`new_tablespace`*
:   將重建索引所在的資料表空間。

<a id="id-1.9.3.163.7"></a>

## 注意

如果你懷疑使用者資料表上的某個索引已損毀，可以直接用
`REINDEX INDEX` 或 `REINDEX TABLE` 重建該索引，或重建該資料表上的所有索引。

如果你需要從系統資料表上索引的損毀中復原，情況會比較困難。在這種情況下，很重要的一點是系統本身不得使用任何可疑的索引。
（事實上，在這類情境下，你可能會發現伺服器程序因依賴已損毀的索引，而在啟動時立即當機。）
若要安全地復原，伺服器必須以
`-P` 選項啟動，此選項會阻止它在系統目錄查詢時使用索引。

其中一種做法是關閉伺服器，並在命令列中加上
`-P` 選項，啟動單一使用者的
PostgreSQL 伺服器。
接著，就可以視你想重建的範圍，執行
`REINDEX DATABASE`、`REINDEX SYSTEM`、
`REINDEX TABLE` 或 `REINDEX INDEX`。如果不確定，可使用
`REINDEX SYSTEM` 來選擇重建資料庫內所有系統索引。之後結束單一使用者伺服器工作階段，並重新啟動一般的伺服器。
關於如何與單一使用者伺服器介面互動的更多資訊，請參閱 [postgres](../reference-server/app-postgres.md) 參考頁面。

另一種做法是在啟動一般伺服器工作階段時，於其命令列選項中加入
`-P`。
不同用戶端的做法各不相同，但在所有以
libpq 為基礎的用戶端中，都可以在啟動用戶端之前，將
`PGOPTIONS` 環境變數設為 `-P`。請注意，雖然此方法不需要封鎖其他用戶端，但在修復完成之前，最好還是防止其他使用者連線到已損毀的資料庫。

`REINDEX` 在效果上類似先刪除再重新建立索引，因為索引內容確實會從頭重建。不過，其鎖定考量則相當不同。`REINDEX` 會鎖定該索引所屬資料表的寫入，但不鎖定讀取。它也會對正在處理的特定索引取得
`ACCESS EXCLUSIVE` 鎖，這會阻擋嘗試使用該索引的讀取。特別是，規劃器不論查詢內容為何，都會嘗試對資料表的每個索引取得
`ACCESS SHARE`
鎖，因此 `REINDEX` 幾乎會阻擋所有查詢，除了少數計畫已被快取、且不使用該特定索引的預備查詢之外。
相對地，
`DROP INDEX` 會短暫地對其所屬資料表取得
`ACCESS EXCLUSIVE` 鎖，同時阻擋寫入與讀取。之後的
`CREATE INDEX` 會鎖定寫入但不鎖定讀取；由於索引尚不存在，不會有讀取嘗試使用它，因此不會產生阻擋，但讀取可能被迫改用成本較高的循序掃描。

在 `REINDEX` 執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog,
pg_temp`。

要對單一索引或資料表重建索引，必須在該資料表上具備
`MAINTAIN` 權限。請注意，雖然對分割索引或分割資料表執行 `REINDEX` 需要在該分割資料表上具備
`MAINTAIN` 權限，但這類指令在處理個別分割區時會略過權限檢查。對綱要或資料庫重建索引，則需要是該綱要或資料庫的擁有者，或具備
[pg_maintain](../../server-administration/user-manag/predefined-roles.md#PREDEFINED-ROLE-PG-MAINTAIN)
角色的權限。特別要注意的是，因此非超級使用者也有可能重建其他使用者所擁有資料表的索引。不過，作為一個特殊例外，
`REINDEX DATABASE`、`REINDEX SCHEMA`
與 `REINDEX SYSTEM` 除非使用者對該目錄具備
`MAINTAIN` 權限，否則會略過共享系統目錄上的索引。

分割索引或分割資料表可分別使用 `REINDEX INDEX` 或 `REINDEX TABLE`
重建索引。指定的分割關聯之每個分割區，會各自在獨立的交易中重建索引。在對分割資料表或分割索引進行操作時，這些指令都不能在交易區塊內使用。

對分割索引或分割資料表使用
`REINDEX` 的 `TABLESPACE` 子句時，只會更新葉節點分割區的資料表空間參照。由於分割索引本身不會被更新，建議另外對它們使用
`ALTER TABLE ONLY`，以便任何新附加的分割區都能繼承新的資料表空間。若操作失敗，可能尚未將所有索引都搬移到新的資料表空間。重新執行該指令會重建所有葉節點分割區，並將先前尚未處理的索引搬移到新的資料表空間。

如果 `SCHEMA`、`DATABASE` 或
`SYSTEM` 與 `TABLESPACE` 一起使用，
系統關聯會被略過，並會產生一則 `WARNING`。
TOAST 資料表上的索引會被重建，但不會被搬移到新的資料表空間。

<a id="SQL-REINDEX-CONCURRENTLY"></a>

### 並行重建索引

<a id="id-1.9.3.163.7.12.2"></a>

重建索引可能會干擾資料庫的正常運作。
一般而言，PostgreSQL 會鎖定其索引正在重建的資料表，阻止寫入，並以對該資料表的單一次掃描完成整個索引建置。其他交易仍可讀取該資料表，但如果它們嘗試在該資料表中插入、更新或刪除資料列，就會被阻擋，直到索引重建完成為止。如果這是一個正在營運中的正式環境資料庫，這可能造成嚴重影響。非常大型的資料表建立索引可能需要數小時，即使是較小的資料表，索引重建也可能讓寫入者被鎖定過長、對正式環境系統來說難以接受的時間。

PostgreSQL 支援以最低限度鎖定寫入的方式重建索引。此方法是透過指定
`REINDEX` 的 `CONCURRENTLY` 選項來啟用的。使用此選項時，
PostgreSQL 必須對每個需要重建的索引，對資料表執行兩次掃描，並等待所有可能會使用該索引的現有交易結束。
這種方法所需的總工作量比標準的索引重建更多，完成所需時間也顯著較長，因為它需要等待可能會修改該索引的未完成交易。不過，由於它允許在索引重建期間繼續正常運作，這種方法對於在正式環境中重建索引相當有用。當然，索引重建所帶來的額外
CPU、記憶體與 I/O 負載，可能會拖慢其他操作。

並行重建索引會經歷以下步驟。每個步驟都在獨立的交易中執行。如果有多個索引要重建，則每個步驟都會先處理完所有索引，才會進入下一個步驟。

1. 系統目錄 `pg_index` 中會新增一個暫時性的過渡索引定義。這個定義將用來取代舊索引。系統會對正在重建索引的索引及其所屬資料表，取得工作階段層級的
   `SHARE UPDATE EXCLUSIVE` 鎖，以在處理過程中防止任何綱要變更。
2. 針對每個新索引，會執行第一輪索引建置。索引建置完成後，其
   `pg_index.indisready` 旗標會切換為「true」，使其可接受插入操作，並在執行該次建置的交易完成後，讓其他工作階段也能看見它。此步驟會針對每個索引，各自在獨立的交易中完成。
3. 接著會執行第二輪，以加入在第一輪執行期間新增的資料列。此步驟同樣會針對每個索引，各自在獨立的交易中完成。
4. 所有參照該索引的限制條件都會改為參照新的索引定義，索引的名稱也會被變更。此時，
   `pg_index.indisvalid` 對新索引會切換為
   「true」，對舊索引則切換為「false」，並執行快取失效處理，使所有先前參照舊索引的工作階段都失效。
5. 舊索引的 `pg_index.indisready` 會被切換為
   「false」，以防止任何新的資料列插入，此步驟會等待可能參照舊索引的執行中查詢完成後才進行。
6. 舊索引會被刪除。針對這些索引與資料表所持有的
   `SHARE UPDATE
   EXCLUSIVE` 工作階段層級鎖，會一併釋放。

如果在重建索引時發生問題，例如唯一值索引發生唯一性衝突，`REINDEX`
指令會失敗，但除了既有索引之外，還會留下一個「invalid」的新索引。這個索引在查詢時會被忽略，因為它可能並不完整；不過它仍會消耗更新時的額外負擔。psql 的 `\d` 指令會將這類索引回報為
`INVALID`：

```

postgres=# \d tab
       Table "public.tab"
 Column |  Type   | Modifiers
--------+---------+-----------
 col    | integer |
Indexes:
    "idx" btree (col)
    "idx_ccnew" btree (col) INVALID
```

如果被標記為 `INVALID` 的索引後綴為
`_ccnew`，則表示它是在並行操作過程中建立的過渡索引，建議的復原方式是用
`DROP INDEX` 刪除它，
然後再次嘗試 `REINDEX CONCURRENTLY`。
如果無效索引後綴改為 `_ccold`，
則表示它是原本無法被刪除的原始索引；
建議的復原方式就只是刪除該索引，因為索引重建本身已經成功。
索引名稱後綴可能會附加一個非零的數字，以確保無效索引名稱的唯一性，例如
`_ccnew1`、
`_ccold2` 等。

一般的索引建置允許在同一資料表上同時進行其他一般索引建置，但同一時間、同一資料表上只能進行一個並行索引建置。在這兩種情況下，其間都不允許對該資料表進行其他類型的綱要變更。另一個差異是，一般的
`REINDEX TABLE` 或 `REINDEX INDEX`
指令可以在交易區塊內執行，但 `REINDEX
CONCURRENTLY` 則不行。

如同任何長時間執行的交易，資料表上的 `REINDEX` 可能會影響哪些資料列能被其他資料表上並行執行的
`VACUUM` 移除。

`REINDEX SYSTEM` 不支援
`CONCURRENTLY`，因為系統目錄無法並行重建索引。

此外，排除限制條件所用的索引無法並行重建索引。如果這類索引直接在此指令中被指名，就會產生錯誤。如果對具有排除限制條件索引的資料表或資料庫並行重建索引，這些索引會被跳過。（不使用
`CONCURRENTLY` 選項的話，是可以重建這類索引的。）

每個執行 `REINDEX` 的後端都會在
`pg_stat_progress_create_index` 檢視表中回報其進度。詳情請參閱
[第 27.4.4 節](../../server-administration/monitoring/progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)。

<a id="id-1.9.3.163.8"></a>

## 範例

重建單一索引：

```

REINDEX INDEX my_index;
```

重建資料表 `my_table` 上的所有索引：

```

REINDEX TABLE my_table;
```

在不信任系統索引已經有效的情況下，重建特定資料庫中的所有索引：

```

$ export PGOPTIONS="-P"
$ psql broken_db
...
broken_db=> REINDEX DATABASE broken_db;
broken_db=> \q
```

在重建索引期間，不阻擋所涉及關聯上的讀寫操作，為某個資料表重建索引：

```

REINDEX TABLE CONCURRENTLY my_broken_table;
```

<a id="id-1.9.3.163.9"></a>

## 相容性

SQL 標準中並沒有 `REINDEX` 指令。

<a id="id-1.9.3.163.10"></a>

## 另請參閱

[CREATE INDEX](sql-createindex.md), [DROP INDEX](sql-dropindex.md), [reindexdb](../reference-client/app-reindexdb.md), [第 27.4.4 節](../../server-administration/monitoring/progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-reindex.html)（原文版本：18.6；核對日期：2026-09-28）
