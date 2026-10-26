<a id="INSTALLATION-PLATFORM-NOTES"></a>

## 17.7. 特定平台注意事項 [#](#installation-platform-notes) <a href="#installation-platform-notes" id="installation-platform-notes"></a>

[17.7.1. Cygwin](installation-platform-notes.md#INSTALLATION-NOTES-CYGWIN)

[17.7.2. macOS](installation-platform-notes.md#INSTALLATION-NOTES-MACOS)

[17.7.3. MinGW](installation-platform-notes.md#INSTALLATION-NOTES-MINGW)

[17.7.4. Solaris](installation-platform-notes.md#INSTALLATION-NOTES-SOLARIS)

[17.7.5. Visual Studio](installation-platform-notes.md#INSTALLATION-NOTES-VISUAL-STUDIO)

本節記錄安裝與設定 PostgreSQL 時，其他與特定平台相關的問題。請務必
同時閱讀安裝說明，特別是[第 17.1 節](install-requirements.md)。此外，關於
迴歸測試結果的判讀，請查看[第 31 章](../regress/README.md)。

本節未涵蓋的平台，沒有已知的特定平台安裝問題。

<a id="INSTALLATION-NOTES-CYGWIN"></a>

### 17.7.1. Cygwin [#](#INSTALLATION-NOTES-CYGWIN)

<a id="id-1.6.4.10.4.2"></a>

PostgreSQL 可以使用 Cygwin（一個 Windows 上類似 Linux 的環境）建置，但這種
方式不如原生 Windows 建置，而且已不再建議在 Cygwin 底下執行伺服器。

從原始碼建置時，請依照 Unix 風格的安裝程序進行（也就是 `./configure;
make` 等等），並注意以下這些 Cygwin 特有的差異：

* 設定你的路徑（path），讓 Cygwin 的 bin 目錄排在 Windows 工具程式之前。
  這有助於避免編譯時發生問題。
* 不支援 `adduser` 命令；請改用 Windows 上合適的使用者管理
  應用程式。否則請略過這個步驟。
* 不支援 `su` 命令；請使用 ssh 在 Windows 上模擬 su。否則請
  略過這個步驟。
* 不支援 OpenSSL。
* 啟動 `cygserver` 以取得共享記憶體支援。方法是輸入命令
  `/usr/sbin/cygserver
  &`。每當你要啟動 PostgreSQL 伺服器，或初始化資料庫叢集
  （`initdb`）時，這個程式都必須正在執行。
  `cygserver` 的預設設定可能需要調整（例如增加
  `SEMMNS`），以避免 PostgreSQL 因為系統資源不足而失敗。
* 在使用非 C 語系的某些系統上，建置可能會失敗。要解決這個問題，可以在建置
  之前執行 `export LANG=C.utf8`，將語系設為 C，並在安裝完
  PostgreSQL 之後，再把它設回原本的設定。
* 平行迴歸測試（`make check`）可能會因為
  `listen()` 待處理佇列（backlog queue）溢位，造成連線被拒絕的錯誤或停止回應，進而產生虛假的
  迴歸測試失敗。你可以使用 make
  變數 `MAX_CONNECTIONS`，如下所示，限制連線數量：

  ```

  make MAX_CONNECTIONS=5 check
  ```

  （在某些系統上，最多可以同時有大約 10 個連線。）

可以將 `cygserver` 與 PostgreSQL 伺服器安裝為 Windows NT
服務。關於如何做到這一點的資訊，請參閱隨附於 Cygwin 上 PostgreSQL 二進位套件
中的 `README` 文件，該文件安裝於
`/usr/share/doc/Cygwin` 目錄中。

<a id="INSTALLATION-NOTES-MACOS"></a>

### 17.7.2. macOS [#](#INSTALLATION-NOTES-MACOS)

<a id="id-1.6.4.10.5.2"></a>

若要在 macOS 上從原始碼建置 PostgreSQL，你需要安裝 Apple 的命令列開發者工具，
方法是執行

```

xcode-select --install
```

（請注意，這會彈出一個 GUI 對話視窗要求確認）。你可以視需要決定是否也安裝 Xcode。

在較新版本的 macOS 上，必須將「sysroot」路徑嵌入到用來尋找部分系統標頭檔的
include 參數中。這會導致 configure 指令碼的輸出結果，隨著設定（configure）時
使用的 SDK 版本而有所不同。在簡單的情境中，這通常不會造成任何問題，但如果你
打算在與建置伺服器程式碼不同的機器上，做類似建置擴充功能的事情，可能就需要
強制使用不同的 sysroot 路徑。若要這麼做，請設定 `PG_SYSROOT`，
例如

```

make PG_SYSROOT=/desired/path all
```

若要找出你機器上合適的路徑，請執行

```

xcrun --show-sdk-path
```

請注意，並不太建議使用與建置核心伺服器時不同的 sysroot 版本來建置擴充功能；在
最糟的情況下，可能會導致難以除錯的 ABI 不一致問題。

在設定（configure）時，你也可以透過指定 `PG_SYSROOT` 給
configure，選擇一個非預設的 sysroot 路徑：

```

./configure ... PG_SYSROOT=/desired/path
```

這主要適用於交叉編譯給其他 macOS 版本使用的情況。並不保證產生出來的執行檔，
能在目前所在的主機上執行。

若要完全停用 `-isysroot` 選項，可以使用

```

./configure ... PG_SYSROOT=none
```

（任何不存在的路徑名稱都可以）。如果你想要使用非 Apple 的編譯器來建置，這
可能會有用，但請留意，PostgreSQL 開發者並未測試或支援這種情況。

macOS 的「系統完整性保護（System Integrity
Protection，SIP）」功能會破壞 `make check`，因為它會阻止將所需的
`DYLD_LIBRARY_PATH` 設定，傳遞給被測試的執行檔。你可以透過在
執行 `make check` 之前先執行 `make
install`，來繞過這個問題。不過，
大多數 PostgreSQL 開發者都是直接關閉 SIP。

<a id="INSTALLATION-NOTES-MINGW"></a>

### 17.7.3. MinGW [#](#INSTALLATION-NOTES-MINGW)

<a id="id-1.6.4.10.6.2"></a>

Windows 版的 PostgreSQL 可以使用 MinGW（一個 Windows 上類似 Unix 的建置環境）
建置。建議使用 [MSYS2](https://www.msys2.org/) 環境來建置，並同樣透過它安裝任何先決套件。

<a id="MINGW-CRASH-DUMPS"></a>

#### 17.7.3.1. 收集當機傾印 [#](#MINGW-CRASH-DUMPS)

如果 Windows 上的 PostgreSQL 發生當機，它具備產生迷你傾印（minidump）的能力，
可以用來追查當機原因，類似於 Unix 上的核心傾印（core dump）。這些傾印檔案
可以使用 Windows Debugger Tools 或 Visual Studio 來讀取。若要在 Windows 上
啟用傾印檔案的產生，請在叢集資料目錄中建立一個名為
`crashdumps` 的子目錄。傾印檔案接著會以根據發生當機之程序
識別碼與當機當下時間所產生的唯一名稱，寫入這個目錄中。

<a id="INSTALLATION-NOTES-SOLARIS"></a>

### 17.7.4. Solaris [#](#INSTALLATION-NOTES-SOLARIS)

<a id="id-1.6.4.10.7.2"></a>

PostgreSQL 在 Solaris 上獲得良好的支援。你的作業系統版本越新，遇到的問題就
會越少。

<a id="INSTALLATION-NOTES-SOLARIS-REQ-TOOLS"></a>

#### 17.7.4.1. 必要工具 [#](#INSTALLATION-NOTES-SOLARIS-REQ-TOOLS)

你可以使用 GCC 或 Sun 的編譯器套件來建置。為了取得更好的程式碼最佳化效果，
強烈建議在 SPARC 架構上使用 Sun 的編譯器。如果
你使用 Sun 的編譯器，請注意不要選到
`/usr/ucb/cc`；
請改用 `/opt/SUNWspro/bin/cc`。

你可以從 <https://www.oracle.com/technetwork/server-storage/solarisstudio/downloads/> 下載 Sun Studio。
許多 GNU 工具已經整合進 Solaris 10 中，或是可以在 Solaris companion CD 上
取得。如果你需要舊版 Solaris 適用的套件，可以在
<http://www.sunfreeware.com> 找到這些工具。
如果你偏好
原始碼，可以參閱 <https://www.gnu.org/prep/ftp>。

<a id="INSTALLATION-NOTES-SOLARIS-CONFIGURE-COMPLAINS"></a>

#### 17.7.4.2. configure 回報測試程式失敗 [#](#INSTALLATION-NOTES-SOLARIS-CONFIGURE-COMPLAINS)

如果 `configure` 回報某個測試程式失敗，這很可能是執行期
連結器（run-time linker）找不到某個函式庫的情況，可能是 libz、libreadline，或是
某個非標準函式庫，例如 libssl。若要指定正確的位置，請在
`configure` 命令列中設定 `LDFLAGS` 環境
變數，例如：

```

configure ... LDFLAGS="-R /usr/sfw/lib:/opt/sfw/lib:/usr/local/lib"
```

更多資訊請參閱
ld 的線上手冊（man page）。

<a id="INSTALLATION-NOTES-SOLARIS-COMP-OPT-PERF"></a>

#### 17.7.4.3. 為求最佳效能而編譯 [#](#INSTALLATION-NOTES-SOLARIS-COMP-OPT-PERF)

在 SPARC 架構上，強烈建議使用 Sun Studio 進行編譯。可以嘗試使用
`-xO5` 最佳化旗標，產生速度明顯較快的執行檔。請勿使用任何
會改變浮點運算行為
與 `errno` 處理方式的旗標（例如
`-fast`）。

如果你沒有理由必須在 SPARC 上使用 64 位元執行檔，建議優先選擇 32 位元版本。
64 位元運算速度較慢，且
64 位元執行檔的速度也比 32 位元版本慢。另一
方面，32 位元程式碼在 AMD64 CPU 系列上並非原生執行，
因此 32 位元程式碼在該 CPU 系列上的速度會明顯較慢。

<a id="INSTALLATION-NOTES-SOLARIS-USING-DTRACE"></a>

#### 17.7.4.4. 使用 DTrace 追蹤 PostgreSQL [#](#INSTALLATION-NOTES-SOLARIS-USING-DTRACE)

是的，可以使用 DTrace。詳情請參閱[第 27.5 節](../monitoring/dynamic-trace.md)。

如果你發現連結 `postgres` 執行檔時，因為以下這樣的錯誤訊息而
中止：

```

Undefined                       first referenced
 symbol                             in file
AbortTransaction                    utils/probes.o
CommitTransaction                   utils/probes.o
ld: fatal: Symbol referencing errors. No output written to postgres
collect2: ld returned 1 exit status
make: *** [postgres] Error 1
```

表示你的 DTrace 安裝版本太舊，無法處理靜態函式中的探針（probe）。你需要
Solaris 10u4 或更新版本，才能使用 DTrace。

<a id="INSTALLATION-NOTES-VISUAL-STUDIO"></a>

### 17.7.5. Visual Studio [#](#INSTALLATION-NOTES-VISUAL-STUDIO)

<a id="id-1.6.4.10.8.2"></a>

建議大多數使用者從 PostgreSQL 網站
<https://www.postgresql.org/download/> 下載 Windows 版的二進位發行版，這是
一個圖形化安裝程式套件。從原始碼建置，只適合正在開發
PostgreSQL 本身或其擴充功能的人。

搭配 Visual Studio 的 Windows 版 PostgreSQL，可以使用 Meson 建置，詳情請參閱
[第 17.4 節](install-meson.md)。
原生 Windows 移植版需要 32 或 64 位元版本的 Windows
10 或更新版本。

原生建置的 psql 不支援命令
列編輯功能。Cygwin 建置版本則支援
命令列編輯，因此如果需要在 Windows 上以互動方式使用 psql，應該使用該版本。

PostgreSQL 可以使用 Microsoft 的 Visual C++ 編譯器套件建置。
這些編譯器可以來自 Visual Studio、
Visual Studio Express，或是某些版本的
Microsoft Windows SDK。如果你尚未設定好
Visual Studio 環境，最簡單的方式是使用
Visual Studio 2022，或是
Windows SDK 10 中的編譯器，兩者都可以從
Microsoft 免費下載。

使用 Microsoft 編譯器套件，可以建置 32 位元與 64 位元版本。
32 位元的 PostgreSQL 建置可以使用
Visual Studio 2015 到
Visual Studio 2022，
以及 10 以上的獨立 Windows SDK 發行版。
64 位元的 PostgreSQL 建置則支援使用
Microsoft Windows SDK 10 以上版本，或
Visual Studio 2015 以上版本。

如果你的建置環境沒有內建受支援版本的
Microsoft Windows SDK，建議升級到最新版本
（目前是第 10 版），可以從 <https://www.microsoft.com/download> 下載。

你必須一律包含
SDK 中的 Windows Headers and Libraries 部分。
如果你安裝的 Windows SDK
包含 Visual C++ 編譯器，
就不需要 Visual Studio 也能建置。
請注意，自 8.0a 版起，Windows SDK 已不再隨附完整的命令列建置環境。

<a id="WINDOWS-REQUIREMENTS"></a>

#### 17.7.5.1. 需求 [#](#WINDOWS-REQUIREMENTS)

在 Windows 上建置
PostgreSQL，需要以下這些額外的產品。

Strawberry Perl
:   執行建置產生指令碼時需要 Strawberry Perl。MinGW
    或 Cygwin 版的 Perl 無法使用。它也必須存在於 PATH 中。
    可以從
    <https://strawberryperl.com> 下載二進位檔。

Bison 與 Flex
:   Bison 與
    Flex 的二進位檔，可以從 <https://github.com/lexxmark/winflexbison> 下載。

以下這些額外的產品並非開始建置時所必需，
但要建置完整套件時則需要。

Magicsplat Tcl
:   建置 PL/Tcl 時需要。
    可以從
    <https://www.magicsplat.com/tcl-installer/index.html> 下載二進位檔。

Diff
:   執行迴歸測試時需要 Diff，可以從
    <http://gnuwin32.sourceforge.net> 下載。

Gettext
:   建置具備 NLS 支援的版本時需要 Gettext，可以從
    <http://gnuwin32.sourceforge.net> 下載。請注意，二進位檔、
    相依套件與開發者檔案都是必要的。

MIT Kerberos
:   GSSAPI 驗證支援需要。MIT Kerberos 可以
    從
    <https://web.mit.edu/Kerberos/dist/index.html> 下載。

libxml2 與 libxslt
:   XML 支援需要。二進位檔可以從
    <https://zlatkovic.com/pub/libxml> 下載，原始碼可以從
    <http://xmlsoft.org> 取得。請注意，libxml2 需要 iconv，
    可以在相同的下載位置取得。

LZ4
:   支援 LZ4 壓縮時需要。
    二進位檔與原始碼可以從
    <https://github.com/lz4/lz4/releases> 下載。

Zstandard
:   支援 Zstandard 壓縮時需要。
    二進位檔與原始碼可以從
    <https://github.com/facebook/zstd/releases> 下載。

OpenSSL
:   SSL 支援需要。二進位檔可以從
    <https://slproweb.com/products/Win32OpenSSL.html>
    下載，原始碼可以從 <https://www.openssl.org> 取得。

ossp-uuid
:   UUID-OSSP 支援（僅限 contrib）需要。原始碼可以
    從
    <http://www.ossp.org/pkg/lib/uuid/> 下載。

Python
:   建置 PL/Python 時需要。可以
    從 <https://www.python.org> 下載二進位檔。

zlib
:   pg_dump 與 pg_restore 的壓縮支援需要。二進位檔可以下載
    自 <https://www.zlib.net>。

<a id="INSTALL-WINDOWS-FULL-64-BIT"></a>

#### 17.7.5.2. 64 位元 Windows 的特別考量 [#](#INSTALL-WINDOWS-FULL-64-BIT)

PostgreSQL 在 64 位元 Windows 上，只能建置給 x64 架構使用。

同一個建置樹中混用 32 位元與 64 位元版本，是不支援的。建置系統會自動偵測
目前是執行在 32 位元還是 64 位元環境，並據此建置 PostgreSQL。因此，在開始
建置之前，先啟動正確的命令提示字元，是很重要的一件事。

若要使用伺服器端的第三方函式庫，例如 Python 或
OpenSSL，這個函式庫也*必須*是
64 位元版本。並不支援在 64 位元
伺服器中載入 32 位元函式庫。PostgreSQL 所支援的部分第三方函式庫，可能只有
32 位元版本，在這種情況下，就無法搭配
64 位元的 PostgreSQL 使用。

<a id="WINDOWS-CRASH-DUMPS"></a>

#### 17.7.5.3. 收集當機傾印 [#](#WINDOWS-CRASH-DUMPS)

如果 Windows 上的 PostgreSQL 發生當機，它具備產生迷你傾印（minidump）的能力，
可以用來追查當機原因，類似於 Unix 上的核心傾印（core dump）。這些傾印檔案
可以使用 Windows Debugger Tools 或 Visual Studio 來讀取。若要在 Windows 上
啟用傾印檔案的產生，請在叢集資料目錄中建立一個名為
`crashdumps` 的子目錄。傾印檔案接著會以根據發生當機之程序
識別碼與當機當下時間所產生的唯一名稱，寫入這個目錄中。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/installation-platform-notes.html)（原文版本：18.6；核對日期：2026-10-10）
