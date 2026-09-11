<a id="TEXTSEARCH-CONTROLS"></a>

## 12.3. 控制文字搜尋 [#](#TEXTSEARCH-CONTROLS)

[12.3.1. 剖析文件](textsearch-controls.md#TEXTSEARCH-PARSING-DOCUMENTS)

[12.3.2. 剖析查詢](textsearch-controls.md#TEXTSEARCH-PARSING-QUERIES)

[12.3.3. 搜尋結果排名](textsearch-controls.md#TEXTSEARCH-RANKING)

[12.3.4. 標示搜尋結果](textsearch-controls.md#TEXTSEARCH-HEADLINE)

要實作全文檢索，必須有一個函式能從文件建立 `tsvector`，並從使用者的查詢建立 `tsquery`。此外，我們需要以有用的順序回傳結果，因此需要一個函式來依文件與查詢的相關程度比較文件。能夠將結果美觀地呈現出來也很重要。PostgreSQL 對上述所有功能都提供了支援。

<a id="TEXTSEARCH-PARSING-DOCUMENTS"></a>

### 12.3.1. 剖析文件 [#](#TEXTSEARCH-PARSING-DOCUMENTS)

PostgreSQL 提供了 `to_tsvector` 函式，可將文件轉換為 `tsvector` 資料型別。

<a id="id-1.5.11.6.3.3"></a>

```

to_tsvector([ config regconfig, ] document text) returns tsvector
```

`to_tsvector` 會將文字文件剖析為語彙單元，將語彙單元簡化為詞素，並回傳一個 `tsvector`，列出這些詞素及其在文件中的位置。文件會依指定的或預設的文字搜尋設定處理。以下是一個簡單的範例：

```

SELECT to_tsvector('english', 'a fat  cat sat on a mat - it ate a fat rats');
                  to_tsvector
-----------------------------------------------------
 'ate':9 'cat':3 'fat':2,11 'mat':7 'rat':12 'sat':4
```

在上面的範例中，我們可以看到產生的 `tsvector` 並不包含單字 `a`、`on` 或 `it`，單字 `rats` 變成了 `rat`，而標點符號 `-` 則被忽略。

`to_tsvector` 函式在內部會呼叫一個剖析器，將文件文字切分為語彙單元，並為每個語彙單元指派一種類型。對每個語彙單元，會查詢一份字典清單（[第 12.6 節](textsearch-dictionaries.md)），而這份清單會依語彙單元類型而有所不同。第一個*辨識出*該語彙單元的字典，會產生一個或多個正規化的*詞素*來代表該語彙單元。例如，`rats` 之所以變成 `rat`，是因為其中一個字典辨識出單字 `rats` 是 `rat` 的複數形式。有些單字會被辨識為*停用詞*（[第 12.6.1 節](textsearch-dictionaries.md#TEXTSEARCH-STOPWORDS)），因為它們出現得太頻繁，對搜尋沒有用處，所以會被忽略。在我們的範例中，這些單字是 `a`、`on` 與 `it`。如果清單中沒有任何字典辨識出該語彙單元，它也會被忽略。在這個範例中，標點符號 `-` 就是如此，因為實際上並沒有為它的語彙單元類型（`Space symbols`）指派任何字典，這表示空白類的語彙單元永遠不會被建立索引。剖析器、字典，以及要為哪些類型的語彙單元建立索引，都是由所選的文字搜尋設定（[第 12.7 節](textsearch-configuration.md)）決定的。同一個資料庫中可以有許多不同的設定，而且各種語言都有預先定義的設定可用。在我們的範例中，使用的是英文的預設設定 `english`。

`setweight` 函式可以用給定的*權重*（weight）標記 `tsvector` 的項目，權重是字母 `A`、`B`、`C` 或 `D` 之一。這通常用來標記來自文件不同部分的項目，例如標題與內文。之後，這項資訊可以用於搜尋結果的排名。

由於 `to_tsvector`(`NULL`) 會回傳 `NULL`，因此只要欄位可能為 null，就建議使用 `coalesce`。以下是從結構化文件建立 `tsvector` 的建議方法：

```

UPDATE tt SET ti =
    setweight(to_tsvector(coalesce(title,'')), 'A')    ||
    setweight(to_tsvector(coalesce(keyword,'')), 'B')  ||
    setweight(to_tsvector(coalesce(abstract,'')), 'C') ||
    setweight(to_tsvector(coalesce(body,'')), 'D');
```

這裡我們使用 `setweight` 標記完成的 `tsvector` 中每個詞素的來源，然後使用 `tsvector` 串接運算子 `||` 合併這些已標記的 `tsvector` 值。（[第 12.4.1 節](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSVECTOR)會詳細說明這些運算。）

<a id="TEXTSEARCH-PARSING-QUERIES"></a>

### 12.3.2. 剖析查詢 [#](#TEXTSEARCH-PARSING-QUERIES)

PostgreSQL 提供了 `to_tsquery`、`plainto_tsquery`、`phraseto_tsquery` 與 `websearch_to_tsquery` 函式，可將查詢轉換為 `tsquery` 資料型別。`to_tsquery` 比 `plainto_tsquery` 或 `phraseto_tsquery` 提供更多功能，但對輸入的要求也比較嚴格。`websearch_to_tsquery` 是 `to_tsquery` 的簡化版本，採用另一種類似網頁搜尋引擎所使用的語法。

<a id="id-1.5.11.6.4.3"></a>

```

to_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`to_tsquery` 會從 *`querytext`* 建立 `tsquery` 值，其內容必須由單一語彙單元組成，並以 `tsquery` 運算子 `&`（AND）、`|`（OR）、`!`（NOT）與 `<->`（FOLLOWED BY）分隔，也可以用括號分組。換句話說，`to_tsquery` 的輸入必須已經遵循[第 8.11.2 節](../datatype/datatype-textsearch.md#DATATYPE-TSQUERY)所述的 `tsquery` 輸入一般規則。差別在於，基本的 `tsquery` 輸入會按字面接受語彙單元，而 `to_tsquery` 則會使用指定的或預設的設定將每個語彙單元正規化為詞素，並依該設定捨棄屬於停用詞的語彙單元。例如：

```

SELECT to_tsquery('english', 'The & Fat & Rats');
  to_tsquery
---------------
 'fat' & 'rat'
```

和基本的 `tsquery` 輸入一樣，可以為每個詞素附加權重，限制它只比對具有這些權重的 `tsvector` 詞素。例如：

```

SELECT to_tsquery('english', 'Fat | Rats:AB');
    to_tsquery
------------------
 'fat' | 'rat':AB
```

此外，也可以在詞素後附加 `*` 來指定前綴比對：

```

SELECT to_tsquery('supern:*A & star:A*B');
        to_tsquery
--------------------------
 'supern':*A & 'star':*AB
```

這樣的詞素會比對 `tsvector` 中任何以給定字串開頭的單字。

`to_tsquery` 也可以接受以單引號括住的片語。這主要在設定中包含可能由這類片語觸發的同義詞庫字典時有用。在下面的範例中，同義詞庫包含規則 `supernovae
stars : sn`：

```

SELECT to_tsquery('''supernovae stars'' & !crab');
  to_tsquery
---------------
 'sn' & !'crab'
```

如果沒有引號，`to_tsquery` 對於沒有以 AND、OR 或 FOLLOWED BY 運算子分隔的語彙單元，會產生語法錯誤。

<a id="id-1.5.11.6.4.7"></a>

```

plainto_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`plainto_tsquery` 會將未格式化的文字 *`querytext`* 轉換為 `tsquery` 值。文字的剖析與正規化方式與 `to_tsvector` 大致相同，然後在保留下來的單字之間插入 `&`（AND）`tsquery` 運算子。

範例：

```

SELECT plainto_tsquery('english', 'The Fat Rats');
 plainto_tsquery
-----------------
 'fat' & 'rat'
```

請注意，`plainto_tsquery` 不會辨識輸入中的 `tsquery` 運算子、權重標籤或前綴比對標籤：

```

SELECT plainto_tsquery('english', 'The Fat & Rats:C');
   plainto_tsquery
---------------------
 'fat' & 'rat' & 'c'
```

這裡所有輸入的標點符號都被捨棄了。

<a id="id-1.5.11.6.4.11"></a>

```

phraseto_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`phraseto_tsquery` 的行為與 `plainto_tsquery` 大致相同，差別在於它會在保留下來的單字之間插入 `<->`（FOLLOWED BY）運算子，而不是 `&`（AND）運算子。此外，停用詞並不是單純被捨棄，而是以插入 `<N>` 運算子（而非 `<->` 運算子）的方式納入考量。這個函式在搜尋確切的詞素序列時很有用，因為 FOLLOWED BY 運算子檢查的是詞素的順序，而不只是所有詞素是否都存在。

範例：

```

SELECT phraseto_tsquery('english', 'The Fat Rats');
 phraseto_tsquery
------------------
 'fat' <-> 'rat'
```

和 `plainto_tsquery` 一樣，`phraseto_tsquery` 函式不會辨識輸入中的 `tsquery` 運算子、權重標籤或前綴比對標籤：

```

SELECT phraseto_tsquery('english', 'The Fat & Rats:C');
      phraseto_tsquery
-----------------------------
 'fat' <-> 'rat' <-> 'c'
```

```

websearch_to_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`websearch_to_tsquery` 會使用另一種語法，從 *`querytext`* 建立 `tsquery` 值；在這種語法中，簡單的未格式化文字就是有效的查詢。與 `plainto_tsquery` 和 `phraseto_tsquery` 不同，它也會辨識某些運算子。此外，這個函式永遠不會產生語法錯誤，因此可以直接使用使用者提供的原始輸入進行搜尋。支援下列語法：

* `unquoted text`：不在引號內的文字，會被轉換為以 `&` 運算子分隔的搜尋詞，如同經過 `plainto_tsquery` 處理。
* `"quoted text"`：引號內的文字，會被轉換為以 `<->` 運算子分隔的搜尋詞，如同經過 `phraseto_tsquery` 處理。
* `OR`：單字「or」會被轉換為 `|` 運算子。
* `-`：破折號會被轉換為 `!` 運算子。

其他標點符號會被忽略。因此，和 `plainto_tsquery` 與 `phraseto_tsquery` 一樣，`websearch_to_tsquery` 函式不會辨識輸入中的 `tsquery` 運算子、權重標籤或前綴比對標籤。

範例：

```

SELECT websearch_to_tsquery('english', 'The fat rats');
 websearch_to_tsquery
----------------------
 'fat' & 'rat'
(1 row)

SELECT websearch_to_tsquery('english', '"supernovae stars" -crab');
       websearch_to_tsquery
----------------------------------
 'supernova' <-> 'star' & !'crab'
(1 row)

SELECT websearch_to_tsquery('english', '"sad cat" or "fat rat"');
       websearch_to_tsquery
-----------------------------------
 'sad' <-> 'cat' | 'fat' <-> 'rat'
(1 row)

SELECT websearch_to_tsquery('english', 'signal -"segmentation fault"');
         websearch_to_tsquery
---------------------------------------
 'signal' & !( 'segment' <-> 'fault' )
(1 row)

SELECT websearch_to_tsquery('english', '""" )( dummy \\ query <->');
 websearch_to_tsquery
----------------------
 'dummi' & 'queri'
(1 row)
```

<a id="TEXTSEARCH-RANKING"></a>

### 12.3.3. 搜尋結果排名 [#](#TEXTSEARCH-RANKING)

排名嘗試衡量文件與特定查詢的相關程度，以便在相符項目很多時，先顯示最相關的項目。PostgreSQL 提供了兩個預先定義的排名函式，它們會考量詞彙、鄰近度與結構資訊；也就是說，它們會考量查詢詞在文件中出現的頻率、這些詞在文件中彼此的距離，以及它們所出現之文件部分的重要性。不過，相關性的概念很模糊，而且與應用高度相關。不同的應用可能需要額外的資訊來排名，例如文件的修改時間。內建的排名函式只是範例。你可以撰寫自己的排名函式，或將它們的結果與其他因素結合，以符合特定的需求。

目前可用的兩個排名函式是：

<a id="id-1.5.11.6.5.3.1.1.1.1"></a> `ts_rank([ weights float4[], ] vector tsvector, query tsquery [, normalization integer ]) returns float4`
:   依據相符詞素的出現頻率為向量排名。

<a id="id-1.5.11.6.5.3.1.2.1.1"></a> `ts_rank_cd([ weights float4[], ] vector tsvector, query tsquery [, normalization integer ]) returns float4`
:   這個函式會為給定的文件向量與查詢計算*覆蓋密度*（cover density）排名，其方法見 Clarke、Cormack 與 Tudhope 於 1999 年發表在期刊「Information Processing and Management」上的「Relevance Ranking for One to Three Term Queries」。覆蓋密度與 `ts_rank` 排名類似，差別在於它會考量相符詞素彼此之間的鄰近程度。

    這個函式需要詞素的位置資訊才能進行計算。因此，它會忽略 `tsvector` 中任何已「移除位置資訊」（stripped）的詞素。如果輸入中沒有保留位置資訊的詞素，結果將為零。（關於 `strip` 函式與 `tsvector` 中的位置資訊，詳情請參閱[第 12.4.1 節](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSVECTOR)。）

對這兩個函式而言，選用的 *`weights`* 參數可以依單字的標記方式，加重或減輕單字出現次數的權重。權重陣列依下列順序指定各類單字的權重：

```

{D-weight, C-weight, B-weight, A-weight}
```

如果沒有提供 *`weights`*，就會使用下列預設值：

```

{0.1, 0.2, 0.4, 1.0}
```

權重通常用來標記來自文件特殊區域的單字，例如標題或開頭的摘要，讓它們與文件內文中的單字相比，受到較高或較低的重視。

由於較長的文件包含查詢詞的機會較大，將文件大小納入考量是合理的；例如，一份一百字的文件中出現五次搜尋詞，很可能比一份一千字的文件中出現五次更相關。兩個排名函式都接受一個整數 *`normalization`* 選項，指定文件長度是否以及如何影響其排名。這個整數選項控制多種行為，因此它是一個位元遮罩：你可以使用 `|` 指定一種或多種行為（例如 `2|4`）。

* 0（預設值）忽略文件長度
* 1 將排名除以 1 加上文件長度的對數
* 2 將排名除以文件長度
* 4 將排名除以各範圍（extent）之間的平均調和距離（只有 `ts_rank_cd` 實作了這一項）
* 8 將排名除以文件中不重複單字的數量
* 16 將排名除以 1 加上文件中不重複單字數量的對數
* 32 將排名除以其自身加 1

如果指定了多個旗標位元，轉換會依上列順序套用。

請務必注意，排名函式不會使用任何全域資訊，因此不可能產生有時會希望得到的、正規化到 1% 或 100% 的公平結果。可以套用正規化選項 32（`rank/(rank+1)`），將所有排名縮放到零到一的範圍內，但這當然只是外觀上的改變，並不會影響搜尋結果的順序。

以下範例只選出排名最高的十個相符項目：

```

SELECT title, ts_rank_cd(textsearch, query) AS rank
FROM apod, to_tsquery('neutrino|(dark & matter)') query
WHERE query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |   rank
-----------------------------------------------+----------
 Neutrinos in the Sun                          |      3.1
 The Sudbury Neutrino Detector                 |      2.4
 A MACHO View of Galactic Dark Matter          |  2.01317
 Hot Gas and Dark Matter                       |  1.91171
 The Virgo Cluster: Hot Plasma and Dark Matter |  1.90953
 Rafting for Solar Neutrinos                   |      1.9
 NGC 4650A: Strange Galaxy and Dark Matter     |  1.85774
 Hot Gas and Dark Matter                       |   1.6123
 Ice Fishing for Cosmic Neutrinos              |      1.6
 Weak Lensing Distorts the Universe            | 0.818218
```

以下是使用正規化排名的相同範例：

```

SELECT title, ts_rank_cd(textsearch, query, 32 /* rank/(rank+1) */ ) AS rank
FROM apod, to_tsquery('neutrino|(dark & matter)') query
WHERE  query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |        rank
-----------------------------------------------+-------------------
 Neutrinos in the Sun                          | 0.756097569485493
 The Sudbury Neutrino Detector                 | 0.705882361190954
 A MACHO View of Galactic Dark Matter          | 0.668123210574724
 Hot Gas and Dark Matter                       |  0.65655958650282
 The Virgo Cluster: Hot Plasma and Dark Matter | 0.656301290640973
 Rafting for Solar Neutrinos                   | 0.655172410958162
 NGC 4650A: Strange Galaxy and Dark Matter     | 0.650072921219637
 Hot Gas and Dark Matter                       | 0.617195790024749
 Ice Fishing for Cosmic Neutrinos              | 0.615384618911517
 Weak Lensing Distorts the Universe            | 0.450010798361481
```

排名的成本可能很高，因為它需要查詢每一份相符文件的 `tsvector`，這可能受限於 I/O 而變得緩慢。遺憾的是，這幾乎無法避免，因為實際的查詢往往會產生大量相符項目。

<a id="TEXTSEARCH-HEADLINE"></a>

### 12.3.4. 標示搜尋結果 [#](#TEXTSEARCH-HEADLINE)

呈現搜尋結果時，理想的做法是顯示每份文件的一部分，以及它與查詢的關聯。搜尋引擎通常會顯示文件的片段，並標示出搜尋詞。PostgreSQL 提供了 `ts_headline` 函式來實作這項功能。

<a id="id-1.5.11.6.6.3"></a>

```

ts_headline([ config regconfig, ] document text, query tsquery [, options text ]) returns text
```

`ts_headline` 接受一份文件與一個查詢，並回傳文件的摘錄，其中查詢中的詞會被標示出來。具體而言，這個函式會使用查詢選出相關的文字片段，然後標示所有出現在查詢中的單字，即使這些單字的位置不符合查詢的限制也一樣。用來剖析文件的設定可以由 *`config`* 指定；如果省略 *`config`*，就會使用 `default_text_search_config` 設定。

如果指定了 *`options`* 字串，它必須由一個或多個以逗號分隔的 *`option`*`=`*`value`* 配對組成。可用的選項有：

* `MaxWords`、`MinWords`（整數）：這兩個數字決定輸出摘要的最長與最短長度。預設值分別是 35 與 15。
* `ShortWord`（整數）：長度小於或等於這個值的單字，如果不是查詢詞，會在摘要的開頭與結尾被捨棄。預設值 3 可以排除常見的英文冠詞。
* `HighlightAll`（布林值）：如果為 `true`，會將整份文件當作摘要，並忽略前面三個參數。預設值是 `false`。
* `MaxFragments`（整數）：要顯示的文字片段數量上限。預設值 0 會選用不以片段為基礎的摘要產生方式。大於零的值會選用以片段為基礎的摘要產生方式（見下文）。
* `StartSel`、`StopSel`（字串）：用來界定文件中出現之查詢單字的字串，以便將它們與其他摘錄的單字區分開來。預設值是「`<b>`」與「`</b>`」，適用於 HTML 輸出（但請參閱下方的警告）。
* `FragmentDelimiter`（字串）：顯示多個片段時，片段之間會以這個字串分隔。預設值是「 `...` 」。

### 警告：跨網站指令碼（XSS）安全性

`ts_headline` 的輸出並不保證可以安全地直接放入網頁中。當 `HighlightAll` 為 `false`（預設值）時，會從文件中移除一些簡單的 XML 標籤，但並不保證能移除所有 HTML 標記。因此，在處理不受信任的輸入時，這並不能有效防禦跨網站指令碼（XSS）等攻擊。要防範這類攻擊，應該從輸入文件中移除所有 HTML 標記，或是對輸出使用 HTML 清理工具（sanitizer）。

這些選項名稱不區分大小寫。如果字串值包含空白或逗號，就必須以雙引號括住。

在不以片段為基礎的摘要產生方式中，`ts_headline` 會找出與給定 *`query`* 相符的項目，並選出其中一個來顯示，優先選擇在允許的摘要長度內包含較多查詢單字的相符項目。在以片段為基礎的摘要產生方式中，`ts_headline` 會找出查詢的相符項目，並將每個相符項目切分為每段不超過 `MaxWords` 個單字的「片段」，優先選擇包含較多查詢單字的片段，並在可能時「延伸」片段以納入周圍的單字。因此，當查詢的相符項目橫跨文件的大範圍區段，或希望顯示多個相符項目時，以片段為基礎的模式會比較有用。無論是哪一種模式，如果找不到任何查詢相符項目，都會顯示由文件前 `MinWords` 個單字組成的單一片段。

例如：

```

SELECT ts_headline('english',
  'The most common type of search
is to find all documents containing given query terms
and return them in order of their similarity to the
query.',
  to_tsquery('english', 'query & similarity'));
                        ts_headline
------------------------------------------------------------
 containing given <b>query</b> terms                       +
 and return them in order of their <b>similarity</b> to the+
 <b>query</b>.

SELECT ts_headline('english',
  'Search terms may occur
many times in a document,
requiring ranking of the search matches to decide which
occurrences to display in the result.',
  to_tsquery('english', 'search & term'),
  'MaxFragments=10, MaxWords=7, MinWords=3, StartSel=<<, StopSel=>>');
                        ts_headline
------------------------------------------------------------
 <<Search>> <<terms>> may occur                            +
 many times ... ranking of the <<search>> matches to decide
```

`ts_headline` 使用的是原始文件，而不是 `tsvector` 摘要，因此它可能會很慢，應謹慎使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-controls.html)（原文版本：18.6；核對日期：2026-09-11）
