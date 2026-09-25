<a id="INSTALL-MAKE"></a>

## 17.3. 以 Autoconf 與 Make 建置與安裝 [#](#INSTALL-MAKE)

[17.3.1. 精簡版](install-make.md#INSTALL-SHORT-MAKE)

[17.3.2. 安裝程序](install-make.md#INSTALL-PROCEDURE-MAKE)

[17.3.3. `configure` 選項](install-make.md#CONFIGURE-OPTIONS)

[17.3.4. `configure` 環境變數](install-make.md#CONFIGURE-ENVVARS)

<a id="INSTALL-SHORT-MAKE"></a>

### 17.3.1. 精簡版 [#](#INSTALL-SHORT-MAKE)

```

./configure
make
su
make install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

完整版本請參閱本節其餘內容。

<a id="INSTALL-PROCEDURE-MAKE"></a>

### 17.3.2. 安裝程序 [#](#INSTALL-PROCEDURE-MAKE)

<a id="CONFIGURE"></a>1. **設定**

   <a id="id-1.6.4.6.3.2.1.2"></a>

   安裝程序的第一步，是針對你的系統設定原始碼樹，並選擇你想要的選項。
   這是透過執行 `configure` 指令稿來完成的。若要採用預設安裝方式，
   只需輸入：

   ```

   ./configure
   ```

   這個指令稿會執行一系列測試，以判斷各種與系統相依的變數值，
   並偵測你作業系統的任何特殊之處，最後會在建置樹中建立數個檔案，
   記錄它所偵測到的結果。

   如果你想讓建置目錄與原始檔案分開，也可以在原始碼樹以外的目錄
   執行 `configure`，然後在那裡進行建置。這個程序稱為
   <a id="id-1.6.4.6.3.2.1.4.2"></a>*VPATH*
   建置。作法如下：

   ```

   mkdir build_dir
   cd build_dir
   /path/to/source/tree/configure [options go here]
   make
   ```

   預設設定會建置伺服器與各項公用程式，以及所有只需要 C 編譯器
   即可建置的用戶端應用程式與介面。所有檔案預設都會安裝在
   `/usr/local/pgsql` 之下。

   你可以透過提供一或多個命令列選項給 `configure`，來自訂建置與
   安裝程序。一般來說，你可能會想自訂安裝位置，或是要建置的選用
   功能集合。`configure` 有大量選項，這些選項說明於
   [17.3.3 節](install-make.md#CONFIGURE-OPTIONS)。

   此外，`configure` 也會回應特定的環境變數，說明於
   [17.3.4 節](install-make.md#CONFIGURE-ENVVARS)。這些變數提供了
   額外的自訂設定方式。
<a id="BUILD"></a>2. **建置**

   若要開始建置，請輸入下列其中一項：

   ```

   make
   make all
   ```

   （請記得使用 GNU make。）
   依你的硬體而定，建置過程大約需要幾分鐘。

   如果你想要建置所有可以建置的內容，包括文件
   （HTML 與 man 頁面）以及額外模組（`contrib`），
   請改為輸入：

   ```

   make world
   ```

   如果你想要建置所有可以建置的內容，包括額外模組
   （`contrib`），但不包括文件，請改為輸入：

   ```

   make world-bin
   ```

   如果你想從另一個 makefile 呼叫這個建置，而不是手動執行，
   你必須取消設定 `MAKELEVEL`，或將其設為零，例如：

   ```

   build-postgresql:
           $(MAKE) -C postgresql MAKELEVEL=0 all
   ```

   若沒有這麼做，可能會導致奇怪的錯誤訊息出現，通常是關於
   缺少標頭檔的訊息。
3. **回歸測試**

   <a id="id-1.6.4.6.3.2.3.2"></a>

   如果你想在安裝之前先測試新建置好的伺服器，可以在此時執行
   回歸測試。回歸測試是一套測試組合，用來驗證 PostgreSQL
   在你的機器上是否如開發者所預期的那樣運作。輸入：

   ```

   make check
   ```

   （以 root 身分執行不會成功；請以非特權使用者執行。）
   關於如何解讀測試結果的詳細資訊，請參閱[第 31 章](../regress/README.md)。
   你可以在之後任何時候，透過重複輸入同一個指令來重新執行這項測試。
<a id="INSTALL"></a>4. **安裝檔案**

   ### 注意

   如果你正在升級既有系統，請務必閱讀
   [18.6 節](../runtime/upgrading.md)，
   其中有關於叢集升級的說明。

   若要安裝 PostgreSQL，請輸入：

   ```

   make install
   ```

   這會將檔案安裝到[步驟 1](install-make.md#CONFIGURE)中所指定的目錄。
   請確認你在該區域擁有適當的寫入權限。一般來說，這個步驟需要以
   root 身分執行。另外，你也可以事先建立目標目錄，並安排好適當的權限。

   若要安裝文件（HTML 與 man 頁面），請輸入：

   ```

   make install-docs
   ```

   如果你在前面建置了整個 world，請改為輸入：

   ```

   make install-world
   ```

   這也會一併安裝文件。

   如果你在前面建置了不含文件的 world，請改為輸入：

   ```

   make install-world-bin
   ```

   你可以使用 `make install-strip` 取代
   `make install`，在安裝時去除可執行檔與函式庫中的符號資訊。
   這樣可以節省一些空間。如果你在建置時啟用了除錯支援，
   去除符號資訊實際上會移除除錯支援，因此只有在確定不再需要
   除錯功能時才應該這麼做。`install-strip` 會嘗試合理地
   節省空間，但它並不具備完美的知識，能從可執行檔中去除每一個
   不需要的位元組，所以如果你想盡可能節省磁碟空間，就必須自行
   手動處理。

   標準安裝會提供用戶端應用程式開發，以及伺服器端程式開發
   （例如以 C 撰寫的自訂函式或資料型別）所需的所有標頭檔。

   **僅安裝用戶端：**
   如果你只想安裝用戶端應用程式與介面函式庫，可以使用下列指令：

   ```

   make -C src/bin install
   make -C src/include install
   make -C src/interfaces install
   make -C doc install
   ```

   `src/bin` 中有少數僅供伺服器端使用的二進位檔，
   但它們的體積都很小。

**解除安裝：**
若要復原安裝，請使用 `make uninstall` 指令。不過，這不會移除任何
已建立的目錄。

**清理：**
安裝完成後，你可以透過從原始碼樹中移除已建置的檔案，來釋放磁碟空間，
指令為 `make clean`。這會保留 `configure`
程式所產生的檔案，讓你之後可以用 `make` 重新建置全部內容。
若要將原始碼樹重設回發行時的狀態，請使用 `make distclean`。
如果你打算在同一個原始碼樹中為多個平台進行建置，就必須這麼做，
並針對每個平台重新設定。（另一種做法是為每個平台使用個別的建置目錄，
讓原始碼樹保持不變。）

如果你完成了一次建置後，才發現 `configure` 選項有誤，
或是你變更了任何 `configure` 會偵測的項目（例如軟體升級），
那麼在重新設定並重新建置之前，最好先執行 `make distclean`。
若不這麼做，你變更的設定選項可能無法傳遞到所有需要的地方。

<a id="CONFIGURE-OPTIONS"></a>

### 17.3.3. `configure` 選項 [#](#CONFIGURE-OPTIONS)

<a id="id-1.6.4.6.4.2"></a>

以下說明 `configure` 的命令列選項。這份清單並不完整
（使用 `./configure --help` 可取得完整清單）。
這裡未涵蓋的選項，是給交叉編譯等進階使用情境使用的，
它們記載於標準的 Autoconf 文件中。

<a id="CONFIGURE-OPTIONS-LOCATIONS"></a>

#### 17.3.3.1. 安裝位置 [#](#CONFIGURE-OPTIONS-LOCATIONS)

這些選項控制 `make install` 會將檔案放在何處。
對大多數情況而言，`--prefix` 選項就已足夠。
如果你有特殊需求，可以使用本節說明的其他選項自訂安裝子目錄。
不過要注意，變更各子目錄之間的相對位置，可能會讓安裝變得不可搬移，
意味著安裝完成後你將無法再移動它。
（`man` 與 `doc` 的位置不受此限制影響。）
若要建立可搬移的安裝，你可能會想使用稍後說明的
`--disable-rpath` 選項。

<a id="CONFIGURE-OPTION-PREFIX"></a>

`--prefix=PREFIX` [#](#CONFIGURE-OPTION-PREFIX)
:   將所有檔案安裝到目錄 *`PREFIX`* 之下，而不是
    `/usr/local/pgsql`。實際的檔案會被安裝到
    各個子目錄中；絕不會有檔案直接安裝在
    *`PREFIX`* 目錄本身。
<a id="CONFIGURE-OPTION-EXEC-PREFIX"></a>

`--exec-prefix=EXEC-PREFIX` [#](#CONFIGURE-OPTION-EXEC-PREFIX)
:   你可以將與架構相依的檔案安裝到與
    *`PREFIX`* 不同的前綴 *`EXEC-PREFIX`* 之下。
    這在多台主機之間共用與架構無關的檔案時很有用。
    如果省略這個選項，*`EXEC-PREFIX`* 會被設為與
    *`PREFIX`* 相同，與架構相依及不相依的檔案都會
    安裝在同一個目錄樹下，這通常是你想要的結果。
<a id="CONFIGURE-OPTION-BINDIR"></a>

`--bindir=DIRECTORY` [#](#CONFIGURE-OPTION-BINDIR)
:   指定可執行程式的目錄。預設值是
    `EXEC-PREFIX/bin`，通常也就是
    `/usr/local/pgsql/bin`。
<a id="CONFIGURE-OPTION-SYSCONFDIR"></a>

`--sysconfdir=DIRECTORY` [#](#CONFIGURE-OPTION-SYSCONFDIR)
:   設定各種設定檔所在的目錄，預設為
    `PREFIX/etc`。
<a id="CONFIGURE-OPTION-LIBDIR"></a>

`--libdir=DIRECTORY` [#](#CONFIGURE-OPTION-LIBDIR)
:   設定用來安裝函式庫與動態載入模組的位置。
    預設值為 `EXEC-PREFIX/lib`。
<a id="CONFIGURE-OPTION-INCLUDEDIR"></a>

`--includedir=DIRECTORY` [#](#CONFIGURE-OPTION-INCLUDEDIR)
:   設定安裝 C 與 C++ 標頭檔的目錄。
    預設值為 `PREFIX/include`。
<a id="CONFIGURE-OPTION-DATAROOTDIR"></a>

`--datarootdir=DIRECTORY` [#](#CONFIGURE-OPTION-DATAROOTDIR)
:   設定各類唯讀資料檔案的根目錄。
    這只會為以下部分選項設定預設值。預設值為
    `PREFIX/share`。
<a id="CONFIGURE-OPTION-DATADIR"></a>

`--datadir=DIRECTORY` [#](#CONFIGURE-OPTION-DATADIR)
:   設定已安裝程式所使用之唯讀資料檔案的目錄。
    預設值為 `DATAROOTDIR`。請注意，這與你的
    資料庫檔案存放位置無關。
<a id="CONFIGURE-OPTION-LOCALEDIR"></a>

`--localedir=DIRECTORY` [#](#CONFIGURE-OPTION-LOCALEDIR)
:   設定安裝地區設定（locale）資料的目錄，
    特別是訊息翻譯目錄檔。預設值為
    `DATAROOTDIR/locale`。
<a id="CONFIGURE-OPTION-MANDIR"></a>

`--mandir=DIRECTORY` [#](#CONFIGURE-OPTION-MANDIR)
:   PostgreSQL 隨附的 man 頁面會安裝在這個目錄下，
    分別放在各自對應的
    `manx` 子目錄中。
    預設值為 `DATAROOTDIR/man`。
<a id="CONFIGURE-OPTION-DOCDIR"></a>

`--docdir=DIRECTORY` [#](#CONFIGURE-OPTION-DOCDIR)
:   設定安裝文件檔案（「man」頁面除外）的根目錄。
    這只會為以下選項設定預設值。這個選項的
    預設值為 `DATAROOTDIR/doc/postgresql`。
<a id="CONFIGURE-OPTION-HTMLDIR"></a>

`--htmldir=DIRECTORY` [#](#CONFIGURE-OPTION-HTMLDIR)
:   PostgreSQL 的 HTML 格式文件會安裝在這個
    目錄下。預設值為
    `DATAROOTDIR`。

### 注意

已特別留意，讓 PostgreSQL 可以安裝到共用的安裝位置
（例如 `/usr/local/include`），而不會干擾系統其他部分的命名空間。
首先，字串「`/postgresql`」會自動附加到
`datadir`、`sysconfdir` 與 `docdir` 之後，
除非完整展開後的目錄名稱已經包含
「`postgres`」或「`pgsql`」字串。
舉例來說，如果你選擇 `/usr/local` 作為前綴，
文件會安裝在 `/usr/local/doc/postgresql`；
但如果前綴是 `/opt/postgres`，
文件則會安裝在 `/opt/postgres/doc`。
用戶端介面的公用 C 標頭檔會安裝到
`includedir`，且不會污染命名空間。
內部標頭檔與伺服器標頭檔則會安裝到
`includedir` 下的私有目錄。關於如何存取各介面的標頭檔，
請參閱各介面各自的文件。最後，如有需要，也會在
`libdir` 下建立一個私有子目錄，
用於存放動態載入模組。

<a id="CONFIGURE-OPTIONS-FEATURES"></a>

#### 17.3.3.2. PostgreSQL 功能 [#](#CONFIGURE-OPTIONS-FEATURES)

本節說明的選項可用來啟用建置各種預設不會建置的
PostgreSQL 功能。這些功能之所以非預設，大多是因為
它們需要額外的軟體，如
[17.1 節](install-requirements.md)所述。

<a id="CONFIGURE-OPTION-ENABLE-NLS"></a>

`--enable-nls[=LANGUAGES]` [#](#CONFIGURE-OPTION-ENABLE-NLS)
:   啟用原生語言支援（NLS，Native Language Support），
    即以非英文語言顯示程式訊息的能力。
    *`LANGUAGES`* 是一個選用、以空白分隔的語言代碼清單，
    用來指定你想要支援的語言，例如
    `--enable-nls='de fr'`。（你所列的清單與實際提供的
    翻譯集合之間的交集，會自動計算出來。）
    如果你沒有指定清單，則會安裝所有可用的翻譯。

    若要使用這個選項，你需要一套 Gettext API 的實作。
<a id="CONFIGURE-OPTION-WITH-PERL"></a>

`--with-perl` [#](#CONFIGURE-OPTION-WITH-PERL)
:   建置 PL/Perl 伺服器端語言。
<a id="CONFIGURE-OPTION-WITH-PYTHON"></a>

`--with-python` [#](#CONFIGURE-OPTION-WITH-PYTHON)
:   建置 PL/Python 伺服器端語言。
<a id="CONFIGURE-OPTION-WITH-TCL"></a>

`--with-tcl` [#](#CONFIGURE-OPTION-WITH-TCL)
:   建置 PL/Tcl 伺服器端語言。
<a id="CONFIGURE-OPTION-WITH-TCLCONFIG"></a>

`--with-tclconfig=DIRECTORY` [#](#CONFIGURE-OPTION-WITH-TCLCONFIG)
:   Tcl 會安裝 `tclConfig.sh` 檔案，其中包含
    建置介接 Tcl 的模組所需的設定資訊。這個檔案通常會
    在一個已知的固定位置自動被找到，但如果你想使用不同版本的
    Tcl，可以指定要尋找
    `tclConfig.sh` 的目錄。
<a id="CONFIGURE-WITH-LLVM"></a>

`--with-llvm` [#](#CONFIGURE-WITH-LLVM)
:   建置時支援以 LLVM 為基礎的 JIT 編譯
    （見[第 30 章](../jit/README.md)）。
    這需要安裝 LLVM 函式庫。
    目前所需的最低 LLVM 版本為 14。

    系統會使用 `llvm-config`<a id="id-1.6.4.6.4.5.3.6.2.2.2"></a>
    來尋找所需的編譯選項。
    系統會在 `PATH` 中搜尋 `llvm-config`。
    如果這樣找不到你想要的程式，
    可以使用 `LLVM_CONFIG` 指定正確
    `llvm-config` 的路徑。例如：

    ```

    ./configure ... --with-llvm LLVM_CONFIG='/path/to/llvm/bin/llvm-config'
    ```

    LLVM 支援需要相容的
    `clang` 編譯器（如有需要，可透過
    `CLANG` 環境變數指定），以及一套可運作的 C++
    編譯器（如有需要，可透過 `CXX`
    環境變數指定）。
<a id="CONFIGURE-OPTION-WITH-LZ4"></a>

`--with-lz4` [#](#CONFIGURE-OPTION-WITH-LZ4)
:   建置時支援 LZ4 壓縮。
<a id="CONFIGURE-OPTION-WITH-ZSTD"></a>

`--with-zstd` [#](#CONFIGURE-OPTION-WITH-ZSTD)
:   建置時支援 Zstandard 壓縮。
<a id="CONFIGURE-OPTION-WITH-SSL"></a>

`--with-ssl=LIBRARY` <a id="id-1.6.4.6.4.5.3.9.1.2"></a> [#](#CONFIGURE-OPTION-WITH-SSL)
:   建置時支援 SSL（加密）連線。
    目前唯一支援的 *`LIBRARY`* 是
    `openssl`，可同時用於
    OpenSSL 與 LibreSSL。
    這需要安裝 OpenSSL 套件。
    `configure` 會檢查所需的標頭檔與函式庫，
    確保你的 OpenSSL 安裝符合需求後才會繼續。
<a id="CONFIGURE-OPTION-WITH-OPENSSL"></a>

`--with-openssl` [#](#CONFIGURE-OPTION-WITH-OPENSSL)
:   `--with-ssl=openssl` 的過時等效選項。
<a id="CONFIGURE-OPTION-WITH-GSSAPI"></a>

`--with-gssapi` [#](#CONFIGURE-OPTION-WITH-GSSAPI)
:   建置時支援 GSSAPI 驗證。使用 GSSAPI 需要安裝
    MIT Kerberos。在許多系統上，GSSAPI 系統
    （屬於 MIT Kerberos 安裝的一部分）並未安裝在
    預設會被搜尋的位置（例如 `/usr/include`、
    `/usr/lib`），因此除了這個選項之外，
    你還必須使用 `--with-includes` 與
    `--with-libraries` 選項。
    `configure` 會檢查所需的標頭檔與函式庫，
    確保你的 GSSAPI 安裝符合需求後才會繼續。
<a id="CONFIGURE-OPTION-WITH-LDAP"></a>

`--with-ldap` [#](#CONFIGURE-OPTION-WITH-LDAP)
:   建置時支援 LDAP<a id="id-1.6.4.6.4.5.3.12.2.1.2"></a>
    驗證與連線參數查詢（詳見
    <a id="INSTALL-LDAP-LINKS"></a>[32.18 節](../../client-interfaces/libpq/libpq-ldap.md)與
    [20.10 節](../client-authentication/auth-ldap.md)以取得更多資訊）。
    在 Unix 上，這需要安裝 OpenLDAP 套件。
    在 Windows 上，則使用預設的 WinLDAP
    函式庫。`configure` 會檢查所需的標頭檔與函式庫，
    確保你的 OpenLDAP 安裝符合需求後才會繼續。
<a id="CONFIGURE-OPTION-WITH-PAM"></a>

`--with-pam` [#](#CONFIGURE-OPTION-WITH-PAM)
:   建置時支援 PAM<a id="id-1.6.4.6.4.5.3.13.2.1.2"></a>
    （Pluggable Authentication Modules，可插拔驗證模組）。
<a id="CONFIGURE-OPTION-WITH-BSD-AUTH"></a>

`--with-bsd-auth` [#](#CONFIGURE-OPTION-WITH-BSD-AUTH)
:   建置時支援 BSD Authentication。
    （BSD Authentication 框架目前僅在 OpenBSD 上可用。）
<a id="CONFIGURE-OPTION-WITH-SYSTEMD"></a>

`--with-systemd` [#](#CONFIGURE-OPTION-WITH-SYSTEMD)
:   建置時支援
    systemd<a id="id-1.6.4.6.4.5.3.15.2.1.2"></a>
    服務通知。如果伺服器是在 systemd 之下啟動，
    這能改善整合效果，但在其他情況下沒有影響；
    詳見[18.3 節](../runtime/server-start.md)以取得更多資訊。
    必須安裝 libsystemd 及其相關標頭檔，
    才能使用這個選項。
<a id="CONFIGURE-OPTION-WITH-BONJOUR"></a>

`--with-bonjour` [#](#CONFIGURE-OPTION-WITH-BONJOUR)
:   建置時支援 Bonjour 自動服務探索。
    這需要你的作業系統支援 Bonjour。
    在 macOS 上建議啟用。
<a id="CONFIGURE-OPTION-WITH-UUID"></a>

`--with-uuid=LIBRARY` [#](#CONFIGURE-OPTION-WITH-UUID)
:   使用指定的 UUID 函式庫，建置
    [uuid-ossp](../../appendixes/contrib/uuid-ossp.md) 模組
    （提供產生 UUID 的函式）。<a id="id-1.6.4.6.4.5.3.17.2.1.2"></a>
    *`LIBRARY`* 必須是下列其中之一：

    * `bsd`：使用 FreeBSD 及其他部分 BSD 衍生系統中的
      UUID 函式
    * `e2fs`：使用由 `e2fsprogs` 專案建立的
      UUID 函式庫；這個函式庫存在於多數 Linux 系統及
      macOS 中，其他平台也可以取得
    * `ossp`：使用 [OSSP UUID 函式庫](http://www.ossp.org/pkg/lib/uuid/)
<a id="CONFIGURE-OPTION-WITH-OSSP-UUID"></a>

`--with-ossp-uuid` [#](#CONFIGURE-OPTION-WITH-OSSP-UUID)
:   `--with-uuid=ossp` 的過時等效選項。
<a id="CONFIGURE-OPTION-WITH-LIBCURL"></a>

`--with-libcurl` [#](#CONFIGURE-OPTION-WITH-LIBCURL)
:   建置時支援以 libcurl 執行 OAuth 2.0 用戶端流程。
    這項功能需要 libcurl 7.61.0 以上版本。
    以此選項建置時，會先檢查所需的標頭檔與函式庫，
    確保你的 curl 安裝符合需求後才會繼續。
<a id="CONFIGURE-OPTION-WITH-LIBNUMA"></a>

`--with-libnuma` [#](#CONFIGURE-OPTION-WITH-LIBNUMA)
:   建置時支援 libnuma，以提供基本的 NUMA 支援。
    僅支援已實作 libnuma 函式庫的平台。
<a id="CONFIGURE-OPTION-WITH-LIBURING"></a>

`--with-liburing` [#](#CONFIGURE-OPTION-WITH-LIBURING)
:   建置時支援 liburing，啟用 io_uring 非同步 I/O 支援。

    為偵測所需的編譯器與連結器選項，PostgreSQL 會查詢
    `pkg-config`。

    若要使用位於非一般位置的 liburing 安裝，
    你可以設定與 `pkg-config` 相關的環境變數
    （詳見其文件）。
<a id="CONFIGURE-OPTION-WITH-LIBXML"></a>

`--with-libxml` [#](#CONFIGURE-OPTION-WITH-LIBXML)
:   建置時使用 libxml2，啟用 SQL/XML 支援。這項功能需要
    Libxml2 2.6.23 以上版本。

    為偵測所需的編譯器與連結器選項，PostgreSQL 會查詢
    `pkg-config`（如果已安裝且認得 libxml2 的話）。
    否則會使用由 libxml2 隨附安裝的
    `xml2-config` 程式（如果能找到的話）。
    建議優先使用 `pkg-config`，因為它能更妥善地
    處理多架構安裝的情況。

    若要使用位於非一般位置的 libxml2 安裝，
    你可以設定與 `pkg-config` 相關的環境變數
    （詳見其文件），或是將環境變數
    `XML2_CONFIG` 設為指向屬於該 libxml2 安裝的
    `xml2-config` 程式，或是設定
    `XML2_CFLAGS` 與 `XML2_LIBS`
    這兩個變數。（如果已安裝 `pkg-config`，
    若要覆寫它對 libxml2 位置的判斷，你必須
    設定 `XML2_CONFIG`，或是同時將
    `XML2_CFLAGS` 與 `XML2_LIBS` 設為非空字串。）
<a id="CONFIGURE-OPTION-WITH-LIBXSLT"></a>

`--with-libxslt` [#](#CONFIGURE-OPTION-WITH-LIBXSLT)
:   建置時使用 libxslt，讓
    [xml2](../../appendixes/contrib/xml2.md)
    模組能執行 XML 的 XSL 轉換。
    必須同時指定 `--with-libxml`。
<a id="CONFIGURE-OPTION-WITH-SEPGSQL"></a>

`--with-selinux` [#](#CONFIGURE-OPTION-WITH-SEPGSQL)
:   建置時支援 SElinux，啟用
    [sepgsql](../../appendixes/contrib/sepgsql.md) 擴充功能。

<a id="CONFIGURE-OPTIONS-ANTI-FEATURES"></a>

#### 17.3.3.3. 反功能 [#](#CONFIGURE-OPTIONS-ANTI-FEATURES)

本節說明的選項，可用來停用預設會建置的
特定 PostgreSQL 功能；如果所需的軟體或系統功能不可用，
可能就需要關閉它們。除非真的有必要，否則不建議使用這些選項。

<a id="CONFIGURE-OPTION-WITHOUT-ICU"></a>

`--without-icu` [#](#CONFIGURE-OPTION-WITHOUT-ICU)
:   建置時不支援
    ICU<a id="id-1.6.4.6.4.6.3.1.2.1.2"></a>
    函式庫，停用 ICU 定序功能（見[23.2 節](../charset/collation.md)）。
<a id="CONFIGURE-OPTION-WITHOUT-READLINE"></a>

`--without-readline` [#](#CONFIGURE-OPTION-WITHOUT-READLINE)
:   將不使用 Readline 函式庫
    （也包含 libedit）。這個選項會停用
    psql 的命令列編輯與歷史紀錄功能。
<a id="CONFIGURE-OPTION-WITH-LIBEDIT-PREFERRED"></a>

`--with-libedit-preferred` [#](#CONFIGURE-OPTION-WITH-LIBEDIT-PREFERRED)
:   優先使用 BSD 授權的 libedit 函式庫，
    而非 GPL 授權的 Readline。只有在你同時安裝了
    兩套函式庫時，這個選項才有意義；在這種情況下，
    預設會使用 Readline。
<a id="CONFIGURE-OPTION-WITHOUT-ZLIB"></a>

`--without-zlib` [#](#CONFIGURE-OPTION-WITHOUT-ZLIB)
:   <a id="id-1.6.4.6.4.6.3.4.2.1.1"></a>
    將不使用 Zlib 函式庫。
    這會停用 pg_dump 與 pg_restore
    對壓縮封存檔的支援。

<a id="CONFIGURE-OPTIONS-BUILD-PROCESS"></a>

#### 17.3.3.4. 建置程序細節 [#](#CONFIGURE-OPTIONS-BUILD-PROCESS)

<a id="CONFIGURE-OPTION-WITH-INCLUDES"></a>

`--with-includes=DIRECTORIES` [#](#CONFIGURE-OPTION-WITH-INCLUDES)
:   *`DIRECTORIES`* 是一份以冒號分隔的目錄清單，
    會被加入編譯器搜尋標頭檔的目錄清單中。
    如果你有選用套件（例如 GNU Readline）
    安裝在非標準位置，
    就必須使用這個選項，通常也需要搭配對應的
    `--with-libraries` 選項。

    範例：`--with-includes=/opt/gnu/include:/usr/sup/include`。
<a id="CONFIGURE-OPTION-WITH-LIBRARIES"></a>

`--with-libraries=DIRECTORIES` [#](#CONFIGURE-OPTION-WITH-LIBRARIES)
:   *`DIRECTORIES`* 是一份以冒號分隔的目錄清單，
    用來搜尋函式庫。如果你的套件安裝在非標準位置，
    你很可能需要使用這個選項（以及對應的
    `--with-includes` 選項）。

    範例：`--with-libraries=/opt/gnu/lib:/usr/sup/lib`。
<a id="CONFIGURE-OPTION-WITH-SYSTEM-TZDATA"></a>

`--with-system-tzdata=DIRECTORY` <a id="id-1.6.4.6.4.7.2.3.1.2"></a> [#](#CONFIGURE-OPTION-WITH-SYSTEM-TZDATA)
:   PostgreSQL 內含自己的時區資料庫，
    這是日期與時間運算所需要的。這個時區資料庫
    事實上與許多作業系統（例如 FreeBSD、Linux 與 Solaris）
    所提供的 IANA 時區資料庫相容，因此再安裝一次會顯得多餘。
    使用這個選項時，會改用位於 *`DIRECTORY`*
    的系統提供的時區資料庫，而不使用
    PostgreSQL 原始碼發行版中內含的資料庫。
    *`DIRECTORY`* 必須以絕對路徑指定。
    在部分作業系統上，`/usr/share/zoneinfo`
    是可能的目錄位置。請注意，安裝程序並不會偵測
    時區資料是否有不符或錯誤。如果你使用這個選項，
    建議執行回歸測試，以確認你所指向的時區資料
    能與 PostgreSQL 正確搭配運作。

    <a id="id-1.6.4.6.4.7.2.3.2.2"></a>

    這個選項主要是為熟悉目標作業系統的二進位套件
    發行者所設計。使用這個選項的主要好處，是每當
    許多地方性日光節約時間規則有所變動時，
    PostgreSQL 套件都不需要重新升級。另一項好處是，
    如果不需要在安裝期間建置時區資料庫檔案，
    PostgreSQL 就可以更直接地進行交叉編譯。
<a id="CONFIGURE-OPTION-WITH-EXTRA-VERSION"></a>

`--with-extra-version=STRING` [#](#CONFIGURE-OPTION-WITH-EXTRA-VERSION)
:   將 *`STRING`* 附加到 PostgreSQL 版本號後面。
    舉例來說，你可以用這個選項，為由未發行的 Git 快照
    建置出來的二進位檔，或是含有自訂修補程式的二進位檔，
    加上額外的版本字串，例如
    `git describe` 識別碼，或是發行套件的版本編號。
<a id="CONFIGURE-OPTION-DISABLE-RPATH"></a>

`--disable-rpath` [#](#CONFIGURE-OPTION-DISABLE-RPATH)
:   不在 PostgreSQL 的可執行檔中加上標記，
    指示它們應在安裝的函式庫目錄中（見 `--libdir`）
    搜尋共用函式庫。在多數平台上，這項標記使用的是
    函式庫目錄的絕對路徑，因此如果你之後搬移了安裝位置，
    這項標記就沒有幫助。不過，如此一來你就需要提供
    其他方式，讓可執行檔能找到共用函式庫。
    一般來說，這需要設定作業系統的動態連結器，
    使其搜尋該函式庫目錄；詳見
    [17.5.1 節](install-post.md#INSTALL-POST-SHLIBS)以取得更多細節。

<a id="CONFIGURE-OPTIONS-MISC"></a>

#### 17.3.3.5. 其他 [#](#CONFIGURE-OPTIONS-MISC)

尤其對測試性建置而言，調整預設埠號
（透過 `--with-pgport`）是相當常見的做法。
本節中的其他選項，建議只有進階使用者才使用。

<a id="CONFIGURE-OPTION-WITH-PGPORT"></a>

`--with-pgport=NUMBER` [#](#CONFIGURE-OPTION-WITH-PGPORT)
:   將 *`NUMBER`* 設為伺服器與用戶端的預設埠號。
    預設值為 5432。這個埠號日後隨時可以變更，
    但如果你在這裡指定，伺服器與用戶端就會編譯進相同的
    預設值，這會非常方便。通常唯一需要選擇非預設值的
    好理由，是你打算在同一台機器上執行多個
    PostgreSQL 伺服器。
<a id="CONFIGURE-OPTION-WITH-KRB-SRVNAM"></a>

`--with-krb-srvnam=NAME` [#](#CONFIGURE-OPTION-WITH-KRB-SRVNAM)
:   GSSAPI 使用的 Kerberos 服務主體預設名稱。
    預設值為 `postgres`。除非你是在為 Windows
    環境建置，否則通常沒有理由變更這個值；
    如果是的話，就必須設為大寫的
    `POSTGRES`。
<a id="CONFIGURE-OPTION-WITH-SEGSIZE"></a>

`--with-segsize=SEGSIZE` [#](#CONFIGURE-OPTION-WITH-SEGSIZE)
:   設定*區段大小（segment size）*，單位為 GB。
    大型資料表會被切割成多個作業系統檔案，每個檔案的
    大小等於區段大小。這樣可以避免許多平台上存在的
    檔案大小限制問題。預設的區段大小為 1 GB，
    在所有受支援的平台上都是安全的。如果你的作業系統支援
    「大檔案（largefile）」（現今大多數系統都支援），
    你就可以使用更大的區段大小。這有助於減少處理極大型
    資料表時所消耗的檔案描述元數量。不過要小心，
    不要選擇超過你的平台與所使用檔案系統所支援的值。
    你可能會使用的其他工具，例如 tar，
    也可能會對可用的檔案大小設下限制。
    建議（雖非絕對必要）將這個值設為 2 的冪次方。
    請注意，變更這個值會破壞磁碟上的資料庫相容性，
    也就是說，你將無法使用 `pg_upgrade`
    升級到採用不同區段大小的建置版本。
<a id="CONFIGURE-OPTION-WITH-BLOCKSIZE"></a>

`--with-blocksize=BLOCKSIZE` [#](#CONFIGURE-OPTION-WITH-BLOCKSIZE)
:   設定*區塊大小（block size）*，單位為 KB。
    這是資料表內部儲存與 I/O 的單位。
    預設值 8 KB 適用於大多數情況，
    但在特殊情況下，其他數值可能有幫助。
    這個值必須是 1 到 32（KB）之間的 2 的冪次方。
    請注意，變更這個值會破壞磁碟上的資料庫相容性，
    也就是說，你將無法使用 `pg_upgrade`
    升級到採用不同區塊大小的建置版本。
<a id="CONFIGURE-OPTION-WITH-WAL-BLOCKSIZE"></a>

`--with-wal-blocksize=BLOCKSIZE` [#](#CONFIGURE-OPTION-WITH-WAL-BLOCKSIZE)
:   設定 *WAL 區塊大小*，單位為 KB。
    這是 WAL 記錄內部儲存與 I/O 的單位。
    預設值 8 KB 適用於大多數情況，
    但在特殊情況下，其他數值可能有幫助。
    這個值必須是 1 到 64（KB）之間的 2 的冪次方。
    請注意，變更這個值會破壞磁碟上的資料庫相容性，
    也就是說，你將無法使用 `pg_upgrade`
    升級到採用不同 WAL 區塊大小的建置版本。

<a id="CONFIGURE-OPTIONS-DEVEL"></a>

#### 17.3.3.6. 開發者選項 [#](#CONFIGURE-OPTIONS-DEVEL)

本節大多數選項主要是供開發或除錯 PostgreSQL 時使用。
除了 `--enable-debug` 之外，其餘選項都不建議用於
正式環境的建置——這個選項在你不幸遇到
臭蟲時，有助於啟用詳細的錯誤回報。
在支援 DTrace 的平台上，`--enable-dtrace`
在正式環境中使用也算合理。

如果你要建置一套用來在伺服器內部開發程式碼的安裝，
建議至少使用 `--enable-debug`
與 `--enable-cassert` 這兩個選項。

<a id="CONFIGURE-OPTION-ENABLE-DEBUG"></a>

`--enable-debug` [#](#CONFIGURE-OPTION-ENABLE-DEBUG)
:   以除錯符號編譯所有程式與函式庫。
    這代表你可以在除錯工具中執行這些程式，以分析問題。
    這會大幅增加已安裝可執行檔的大小，而且在非 GCC 的
    編譯器上，通常也會停用編譯器最佳化，導致執行速度變慢。
    不過，能取得符號資訊，對處理任何可能發生的問題
    非常有幫助。目前，只有在你使用 GCC 時，才建議在
    正式環境安裝中使用這個選項。但如果你正在進行開發工作，
    或執行的是 beta 版本，就應該一律啟用它。
<a id="CONFIGURE-OPTION-ENABLE-CASSERT"></a>

`--enable-cassert` [#](#CONFIGURE-OPTION-ENABLE-CASSERT)
:   啟用伺服器中的*斷言（assertion）*檢查，這會測試許多
    「不應該發生」的情況。這對程式碼開發而言相當寶貴，
    但這些測試可能會明顯拖慢伺服器速度。
    此外，開啟這些測試並不必然能提升伺服器的穩定性！
    斷言檢查並未依嚴重程度分類，因此即使是相對無害的錯誤，
    只要觸發斷言失敗，仍然會導致伺服器重新啟動。
    這個選項不建議用於正式環境，但在開發工作或執行 beta 版本時，
    應該要啟用它。
<a id="CONFIGURE-OPTION-ENABLE-TAP-TESTS"></a>

`--enable-tap-tests` [#](#CONFIGURE-OPTION-ENABLE-TAP-TESTS)
:   啟用使用 Perl TAP 工具的測試。這需要安裝 Perl，
    以及 Perl 模組 `IPC::Run`。
    詳見[31.4 節](../regress/regress-tap.md)以取得更多資訊。
<a id="CONFIGURE-OPTION-ENABLE-DEPEND"></a>

`--enable-depend` [#](#CONFIGURE-OPTION-ENABLE-DEPEND)
:   啟用自動相依性追蹤。使用這個選項時，makefile
    會被設定為：當任何標頭檔變更時，所有受影響的物件檔
    都會重新建置。如果你正在進行開發工作，這會很有用，
    但如果你只打算編譯一次然後安裝，這就只是多餘的負擔。
    目前，這個選項只能搭配 GCC 使用。
<a id="CONFIGURE-OPTION-ENABLE-COVERAGE"></a>

`--enable-coverage` [#](#CONFIGURE-OPTION-ENABLE-COVERAGE)
:   如果使用 GCC，所有程式與函式庫都會加上程式碼涵蓋率
    測試的檢測工具進行編譯。執行時，它們會在建置目錄中
    產生含有程式碼涵蓋率統計資料的檔案。
    詳見[31.5 節](../regress/regress-coverage.md)以取得
    更多資訊。這個選項僅適用於 GCC，且僅在進行開發工作時使用。
<a id="CONFIGURE-OPTION-ENABLE-PROFILING"></a>

`--enable-profiling` [#](#CONFIGURE-OPTION-ENABLE-PROFILING)
:   如果使用 GCC，所有程式與函式庫都會以可供效能剖析
    （profiling）的方式編譯。後端結束時，會建立一個子目錄，
    其中含有記錄效能剖析資料的
    `gmon.out` 檔案。
    這個選項僅適用於 GCC，且僅在進行開發工作時使用。
<a id="CONFIGURE-OPTION-ENABLE-DTRACE"></a>

`--enable-dtrace` [#](#CONFIGURE-OPTION-ENABLE-DTRACE)
:   <a id="id-1.6.4.6.4.9.4.7.2.1.1"></a>
    編譯 PostgreSQL 時支援動態追蹤工具
    DTrace。
    詳見[27.5 節](../monitoring/dynamic-trace.md)以取得更多資訊。

    你可以設定環境變數 `DTRACE`，
    來指向 `dtrace` 程式。
    這通常是必要的，因為 `dtrace`
    一般安裝於 `/usr/sbin`，
    可能不在你的 `PATH` 之中。

    可以在環境變數 `DTRACEFLAGS` 中，
    指定要傳給 `dtrace` 程式的額外命令列選項。
    在 Solaris 上，若要在 64 位元二進位檔中納入 DTrace 支援，
    你必須指定
    `DTRACEFLAGS="-64"`。例如，
    使用 GCC 編譯器時：

    ```

    ./configure CC='gcc -m64' --enable-dtrace DTRACEFLAGS='-64' ...
    ```

    使用 Sun 的編譯器時：

    ```

    ./configure CC='/opt/SUNWspro/bin/cc -xtarget=native64' --enable-dtrace DTRACEFLAGS='-64' ...
    ```
<a id="CONFIGURE-OPTION-ENABLE-INJECTION-POINTS"></a>

`--enable-injection-points` [#](#CONFIGURE-OPTION-ENABLE-INJECTION-POINTS)
:   編譯 PostgreSQL 時支援伺服器內部的注入點
    （injection points）。注入點允許在伺服器內部預先定義的
    程式碼路徑中，執行使用者自訂的程式碼。這有助於
    以可控制的方式進行測試，以及調查並行情境。
    這個選項預設為停用。詳見
    [36.10.14 節](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)
    以取得更多細節。這個選項僅供開發人員在測試時使用。
<a id="CONFIGURE-OPTION-WITH-SEGSIZE-BLOCKS"></a>

`--with-segsize-blocks=SEGSIZE_BLOCKS` [#](#CONFIGURE-OPTION-WITH-SEGSIZE-BLOCKS)
:   以區塊為單位，指定關聯（relation）的區段大小。
    如果同時指定了 `--with-segsize` 與這個選項，
    以這個選項為準。
    這個選項僅供開發人員用來測試與區段相關的程式碼。

<a id="CONFIGURE-ENVVARS"></a>

### 17.3.4. `configure` 環境變數 [#](#CONFIGURE-ENVVARS)

<a id="id-1.6.4.6.5.2"></a>

除了上面說明的一般命令列選項之外，
`configure` 也會回應一些環境變數。
你可以在 `configure` 命令列中指定環境變數，例如：

```

./configure CC=/opt/bin/gcc CFLAGS='-O2 -pipe'
```

以這種方式使用時，環境變數與命令列選項幾乎沒有差別。
你也可以事先設定這類變數：

```

export CC=/opt/bin/gcc
export CFLAGS='-O2 -pipe'
./configure
```

這種用法很方便，因為許多程式的設定指令稿，
都以類似的方式回應這些變數。

這些環境變數中最常用的是
`CC` 與 `CFLAGS`。
如果你偏好使用與 `configure`
所選擇不同的 C 編譯器，可以將變數 `CC`
設為你選擇的程式。預設情況下，`configure`
會優先選用可用的 `gcc`，若無則使用該平台的
預設編譯器（通常是 `cc`）。同樣地，
如有需要，你也可以透過 `CFLAGS` 變數
覆寫預設的編譯器旗標。

以下是可以用這種方式設定的重要變數清單：

<a id="CONFIGURE-ENVVARS-BISON"></a>

`BISON` [#](#CONFIGURE-ENVVARS-BISON)
:   Bison 程式
<a id="CONFIGURE-ENVVARS-CC"></a>

`CC` [#](#CONFIGURE-ENVVARS-CC)
:   C 編譯器
<a id="CONFIGURE-ENVVARS-CFLAGS"></a>

`CFLAGS` [#](#CONFIGURE-ENVVARS-CFLAGS)
:   要傳給 C 編譯器的選項
<a id="CONFIGURE-ENVVARS-CLANG"></a>

`CLANG` [#](#CONFIGURE-ENVVARS-CLANG)
:   使用 `--with-llvm` 編譯時，
    用來處理原始碼以進行內嵌（inlining）的
    `clang` 程式路徑
<a id="CONFIGURE-ENVVARS-CPP"></a>

`CPP` [#](#CONFIGURE-ENVVARS-CPP)
:   C 前置處理器
<a id="CONFIGURE-ENVVARS-CPPFLAGS"></a>

`CPPFLAGS` [#](#CONFIGURE-ENVVARS-CPPFLAGS)
:   要傳給 C 前置處理器的選項
<a id="CONFIGURE-ENVVARS-CXX"></a>

`CXX` [#](#CONFIGURE-ENVVARS-CXX)
:   C++ 編譯器
<a id="CONFIGURE-ENVVARS-CXXFLAGS"></a>

`CXXFLAGS` [#](#CONFIGURE-ENVVARS-CXXFLAGS)
:   要傳給 C++ 編譯器的選項
<a id="CONFIGURE-ENVVARS-DTRACE"></a>

`DTRACE` [#](#CONFIGURE-ENVVARS-DTRACE)
:   `dtrace` 程式的位置
<a id="CONFIGURE-ENVVARS-DTRACEFLAGS"></a>

`DTRACEFLAGS` [#](#CONFIGURE-ENVVARS-DTRACEFLAGS)
:   要傳給 `dtrace` 程式的選項
<a id="CONFIGURE-ENVVARS-FLEX"></a>

`FLEX` [#](#CONFIGURE-ENVVARS-FLEX)
:   Flex 程式
<a id="CONFIGURE-ENVVARS-LDFLAGS"></a>

`LDFLAGS` [#](#CONFIGURE-ENVVARS-LDFLAGS)
:   連結可執行檔或共用函式庫時要使用的選項
<a id="CONFIGURE-ENVVARS-LDFLAGS-EX"></a>

`LDFLAGS_EX` [#](#CONFIGURE-ENVVARS-LDFLAGS-EX)
:   僅用於連結可執行檔的額外選項
<a id="CONFIGURE-ENVVARS-LDFLAGS-SL"></a>

`LDFLAGS_SL` [#](#CONFIGURE-ENVVARS-LDFLAGS-SL)
:   僅用於連結共用函式庫的額外選項
<a id="CONFIGURE-ENVVARS-LLVM-CONFIG"></a>

`LLVM_CONFIG` [#](#CONFIGURE-ENVVARS-LLVM-CONFIG)
:   用來找出 LLVM 安裝位置的
    `llvm-config` 程式
<a id="CONFIGURE-ENVVARS-MSGFMT"></a>

`MSGFMT` [#](#CONFIGURE-ENVVARS-MSGFMT)
:   用於原生語言支援的 `msgfmt` 程式
<a id="CONFIGURE-ENVVARS-PERL"></a>

`PERL` [#](#CONFIGURE-ENVVARS-PERL)
:   Perl 直譯器程式。這會用來判斷建置 PL/Perl
    所需的相依套件。預設值為
    `perl`。
<a id="CONFIGURE-ENVVARS-PYTHON"></a>

`PYTHON` [#](#CONFIGURE-ENVVARS-PYTHON)
:   Python 直譯器程式。這會用來判斷建置 PL/Python
    所需的相依套件。如果未設定，會依序偵測
    `python3 python`。
<a id="CONFIGURE-ENVVARS-TCLSH"></a>

`TCLSH` [#](#CONFIGURE-ENVVARS-TCLSH)
:   Tcl 直譯器程式。這會用來
    判斷建置 PL/Tcl 所需的相依套件。
    如果未設定，會依序偵測：`tclsh tcl tclsh8.6 tclsh86 tclsh8.5 tclsh85
    tclsh8.4 tclsh84`。
<a id="CONFIGURE-ENVVARS-XML2-CONFIG"></a>

`XML2_CONFIG` [#](#CONFIGURE-ENVVARS-XML2-CONFIG)
:   用來找出 libxml2 安裝位置的
    `xml2-config` 程式

有時候，在 `configure` 選定的編譯選項之外，
事後再加上額外的編譯器旗標會很有用。一個重要的例子是，
gcc 的 `-Werror` 選項不能包含在傳給
`configure` 的 `CFLAGS` 中，
因為這會破壞 `configure` 內建的許多測試。
若要加上這類旗標，請在執行 `make` 時，
將它們放入 `COPT` 環境變數。
`COPT` 的內容，會被加入
`configure` 所設定的 `CFLAGS`、`CXXFLAGS` 與 `LDFLAGS`
選項中。例如，你可以這麼做：

```

make COPT='-Werror'
```

或者：

```

export COPT='-Werror'
make
```

### 注意

如果使用 GCC，建議至少以
`-O1` 的最佳化等級進行建置，因為不進行最佳化
（`-O0`）會停用一些重要的編譯器警告
（例如使用未初始化變數的警告）。不過，非零的最佳化等級
可能會讓除錯變得更複雜，因為逐步執行已編譯的程式碼時，
通常無法與原始碼的行數一一對應。如果你在嘗試除錯
最佳化過的程式碼時感到困惑，可以針對你感興趣的特定檔案，
以 `-O0` 重新編譯。一個簡單的做法，
是透過傳給 make 的選項來執行：
`make PROFILE=-O0 file.o`。

`COPT` 與 `PROFILE` 這兩個環境變數，
在 PostgreSQL 的各個 makefile 中實際上是以相同方式處理的。
要使用哪一個純屬個人偏好，但開發者之間常見的習慣，
是以 `PROFILE` 進行一次性的旗標調整，
而 `COPT` 則可能會一直保持設定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/install-make.html)（原文版本：18.6；核對日期：2026-09-26）
