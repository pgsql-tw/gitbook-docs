<a id="UPGRADING"></a>

## 18.6. 升級 PostgreSQL 叢集 [#](#UPGRADING)

[18.6.1. 透過 pg_dumpall 升級資料](upgrading.md#UPGRADING-VIA-PGDUMPALL)

[18.6.2. 透過 pg_upgrade 升級資料](upgrading.md#UPGRADING-VIA-PG-UPGRADE)

[18.6.3. 透過複寫升級資料](upgrading.md#UPGRADING-VIA-REPLICATION)

<a id="id-1.6.5.9.2"></a><a id="id-1.6.5.9.3"></a>

本節討論如何將您的資料庫資料，從一個 PostgreSQL 發行版，
升級到較新的發行版。

目前的 PostgreSQL 版本編號，由主要版本號與次要版本號組成。
舉例來說，在版本編號 10.1 中，10 是主要版本號，
1 是次要版本號，代表這是主要版本 10 的第一個次要發行版。
對於 PostgreSQL 10.0 之前的發行版，版本編號則由三個數字組成，
例如 9.5.3。在這種情況下，主要版本，由版本編號的前兩組數字構成，
例如 9.5，次要版本則是第三個數字，例如 3，
代表這是主要版本 9.5 的第三個次要發行版。

次要發行版，絕不會變更內部儲存格式，
並且永遠與相同主要版本號的更早或更晚次要發行版相容。
舉例來說，版本 10.1 與版本 10.0 及版本 10.6 相容。
同樣地，例如 9.5.3 與 9.5.0、9.5.1 及 9.5.6 相容。
若要在相容版本之間更新，您只需在伺服器停機期間，
替換執行檔，然後重新啟動伺服器即可。資料目錄保持不變——
次要升級就是這麼簡單。

對於 PostgreSQL 的*主要*發行版而言，
內部資料儲存格式可能會發生變更，因此升級也會較為複雜。
將資料轉移到新主要版本的傳統方法，
是傾印（dump）並還原資料庫，不過這可能會相當緩慢。
更快速的方法，是使用
[pg_upgrade](../../reference/reference-server/pgupgrade.md)。
如下文所述，也可以使用複寫方法進行升級。
（若您使用的是預先封裝的 PostgreSQL 版本，
它可能會提供協助進行主要版本升級的指令碼。
詳情請參閱套件層級的相關文件。）

新的主要版本，通常也會引入一些對使用者可見的不相容變更，
因此可能需要修改應用程式的程式設計。所有對使用者可見的變更，
都會列在版本說明中（[附錄 E](../../appendixes/release/README.md)）；
請特別留意標示為「Migration」的章節。雖然您可以直接
從某個主要版本，升級至另一個主要版本，而不必先升級到
中間的版本，但您仍應閱讀所有中間版本的主要版本說明。

謹慎的使用者，會想要先在新版本上測試其用戶端應用程式，
才會完全切換過去；因此，同時安裝新舊兩個版本，
通常是個好主意。在測試 PostgreSQL 主要版本升級時，
請考慮以下幾類可能發生的變更：

管理
:   每個主要發行版中，管理者可用來監控與控制
    伺服器的功能，通常都會有所變更與改進。

SQL
:   除非版本說明中特別提及，否則這通常僅涉及
    新的 SQL 指令功能，而不涉及行為上的變更。

函式庫 API
:   除非版本說明中特別提及，否則像 libpq
    這樣的函式庫，通常只會新增功能。

系統目錄
:   系統目錄的變更，通常只會影響資料庫管理工具。

伺服器 C 語言 API
:   這涉及後端函式 API 的變更，該 API 是以
    C 程式語言撰寫的。這類變更，
    會影響那些深入參照伺服器內部後端函式的程式碼。

<a id="UPGRADING-VIA-PGDUMPALL"></a>

### 18.6.1. 透過 pg_dumpall 升級資料 [#](#UPGRADING-VIA-PGDUMPALL)

其中一種升級方法，是從某個 PostgreSQL 主要版本，
傾印資料，再還原到另一個版本——若要這麼做，
您必須使用像 pg_dumpall 這樣的*邏輯*備份工具；
檔案系統層級的備份方法，並不適用。（系統中已有檢查機制，
會防止您在不相容的 PostgreSQL 版本上，
使用某個資料目錄，因此即使嘗試在某個資料目錄上，
啟動錯誤版本的伺服器，也不會造成重大損害。）

建議您使用*較新*版本 PostgreSQL 所附帶的
pg_dump 與 pg_dumpall 程式，
以善用這些程式中可能已有的改進。目前發行版的傾印程式，
能夠讀取回溯至 9.2 版本的任何伺服器版本的資料。

以下指示，假設您現有的安裝位於
`/usr/local/pgsql` 目錄下，且資料區域位於
`/usr/local/pgsql/data`。請自行代換為
您實際使用的路徑。

1. 若要製作備份，請確認資料庫目前沒有正在更新。
   這不會影響備份的完整性，但已變更的資料，
   當然就不會包含在內。若有必要，請編輯
   `/usr/local/pgsql/data/pg_hba.conf`（或相當的檔案）
   中的權限，禁止除您以外的所有人存取。
   關於存取控制的更多資訊，
   請參閱[第 20 章](../client-authentication/README.md)。

   <a id="id-1.6.5.9.11.5.1.2.1"></a>
   若要備份您的資料庫安裝，請輸入：

   ```

   pg_dumpall > outputfile
   ```

   要製作備份，您可以使用目前執行版本所附帶的
   pg_dumpall 指令；詳情請參閱
   [25.1.2 節](../backup/backup-dump.md#BACKUP-DUMP-ALL)。
   不過，為了獲得最佳結果，請盡量使用
   PostgreSQL 18.6 版所附帶的
   pg_dumpall 指令，因為此版本，
   包含了對舊版本的錯誤修正與改進。雖然這項建議，
   在您尚未安裝新版本時，可能顯得有些奇怪，
   但若您計劃將新版本與舊版本並行安裝，
   就建議遵循此建議。在這種情況下，
   您可以正常完成安裝，之後再轉移資料。
   這也能縮短停機時間。
2. 關閉舊的伺服器：

   ```

   pg_ctl stop
   ```

   在已設定於開機時啟動 PostgreSQL 的系統上，
   可能會有一支啟動檔案，能完成相同的工作。舉例來說，
   在 Red Hat Linux 系統上，您或許會發現以下方式可行：

   ```

   /etc/rc.d/init.d/postgresql stop
   ```

   關於啟動與停止伺服器的詳情，
   請參閱[第 18 章](README.md)。
3. 若要從備份還原，若舊的安裝目錄並非依版本命名，
   請將其重新命名或刪除。建議將該目錄重新命名，
   而非直接刪除，以便在遇到問題時，
   能夠還原回舊版本。請注意，該目錄可能會佔用
   相當多的磁碟空間。若要重新命名該目錄，
   可使用類似以下的指令：

   ```

   mv /usr/local/pgsql /usr/local/pgsql.old
   ```

   （請務必將整個目錄，作為單一單位一併移動，
   以確保相對路徑保持不變。）
4. 依照[第 17 章](../installation/README.md)所述，
   安裝新版本的 PostgreSQL。
5. 若有需要，請建立一個新的資料庫叢集。請記得，
   您必須以特殊資料庫使用者帳號登入的狀態下，
   執行以下指令（若您正在進行升級，應該已經有此帳號）。

   ```

   /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
   ```
6. 還原您先前的 `pg_hba.conf`，
   以及任何 `postgresql.conf` 的修改內容。
7. 同樣以特殊資料庫使用者帳號，
   啟動資料庫伺服器：

   ```

   /usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data
   ```
8. 最後，使用以下指令，從備份還原您的資料：

   ```

   /usr/local/pgsql/bin/psql -d postgres -f outputfile
   ```

   請使用*新版*的 psql。

若要達到最短的停機時間，可以將新伺服器安裝在
另一個目錄下，並讓新舊兩個伺服器，
在不同的連接埠上並行執行。接著，您就可以使用類似以下的方式：

```

pg_dumpall -p 5432 | psql -d postgres -p 5433
```

來轉移您的資料。

<a id="UPGRADING-VIA-PG-UPGRADE"></a>

### 18.6.2. 透過 pg_upgrade 升級資料 [#](#UPGRADING-VIA-PG-UPGRADE)

[pg_upgrade](../../reference/reference-server/pgupgrade.md) 模組，
可讓某個安裝，直接就地從一個 PostgreSQL 主要版本，
遷移至另一個版本。升級可以在數分鐘內完成，
特別是在使用 `--link` 模式時。它所需要的步驟，
與上述 pg_dumpall 方式類似，例如啟動／停止伺服器，
以及執行 initdb。pg_upgrade
的[文件](../../reference/reference-server/pgupgrade.md)，
概述了所需的步驟。

<a id="UPGRADING-VIA-REPLICATION"></a>

### 18.6.3. 透過複寫升級資料 [#](#UPGRADING-VIA-REPLICATION)

您也可以使用邏輯複寫方法，建立一個使用較新版本 PostgreSQL
的待命伺服器。之所以可行，是因為邏輯複寫，
支援在不同主要版本的 PostgreSQL 之間進行複寫。
待命伺服器，可以位於同一部電腦，也可以位於不同的電腦。
一旦它與主要伺服器（執行較舊版本 PostgreSQL）同步完成，
您就可以切換主要伺服器，讓該待命伺服器成為主要伺服器，
並關閉舊的資料庫實體。這樣的切換，
在升級過程中，只會造成數秒鐘的停機時間。

這種升級方式，可以使用內建的邏輯複寫功能來完成，
也可以使用外部的邏輯複寫系統，例如
pglogical、Slony、Londiste
與 Bucardo。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/upgrading.html)（原文版本：18.6；核對日期：2026-09-22）
