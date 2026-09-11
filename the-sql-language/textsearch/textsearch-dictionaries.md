<a id="TEXTSEARCH-DICTIONARIES"></a>

## 12.6. 字典 [#](#TEXTSEARCH-DICTIONARIES)

[12.6.1. 停用詞](textsearch-dictionaries.md#TEXTSEARCH-STOPWORDS)

[12.6.2. Simple 字典](textsearch-dictionaries.md#TEXTSEARCH-SIMPLE-DICTIONARY)

[12.6.3. 同義詞字典](textsearch-dictionaries.md#TEXTSEARCH-SYNONYM-DICTIONARY)

[12.6.4. 同義詞庫字典](textsearch-dictionaries.md#TEXTSEARCH-THESAURUS)

[12.6.5. Ispell 字典](textsearch-dictionaries.md#TEXTSEARCH-ISPELL-DICTIONARY)

[12.6.6. Snowball 字典](textsearch-dictionaries.md#TEXTSEARCH-SNOWBALL-DICTIONARY)

字典用來剔除在搜尋中不應考慮的單字（*停用詞*），並將單字*正規化*，讓同一個單字的不同衍生形式能夠相符。成功正規化的單字稱為*詞素*（lexeme）。除了提升搜尋品質之外，正規化與移除停用詞也能縮小文件的 `tsvector` 表示法，進而提升效能。正規化並不一定具有語言學上的意義，通常取決於應用的語意。

以下是一些正規化的範例：

* 語言學上的：Ispell 字典會嘗試將輸入的單字簡化為正規化形式；詞幹字典則會移除字尾
* 可以將 URL 位置標準化，讓等價的 URL 能夠相符：

  * http://www.pgsql.ru/db/mw/index.html
  * http://www.pgsql.ru/db/mw/
  * http://www.pgsql.ru/db/../db/mw/index.html
* 可以將顏色名稱替換為其十六進位值，例如 `red, green, blue, magenta -> FF0000, 00FF00, 0000FF, FF00FF`
* 如果要為數字建立索引，可以移除部分小數位數以縮小可能數值的範圍；例如，如果只保留小數點後兩位，*3.14*159265359、*3.14*15926 與 *3.14* 在正規化之後就會相同。

字典是一個程式，它接受一個語彙單元作為輸入，並回傳：

* 如果字典認得該輸入語彙單元，就回傳詞素陣列（請注意，一個語彙單元可以產生多個詞素）
* 設定了 `TSL_FILTER` 旗標的單一詞素，用來以新的語彙單元取代原本的語彙單元，並傳給後續的字典（執行此動作的字典稱為*過濾字典*，filtering dictionary）
* 如果字典認得該語彙單元，但它是停用詞，就回傳空陣列
* 如果字典無法辨識該輸入語彙單元，就回傳 `NULL`

PostgreSQL 為許多語言提供了預先定義的字典。另外也有數個預先定義的範本，可用來以自訂參數建立新的字典。以下會說明每一個預先定義的字典範本。如果沒有合適的現有範本，也可以建立新的範本；範例請參閱 PostgreSQL 發行版本的 `contrib/` 區域。

文字搜尋設定會將一個剖析器與一組字典綁定在一起，用來處理剖析器輸出的語彙單元。對於剖析器可能回傳的每一種語彙單元類型，設定都會指定一份獨立的字典清單。當剖析器找到該類型的語彙單元時，會依序查詢清單中的每一個字典，直到有某個字典將它辨識為已知單字為止。如果它被認定為停用詞，或者沒有任何字典辨識出該語彙單元，它就會被捨棄，不會被建立索引，也不會被搜尋。一般而言，第一個回傳非 `NULL` 輸出的字典會決定結果，其餘的字典都不會被查詢；但過濾字典可以將給定的單字替換為修改過的單字，再傳給後續的字典。

設定字典清單的一般原則是：最先放置範圍最窄、最特定的字典，接著放較通用的字典，最後以非常通用的字典作結，例如能辨識所有內容的 Snowball 詞幹處理器或 `simple`。例如，針對天文學專用的搜尋（`astro_en` 設定），可以將語彙單元類型 `asciiword`（ASCII 單字）綁定到天文學術語的同義詞字典、一般的英文字典，以及 Snowball 英文詞幹處理器：

```

ALTER TEXT SEARCH CONFIGURATION astro_en
    ADD MAPPING FOR asciiword WITH astrosyn, english_ispell, english_stem;
```

過濾字典可以放在清單中的任何位置，只是放在最後會沒有用處。過濾字典可用來將單字部分正規化，以簡化後續字典的工作。例如，過濾字典可以用來移除帶重音字母上的重音符號，就像 [unaccent](../../appendixes/contrib/unaccent.md) 模組所做的那樣。

<a id="TEXTSEARCH-STOPWORDS"></a>

### 12.6.1. 停用詞 [#](#TEXTSEARCH-STOPWORDS)

停用詞是非常常見、幾乎出現在每一份文件中，而且沒有辨別價值的單字。因此，在全文檢索的情境下可以忽略它們。例如，每一篇英文文字都包含 `a` 與 `the` 這類單字，因此將它們儲存在索引中是沒有用的。不過，停用詞確實會影響 `tsvector` 中的位置，進而影響排名：

```

SELECT to_tsvector('english', 'in the list of stop words');
        to_tsvector
----------------------------
 'list':3 'stop':5 'word':6
```

缺少的位置 1、2、4 是因為停用詞的關係。包含與不包含停用詞的文件，計算出的排名差異相當大：

```

SELECT ts_rank_cd (to_tsvector('english', 'in the list of stop words'), to_tsquery('list & stop'));
 ts_rank_cd
------------
       0.05

SELECT ts_rank_cd (to_tsvector('english', 'list stop words'), to_tsquery('list & stop'));
 ts_rank_cd
------------
        0.1
```

如何處理停用詞取決於個別的字典。例如，`ispell` 字典會先將單字正規化，再查看停用詞清單；而 `Snowball` 詞幹處理器則會先檢查停用詞清單。行為不同的原因是為了減少雜訊。

<a id="TEXTSEARCH-SIMPLE-DICTIONARY"></a>

### 12.6.2. Simple 字典 [#](#TEXTSEARCH-SIMPLE-DICTIONARY)

`simple` 字典範本的運作方式，是將輸入的語彙單元轉為小寫，並與停用詞檔案比對。如果在檔案中找到，就回傳空陣列，使該語彙單元被捨棄。如果沒有找到，就回傳該單字的小寫形式作為正規化的詞素。另外，也可以將字典設定為把非停用詞回報為無法辨識，讓它們傳給清單中的下一個字典。

以下是使用 `simple` 範本定義字典的範例：

```

CREATE TEXT SEARCH DICTIONARY public.simple_dict (
    TEMPLATE = pg_catalog.simple,
    STOPWORDS = english
);
```

這裡的 `english` 是停用詞檔案的基本名稱。該檔案的完整名稱是 `$SHAREDIR/tsearch_data/english.stop`，其中 `$SHAREDIR` 代表 PostgreSQL 安裝的共用資料目錄，通常是 `/usr/local/share/postgresql`（如果不確定，可以使用 `pg_config
--sharedir` 查詢）。
檔案格式就只是一份單字清單，每行一個單字。空白行與行尾空白會被忽略，大寫會轉為小寫，但除此之外不會對檔案內容做任何其他處理。

現在我們可以測試這個字典：

```

SELECT ts_lexize('public.simple_dict', 'YeS');
 ts_lexize
-----------
 {yes}

SELECT ts_lexize('public.simple_dict', 'The');
 ts_lexize
-----------
 {}
```

我們也可以選擇在停用詞檔案中找不到該單字時回傳 `NULL`，而不是小寫形式的單字。只要將字典的 `Accept` 參數設為 `false`，就能選擇這種行為。延續上面的範例：

```

ALTER TEXT SEARCH DICTIONARY public.simple_dict ( Accept = false );

SELECT ts_lexize('public.simple_dict', 'YeS');
 ts_lexize
-----------


SELECT ts_lexize('public.simple_dict', 'The');
 ts_lexize
-----------
 {}
```

在預設設定 `Accept` = `true` 之下，只有將 `simple` 字典放在字典清單的最後才有用，因為它永遠不會將任何語彙單元傳給後續的字典。反過來說，只有在後面至少還有一個字典時，`Accept` = `false` 才有用。

### 警示

大多數類型的字典都依賴設定檔，例如停用詞檔案。這些檔案*必須*以 UTF-8 編碼儲存。如果資料庫的實際編碼不同，這些檔案在被讀入伺服器時會轉換為資料庫的實際編碼。

### 警示

一般而言，資料庫工作階段只會在工作階段中第一次使用字典時，讀取一次字典的設定檔。如果你修改了設定檔，並想強制既有的工作階段載入新的內容，請對該字典執行 `ALTER TEXT SEARCH DICTIONARY` 指令。這可以是一個實際上不改變任何參數值的「虛擬」更新。

<a id="TEXTSEARCH-SYNONYM-DICTIONARY"></a>

### 12.6.3. 同義詞字典 [#](#TEXTSEARCH-SYNONYM-DICTIONARY)

這個字典範本用來建立以同義詞取代單字的字典。它不支援片語（片語請使用同義詞庫範本（[第 12.6.4 節](textsearch-dictionaries.md#TEXTSEARCH-THESAURUS)））。同義詞字典可以用來克服語言學上的問題，例如防止英文詞幹字典將單字「Paris」簡化為「pari」。只要在同義詞字典中加入一行 `Paris paris`，並將它放在 `english_stem` 字典之前即可。例如：

```

SELECT * FROM ts_debug('english', 'Paris');
   alias   |   description   | token |  dictionaries  |  dictionary  | lexemes
-----------+-----------------+-------+----------------+--------------+---------
 asciiword | Word, all ASCII | Paris | {english_stem} | english_stem | {pari}

CREATE TEXT SEARCH DICTIONARY my_synonym (
    TEMPLATE = synonym,
    SYNONYMS = my_synonyms
);

ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR asciiword
    WITH my_synonym, english_stem;

SELECT * FROM ts_debug('english', 'Paris');
   alias   |   description   | token |       dictionaries        | dictionary | lexemes
-----------+-----------------+-------+---------------------------+------------+---------
 asciiword | Word, all ASCII | Paris | {my_synonym,english_stem} | my_synonym | {paris}
```

`synonym` 範本唯一必要的參數是 `SYNONYMS`，也就是其設定檔的基本名稱，在上面的範例中是 `my_synonyms`。該檔案的完整名稱是 `$SHAREDIR/tsearch_data/my_synonyms.syn`（其中 `$SHAREDIR` 代表 PostgreSQL 安裝的共用資料目錄）。檔案格式就是每個要替換的單字一行，單字後面接著它的同義詞，以空白分隔。空白行與行尾空白會被忽略。

`synonym` 範本還有一個選用參數 `CaseSensitive`，預設值為 `false`。當 `CaseSensitive` 為 `false` 時，同義詞檔案中的單字會轉為小寫，輸入的語彙單元也一樣。當它為 `true` 時，單字與語彙單元都不會轉為小寫，而是直接比較。

可以在設定檔中同義詞的結尾加上星號（`*`），表示該同義詞是一個前綴。在 `to_tsvector()` 中使用該項目時會忽略星號，但在 `to_tsquery()` 中使用時，結果會是帶有前綴比對標記的查詢項目（請參閱[第 12.3.2 節](textsearch-controls.md#TEXTSEARCH-PARSING-QUERIES)）。例如，假設 `$SHAREDIR/tsearch_data/synonym_sample.syn` 中有下列項目：

```

postgres        pgsql
postgresql      pgsql
postgre pgsql
gogle   googl
indices index*
```

那麼我們會得到下列結果：

```

mydb=# CREATE TEXT SEARCH DICTIONARY syn (template=synonym, synonyms='synonym_sample');
mydb=# SELECT ts_lexize('syn', 'indices');
 ts_lexize
-----------
 {index}
(1 row)

mydb=# CREATE TEXT SEARCH CONFIGURATION tst (copy=simple);
mydb=# ALTER TEXT SEARCH CONFIGURATION tst ALTER MAPPING FOR asciiword WITH syn;
mydb=# SELECT to_tsvector('tst', 'indices');
 to_tsvector
-------------
 'index':1
(1 row)

mydb=# SELECT to_tsquery('tst', 'indices');
 to_tsquery
------------
 'index':*
(1 row)

mydb=# SELECT 'indexes are very useful'::tsvector;
            tsvector
---------------------------------
 'are' 'indexes' 'useful' 'very'
(1 row)

mydb=# SELECT 'indexes are very useful'::tsvector @@ to_tsquery('tst', 'indices');
 ?column?
----------
 t
(1 row)
```

<a id="TEXTSEARCH-THESAURUS"></a>

### 12.6.4. 同義詞庫字典 [#](#TEXTSEARCH-THESAURUS)

同義詞庫字典（thesaurus dictionary，有時縮寫為 TZ）是一組單字的集合，包含單字與片語之間關係的資訊，例如上位詞（broader term，BT）、下位詞（narrower term，NT）、優先詞、非優先詞、相關詞等等。

基本上，同義詞庫字典會將所有非優先詞替換為一個優先詞，並可選擇同時保留原本的詞以建立索引。PostgreSQL 目前實作的同義詞庫字典，是加入了*片語*支援的同義詞字典延伸。同義詞庫字典需要下列格式的設定檔：

```

# this is a comment
sample word(s) : indexed word(s)
more sample word(s) : more indexed word(s)
...
```

其中冒號（`:`）符號作為片語與其替換內容之間的分隔符號。

同義詞庫字典會使用一個*子字典*（subdictionary，在字典的設定中指定），在檢查片語是否相符之前先將輸入文字正規化。只能選擇一個子字典。如果子字典無法辨識某個單字，就會回報錯誤。在這種情況下，你應該移除該單字的使用，或是讓子字典認識它。你可以在索引詞的開頭加上星號（`*`），略過對它套用子字典，但所有範例詞都*必須*是子字典已知的單字。

如果有多個片語與輸入相符，同義詞庫字典會選擇最長的相符項目；長度相同時，則以最後一個定義為準。

無法指定子字典所辨識的特定停用詞；請改用 `?` 標記任何停用詞可以出現的位置。例如，假設依子字典的定義，`a` 與 `the` 都是停用詞：

```

? one ? two : swsw
```

會比對 `a one the two` 與 `the one a two`；兩者都會被替換為 `swsw`。

由於同義詞庫字典具備辨識片語的能力，它必須記住自己的狀態，並與剖析器互動。同義詞庫字典會使用這些指派來檢查它應該處理下一個單字，還是停止累積。同義詞庫字典必須謹慎設定。例如，如果同義詞庫字典只被指派處理 `asciiword` 語彙單元，那麼像 `one 7` 這樣的同義詞庫字典定義就無法運作，因為語彙單元類型 `uint` 並沒有指派給該同義詞庫字典。

### 警示

同義詞庫會在建立索引時使用，因此同義詞庫字典參數的任何變更都*需要*重建索引。對於大多數其他類型的字典，新增或移除停用詞之類的小變更並不會強制需要重建索引。

<a id="TEXTSEARCH-THESAURUS-CONFIG"></a>

#### 12.6.4.1. 同義詞庫設定 [#](#TEXTSEARCH-THESAURUS-CONFIG)

要定義新的同義詞庫字典，請使用 `thesaurus` 範本。例如：

```

CREATE TEXT SEARCH DICTIONARY thesaurus_simple (
    TEMPLATE = thesaurus,
    DictFile = mythesaurus,
    Dictionary = pg_catalog.english_stem
);
```

其中：

* `thesaurus_simple` 是新字典的名稱
* `mythesaurus` 是同義詞庫設定檔的基本名稱。（它的完整名稱是 `$SHAREDIR/tsearch_data/mythesaurus.ths`，其中 `$SHAREDIR` 代表安裝的共用資料目錄。）
* `pg_catalog.english_stem` 是用於同義詞庫正規化的子字典（這裡是 Snowball 英文詞幹處理器）。請注意，子字典會有它自己的設定（例如停用詞），這裡並未列出。

現在就可以在設定中將同義詞庫字典 `thesaurus_simple` 綁定到想要的語彙單元類型，例如：

```

ALTER TEXT SEARCH CONFIGURATION russian
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart
    WITH thesaurus_simple;
```

<a id="TEXTSEARCH-THESAURUS-EXAMPLES"></a>

#### 12.6.4.2. 同義詞庫範例 [#](#TEXTSEARCH-THESAURUS-EXAMPLES)

考慮一個簡單的天文學同義詞庫 `thesaurus_astro`，其中包含一些天文學的詞語組合：

```

supernovae stars : sn
crab nebulae : crab
```

以下我們建立一個字典，並將一些語彙單元類型綁定到天文學同義詞庫與英文詞幹處理器：

```

CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
    TEMPLATE = thesaurus,
    DictFile = thesaurus_astro,
    Dictionary = english_stem
);

ALTER TEXT SEARCH CONFIGURATION russian
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart
    WITH thesaurus_astro, english_stem;
```

現在我們可以看看它是如何運作的。`ts_lexize` 對於測試同義詞庫不太有用，因為它會將輸入視為單一語彙單元。我們可以改用 `plainto_tsquery` 與 `to_tsvector`，它們會將輸入字串切分為多個語彙單元：

```

SELECT plainto_tsquery('supernova star');
 plainto_tsquery
-----------------
 'sn'

SELECT to_tsvector('supernova star');
 to_tsvector
-------------
 'sn':1
```

原則上，如果將參數加上引號，也可以使用 `to_tsquery`：

```

SELECT to_tsquery('''supernova star''');
 to_tsquery
------------
 'sn'
```

請注意，`supernova star` 會與 `thesaurus_astro` 中的 `supernovae stars` 相符，因為我們在同義詞庫的定義中指定了 `english_stem` 詞幹處理器。詞幹處理器移除了 `e` 與 `s`。

若要同時為原本的片語與替換內容建立索引，只要將原片語也放入定義的右側即可：

```

supernovae stars : sn supernovae stars

SELECT plainto_tsquery('supernova star');
       plainto_tsquery
-----------------------------
 'sn' & 'supernova' & 'star'
```

<a id="TEXTSEARCH-ISPELL-DICTIONARY"></a>

### 12.6.5. Ispell 字典 [#](#TEXTSEARCH-ISPELL-DICTIONARY)

Ispell 字典範本支援*詞形字典*（morphological dictionary），可以將一個單字的多種不同語言形式正規化為相同的詞素。例如，英文的 Ispell 字典可以比對搜尋詞 `bank` 的所有詞形變化，例如 `banking`、`banked`、`banks`、`banks'` 與 `bank's`。

標準的 PostgreSQL 發行版本並不包含任何 Ispell 設定檔。許多語言的字典可以從 [Ispell](https://www.cs.hmc.edu/~geoff/ispell.html) 取得。此外，也支援一些較新的字典檔案格式：[MySpell](https://en.wikipedia.org/wiki/MySpell)（OO < 2.0.1）與 [Hunspell](https://hunspell.github.io/)（OO >= 2.0.2）。[OpenOffice Wiki](https://wiki.openoffice.org/wiki/Dictionaries) 上有大量的字典清單。

要建立 Ispell 字典，請執行下列步驟：

* 下載字典設定檔。OpenOffice 擴充套件檔案的副檔名是 `.oxt`。必須從中取出 `.aff` 與 `.dic` 檔案，並將副檔名改為 `.affix` 與 `.dict`。對於某些字典檔案，還需要使用指令將字元轉換為 UTF-8 編碼（例如挪威語字典）：

  ```

  iconv -f ISO_8859-1 -t UTF-8 -o nn_no.affix nn_NO.aff
  iconv -f ISO_8859-1 -t UTF-8 -o nn_no.dict nn_NO.dic
  ```
* 將檔案複製到 `$SHAREDIR/tsearch_data` 目錄
* 使用下列指令將檔案載入 PostgreSQL：

  ```

  CREATE TEXT SEARCH DICTIONARY english_hunspell (
      TEMPLATE = ispell,
      DictFile = en_us,
      AffFile = en_us,
      Stopwords = english);
  ```

這裡的 `DictFile`、`AffFile` 與 `StopWords` 分別指定字典、詞綴與停用詞檔案的基本名稱。停用詞檔案的格式與前面 `simple` 字典類型所說明的相同。其他檔案的格式在此不詳述，但可以從上述網站取得。

Ispell 字典通常只能辨識有限的一組單字，因此後面應該接著另一個範圍更廣的字典，例如能辨識所有內容的 Snowball 字典。

Ispell 的 `.affix` 檔案具有下列結構：

```

prefixes
flag *A:
    .           >   RE      # As in enter > reenter
suffixes
flag T:
    E           >   ST      # As in late > latest
    [^AEIOU]Y   >   -Y,IEST # As in dirty > dirtiest
    [AEIOU]Y    >   EST     # As in gray > grayest
    [^EY]       >   EST     # As in small > smallest
```

而 `.dict` 檔案具有下列結構：

```

lapse/ADGRS
lard/DGRS
large/PRTY
lark/MRS
```

`.dict` 檔案的格式是：

```

basic_form/affix_class_name
```

在 `.affix` 檔案中，每個詞綴旗標都以下列格式描述：

```

condition > [-stripping_letters,] adding_affix
```

這裡的 condition 格式類似於正規表示式的格式。它可以使用 `[...]` 與 `[^...]` 分組。例如，`[AEIOU]Y` 表示單字的最後一個字母是 `"y"`，而倒數第二個字母是 `"a"`、`"e"`、`"i"`、`"o"` 或 `"u"`。`[^EY]` 表示最後一個字母既不是 `"e"`，也不是 `"y"`。

Ispell 字典支援拆分複合詞，這是一項很有用的功能。請注意，詞綴檔案應該使用 `compoundwords controlled` 陳述指定一個特殊旗標，用來標記可以參與組成複合詞的字典單字：

```

compoundwords  controlled z
```

以下是一些挪威語的範例：

```

SELECT ts_lexize('norwegian_ispell', 'overbuljongterningpakkmesterassistent');
   {over,buljong,terning,pakk,mester,assistent}
SELECT ts_lexize('norwegian_ispell', 'sjokoladefabrikk');
   {sjokoladefabrikk,sjokolade,fabrikk}
```

MySpell 格式是 Hunspell 的子集。Hunspell 的 `.affix` 檔案具有下列結構：

```

PFX A Y 1
PFX A   0     re         .
SFX T N 4
SFX T   0     st         e
SFX T   y     iest       [^aeiou]y
SFX T   0     est        [aeiou]y
SFX T   0     est        [^ey]
```

詞綴類別的第一行是標頭。詞綴規則的各個欄位列在標頭之後：

* 參數名稱（PFX 或 SFX）
* 旗標（詞綴類別的名稱）
* 從單字開頭（前綴時）或結尾（後綴時）移除的字元
* 要加上的詞綴
* 格式類似於正規表示式的條件。

`.dict` 檔案看起來與 Ispell 的 `.dict` 檔案相似：

```

larder/M
lardy/RT
large/RSPMYT
largehearted
```

### 注意

MySpell 不支援複合詞。Hunspell 對複合詞有完善的支援。目前 PostgreSQL 只實作了 Hunspell 的基本複合詞運算。

<a id="TEXTSEARCH-SNOWBALL-DICTIONARY"></a>

### 12.6.6. Snowball 字典 [#](#TEXTSEARCH-SNOWBALL-DICTIONARY)

Snowball 字典範本是以 Martin Porter 的專案為基礎，他是廣受歡迎的英文 Porter 詞幹演算法的發明者。Snowball 現在為許多語言提供詞幹演算法（更多資訊請參閱 [Snowball 網站](https://snowballstem.org/)）。每種演算法都知道如何在其語言中，將單字常見的變化形式簡化為基本或詞幹拼法。Snowball 字典需要 `language` 參數來識別要使用哪一個詞幹處理器，並可選擇指定 `stopword` 檔案名稱，提供要剔除的單字清單。（PostgreSQL 的標準停用詞清單也是由 Snowball 專案提供的。）例如，系統內建有一個等同於下列內容的定義

```

CREATE TEXT SEARCH DICTIONARY english_stem (
    TEMPLATE = snowball,
    Language = english,
    StopWords = english
);
```

停用詞檔案的格式與先前說明的相同。

Snowball 字典會辨識所有內容，不論它是否能夠簡化該單字，因此應該放在字典清單的最後。將它放在任何其他字典之前是沒有用的，因為語彙單元永遠不會通過它而傳到下一個字典。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-dictionaries.html)（原文版本：18.6；核對日期：2026-09-11）
