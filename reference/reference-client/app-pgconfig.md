<a id="APP-PGCONFIG"></a><a id="id-1.9.4.13.1"></a>

## pg_config

pg_config — 取得已安裝之 PostgreSQL 版本的相關資訊

<a id="id-1.9.4.13.4"></a>

## 語法

<a id="id-1.9.4.13.4.1"></a>

`pg_config` [*`option`*...]

<a id="id-1.9.4.13.5"></a>

## 說明

pg_config 工具程式會印出目前已安裝之 PostgreSQL 版本的組態參數。例如，它的用途之一是讓想要與 PostgreSQL 介接的軟體套件，能夠更容易找到所需的標頭檔與函式庫。

<a id="id-1.9.4.13.6"></a>

## 選項

要使用 pg_config，請提供下列一個或多個選項：

`--bindir`
:   印出使用者可執行檔的位置。例如，可以用它來找出 `psql` 程式。這通常也是 `pg_config` 程式所在的位置。

`--docdir`
:   印出文件檔案的位置。

`--htmldir`
:   印出 HTML 文件檔案的位置。

`--includedir`
:   印出用戶端介面之 C 標頭檔的位置。

`--pkgincludedir`
:   印出其他 C 標頭檔的位置。

`--includedir-server`
:   印出伺服器端程式設計用之 C 標頭檔的位置。

`--libdir`
:   印出目的碼函式庫的位置。

`--pkglibdir`
:   印出可動態載入之模組的位置，或伺服器會在何處搜尋這些模組。（其他與架構相關的資料檔案也可能安裝在此目錄中。）

`--localedir`
:   印出區域設定（locale）支援檔案的位置。（若建置 PostgreSQL 時未設定區域設定支援，這會是空字串。）

`--mandir`
:   印出手冊頁（manual page）的位置。

`--sharedir`
:   印出與架構無關之支援檔案的位置。

`--sysconfdir`
:   印出全系統組態檔的位置。

`--pgxs`
:   印出擴充功能 makefile 的位置。

`--configure`
:   印出設定 PostgreSQL 以進行建置時，傳給 `configure` 腳本的選項。這可用來重現相同的組態，或查出某個二進位套件是以哪些選項建置的。（不過請注意，二進位套件通常包含廠商特有的自訂修補程式。）另請參閱下方的範例。

`--cc`
:   印出建置 PostgreSQL 時所用的 `CC` 變數的值。這會顯示所使用的 C 編譯器。

`--cppflags`
:   印出建置 PostgreSQL 時所用的 `CPPFLAGS` 變數的值。這會顯示前置處理階段所需的 C 編譯器參數（通常是 `-I` 參數）。

`--cflags`
:   印出建置 PostgreSQL 時所用的 `CFLAGS` 變數的值。這會顯示 C 編譯器參數。

`--cflags_sl`
:   印出建置 PostgreSQL 時所用的 `CFLAGS_SL` 變數的值。這會顯示建置共享函式庫時所用的額外 C 編譯器參數。

`--ldflags`
:   印出建置 PostgreSQL 時所用的 `LDFLAGS` 變數的值。這會顯示連結器參數。

`--ldflags_ex`
:   印出建置 PostgreSQL 時所用的 `LDFLAGS_EX` 變數的值。這會顯示僅在建置可執行檔時使用的連結器參數。

`--ldflags_sl`
:   印出建置 PostgreSQL 時所用的 `LDFLAGS_SL` 變數的值。這會顯示僅在建置共享函式庫時使用的連結器參數。

`--libs`
:   印出建置 PostgreSQL 時所用的 `LIBS` 變數的值。其內容通常是用於連結至 PostgreSQL 之外部函式庫的 `-l` 參數。

`--version`
:   印出 PostgreSQL 的版本。

`-?`<br>`--help`
:   顯示 pg_config 命令列引數的說明後結束。

若指定了超過一個選項，資訊會依該順序印出，每行一項。若未指定任何選項，則會印出所有可用的資訊，並附上標籤。

<a id="id-1.9.4.13.7"></a>

## 注意事項

選項 `--docdir`、`--pkgincludedir`、`--localedir`、`--mandir`、`--sharedir`、`--sysconfdir`、`--cc`、`--cppflags`、`--cflags`、`--cflags_sl`、`--ldflags`、`--ldflags_sl` 與 `--libs` 是在 PostgreSQL 8.1 中新增的。選項 `--htmldir` 是在 PostgreSQL 8.4 中新增的。選項 `--ldflags_ex` 是在 PostgreSQL 9.0 中新增的。

<a id="id-1.9.4.13.8"></a>

## 範例

要重現目前 PostgreSQL 安裝的建置組態，請執行下列命令：

```

eval ./configure `pg_config --configure`
```

`pg_config --configure` 的輸出包含 shell 引號，以便正確表示含有空格的引數。因此，必須使用 `eval` 才能得到正確的結果。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgconfig.html)（原文版本：18.6；核對日期：2026-10-09）
