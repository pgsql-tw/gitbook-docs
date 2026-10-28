<a id="DOCGUIDE-TOOLSETS"></a>

## J.2. 工具組 [#](#docguide-toolsets) <a href="#docguide-toolsets" id="docguide-toolsets"></a>

[J.2.1. 在 Fedora、RHEL 及其衍生版本上安裝](docguide-toolsets.md#docguide-toolsets-inst-fedora-et-al)

[J.2.2. 在 FreeBSD 上安裝](docguide-toolsets.md#docguide-toolsets-inst-freebsd)

[J.2.3. Debian 套件](docguide-toolsets.md#docguide-toolsets-inst-debian)

[J.2.4. macOS](docguide-toolsets.md#docguide-toolsets-inst-macos)

[J.2.5. 由 `configure` 偵測](docguide-toolsets.md#docguide-toolsets-configure)

下列工具用於處理文件。其中有些
可能是選用的，如各項所註明。

<a id="DOCGUIDE-TOOLSETS-DOCBOOK-DTD"></a>

[DocBook DTD](https://www.oasis-open.org/docbook/) [#](#DOCGUIDE-TOOLSETS-DOCBOOK-DTD)
:   這是 DocBook 本身的定義。我們目前使用 4.5
    版；不能使用更新或更舊的版本。你需要的是
    DocBook DTD 的 XML 變體，而不是
    SGML 變體。
<a id="DOCGUIDE-TOOLSETS-DOCBOOK-XSL"></a>

[DocBook XSL 樣式表](https://github.com/docbook/wiki/wiki/DocBookXslStylesheets) [#](#DOCGUIDE-TOOLSETS-DOCBOOK-XSL)

其中包含將
DocBook 原始檔轉換為其他格式（例如
HTML）的處理指令。

目前要求的最低版本為 1.77.0，但建議
使用可取得的最新版本，以獲得最佳結果。
<a id="DOCGUIDE-TOOLSETS-LIBXML2"></a>

[Libxml2](http://xmlsoft.org/)（提供 `xmllint`） [#](#DOCGUIDE-TOOLSETS-LIBXML2)
:   此函式庫及其所含的 `xmllint` 工具
    用於處理 XML。許多開發者應該已經
    安裝了 Libxml2，因為建置 PostgreSQL 程式碼時
    也會用到它。不過請注意，
    `xmllint` 可能需要從
    另一個子套件安裝。
<a id="DOCGUIDE-TOOLSETS-LIBXSLT"></a>

[Libxslt](http://xmlsoft.org/XSLT/)（提供 `xsltproc`） [#](#DOCGUIDE-TOOLSETS-LIBXSLT)
:   `xsltproc` 是一個 XSLT 處理器，也就是一個
    使用 XSLT 樣式表將 XML 轉換為其他格式的程式。
<a id="DOCGUIDE-TOOLSETS-FOP"></a>

[FOP](https://xmlgraphics.apache.org/fop/) [#](#DOCGUIDE-TOOLSETS-FOP)
:   這是一個可以將 XML 轉換為 PDF 等格式的程式。
    只有在你想建置 PDF 格式的文件時才需要它。

對於處理文件所需的各種工具，我們已有
數種安裝方式的實際經驗，
將於下文說明。這些工具可能還有其他
打包好的發行版本。請將套件狀態回報至
文件郵件清單，我們會將該資訊納入
此處。

<a id="DOCGUIDE-TOOLSETS-INST-FEDORA-ET-AL"></a>

### J.2.1. 在 Fedora、RHEL 及其衍生版本上安裝 [#](#docguide-toolsets-inst-fedora-et-al) <a href="#docguide-toolsets-inst-fedora-et-al" id="docguide-toolsets-inst-fedora-et-al"></a>

若要安裝所需的套件，請使用：

```

yum install docbook-dtds docbook-style-xsl libxslt fop
```

<a id="DOCGUIDE-TOOLSETS-INST-FREEBSD"></a>

### J.2.2. 在 FreeBSD 上安裝 [#](#docguide-toolsets-inst-freebsd) <a href="#docguide-toolsets-inst-freebsd" id="docguide-toolsets-inst-freebsd"></a>

若要使用 `pkg` 安裝所需的套件，請使用：

```

pkg install docbook-xml docbook-xsl libxslt fop
```

從 `doc`
目錄建置文件時，你需要使用 `gmake`，因為
所提供的建置檔（makefile）不適用於 FreeBSD 的 `make`。

<a id="DOCGUIDE-TOOLSETS-INST-DEBIAN"></a>

### J.2.3. Debian 套件 [#](#docguide-toolsets-inst-debian) <a href="#docguide-toolsets-inst-debian" id="docguide-toolsets-inst-debian"></a>

Debian GNU/Linux 提供了一整套
文件工具的套件。
若要安裝，只需使用：

```

apt-get install docbook-xml docbook-xsl libxml2-utils xsltproc fop
```

<a id="DOCGUIDE-TOOLSETS-INST-MACOS"></a>

### J.2.4. macOS [#](#docguide-toolsets-inst-macos) <a href="#docguide-toolsets-inst-macos" id="docguide-toolsets-inst-macos"></a>

若你使用 MacPorts，以下命令即可完成設定：

```

sudo port install docbook-xml docbook-xsl-nons libxslt fop
```

若你使用 Homebrew，請使用：

```

brew install docbook docbook-xsl libxslt fop
```

Homebrew 提供的程式需要設定下列環境變數。
在 Intel 架構的機器上，請使用：

```

export XML_CATALOG_FILES=/usr/local/etc/xml/catalog
```

在 Apple Silicon 架構的機器上，請使用：

```

export XML_CATALOG_FILES=/opt/homebrew/etc/xml/catalog
```

若未設定，`xsltproc` 會擲出類似下列的錯誤：

```

I/O error : Attempt to load network entity http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd
postgres.sgml:21: warning: failed to load external entity "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd"
...
```

雖然可以使用 Apple 提供的
`xmllint` 與 `xsltproc` 版本，
而不使用 MacPorts 或 Homebrew 提供的版本，但你仍然需要
安裝 DocBook DTD 與樣式表，並設定指向它們的
目錄（catalog）檔案。

<a id="DOCGUIDE-TOOLSETS-CONFIGURE"></a>

### J.2.5. 由 `configure` 偵測 [#](#docguide-toolsets-configure) <a href="#docguide-toolsets-configure" id="docguide-toolsets-configure"></a>

在建置文件之前，你需要執行
`configure` 指令碼，就像建置
PostgreSQL 程式本身時一樣。
請檢查執行結束前的輸出，應該會類似
如下：

```

checking for xmllint... xmllint
checking for xsltproc... xsltproc
checking for fop... fop
checking for dbtoepub... dbtoepub
```

若找不到 `xmllint` 或 `xsltproc`，
就無法建置任何文件。
只有在建置 PDF 格式的文件時才需要 `fop`。
只有在建置 EPUB 格式的文件時才需要 `dbtoepub`。

必要時，你可以告訴 `configure` 到哪裡尋找
這些程式，例如

```

./configure ... XMLLINT=/opt/local/bin/xmllint ...
```

若你偏好使用 Meson 建置 PostgreSQL，
則改為依照
[第 17.4 節](../../server-administration/installation/install-meson.md)所述執行 `meson setup`，然後請參閱
[第 J.4 節](docguide-build-meson.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/docguide-toolsets.html)（原文版本：18.6；核對日期：2026-10-22）
