<a id="TEXTSEARCH-FEATURES"></a>

## 12.4. 其他功能 [#](#TEXTSEARCH-FEATURES)

[12.4.1. 操作文件](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSVECTOR)

[12.4.2. 操作查詢](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSQUERY)

[12.4.3. 自動更新用的觸發程序](textsearch-features.md#TEXTSEARCH-UPDATE-TRIGGERS)

[12.4.4. 收集文件統計資訊](textsearch-features.md#TEXTSEARCH-STATISTICS)

本節說明在文字搜尋中很有用的其他函式與運算子。

<a id="TEXTSEARCH-MANIPULATE-TSVECTOR"></a>

### 12.4.1. 操作文件 [#](#TEXTSEARCH-MANIPULATE-TSVECTOR)

[第 12.3.1 節](textsearch-controls.md#TEXTSEARCH-PARSING-DOCUMENTS)說明了如何將原始的文字文件轉換為 `tsvector` 值。PostgreSQL 也提供了一些函式與運算子，可用來操作已經是 `tsvector` 形式的文件。

<a id="id-1.5.11.7.3.3.1.1.1"></a> `tsvector || tsvector`
:   `tsvector` 串接運算子會回傳一個向量，合併作為參數的兩個向量的詞素與位置資訊。串接時會保留位置與權重標籤。右側向量中出現的位置，會加上左側向量中最大的位置作為位移，因此結果幾乎等同於將兩份原始文件字串串接後再執行 `to_tsvector` 的結果。（這種等價並不完全精確，因為從左側參數結尾移除的停用詞不會影響結果；但如果使用文字串接，這些停用詞就會影響右側參數中詞素的位置。）

    以向量形式串接，而不是在套用 `to_tsvector` 之前先串接文字，其中一個優點是可以使用不同的設定來剖析文件的不同部分。此外，由於 `setweight` 函式會以相同方式標記給定向量中的所有詞素，如果你想以不同的權重標記文件的不同部分，就必須在串接之前先剖析文字並執行 `setweight`。

<a id="id-1.5.11.7.3.3.2.1.1"></a> `setweight(vector tsvector, weight "char") returns tsvector`
:   `setweight` 會回傳輸入向量的副本，其中每個位置都已標記為給定的 *`weight`*，也就是 `A`、`B`、`C` 或 `D` 之一。（`D` 是新向量的預設值，因此不會在輸出中顯示。）串接向量時會保留這些標籤，讓排名函式可以對來自文件不同部分的單字給予不同的權重。

    請注意，權重標籤是套用在*位置*上，而不是*詞素*上。如果輸入向量已經移除了位置資訊，`setweight` 就不會有任何作用。

<a id="id-1.5.11.7.3.3.3.1.1"></a> `length(vector tsvector) returns integer`
:   回傳向量中儲存的詞素數量。

<a id="id-1.5.11.7.3.3.4.1.1"></a> `strip(vector tsvector) returns tsvector`
:   回傳一個向量，列出與給定向量相同的詞素，但不含任何位置或權重資訊。結果通常比未移除位置資訊的向量小很多，但用處也比較少。對已移除位置資訊的向量進行相關性排名，效果不如未移除的向量。此外，`<->`（FOLLOWED BY）`tsquery` 運算子永遠不會比對已移除位置資訊的輸入，因為它無法判定詞素出現位置之間的距離。

`tsvector` 相關函式的完整清單請參閱[表 9.43](../functions/functions-textsearch.md#TEXTSEARCH-FUNCTIONS-TABLE)。

<a id="TEXTSEARCH-MANIPULATE-TSQUERY"></a>

### 12.4.2. 操作查詢 [#](#TEXTSEARCH-MANIPULATE-TSQUERY)

[第 12.3.2 節](textsearch-controls.md#TEXTSEARCH-PARSING-QUERIES)說明了如何將原始的文字查詢轉換為 `tsquery` 值。PostgreSQL 也提供了一些函式與運算子，可用來操作已經是 `tsquery` 形式的查詢。

`tsquery && tsquery`
:   回傳兩個給定查詢的 AND 組合。

`tsquery || tsquery`
:   回傳兩個給定查詢的 OR 組合。

`!! tsquery`
:   回傳給定查詢的否定（NOT）。

`tsquery <-> tsquery`
:   回傳一個查詢，使用 `<->`（FOLLOWED BY）`tsquery` 運算子，搜尋第一個給定查詢的相符項目後面緊接著第二個給定查詢的相符項目。例如：

```

    SELECT to_tsquery('fat') <-> to_tsquery('cat | rat');
              ?column?
    ----------------------------
     'fat' <-> ( 'cat' | 'rat' )
    ```

<a id="id-1.5.11.7.4.3.5.1.1"></a> `tsquery_phrase(query1 tsquery, query2 tsquery [, distance integer ]) returns tsquery`
:   回傳一個查詢，使用 `<N>` `tsquery` 運算子，搜尋第一個給定查詢的相符項目後面、恰好相距 *`distance`* 個詞素處出現第二個給定查詢的相符項目。例如：

```

    SELECT tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10);
      tsquery_phrase
    ------------------
     'fat' <10> 'cat'
    ```

<a id="id-1.5.11.7.4.3.6.1.1"></a> `numnode(query tsquery) returns integer`
:   回傳 `tsquery` 中的節點數量（詞素加上運算子）。這個函式可用來判斷 *`query`* 是否有意義（回傳值 > 0），或是只包含停用詞（回傳 0）。範例：

```

    SELECT numnode(plainto_tsquery('the any'));
    NOTICE:  query contains only stopword(s) or doesn't contain lexeme(s), ignored
     numnode
    ---------
           0

    SELECT numnode('foo & bar'::tsquery);
     numnode
    ---------
           3
    ```

<a id="id-1.5.11.7.4.3.7.1.1"></a> `querytree(query tsquery) returns text`
:   回傳 `tsquery` 中可用於搜尋索引的部分。這個函式可用來偵測無法使用索引的查詢，例如只包含停用詞或只包含否定詞的查詢。例如：

```

    SELECT querytree(to_tsquery('defined'));
     querytree
    -----------
     'defin'

    SELECT querytree(to_tsquery('!defined'));
     querytree
    -----------
     T
    ```

<a id="TEXTSEARCH-QUERY-REWRITING"></a>

#### 12.4.2.1. 查詢改寫 [#](#TEXTSEARCH-QUERY-REWRITING)

<a id="id-1.5.11.7.4.4.2"></a>

`ts_rewrite` 系列函式會在給定的 `tsquery` 中搜尋目標子查詢出現的位置，並將每次出現的位置替換為替代子查詢。本質上，這項運算就是 `tsquery` 專用的子字串替換。目標與替代的組合可以視為一條*查詢改寫規則*（query rewrite rule）。這類改寫規則的集合可以成為強大的搜尋輔助工具。例如，你可以使用同義詞擴大搜尋範圍（例如 `new york`、`big apple`、`nyc`、`gotham`），或縮小搜尋範圍，將使用者引導到某個熱門主題。這項功能與同義詞庫字典（[第 12.6.4 節](textsearch-dictionaries.md#TEXTSEARCH-THESAURUS)）在功能上有些重疊。不過，你可以隨時修改一組改寫規則而不需要重建索引，而更新同義詞庫則需要重建索引才會生效。

`ts_rewrite (query tsquery, target tsquery, substitute tsquery) returns tsquery`
:   這種形式的 `ts_rewrite` 只會套用單一條改寫規則：只要 *`query`* 中出現 *`target`*，就將它替換為 *`substitute`*。例如：

```

    SELECT ts_rewrite('a & b'::tsquery, 'a'::tsquery, 'c'::tsquery);
     ts_rewrite
    ------------
     'b' & 'c'
    ```

`ts_rewrite (query tsquery, select text) returns tsquery`
:   這種形式的 `ts_rewrite` 接受一個起始的 *`query`*，以及一個以文字字串給定的 SQL *`select`* 指令。*`select`* 必須產生兩個 `tsquery` 型別的欄位。對於 *`select`* 結果的每一筆資料列，會在目前的 *`query`* 值中，將第一個欄位的值（目標）替換為第二個欄位的值（替代）。例如：

```

    CREATE TABLE aliases (t tsquery PRIMARY KEY, s tsquery);
    INSERT INTO aliases VALUES('a', 'c');

    SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM aliases');
     ts_rewrite
    ------------
     'b' & 'c'
    ```

    請注意，以這種方式套用多條改寫規則時，套用的順序可能很重要；因此實務上你會希望來源查詢依某個排序鍵進行 `ORDER BY`。

我們來看一個真實的天文學範例。我們將使用由資料表驅動的改寫規則來擴充查詢 `supernovae`：

```

CREATE TABLE aliases (t tsquery primary key, s tsquery);
INSERT INTO aliases VALUES(to_tsquery('supernovae'), to_tsquery('supernovae|sn'));

SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT * FROM aliases');
           ts_rewrite
---------------------------------
 'crab' & ( 'supernova' | 'sn' )
```

只要更新資料表，就能改變改寫規則：

```

UPDATE aliases
SET s = to_tsquery('supernovae|sn & !nebulae')
WHERE t = to_tsquery('supernovae');

SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT * FROM aliases');
                 ts_rewrite
---------------------------------------------
 'crab' & ( 'supernova' | 'sn' & !'nebula' )
```

當改寫規則很多時，改寫可能會很慢，因為它會檢查每一條規則是否可能相符。為了過濾掉明顯不可能相符的規則，我們可以使用 `tsquery` 型別的包含運算子。在下面的範例中，我們只選出可能與原始查詢相符的規則：

```

SELECT ts_rewrite('a & b'::tsquery,
                  'SELECT t,s FROM aliases WHERE ''a & b''::tsquery @> t');
 ts_rewrite
------------
 'b' & 'c'
```

<a id="TEXTSEARCH-UPDATE-TRIGGERS"></a>

### 12.4.3. 自動更新用的觸發程序 [#](#TEXTSEARCH-UPDATE-TRIGGERS)

<a id="id-1.5.11.7.5.2"></a>

### 注意

本節所述的方法，已經被[第 12.2.2 節](textsearch-tables.md#TEXTSEARCH-TABLES-INDEX)所述的儲存式產生欄位取代。

使用獨立欄位來儲存文件的 `tsvector` 表示法時，必須建立一個觸發程序，在文件內容欄位變更時更新 `tsvector` 欄位。系統為此提供了兩個內建的觸發程序函式，你也可以自行撰寫。

```

tsvector_update_trigger(tsvector_column_name,​ config_name, text_column_name [, ... ])
tsvector_update_trigger_column(tsvector_column_name,​ config_column_name, text_column_name [, ... ])
```

這些觸發程序函式會在 `CREATE TRIGGER` 指令所指定參數的控制下，自動從一個或多個文字欄位計算出 `tsvector` 欄位。以下是它們的使用範例：

```

CREATE TABLE messages (
    title       text,
    body        text,
    tsv         tsvector
);

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON messages FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(tsv, 'pg_catalog.english', title, body);

INSERT INTO messages VALUES('title here', 'the body text is here');

SELECT * FROM messages;
   title    |         body          |            tsv
------------+-----------------------+----------------------------
 title here | the body text is here | 'bodi':4 'text':5 'titl':1

SELECT title, body FROM messages WHERE tsv @@ to_tsquery('title & body');
   title    |         body
------------+-----------------------
 title here | the body text is here
```

建立這個觸發程序之後，`title` 或 `body` 的任何變更都會自動反映到 `tsv` 中，應用程式不必再為此操心。

觸發程序的第一個參數必須是要更新的 `tsvector` 欄位名稱。第二個參數指定用來執行轉換的文字搜尋設定。對於 `tsvector_update_trigger`，設定名稱就直接作為觸發程序的第二個參數給定。它必須如上所示以 schema 限定，這樣觸發程序的行為才不會隨 `search_path` 的變更而改變。對於 `tsvector_update_trigger_column`，觸發程序的第二個參數是另一個資料表欄位的名稱，該欄位必須是 `regconfig` 型別。這讓每一筆資料列都可以選擇各自的設定。其餘的參數是文字欄位（`text`、`varchar` 或 `char` 型別）的名稱。這些欄位會依給定的順序納入文件中。NULL 值會被略過（但其他欄位仍然會被建立索引）。

這些內建觸發程序的一個限制是，它們會以相同方式處理所有輸入欄位。如果要以不同方式處理欄位（例如，讓標題與內文有不同的權重），就必須撰寫自訂的觸發程序。以下是使用 PL/pgSQL 作為觸發程序語言的範例：

```

CREATE FUNCTION messages_trigger() RETURNS trigger AS $$
begin
  new.tsv :=
     setweight(to_tsvector('pg_catalog.english', coalesce(new.title,'')), 'A') ||
     setweight(to_tsvector('pg_catalog.english', coalesce(new.body,'')), 'D');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON messages FOR EACH ROW EXECUTE FUNCTION messages_trigger();
```

請記住，在觸發程序中建立 `tsvector` 值時，明確指定設定名稱是很重要的，這樣欄位的內容才不會受到 `default_text_search_config` 變更的影響。若沒有這樣做，很可能會導致問題，例如在傾印與還原之後搜尋結果改變。

<a id="TEXTSEARCH-STATISTICS"></a>

### 12.4.4. 收集文件統計資訊 [#](#TEXTSEARCH-STATISTICS)

<a id="id-1.5.11.7.6.2"></a>

`ts_stat` 函式可用來檢查你的設定，以及找出停用詞的候選。

```

ts_stat(sqlquery text, [ weights text, ]
        OUT word text, OUT ndoc integer,
        OUT nentry integer) returns setof record
```

*`sqlquery`* 是一個包含 SQL 查詢的文字值，該查詢必須回傳單一個 `tsvector` 欄位。`ts_stat` 會執行該查詢，並回傳 `tsvector` 資料中每個不同詞素（單字）的統計資訊。回傳的欄位有

* *`word`* `text`：詞素的值
* *`ndoc`* `integer`：該單字出現過的文件（`tsvector`）數量
* *`nentry`* `integer`：該單字出現的總次數

如果提供了 *`weights`*，就只會計算具有其中某個權重的出現次數。

例如，要找出文件集合中出現頻率最高的十個單字：

```

SELECT * FROM ts_stat('SELECT vector FROM apod')
ORDER BY nentry DESC, ndoc DESC, word
LIMIT 10;
```

同樣的查詢，但只計算權重為 `A` 或 `B` 的單字出現次數：

```

SELECT * FROM ts_stat('SELECT vector FROM apod', 'ab')
ORDER BY nentry DESC, ndoc DESC, word
LIMIT 10;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-features.html)（原文版本：18.6；核對日期：2026-09-11）
