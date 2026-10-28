<a id="APP-PGVERIFYBACKUP"></a><a id="id-1.9.4.20.1"></a>

## pg_verifybackup

pg_verifybackup — 驗證 PostgreSQL 叢集基礎備份的完整性

<a id="id-1.9.4.20.4"></a>

## 語法

<a id="id-1.9.4.20.4.1"></a>

`pg_verifybackup` [*`option`*...]

<a id="id-1.9.4.20.5"></a>

## 說明

pg_verifybackup 用來對照伺服器在備份當時所產生的 `backup_manifest`，檢查以 `pg_basebackup` 製作的資料庫叢集備份的完整性。備份可以「plain」或「tar」格式儲存；這包含以 pg_basebackup 支援的任何演算法壓縮的 tar 格式備份。不過，目前只有 plain 格式的備份支援 `WAL` 驗證。因此，若備份以 tar 格式儲存，應該使用 `-n, --no-parse-wal` 選項。

請務必注意，pg_verifybackup 所執行的驗證並不包含、也無法包含執行中的伺服器在嘗試使用該備份時會執行的每一項檢查。即使你使用此工具，仍應執行測試還原，並驗證產生的資料庫如預期運作，且看起來包含正確的資料。不過，pg_verifybackup 能偵測出許多因儲存問題或使用者錯誤而常見的問題。

備份驗證分四個階段進行。首先，`pg_verifybackup` 會讀取 `backup_manifest` 檔案。若該檔案不存在、無法讀取、格式錯誤、系統識別碼與備份目錄的 `pg_control` 不符，或未通過以其自身內部檢查碼進行的驗證，`pg_verifybackup` 會以嚴重錯誤終止。

第二，`pg_verifybackup` 會嘗試驗證目前儲存在磁碟上的資料檔案與伺服器原本要傳送的資料檔案完全相同，但有一些例外，說明如下。多出與缺少的檔案都會被偵測出來，但有少數例外。此步驟會忽略 `postgresql.auto.conf`、`standby.signal` 與 `recovery.signal` 是否存在或有任何修改，因為這些檔案預期可能在製作備份的過程中被建立或修改。它也不會對目標目錄中的 `backup_manifest` 檔案或 `pg_wal` 內的任何內容提出異議，即使這些檔案不會列在備份清單中。只會檢查檔案；目錄是否存在不會被驗證，只會間接驗證：若某個目錄缺少了，它原本應包含的任何檔案必然也會缺少。

接著，`pg_verifybackup` 會對所有檔案計算檢查碼，將檢查碼與清單中的值比較，並對計算出的檢查碼與清單中儲存的檢查碼不符的任何檔案發出錯誤。對於在前一步驟中產生錯誤的任何檔案，不會執行此步驟，因為已知它們有問題。在前一步驟中被忽略的檔案，在此步驟中也會被忽略。

最後，`pg_verifybackup` 會使用清單來驗證復原備份所需的預寫日誌記錄存在，且能夠被讀取與剖析。`backup_manifest` 包含需要哪些預寫日誌記錄的資訊，而 `pg_verifybackup` 會使用該資訊呼叫 `pg_waldump` 來剖析這些預寫日誌記錄。這時會使用 `--quiet` 旗標，讓 `pg_waldump` 只回報錯誤，而不產生任何其他輸出。雖然這種程度的驗證足以偵測明顯的問題，例如缺少檔案或內部檢查碼不符的檔案，但還不夠全面，無法偵測嘗試復原時可能發生的每一種問題。例如，伺服器錯誤所產生、檢查碼正確但指定了無意義動作的預寫日誌記錄，就無法以此方法偵測。

請注意，若存在復原備份時不需要的額外 WAL 檔案，此工具不會檢查它們，不過可以另外呼叫 `pg_waldump` 來達成此目的。也請注意，WAL 驗證與版本相關：你必須使用與所檢查備份相對應版本的 `pg_verifybackup`，因而也是相對應版本的 `pg_waldump`。相較之下，資料檔案完整性檢查應該能與任何會產生 `backup_manifest` 檔案的伺服器版本搭配運作。

<a id="id-1.9.4.20.6"></a>

## 選項

pg_verifybackup 接受下列命令列引數：

`-e`<br>`--exit-on-error`
:   一偵測到備份有問題就立即結束。若未指定此選項，`pg_verifybackup` 在偵測到問題後仍會繼續檢查備份，並將偵測到的所有問題回報為錯誤。

`-F format`<br>`--format=format`
:   指定備份的格式。*`format`* 可以是下列其中之一：

    `p`<br>`plain`
    :   備份由一般檔案組成，配置方式與來源伺服器的資料目錄及資料表空間相同。

    `t`<br>`tar`
    :   備份由 tar 檔案組成，這些檔案可能經過壓縮。有效的備份包含存放主資料目錄的 `base.tar` 檔案、存放 WAL 檔案的 `pg_wal.tar`，以及每個資料表空間各自的 tar 檔案（以該資料表空間的 OID 命名）。若備份經過壓縮，每個檔名結尾都會加上相應的壓縮副檔名。

`-i path`<br>`--ignore=path`
:   比較備份中實際存在的資料檔案清單與 `backup_manifest` 檔案中所列的檔案時，忽略指定的檔案或目錄；該檔案或目錄應以相對路徑名稱表示。若指定的是目錄，此選項會影響以該位置為根的整個子樹。若相對路徑名稱與指定的路徑名稱相符，關於多出檔案、缺少檔案、檔案大小差異或檢查碼不符的警示都會被抑制。此選項可以指定多次。

`-m path`<br>`--manifest-path=path`
:   使用位於指定路徑的清單檔案，而不是位於備份目錄根目錄的清單檔案。

`-n`<br>`--no-parse-wal`
:   不嘗試剖析從此備份復原所需的預寫日誌資料。

`-P`<br>`--progress`

啟用進度回報。開啟此選項後，會在驗證檢查碼時提供進度報告。

此選項不能與 `--quiet` 選項一起使用。

`-q`<br>`--quiet`
:   備份驗證成功時不印出任何內容。

`-s`<br>`--skip-checksums`
:   不驗證資料檔案的檢查碼。仍會檢查檔案是否存在以及檔案大小。由於不需要讀取檔案本身，這會快得多。

`-w path`<br>`--wal-directory=path`
:   嘗試剖析儲存在指定目錄中的 WAL 檔案，而不是 `pg_wal` 中的。若備份儲存在與 WAL 歸檔不同的位置，這可能很有用。

另外也提供其他選項：

`-V`<br>`--version`
:   印出 pg_verifybackup 版本後結束。

`-?`<br>`--help`
:   顯示 pg_verifybackup 命令列引數的說明後結束。

<a id="id-1.9.4.20.7"></a>

## 範例

若要製作位於 `mydbserver` 之伺服器的基礎備份，並驗證備份的完整性：

```

$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
$ pg_verifybackup /usr/local/pgsql/data
```

若要製作位於 `mydbserver` 之伺服器的基礎備份，將清單移到備份目錄之外的某處，然後驗證備份：

```

$ pg_basebackup -h mydbserver -D /usr/local/pgsql/backup1234
$ mv /usr/local/pgsql/backup1234/backup_manifest /my/secure/location/backup_manifest.1234
$ pg_verifybackup -m /my/secure/location/backup_manifest.1234 /usr/local/pgsql/backup1234
```

若要驗證備份，同時忽略手動加入備份目錄的檔案，並略過檢查碼驗證：

```

$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
$ edit /usr/local/pgsql/data/note.to.self
$ pg_verifybackup --ignore=note.to.self --skip-checksums /usr/local/pgsql/data
```

<a id="id-1.9.4.20.8"></a>

## 另請參閱

[pg_basebackup](app-pgbasebackup.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgverifybackup.html)（原文版本：18.6；核對日期：2026-10-09）
