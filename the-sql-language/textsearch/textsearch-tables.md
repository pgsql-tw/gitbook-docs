<a id="TEXTSEARCH-TABLES"></a>

## 12.2. 資料表與索引 [#](#TEXTSEARCH-TABLES)

[12.2.1. 搜尋資料表](textsearch-tables.md#TEXTSEARCH-TABLES-SEARCH)

[12.2.2. 建立索引](textsearch-tables.md#TEXTSEARCH-TABLES-INDEX)

前一節的範例是以簡單的常數字串說明全文比對。本節說明如何搜尋資料表中的資料，並可選擇使用索引。

<a id="TEXTSEARCH-TABLES-SEARCH"></a>

### 12.2.1. 搜尋資料表 [#](#TEXTSEARCH-TABLES-SEARCH)

不使用索引也可以進行全文檢索。以下是一個簡單的查詢，會印出 `body` 欄位中包含單字 `friend` 的每一筆資料列的 `title`：

```

SELECT title
FROM pgweb
WHERE to_tsvector('english', body) @@ to_tsquery('english', 'friend');
```

這也會找到相關的單字，例如 `friends` 與 `friendly`，因為它們都會被簡化為相同的正規化詞素。

上面的查詢指定要使用 `english` 設定來剖析與正規化字串。我們也可以省略設定參數：

```

SELECT title
FROM pgweb
WHERE to_tsvector(body) @@ to_tsquery('friend');
```

這個查詢會使用 [default_text_search_config](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) 所設定的設定。

一個比較複雜的例子，是選出 `title` 或 `body` 中包含 `create` 與 `table` 的十份最新文件：

```

SELECT title
FROM pgweb
WHERE to_tsvector(title || ' ' || body) @@ to_tsquery('create & table')
ORDER BY last_mod_date DESC
LIMIT 10;
```

為了清楚起見，我們省略了 `coalesce` 函式呼叫；如果要找出兩個欄位之一包含 `NULL` 的資料列，就會需要它們。

雖然這些查詢不使用索引也能運作，但大多數應用程式會發現這種做法太慢，也許只有偶爾進行的臨時搜尋例外。實際運用文字搜尋時，通常需要建立索引。

<a id="TEXTSEARCH-TABLES-INDEX"></a>

### 12.2.2. 建立索引 [#](#TEXTSEARCH-TABLES-INDEX)

我們可以建立 GIN 索引（[第 12.9 節](textsearch-indexes.md)）來加速文字搜尋：

```

CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector('english', body));
```

請注意這裡使用的是兩個參數版本的 `to_tsvector`。只有指定了設定名稱的文字搜尋函式，才能用在運算式索引（[第 11.7 節](../indexes/indexes-expressional.md)）中。這是因為索引內容必須不受 [default_text_search_config](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) 影響。如果會受到影響，索引內容就可能不一致，因為不同的項目可能包含以不同文字搜尋設定建立的 `tsvector`，而且無從判斷哪個項目是哪個設定建立的。這樣的索引也不可能被正確地傾印與還原。

由於上面的索引使用的是兩個參數版本的 `to_tsvector`，只有使用相同設定名稱之兩個參數版本 `to_tsvector` 的查詢參照，才會使用該索引。也就是說，`WHERE
to_tsvector('english', body) @@ 'a & b'` 可以使用該索引，
但 `WHERE to_tsvector(body) @@ 'a & b'` 則不行。這可確保索引只會在與建立索引項目時相同的設定下使用。

也可以設定更複雜的運算式索引，由另一個欄位指定設定名稱，例如：

```

CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector(config_name, body));
```

其中 `config_name` 是 `pgweb` 資料表中的一個欄位。這讓同一個索引中可以混合使用不同的設定，同時記錄每個索引項目所使用的設定。例如，如果文件集合中包含不同語言的文件，這就會很有用。同樣地，要使用該索引的查詢也必須寫成相符的形式，例如 `WHERE to_tsvector(config_name, body) @@ 'a & b'`。

索引甚至可以串接多個欄位：

```

CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector('english', title || ' ' || body));
```

另一種做法是建立一個獨立的 `tsvector` 欄位來保存 `to_tsvector` 的輸出。若要讓這個欄位隨來源資料自動保持最新，請使用儲存式產生欄位（stored generated column）。這個範例串接了 `title` 與 `body`，並使用 `coalesce` 確保在其中一個欄位為 `NULL` 時，另一個欄位仍會被建立索引：

```

ALTER TABLE pgweb
    ADD COLUMN textsearchable_index_col tsvector
               GENERATED ALWAYS AS (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))) STORED;
```

接著我們建立一個 GIN 索引來加速搜尋：

```

CREATE INDEX textsearch_idx ON pgweb USING GIN (textsearchable_index_col);
```

現在我們就可以進行快速的全文檢索了：

```

SELECT title
FROM pgweb
WHERE textsearchable_index_col @@ to_tsquery('create & table')
ORDER BY last_mod_date DESC
LIMIT 10;
```

與運算式索引相比，獨立欄位做法的一個優點是，不需要在查詢中明確指定文字搜尋設定就能使用索引。如上例所示，查詢可以依賴 `default_text_search_config`。另一個優點是搜尋會比較快，因為不需要重新呼叫 `to_tsvector` 來驗證索引相符的結果。（這在使用 GiST 索引時比使用 GIN 索引時更重要；請參閱[第 12.9 節](textsearch-indexes.md)。）不過，運算式索引的做法設定起來比較簡單，而且由於沒有明確儲存 `tsvector` 表示法，所需的磁碟空間也比較少。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-tables.html)（原文版本：18.6；核對日期：2026-09-11）
