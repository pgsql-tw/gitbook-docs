<a id="UNACCENT"></a>

## F.48. unaccent — 移除變音符號的文字搜尋字典 [#](#unaccent) <a href="#unaccent" id="unaccent"></a>

[F.48.1. 設定](unaccent.md#UNACCENT-CONFIGURATION)

[F.48.2. 用法](unaccent.md#UNACCENT-USAGE)

[F.48.3. 函式](unaccent.md#UNACCENT-FUNCTIONS)

<a id="id-1.11.7.58.2"></a>

`unaccent` 是一種文字搜尋字典，會從詞素中移除重音符號（變音符號）。它是一種過濾字典，也就是說，與字典的一般行為不同，它的輸出一律會傳給下一個字典（若有的話）。這使全文檢索得以進行不區分重音符號的處理。

目前的 `unaccent` 實作無法作為 `thesaurus` 字典的正規化字典使用。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="UNACCENT-CONFIGURATION"></a>

### F.48.1. 設定 [#](#UNACCENT-CONFIGURATION)

`unaccent` 字典接受下列選項：

* `RULES` 是包含轉換規則清單之檔案的基本名稱。此檔案必須存放在 `$SHAREDIR/tsearch_data/`（其中 `$SHAREDIR` 表示 PostgreSQL 安裝的共用資料目錄）。其名稱必須以 `.rules` 結尾（此結尾不應包含在 `RULES` 參數中）。

規則檔的格式如下：

* 每一行代表一條轉換規則，由一個帶重音符號的字元與其後一個不帶重音符號的字元組成。前者會被轉換為後者。例如：

  ```

  À        A
  Á        A
  Â        A
  Ã        A
  Ä        A
  Å        A
  Æ        AE
  ```

  兩個字元之間必須以空白分隔，且一行開頭或結尾的任何空白都會被忽略。
* 或者，若一行只給定一個字元，該字元的所有出現處都會被刪除；這在以獨立字元表示重音符號的語言中很有用。
* 事實上，每個「字元」都可以是任何不含空白的字串，因此除了移除變音符號之外，`unaccent` 字典也可以用於其他種類的子字串替換。
* 有些字元（例如數字符號）的轉換規則可能需要空白。此時可以在轉換後的字元前後加上雙引號。若要在轉換後的字元中包含雙引號，該雙引號必須以第二個雙引號跳脫。例如：

  ```

  ¼      " 1/4"
  ½      " 1/2"
  ¾      " 3/4"
  “       """"
  ”       """"
  ```
* 與其他 PostgreSQL 文字搜尋設定檔一樣，規則檔必須以 UTF-8 編碼儲存。載入時，資料會自動轉換為目前資料庫的編碼。任何含有無法轉換之字元的行都會被靜默忽略，因此規則檔可以包含不適用於目前編碼的規則。

更完整的範例可在 `unaccent.rules` 中找到，它可直接用於大多數歐洲語言，並會在安裝 `unaccent` 模組時安裝於 `$SHAREDIR/tsearch_data/`。此規則檔會將帶重音符號的字元轉換為不帶重音符號的相同字元，也會將連字展開為等效的一串簡單字元（例如將 Æ 展開為 AE）。

<a id="UNACCENT-USAGE"></a>

### F.48.2. 用法 [#](#UNACCENT-USAGE)

安裝 `unaccent` 擴充功能時，會建立文字搜尋範本 `unaccent`，以及以它為基礎的字典 `unaccent`。`unaccent` 字典的預設參數設定為 `RULES='unaccent'`，因此可立即搭配標準的 `unaccent.rules` 檔案使用。若有需要，你可以修改此參數，例如

```

mydb=# ALTER TEXT SEARCH DICTIONARY unaccent (RULES='my_rules');
```

或是以此範本為基礎建立新的字典。

若要測試此字典，可以試試：

```

mydb=# select ts_lexize('unaccent','Hôtel');
 ts_lexize
-----------
 {Hotel}
(1 row)
```

以下範例說明如何將 `unaccent` 字典加入文字搜尋設定：

```

mydb=# CREATE TEXT SEARCH CONFIGURATION fr ( COPY = french );
mydb=# ALTER TEXT SEARCH CONFIGURATION fr
        ALTER MAPPING FOR hword, hword_part, word
        WITH unaccent, french_stem;
mydb=# select to_tsvector('fr','Hôtels de la Mer');
    to_tsvector
-------------------
 'hotel':1 'mer':4
(1 row)

mydb=# select to_tsvector('fr','Hôtel de la Mer') @@ to_tsquery('fr','Hotels');
 ?column?
----------
 t
(1 row)

mydb=# select ts_headline('fr','Hôtel de la Mer',to_tsquery('fr','Hotels'));
      ts_headline
------------------------
 <b>Hôtel</b> de la Mer
(1 row)
```

<a id="UNACCENT-FUNCTIONS"></a>

### F.48.3. 函式 [#](#UNACCENT-FUNCTIONS)

`unaccent()` 函式會從給定的字串中移除重音符號（變音符號）。基本上，它是 `unaccent` 型字典的包裝函式，但可以在一般的文字搜尋情境之外使用。

<a id="id-1.11.7.58.8.3"></a>

```

unaccent([dictionary regdictionary, ] string text) returns text
```

若省略 *`dictionary`* 引數，則會使用名為 `unaccent`、且與 `unaccent()` 函式本身位於同一綱要中的文字搜尋字典。

例如：

```

SELECT unaccent('unaccent', 'Hôtel');
SELECT unaccent('Hôtel');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/unaccent.html)（原文版本：18.6；核對日期：2026-10-22）
