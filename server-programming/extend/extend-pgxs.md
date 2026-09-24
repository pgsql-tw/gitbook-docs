<a id="EXTEND-PGXS"></a>
## 36.18. 擴充功能建置基礎架構 [#](#EXTEND-PGXS)

<a id="id-1.8.3.21.2"></a>

如果您正在考慮發布您的
PostgreSQL 擴充功能模組，為它們建立一套可移植的
建置系統可能相當困難。因此
PostgreSQL 安裝套件提供了一套用於擴充功能的
建置基礎架構，稱為 PGXS，讓
簡單的擴充功能模組可以直接針對已安裝的伺服器來建置。
PGXS 主要是設計給包含 C 程式碼的
擴充功能使用，不過純 SQL 的擴充功能也可以使用它。請注意
PGXS 並非設計成一套通用的建置系統框架，可用來
建置任何與 PostgreSQL 介接的軟體；
它只是將簡單伺服器擴充功能模組的常見建置規則自動化。對於
較複雜的套件，您可能需要撰寫自己的建置系統。

若要為您的擴充功能使用 PGXS 基礎架構，
您必須撰寫一個簡單的 makefile。
在該 makefile 中，您需要設定一些變數，
並引入全域的 PGXS makefile。
以下範例建置了一個名為
`isbn_issn` 的擴充功能模組，其中包含一個含有
一些 C 程式碼的共享程式庫、一個擴充功能控制檔、一個 SQL 指令碼、一個引入檔
（只有在其他模組需要不透過 SQL 存取擴充功能函式時才需要）
以及一份文件說明文字檔：

```

MODULES = isbn_issn
EXTENSION = isbn_issn
DATA = isbn_issn--1.0.sql
DOCS = README.isbn_issn
HEADERS_isbn_issn = isbn_issn.h

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
```

最後三行應該永遠保持不變。在檔案較前面的
部分，您可以指定變數或加入自訂的
make 規則。

請設定以下三個變數其中之一，以指定要建置的內容：

<a id="EXTEND-PGXS-MODULES"></a>

`MODULES` [#](#EXTEND-PGXS-MODULES)
:   要從具有相同字幹（stem）的來源檔建置的共享程式庫物件清單
    （此清單中不要包含程式庫後綴）
<a id="EXTEND-PGXS-MODULE-BIG"></a>

`MODULE_big` [#](#EXTEND-PGXS-MODULE-BIG)
:   要從多個來源檔建置的共享程式庫
    （物件檔清單請列在 `OBJS` 中）
<a id="EXTEND-PGXS-PROGRAM"></a>

`PROGRAM` [#](#EXTEND-PGXS-PROGRAM)
:   要建置的可執行程式
    （物件檔清單請列在 `OBJS` 中）

以下變數也可以設定：

<a id="EXTEND-PGXS-EXTENSION"></a>

`EXTENSION` [#](#EXTEND-PGXS-EXTENSION)
:   擴充功能名稱；每個名稱都必須提供一個
    `extension.control` 檔，
    此檔案將被安裝到
    `prefix/share/extension`
<a id="EXTEND-PGXS-MODULEDIR"></a>

`MODULEDIR` [#](#EXTEND-PGXS-MODULEDIR)
:   `prefix/share`
    下的子目錄，DATA 與 DOCS 檔案應安裝於此
    （若未設定，預設值在
    `EXTENSION` 有設定時為 `extension`，
    否則為 `contrib`）
<a id="EXTEND-PGXS-DATA"></a>

`DATA` [#](#EXTEND-PGXS-DATA)
:   要安裝到 `prefix/share/$MODULEDIR` 的任意檔案
<a id="EXTEND-PGXS-DATA-BUILT"></a>

`DATA_built` [#](#EXTEND-PGXS-DATA-BUILT)
:   要安裝到
    `prefix/share/$MODULEDIR` 的任意檔案，
    這些檔案需要先經過建置
<a id="EXTEND-PGXS-DATA-TSEARCH"></a>

`DATA_TSEARCH` [#](#EXTEND-PGXS-DATA-TSEARCH)
:   要安裝到
    `prefix/share/tsearch_data` 下的任意檔案
<a id="EXTEND-PGXS-DOCS"></a>

`DOCS` [#](#EXTEND-PGXS-DOCS)
:   要安裝到 `prefix/doc/$MODULEDIR` 下的任意檔案
<a id="EXTEND-PGXS-HEADERS"></a>

`HEADERS`<br>`HEADERS_built` [#](#EXTEND-PGXS-HEADERS)
:   要（視需要先建置後）安裝到 `prefix/include/server/$MODULEDIR/$MODULE_big` 下的檔案。

    與 `DATA_built` 不同，`HEADERS_built` 中的檔案
    不會被 `clean` 目標移除；若您希望它們被移除，
    請將它們另外加入 `EXTRA_CLEAN`，或自行加入規則來處理。
<a id="EXTEND-PGXS-HEADERS-MODULE"></a>

`HEADERS_$MODULE`<br>`HEADERS_built_$MODULE` [#](#EXTEND-PGXS-HEADERS-MODULE)
:   要（視需要先建置後）安裝到
    `prefix/include/server/$MODULEDIR/$MODULE` 下的檔案，
    其中 `$MODULE` 必須是
    `MODULES` 或 `MODULE_big` 中所使用的模組名稱。

    與 `DATA_built` 不同，`HEADERS_built_$MODULE` 中的檔案
    不會被 `clean` 目標移除；若您希望它們被移除，
    請將它們另外加入 `EXTRA_CLEAN`，或自行加入規則來處理。

    對同一個模組同時使用這兩個變數，或以任何方式組合使用都是合法的，
    除非您在
    `MODULES` 清單中有兩個模組名稱僅差在是否有
    `built_` 前綴，這會造成語意不明確。在
    那種（希望不太可能發生的）情況下，您應該只使用
    `HEADERS_built_$MODULE` 變數。
<a id="EXTEND-PGXS-SCRIPTS"></a>

`SCRIPTS` [#](#EXTEND-PGXS-SCRIPTS)
:   要安裝到 `prefix/bin` 的指令碼檔案
    （非二進位檔）
<a id="EXTEND-PGXS-SCRIPTS-BUILT"></a>

`SCRIPTS_built` [#](#EXTEND-PGXS-SCRIPTS-BUILT)
:   要安裝到
    `prefix/bin` 的指令碼檔案
    （非二進位檔），這些檔案需要先經過建置
<a id="EXTEND-PGXS-REGRESS"></a>

`REGRESS` [#](#EXTEND-PGXS-REGRESS)
:   迴歸測試案例清單（不含副檔名），詳情請見下文
<a id="EXTEND-PGXS-REGRESS-OPTS"></a>

`REGRESS_OPTS` [#](#EXTEND-PGXS-REGRESS-OPTS)
:   要傳遞給 pg_regress 的額外開關
<a id="EXTEND-PGXS-ISOLATION"></a>

`ISOLATION` [#](#EXTEND-PGXS-ISOLATION)
:   隔離性測試案例清單，詳情請見下文
<a id="EXTEND-PGXS-ISOLATION-OPTS"></a>

`ISOLATION_OPTS` [#](#EXTEND-PGXS-ISOLATION-OPTS)
:   要傳遞給
    pg_isolation_regress 的額外開關
<a id="EXTEND-PGXS-TAP-TESTS"></a>

`TAP_TESTS` [#](#EXTEND-PGXS-TAP-TESTS)
:   指定是否需要執行 TAP 測試的開關，詳情請見下文
<a id="EXTEND-PGXS-NO-INSTALL"></a>

`NO_INSTALL` [#](#EXTEND-PGXS-NO-INSTALL)
:   不定義 `install` 目標，適用於
    不需要安裝其建置產物的測試模組
<a id="EXTEND-PGXS-NO-INSTALLCHECK"></a>

`NO_INSTALLCHECK` [#](#EXTEND-PGXS-NO-INSTALLCHECK)
:   不定義 `installcheck` 目標，適用於例如測試需要特殊設定，或不使用 pg_regress 的情況
<a id="EXTEND-PGXS-EXTRA-CLEAN"></a>

`EXTRA_CLEAN` [#](#EXTEND-PGXS-EXTRA-CLEAN)
:   在 `make clean` 時要另外移除的檔案
<a id="EXTEND-PGXS-PG-CPPFLAGS"></a>

`PG_CPPFLAGS` [#](#EXTEND-PGXS-PG-CPPFLAGS)
:   將被加到 `CPPFLAGS` 之前
<a id="EXTEND-PGXS-PG-CFLAGS"></a>

`PG_CFLAGS` [#](#EXTEND-PGXS-PG-CFLAGS)
:   將被加到 `CFLAGS` 之後
<a id="EXTEND-PGXS-PG-CXXFLAGS"></a>

`PG_CXXFLAGS` [#](#EXTEND-PGXS-PG-CXXFLAGS)
:   將被加到 `CXXFLAGS` 之後
<a id="EXTEND-PGXS-PG-LDFLAGS"></a>

`PG_LDFLAGS` [#](#EXTEND-PGXS-PG-LDFLAGS)
:   將被加到 `LDFLAGS` 之前
<a id="EXTEND-PGXS-PG-LIBS"></a>

`PG_LIBS` [#](#EXTEND-PGXS-PG-LIBS)
:   將被加入 `PROGRAM` 的連結行
<a id="EXTEND-PGXS-SHLIB-LINK"></a>

`SHLIB_LINK` [#](#EXTEND-PGXS-SHLIB-LINK)
:   將被加入 `MODULE_big` 的連結行
<a id="EXTEND-PGXS-PG-CONFIG"></a>

`PG_CONFIG` [#](#EXTEND-PGXS-PG-CONFIG)
:   要建置的目標
    PostgreSQL 安裝所對應的 pg_config 程式路徑
    （通常只要用 `pg_config` 即可，
    使用您 `PATH` 中的第一個）

將這個 makefile 以 `Makefile` 的檔名放在
您擴充功能所在的目錄中。接著您就可以執行
`make` 來編譯，再執行 `make
install` 來安裝您的模組。預設情況下，擴充功能會針對
`PATH` 中第一個找到的 `pg_config`
程式所對應的
PostgreSQL 安裝來編譯並安裝。您可以透過
設定 `PG_CONFIG` 指向另一個
`pg_config` 程式（可以在 makefile 中設定，也可以在
`make` 命令列上設定）來使用不同的安裝。

您可以透過在執行 `make install` 時設定
`make` 變數 `prefix`，
來選擇一個獨立的目錄前綴，作為擴充功能檔案的安裝位置，
如下所示：

```

make install prefix=/usr/local/postgresql
```

這會將擴充功能的控制檔與 SQL 檔安裝到
`/usr/local/postgresql/share`，共享模組則安裝到
`/usr/local/postgresql/lib`。若此前綴不
包含字串 `postgres` 或
`pgsql`，例如

```

make install prefix=/usr/local/extras
```

則會在目錄名稱後面附加
`postgresql`，將控制檔與 SQL 檔安裝到
`/usr/local/extras/share/postgresql/extension`，
共享模組則安裝到 `/usr/local/extras/lib/postgresql`。
無論哪一種情況，您都需要設定 [extension_control_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH) 與 [dynamic_library_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH)，讓
PostgreSQL 伺服器能夠找到這些檔案：

```

extension_control_path = '/usr/local/extras/share/postgresql:$system'
dynamic_library_path = '/usr/local/extras/lib/postgresql:$libdir'
```

您也可以在擴充功能原始碼樹之外的目錄執行 `make`，
如果您想要讓建置目錄與原始碼樹分開的話。
這個做法也稱為
<a id="id-1.8.3.21.8.2"></a>*VPATH*
建置。作法如下：

```

mkdir build_dir
cd build_dir
make -f /path/to/extension/source/tree/Makefile
make -f /path/to/extension/source/tree/Makefile install
```

另一種方式是，您可以用類似核心程式碼所使用的方式，
為 VPATH 建置設定一個目錄。其中一種做法是使用
核心指令碼 `config/prep_buildtree`。完成此步驟後，
您就可以透過設定 `make` 變數
`VPATH` 來進行建置，如下所示：

```

make VPATH=/path/to/extension/source/tree
make VPATH=/path/to/extension/source/tree install
```

這個做法能夠適用於更多樣化的目錄配置。

`REGRESS` 變數所列出的指令碼，是用於
您模組的迴歸測試，可以在執行 `make install`
之後透過 `make installcheck` 來啟動。若要讓這個
機制運作，您必須有一個正在執行中的 PostgreSQL 伺服器。
`REGRESS` 中所列出的指令碼檔案，必須放在
擴充功能目錄下名為 `sql/` 的子目錄中。
這些檔案的副檔名必須是 `.sql`，而該副檔名
不得包含在 makefile 的 `REGRESS` 清單中。針對每個
測試，還應該有一個檔案，內含預期輸出，放在
名為 `expected/` 的子目錄中，字幹相同，
副檔名為 `.out`。`make installcheck`
會透過 psql 執行每個測試指令碼，並將
所得到的輸出與相符的預期檔案進行比對。任何差異都會
寫入檔案 `regression.diffs`，格式為 `diff
-c`。請注意，若嘗試執行缺少對應預期檔案的測試，將會被回報為「trouble」（表示發現問題），因此請確保
您擁有所有的預期檔案。

`ISOLATION` 變數所列出的指令碼，是用來
對您模組在並行工作階段下的行為進行壓力測試，可以在執行
`make install` 之後透過 `make installcheck`
來啟動。若要讓這個機制運作，您必須有一個
正在執行中的 PostgreSQL 伺服器。`ISOLATION`
中所列出的指令碼檔案，必須放在
擴充功能目錄下名為 `specs/` 的子目錄中。這些檔案的
副檔名必須是 `.spec`，而該副檔名不得包含
在 makefile 的 `ISOLATION` 清單中。針對每個
測試，還應該有一個檔案，內含預期輸出，放在
名為 `expected/` 的子目錄中，字幹相同，
副檔名為 `.out`。`make installcheck`
會執行每個測試指令碼，並將所得到的輸出與
相符的預期檔案進行比對。任何差異都會寫入檔案
`output_iso/regression.diffs`，格式為
`diff -c`。請注意，若嘗試執行缺少對應預期檔案的測試，將會被回報為「trouble」（表示發現問題），因此
請確保您擁有所有的預期檔案。

`TAP_TESTS` 用於啟用 TAP 測試。每次執行的
資料會存放在名為 `tmp_check/` 的子目錄中。
另請參閱 [31.4 節](../../server-administration/regress/regress-tap.md)以取得更多詳情。

<a id="EXTEND-PGXS-TAP-TESTS-TIP"></a>

### 提示

建立預期檔案最簡單的方法，是先建立空檔案，
然後執行一次測試（這樣當然會回報出差異）。檢查
`results/` 目錄中（針對 `REGRESS`
中的測試）或
`output_iso/results/` 目錄中（針對
`ISOLATION` 中的測試）實際產生的結果檔案，
如果符合您對該測試的預期，再將它們複製到
`expected/` 目錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/extend-pgxs.html)（原文版本：18.6；核對日期：2026-09-24）
