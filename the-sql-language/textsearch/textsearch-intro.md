<a id="TEXTSEARCH-INTRO"></a>

## 12.1. 簡介 [#](#TEXTSEARCH-INTRO)

[12.1.1. 什麼是文件？](textsearch-intro.md#TEXTSEARCH-DOCUMENT)

[12.1.2. 基本文字比對](textsearch-intro.md#TEXTSEARCH-MATCHING)

[12.1.3. 設定](textsearch-intro.md#TEXTSEARCH-INTRO-CONFIGURATIONS)

全文檢索（或簡稱*文字搜尋*，text search）提供的功能，是找出符合某個*查詢*（query）的自然語言*文件*（document），並可選擇依與查詢的相關程度排序。最常見的搜尋類型，是找出所有包含指定*查詢詞*（query term）的文件，並依它們與查詢的*相似度*（similarity）順序回傳。`query` 與 `similarity` 的概念非常有彈性，取決於具體的應用。最簡單的搜尋會把 `query` 視為一組單字，並把 `similarity` 視為查詢單字在文件中出現的頻率。

資料庫中的文字搜尋運算子已經存在多年。PostgreSQL 為文字資料型別提供了 `~`、`~*`、`LIKE` 與 `ILIKE` 運算子，但它們缺少現代資訊系統所需的許多基本特性：

* 沒有語言學上的支援，即使是英文也一樣。正規表示式並不足夠，因為它們無法輕易處理衍生詞，例如 `satisfies` 與 `satisfy`。你可能會漏掉包含 `satisfies` 的文件，雖然你在搜尋 `satisfy` 時很可能也希望找到它們。雖然可以用 `OR` 來搜尋多種衍生形式，但這樣既繁瑣又容易出錯（有些單字可能有數千種衍生形式）。
* 它們不提供搜尋結果的排序（排名），因此在找到數千份相符文件時就沒有什麼用處。
* 它們往往很慢，因為沒有索引支援，每次搜尋都必須處理所有文件。

全文索引讓文件可以先經過*前置處理*（preprocess），並儲存索引供之後快速搜尋。前置處理包括：

* *將文件剖析為*語彙單元*（token）*。識別各種類別的語彙單元（例如數字、單字、複合詞、電子郵件地址）很有用，這樣就能以不同方式處理它們。原則上，語彙單元的類別取決於具體的應用，但就大多數用途而言，使用一組預先定義的類別就已足夠。PostgreSQL 使用*剖析器*（parser）來執行這個步驟。系統提供了一個標準剖析器，也可以依特定需求建立自訂的剖析器。
* *將語彙單元轉換為*詞素*（lexeme）*。詞素和語彙單元一樣是字串，但它已經過*正規化*（normalize），讓同一個單字的不同形式變得一致。例如，正規化幾乎都會將大寫字母轉為小寫，而且通常會移除字尾（例如英文中的 `s` 或 `es`）。這讓搜尋能找到同一個單字的各種變化形式，而不必繁瑣地輸入所有可能的變化。此外，這個步驟通常會剔除*停用詞*（stop word），也就是那些常見到對搜尋毫無用處的單字。（簡而言之，語彙單元是文件文字的原始片段，而詞素則是被認為對建立索引與搜尋有用的單字。）PostgreSQL 使用*字典*（dictionary）來執行這個步驟。系統提供了多種標準字典，也可以依特定需求建立自訂的字典。
* *以最適合搜尋的方式儲存前置處理後的文件*。例如，每份文件可以表示成一個已排序的正規化詞素陣列。除了詞素之外，通常也會希望儲存位置資訊，以用於*鄰近度排名*（proximity ranking），讓查詢單字分布較「密集」的文件，排名比查詢單字分散的文件更高。

字典讓你可以精細控制語彙單元的正規化方式。透過適當的字典，你可以：

* 定義不應建立索引的停用詞。
* 使用 Ispell 將同義詞對應到單一單字。
* 使用同義詞庫（thesaurus）將片語對應到單一單字。
* 使用 Ispell 字典將單字的各種變化形式對應到標準形式。
* 使用 Snowball 詞幹規則將單字的各種變化形式對應到標準形式。

系統提供了 `tsvector` 資料型別來儲存前置處理後的文件，並提供 `tsquery` 型別來表示處理過的查詢（[第 8.11 節](../datatype/datatype-textsearch.md)）。這些資料型別有許多可用的函式與運算子（[第 9.13 節](../functions/functions-textsearch.md)），其中最重要的是比對運算子 `@@`，我們會在[第 12.1.2 節](textsearch-intro.md#TEXTSEARCH-MATCHING)介紹它。全文檢索可以使用索引來加速（[第 12.9 節](textsearch-indexes.md)）。

<a id="TEXTSEARCH-DOCUMENT"></a>

### 12.1.1. 什麼是文件？ [#](#TEXTSEARCH-DOCUMENT)

<a id="id-1.5.11.4.10.2"></a>

*文件*（document）是全文檢索系統中的搜尋單位，例如一篇雜誌文章或一封電子郵件。文字搜尋引擎必須能夠剖析文件，並儲存詞素（關鍵詞）與其所屬文件之間的關聯。之後，這些關聯會用來搜尋包含查詢單字的文件。

在 PostgreSQL 中進行搜尋時，文件通常是資料庫資料表某一筆資料列中的文字欄位，也可能是這類欄位的組合（串接），這些欄位可能儲存在多個資料表中，或是動態取得的。換句話說，文件可以由不同的部分組合起來以建立索引，而它未必以完整的形式儲存在任何地方。例如：

```

SELECT title || ' ' ||  author || ' ' ||  abstract || ' ' || body AS document
FROM messages
WHERE mid = 12;

SELECT m.title || ' ' || m.author || ' ' || m.abstract || ' ' || d.body AS document
FROM messages m, docs d
WHERE m.mid = d.did AND m.mid = 12;
```

### 注意

實際上，在這些範例查詢中應該使用 `coalesce`，以免單一個 `NULL` 屬性導致整份文件的結果變成 `NULL`。

另一種做法是將文件以純文字檔的形式儲存在檔案系統中。在這種情況下，資料庫可以用來儲存全文索引並執行搜尋，再以某個唯一識別碼從檔案系統取得文件。不過，從資料庫外部取得檔案需要超級使用者權限或特殊的函式支援，因此這通常不如將所有資料都保存在 PostgreSQL 內部來得方便。此外，將所有資料都保存在資料庫中，也便於存取文件的中繼資料，以協助建立索引與顯示。

就文字搜尋的用途而言，每份文件都必須簡化為前置處理後的 `tsvector` 格式。搜尋與排名完全是在文件的 `tsvector` 表示法上進行的；只有在文件被選出要顯示給使用者時，才需要取得原始文字。因此我們常把 `tsvector` 當作文件本身來談，但它當然只是完整文件的精簡表示。

<a id="TEXTSEARCH-MATCHING"></a>

### 12.1.2. 基本文字比對 [#](#TEXTSEARCH-MATCHING)

PostgreSQL 中的全文檢索是以比對運算子 `@@` 為基礎，當 `tsvector`（文件）與 `tsquery`（查詢）相符時，它會回傳 `true`。哪一種資料型別寫在前面都沒有關係：

```

SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector @@ 'cat & rat'::tsquery;
 ?column?
----------
 t

SELECT 'fat & cow'::tsquery @@ 'a fat cat sat on a mat and ate a fat rat'::tsvector;
 ?column?
----------
 f
```

如上例所示，`tsquery` 並不只是原始文字，`tsvector` 也一樣。`tsquery` 包含搜尋詞，這些搜尋詞必須是已經正規化的詞素，並且可以使用 AND、OR、NOT 與 FOLLOWED BY 運算子組合多個搜尋詞。（語法細節請參閱[第 8.11.2 節](../datatype/datatype-textsearch.md#DATATYPE-TSQUERY)。）`to_tsquery`、`plainto_tsquery` 與 `phraseto_tsquery` 函式有助於將使用者撰寫的文字轉換為適當的 `tsquery`，主要是將文字中出現的單字正規化。同樣地，`to_tsvector` 用於剖析與正規化文件字串。因此實務上，文字搜尋比對看起來會比較像這樣：

```

SELECT to_tsvector('fat cats ate fat rats') @@ to_tsquery('fat & rat');
 ?column?
----------
 t
```

請注意，如果寫成下面這樣，這項比對就不會成功：

```

SELECT 'fat cats ate fat rats'::tsvector @@ to_tsquery('fat & rat');
 ?column?
----------
 f
```

因為這裡不會對單字 `rats` 進行正規化。`tsvector` 的元素是詞素，會被假設為已經正規化，因此 `rats` 與 `rat` 並不相符。

`@@` 運算子也支援 `text` 輸入，因此在簡單的情況下，可以省略將文字字串明確轉換為 `tsvector` 或 `tsquery` 的步驟。可用的變化形式有：

```

tsvector @@ tsquery
tsquery  @@ tsvector
text @@ tsquery
text @@ text
```

前兩種我們已經看過了。`text` `@@` `tsquery` 形式等同於 `to_tsvector(x) @@ y`。`text` `@@` `text` 形式等同於 `to_tsvector(x) @@ plainto_tsquery(y)`。

在 `tsquery` 中，`&`（AND）運算子表示它的兩個參數都必須出現在文件中才算相符。同樣地，`|`（OR）運算子表示至少必須出現一個參數，而 `!`（NOT）運算子則表示它的參數必須*不*出現才算相符。例如，查詢 `fat & ! rat` 會比對包含 `fat` 但不包含 `rat` 的文件。

搜尋片語可以借助 `<->`（FOLLOWED BY）`tsquery` 運算子來達成，它只有在其參數的相符項目彼此相鄰且依給定順序出現時才會相符。例如：

```

SELECT to_tsvector('fatal error') @@ to_tsquery('fatal <-> error');
 ?column?
----------
 t

SELECT to_tsvector('error is not fatal') @@ to_tsquery('fatal <-> error');
 ?column?
----------
 f
```

FOLLOWED BY 運算子還有一個更通用的版本，形式為 `<N>`，其中 *`N`* 是一個整數，代表相符詞素之間的位置差距。`<1>` 與 `<->` 相同，而 `<2>` 則允許相符項目之間恰好出現一個其他詞素，依此類推。`phraseto_tsquery` 函式會利用這個運算子建構 `tsquery`，讓它在某些單字是停用詞時，仍能比對多字的片語。例如：

```

SELECT phraseto_tsquery('cats ate rats');
       phraseto_tsquery
-------------------------------
 'cat' <-> 'ate' <-> 'rat'

SELECT phraseto_tsquery('the cats ate the rats');
       phraseto_tsquery
-------------------------------
 'cat' <-> 'ate' <2> 'rat'
```

有時很有用的一個特殊情況是，可以使用 `<0>` 要求兩個樣式比對到同一個單字。

可以使用括號來控制 `tsquery` 運算子的巢狀結構。沒有括號時，`|` 的結合力最弱，其次是 `&`，再來是 `<->`，而 `!` 的結合力最強。

值得注意的是，AND/OR/NOT 運算子出現在 FOLLOWED BY 運算子的參數中時，其意義與不在其中時略有不同，因為在 FOLLOWED BY 中，相符項目的確切位置很重要。例如，一般而言 `!x` 只會比對任何地方都不包含 `x` 的文件。但 `!x <-> y` 會比對不緊接在 `x` 之後的 `y`；文件中其他位置出現的 `x` 並不會阻止相符。另一個例子是，`x & y` 一般只要求 `x` 與 `y` 都出現在文件中的某處，但 `(x & y) <-> z` 則要求 `x` 與 `y` 在同一個位置相符，且緊接在 `z` 之前。因此，這個查詢的行為與 `x <-> z & y <-> z` 不同，後者會比對包含兩個獨立序列 `x z` 與 `y z` 的文件。（照目前的寫法，這個特定查詢是沒有用的，因為 `x` 與 `y` 不可能在同一個位置相符；但在更複雜的情況下，例如使用前綴比對樣式時，這種形式的查詢可能會有用。）

<a id="TEXTSEARCH-INTRO-CONFIGURATIONS"></a>

### 12.1.3. 設定 [#](#TEXTSEARCH-INTRO-CONFIGURATIONS)

以上都是簡單的文字搜尋範例。如前所述，全文檢索功能還能做到更多事情：略過特定單字（停用詞）不建立索引、處理同義詞，以及使用更精密的剖析方式，例如不只依空白字元來剖析。這些功能是由*文字搜尋設定*（text search configuration）控制的。PostgreSQL 內建了許多語言的預先定義設定，你也可以輕鬆建立自己的設定。（psql 的 `\dF` 指令會顯示所有可用的設定。）

安裝時會選擇適當的設定，並在 `postgresql.conf` 中相應地設定 [default_text_search_config](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG)。如果整個叢集都使用相同的文字搜尋設定，就可以使用 `postgresql.conf` 中的值。如果要在整個叢集中使用不同的設定，但在任何單一資料庫中都使用相同的設定，請使用 `ALTER DATABASE ... SET`。否則，你可以在每個工作階段中設定 `default_text_search_config`。

每個依賴設定的文字搜尋函式都有一個選用的 `regconfig` 參數，因此可以明確指定要使用的設定。只有在省略這個參數時，才會使用 `default_text_search_config`。

為了更容易建立自訂的文字搜尋設定，設定是由較簡單的資料庫物件組合而成的。PostgreSQL 的文字搜尋功能提供了四種與設定相關的資料庫物件：

* *文字搜尋剖析器*（text search parser）會將文件切分為語彙單元，並為每個語彙單元分類（例如分為單字或數字）。
* *文字搜尋字典*（text search dictionary）會將語彙單元轉換為正規化形式，並剔除停用詞。
* *文字搜尋範本*（text search template）提供字典底層的函式。（字典只是指定一個範本以及該範本的一組參數。）
* *文字搜尋設定*（text search configuration）會選擇一個剖析器，以及一組用來正規化剖析器所產生語彙單元的字典。

文字搜尋剖析器與範本是由低階的 C 函式建構而成的，因此開發新的剖析器或範本需要 C 程式設計能力，而將它們安裝到資料庫中則需要超級使用者權限。（PostgreSQL 發行版本的 `contrib/` 區域中有附加剖析器與範本的範例。）由於字典與設定只是將一些底層的剖析器與範本參數化並連接起來，建立新的字典或設定並不需要特殊權限。本章稍後會有建立自訂字典與設定的範例。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-intro.html)（原文版本：18.6；核對日期：2026-09-11）
