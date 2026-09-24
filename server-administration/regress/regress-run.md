<a id="REGRESS-RUN"></a>

## 31.1. 執行測試 [#](#REGRESS-RUN)

[31.1.1. 針對暫時安裝執行測試](regress-run.md#REGRESS-RUN-TEMP-INST)

[31.1.2. 針對既有安裝執行測試](regress-run.md#REGRESS-RUN-EXISTING-INST)

[31.1.3. 額外的測試套組](regress-run.md#REGRESS-ADDITIONAL)

[31.1.4. 地區設定與編碼](regress-run.md#REGRESS-RUN-LOCALE)

[31.1.5. 自訂伺服器設定](regress-run.md#REGRESS-RUN-CUSTOM-SETTINGS)

[31.1.6. 額外測試](regress-run.md#REGRESS-RUN-EXTRA-TESTS)

迴歸測試可以針對已安裝並正在執行的伺服器執行，
也可以使用建置樹內的暫時安裝來執行。此外，
測試還有「平行」與「循序」兩種執行模式。
循序模式會單獨執行每個測試指令碼，
而平行模式則會啟動多個伺服器程序，
以平行方式執行成組的測試。平行測試能提升信心，
確認程序間通訊與鎖定機制運作正常。
若某些測試有此需求，即使在「平行」模式下，
仍可能以循序方式執行。

<a id="REGRESS-RUN-TEMP-INST"></a>

### 31.1.1. 針對暫時安裝執行測試 [#](#REGRESS-RUN-TEMP-INST)

若要在建置完成後、安裝之前執行平行迴歸測試，
請在頂層目錄中輸入：

```

make check
```

（或者，你也可以切換到
`src/test/regress`，在該處執行此命令。）
以平行方式執行的測試，會加上「+」前綴，
而以循序方式執行的測試，則會加上「-」前綴。
最後你應該會看到類似下列的內容：

```


# All 213 tests passed.
```

或者是一則說明哪些測試失敗的訊息。在認定「失敗」
代表嚴重問題之前，請先參閱下方的[31.2 節](regress-evaluation.md)。

由於此測試方法會執行一個暫時性伺服器，
若你以 root 使用者身分進行建置，此方法將無法運作，
因為伺服器不會以 root 身分啟動。建議的做法，
是不要以 root 身分進行建置，或是在完成安裝之後
才進行測試。

若你已將 PostgreSQL 設定為安裝到
已存在較舊版 PostgreSQL 安裝的位置，
且在安裝新版本之前執行 `make check`，
可能會發現測試因為新程式嘗試使用已安裝的共享程式庫
而失敗。（典型的徵狀是抱怨未定義的符號。）
若你希望在覆寫舊安裝之前執行測試，
就需要以 `configure --disable-rpath`
進行建置。然而，並不建議你在最終安裝時使用此選項。

平行迴歸測試會以你的使用者 ID，
啟動相當多的程序。目前，最大並行數為
二十個平行測試指令碼，也就是說會有四十個程序：
每個測試指令碼都有一個伺服器程序，
以及一個 psql 程序。因此，
若你的系統強制執行單一使用者的程序數量上限，
請確保此上限至少為五十左右，
否則你在平行測試中，可能會遇到看似隨機發生的失敗。
若你無法提高此上限，可以透過設定
`MAX_CONNECTIONS` 參數，
來降低平行程度。例如：

```

make MAX_CONNECTIONS=10 check
```

會限制最多同時執行十個測試。

<a id="REGRESS-RUN-EXISTING-INST"></a>

### 31.1.2. 針對既有安裝執行測試 [#](#REGRESS-RUN-EXISTING-INST)

若要在安裝完成後執行測試（請參閱
[第 17 章](../installation/README.md)），
請依照 [第 18 章](../runtime/README.md) 中的說明，
初始化資料目錄並啟動伺服器，接著輸入：

```

make installcheck
```

或若要進行平行測試：

```

make installcheck-parallel
```

除非以 `PGHOST` 與 `PGPORT`
環境變數另行指定，否則測試預期會連線至本機主機，
並使用預設連接埠號碼。測試會在一個名為
`regression` 的資料庫中執行；
任何現有的同名資料庫都會被捨棄。

測試也會暫時建立一些叢集層級的物件，
例如角色、資料表空間與訂閱。這些物件的名稱，
會以 `regress_` 開頭。若你所使用的安裝中，
確實存在以此方式命名的全域物件，
請留意不要使用 `installcheck` 模式。

<a id="REGRESS-ADDITIONAL"></a>

### 31.1.3. 額外的測試套組 [#](#REGRESS-ADDITIONAL)

`make check` 與 `make installcheck`
命令，只會執行「核心」迴歸測試，
用來測試 PostgreSQL 伺服器的內建功能。
原始碼發行套件中，含有許多額外的測試套組，
其中大多數與選用程序語言等附加功能有關。

若要針對已選擇要建置之模組執行所有適用的測試套組
（包括核心測試），請在建置樹頂層輸入以下其中一個命令：

```

make check-world
make installcheck-world
```

這些命令會分別使用暫時性伺服器，或已安裝的伺服器
來執行測試，就如同先前針對 `make check`
與 `make installcheck` 所說明的一樣。
其他考量事項，也與先前針對各方法所說明的相同。
請注意，`make check-world` 會為每個
受測模組建置獨立的執行個體（暫時資料目錄），
因此比 `make installcheck-world`
需要更多時間與磁碟空間。

在具備多核心 CPU、且作業系統限制不嚴格的現代機器上，
你可以透過平行處理大幅加快速度。
大多數 PostgreSQL 開發人員實際用來執行所有測試的做法，
類似下列這樣：

```

make check-world -j8 >/dev/null
```

`-j` 限制值接近或略高於可用核心數。
捨棄標準輸出，能消除在你只想確認是否成功時，
沒有意義的訊息雜訊。（若發生失敗，
標準錯誤訊息通常已足以讓你判斷該從何處進一步查看。）

另外，你也可以在建置樹的相應子目錄中，
輸入 `make check` 或 `make installcheck`，
執行個別的測試套組。請記住，
`make installcheck` 假設你已安裝相關模組，
而不只是核心伺服器。

可以用這種方式呼叫的額外測試包括：

* 選用程序語言的迴歸測試。
  這些測試位於 `src/pl` 底下。
* `contrib` 模組的迴歸測試，
  位於 `contrib` 底下。
  並非所有 `contrib` 模組都有測試。
* 介面程式庫的迴歸測試，
  位於 `src/interfaces/libpq/test` 與
  `src/interfaces/ecpg/test` 中。
* 核心支援之驗證方法的測試，
  位於 `src/test/authentication` 中。
  （關於其他驗證相關測試，請見下文。）
* 用於對並行工作階段行為施加壓力的測試，
  位於 `src/test/isolation` 中。
* 當機復原與實體複寫的測試，
  位於 `src/test/recovery` 中。
* 邏輯複寫的測試，
  位於 `src/test/subscription` 中。
* 用戶端程式的測試，位於 `src/bin` 底下。

在使用 `installcheck` 模式時，
這些測試會建立並刪除名稱中包含
`regression` 的測試資料庫，
例如 `pl_regression`
或 `contrib_regression`。若你所使用的安裝中，
確實存在以此方式命名的非測試用資料庫，
請留意不要使用 `installcheck` 模式。

其中部分輔助測試套組，
使用了 [31.4 節](regress-tap.md)所說明的 TAP 架構。
只有在 PostgreSQL 是以
`--enable-tap-tests` 選項進行組態設定時，
才會執行以 TAP 為基礎的測試。
這在開發時建議啟用，
但若沒有合適的 Perl 安裝，也可以省略。

有些測試套組預設不會執行，原因可能是
在多使用者系統上執行並不安全、需要特殊軟體，
或需要耗費大量資源。你可以透過將
`make` 變數或環境變數
`PG_TEST_EXTRA` 設為以空白分隔的清單，
來決定要額外執行哪些測試套組，例如：

```

make check-world PG_TEST_EXTRA='kerberos ldap ssl load_balance libpq_encryption'
```

目前支援下列值：

`kerberos`
:   執行 `src/test/kerberos` 底下的測試套組。
    這需要安裝 MIT Kerberos，並會開啟 TCP/IP 監聽 socket。

`ldap`
:   執行 `src/test/ldap` 底下的測試套組。
    這需要安裝 OpenLDAP，並會開啟
    TCP/IP 監聽 socket。

`libpq_encryption`
:   執行測試
    `src/interfaces/libpq/t/005_negotiate_encryption.pl`。
    這會開啟 TCP/IP 監聽 socket。若 `PG_TEST_EXTRA`
    也包含 `kerberos`，
    則會啟用需要安裝 MIT Kerberos 的額外測試。

`load_balance`
:   執行測試
    `src/interfaces/libpq/t/004_load_balance_dns.pl`。
    這需要編輯系統的 `hosts` 檔案，
    並會開啟 TCP/IP 監聽 socket。

`oauth`
:   執行 `src/test/modules/oauth_validator`
    底下的測試套組。這會為一個執行 HTTPS 的測試伺服器，
    開啟 TCP/IP 監聽 socket。

`regress_dump_restore`
:   在
    `src/bin/pg_upgrade/t/002_pg_upgrade.pl`
    中執行一項額外的測試套組，
    透過 `pg_dump`／
    `pg_restore` 對迴歸資料庫進行循環測試。
    預設未啟用，因為它相當耗費資源。

`sepgsql`
:   執行 `contrib/sepgsql` 底下的測試套組。
    這需要以特定方式設定好的 SELinux 環境；請參閱
    [F.40.3 節](../../appendixes/contrib/sepgsql.md#SEPGSQL-REGRESSION)。

`ssl`
:   執行 `src/test/ssl` 底下的測試套組。
    這會開啟 TCP/IP 監聽 socket。

`wal_consistency_checking`
:   在執行 `src/test/recovery` 底下的部分測試時，
    使用 `wal_consistency_checking=all`。
    預設未啟用，因為它相當耗費資源。

`xid_wraparound`
:   執行 `src/test/modules/xid_wraparound`
    底下的測試套組。
    預設未啟用，因為它相當耗費資源。

即使 `PG_TEST_EXTRA` 中提及了
目前建置組態不支援的功能，其對應測試也不會被執行。

此外，`src/test/modules` 中還有一些測試，
會由 `make check-world` 執行，
但不會由 `make installcheck-world` 執行。
這是因為它們會安裝非正式環境用的擴充功能，
或有其他被認為不適用於正式環境安裝的副作用。
若你願意，可以在這些子目錄的其中一個中執行
`make install` 與 `make installcheck`，
但並不建議你對非測試用的伺服器這麼做。

<a id="REGRESS-RUN-LOCALE"></a>

### 31.1.4. 地區設定與編碼 [#](#REGRESS-RUN-LOCALE)

依預設，使用暫時安裝的測試，
會使用目前環境中所定義的地區設定，
以及由 `initdb` 所決定的對應資料庫編碼。
透過設定適當的環境變數，測試不同的地區設定，
可能會很有用，例如：

```

make check LANG=C
make check LC_COLLATE=en_US.utf8 LC_CTYPE=fr_CA.utf8
```

由於實作方式的緣故，設定 `LC_ALL`
對此目的並不會生效；其他所有地區設定相關的
環境變數則都能正常運作。

當針對既有安裝進行測試時，地區設定
是由既有的資料庫叢集所決定，
無法針對該次測試執行另外設定。

你也可以透過設定變數 `ENCODING`，
明確選擇資料庫編碼，例如：

```

make check LANG=C ENCODING=EUC_JP
```

以此方式設定資料庫編碼，
通常只有在地區設定為 C 時才有意義；
否則編碼會依地區設定自動選擇，
若你指定的編碼與地區設定不符，就會導致錯誤。

無論是針對暫時安裝還是既有安裝進行測試，
都可以設定資料庫編碼，不過在後者的情況下，
該編碼必須與該安裝的地區設定相容。

<a id="REGRESS-RUN-CUSTOM-SETTINGS"></a>

### 31.1.5. 自訂伺服器設定 [#](#REGRESS-RUN-CUSTOM-SETTINGS)

執行測試套組時，有幾種方式可以使用自訂的伺服器設定。
這對於啟用額外的記錄、調整資源限制，
或啟用額外的執行時期檢查（例如
[debug_discard_caches](../runtime-config/runtime-config-developer.md#GUC-DEBUG-DISCARD-CACHES)）
可能很有用。但請注意，
並非所有測試都能保證在任意設定下順利通過。

可以透過環境變數 `PG_TEST_INITDB_EXTRA_OPTS`，
將額外選項傳遞給測試設定期間內部執行的各個
`initdb` 命令。例如，
若要在啟用總和檢查碼、
並使用自訂 WAL 區段大小與
`work_mem` 設定的情況下執行測試，可使用：

```

make check PG_TEST_INITDB_EXTRA_OPTS='-k --wal-segsize=4 -c work_mem=50MB'
```

對於核心迴歸測試套組，
以及其他由 `pg_regress` 驅動的測試而言，
也可以透過 `PGOPTIONS` 環境變數
（適用於允許此方式的設定）設定自訂的執行時期伺服器設定，
例如：

```

make check PGOPTIONS="-c debug_parallel_query=regress -c work_mem=50MB"
```

（這運用了 libpq 所提供的功能；詳情請參閱
[options](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNECT-OPTIONS)。）

當針對暫時安裝執行測試時，
也可以透過提供預先寫好的 `postgresql.conf`
來設定自訂設定：

```

echo 'log_checkpoints = on' > test_postgresql.conf
echo 'work_mem = 50MB' >> test_postgresql.conf
make check EXTRA_REGRESS_OPTS="--temp-config=test_postgresql.conf"
```

<a id="REGRESS-RUN-EXTRA-TESTS"></a>

### 31.1.6. 額外測試 [#](#REGRESS-RUN-EXTRA-TESTS)

核心迴歸測試套組中，含有少數幾個預設不會執行的測試檔案，
原因是它們可能與平台相依，或需要非常長的時間才能執行完畢。
你可以透過設定變數 `EXTRA_TESTS`，
執行這些或其他額外的測試檔案。例如，
若要執行 `numeric_big` 測試：

```

make check EXTRA_TESTS=numeric_big
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/regress-run.html)（原文版本：18.6；核對日期：2026-09-24）
