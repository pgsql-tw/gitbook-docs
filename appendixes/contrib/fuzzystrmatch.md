## F.16. fuzzystrmatch — 判定字串相似性與距離 [#](#FUZZYSTRMATCH)

[F.16.1. Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-SOUNDEX)

[F.16.2. Daitch-Mokotoff Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-DAITCH-MOKOTOFF)

[F.16.3. Levenshtein](fuzzystrmatch.md#FUZZYSTRMATCH-LEVENSHTEIN)

[F.16.4. Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-METAPHONE)

[F.16.5. Double Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-DOUBLE-METAPHONE)

<a id="id-1.11.7.26.2"></a>

`fuzzystrmatch` 模組提供數個函式，用於判定字串之間的相似性與距離。

### 注意

目前，`soundex`、`metaphone`、`dmetaphone` 與 `dmetaphone_alt` 函式無法良好處理多位元組編碼（如 UTF-8）。請對這類資料使用 `daitch_mokotoff` 或 `levenshtein`。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="FUZZYSTRMATCH-SOUNDEX"></a>

### F.16.1. Soundex [#](#FUZZYSTRMATCH-SOUNDEX)

Soundex 系統會將發音相似的名稱轉換為相同的代碼，以進行比對。美國人口普查最初於 1880、1900 與 1910 年使用此系統。請注意，Soundex 對非英語名稱不太有用。

`fuzzystrmatch` 模組提供兩個處理 Soundex 代碼的函式：

<a id="id-1.11.7.26.6.4"></a><a id="id-1.11.7.26.6.5"></a>

```

soundex(text) returns text
difference(text, text) returns int
```

`soundex` 函式會將字串轉換為其 Soundex 代碼。`difference` 函式會將兩個字串轉換為其 Soundex 代碼，然後回報相符代碼位置的數目。由於 Soundex 代碼有四個字元，結果範圍為零到四；零表示沒有相符，四表示完全相符。（因此，這個函式的名稱並不恰當；`similarity` 會是更好的名稱。）

以下是一些使用範例：

```

SELECT soundex('hello world!');

SELECT soundex('Anne'), soundex('Ann'), difference('Anne', 'Ann');
SELECT soundex('Anne'), soundex('Andrew'), difference('Anne', 'Andrew');
SELECT soundex('Anne'), soundex('Margaret'), difference('Anne', 'Margaret');

CREATE TABLE s (nm text);

INSERT INTO s VALUES ('john');
INSERT INTO s VALUES ('joan');
INSERT INTO s VALUES ('wobbly');
INSERT INTO s VALUES ('jack');

SELECT * FROM s WHERE soundex(nm) = soundex('john');

SELECT * FROM s WHERE difference(s.nm, 'john') > 2;
```

<a id="FUZZYSTRMATCH-DAITCH-MOKOTOFF"></a>

### F.16.2. Daitch-Mokotoff Soundex [#](#FUZZYSTRMATCH-DAITCH-MOKOTOFF)

如同原始的 Soundex 系統，Daitch-Mokotoff Soundex 會將發音相似的名稱轉換為相同代碼來進行比對。不過，Daitch-Mokotoff Soundex 對非英語名稱的適用性遠高於原始系統。相對於原始系統的主要改良包括：

* 代碼以最先出現的六個有意義字母為基礎，而不是四個。
* 一個字母或字母組合會對應到十種可能代碼，而不是七種。
* 兩個連續字母具有單一發音時，會編碼為單一數字。
* 字母或字母組合可能有不同發音時，會產生多個代碼來涵蓋所有可能性。

<a id="id-1.11.7.26.7.3"></a>

此函式會為輸入值產生 Daitch-Mokotoff Soundex 代碼：

```

daitch_mokotoff(source text) returns text[]
```

結果可能依合理發音的數量而含有一個或多個代碼，因此以陣列表示。

由於 Daitch-Mokotoff Soundex 代碼只有六位數，*`source`* 最好是單一單字或名稱。

以下是一些範例：

```

SELECT daitch_mokotoff('George');
 daitch_mokotoff
-----------------
 {595000}

SELECT daitch_mokotoff('John');
 daitch_mokotoff
-----------------
 {160000,460000}

SELECT daitch_mokotoff('Bierschbach');
                      daitch_mokotoff
-----------------------------------------------------------
 {794575,794574,794750,794740,745750,745740,747500,747400}

SELECT daitch_mokotoff('Schwartzenegger');
 daitch_mokotoff
-----------------
 {479465}
```

若要比對單一名稱，可直接使用 `&&` 運算子比對傳回的文字陣列：只要有任何重疊即可視為相符。為提高效率，可使用 GIN 索引；請參閱[第 65.4 節](../../internals/indextypes/gin.md)及下列範例：

```

CREATE TABLE s (nm text);
CREATE INDEX ix_s_dm ON s USING gin (daitch_mokotoff(nm)) WITH (fastupdate = off);

INSERT INTO s (nm) VALUES
  ('Schwartzenegger'),
  ('John'),
  ('James'),
  ('Steinman'),
  ('Steinmetz');

SELECT * FROM s WHERE daitch_mokotoff(nm) && daitch_mokotoff('Swartzenegger');
SELECT * FROM s WHERE daitch_mokotoff(nm) && daitch_mokotoff('Jane');
SELECT * FROM s WHERE daitch_mokotoff(nm) && daitch_mokotoff('Jens');
```

若要為任意數量且任意順序的名稱建立索引並進行比對，可使用全文檢索功能。請參閱[第 12 章](../../the-sql-language/textsearch/README.md)及下列範例：

```

CREATE FUNCTION soundex_tsvector(v_name text) RETURNS tsvector
BEGIN ATOMIC
  SELECT to_tsvector('simple',
                     string_agg(array_to_string(daitch_mokotoff(n), ' '), ' '))
  FROM regexp_split_to_table(v_name, '\s+') AS n;
END;

CREATE FUNCTION soundex_tsquery(v_name text) RETURNS tsquery
BEGIN ATOMIC
  SELECT string_agg('(' || array_to_string(daitch_mokotoff(n), '|') || ')', '&')::tsquery
  FROM regexp_split_to_table(v_name, '\s+') AS n;
END;

CREATE TABLE s (nm text);
CREATE INDEX ix_s_txt ON s USING gin (soundex_tsvector(nm)) WITH (fastupdate = off);

INSERT INTO s (nm) VALUES
  ('John Doe'),
  ('Jane Roe'),
  ('Public John Q.'),
  ('George Best'),
  ('John Yamson');

SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('john');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('jane doe');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('john public');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('besst, giorgio');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('Jameson John');
```

若要避免在索引重新檢查時重新計算 Soundex 代碼，可使用獨立欄位的索引取代表達式索引。可使用儲存的自動欄位達成此目的；請參閱[第 5.4 節](../../the-sql-language/ddl/ddl-generated-columns.md)。

<a id="FUZZYSTRMATCH-LEVENSHTEIN"></a>

### F.16.3. Levenshtein [#](#FUZZYSTRMATCH-LEVENSHTEIN)

此函式計算兩個字串之間的 Levenshtein 距離：

<a id="id-1.11.7.26.8.3"></a><a id="id-1.11.7.26.8.4"></a>

```

levenshtein(source text, target text, ins_cost int, del_cost int, sub_cost int) returns int
levenshtein(source text, target text) returns int
levenshtein_less_equal(source text, target text, ins_cost int, del_cost int, sub_cost int, max_d int) returns int
levenshtein_less_equal(source text, target text, max_d int) returns int
```

`source` 與 `target` 都可以是任意非 NULL 字串，最多 255 個字元。成本參數分別指定插入、刪除或替換一個字元的成本。您可以如函式的第二種版本般省略成本參數；在此情況下，它們的預設值皆為 1。

`levenshtein_less_equal` 是 Levenshtein 函式的加速版本，適用於只關心較小距離的情況。若實際距離小於或等於 `max_d`，`levenshtein_less_equal` 會傳回正確距離；否則會傳回大於 `max_d` 的某個值。若 `max_d` 為負數，行為與 `levenshtein` 相同。

範例：

```

test=# SELECT levenshtein('GUMBO', 'GAMBOL');
 levenshtein
-------------
           2
(1 row)

test=# SELECT levenshtein('GUMBO', 'GAMBOL', 2, 1, 1);
 levenshtein
-------------
           3
(1 row)

test=# SELECT levenshtein_less_equal('extensive', 'exhaustive', 2);
 levenshtein_less_equal
------------------------
                      3
(1 row)

test=# SELECT levenshtein_less_equal('extensive', 'exhaustive', 4);
 levenshtein_less_equal
------------------------
                      4
(1 row)
```

<a id="FUZZYSTRMATCH-METAPHONE"></a>

### F.16.4. Metaphone [#](#FUZZYSTRMATCH-METAPHONE)

Metaphone 與 Soundex 相同，都是基於為輸入字串建立代表性代碼的概念。兩個字串若有相同代碼，便視為相似。

此函式計算輸入字串的 Metaphone 代碼：

<a id="id-1.11.7.26.9.4"></a>

```

metaphone(source text, max_output_length int) returns text
```

`source` 必須是最多 255 個字元的非 NULL 字串。`max_output_length` 設定輸出 Metaphone 代碼的最大長度；若更長，輸出會截斷為此長度。

範例：

```

test=# SELECT metaphone('GUMBO', 4);
 metaphone
-----------
 KM
(1 row)
```

<a id="FUZZYSTRMATCH-DOUBLE-METAPHONE"></a>

### F.16.5. Double Metaphone [#](#FUZZYSTRMATCH-DOUBLE-METAPHONE)

Double Metaphone 系統會為指定輸入字串計算兩個「聽起來相像」的字串：一個「主要」和一個「替代」。在多數情況下兩者相同，但特別是非英語名稱，兩者可能會因發音而略有不同。這些函式會計算主要與替代代碼：

<a id="id-1.11.7.26.10.3"></a><a id="id-1.11.7.26.10.4"></a>

```

dmetaphone(source text) returns text
dmetaphone_alt(source text) returns text
```

輸入字串沒有長度限制。

範例：

```

test=# SELECT dmetaphone('gumbo');
 dmetaphone
------------
 KMP
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/fuzzystrmatch.html)
