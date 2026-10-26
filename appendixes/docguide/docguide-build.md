<a id="DOCGUIDE-BUILD"></a>

## J.3. 使用 Make 建置文件 [#](#docguide-build) <a href="#docguide-build" id="docguide-build"></a>

[J.3.1. HTML](docguide-build.md#DOCGUIDE-BUILD-HTML)

[J.3.2. 線上手冊頁（Manpages）](docguide-build.md#DOCGUIDE-BUILD-MANPAGES)

[J.3.3. PDF](docguide-build.md#DOCGUIDE-BUILD-PDF)

[J.3.4. 語法檢查](docguide-build.md#DOCGUIDE-BUILD-SYNTAX-CHECK)

一切設定就緒後，切換到
`doc/src/sgml` 目錄，並執行
下列各小節所述的其中一個命令來建置
文件。（請記得使用 GNU make。）

<a id="DOCGUIDE-BUILD-HTML"></a>

### J.3.1. HTML [#](#DOCGUIDE-BUILD-HTML)

若要建置 HTML 版本的文件：

```

doc/src/sgml$ make html
```

這也是預設的建置目標。輸出會位於
`html` 子目錄。

若要產生使用 [postgresql.org](https://www.postgresql.org/docs/current/) 樣式表、而非
預設簡易樣式的 HTML 文件，請使用：

```

doc/src/sgml$ make STYLE=website html
```

若使用 `STYLE=website` 選項，產生的 HTML
檔案會參照託管在 [postgresql.org](https://www.postgresql.org/docs/current/) 上的樣式表，
因此檢視時需要網路連線。

<a id="DOCGUIDE-BUILD-MANPAGES"></a>

### J.3.2. 線上手冊頁（Manpages） [#](#DOCGUIDE-BUILD-MANPAGES)

我們使用 DocBook XSL 樣式表，將
DocBook
`refentry` 頁面轉換為適合 man
手冊頁的 \*roff 輸出。若要建立 man 手冊頁，請使用以下命令：

```

doc/src/sgml$ make man
```

<a id="DOCGUIDE-BUILD-PDF"></a>

### J.3.3. PDF [#](#DOCGUIDE-BUILD-PDF)

若要使用 FOP 產生 PDF 版本的文件，
可以依偏好的紙張格式，使用下列
其中一個命令：

* A4 格式：

  ```

  doc/src/sgml$ make postgres-A4.pdf
  ```
* 美國信紙（U.S. letter）格式：

  ```

  doc/src/sgml$ make postgres-US.pdf
  ```

由於 PostgreSQL 文件相當
龐大，FOP 會需要大量的
記憶體。因此，在某些系統上，建置會因
記憶體相關的錯誤訊息而失敗。這通常可以藉由在設定檔
`~/.foprc` 中設定 Java 堆積（heap）參數來修正，例如：

```

# FOP binary distribution
FOP_OPTS='-Xmx1500m'
# Debian
JAVA_ARGS='-Xmx1500m'
# Red Hat
ADDITIONAL_FLAGS='-Xmx1500m'
```

建置需要一定的最低記憶體量，而在某種程度上，
更多的記憶體似乎能讓建置稍微快一些。在記憶體
非常少（小於 1 GB）的系統上，建置可能會因
置換（swapping）而非常緩慢，或根本無法完成。

在預設設定下，FOP 會為每一頁發出一則
`INFO` 訊息。日誌等級可以
透過 `~/.foprc` 變更：

```

LOGCHOICE=-Dorg.apache.commons.logging.Log=​org.apache.commons.logging.impl.SimpleLog
LOGLEVEL=-Dorg.apache.commons.logging.simplelog.defaultlog=WARN
```

譯註：上方 LOGCHOICE 一行在「Log=」與「org.apache」之間，原文含有一個看不見的零寬空白字元（U+200B）。範例依原樣保留，但若直接複製使用，Java 會因類別名稱不正確而找不到日誌實作；實際設定時請刪除此字元，寫成 LOGCHOICE=-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.SimpleLog。

也可以手動使用其他 XSL-FO 處理器，但自動化建置
程序只支援 FOP。

<a id="DOCGUIDE-BUILD-SYNTAX-CHECK"></a>

### J.3.4. 語法檢查 [#](#DOCGUIDE-BUILD-SYNTAX-CHECK)

建置文件可能需要很長的時間。不過，有一種
方法可以只檢查文件檔案的語法是否正確，
只需要幾秒鐘：

```

doc/src/sgml$ make check
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/docguide-build.html)（原文版本：18.6；核對日期：2026-10-22）
