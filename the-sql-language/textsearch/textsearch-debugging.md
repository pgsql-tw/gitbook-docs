<a id="TEXTSEARCH-DEBUGGING"></a>

## 12.8. 測試與除錯文字搜尋 [#](#TEXTSEARCH-DEBUGGING)

[12.8.1. 設定測試](textsearch-debugging.md#TEXTSEARCH-CONFIGURATION-TESTING)

[12.8.2. 剖析器測試](textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING)

[12.8.3. 字典測試](textsearch-debugging.md#TEXTSEARCH-DICTIONARY-TESTING)

自訂文字搜尋設定的行為很容易變得令人困惑。本節所述的函式可用來測試文字搜尋物件。你可以測試完整的設定，也可以分別測試剖析器與字典。

<a id="TEXTSEARCH-CONFIGURATION-TESTING"></a>

### 12.8.1. 設定測試 [#](#TEXTSEARCH-CONFIGURATION-TESTING)

`ts_debug` 函式可以讓你輕鬆測試文字搜尋設定。

<a id="id-1.5.11.11.3.3"></a>

```

ts_debug([ config regconfig, ] document text,
         OUT alias text,
         OUT description text,
         OUT token text,
         OUT dictionaries regdictionary[],
         OUT dictionary regdictionary,
         OUT lexemes text[])
         returns setof record
```

`ts_debug` 會顯示 *`document`* 中每個語彙單元的資訊，這些語彙單元由剖析器產生，並經過所設定的字典處理。它會使用 *`config`* 所指定的設定；如果省略該參數，則使用 `default_text_search_config`。

`ts_debug` 會為剖析器在文字中識別出的每個語彙單元回傳一筆資料列。回傳的欄位有

* *`alias`* `text`：語彙單元類型的簡稱
* *`description`* `text`：語彙單元類型的說明
* *`token`* `text`：語彙單元的文字
* *`dictionaries`* `regdictionary[]`：設定為此語彙單元類型所選定的字典
* *`dictionary`* `regdictionary`：辨識出該語彙單元的字典；如果沒有任何字典辨識出來，則為 `NULL`
* *`lexemes`* `text[]`：辨識出該語彙單元的字典所產生的詞素；如果沒有任何字典辨識出來，則為 `NULL`；空陣列（`{}`）表示它被辨識為停用詞

以下是一個簡單的範例：

```

SELECT * FROM ts_debug('english', 'a fat  cat sat on a mat - it ate a fat rats');
   alias   |   description   | token |  dictionaries  |  dictionary  | lexemes
-----------+-----------------+-------+----------------+--------------+---------
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | fat   | {english_stem} | english_stem | {fat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | cat   | {english_stem} | english_stem | {cat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | sat   | {english_stem} | english_stem | {sat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | on    | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | mat   | {english_stem} | english_stem | {mat}
 blank     | Space symbols   |       | {}             |              |
 blank     | Space symbols   | -     | {}             |              |
 asciiword | Word, all ASCII | it    | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | ate   | {english_stem} | english_stem | {ate}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | fat   | {english_stem} | english_stem | {fat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | rats  | {english_stem} | english_stem | {rat}
```

為了進行更完整的示範，我們先為英文建立一個 `public.english` 設定與 Ispell 字典：

```

CREATE TEXT SEARCH CONFIGURATION public.english ( COPY = pg_catalog.english );

CREATE TEXT SEARCH DICTIONARY english_ispell (
    TEMPLATE = ispell,
    DictFile = english,
    AffFile = english,
    StopWords = english
);

ALTER TEXT SEARCH CONFIGURATION public.english
   ALTER MAPPING FOR asciiword WITH english_ispell, english_stem;
```

```

SELECT * FROM ts_debug('public.english', 'The Brightest supernovaes');
   alias   |   description   |    token    |         dictionaries          |   dictionary   |   lexemes
-----------+-----------------+-------------+-------------------------------+----------------+-------------
 asciiword | Word, all ASCII | The         | {english_ispell,english_stem} | english_ispell | {}
 blank     | Space symbols   |             | {}                            |                |
 asciiword | Word, all ASCII | Brightest   | {english_ispell,english_stem} | english_ispell | {bright}
 blank     | Space symbols   |             | {}                            |                |
 asciiword | Word, all ASCII | supernovaes | {english_ispell,english_stem} | english_stem   | {supernova}
```

在這個範例中，剖析器將單字 `Brightest` 辨識為 `ASCII word`（別名 `asciiword`）。這個語彙單元類型的字典清單是 `english_ispell` 與 `english_stem`。這個單字被 `english_ispell` 辨識出來，並被簡化為名詞 `bright`。單字 `supernovaes` 對 `english_ispell` 字典而言是未知的，因此它被傳給下一個字典，而且幸運地被辨識出來（事實上，`english_stem` 是一個能辨識所有內容的 Snowball 字典；這就是它被放在字典清單最後的原因）。

單字 `The` 被 `english_ispell` 字典辨識為停用詞（[第 12.6.1 節](textsearch-dictionaries.md#TEXTSEARCH-STOPWORDS)），因此不會被建立索引。空白也會被捨棄，因為設定完全沒有為它們提供任何字典。

你可以明確指定想要查看的欄位，以縮減輸出的寬度：

```

SELECT alias, token, dictionary, lexemes
FROM ts_debug('public.english', 'The Brightest supernovaes');
   alias   |    token    |   dictionary   |   lexemes
-----------+-------------+----------------+-------------
 asciiword | The         | english_ispell | {}
 blank     |             |                |
 asciiword | Brightest   | english_ispell | {bright}
 blank     |             |                |
 asciiword | supernovaes | english_stem   | {supernova}
```

<a id="TEXTSEARCH-PARSER-TESTING"></a>

### 12.8.2. 剖析器測試 [#](#TEXTSEARCH-PARSER-TESTING)

下列函式可以直接測試文字搜尋剖析器。

<a id="id-1.5.11.11.4.3"></a>

```

ts_parse(parser_name text, document text,
         OUT tokid integer, OUT token text) returns setof record
ts_parse(parser_oid oid, document text,
         OUT tokid integer, OUT token text) returns setof record
```

`ts_parse` 會剖析給定的 *`document`*，並回傳一系列紀錄，剖析所產生的每個語彙單元各對應一筆。每筆紀錄都包含一個 `tokid`，表示所指派的語彙單元類型，以及一個 `token`，也就是該語彙單元的文字。例如：

```

SELECT * FROM ts_parse('default', '123 - a number');
 tokid | token
-------+--------
    22 | 123
    12 |
    12 | -
     1 | a
    12 |
     1 | number
```

<a id="id-1.5.11.11.4.6"></a>

```

ts_token_type(parser_name text, OUT tokid integer,
              OUT alias text, OUT description text) returns setof record
ts_token_type(parser_oid oid, OUT tokid integer,
              OUT alias text, OUT description text) returns setof record
```

`ts_token_type` 會回傳一個資料表，描述指定的剖析器能夠辨識的每一種語彙單元類型。對於每一種語彙單元類型，這個資料表會提供剖析器用來標記該類型語彙單元的整數 `tokid`、在設定指令中用來稱呼該語彙單元類型的 `alias`，以及一段簡短的 `description`。例如：

```

SELECT * FROM ts_token_type('default');
 tokid |      alias      |               description
-------+-----------------+------------------------------------------
     1 | asciiword       | Word, all ASCII
     2 | word            | Word, all letters
     3 | numword         | Word, letters and digits
     4 | email           | Email address
     5 | url             | URL
     6 | host            | Host
     7 | sfloat          | Scientific notation
     8 | version         | Version number
     9 | hword_numpart   | Hyphenated word part, letters and digits
    10 | hword_part      | Hyphenated word part, all letters
    11 | hword_asciipart | Hyphenated word part, all ASCII
    12 | blank           | Space symbols
    13 | tag             | XML tag
    14 | protocol        | Protocol head
    15 | numhword        | Hyphenated word, letters and digits
    16 | asciihword      | Hyphenated word, all ASCII
    17 | hword           | Hyphenated word, all letters
    18 | url_path        | URL path
    19 | file            | File or path name
    20 | float           | Decimal notation
    21 | int             | Signed integer
    22 | uint            | Unsigned integer
    23 | entity          | XML entity
```

<a id="TEXTSEARCH-DICTIONARY-TESTING"></a>

### 12.8.3. 字典測試 [#](#TEXTSEARCH-DICTIONARY-TESTING)

`ts_lexize` 函式可以協助測試字典。

<a id="id-1.5.11.11.5.3"></a>

```

ts_lexize(dict regdictionary, token text) returns text[]
```

如果字典認得輸入的 *`token`*，`ts_lexize` 會回傳詞素陣列；如果字典認得該語彙單元但它是停用詞，則回傳空陣列；如果是未知的單字，則回傳 `NULL`。

範例：

```

SELECT ts_lexize('english_stem', 'stars');
 ts_lexize
-----------
 {star}

SELECT ts_lexize('english_stem', 'a');
 ts_lexize
-----------
 {}
```

### 注意

`ts_lexize` 函式預期的是單一個*語彙單元*，而不是文字。以下是一個可能造成混淆的例子：

```

SELECT ts_lexize('thesaurus_astro', 'supernovae stars') is null;
 ?column?
----------
 t
```

同義詞庫字典 `thesaurus_astro` 確實認得片語 `supernovae stars`，但 `ts_lexize` 會失敗，因為它不會剖析輸入文字，而是將它視為單一語彙單元。請使用 `plainto_tsquery` 或 `to_tsvector` 來測試同義詞庫字典，例如：

```

SELECT plainto_tsquery('supernovae stars');
 plainto_tsquery
-----------------
 'sn'
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-debugging.html)（原文版本：18.6；核對日期：2026-09-11）
