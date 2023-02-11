# 23.6. Tablespaces

PostgreSQL 中的資料表空間允許資料庫管理者定義檔案系統中可以儲存資料庫物件的檔案的路徑。建立完成後，在建立資料庫物件時可以透過名稱來引用資料表空間。

通過使用資料表空間，管理者可以控制 PostgreSQL 安裝的磁碟規畫。至少在兩個方面是很有用的。首先，如果初始化叢集的分割區(partition)或磁碟區(volume)的空間不足並且無法擴展時，則可以在不同的分割區上建立資料表空間，資料庫系統重新配置即可使用。

其次，資料表空間允許管理者依資料庫物件特性的知識來優化效能。例如，使用率很高的索引可以放置在非常快速、高可用的磁碟上，例如昂貴的固態磁碟。另一方面，對於很少使用或不關鍵的歸檔資料的資料表可以儲存在較便宜、速度較慢的磁碟系統上。

{% hint style="info" %}
即使位於主 PostgreSQL 資料目錄之外，資料表空間也是資料庫叢集組成的一部分，並且它將作為資料檔案的自治集合來處理。它們會依賴於主資料目錄中包含的中繼資料，因此無法附加到不同的資料庫叢集或單獨備份。同樣，如果您失去了一個資料表空間（檔案被刪除、磁碟故障等），資料庫叢集可能變得不可讀取或無法啟動。所以將資料表空間放置在臨時檔案系統（如 RAM Disk）上會影響整個叢集的可靠性。
{% endhint %}

要定義資料表空間，請使用 [CREATE TABLESPACE ](../../reference/sql-commands/create-tablespace.md)指令，例如：

```
CREATE TABLESPACE fastspace LOCATION '/ssd1/postgresql/data';
```

該路徑必須是 PostgreSQL 作業系統使用者所擁有的空白目錄。隨後在資料表空間內建立的所有物件都將儲存在此目錄下的檔案中。該位置不得位於可移除或瞬時儲存上，因為如果資料表空間失去了，叢集可能會無法運行。

{% hint style="info" %}
在每個邏輯檔案系統中建立多個資料表空間通常沒有什麼意義，因為你無法控制邏輯檔案系統內單個檔案的位置。但是，PostgreSQL 不會強制實施任何此類限制，事實上它並不直接發現系統上的檔案系統界線。 它只是將檔案儲存在你告訴它所使用的目錄中而已。
{% endhint %}

建立資料表空間本身必須以資料庫超級使用者的身份完成，但在此之後，你可以允許普通的資料庫使用者來使用它。為此，請為它們授予 CREATE 的權限。

資料表、索引和整個資料庫可以分配給特定的資料表空間。為此，具有給定資料表空間上的 CREATE 權限的使用者必須將資料表空間名稱作為參數傳遞給相關的指令。例如，下面會在資料表空間 space1 中建立一個資料表：

```sql
CREATE TABLE foo(i int) TABLESPACE space1;
```

或者，使用 [default\_tablespace](../server-configuration/client-connection-defaults.md#default\_tablespace-string) 參數：

```sql
SET default_tablespace = space1;
CREATE TABLE foo(i int);
```

當 default\_tablespace 設定為空字符之外的任何內容時，它將為 CREATE TABLE 和 CREATE INDEX 指令提供一個隱含的 TABLESPACE 子句，當它們沒有明確的 TABLESPACE 子句的時候。

還有一個 [temp\_tablespaces](../server-configuration/client-connection-defaults.md#temp\_tablespaces-string) 參數，用於指定臨時資料表和索引的位置，以及用於排序大型資料之類目的的臨時檔案。這可以是資料表空間名稱的列表，而不是只有一個，以便與臨時物件關聯的負載可以分佈在多個資料表空間中。每次建立臨時物件時都會挑選該列表的隨機成員。

與資料庫關聯的資料表空間用於儲存該資料庫的系統目錄。此外，如果沒有給予 TABLESPACE 子句也沒有其他由 default\_tablespace 或 temp\_tablespaces（根據需要）的選擇指定的話，那麼它是用於在資料庫內建立的資料表、索引和臨時檔案的預設資料表空間。如果建立的資料庫沒有為其指定資料表空間，則它使用與從其複製的模板資料庫相同的資料表空間。

當資料庫叢集初始化時，會自動建立兩個資料表空間。pg\_global 資料表空間用於共享的系統目錄。pg\_default 資料表空間是 template1 和 template0 資料庫的預設資料表空間（因此，除非它被 CREATE DATABASE 中的 TABLESPACE 子句所取代，否則它將成為其他資料庫的預設資料表空間）。

一旦建立之後，可以從任何資料庫使用資料表空間，只要請求的使用者具有足夠的權限即可。這意味著，除非所有使用資料表空間的資料庫中所有物件都被刪除，否則不能刪除資料表空間。

要刪除空的資料表空間，請使用 [DROP TABLESPACE](../../reference/sql-commands/drop-tablespace.md) 指令。

例如，要確認一組現有的資料表空間，請檢查 [pg\_tablespace](../../internals/system-catalogs/51.54.-pg\_tablespace.md) 系統目錄

```sql
SELECT spcname FROM pg_tablespace;
```

psql 工具中的 \db 指令對於列出現有的資料表空間也很有用。

PostgreSQL 利用 symbolic link 來簡化資料表空間的管理。但這也意味著資料表空間只能用於支援 symbolic link 的系統。

目錄 $PGDATA/pg\_tblspc 包含指向叢集中定義的每個非內建資料表空間的 symbolic link。儘管並不推薦，但可以透過重新定義這些連接來手動調整資料表空間的佈局。在伺服器運行期間，任何情況下都不會執行此操作。請注意，在 PostgreSQL 9.1 及更早版本中，你還需要使用新位置更新 pg\_tablespace 目錄。（如果你不這樣做，pg\_dump 將繼續輸出到舊的資料表空間路徑。）
