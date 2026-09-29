<a id="LOCALE"></a>

## 23.1. 區域設定支援 [#](#LOCALE)

[23.1.1. 概觀](locale.md#LOCALE-OVERVIEW)

[23.1.2. 行為](locale.md#LOCALE-BEHAVIOR)

[23.1.3. 選擇區域設定](locale.md#LOCALE-SELECTING-LOCALES)

[23.1.4. 區域設定提供者](locale.md#LOCALE-PROVIDERS)

[23.1.5. ICU 區域設定](locale.md#ICU-LOCALES)

[23.1.6. 問題](locale.md#LOCALE-PROBLEMS)

<a id="id-1.6.10.3.2"></a>

*區域設定*（Locale）支援是指應用程式遵循文化上對字母、排序、
數字格式等方面的偏好。PostgreSQL 使用伺服器作業系統提供的標準 ISO
C 與 POSIX 區域設定機制。如需更多資訊，請參閱你所使用
系統的文件。

<a id="LOCALE-OVERVIEW"></a>

### 23.1.1. 概觀 [#](#LOCALE-OVERVIEW)

當使用 `initdb` 建立資料庫叢集時，區域設定支援
會自動初始化。
`initdb` 預設會以其執行環境的區域設定
初始化資料庫叢集，因此如果你的系統已經設定為使用你想要在資料庫叢集中使用的區域設定，
就不需要做其他任何事。如果你想使用其他區域設定（或你不確定
系統目前設定為哪一種區域設定），你可以透過指定
`--locale` 選項，明確指示
`initdb` 要使用哪個區域設定。例如：

```

initdb --locale=sv_SE
```

這個 Unix 系統的範例會將區域設定設為瑞典（`SE`）所使用的瑞典語
（`sv`）。其他可能的選項還包括
`en_US`（美式英文）與 `fr_CA`（加拿大法語）。若某個
區域設定可以使用一種以上的字元集，其規格可以採用
*`language_territory.codeset`* 的形式。舉例來說，
`fr_BE.UTF-8` 代表比利時（BE）所使用的
法語（fr），並採用 UTF-8 字元集
編碼。

在你的系統上，有哪些區域設定可用、以何種名稱表示，取決於
作業系統供應商所提供的內容以及所安裝的項目。在大多數 Unix 系統上，
`locale -a` 指令會列出可用的區域設定清單。
Windows 使用較為冗長的區域設定名稱，例如 `German_Germany`
或 `Swedish_Sweden.1252`，但原理是相同的。

有時候混用來自不同區域設定的規則會很有用，例如使用英文的定序規則，但搭配西班牙文的訊息。為了支援這種做法，
系統提供了一組區域設定子分類，各自只控制在地化規則的
某些特定面向：

<table border="1" class="informaltable"><colgroup><col class="col1"/><col class="col2"/></colgroup><tbody><tr><td><code class="envar">LC_COLLATE</code></td><td>字串排序順序</td></tr><tr><td><code class="envar">LC_CTYPE</code></td><td>字元分類（什麼是字母？其對應的大寫字母為何？）</td></tr><tr><td><code class="envar">LC_MESSAGES</code></td><td>訊息所使用的語言</td></tr><tr><td><code class="envar">LC_MONETARY</code></td><td>貨幣金額的格式</td></tr><tr><td><code class="envar">LC_NUMERIC</code></td><td>數字的格式</td></tr><tr><td><code class="envar">LC_TIME</code></td><td>日期與時間的格式</td></tr></tbody></table>

這些分類名稱會轉換為
`initdb` 選項的名稱，用來覆寫特定分類的區域設定
選擇。舉例來說，若要將區域設定設為
加拿大法語，但貨幣格式採用美式規則，可使用
`initdb --locale=fr_CA --lc-monetary=en_US`。

如果你希望系統的行為就像完全沒有區域設定支援一樣，
請使用特殊的區域設定名稱 `C`，或等效的
`POSIX`。

部分區域設定分類的值必須在建立
資料庫時就固定下來。你可以為不同的資料庫使用不同的設定，但一旦某個資料庫建立完成，
就無法再變更該資料庫的這些設定。`LC_COLLATE`
與 `LC_CTYPE` 便屬於這類分類。它們會影響
索引的排序順序，因此必須維持固定，否則文字欄位上的
索引可能會損毀。
（不過你可以透過定序來緩解這項限制，詳見
[第 23.2 節](collation.md)討論。）
這些分類的預設值
是在執行 `initdb` 時決定的，
除非在 `CREATE DATABASE` 指令中另行指定，否則建立新資料庫時都會沿用這些值。

其他區域設定分類可以隨時透過
設定與這些區域設定分類同名的伺服器組態參數來變更（詳情見[第 19.11.2 節](../runtime-config/runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT)）。
`initdb` 所選擇的值實際上只會被寫入
組態檔 `postgresql.conf`，用於在伺服器
啟動時做為預設值。如果你從 `postgresql.conf` 中
移除這些設定，伺服器就會繼承其執行環境的
設定值。

請注意，伺服器的區域設定行為是由伺服器所看到的
環境變數決定，而非由任何用戶端的環境決定。因此，請務必
在啟動伺服器之前正確設定區域設定。這也表示，如果
用戶端與伺服器使用不同的區域設定，訊息可能會依據其來源
以不同語言呈現。

### 注意

當我們談到從執行
環境繼承區域設定時，在大多數作業系統上，這表示如下：
對於某個特定的區域設定分類，比方說定序，系統會依序
查詢以下環境變數，直到找到某個已設定的變數為止：`LC_ALL`、`LC_COLLATE`
（或對應該分類的變數）、
`LANG`。如果這些環境變數都未
設定，則區域設定會預設為 `C`。

某些訊息在地化函式庫也會參考環境
變數 `LANGUAGE`，該變數會覆寫所有其他區域設定，
以決定訊息所使用的語言。如果
有疑問，請參閱你作業系統的文件，
特別是關於
gettext 的文件。

若要啟用訊息翻譯成使用者偏好語言的功能，
必須在建置時選用 NLS
（`configure --enable-nls`）。其他所有區域設定支援
都是自動內建的。

<a id="LOCALE-BEHAVIOR"></a>

### 23.1.2. 行為 [#](#LOCALE-BEHAVIOR)

區域設定會影響下列 SQL 功能：

* 在使用 `ORDER BY` 或標準比較運算子對文字資料進行查詢時的排序順序
  <a id="id-1.6.10.3.5.2.1.1.1.2"></a>
* `upper`、`lower` 與 `initcap`
  函式
  <a id="id-1.6.10.3.5.2.1.2.1.4"></a>
  <a id="id-1.6.10.3.5.2.1.2.1.5"></a>
* 模式比對運算子（`LIKE`、`SIMILAR TO`，
  以及 POSIX 風格的正規表示式）；區域設定會同時影響
  不區分大小寫的比對，以及以字元類別為基礎之正規表示式的字元
  分類方式
  <a id="id-1.6.10.3.5.2.1.3.1.3"></a>
  <a id="id-1.6.10.3.5.2.1.3.1.4"></a>
* `to_char` 系列函式
  <a id="id-1.6.10.3.5.2.1.4.1.2"></a>
* 在 `LIKE` 子句中使用索引的能力

在 PostgreSQL 中使用 `C` 或
`POSIX` 以外的區域設定，其缺點在於效能
影響。它會拖慢字元處理速度，並且使一般索引無法被
`LIKE` 使用。因此，只有在你確實需要區域設定時才應該使用它們。

作為一種讓 PostgreSQL 在非 C 區域設定下也能搭配
`LIKE` 使用索引的替代方案，系統提供了幾種自訂
運算子類別。這些運算子類別可以建立一種索引，用來執行嚴格的逐字元
比較，而忽略區域設定的比較規則。詳情請參閱[第 11.10 節](../../the-sql-language/indexes/indexes-opclass.md)。
另一種做法是使用
`C` 定序建立索引，詳見
[第 23.2 節](collation.md)討論。

<a id="LOCALE-SELECTING-LOCALES"></a>

### 23.1.3. 選擇區域設定 [#](#LOCALE-SELECTING-LOCALES)

可以依需求在不同的範疇選擇區域設定。
上面的概觀說明了如何使用
`initdb` 為整個叢集指定區域設定，作為預設值。以下
清單顯示可以在何處選擇區域設定。清單中每一項都會為後續項目提供
預設值，而較後面的每一項都允許以更細的粒度覆寫預設值。

1. 如上所述，作業系統的環境會為新初始化的資料庫叢集提供
   預設的區域設定。在
   許多情況下，這樣就已經足夠：如果作業系統已針對
   所需的語言／地區進行設定，PostgreSQL 預設
   也會依循該區域設定運作。
2. 如上所示，`initdb` 的命令列選項
   可以為新初始化的資料庫叢集指定區域設定。如果作業系統沒有你想要在資料庫系統中使用的
   區域設定組態，就可以使用此方式。
3. 可以為每個資料庫分別選擇區域設定。SQL 指令
   `CREATE DATABASE` 及其對應的命令列工具
   `createdb` 都提供了相關選項。舉例來說，
   若某個資料庫叢集內含多個租戶各自需求不同的資料庫，就可以使用此方式。
4. 可以針對個別資料表欄位設定區域設定。這需要使用一種稱為
   *定序（collation）* 的 SQL 物件，說明於
   [第 23.2 節](collation.md)。舉例來說，若要以不同語言排序資料，或自訂某張資料表的排序順序，就可以使用此方式。
5. 最後，也可以針對個別查詢選擇區域設定。同樣地，這也是
   使用 SQL 定序物件。這可以用來根據執行階段的選擇來改變排序順序，或用於臨時性的實驗。

<a id="LOCALE-PROVIDERS"></a>

### 23.1.4. 區域設定提供者 [#](#LOCALE-PROVIDERS)

區域設定提供者指定了哪一個函式庫定義了
定序與字元分類的區域設定行為。

如上所述，用來選擇區域設定的各項指令與工具，
都各自提供了一個選項來選擇區域設定提供者。以下是使用
ICU 提供者初始化資料庫叢集的範例：

```

initdb --locale-provider=icu --icu-locale=en
```

詳情請參閱各相關指令與程式的說明。請注意，你可以
在不同的粒度上混用區域設定提供者，
例如在叢集層級預設使用 `libc`，
但讓其中一個資料庫使用 `icu`
提供者，然後在這些資料庫中同時使用任一提供者的定序物件。

無論使用哪一種區域設定提供者，作業系統仍然會被用來
提供某些區域設定相關的行為，例如訊息（見 [lc_messages](../runtime-config/runtime-config-client.md#GUC-LC-MESSAGES)）。

以下列出可用的區域設定提供者：

`builtin`
:   `builtin` 提供者使用內建的運算。此提供者僅支援
    `C`、`C.UTF-8` 與
    `PG_UNICODE_FAST` 這幾種區域設定。

    `C` 區域設定的行為與 libc 提供者中的
    `C` 區域設定相同。使用此區域設定時，
    行為可能取決於資料庫編碼。

    `C.UTF-8` 區域設定僅在資料庫編碼為
    `UTF-8` 時可用，其行為
    以 Unicode 為基礎。定序僅使用碼點（code point）值。
    正規表示式字元類別以「POSIX
    相容」語意為基礎，大小寫對應則採用「簡易（simple）」變體。

    `PG_UNICODE_FAST` 區域設定僅在
    資料庫編碼為 `UTF-8` 時可用，其行為
    以 Unicode 為基礎。定序僅使用碼點值。
    正規表示式字元類別以「標準（Standard）」
    語意為基礎，大小寫對應則採用「完整（full）」變體。

`icu`
:   `icu` 提供者使用外部的
    ICU<a id="id-1.6.10.3.7.6.2.2.1.2"></a>
    函式庫。建置 PostgreSQL 時
    必須已設定支援。

    ICU 提供的定序與字元分類行為與作業系統及資料庫編碼
    無關，若你預期未來會轉換到其他平台且不想改變結果，這會是較理想的選擇。
    `LC_COLLATE` 與
    `LC_CTYPE` 可以獨立於 ICU
    區域設定進行設定。

    ### 注意

    對於 ICU 提供者而言，結果可能取決於所使用的 ICU
    函式庫版本，因為該函式庫會隨時間更新以反映自然語言的變化。

`libc`
:   `libc` 提供者使用作業系統的 C
    函式庫。定序與字元分類行為
    由 `LC_COLLATE` 與 `LC_CTYPE`
    設定所控制，因此兩者無法獨立設定。

    ### 注意

    在使用 libc 提供者時，同一個區域設定名稱在不同平台上
    可能會有不同的行為。

<a id="ICU-LOCALES"></a>

### 23.1.5. ICU 區域設定 [#](#ICU-LOCALES)

<a id="ICU-LOCALE-NAMES"></a>

#### 23.1.5.1. ICU 區域設定名稱 [#](#ICU-LOCALE-NAMES)

ICU 的區域設定名稱格式是一個[語言標籤（Language Tag）](locale.md#ICU-LANGUAGE-TAG)。

```

CREATE COLLATION mycollation1 (provider = icu, locale = 'ja-JP');
CREATE COLLATION mycollation2 (provider = icu, locale = 'fr');
```

<a id="ICU-CANONICALIZATION"></a>

#### 23.1.5.2. 區域設定的正規化與驗證 [#](#ICU-CANONICALIZATION)

在定義新的 ICU 定序物件，或以 ICU 作為
提供者的資料庫時，若所給定的區域設定名稱尚未採用語言標籤的形式，就會被轉換（「正規化」）為該形式。舉例來說，

```

CREATE COLLATION mycollation3 (provider = icu, locale = 'en-US-u-kn-true');
NOTICE:  using standard form "en-US-u-kn" for locale "en-US-u-kn-true"
CREATE COLLATION mycollation4 (provider = icu, locale = 'de_DE.utf8');
NOTICE:  using standard form "de-DE" for locale "de_DE.utf8"
```

若你看到這則通知訊息，請確認 `provider` 與
`locale` 是你所預期的結果。若要在使用 ICU 提供者時得到一致的結果，
請直接指定正規的[語言標籤](locale.md#ICU-LANGUAGE-TAG)，
而不要依賴這種轉換機制。

沒有語言名稱，或使用特殊語言名稱
`root` 的區域設定，會被轉換為使用語言
`und`（「undefined，未定義」）。

ICU 可以將大多數 libc 的區域設定名稱，以及其他一些格式，
轉換為語言標籤，以便更容易轉換到 ICU。若在
ICU 中使用 libc 風格的區域設定名稱，其行為可能與在 libc 中不完全相同。

如果在解讀區域設定名稱時發生問題，或該區域設定名稱所代表的
語言或地區是 ICU 無法辨識的，你將會看到
以下警告：

```

CREATE COLLATION nonsense (provider = icu, locale = 'nonsense');
WARNING:  ICU locale "nonsense" has unknown language "nonsense"
HINT:  To disable ICU locale validation, set parameter icu_validation_level to DISABLED.
CREATE COLLATION
```

[icu_validation_level](../runtime-config/runtime-config-client.md#GUC-ICU-VALIDATION-LEVEL) 控制該訊息的
回報方式。除非設為 `ERROR`，
否則仍然會建立該定序，但其行為可能不是使用者原本想要的。

<a id="ICU-LANGUAGE-TAG"></a>

#### 23.1.5.3. 語言標籤 [#](#ICU-LANGUAGE-TAG)

語言標籤定義於 BCP 47 中，是用來
識別語言、地區及區域設定其他相關資訊的標準化識別碼。

基本的語言標籤形式很單純，就是
*`language`*`-`*`region`*；
或甚至僅有 *`language`*。
*`language`* 是一個語言代碼
（例如法語為 `fr`），
*`region`* 則是一個地區代碼
（例如加拿大為 `CA`）。範例：
`ja-JP`、`de`，或
`fr-CA`。

定序設定也可以包含在語言標籤中，以自訂
定序行為。ICU 允許廣泛的自訂，例如
對重音、大小寫及標點符號的敏感度（或不敏感度）；
文字中數字的處理方式；以及許多其他選項，以滿足
多樣化的使用需求。

若要在語言標籤中加入這些額外的定序資訊，
請附加 `-u`，表示後面接著有額外的
定序設定，接著是一個或多個
`-`*`key`*`-`*`value`*
配對。*`key`* 是[定序設定](collation.md#ICU-COLLATION-SETTINGS)的
鍵值，*`value`* 是該設定的合法值。對於
布林值設定，`-`*`key`*
可以在不指定對應
`-`*`value`* 的情況下使用，此時隱含的值即為
`true`。

舉例來說，語言標籤 `en-US-u-kn-ks-level2`
代表美國地區的英文區域設定，並搭配
定序設定 `kn` 設為 `true`
以及 `ks` 設為 `level2`。這些
設定表示該定序將不區分大小寫，且將一連串
數字視為單一數值：

```

CREATE COLLATION mycollation5 (provider = icu, deterministic = false, locale = 'en-US-u-kn-ks-level2');
SELECT 'aB' = 'Ab' COLLATE mycollation5 as result;
 result
--------
 t
(1 row)

SELECT 'N-45' < 'N-123' COLLATE mycollation5 as result;
 result
--------
 t
(1 row)
```

如需使用語言標籤搭配自訂定序資訊的更多細節與範例，
詳見[第 23.2.3 節](collation.md#ICU-CUSTOM-COLLATIONS)。

<a id="LOCALE-PROBLEMS"></a>

### 23.1.6. 問題 [#](#LOCALE-PROBLEMS)

如果區域設定支援未依照上述說明運作，
請檢查你作業系統中的區域設定支援是否
設定正確。若要檢查系統上安裝了哪些區域設定，
若你的作業系統有提供，可以使用
`locale -a` 指令。

請確認 PostgreSQL 實際使用的區域設定
是否如你所想。`LC_COLLATE` 與 `LC_CTYPE`
設定是在建立資料庫時決定的，且除非建立新的資料庫，
否則無法變更。其他區域設定
（包括 `LC_MESSAGES` 與 `LC_MONETARY`）
最初是由伺服器啟動時所處的環境決定，但
可以隨時動態變更。你可以使用 `SHOW` 指令
檢查目前作用中的區域設定。

原始碼發行版中的 `src/test/locale` 目錄
包含一組
PostgreSQL 區域設定支援的測試套件。

如果用戶端應用程式是透過解析錯誤訊息的文字來處理伺服器端的錯誤，
那麼當伺服器的訊息使用不同語言時，這類應用程式顯然會出現問題。建議此類
應用程式的作者改用錯誤代碼機制。

維護訊息翻譯目錄需要許多志工持續不斷地
付出，他們希望能看到
PostgreSQL 好好地使用自己偏好的語言。
如果你所使用語言的訊息目前不存在，或尚未完整翻譯，
歡迎你提供協助。如果你想
幫忙，請參閱[第 56 章](../../internals/nls/README.md)，或寫信給開發者
郵件清單。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/locale.html)（原文版本：18.6；核對日期：2026-09-28）
