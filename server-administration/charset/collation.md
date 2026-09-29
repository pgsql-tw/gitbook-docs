<a id="COLLATION"></a>

## 23.2. 定序支援 [#](#COLLATION)

[23.2.1. 概念](collation.md#COLLATION-CONCEPTS)

[23.2.2. 管理定序](collation.md#COLLATION-MANAGING)

[23.2.3. ICU 自訂定序](collation.md#ICU-CUSTOM-COLLATIONS)

<a id="id-1.6.10.4.2"></a>

定序（collation）功能讓你可以針對每個欄位，甚至每個運算，
指定資料的排序順序與字元分類行為。
這緩解了資料庫的
`LC_COLLATE` 與 `LC_CTYPE` 設定
在建立之後便無法變更的限制。

<a id="COLLATION-CONCEPTS"></a>

### 23.2.1. 概念 [#](#COLLATION-CONCEPTS)

概念上，每一個可定序資料型別的運算式都有一個
定序。（內建的可定序資料型別為
`text`、`varchar` 與 `char`。
使用者自訂的基礎型別也可以被標記為可定序，當然，
建立在可定序資料型別之上的[*[網域](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN)*](../../appendixes/glossary/README.md#GLOSSARY-DOMAIN)也是可定序的。）若該
運算式是欄位參照，則該運算式的定序即為
該欄位所定義的定序。若該運算式是常數，則
定序為該常數之資料型別的預設定序。較複雜運算式的定序則
如下所述，由其輸入的定序衍生而來。

某個運算式的定序可以是「default（預設）」
定序，即代表該資料庫所定義的區域設定。某個
運算式的定序也可能是不確定的（indeterminate）。在這種情況下，需要知道
定序的排序操作及其他操作將會失敗。

當資料庫系統需要執行排序或字元
分類時，它會使用輸入運算式的定序。舉例來說，這會發生在
`ORDER BY` 子句，
以及像 `<` 這樣的函式或運算子呼叫中。
`ORDER BY` 子句所套用的定序，
就是排序鍵的定序。函式或運算子呼叫所套用的定序，
則如下所述，由其引數衍生而來。除了比較運算子之外，
在大小寫轉換函式（例如
`lower`、`upper` 與
`initcap`）、模式比對運算子，以及
`to_char` 與相關函式中，也都會考慮定序。

對於函式或運算子呼叫，藉由檢視引數定序所衍生出的
定序，會在執行階段用來執行
指定的運算。若函式或運算子呼叫的結果屬於
可定序資料型別，該定序也會在剖析階段被用作
該函式或運算子運算式所定義的定序，以備
在有外圍運算式需要知道其定序時使用。

運算式的*定序衍生（collation derivation）*
可以是隱含（implicit）或明確（explicit）的。這項區別會影響
當運算式中出現多個不同定序時，如何組合這些定序。當使用
`COLLATE` 子句時，即發生明確的定序
衍生；所有其他定序衍生皆為隱含的。當需要
組合多個定序時（例如在函式呼叫中），會採用以下
規則：

1. 若任何輸入運算式具有明確的定序衍生，則
   所有輸入運算式中明確衍生的定序都必須
   相同，否則會引發錯誤。若存在任何明確
   衍生的定序，該定序即為
   定序組合的結果。
2. 否則，所有輸入運算式都必須具有相同的隱含
   定序衍生，或使用預設定序。若存在任何非預設
   定序，該定序即為定序組合的結果。
   否則，結果即為預設定序。
3. 若輸入運算式之間存在互相衝突的非預設隱含定序，
   則該組合會被視為具有不確定的
   定序。除非所呼叫的特定函式需要知道應套用哪個
   定序，否則這並不算是錯誤情況。若
   確實需要，則會在執行階段引發錯誤。

舉例來說，考慮下列資料表定義：

```

CREATE TABLE test1 (
    a text COLLATE "de_DE",
    b text COLLATE "es_ES",
    ...
);
```

那麼在

```

SELECT a < 'foo' FROM test1;
```

中，`<` 比較會依照
`de_DE` 規則執行，因為該運算式結合了
隱含衍生的定序與預設定序。但在

```

SELECT a < ('foo' COLLATE "fr_FR") FROM test1;
```

中，比較則會使用 `fr_FR` 規則執行，
因為明確的定序衍生會覆寫隱含的定序衍生。
此外，給定

```

SELECT a < b FROM test1;
```

剖析器無法判斷應套用哪一個定序，因為
`a` 與 `b` 這兩個欄位的隱含定序
互相衝突。由於 `<` 運算子
確實需要知道該使用哪個定序，這會導致
錯誤。你可以在任一輸入運算式上附加明確的定序
指定符來解決此錯誤，如下所示：

```

SELECT a < b COLLATE "de_DE" FROM test1;
```

或等效地寫成

```

SELECT a COLLATE "de_DE" < b FROM test1;
```

另一方面，結構上類似的情況

```

SELECT a || b FROM test1;
```

則不會導致錯誤，因為 `||` 運算子
不在乎定序：無論定序為何，其結果都相同。

指派給某個函式或運算子之組合輸入運算式的定序，
若該函式或運算子傳回的結果屬於可定序
資料型別，也會被視為套用於該函式或運算子的
結果。因此，在

```

SELECT * FROM test1 ORDER BY a || 'foo';
```

中，排序將依照 `de_DE` 規則進行。
但這個查詢：

```

SELECT * FROM test1 ORDER BY a || b;
```

會導致錯誤，因為即使 `||` 運算子
不需要知道定序，`ORDER BY` 子句卻需要。
如同之前一樣，這項衝突可以透過明確的定序
指定符解決：

```

SELECT * FROM test1 ORDER BY a || b COLLATE "fr_FR";
```

<a id="COLLATION-MANAGING"></a>

### 23.2.2. 管理定序 [#](#COLLATION-MANAGING)

定序是一種 SQL 綱要物件，它將一個 SQL 名稱對應到
作業系統中已安裝函式庫所提供的區域設定。定序
定義具有一個*提供者（provider）*，用來指定哪個
函式庫提供區域設定資料。其中一種標準提供者名稱
是 `libc`，它使用作業系統 C 函式庫所
提供的區域設定。這些也是作業系統所提供的大多數工具
所使用的區域設定。另一個提供者
是 `icu`，它使用外部的
ICU<a id="id-1.6.10.4.5.2.4"></a> 函式庫。ICU 區域設定只有在
建置 PostgreSQL 時已設定 ICU 支援的情況下才能使用。

由 `libc` 提供的定序物件，對應到
`LC_COLLATE` 與 `LC_CTYPE`
設定的組合，如同 `setlocale()` 系統函式庫呼叫所接受的形式一般。（正如
其名稱所暗示的，定序的主要目的是設定
`LC_COLLATE`，用於控制排序順序。不過
在實務上，很少需要讓
`LC_CTYPE` 設定與
`LC_COLLATE` 不同，因此將這兩者
歸納為同一個概念，會比另外建立一套
針對每個運算式設定 `LC_CTYPE` 的機制來得方便。）此外，
`libc` 定序與某個字元集編碼綁定在一起（見[第 23.3 節](multibyte.md)）。
同一個定序名稱可能存在於不同的編碼中。

由 `icu` 提供的定序物件，對應到
ICU 函式庫所提供的具名定序器（collator）。ICU 不支援
分開設定「collate」與「ctype」，因此
兩者永遠相同。此外，ICU 定序與編碼
無關，因此在一個資料庫中，同一名稱的 ICU 定序永遠
只有一個。

<a id="COLLATION-MANAGING-STANDARD"></a>

#### 23.2.2.1. 標準定序 [#](#COLLATION-MANAGING-STANDARD)

在所有平台上，都支援以下定序：

`unicode`
:   這個 SQL 標準定序使用 Unicode Collation
    Algorithm（Unicode 定序演算法），搭配 Default Unicode Collation Element Table
    進行排序。它在所有編碼下皆可使用。使用此定序
    需要 ICU 支援，且若 PostgreSQL 是以不同版本的 ICU 建置，
    其行為可能會有所變動。（此定序的行為與
    ICU root 區域設定相同；見
    [`und-x-icu`（表示「undefined，未定義」）](collation.md#COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU)。）

`ucs_basic`
:   這個 SQL 標準定序使用 Unicode 碼點值進行排序，
    而非自然語言順序，且只有 ASCII 字母
    「`A`」到
    「`Z`」被視為字母。其
    行為在所有版本間皆高效且穩定。僅適用於
    編碼 `UTF8`。（此定序的行為與
    `UTF8` 編碼下 libc 區域設定規格
    `C` 的行為相同。）

`pg_unicode_fast`
:   此定序依 Unicode 碼點值排序，而非
    自然語言順序。對於
    `lower`、`initcap` 及 `upper`
    這幾個函式，它使用
    Unicode 完整大小寫對應（full case mapping）。對於模式比對
    （包括正規表示式），它使用 Unicode [相容性
    屬性（Compatibility Properties）](https://www.unicode.org/reports/tr18/#Compatibility_Properties) 的標準（Standard）變體。在
    某一個 Postgres 主要版本內，其行為高效且穩定。僅
    適用於編碼 `UTF8`。

`pg_c_utf8`
:   此定序依 Unicode 碼點值排序，而非
    自然語言順序。對於
    `lower`、`initcap` 及
    `upper` 這幾個函式，它使用
    Unicode 簡易大小寫對應（simple case mapping）。對於模式比對
    （包括正規表示式），它使用 Unicode [相容性
    屬性](https://www.unicode.org/reports/tr18/#Compatibility_Properties) 的 POSIX 相容變體。在某一個
    PostgreSQL 主要版本內，其行為高效且穩定。此定序
    僅適用於編碼 `UTF8`。

`C`（等同於 `POSIX`）
:   `C` 與 `POSIX` 定序
    以「傳統 C」行為為基礎。它們依位元組
    值排序，而非自然語言順序，且只有 ASCII 字母
    「`A`」到
    「`Z`」被視為字母。針對
    給定的資料庫編碼，其行為在所有版本間皆高效且穩定，
    但不同的資料庫編碼之間，行為可能有所差異。

`default`
:   `default` 定序選用資料庫建立時所指定的
    區域設定。

依作業系統支援情況，可能還有其他定序可用。這些額外定序的
效率與穩定性，取決於定序提供者、
提供者版本及區域設定。

<a id="COLLATION-MANAGING-PREDEFINED"></a>

#### 23.2.2.2. 預先定義的定序 [#](#COLLATION-MANAGING-PREDEFINED)

若作業系統支援在單一程式中使用多個區域設定
（`newlocale` 及相關函式），
或已設定 ICU 支援，
則在初始化資料庫叢集時，`initdb`
會依據當時在作業系統中找到的所有區域設定，
在系統目錄 `pg_collation` 中填入
對應的定序。

若要檢視目前可用的區域設定，可使用查詢 `SELECT
* FROM pg_collation`，或在 psql 中使用
`\dOS+` 指令。

<a id="COLLATION-MANAGING-PREDEFINED-LIBC"></a>

##### 23.2.2.2.1. libc 定序 [#](#COLLATION-MANAGING-PREDEFINED-LIBC)

舉例來說，作業系統可能會
提供一個名為 `de_DE.utf8` 的區域設定。
此時 `initdb` 便會為編碼 `UTF8`
建立一個名為 `de_DE.utf8` 的定序，
其 `LC_COLLATE` 與
`LC_CTYPE` 皆設定為 `de_DE.utf8`。
它同時也會建立一個名稱去掉 `.utf8`
標記的定序。因此你也可以使用
`de_DE` 這個名稱來使用該定序，
這樣寫起來較不繁瑣，也讓名稱較不受限於編碼。不過請注意，
初始的定序名稱集合仍然
與平台有關。

`libc` 所提供的預設定序集合，會直接對應到
作業系統中已安裝的區域設定，可以使用
`locale -a` 指令列出這些區域設定。若
需要一個 `LC_COLLATE` 與
`LC_CTYPE` 值不同的 `libc` 定序，
或是資料庫系統初始化後作業系統安裝了新的
區域設定，則可以使用
[CREATE COLLATION](../../reference/sql-commands/sql-createcollation.md) 指令建立新的定序。
也可以使用
[`pg_import_system_collations()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-COLLATION) 函式，一次匯入大量的新作業系統區域設定。

在任何特定的資料庫中，只有使用該
資料庫編碼的定序才有意義。`pg_collation` 中的
其他項目會被忽略。因此，即使去除標記後的定序
名稱（例如 `de_DE`）在全域中並不唯一，
在給定的資料庫內仍可以被視為唯一。
建議使用去除標記後的定序名稱，因為如果你日後決定
改用其他資料庫編碼，需要變更的地方會少一項。
不過請注意，無論資料庫編碼為何，
`default`、`C` 及 `POSIX` 定序皆可使用。

即使兩個不同的定序物件屬性完全相同，
PostgreSQL 仍會將它們視為不相容的定序物件。
因此，舉例來說，

```

SELECT a COLLATE "C" < b COLLATE "POSIX" FROM test1;
```

即使 `C` 與 `POSIX`
定序的行為完全相同，此陳述式仍會引發錯誤。因此不建議
混用去除標記與未去除標記的定序名稱。

<a id="COLLATION-MANAGING-PREDEFINED-ICU"></a>

##### 23.2.2.2.2. ICU 定序 [#](#COLLATION-MANAGING-PREDEFINED-ICU)

在 ICU 中，逐一列舉所有可能的區域設定名稱並不合理。ICU
使用一套特殊的區域設定命名系統，但可用來命名一個區域設定
的方式，比實際獨特的區域設定數量還多。
`initdb` 會使用 ICU API 擷取出一組獨特的
區域設定，用以填入初始的定序集合。ICU 所提供的定序，
會以 BCP 47 語言標籤格式建立在 SQL 環境中，並附加
「private use（私人使用）」
延伸標記 `-x-icu`，以便與
libc 區域設定區分開來。

以下是一些可能被建立的定序範例：

<a id="COLLATION-MANAGING-PREDEFINED-ICU-DE-X-ICU"></a>

`de-x-icu` [#](#COLLATION-MANAGING-PREDEFINED-ICU-DE-X-ICU)
:   德文定序，預設變體
<a id="COLLATION-MANAGING-PREDEFINED-ICU-DE-AT-X-ICU"></a>

`de-AT-x-icu` [#](#COLLATION-MANAGING-PREDEFINED-ICU-DE-AT-X-ICU)
:   奧地利地區的德文定序，預設變體

    （也會存在例如 `de-DE-x-icu`
    或 `de-CH-x-icu` 等定序，但截至本文撰寫時，它們
    等同於 `de-x-icu`。）
<a id="COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU"></a>

`und-x-icu`（表示「undefined，未定義」） [#](#COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU)
:   ICU「root（根）」定序。使用此定序可取得
    合理的、與語言無關的排序順序。

某些（較少使用的）編碼不受 ICU 支援。當
資料庫編碼為這類編碼之一時，
`pg_collation` 中的 ICU 定序項目會被忽略。嘗試使用其中之一
將會引發類似「collation "de-x-icu" for
encoding "WIN874" does not exist」的錯誤。

<a id="COLLATION-CREATE"></a>

#### 23.2.2.3. 建立新的定序物件 [#](#COLLATION-CREATE)

若標準與預先定義的定序不敷使用，使用者可以
使用 SQL
指令 [CREATE COLLATION](../../reference/sql-commands/sql-createcollation.md) 建立自己的定序物件。

標準與預先定義的定序，如同所有預先定義的物件一樣，
都位於 `pg_catalog` 綱要中。
使用者自訂的定序應建立在使用者綱要中。這也能
確保它們會被 `pg_dump` 儲存。

<a id="COLLATION-MANAGING-CREATE-LIBC"></a>

##### 23.2.2.3.1. libc 定序 [#](#COLLATION-MANAGING-CREATE-LIBC)

可以像這樣建立新的 libc 定序：

```

CREATE COLLATION german (provider = libc, locale = 'de_DE');
```

此指令中 `locale` 子句可接受的確切值，
取決於作業系統。在類 Unix 系統上，
`locale -a` 指令會顯示一份清單。

由於預先定義的 libc 定序，已經包含了資料庫實例
初始化時作業系統中所定義的所有定序，
因此通常不太需要手動建立新的定序。
可能的原因是想使用不同的命名系統（在此情況下
另見[第 23.2.2.3.3 節](collation.md#COLLATION-COPY)），或是作業系統
已升級並提供了新的區域設定定義（在此情況下另見
[`pg_import_system_collations()`](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-COLLATION)）。

<a id="COLLATION-MANAGING-CREATE-ICU"></a>

##### 23.2.2.3.2. ICU 定序 [#](#COLLATION-MANAGING-CREATE-ICU)

可以像這樣建立 ICU 定序：

```

CREATE COLLATION german (provider = icu, locale = 'de-DE');
```

ICU 區域設定以 BCP 47 [語言標籤](locale.md#ICU-LANGUAGE-TAG) 的形式指定，
但也可以接受大多數 libc 風格的區域設定名稱。若有可能，
libc 風格的區域設定名稱會被轉換為語言標籤。

新的 ICU 定序可以透過在語言標籤中加入
定序屬性，對定序行為進行廣泛的自訂。詳見
[第 23.2.3 節](collation.md#ICU-CUSTOM-COLLATIONS)。

<a id="COLLATION-COPY"></a>

##### 23.2.2.3.3. 複製定序 [#](#COLLATION-COPY)

[CREATE COLLATION](../../reference/sql-commands/sql-createcollation.md) 指令也可以用來
從既有的定序建立新定序，這在你想於應用程式中
使用與作業系統無關的定序名稱、建立相容性名稱，
或以較易讀的名稱使用 ICU 提供的定序時會很有用。例如：

```

CREATE COLLATION german FROM "de_DE";
CREATE COLLATION french FROM "fr-x-icu";
```

<a id="COLLATION-NONDETERMINISTIC"></a>

#### 23.2.2.4. 非確定性定序 [#](#COLLATION-NONDETERMINISTIC)

定序可以是*確定性（deterministic）*
或*非確定性（nondeterministic）*的。確定性定序使用
確定性比較，也就是只有在兩個字串由完全相同的位元組序列
組成時，才會將它們視為相等。非確定性
比較則可能將由不同位元組組成的字串判定為相等。典型的情況包括
不區分大小寫的比較、不區分重音的比較，以及
不同 Unicode 正規化形式之字串的比較。實際上是否要
實作出這類不敏感的比較，取決於定序提供者；
deterministic（確定性）旗標只決定了在出現平手時
是否以逐位元組比較來分出勝負。如需更多關於
術語的資訊，另見 [Unicode Technical
Standard 10](https://www.unicode.org/reports/tr10)。

若要建立非確定性定序，請在 `CREATE
COLLATION` 中指定屬性
`deterministic = false`，例如：

```

CREATE COLLATION ndcoll (provider = icu, locale = 'und', deterministic = false);
```

此範例會以非確定性的方式使用標準 Unicode 定序。
特別是，這樣可以讓不同正規化形式的字串
被正確地比較為相等。更有趣的範例則會運用
上述 ICU 自訂功能。例如：

```

CREATE COLLATION case_insensitive (provider = icu, locale = 'und-u-ks-level2', deterministic = false);
CREATE COLLATION ignore_accents (provider = icu, locale = 'und-u-ks-level1-kc-true', deterministic = false);
```

所有標準與預先定義的定序皆為確定性定序，所有
使用者自訂的定序預設也都是確定性定序。雖然
非確定性定序能帶來更「正確」的行為，
尤其是在考量 Unicode 的完整能力及其眾多特殊情況時，
它們也有一些缺點。首要的是，使用它們會導致
效能下降。請特別注意，B 樹（B-tree）無法對使用
非確定性定序的索引進行去重複（deduplication）。此外，
某些操作在非確定性定序下無法使用，
例如部分模式比對操作。因此，應該只有在
確實需要非確定性定序的情況下才使用它們。

### 提示

若要處理不同 Unicode 正規化形式的文字，另一種選擇是使用
`normalize` 與 `is normalized`
這兩個函式／運算式來預先處理或檢查字串，
而不使用非確定性定序。這兩種做法各有不同的取捨。

<a id="ICU-CUSTOM-COLLATIONS"></a>

### 23.2.3. ICU 自訂定序 [#](#ICU-CUSTOM-COLLATIONS)

ICU 允許透過在語言標籤中定義帶有定序設定的新定序，
對定序行為進行廣泛的控制。這些
設定可以修改定序順序，以滿足各種需求。舉例
來說：

```

-- ignore differences in accents and case
CREATE COLLATION ignore_accent_case (provider = icu, deterministic = false, locale = 'und-u-ks-level1');
SELECT 'Å' = 'A' COLLATE ignore_accent_case; -- true
SELECT 'z' = 'Z' COLLATE ignore_accent_case; -- true

-- upper case letters sort before lower case.
CREATE COLLATION upper_first (provider = icu, locale = 'und-u-kf-upper');
SELECT 'B' < 'b' COLLATE upper_first; -- true

-- treat digits numerically and ignore punctuation
CREATE COLLATION num_ignore_punct (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-kn');
SELECT 'id-45' < 'id-123' COLLATE num_ignore_punct; -- true
SELECT 'w;x*y-z' = 'wxyz' COLLATE num_ignore_punct; -- true
```

許多可用的選項說明於[第 23.2.3.2 節](collation.md#ICU-COLLATION-SETTINGS)中，更多詳情另見[第 23.2.3.5 節](collation.md#ICU-EXTERNAL-REFERENCES)。

<a id="ICU-COLLATION-COMPARISON-LEVELS"></a>

#### 23.2.3.1. ICU 比較層級 [#](#ICU-COLLATION-COMPARISON-LEVELS)

ICU 中兩個字串的比較（定序）是由一套
多層級（multi-level）流程所決定，其中文字特徵會被分組為
「層級（level）」。每個層級的處理方式，由[定序設定](collation.md#ICU-COLLATION-SETTINGS-TABLE)所控制。層級
越高，代表越精細的文字特徵。

[表格 23.1](collation.md#ICU-COLLATION-LEVELS) 顯示了在判定
給定層級的相等性時，哪些文字特徵差異會被視為
顯著。Unicode 字元 `U+2063` 是一個
隱形分隔符號，如表中所示，在
`identic` 以下的所有比較層級中都會被忽略。

<a id="ICU-COLLATION-LEVELS"></a>

**表格 23.1. ICU 定序層級**

<table border="1" class="table" summary="ICU Collation Levels"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/><col class="col6"/><col class="col7"/><col class="col8"/></colgroup><thead><tr><th>層級</th><th>說明</th><th><code class="literal">'f' = 'f'</code></th><th><code class="literal">'ab' = U&amp;'a\2063b'</code></th><th><code class="literal">'x-y' = 'x_y'</code></th><th><code class="literal">'g' = 'G'</code></th><th><code class="literal">'n' = 'ñ'</code></th><th><code class="literal">'y' = 'z'</code></th></tr></thead><tbody><tr><td>level1</td><td>基本字元（Base Character）</td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td></tr><tr><td>level2</td><td>重音（Accents）</td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr><tr><td>level3</td><td>大小寫／變體（Case/Variants）</td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr><tr><td>level4</td><td>標點符號（Punctuation）<a class="footnote" href="#ftn.id-1.6.10.4.6.3.4.2.10.4.2.1"><sup class="footnote" id="id-1.6.10.4.6.3.4.2.10.4.2.1">[a]</sup></a></td><td><code class="literal">true</code></td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr><tr><td>identic</td><td>全部（All）</td><td><code class="literal">true</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td><td><code class="literal">false</code></td></tr></tbody><tbody class="footnotes"><tr><td colspan="8"><div class="footnote" id="ftn.id-1.6.10.4.6.3.4.2.10.4.2.1"><p><a class="para" href="#id-1.6.10.4.6.3.4.2.10.4.2.1"><sup class="para">[a] </sup></a>僅適用於
         <code class="literal">ka-shifted</code>；見 <a class="xref" href="collation.md#ICU-COLLATION-SETTINGS-TABLE">表格 23.2</a></p></div></td></tr></tbody></table>

<br>

在每一個層級，即使完全關閉正規化，系統仍會進行
基本的正規化。舉例來說，`'á'` 可能由
碼點 `U&'\0061\0301'` 組成，也可能由單一
碼點 `U&'\00E1'` 組成，這兩種序列
即使在 `identic` 層級也會被視為相等。若要將
碼點表示法的任何差異都視為不同，請使用建立時
`deterministic` 設為
`true` 的定序。

<a id="ICU-COLLATION-LEVEL-EXAMPLES"></a>

##### 23.2.3.1.1. 定序層級範例 [#](#ICU-COLLATION-LEVEL-EXAMPLES)

```

CREATE COLLATION level3 (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-level3');
CREATE COLLATION level4 (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-level4');
CREATE COLLATION identic (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-identic');

-- invisible separator ignored at all levels except identic
SELECT 'ab' = U&'a\2063b' COLLATE level4; -- true
SELECT 'ab' = U&'a\2063b' COLLATE identic; -- false

-- punctuation ignored at level3 but not at level 4
SELECT 'x-y' = 'x_y' COLLATE level3; -- true
SELECT 'x-y' = 'x_y' COLLATE level4; -- false
```

<a id="ICU-COLLATION-SETTINGS"></a>

#### 23.2.3.2. ICU 區域設定的定序設定 [#](#ICU-COLLATION-SETTINGS)

[表格 23.2](collation.md#ICU-COLLATION-SETTINGS-TABLE) 顯示了可用的
定序設定，這些設定可以作為語言標籤的一部分，用來
自訂定序。

<a id="ICU-COLLATION-SETTINGS-TABLE"></a>

**表格 23.2. ICU 定序設定**

<table border="1" class="table" summary="ICU Collation Settings"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>鍵</th><th>值</th><th>預設值</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">co</code></td><td><code class="literal">emoji</code>, <code class="literal">phonebk</code>, <code class="literal">standard</code>, <em class="replaceable"><code>...</code></em></td><td><code class="literal">standard</code></td><td>
          定序類型。額外選項與詳情見 <a class="xref" href="collation.md#ICU-EXTERNAL-REFERENCES">第 23.2.3.5 節</a>。
         </td></tr><tr><td><code class="literal">ka</code></td><td><code class="literal">noignore</code>, <code class="literal">shifted</code></td><td><code class="literal">noignore</code></td><td>
          若設為 <code class="literal">shifted</code>，會使某些字元
          （例如標點符號或空格）在比較時被忽略。鍵
          <code class="literal">ks</code> 必須設為 <code class="literal">level3</code> 或
          更低才會生效。設定鍵 <code class="literal">kv</code> 可控制要忽略哪些
          字元類別。
         </td></tr><tr><td><code class="literal">kb</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
          第 2 層級差異的反向比較。例如，
          區域設定 <code class="literal">und-u-kb</code> 會將 <code class="literal">'àe'</code>
          排在 <code class="literal">'aé'</code> 之前。
         </td></tr><tr><td><code class="literal">kc</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
<p>
           將大小寫分離為介於重音與其他第 3 層級特徵之間的「第
           2.5 層級」。
          </p>
<p>
           若設為 <code class="literal">true</code>，且 <code class="literal">ks</code> 設
           為 <code class="literal">level1</code>，會忽略重音，但仍會考慮
           大小寫。
          </p>
</td></tr><tr><td><code class="literal">kf</code></td><td>
<code class="literal">upper</code>, <code class="literal">lower</code>,
          <code class="literal">false</code>
</td><td><code class="literal">false</code></td><td>
          若設為 <code class="literal">upper</code>，大寫會排在
          小寫之前。若設為 <code class="literal">lower</code>，小寫會排在
          大寫之前。若設為 <code class="literal">false</code>，排序方式則取決於
          該區域設定的規則。
         </td></tr><tr><td><code class="literal">kn</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
          若設為 <code class="literal">true</code>，字串中的數字會被
          視為單一數值，而非一連串
          數字。例如，<code class="literal">'id-45'</code> 會排在
          <code class="literal">'id-123'</code> 之前。
         </td></tr><tr><td><code class="literal">kk</code></td><td><code class="literal">true</code>, <code class="literal">false</code></td><td><code class="literal">false</code></td><td>
<p>
           啟用完整正規化；可能會影響效能。即使設為
           <code class="literal">false</code>，仍會進行基本
           正規化。需要完整正規化的語言，其區域設定通常會預設啟用此設定。
          </p>
<p>
           完整正規化在某些情況下很重要，例如當
           多個重音符號套用在同一個字元上時。舉例來說，
           碼點序列 <code class="literal">U&amp;'\0065\0323\0302'</code>
           與 <code class="literal">U&amp;'\0065\0302\0323'</code> 分別代表
           以不同順序套用了揚抑符（circumflex）與下加點（dot-below）重音符號的
           <code class="literal">e</code>。啟用完整正規化
           後，這些碼點序列會被視為相等；否則它們
           就不相等。
          </p>
</td></tr><tr><td><code class="literal">kr</code></td><td>
<code class="literal">space</code>, <code class="literal">punct</code>,
          <code class="literal">symbol</code>, <code class="literal">currency</code>,
          <code class="literal">digit</code>, <em class="replaceable"><code>script-id</code></em>
</td><td> </td><td>
<p>
           設為一個或多個合法值，或任何 BCP 47
           <em class="replaceable"><code>script-id</code></em>，例如 <code class="literal">latn</code>
           （「拉丁文」）或 <code class="literal">grek</code>（「希臘文」）。多個值以
           「<code class="literal">-</code>」分隔。
          </p>
<p>
           重新定義各類字元的排序方式；在清單中位置較前面的
           類別，其字元會排在位置較後面的類別之前。例如，值
           <code class="literal">digit-currency-space</code>（作為語言標籤的一部分，
           如 <code class="literal">und-u-kr-digit-currency-space</code>）會將
           標點符號排在數字與空格之前。
          </p>
</td></tr><tr><td><code class="literal">ks</code></td><td><code class="literal">level1</code>, <code class="literal">level2</code>, <code class="literal">level3</code>, <code class="literal">level4</code>, <code class="literal">identic</code></td><td><code class="literal">level3</code></td><td>
          判定相等性時的敏感度（或稱「強度」），
          <code class="literal">level1</code> 對差異最不敏感，
          <code class="literal">identic</code> 對差異最敏感。詳見
          <a class="xref" href="collation.md#ICU-COLLATION-LEVELS">表格 23.1</a>。
         </td></tr><tr><td><code class="literal">kv</code></td><td>
<code class="literal">space</code>, <code class="literal">punct</code>,
          <code class="literal">symbol</code>, <code class="literal">currency</code>
</td><td><code class="literal">punct</code></td><td>
          第 3 層級比較時要忽略的字元類別。設為
          較後面的值時會包含較前面的值；
          例如 <code class="literal">symbol</code> 在要忽略的字元中
          也會包含 <code class="literal">punct</code> 與
          <code class="literal">space</code>。鍵 <code class="literal">ka</code> 必須設為
          <code class="literal">shifted</code>，且鍵 <code class="literal">ks</code> 必須設為
          <code class="literal">level3</code> 或更低才會生效。
         </td></tr></tbody></table>

<br>

預設值可能取決於區域設定，上表並非
完整清單。更多選項與詳情另見[第 23.2.3.5 節](collation.md#ICU-EXTERNAL-REFERENCES)。

### 注意

對於許多定序設定而言，你必須在建立定序時將
`deterministic` 設為 `false`，
該設定才會產生預期效果（見[第 23.2.2.4 節](collation.md#COLLATION-NONDETERMINISTIC)）。此外，某些
設定只有在鍵 `ka` 設為
`shifted` 時才會生效（見[表格 23.2](collation.md#ICU-COLLATION-SETTINGS-TABLE)）。

<a id="ICU-LOCALE-EXAMPLES"></a>

#### 23.2.3.3. 定序設定範例 [#](#ICU-LOCALE-EXAMPLES)

<a id="COLLATION-MANAGING-CREATE-ICU-DE-U-CO-PHONEBK-X-ICU"></a>

`CREATE COLLATION "de-u-co-phonebk-x-icu" (provider = icu, locale = 'de-u-co-phonebk');` [#](#COLLATION-MANAGING-CREATE-ICU-DE-U-CO-PHONEBK-X-ICU)
:   採用電話簿定序類型的德文定序
<a id="COLLATION-MANAGING-CREATE-ICU-UND-U-CO-EMOJI-X-ICU"></a>

`CREATE COLLATION "und-u-co-emoji-x-icu" (provider = icu, locale = 'und-u-co-emoji');` [#](#COLLATION-MANAGING-CREATE-ICU-UND-U-CO-EMOJI-X-ICU)
:   依照 Unicode Technical Standard #51，採用表情符號定序類型的根定序
<a id="COLLATION-MANAGING-CREATE-ICU-EN-U-KR-GREK-LATN"></a>

`CREATE COLLATION latinlast (provider = icu, locale = 'en-u-kr-grek-latn');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KR-GREK-LATN)
:   將希臘字母排在拉丁字母之前。（預設為拉丁字母在希臘字母之前。）
<a id="COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER"></a>

`CREATE COLLATION upperfirst (provider = icu, locale = 'en-u-kf-upper');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER)
:   將大寫字母排在小寫字母之前。（預設為
    小寫字母在前。）
<a id="COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER-KR-GREK-LATN"></a>

`CREATE COLLATION special (provider = icu, locale = 'en-u-kf-upper-kr-grek-latn');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER-KR-GREK-LATN)
:   結合以上兩個選項。

<a id="ICU-TAILORING-RULES"></a>

#### 23.2.3.4. ICU 裁定規則（Tailoring Rules） [#](#ICU-TAILORING-RULES)

若上述定序設定所提供的選項不敷使用，可以透過裁定規則
變更定序元素的順序，其語法詳見
<https://unicode-org.github.io/icu/userguide/collation/customization/>。

以下這個簡單範例，會以 root 區域設定為基礎，
搭配一條裁定規則建立一個定序：

```

CREATE COLLATION custom (provider = icu, locale = 'und', rules = '&V << w <<< W');
```

依照這條規則，字母「W」會排在
「V」之後，但被視為類似重音的次要差異。這類規則
包含在部分語言的區域設定定義之中。（當然，若某個
區域設定定義已經包含了所需的規則，就不需要再明確
指定一次。）

以下是一個較複雜的範例。以下陳述式建立了一個
名為 `ebcdic` 的定序，其規則會依照
EBCDIC 編碼的順序排序 US-ASCII 字元。

```

CREATE COLLATION ebcdic (provider = icu, locale = 'und',
rules = $$
& ' ' < '.' < '<' < '(' < '+' < \|
< '&' < '!' < '$' < '*' < ')' < ';'
< '-' < '/' < ',' < '%' < '_' < '>' < '?'
< '`' < ':' < '#' < '@' < \' < '=' < '"'
<*a-r < '~' <*s-z < '^' < '[' < ']'
< '{' <*A-I < '}' <*J-R < '\' <*S-Z <*0-9
$$);

SELECT c
FROM (VALUES ('a'), ('b'), ('A'), ('B'), ('1'), ('2'), ('!'), ('^')) AS x(c)
ORDER BY c COLLATE ebcdic;
 c
---
 !
 a
 b
 ^
 A
 B
 1
 2
```

<a id="ICU-EXTERNAL-REFERENCES"></a>

#### 23.2.3.5. ICU 外部參考資料 [#](#ICU-EXTERNAL-REFERENCES)

本節（[第 23.2.3 節](collation.md#ICU-CUSTOM-COLLATIONS)）僅對 ICU
行為與語言標籤做了簡短概述。技術細節、額外選項及新行為，
請參閱以下文件：

* [Unicode Technical Standard #35](https://www.unicode.org/reports/tr35/tr35-collation.html)
* [BCP 47](https://www.rfc-editor.org/info/bcp47)
* [CLDR repository](https://github.com/unicode-org/cldr/blob/master/common/bcp47/collation.xml)
* <https://unicode-org.github.io/icu/userguide/locale/>
* <https://unicode-org.github.io/icu/userguide/collation/>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/collation.html)（原文版本：18.6；核對日期：2026-09-28）
