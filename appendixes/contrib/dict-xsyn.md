## F.13. `dict_xsyn` — 同義詞全文檢索字典範例 [#](#DICT-XSYN)

[F.13.1. 設定](dict-xsyn.md#DICT-XSYN-CONFIG)

[F.13.2. 使用方式](dict-xsyn.md#DICT-XSYN-USAGE)

<a id="id-1.11.7.23.2"></a>

`dict_xsyn`（Extended Synonym Dictionary）是全文檢索附加字典範本的範例。此字典型別會以同義詞群組取代詞彙，因此可使用任一同義詞搜尋該詞彙。

<a id="DICT-XSYN-CONFIG"></a>

### F.13.1. 設定 [#](#DICT-XSYN-CONFIG)

`dict_xsyn` 字典接受下列選項：

* `matchorig` 控制字典是否接受原始詞彙。預設值為 `true`。
* `matchsynonyms` 控制字典是否接受同義詞。預設值為 `false`。
* `keeporig` 控制字典輸出是否包含原始詞彙。預設值為 `true`。
* `keepsynonyms` 控制字典輸出是否包含同義詞。預設值為 `true`。
* `rules` 是包含同義詞清單之檔案的基底名稱。此檔案必須存放於 `$SHAREDIR/tsearch_data/`（其中 `$SHAREDIR` 是 PostgreSQL 安裝的共享資料目錄）。檔名必須以 `.rules` 結尾（但不得將此副檔名包含在 `rules` 參數中）。

規則檔案具有下列格式：

* 每一行代表一個詞彙的同義詞群組，該詞彙位於行首。同義詞以空白字元分隔，如下：

  ```

  word syn1 syn2 syn3
  ```
* 井字號（`#`）是註解分隔符，可出現在行中的任何位置。該行其餘內容會被略過。

請參考安裝於 `$SHAREDIR/tsearch_data/` 的 `xsyn_sample.rules` 範例。

<a id="DICT-XSYN-USAGE"></a>

### F.13.2. 使用方式 [#](#DICT-XSYN-USAGE)

安裝 `dict_xsyn` 擴充功能會以預設參數建立全文檢索範本 `xsyn_template` 與基於該範本的字典 `xsyn`。你可以變更這些參數，例如：

```

mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=false);
ALTER TEXT SEARCH DICTIONARY
```

也可以基於該範本建立新的字典。

若要測試此字典，可以嘗試：

```

mydb=# SELECT ts_lexize('xsyn', 'word');
      ts_lexize
-----------------------
 {syn1,syn2,syn3}

mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=true);
ALTER TEXT SEARCH DICTIONARY

mydb=# SELECT ts_lexize('xsyn', 'word');
      ts_lexize
-----------------------
 {word,syn1,syn2,syn3}

mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=false, MATCHSYNONYMS=true);
ALTER TEXT SEARCH DICTIONARY

mydb=# SELECT ts_lexize('xsyn', 'syn1');
      ts_lexize
-----------------------
 {syn1,syn2,syn3}

mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=true, MATCHORIG=false, KEEPSYNONYMS=false);
ALTER TEXT SEARCH DICTIONARY

mydb=# SELECT ts_lexize('xsyn', 'syn1');
      ts_lexize
-----------------------
 {word}
```

實際使用時，會如[第 12 章](../../the-sql-language/textsearch/README.md)所述，將它納入全文檢索設定。範例如下：

```

ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR word, asciiword WITH xsyn, english_stem;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dict-xsyn.html)（原文版本：18.6；核對日期：2026-09-06）
