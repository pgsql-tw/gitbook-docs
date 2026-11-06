<a id="PGTRGM"></a>

## F.35. pg_trgm — 支援以三元組比對文字相似度 [#](#pgtrgm) <a href="#pgtrgm" id="pgtrgm"></a>

[F.35.1. 三元組（或三字圖）概念](pgtrgm.md#pgtrgm-concepts)

[F.35.2. 函式與運算子](pgtrgm/pgtrgm-funcs-ops.md#pgtrgm-funcs-ops)

[F.35.3. GUC 參數](pgtrgm.md#pgtrgm-guc)

[F.35.4. 索引支援](pgtrgm.md#pgtrgm-index)

[F.35.5. 文字檢索整合](pgtrgm.md#pgtrgm-text-search)

[F.35.6. 參考資料](pgtrgm.md#pgtrgm-references)

[F.35.7. 作者](pgtrgm.md#pgtrgm-authors)

<a id="id-1.11.7.45.2"></a>

`pg_trgm` 模組提供依據三元組（trigram）比對來判定英數文字相似度的函式與運算子，以及支援快速搜尋相似字串的索引運算子類別。

此模組被視為「受信任」，也就是可由在目前資料庫中具有 `CREATE` 權限的非超級使用者安裝。

<a id="PGTRGM-CONCEPTS"></a>

### F.35.1. 三元組（或三字圖）概念 [#](#pgtrgm-concepts) <a href="#pgtrgm-concepts" id="pgtrgm-concepts"></a>

三元組是從字串中取出的一組三個連續字元。我們可以計算兩個字串共有的三元組數量，藉此衡量它們的相似度。事實證明，這個簡單的想法在衡量許多自然語言中單字的相似度時非常有效。

### 注意

`pg_trgm` 從字串擷取三元組時，會忽略非單字字元（非英數字元）。在決定字串所含的三元組集合時，每個單字都視為前面加上兩個空格、後面加上一個空格。例如，字串“`cat`”的三元組集合為
“ `c`”、
“ `ca`”、
“`cat`”與
“`at` ”。
字串“`foo|bar`”的三元組集合為
“ `f`”、
“ `fo`”、
“`foo`”、
“`oo` ”、
“ `b`”、
“ `ba`”、
“`bar`”與
“`ar` ”。

### F.35.2. 函式與運算子 [#](#pgtrgm-funcs-ops) <a href="#pgtrgm-funcs-ops" id="pgtrgm-funcs-ops"></a>

完整內容請見 [F.35.2. 函式與運算子](pgtrgm/pgtrgm-funcs-ops.md#pgtrgm-funcs-ops)。

<a id="PGTRGM-GUC"></a>

### F.35.3. GUC 參數 [#](#pgtrgm-guc) <a href="#pgtrgm-guc" id="pgtrgm-guc"></a>

<a id="GUC-PGTRGM-SIMILARITY-THRESHOLD"></a>

`pg_trgm.similarity_threshold` (`real`) <a id="id-1.11.7.45.7.2.1.1.3"></a> [#](#GUC-PGTRGM-SIMILARITY-THRESHOLD)
:   設定 `%` 運算子目前使用的相似度門檻。門檻必須介於 0 與 1 之間（預設為 0.3）。
<a id="GUC-PGTRGM-WORD-SIMILARITY-THRESHOLD"></a>

`pg_trgm.word_similarity_threshold` (`real`) <a id="id-1.11.7.45.7.2.2.1.3"></a> [#](#GUC-PGTRGM-WORD-SIMILARITY-THRESHOLD)
:   設定 `<%` 與 `%>` 運算子目前使用的單字相似度門檻。門檻必須介於 0 與 1 之間（預設為 0.6）。
<a id="GUC-PGTRGM-STRICT-WORD-SIMILARITY-THRESHOLD"></a>

`pg_trgm.strict_word_similarity_threshold` (`real`) <a id="id-1.11.7.45.7.2.3.1.3"></a> [#](#GUC-PGTRGM-STRICT-WORD-SIMILARITY-THRESHOLD)
:   設定 `<<%` 與 `%>>` 運算子目前使用的嚴格單字相似度門檻。門檻必須介於 0 與 1 之間（預設為 0.5）。

<a id="PGTRGM-INDEX"></a>

### F.35.4. 索引支援 [#](#pgtrgm-index) <a href="#pgtrgm-index" id="pgtrgm-index"></a>

`pg_trgm` 模組提供 GiST 與 GIN 索引運算子類別，讓你可以在文字欄位上建立索引，以進行非常快速的相似度搜尋。這些索引類型支援上述的相似度運算子，此外也支援以三元組為基礎、用於 `LIKE`、`ILIKE`、`~`、`~*` 與 `=` 查詢的索引搜尋。在預設建置的 `pg_trgm` 中，相似度比較不區分大小寫。不支援不等式運算子。請注意，對於等值運算子，這些索引的效率可能不如一般的 B-tree 索引。

範例：

```

CREATE TABLE test_trgm (t text);
CREATE INDEX trgm_idx ON test_trgm USING GIST (t gist_trgm_ops);
```

或

```

CREATE INDEX trgm_idx ON test_trgm USING GIN (t gin_trgm_ops);
```

`gist_trgm_ops` GiST 運算子類別（opclass）將一組三元組近似表示為點陣圖簽章。其選用的整數參數 `siglen` 決定簽章長度（以位元組計）。預設長度為 12 位元組。簽章長度的有效值介於 1 至 2024 位元組之間。較長的簽章可帶來更精確的搜尋（掃描索引中較小的部分與較少的堆積頁面），代價是索引較大。

使用 32 位元組簽章長度建立此類索引的範例：

```

CREATE INDEX trgm_idx ON test_trgm USING GIST (t gist_trgm_ops(siglen=32));
```

此時，你就有了 `t` 欄位上的索引，可用於相似度搜尋。典型的查詢如下：

```

SELECT t, similarity(t, 'word') AS sml
  FROM test_trgm
  WHERE t % 'word'
  ORDER BY sml DESC, t;
```

這會傳回文字欄位中所有與 *`word`* 足夠相似的值，並依比對程度由最佳到最差排序。即使資料集非常大，也會使用索引讓此操作快速完成。

上述查詢的一種變形是：

```

SELECT t, t <-> 'word' AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

GiST 索引可以相當有效率地實作此查詢，但 GIN 索引不行。當只需要少數幾個最接近的比對結果時，它通常會勝過第一種寫法。

你也可以將 `t` 欄位上的索引用於單字相似度或嚴格單字相似度。典型的查詢如下：

```

SELECT t, word_similarity('word', t) AS sml
  FROM test_trgm
  WHERE 'word' <% t
  ORDER BY sml DESC, t;
```

以及

```

SELECT t, strict_word_similarity('word', t) AS sml
  FROM test_trgm
  WHERE 'word' <<% t
  ORDER BY sml DESC, t;
```

這會傳回文字欄位中所有符合下列條件的值：其對應的有序三元組集合中，存在與 *`word`* 的三元組集合足夠相似的連續範圍；結果依比對程度由最佳到最差排序。即使資料集非常大，也會使用索引讓此操作快速完成。

上述查詢可能的變形有：

```

SELECT t, 'word' <<-> t AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

以及

```

SELECT t, 'word' <<<-> t AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

GiST 索引可以相當有效率地實作此查詢，但 GIN 索引不行。

從 PostgreSQL 9.1 開始，這些索引類型也支援 `LIKE` 與 `ILIKE` 的索引搜尋，例如：

```

SELECT * FROM test_trgm WHERE t LIKE '%foo%bar';
```

索引搜尋的運作方式是從搜尋字串中擷取三元組，再到索引中查找這些三元組。搜尋字串中的三元組越多，索引搜尋就越有效。與以 B-tree 為基礎的搜尋不同，搜尋字串不需要左錨定（left-anchored）。

從 PostgreSQL 9.3 開始，這些索引類型也支援正規表示式比對（`~` 與 `~*` 運算子）的索引搜尋，例如：

```

SELECT * FROM test_trgm WHERE t ~ '(foo|bar)';
```

索引搜尋的運作方式是從正規表示式中擷取三元組，再到索引中查找這些三元組。能從正規表示式中擷取出的三元組越多，索引搜尋就越有效。與以 B-tree 為基礎的搜尋不同，搜尋字串不需要左錨定。

不論是 `LIKE` 還是正規表示式搜尋，都請記住：無法從中擷取出任何三元組的模式，會退化為完整索引掃描。

要選擇 GiST 還是 GIN 索引，取決於 GiST 與 GIN 的相對效能特性，這部分在其他地方另有討論。

<a id="PGTRGM-TEXT-SEARCH"></a>

### F.35.5. 文字檢索整合 [#](#pgtrgm-text-search) <a href="#pgtrgm-text-search" id="pgtrgm-text-search"></a>

三元組比對與全文索引搭配使用時，是非常有用的工具。特別是，它可以幫助辨識拼錯的輸入單字，這些單字無法由全文檢索機制直接比對到。

第一步是產生一個輔助資料表，其中包含文件中所有不重複的單字：

```

CREATE TABLE words AS SELECT word FROM
        ts_stat('SELECT to_tsvector(''simple'', bodytext) FROM documents');
```

其中 `documents` 是一個資料表，含有我們想要搜尋的文字欄位 `bodytext`。之所以對 `to_tsvector` 函式使用 `simple` 設定，而不使用特定語言的設定，是因為我們想要取得原始（未經詞幹處理）單字的清單。

接著，在單字欄位上建立三元組索引：

```

CREATE INDEX words_idx ON words USING GIN (word gin_trgm_ops);
```

現在，就可以使用類似前一個範例的 `SELECT` 查詢，為使用者搜尋詞中拼錯的單字建議正確拼法。一個有用的額外檢查，是要求選出的單字長度也與拼錯的單字相近。

### 注意

由於 `words` 資料表是以獨立的靜態資料表產生，因此需要定期重新產生，才能與文件集合保持相當程度的同步。通常不需要讓它保持完全即時。

<a id="PGTRGM-REFERENCES"></a>

### F.35.6. 參考資料 [#](#pgtrgm-references) <a href="#pgtrgm-references" id="pgtrgm-references"></a>

GiST 開發網站
<http://www.sai.msu.su/~megera/postgres/gist/>

Tsearch2 開發網站
<http://www.sai.msu.su/~megera/postgres/gist/tsearch/V2/>

<a id="PGTRGM-AUTHORS"></a>

### F.35.7. 作者 [#](#pgtrgm-authors) <a href="#pgtrgm-authors" id="pgtrgm-authors"></a>

Oleg Bartunov `<oleg@sai.msu.su>`，莫斯科，Moscow University，俄羅斯

Teodor Sigaev `<teodor@sigaev.ru>`，莫斯科，Delta-Soft Ltd.，俄羅斯

Alexander Korotkov `<a.korotkov@postgrespro.ru>`，莫斯科，Postgres Professional，俄羅斯

文件：Christopher Kings-Lynne

本模組由 Delta-Soft Ltd.（俄羅斯莫斯科）贊助。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgtrgm.html)（原文版本：18.6；核對日期：2026-10-23）
