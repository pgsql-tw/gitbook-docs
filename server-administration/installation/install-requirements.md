<a id="INSTALL-REQUIREMENTS"></a>

## 17.1. 需求 [#](#INSTALL-REQUIREMENTS)

一般來說，現代的 Unix 相容平台應該都能執行
PostgreSQL。
在本版本發布時曾接受過特定測試的平台，
列於下方的[第 17.6 節](supported-platforms.md)中。

建置 PostgreSQL 需要以下軟體套件：

* <a id="id-1.6.4.4.3.2.1.1.1"></a>
  必須要有 GNU make 3.81（含）以上版本；其他的
  make 程式、或較舊版本的 GNU make，都*無法*運作。
  （GNU make 有時會以
  `gmake` 這個名稱安裝。）若要測試是否已安裝 GNU
  make，可輸入：

  ```

  make --version
  ```
* <a id="id-1.6.4.4.3.2.2.1.1"></a>
  另外，PostgreSQL 也可以使用
  [Meson](https://mesonbuild.com/) 來建置。若要在 Windows 上
  使用 Visual Studio 建置 PostgreSQL，
  這是唯一的選項。對其他平台而言，
  目前使用 Meson 仍屬實驗性質。如果
  你選擇使用 Meson，就不需要
  GNU make，但下方其他的需求仍然適用。

  Meson 所需的最低版本為 0.54。
* 你需要一套 ISO/ANSI C 編譯器（至少要
  相容 C99）。建議使用近期
  版本的 GCC，但已知
  PostgreSQL 也能以多家廠商提供的各種不同編譯器
  建置。
* 除了 gzip 或 bzip2 之外，還需要 tar 來
  解開原始碼發行套件。
* <a id="id-1.6.4.4.3.2.5.1.1"></a>
  <a id="id-1.6.4.4.3.2.5.1.2"></a>
  <a id="id-1.6.4.4.3.2.5.1.3"></a>
  <a id="id-1.6.4.4.3.2.5.1.4"></a>
  必須要有 Flex 及 Bison。無法使用其他的
  lex 及 yacc 程式。
  Bison 版本需至少為 2.3。
* <a id="id-1.6.4.4.3.2.6.1.1"></a>
  建置過程中，以及執行部分測試套件時，需要 Perl 5.14
  或更新版本。（此需求與建置 PL/Perl 的需求彼此獨立，
  詳見下方說明。）
* <a id="id-1.6.4.4.3.2.7.1.1"></a>
  <a id="id-1.6.4.4.3.2.7.1.2"></a>
  預設會使用 GNU Readline
  函式庫。它讓 psql（
  PostgreSQL 的命令列 SQL 直譯器）能夠記住你輸入過的每一個
  指令，並讓你可以用方向鍵回溯並
  編輯先前輸入過的指令。這非常有幫助，強烈
  建議使用。如果你不想使用它，就必須指定
  `--without-readline` 選項給
  `configure`。另外，你通常也可以改用
  BSD 授權的 `libedit` 函式庫，這套函式庫原本是在
  NetBSD 上開發的。
  `libedit` 函式庫與
  GNU Readline 相容，當找不到
  `libreadline`、或是在
  `configure` 中使用
  `--with-libedit-preferred` 選項時，就會改用它。如果你使用的是基於套件管理的
  Linux 發行版，請留意：如果該發行版將
  `readline` 與 `readline-devel` 拆成兩個套件，
  你需要兩者都安裝。
* <a id="id-1.6.4.4.3.2.8.1.1"></a>
  預設會使用 zlib 壓縮函式庫。如果你不想使用它，就必須
  指定 `--without-zlib` 選項給
  `configure`。使用此選項會
  停用 pg_dump 及
  pg_restore 中對壓縮封存檔的支援。
* 預設會使用 ICU 函式庫。如果你不想使用它，就必須指定 `--without-icu` 選項給 `configure`。使用此選項會停用 ICU 定序功能的支援（請參閱[第 23.2 節](../charset/collation.md)）。

  ICU 支援需要安裝 ICU4C
  套件。目前 ICU4C 所需的最低版本
  為 4.2。

  預設會使用
  pkg-config<a id="id-1.6.4.4.3.2.9.3.2"></a>
  來找出所需的編譯選項。此功能支援
  ICU4C 4.6 及以上版本。
  若為較舊版本、或系統上沒有 pkg-config，
  則可以在 `configure` 中指定
  `ICU_CFLAGS` 及
  `ICU_LIBS` 這兩個變數，如下例所示：

  ```

  ./configure ... ICU_CFLAGS='-I/some/where/include' ICU_LIBS='-L/some/where/lib -licui18n -licuuc -licudata'
  ```

  （如果編譯器的預設搜尋路徑中已包含
  ICU4C，你仍然需要指定非空字串，
  才能避免使用 pkg-config，例如
  `ICU_CFLAGS=' '`。）

以下這些套件屬於選用性質。在
預設組態設定中並不需要它們，但在啟用特定建置
選項時就會需要，詳如下述：

* 若要建置伺服器端程式語言
  PL/Perl，你需要一套完整的
  Perl 安裝，包含
  `libperl` 函式庫及標頭檔。
  所需的最低版本為 Perl 5.14。
  由於 PL/Perl 會是一個共享
  函式庫，因此在大多數平台上，<a id="id-1.6.4.4.4.1.1.1.6"></a>
  `libperl` 函式庫也必須是共享函式庫。這在近期版本的
  Perl 中似乎是預設狀態，但在較早的版本
  並非如此，而且無論如何，這都取決於在你所在
  站台安裝 Perl 的人所做的選擇。如果選擇建置
  PL/Perl，但卻找不到共享的
  `libperl`，`configure` 就會失敗。在這種情況下，你就必須
  手動重新建置並安裝 Perl，才能夠
  建置 PL/Perl。在為
  Perl 進行組態設定的過程中，請要求
  建置為共享函式庫。

  如果你打算相當頻繁地使用
  PL/Perl（而不只是偶爾用用），應該確保
  該 Perl 安裝是在啟用
  `usemultiplicity` 選項的情況下建置的（`perl -V`
  可以顯示是否屬於這種情況）。
* 若要建置 PL/Python 伺服器端程式
  語言，你需要一套 Python
  安裝，包含標頭檔以及
  sysconfig 模組。所支援的最低
  版本為 Python 3.6.8。

  由於 PL/Python 會是一個共享
  函式庫，因此在大多數平台上，<a id="id-1.6.4.4.4.1.2.2.2"></a>
  `libpython` 函式庫也必須是共享函式庫。從原始碼建置的
  預設 Python 安裝並非如此，但
  許多作業系統發行版都有提供共享
  函式庫版本。如果選擇建置
  PL/Python，但卻找不到共享的
  `libpython`，`configure` 就會失敗。這可能
  表示你必須安裝額外的套件，或是重新建置（部分）你的
  Python 安裝，以便提供這個共享
  函式庫。若從原始碼建置，請在執行 Python 的
  configure 時加上 `--enable-shared` 旗標。
* 若要建置 PL/Tcl
  程序語言，你當然需要一套 Tcl
  安裝。所需的最低版本為
  Tcl 8.4。
* 若要啟用原生語言支援（Native Language Support, NLS）——也
  就是讓程式訊息能以英文以外的語言顯示——你需要一套
  Gettext API 的實作。部分作業
  系統本身就內建此功能（例如 Linux、NetBSD、
  Solaris），至於其他系統，你
  可以從 <https://www.gnu.org/software/gettext/> 下載附加套件。
  如果你使用的是 GNU C 函式庫中內建的
  Gettext 實作，還需要額外
  安裝 GNU Gettext 套件，以取得部分
  工具程式；至於其他實作，則
  不需要另外安裝。
* 如果你想要支援加密的用戶端連線，就
  需要 OpenSSL。在沒有
  `/dev/urandom` 的平台上（Windows 除外），OpenSSL 也是
  產生亂數所必需的。所需的
  最低版本為 1.1.1。

  此外，透過 OpenSSL 相容層，也支援使用
  LibreSSL。所需的
  最低版本為 3.4（來自 OpenBSD
  7.0 版）。
* 如果你想要支援使用這些服務進行驗證，就需要 MIT Kerberos（用於 GSSAPI）、
  OpenLDAP，及／或 PAM。
* 你需要 Curl，才能建置一個選用模組，
  用來為用戶端應用程式實作 [OAuth 裝置
  授權流程](../../client-interfaces/libpq/libpq-oauth.md)。
* 如果你想要支援使用該方法進行資料
  壓縮，就需要 LZ4；請參閱
  [default_toast_compression](../runtime-config/runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION) 及
  [wal_compression](../runtime-config/runtime-config-wal.md#GUC-WAL-COMPRESSION)。
* 如果你想要支援使用該方法進行資料
  壓縮，就需要 Zstandard；請參閱
  [wal_compression](../runtime-config/runtime-config-wal.md#GUC-WAL-COMPRESSION)。
  所需的最低版本為 1.4.0。
* 若要建置 PostgreSQL 文件，
  另有一套獨立的需求；請參閱
  [第 J.2 節](../../appendixes/docguide/docguide-toolsets.md)。

如果你需要取得 GNU 套件，可以
在你當地的 GNU 鏡像站取得（參閱 <https://www.gnu.org/prep/ftp>
以取得站台清單），或是在 <ftp://ftp.gnu.org/gnu/> 取得。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/install-requirements.html)（原文版本：18.6；核對日期：2026-09-25）
