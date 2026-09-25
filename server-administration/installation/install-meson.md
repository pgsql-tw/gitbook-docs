<a id="INSTALL-MESON"></a>

## 17.4. 使用 Meson 建置與安裝 [#](#INSTALL-MESON)

[17.4.1. 簡短版本](install-meson.md#INSTALL-SHORT-MESON)

[17.4.2. 安裝程序](install-meson.md#INSTALL-PROCEDURE-MESON)

[17.4.3. `meson setup` 選項](install-meson.md#MESON-OPTIONS)

[17.4.4. `meson` 建置目標](install-meson.md#TARGETS-MESON)

<a id="INSTALL-SHORT-MESON"></a>

### 17.4.1. 簡短版本 [#](#INSTALL-SHORT-MESON)

```

meson setup build --prefix=/usr/local/pgsql
cd build
ninja
su
ninja install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

完整版說明請見本節其餘的內容。

<a id="INSTALL-PROCEDURE-MESON"></a>

### 17.4.2. 安裝程序 [#](#INSTALL-PROCEDURE-MESON)

<a id="MESON-CONFIGURE"></a>1. **設定**

   安裝程序的第一步，是為你的系統設定建置樹（build tree），並選擇你想要的選項。你可以使用
   `meson setup` 指令，來建立並設定建置目錄。

   ```

   meson setup build
   ```

   setup 指令會接受 `builddir` 與 `srcdir`
   兩個參數。若未指定 `srcdir`，Meson 會根據目前所在的目錄以及
   `meson.build` 的位置來推斷 `srcdir`。`builddir`
   則是必要參數。

   執行 `meson setup` 會載入建置設定檔並準備好建置目錄。
   此外，你也可以傳入多個建置選項給 Meson。以下各小節會提到一些常用的
   選項，舉例來說：

   ```

   # configure with a different installation prefix
   meson setup build --prefix=/home/user/pg-install

   # configure to generate a debug build
   meson setup build --buildtype=debug

   # configure to build with OpenSSL support
   meson setup build -Dssl=openssl
   ```

   設定建置目錄是一次性的步驟。若要在下次建置前重新設定，你可以直接使用
   `meson configure` 指令

   ```

   meson configure -Dcassert=true
   ```

   `meson configure` 常用的命令列選項，請參見
   [第 17.4.3 節](install-meson.md#MESON-OPTIONS) 的說明。
<a id="MESON-BUILD"></a>2. **建置**

   Meson 預設使用 [Ninja](https://ninja-build.org/) 建置工具。若要用 Meson
   建置 PostgreSQL 原始碼，你只需要在建置目錄中使用
   `ninja` 指令即可。

   ```

   ninja
   ```

   Ninja 會自動偵測你電腦上的 CPU 數量，並據此自動平行化建置。你可以透過命令列參數
   `-j` 來覆寫要使用的平行程序數量。

   值得一提的是，在完成初次的設定步驟之後，編譯時你唯一需要輸入的指令就是
   `ninja`。無論你如何變動你的原始碼樹（只要不是把它整個搬到全新的位置），
   Meson 都會偵測到變動並自動重新產生建置內容。這在你有多個建置目錄時特別方便：
   通常其中一個用於開發（也就是「debug」建置），其他則偶爾才會用到（例如「靜態分析」建置）。
   只要切換到對應的目錄並執行 Ninja，就能建置任何一種設定。

   如果你想改用 ninja 以外的後端來建置，可以在 configure 時使用
   `--backend` 選項來選擇想用的後端，然後再用 `meson compile`
   來建置。想進一步了解這些後端以及可以提供給 ninja 的其他參數，
   可以參考 [Meson 文件](https://mesonbuild.com/Running-Meson.html#building-from-the-source)。
3. **迴歸測試**

   <a id="id-1.6.4.7.3.2.3.2"></a>

   如果你想在安裝新建置的伺服器之前先測試看看，可以在這個階段執行迴歸測試。
   迴歸測試是一套測試套件，用來驗證 PostgreSQL 在你的機器上執行的行為，
   符合開發者原先預期的樣子。輸入：

   ```

   meson test
   ```

   （這個指令不能以 root 身分執行；請以非特權使用者執行。）
   關於如何解讀測試結果的詳細資訊，請參見 [第 31 章](../regress/README.md)。
   你可以在之後任何時候，再次執行同一個指令來重複這項測試。

   若要針對正在執行中的 postgres 實例，執行 pg_regress 與 pg_isolation_regress
   測試，請在 **`meson test`** 的參數中加上
   **`--setup running`**。
<a id="MESON-INSTALL"></a>4. **安裝檔案**

   ### 注意

   如果你正在升級既有的系統，請務必先閱讀
   [第 18.6 節](../runtime/upgrading.md)，
   當中有關於升級叢集的說明。

   PostgreSQL 建置完成後，你只需要執行
   `ninja install` 指令即可安裝。

   ```

   ninja install
   ```

   這會把檔案安裝到你在 [步驟 1](install-meson.md#MESON-CONFIGURE) 中指定的目錄裡。
   請確認你對該區域擁有適當的寫入權限；這個步驟可能需要以 root 身分執行。
   你也可以改為預先建立好目標目錄，並安排好適當的權限。
   標準安裝會提供用戶端應用程式開發，以及伺服器端程式開發（例如用 C
   撰寫的自訂函式或資料型別）所需的所有標頭檔。

   多數情況下 `ninja install` 就已經足夠，但如果你想使用更多選項
   （例如以 `--quiet` 抑制多餘的輸出），也可以改用
   `meson install`。你可以在 Meson 文件中進一步了解
   [meson install](https://mesonbuild.com/Commands.html#install)
   及其選項。

**解除安裝：**
若要復原安裝，可以使用 `ninja
uninstall` 指令。

**清理：**
安裝完成後，你可以使用 `ninja clean`
指令，從原始碼樹中移除建置產出的檔案，藉此釋放磁碟空間。

<a id="MESON-OPTIONS"></a>

### 17.4.3. `meson setup` 選項 [#](#MESON-OPTIONS)

以下說明 `meson setup` 的命令列選項。這份清單並不完整
（可用 `meson configure --help` 取得完整清單）。此處未列出的選項是給進階使用情境用的，
記載於標準 [Meson
文件](https://mesonbuild.com/Commands.html#configure) 中。這些參數同樣可以在 `meson
setup` 時使用。

<a id="MESON-OPTIONS-LOCATIONS"></a>

#### 17.4.3.1. 安裝位置 [#](#MESON-OPTIONS-LOCATIONS)

這些選項用來控制 `ninja install`（或 `meson install`）要把檔案放到哪裡。
`--prefix` 選項（範例見
[第 17.4.1 節](install-meson.md#INSTALL-SHORT-MESON)）對多數情況來說已經足夠。
若你有特殊需求，可以用本節所述的其他選項來自訂安裝子目錄。
不過請留意，變更各子目錄的相對位置，可能會導致安裝結果無法「可搬遷（relocatable）」，
也就是安裝完成後將無法再搬動它。
（`man` 與 `doc` 的位置不受此限制影響。）
若要讓安裝結果可搬遷，你可能會想使用稍後提到的
`-Drpath=false` 選項。

<a id="CONFIGURE-PREFIX-MESON"></a>

`--prefix=PREFIX` [#](#CONFIGURE-PREFIX-MESON)
:   將所有檔案安裝到 *`PREFIX`* 目錄底下，
    而不是預設的 `/usr/local/pgsql`（Unix 系統上）或
    `current drive letter:/usr/local/pgsql`（Windows 上）。
    實際的檔案會被安裝到各個子目錄中；不會有任何檔案直接安裝在
    *`PREFIX`* 目錄本身。
<a id="CONFIGURE-BINDIR-MESON"></a>

`--bindir=DIRECTORY` [#](#CONFIGURE-BINDIR-MESON)
:   指定可執行程式所在的目錄。預設為
    `PREFIX/bin`。
<a id="CONFIGURE-SYSCONFDIR-MESON"></a>

`--sysconfdir=DIRECTORY` [#](#CONFIGURE-SYSCONFDIR-MESON)
:   設定各種設定檔所在的目錄，
    預設為 `PREFIX/etc`。
<a id="CONFIGURE-LIBDIR-MESON"></a>

`--libdir=DIRECTORY` [#](#CONFIGURE-LIBDIR-MESON)
:   設定要安裝函式庫與可動態載入模組的位置。預設為
    `PREFIX/lib`。
<a id="CONFIGURE-INCLUDEDIR-MESON"></a>

`--includedir=DIRECTORY` [#](#CONFIGURE-INCLUDEDIR-MESON)
:   設定安裝 C 與 C++ 標頭檔的目錄。
    預設為 `PREFIX/include`。
<a id="CONFIGURE-DATADIR-MESON"></a>

`--datadir=DIRECTORY` [#](#CONFIGURE-DATADIR-MESON)
:   設定已安裝程式所使用之唯讀資料檔的目錄。預設為
    `PREFIX/share`。請注意，這與你的資料庫檔案要放在哪裡
    完全無關。
<a id="CONFIGURE-LOCALEDIR-MESON"></a>

`--localedir=DIRECTORY` [#](#CONFIGURE-LOCALEDIR-MESON)
:   設定要安裝地區化（locale）資料的目錄，特別是訊息翻譯目錄檔案。預設為
    `DATADIR/locale`。
<a id="CONFIGURE-MANDIR-MESON"></a>

`--mandir=DIRECTORY` [#](#CONFIGURE-MANDIR-MESON)
:   PostgreSQL 附帶的 man page 會被安裝在
    這個目錄底下，依各自所屬的
    `manx` 子目錄分類。
    預設為 `DATADIR/man`。

### 注意

我們特別留意讓 PostgreSQL 可以安裝到共用的安裝位置中
（例如 `/usr/local/include`），而不會干擾到系統其餘部分的命名空間。
首先，字串「`/postgresql`」會自動附加到
`datadir`、`sysconfdir` 與 `docdir`
之後，除非展開後的完整目錄名稱本身已經包含
「`postgres`」或
「`pgsql`」字串。舉例來說，若你選擇
`/usr/local` 作為前綴，文件會被安裝到
`/usr/local/doc/postgresql`；
但如果前綴是 `/opt/postgres`，文件則會安裝在
`/opt/postgres/doc`。用戶端介面的公開 C
標頭檔會安裝到 `includedir` 底下，且維持命名空間乾淨。
內部標頭檔與伺服器端標頭檔則會安裝到
`includedir` 底下的私有目錄中。各介面各自的文件中
會說明如何存取其標頭檔。最後，若有需要，也會在
`libdir` 底下為可動態載入模組建立一個私有子目錄。

<a id="MESON-OPTIONS-FEATURES"></a>

#### 17.4.3.2. PostgreSQL 功能 [#](#MESON-OPTIONS-FEATURES)

本節所述的選項，可用來啟用建置各種 PostgreSQL 的選用功能。
其中多數功能需要額外的軟體支援，詳見
[第 17.1 節](install-requirements.md)；若偵測到所需軟體，會自動啟用這些功能。
你可以手動將這些功能設為 `enabled` 以強制啟用，或設為
`disabled` 以不將其建置進去，藉此改變這種行為。

要指定 PostgreSQL 專屬的選項，選項名稱前必須加上
`-D` 前綴。

<a id="CONFIGURE-WITH-NLS-MESON"></a>

`-Dnls={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-NLS-MESON)
:   啟用或停用原生語言支援（Native Language Support，NLS），
    也就是讓程式能以英文以外的語言顯示訊息的能力。預設為 auto，
    若偵測到 Gettext
    API 的實作，就會自動啟用。
<a id="CONFIGURE-WITH-PLPERL-MESON"></a>

`-Dplperl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLPERL-MESON)
:   建置 PL/Perl 伺服器端語言。
    預設為 auto。
<a id="CONFIGURE-WITH-PLPYTHON-MESON"></a>

`-Dplpython={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLPYTHON-MESON)
:   建置 PL/Python 伺服器端語言。
    預設為 auto。
<a id="CONFIGURE-WITH-PLTCL-MESON"></a>

`-Dpltcl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLTCL-MESON)
:   建置 PL/Tcl 伺服器端語言。
    預設為 auto。
<a id="CONFIGURE-WITH-TCL-VERSION-MESON"></a>

`-Dtcl_version=TCL_VERSION` [#](#CONFIGURE-WITH-TCL-VERSION-MESON)
:   指定建置 PL/Tcl 時要使用的 Tcl 版本。
<a id="CONFIGURE-WITH-ICU-MESON"></a>

`-Dicu={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-ICU-MESON)
:   建置時支援
    ICU<a id="id-1.6.4.7.4.4.4.6.2.1.2"></a>
    函式庫，以便使用 ICU 定序（collation）功能（參見 [第 23.2 節](../charset/collation.md)）。預設為 auto，且需要安裝
    ICU4C 套件。目前所需的 ICU4C
    最低版本為 4.2。
<a id="CONFIGURE-WITH-LLVM-MESON"></a>

`-Dllvm={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LLVM-MESON)
:   建置時支援以 LLVM 為基礎的
    JIT 編譯（參見 [第 30 章](../jit/README.md)）。
    這需要安裝 LLVM 函式庫。
    目前所需的 LLVM 最低版本為 14。預設為
    停用。

    系統會使用 `llvm-config`<a id="id-1.6.4.7.4.4.4.7.2.2.2"></a>
    來尋找所需的編譯選項。系統會在你的 `PATH` 中搜尋
    `llvm-config`，接著再搜尋各個受支援版本對應的
    `llvm-config-$version`。
    若這樣仍找不到你要的程式，可以用 `LLVM_CONFIG` 來指定
    正確 `llvm-config` 的路徑。
<a id="CONFIGURE-WITH-LZ4-MESON"></a>

`-Dlz4={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LZ4-MESON)
:   建置時支援 LZ4 壓縮。
    預設為 auto。
<a id="CONFIGURE-WITH-ZSTD-MESON"></a>

`-Dzstd={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-ZSTD-MESON)
:   建置時支援 Zstandard 壓縮。
    預設為 auto。
<a id="CONFIGURE-WITH-SSL-MESON"></a>

`-Dssl={ auto | LIBRARY }` <a id="id-1.6.4.7.4.4.4.10.1.2"></a> [#](#CONFIGURE-WITH-SSL-MESON)
:   建置時支援 SSL（加密）連線。
    目前唯一支援的 *`LIBRARY`* 是
    `openssl`。這需要安裝
    OpenSSL 套件。使用此選項建置時，
    會先檢查所需的標頭檔與函式庫，確認你的 OpenSSL
    安裝符合需求後才會繼續。此選項預設為 auto。
<a id="CONFIGURE-WITH-GSSAPI-MESON"></a>

`-Dgssapi={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-GSSAPI-MESON)
:   建置時支援 GSSAPI 認證。使用 GSSAPI 需要安裝 MIT Kerberos。
    在許多系統上，GSSAPI 系統（屬於 MIT Kerberos 安裝的一部分）
    並不會安裝在預設搜尋的位置（例如 `/usr/include`、
    `/usr/lib`）。
    在這些情況下，PostgreSQL 會查詢 `pkg-config` 來
    偵測所需的編譯器與連結器選項。預設為 auto。
    `meson configure` 會先檢查所需的
    標頭檔與函式庫，確認你的 GSSAPI 安裝符合需求後才會繼續。
<a id="CONFIGURE-WITH-LDAP-MESON"></a>

`-Dldap={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LDAP-MESON)
:   建置時支援
    LDAP<a id="id-1.6.4.7.4.4.4.12.2.1.2"></a>
    功能，用於認證及連線參數查詢（更多資訊請參見
    <a id="INSTALL-LDAP-LINKS-MESON"></a>[第 32.18 節](../../client-interfaces/libpq/libpq-ldap.md) 與
    [第 20.10 節](../client-authentication/auth-ldap.md)）。在 Unix 上，
    這需要安裝 OpenLDAP 套件。在 Windows 上，
    則會使用預設的 WinLDAP
    函式庫。預設為 auto。`meson
    configure` 會先檢查所需的標頭檔與
    函式庫，確認你的 OpenLDAP
    安裝符合需求後才會繼續。
<a id="CONFIGURE-WITH-PAM-MESON"></a>

`-Dpam={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PAM-MESON)
:   建置時支援
    PAM<a id="id-1.6.4.7.4.4.4.13.2.1.2"></a>
    （Pluggable Authentication Modules）。預設為 auto。
<a id="CONFIGURE-WITH-BSD-AUTH-MESON"></a>

`-Dbsd_auth={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-BSD-AUTH-MESON)
:   建置時支援 BSD Authentication。（BSD Authentication
    框架目前僅在 OpenBSD 上可用。）預設為 auto。
<a id="CONFIGURE-WITH-SYSTEMD-MESON"></a>

`-Dsystemd={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-SYSTEMD-MESON)
:   建置時支援
    systemd<a id="id-1.6.4.7.4.4.4.15.2.1.2"></a>
    服務通知。若伺服器是在 systemd 底下啟動，
    這能改善整合程度；若非如此則沒有影響；詳見 [第 18.3 節](../runtime/server-start.md)。預設為
    auto。使用此選項需要安裝 libsystemd 以及相關的
    標頭檔。
<a id="CONFIGURE-WITH-BONJOUR-MESON"></a>

`-Dbonjour={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-BONJOUR-MESON)
:   建置時支援 Bonjour 自動服務探索。預設
    為 auto，且需要你的作業系統支援 Bonjour。
    建議在 macOS 上使用。
<a id="CONFIGURE-WITH-UUID-MESON"></a>

`-Duuid=LIBRARY` [#](#CONFIGURE-WITH-UUID-MESON)
:   使用指定的 UUID 函式庫，建置 [uuid-ossp](../../appendixes/contrib/uuid-ossp.md) 模組
    （提供產生 UUID 的函式）。<a id="id-1.6.4.7.4.4.4.17.2.1.2"></a>
    *`LIBRARY`* 必須是下列其中之一：

    * `none`：不建置 uuid 模組。此為預設值。
    * `bsd`：使用 FreeBSD 及部分其他 BSD 衍生系統中內建的
      UUID 函式
    * `e2fs`：使用由
      `e2fsprogs` 專案所建立的 UUID 函式庫；此函式庫存在於多數
      Linux 系統與 macOS 中，其他平台上也可另行取得
    * `ossp`：使用 [OSSP UUID 函式庫](http://www.ossp.org/pkg/lib/uuid/)
<a id="CONFIGURE-WITH-LIBCURL-MESON"></a>

`-Dlibcurl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBCURL-MESON)
:   建置時支援 libcurl，以用於 OAuth 2.0 用戶端流程。
    此功能需要 libcurl 7.61.0 或更新版本。
    使用此選項建置時，會先檢查所需的標頭檔
    與函式庫，確認你的 Curl
    安裝符合需求後才會繼續。此選項預設為 auto。
<a id="CONFIGURE-WITH-LIBURING-MESON"></a>

`-Dliburing={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBURING-MESON)
:   建置時支援 liburing，以啟用非同步 I/O 所需的 io_uring 支援。
    預設為 auto。

    若要使用安裝在非常見位置的 liburing，你可以設定
    `pkg-config` 相關的環境
    變數（詳見其文件）。
<a id="CONFIGURE-WITH-LIBNUMA-MESON"></a>

`-Dlibnuma={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBNUMA-MESON)
:   建置時支援 libnuma，以提供基本的 NUMA 支援。
    僅在已實作 libnuma
    函式庫的平台上受支援。此選項預設為 auto。
<a id="CONFIGURE-WITH-LIBXML-MESON"></a>

`-Dlibxml={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBXML-MESON)
:   建置時支援 libxml2，以啟用 SQL/XML 支援。預設為
    auto。此功能需要 libxml2 2.6.23 或更新版本。

    若要使用安裝在非常見位置的 libxml2，你可以設定
    `pkg-config` 相關的環境
    變數（詳見其文件）。
<a id="CONFIGURE-WITH-LIBXSLT-MESON"></a>

`-Dlibxslt={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBXSLT-MESON)
:   建置時支援 libxslt，以啟用
    [xml2](../../appendixes/contrib/xml2.md)
    模組，用於執行 XML 的 XSL 轉換。
    必須同時指定 `-Dlibxml`。預設為
    auto。
<a id="CONFIGURE-WITH-SEPGSQL-MESON"></a>

`-Dselinux={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-SEPGSQL-MESON)
:   建置時支援 SElinux，以啟用 [sepgsql](../../appendixes/contrib/sepgsql.md)
    擴充功能。預設為 auto。

<a id="MESON-OPTIONS-ANTI-FEATURES"></a>

#### 17.4.3.3. 反功能 [#](#MESON-OPTIONS-ANTI-FEATURES)

<a id="CONFIGURE-READLINE-MESON"></a>

`-Dreadline={ auto | enabled | disabled }` [#](#CONFIGURE-READLINE-MESON)
:   允許使用 Readline 函式庫（也包括
    libedit）。此選項預設為
    auto，可為 psql 啟用命令列編輯與歷史紀錄功能，
    強烈建議啟用。
<a id="CONFIGURE-LIBEDIT-PREFERRED-MESON"></a>

`-Dlibedit_preferred={ true | false }` [#](#CONFIGURE-LIBEDIT-PREFERRED-MESON)
:   將此選項設為 true，會優先使用 BSD 授權的
    libedit 函式庫，而非 GPL 授權的
    Readline。此選項只有在你同時安裝了兩個
    函式庫時才有意義；預設為 false，也就是使用
    Readline。
<a id="CONFIGURE-ZLIB-MESON"></a>

`-Dzlib={ auto | enabled | disabled }` [#](#CONFIGURE-ZLIB-MESON)
:   <a id="id-1.6.4.7.4.5.2.3.2.1.1"></a>
    啟用 Zlib 函式庫的使用。
    預設為 auto，可為 pg_dump、
    pg_restore 與 pg_basebackup 啟用壓縮封存檔的支援，
    建議啟用。

<a id="MESON-OPTIONS-BUILD-PROCESS"></a>

#### 17.4.3.4. 建置程序詳情 [#](#MESON-OPTIONS-BUILD-PROCESS)

<a id="CONFIGURE-AUTO-FEATURES-MESON"></a>

`--auto-features={ auto | enabled | disabled }` [#](#CONFIGURE-AUTO-FEATURES-MESON)
:   設定此選項可以覆寫所有「auto」功能（也就是在偵測到所需軟體時
    會自動啟用的功能）的值。當你想一次停用或啟用所有「選用」功能，
    而不想逐一手動設定時，這會很有用。
    此參數的預設值為 auto。
<a id="CONFIGURE-BACKEND-MESON"></a>

`--backend=BACKEND` [#](#CONFIGURE-BACKEND-MESON)
:   Meson 預設使用的後端是 ninja，多數使用情境下都已足夠。
    但如果你想完整整合 Visual
    Studio，可以將 *`BACKEND`* 設為
    `vs`。
<a id="CONFIGURE-C-ARGS-MESON"></a>

`-Dc_args=OPTIONS` [#](#CONFIGURE-C-ARGS-MESON)
:   此選項可用來傳遞額外選項給 C 編譯器。
<a id="CONFIGURE-C-LINK-ARGS-MESON"></a>

`-Dc_link_args=OPTIONS` [#](#CONFIGURE-C-LINK-ARGS-MESON)
:   此選項可用來傳遞額外選項給 C 連結器。
<a id="CONFIGURE-EXTRA-INCLUDE-DIRS-MESON"></a>

`-Dextra_include_dirs=DIRECTORIES` [#](#CONFIGURE-EXTRA-INCLUDE-DIRS-MESON)
:   *`DIRECTORIES`* 是一份以逗號分隔的目錄清單，
    會被加入編譯器搜尋標頭檔的路徑清單中。若你有選用套件
    （例如 GNU
    Readline）安裝在非標準位置，就必須使用此選項，
    通常也需要一併使用對應的
    `-Dextra_lib_dirs` 選項。

    範例：`-Dextra_include_dirs=/opt/gnu/include,/usr/sup/include`。
<a id="CONFIGURE-EXTRA-LIB-DIRS-MESON"></a>

`-Dextra_lib_dirs=DIRECTORIES` [#](#CONFIGURE-EXTRA-LIB-DIRS-MESON)
:   *`DIRECTORIES`* 是一份以逗號分隔的目錄清單，
    用於搜尋函式庫。如果你有套件安裝在非標準位置，
    你很可能需要使用這個選項（以及對應的
    `-Dextra_include_dirs` 選項）。

    範例：`-Dextra_lib_dirs=/opt/gnu/lib,/usr/sup/lib`。
<a id="CONFIGURE-SYSTEM-TZDATA-MESON"></a>

`-Dsystem_tzdata=DIRECTORY` <a id="id-1.6.4.7.4.6.2.7.1.2"></a> [#](#CONFIGURE-SYSTEM-TZDATA-MESON)
:   PostgreSQL 內含自己的時區
    資料庫，這是日期與時間運算所需要的。這個時區資料庫實際上
    與許多作業系統（如 FreeBSD、Linux、
    Solaris）所提供的 IANA 時區資料庫相容，因此再安裝一份
    其實是多餘的。使用此選項時，系統中
    *`DIRECTORY`* 提供的時區資料庫，
    會取代 PostgreSQL 原始碼套件中內含的那一份。
    *`DIRECTORY`* 必須指定為絕對路徑。
    在某些作業系統上，`/usr/share/zoneinfo` 是可能適用的目錄。
    請注意，安裝程序不會偵測時區資料是否不符或有誤。若你使用此
    選項，建議執行迴歸測試，以驗證你所指向的時區資料
    能夠與 PostgreSQL 正確搭配運作。

    <a id="id-1.6.4.7.4.6.2.7.2.2"></a>

    此選項主要是設計給熟悉目標作業系統的二進位套件發行者使用。
    使用此選項的主要好處是，每當眾多本地日光節約時間規則變動時，
    PostgreSQL 套件都不需要跟著升級。另一項好處是，
    若安裝過程不需要建置時區資料庫檔案，PostgreSQL 的交叉編譯
    也能更加直接順利。
<a id="CONFIGURE-EXTRA-VERSION-MESON"></a>

`-Dextra_version=STRING` [#](#CONFIGURE-EXTRA-VERSION-MESON)
:   將 *`STRING`* 附加到 PostgreSQL 版本
    號碼後面。舉例來說，你可以用這個選項，為由未發行的 Git
    快照建置出來、或含有自訂修補程式的二進位檔標註額外的版本字串，
    例如 `git
    describe` 所產生的識別碼，或是發行套件的版本編號。
<a id="CONFIGURE-RPATH-MESON"></a>

`-Drpath={ true | false }` [#](#CONFIGURE-RPATH-MESON)
:   此選項預設為 true。若設為 false，
    則不會在 PostgreSQL 的執行檔中
    加上標記，指出應在安裝目錄下的函式庫目錄中搜尋共用函式庫
    （參見 `--libdir`）。
    在多數平台上，這種標記會使用函式庫目錄的絕對路徑，
    因此若你之後搬遷了整個安裝，這種標記就沒有幫助。
    在這種情況下，你就需要另外提供讓執行檔能找到共用函式庫
    的其他方式。通常這需要設定作業系統的
    動態連結器，讓它搜尋該函式庫目錄；詳情請見
    [第 17.5.1 節](install-post.md#INSTALL-POST-SHLIBS)。
<a id="CONFIGURE-BINARY-NAME-MESON"></a>

`-DBINARY_NAME=PATH` [#](#CONFIGURE-BINARY-NAME-MESON)
:   若建置 PostgreSQL（無論是否搭配選用旗標）所需的某個程式，
    是存放在非標準路徑下，你可以手動指定給
    `meson configure`。支援此做法的完整程式清單，
    可透過執行 `meson
    configure` 取得。範例：

    ```
    meson configure -DBISON=PATH_TO_BISON
    ```

<a id="MESON-OPTIONS-DOCS"></a>

#### 17.4.3.5. 文件 [#](#MESON-OPTIONS-DOCS)

建置文件所需的工具，請參見 [Section J.2](../../appendixes/docguide/docguide-toolsets.md)。

<a id="CONFIGURE-DOCS-MESON"></a>

`-Ddocs={ auto | enabled | disabled }` [#](#CONFIGURE-DOCS-MESON)
:   啟用以 HTML 與
    man 格式建置文件。預設為 auto。
<a id="CONFIGURE-DOCS-PDF-MESON"></a>

`-Ddocs_pdf={ auto | enabled | disabled }` [#](#CONFIGURE-DOCS-PDF-MESON)
:   啟用以 PDF
    格式建置文件。預設為 auto。
<a id="CONFIGURE-DOCS-HTML-STYLE"></a>

`-Ddocs_html_style={ simple | website }` [#](#CONFIGURE-DOCS-HTML-STYLE)
:   控制要使用哪一份 CSS 樣式表。預設值
    為 `simple`。若設為 `website`，
    HTML 文件會參照 [postgresql.org](https://www.postgresql.org/docs/current/) 所使用的樣式表。

<a id="MESON-OPTIONS-MISC"></a>

#### 17.4.3.6. 其他 [#](#MESON-OPTIONS-MISC)

<a id="CONFIGURE-PGPORT-MESON"></a>

`-Dpgport=NUMBER` [#](#CONFIGURE-PGPORT-MESON)
:   將 *`NUMBER`* 設為伺服器與用戶端的預設連接埠
    編號。預設值為 5432。連接埠之後任何時候
    都可以改變，但若你在此指定，伺服器與用戶端就會內建
    相同的預設值，這相當方便。通常唯一值得選用非預設值的理由，
    是你打算在同一台機器上執行多個
    PostgreSQL 伺服器。
<a id="CONFIGURE-KRB-SRVNAM-MESON"></a>

`-Dkrb_srvnam=NAME` [#](#CONFIGURE-KRB-SRVNAM-MESON)
:   GSSAPI 所使用的 Kerberos 服務主體（service principal）
    預設名稱。
    預設值為 `postgres`。除非你是要為 Windows
    環境建置，否則通常沒有理由需要更改；若是這種情況，
    則必須設為大寫的
    `POSTGRES`。
<a id="CONFIGURE-SEGSIZE-MESON"></a>

`-Dsegsize=SEGSIZE` [#](#CONFIGURE-SEGSIZE-MESON)
:   設定*區段大小（segment size）*，單位為 GB。大型資料表
    會被切分成多個作業系統檔案，每個檔案的大小
    等於區段大小。這樣可以避免許多平台上都存在的
    檔案大小限制問題。預設的區段大小為 1 GB，
    在所有受支援的平台上都是安全的。若你的作業系統支援
    「大型檔案（largefile）」（現今多數系統都支援），你可以使用
    更大的區段大小。這有助於在處理非常大的資料表時，
    減少所耗用的檔案描述符數量。
    但請小心，不要選擇超出你平台與所要使用之檔案系統
    支援範圍的值。你可能想使用的其他工具（例如 tar），
    也可能對可用的檔案大小設有限制。
    建議（雖非絕對必要）將此值設為 2 的次方。
<a id="CONFIGURE-BLOCKSIZE-MESON"></a>

`-Dblocksize=BLOCKSIZE` [#](#CONFIGURE-BLOCKSIZE-MESON)
:   設定*區塊大小（block size）*，單位為 KB。這是資料表內
    儲存與 I/O 的基本單位。預設值 8 KB
    適用於多數情況；但在特殊情況下，其他值也可能有用。
    此值必須是介於 1 到 32（KB）之間、且為 2 的次方的數字。
<a id="CONFIGURE-WAL-BLOCKSIZE-MESON"></a>

`-Dwal_blocksize=BLOCKSIZE` [#](#CONFIGURE-WAL-BLOCKSIZE-MESON)
:   設定 *WAL 區塊大小*，單位為 KB。這是 WAL
    日誌內儲存與 I/O 的基本單位。預設值 8 KB
    適用於多數情況；但在特殊情況下，其他值也可能有用。
    此值必須是介於 1 到 64（KB）之間、且為 2 的次方的數字。

<a id="MESON-OPTIONS-DEVEL"></a>

#### 17.4.3.7. 開發者選項 [#](#MESON-OPTIONS-DEVEL)

本節多數選項只在開發或除錯
PostgreSQL 時才有意義。這些選項並不建議用於正式環境的建置，
但 `--debug` 除外——它在你不幸遇到臭蟲、需要啟用詳細的臭蟲回報時會很有用。
在支援 DTrace 的平台上，`-Ddtrace`
在正式環境中使用也算合理。

若要建置一份用於在伺服器內部開發程式碼的安裝，建議至少加上
`--buildtype=debug`
與 `-Dcassert` 選項。

<a id="CONFIGURE-BUILDTYPE-MESON"></a>

`--buildtype=BUILDTYPE` [#](#CONFIGURE-BUILDTYPE-MESON)
:   此選項可用來指定要使用的 buildtype；預設為
    `debugoptimized`。若你想比此選項提供的更精細地
    控制除錯符號與最佳化等級，可以參考
    `--debug` 與
    `--optimization` 旗標。

    一般常用的建置類型有：`plain`、
    `debug`、`debugoptimized` 與
    `release`。關於這些類型的更多資訊，可參見
    [Meson
    文件](https://mesonbuild.com/Running-Meson.html#configuring-the-build-directory)。
<a id="CONFIGURE-DEBUG-MESON"></a>

`--debug` [#](#CONFIGURE-DEBUG-MESON)
:   以除錯符號編譯所有程式與函式庫。這表示
    你可以在除錯器中執行這些程式，以分析問題。
    這會大幅增加已安裝執行檔的大小，而在非 GCC 的編譯器上，
    通常也會停用編譯器最佳化，導致執行變慢。不過，
    擁有這些符號對於處理各種可能出現的問題非常有幫助。
    目前僅建議在使用 GCC 時，於正式環境安裝中啟用此選項。
    但若你在進行開發工作或執行 beta 版本，則應該一律開啟它。
<a id="CONFIGURE-OPTIMIZATION-MESON"></a>

`--optimization`=*`LEVEL`* [#](#CONFIGURE-OPTIMIZATION-MESON)
:   指定最佳化等級。`LEVEL` 可設為 {0,g,1,2,3,s} 其中之一。
<a id="CONFIGURE-WERROR-MESON"></a>

`--werror` [#](#CONFIGURE-WERROR-MESON)
:   設定此選項後，會要求編譯器將警告視為
    錯誤。這對程式碼開發很有幫助。
<a id="CONFIGURE-CASSERT-MESON"></a>

`-Dcassert={ true | false }` [#](#CONFIGURE-CASSERT-MESON)
:   在伺服器中啟用*斷言（assertion）*檢查，
    用來測試許多「不應該發生」的情況。這對程式碼開發
    來說非常寶貴，但這些測試會明顯拖慢伺服器的速度。
    此外，開啟這些測試也未必能提升伺服器的穩定性！
    這些斷言檢查並未依嚴重程度分類，因此原本可能只是
    相對無害的錯誤，一旦觸發斷言失敗，仍會導致伺服器重新啟動。
    並不建議在正式環境中使用此選項，但若你在進行開發工作
    或執行 beta 版本，則應該開啟它。
<a id="CONFIGURE-TAP-TESTS-MESON"></a>

`-Dtap_tests={ auto | enabled | disabled }` [#](#CONFIGURE-TAP-TESTS-MESON)
:   啟用使用 Perl TAP 工具的測試。預設為 auto，
    且需要安裝 Perl 以及 Perl 模組 `IPC::Run`。
    詳見 [第 31.4 節](../regress/regress-tap.md)。
<a id="CONFIGURE-PG-TEST-EXTRA-MESON"></a>

`-DPG_TEST_EXTRA=TEST_SUITES` [#](#CONFIGURE-PG-TEST-EXTRA-MESON)
:   啟用額外的測試套件；這些套件預設不會執行，
    因為它們在多使用者系統上執行並不安全、需要特殊軟體才能執行，
    或是相當耗費資源。參數是一份以空白分隔的清單，
    列出要啟用的測試。詳見
    [第 31.1.3 節](../regress/regress-run.md#REGRESS-ADDITIONAL)。若執行測試時已設定
    `PG_TEST_EXTRA` 環境變數，則會覆寫此設定時期的選項。
<a id="CONFIGURE-B-COVERAGE-MESON"></a>

`-Db_coverage={ true | false }` [#](#CONFIGURE-B-COVERAGE-MESON)
:   若使用 GCC，所有程式與函式庫都會加上
    程式碼涵蓋率測試的插樁（instrumentation）來編譯。執行時，
    它們會在建置目錄中產生含有程式碼涵蓋率
    指標的檔案。
    詳見 [第 31.5 節](../regress/regress-coverage.md)。此選項僅適用於 GCC，
    且僅在進行開發工作時使用。
<a id="CONFIGURE-DTRACE-MESON"></a>

`-Ddtrace={ auto | enabled | disabled }` [#](#CONFIGURE-DTRACE-MESON)
:   <a id="id-1.6.4.7.4.9.4.9.2.1.1"></a>
    啟用此選項會編譯出支援動態追蹤工具
    DTrace 的 PostgreSQL。
    詳見 [第 27.5 節](../monitoring/dynamic-trace.md)。

    你可以設定 `DTRACE` 選項，
    來指向 `dtrace` 程式。這通常是必要的，
    因為 `dtrace` 一般安裝在
    `/usr/sbin` 底下，而這個位置可能不在你的
    `PATH` 中。
<a id="CONFIGURE-INJECTION-POINTS-MESON"></a>

`-Dinjection_points={ true | false }` [#](#CONFIGURE-INJECTION-POINTS-MESON)
:   編譯出支援伺服器內插樁點（injection points）的
    PostgreSQL。插樁點可讓你在伺服器內部預先定義好的程式碼路徑中，
    執行使用者自訂的程式碼。
    這有助於以受控的方式進行測試，以及調查並行相關的情境。
    此選項預設為停用。更多細節請見
    [第 36.10.14 節](../../server-programming/extend/xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)。此
    選項僅供開發者用於測試。
<a id="CONFIGURE-SEGSIZE-BLOCKS-MESON"></a>

`-Dsegsize_blocks=SEGSIZE_BLOCKS` [#](#CONFIGURE-SEGSIZE-BLOCKS-MESON)
:   以區塊數指定關聯（relation）的區段大小。若同時指定了
    `-Dsegsize` 與此選項，則以此選項為準。
    此選項僅供開發者用於測試區段相關的程式碼。

<a id="TARGETS-MESON"></a>

### 17.4.4. `meson` 建置目標 [#](#TARGETS-MESON)

個別的建置目標可以用 `ninja` *`target`* 來建置。
若未指定目標，則會建置除文件以外的所有項目。個別的建置產物，
可以用其路徑／檔名作為 *`target`* 來建置。

<a id="TARGETS-MESON-CODE"></a>

#### 17.4.4.1. 程式碼目標 [#](#TARGETS-MESON-CODE)

<a id="MESON-TARGET-ALL"></a>

`all` [#](#MESON-TARGET-ALL)
:   建置除文件以外的所有內容
<a id="MESON-TARGET-BACKEND"></a>

`backend` [#](#MESON-TARGET-BACKEND)
:   建置後端及相關模組
<a id="MESON-TARGET-BIN"></a>

`bin` [#](#MESON-TARGET-BIN)
:   建置前端執行檔
<a id="MESON-TARGET-CONTRIB"></a>

`contrib` [#](#MESON-TARGET-CONTRIB)
:   建置 contrib 模組
<a id="MESON-TARGET-PL"></a>

`pl` [#](#MESON-TARGET-PL)
:   建置程序語言（procedural language）

<a id="TARGETS-MESON-DEVELOPER"></a>

#### 17.4.4.2. 開發者目標 [#](#TARGETS-MESON-DEVELOPER)

<a id="MESON-TARGET-REFORMAT-DAT-FILES"></a>

`reformat-dat-files` [#](#MESON-TARGET-REFORMAT-DAT-FILES)
:   將目錄資料檔重新改寫為標準格式
<a id="MESON-TARGET-EXPAND-DAT-FILES"></a>

`expand-dat-files` [#](#MESON-TARGET-EXPAND-DAT-FILES)
:   展開所有資料檔，使其包含預設值
<a id="MESON-TARGET-UPDATE-UNICODE"></a>

`update-unicode` [#](#MESON-TARGET-UPDATE-UNICODE)
:   將 unicode 資料更新為新版本

<a id="TARGETS-MESON-DOCUMENTATION"></a>

#### 17.4.4.3. 文件目標 [#](#TARGETS-MESON-DOCUMENTATION)

<a id="MESON-TARGET-HTML"></a>

`html` [#](#MESON-TARGET-HTML)
:   以多頁 HTML 格式建置文件
<a id="MESON-TARGET-MAN"></a>

`man` [#](#MESON-TARGET-MAN)
:   以 man page 格式建置文件
<a id="MESON-TARGET-DOCS"></a>

`docs` [#](#MESON-TARGET-DOCS)
:   以多頁 HTML 及 man page 格式建置文件
<a id="MESON-TARGET-DOC-SRC-SGML-POSTGRES-A4.PDF"></a>

`doc/src/sgml/postgres-A4.pdf` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES-A4.PDF)
:   以 PDF 格式建置文件，頁面尺寸為 A4
<a id="MESON-TARGET-DOC-SRC-SGML-POSTGRES-US.PDF"></a>

`doc/src/sgml/postgres-US.pdf` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES-US.PDF)
:   以 PDF 格式建置文件，頁面尺寸為美規信紙（US letter）
<a id="MESON-TARGET-DOC-SRC-SGML-POSTGRES.HTML"></a>

`doc/src/sgml/postgres.html` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES.HTML)
:   以單頁 HTML 格式建置文件
<a id="MESON-TARGET-ALLDOCS"></a>

`alldocs` [#](#MESON-TARGET-ALLDOCS)
:   以所有受支援的格式建置文件

<a id="TARGETS-MESON-INSTALLATION"></a>

#### 17.4.4.4. 安裝目標 [#](#TARGETS-MESON-INSTALLATION)

<a id="MESON-TARGET-INSTALL"></a>

`install` [#](#MESON-TARGET-INSTALL)
:   安裝 postgres，不含文件
<a id="MESON-TARGET-INSTALL-DOCS"></a>

`install-docs` [#](#MESON-TARGET-INSTALL-DOCS)
:   以多頁 HTML 及 man page 格式安裝文件
<a id="MESON-TARGET-INSTALL-HTML"></a>

`install-html` [#](#MESON-TARGET-INSTALL-HTML)
:   以多頁 HTML 格式安裝文件
<a id="MESON-TARGET-INSTALL-MAN"></a>

`install-man` [#](#MESON-TARGET-INSTALL-MAN)
:   以 man page 格式安裝文件
<a id="MESON-TARGET-INSTALL-QUIET"></a>

`install-quiet` [#](#MESON-TARGET-INSTALL-QUIET)
:   與「install」相同，但不會顯示已安裝的檔案
<a id="MESON-TARGET-INSTALL-WORLD"></a>

`install-world` [#](#MESON-TARGET-INSTALL-WORLD)
:   安裝 postgres，包含多頁 HTML 及 man page 格式的文件
<a id="MESON-TARGET-UNINSTALL"></a>

`uninstall` [#](#MESON-TARGET-UNINSTALL)
:   移除已安裝的檔案

<a id="TARGETS-MESON-OTHER"></a>

#### 17.4.4.5. 其他目標 [#](#TARGETS-MESON-OTHER)

<a id="MESON-TARGET-CLEAN"></a>

`clean` [#](#MESON-TARGET-CLEAN)
:   移除所有建置產物
<a id="MESON-TARGET-TEST"></a>

`test` [#](#MESON-TARGET-TEST)
:   執行所有已啟用的測試（包含 contrib）
<a id="MESON-TARGET-WORLD"></a>

`world` [#](#MESON-TARGET-WORLD)
:   建置所有內容，包含文件
<a id="MESON-TARGET-HELP"></a>

`help` [#](#MESON-TARGET-HELP)
:   列出重要的目標

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/install-meson.html)（原文版本：18.6；核對日期：2026-09-25）
