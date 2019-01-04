# 9.4. 字串函式及運算子

本節介紹用於檢查和操作字串值的函數和運算子。此節中的字串包括 character，character varying 和 text 的內容。除非另有說明，否則下面列出的所有函數都適用於所有這些型別，但在使用字串型別時要小心自動填充字元的潛在影響。對於 bit-string 型別，一些函數也可以處理。

SQL 定義了一些字串函數，它們使用關鍵字而不是逗號來分隔參數。詳情見 [Table 9.8](string-functions-and-operators.md#table-9-8-sql-string-functions-and-operators)。PostgreSQL 還提供了一般函數呼叫語法的這些函數的版本（參見 [Table 9.9](string-functions-and-operators.md#table-9-9-other-string-functions)）。

**注意**  
在 PostgreSQL 8.3 之前，由於存在從這些資料型別到文字的強制轉換，這些函數也會默默地接受幾個非字串資料型別的值。但這些強制措施已被刪除，因為它們經常引起令人驚訝的行為。不過，字串連接運算子（\|\|）仍然接受非字串輸入，只要至少有一個輸入是字串型別，如 Table 9.8 所示。對於其他情況，如果需要複製先前的行為，請在語法中加入明確的轉換。

#### **Table 9.8. SQL String Functions and Operators**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| _`string`_ `||` _`string`_ | `text` | 字串連接 | `'Post' || 'greSQL'` | `PostgreSQL` |
| _`string`_ `||` _`non-string`_ or _`non-string`_ `||`_`string`_ | `text` | 字串與一個非字串輸入連接 | `'Value: ' || 42` | `Value: 42` |
| `bit_length(`_`string`_\) | `int` | 字串中的位元數 | `bit_length('jose')` | `32` |
| `char_length(`_`string`_\) or `character_length(`_`string`_\) | `int` | 字串中的字元數 | `char_length('jose')` | `4` |
| `lower(`_`string`_\) | `text` | 將字串轉換為小寫 | `lower('TOM')` | `tom` |
| `octet_length(`_`string`_\) | `int` | 字串中的位元組數 | `octet_length('jose')` | `4` |
| `overlay(`_`string`_ placing _`string`_ from`int` \[for `int`\]\) | `text` | 子字串替換 | `overlay('Txxxxas' placing 'hom' from 2 for 4)` | `Thomas` |
| `position(`_`substring`_ in _`string`_\) | `int` | 指出子字串的位置 | `position('om' in 'Thomas')` | `3` |
| `substring(`_`string`_ \[from `int`\] \[for`int`\]\) | `text` | 提取子字串 | `substring('Thomas' from 2 for 3)` | `hom` |
| `substring(`_`string`_ from _`pattern`_\) | `text` | 提取符合 POSIX 正規表示式的子字串。有關特徵比對的更多訊息，請參見[第 9.7 節](pattern-matching.md)。 | `substring('Thomas' from '...$')` | `mas` |
| `substring(`_`string`_ from _`pattern`_ for_`escape`_\) | `text` | 提取符合 SQL 正規表示式的子字串。有關特徵比對的更多訊息，請參閱[第 9.7 節](pattern-matching.md)。 | `substring('Thomas' from '%#"o_a#"_' for '#')` | `oma` |
| `trim([leading | trailing | both] [`_`characters`_\] from _`string`_\) | `text` | 從字串的開頭，結尾或兩端（兩者都是預設值）中刪除包含某些字元（預設為空格）的最長字串 | `trim(both 'xyz' from 'yxTomxx')` | `Tom` |
| `trim([leading | trailing | both] [from]` _`string`_ \[, _`characters`_\] \) | `text` | trim\(\) 的非標準語法 | `trim(both from 'yxTomxx', 'xyz')` | `Tom` |
| `upper(`_`string`_\) | `text` | 將字串轉換為大寫 | `upper('tom')` | `TOM` |

還有其他字串操作函數可用，在 [Table 9.9](string-functions-and-operators.md#table-9-9-other-string-functions) 中列出。 其中一些內部用於實作 SQL 標準的字串函數列在 [Table 9.8](string-functions-and-operators.md#table-9-8-sql-string-functions-and-operators)。

#### **Table 9.9. Other String Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `ascii(`_`string`_\) | `int` | 參數的第一個字元的 ASCII 碼。對於 UTF8，回傳字元的 Unicode 代碼。對於其他多位元組編碼，參數必須是 ASCII 字元。 | `ascii('x')` | `120` |
| `btrim(`_`string`_ `text` \[, _`characters`_`text`\]\) | `text` | 從字串的開頭和結尾刪除特定字元的最長字串（預設為空格） | `btrim('xyxtrimyyx', 'xyz')` | `trim` |
| `chr(int`\) | `text` | 輸出給定代碼的字元。對於 UTF8，該參數被視為 Unicode 代碼。對於其他多位元組編碼，參數必須指定 ASCII 字元。不允許使用 NULL（0）字元，因為文字資料型別無法儲存這個位元組。 | `chr(65)` | `A` |
| `concat(`_`str`_ `"any"` \[, _`str`_ `"any"` \[, ...\] \]\) | `text` | 連接所有參數的文字結果。NULL 參數會被忽略。 | `concat('abcde', 2, NULL, 22)` | `abcde222` |
| `concat_ws(`_`sep`_ `text`, _`str`_ `"any"` \[,_`str`_ `"any"` \[, ...\] \]\) | `text` | 使用分隔字元連接除第一個參數以外的所有參數。第一個參數用作分隔字串。NULL 參數會被忽略。 | `concat_ws(',', 'abcde', 2, NULL, 22)` | `abcde,2,22` |
| `convert(`_`string`_ `bytea`,_`src_encoding`_ `name`, _`dest_encoding`_`name`\) | `bytea` | 將字串轉換為 dest\_encoding。原始編碼由 src\_encoding 指定。該字串必須在此編碼中有效。可以透過 CREATE CONVERSION 定義轉換。還有一些預定義的轉換。有關可用的轉換，請參閱 [Table 9.10](string-functions-and-operators.md#table-9-10-built-in-conversions)。 | `convert('text_in_utf8', 'UTF8', 'LATIN1')` | `text_in_utf8`represented in Latin-1 encoding \(ISO 8859-1\) |
| `convert_from(`_`string`_ `bytea`,_`src_encoding`_ `name`\) | `text` | 將字串轉換為資料庫編碼。原始編碼由 src\_encoding 指定。該字串必須在此編碼中有效。 | `convert_from('text_in_utf8', 'UTF8')` | `text_in_utf8`represented in the current database encoding |
| `convert_to(`_`string`_ `text`,_`dest_encoding`_ `name`\) | `bytea` | 將字串轉換為 dest\_encoding。 | `convert_to('some text', 'UTF8')` | `some text` represented in the UTF8 encoding |
| `decode(`_`string`_ `text`, _`format`_ `text`\) | `bytea` | 從字串中的文字表示中解碼二進位資料。格式選項與編碼相同。 | `decode('MTIzAAE=', 'base64')` | `\x3132330001` |
| `encode(`_`data`_ `bytea`, _`format`_ `text`\) | `text` | 將二進制資料編碼為文字表示。支援的格式為：base64，hex，escape。escape 將零位元組和 high-bit-set 位元組轉換為八進制序列（\nnn）並將倒斜線加倍。 | `encode(E'123\\000\\001', 'base64')` | `MTIzAAE=` |
| `format`\(_`formatstr`_ `text` \[,_`formatarg`_ `"any"` \[, ...\] \]\) | `text` | 根據格式字串格式化參數。此功能類似於 C 函數 sprintf。詳見 [9.4.1 節](string-functions-and-operators.md#9-4-1-format)。 | `format('Hello %s, %1$s', 'World')` | `Hello World, World` |
| `initcap(`_`string`_\) | `text` | 將每個單詞的第一個字母轉換為大寫，其餘單詞轉換為小寫。單詞是由非字母數字字元分隔的字母數字字元序列。 | `initcap('hi THOMAS')` | `Hi Thomas` |
| `left(`_`str`_ `text`, _`n`_ `int`\) | `text` | 回傳字串中的前 n 個字元。當 n 為負數時，回傳除最後 \|n\| 之外的所有內容字元。 | `left('abcde', 2)` | `ab` |
| `length(`_`string`_\) | `int` | 字串中的字元數 | `length('jose')` | `4` |
| `length(`_`string`_ `bytea`, _`encoding`_`name` \) | `int` | 給定編碼中字串中的字元數。該字串必須在此編碼中有效。 | `length('jose', 'UTF8')` | `4` |
| `lpad(`_`string`_ `text`, _`length`_ `int` \[,_`fill`_ `text`\]\) | `text` | 透過在字元填充前加上字串填充（預設為空格）。 如果字串已經長於長度，那麼它將被截斷（在右側）。 | `lpad('hi', 5, 'xy')` | `xyxhi` |
| `ltrim(`_`string`_ `text` \[, _`characters`_`text`\]\) | `text` | 從字串的開頭刪除最長指定字元的字串（預設為空格） | `ltrim('zzzytest', 'xyz')` | `test` |
| `md5(`_`string`_\) | `text` | 計算字串的 MD5 雜湊值，以十六進位形式回傳結果 | `md5('abc')` | `900150983cd24fb0 d6963f7d28e17f72` |
| `parse_ident(`_`qualified_identifier`_`text` \[, _`strictmode`_ `boolean`DEFAULT true \] \) | `text[]` | 將 qualified\_identifier 以標示字拆分為陣列，刪除任何單個標示字的引用。預設情況下，最後一個標示字後面的額外字元將被視為錯誤；但如果第二個參數為 false，則忽略這些額外的字元。（此行為對於解析函數等物件的名稱很有用。）請注意，此函數不會截斷超長標示字。如果要截斷，可以將結果轉換為 name\[\]。 | `parse_ident('"SomeSchema".someTable')` | `{SomeSchema,sometable}` |
| `pg_client_encoding()` | `name` | 目前用戶端的編碼名稱 | `pg_client_encoding()` | `SQL_ASCII` |
| `quote_ident(`_`string`_ `text`\) | `text` | 回傳適當引用的字串，以用作 SQL 語句字串中的標示字。僅在必要時加上引號（即如果字串包含非標示字或將被大小寫折疊）。 嵌入式引號會正確加倍。請參閱[例 42.1](../../server-programming/pl-pgsql-sql-procedural-language/basic-statements.md)。 | `quote_ident('Foo bar')` | `"Foo bar"` |
| `quote_literal(`_`string`_ `text`\) | `text` | 回傳適當引用的字串，以用作 SQL 語句字串中的字串文字。嵌入式單引號和倒斜線會適當加倍。請注意，quote\_literal 在 null 輸入時回傳 null；如果參數可能為 null，則 quote\_nullable 通常更合適。請參閱[例 42.1](../../server-programming/pl-pgsql-sql-procedural-language/basic-statements.md)。 | `quote_literal(E'O\'Reilly')` | `'O''Reilly'` |
| `quote_literal(`_`value`_ `anyelement`\) | `text` | 將給定的值強制轉換為文字型別，然後將其引用為文字。嵌入式單引號和反斜線會適當加倍。 | `quote_literal(42.5)` | `'42.5'` |
| `quote_nullable(`_`string`_ `text`\) | `text` | 回傳適當引用的字串，以用作 SQL 語句字串中的字串文字；或者，如果參數為 null，則回傳NULL。嵌入式單引號和倒斜線將適當加倍。請參閱[例 42.1](../../server-programming/pl-pgsql-sql-procedural-language/basic-statements.md)。 | `quote_nullable(NULL)` | `NULL` |
| `quote_nullable(`_`value`_ `anyelement`\) | `text` | 將給定的值強制轉換為文字型別，然後將其引用為文字；或者，如果參數為 null，則回傳 NULL。嵌入式單引號和倒斜線將適當加倍。 | `quote_nullable(42.5)` | `'42.5'` |
| `regexp_match(`_`string`_ `text`,_`pattern`_ `text` \[, _`flags`_ `text`\]\) | `text[]` | 回傳由 POSIX 正規表示式與字串的第一個匹配產生的子字串。有關更多訊息，請參閱[第 9.7.3 節](pattern-matching.md#9-7-3-posix-regular-expressions)。 | `regexp_match('foobarbequebaz', '(bar)(beque)')` | `{bar,beque}` |
| `regexp_matches(`_`string`_ `text`,_`pattern`_ `text` \[, _`flags`_ `text`\]\) | `setof text[]` | 回傳透過將 POSIX 正規表示式與字串匹配而得到的子字串。有關更多訊息，請參閱[第 9.7.3 節](pattern-matching.md#9-7-3-posix-regular-expressions)。 | `regexp_matches('foobarbequebaz', 'ba.', 'g')` | `{bar}{baz}`\(2 rows\) |
| `regexp_replace(`_`string`_ `text`,_`pattern`_ `text`, _`replacement`_ `text`\[, _`flags`_ `text`\]\) | `text` | 替換與 POSIX 正規表示式匹配的子字串。有關更多訊息，請參閱[第 9.7.3 節](pattern-matching.md#9-7-3-posix-regular-expressions)。 | `regexp_replace('Thomas', '.[mN]a.', 'M')` | `ThM` |
| `regexp_split_to_array(`_`string`_`text`, _`pattern`_ `text` \[, _`flags`_ `text`\]\) | `text[]` | 使用 POSIX 正規表示式作為分隔字拆分字串。有關更多訊息，請參閱[第 9.7.3 節](pattern-matching.md#9-7-3-posix-regular-expressions)。 | `regexp_split_to_array('hello world', E'\\s+')` | `{hello,world}` |
| `regexp_split_to_table(`_`string`_`text`, _`pattern`_ `text` \[, _`flags`_`text`\]\) | `setof text` | 使用 POSIX 正規表示式作為分隔字拆分字串。有關更多訊息，請參閱[第 9.7.3 節](pattern-matching.md#9-7-3-posix-regular-expressions)。 | `regexp_split_to_table('hello world', E'\\s+')` | `helloworld`\(2 rows\) |
| `repeat(`_`string`_ `text`, _`number`_ `int`\) | `text` | 將字串重複的指定次數 | `repeat('Pg', 4)` | `PgPgPgPg` |
| `replace(`_`string`_ `text`, _`from`_ `text`,_`to`_ `text`\) | `text` | 以子字串 to 替換所有符合 from 的子字串 | `replace('abcdefabcdef', 'cd', 'XX')` | `abXXefabXXef` |
| `reverse(`_`str`_\) | `text` | 回傳反轉字串。 | `reverse('abcde')` | `edcba` |
| `right(`_`str`_ `text`, _`n`_ `int`\) | `text` | 回傳字串中的最後 n 個字元。當 n 為負數時，回傳除了第一個 \|n\| 之外的所有字元。 | `right('abcde', 2)` | `de` |
| `rpad(`_`string`_ `text`, _`length`_ `int` \[,_`fill`_ `text`\]\) | `text` | 透過附加字元 fill（預設為空格）將字串填充至長度 length。如果字串已經長於 length，那麼它將被截斷。 | `rpad('hi', 5, 'xy')` | `hixyx` |
| `rtrim(`_`string`_ `text` \[, _`characters`_`text`\]\) | `text` | 從字串末尾刪除最長某包含 characters （預設為空格）的字串 | `rtrim('testxxzx', 'xyz')` | `test` |
| `split_part(`_`string`_ `text`,_`delimiter`_ `text`, _`field`_ `int`\) | `text` | 在分隔字上拆分字串並回傳給定段落（從一個字元開始） | `split_part('abc~@~def~@~ghi', '~@~', 2)` | `def` |
| `strpos(`_`string`_, _`substring`_\) | `int` | 回傳子字串的位置（與 position 相同，但請注意參數順序不同） | `strpos('high', 'ig')` | `2` |
| `substr(`_`string`_, _`from`_ \[, _`count`_\]\) | `text` | 提取子字串（與 substring 相同） | `substr('alphabet', 3, 2)` | `ph` |
| `to_ascii(`_`string`_ `text` \[, _`encoding`_`text`\]\) | `text` | 從其他編碼將字串轉換為 ASCII（僅支援從 LATIN1，LATIN2，LATIN9 和 WIN1250 編碼轉換） | `to_ascii('Karel')` | `Karel` |
| `to_hex(`_`number`_ `int` or `bigint`\) | `text` | 將數字轉換為其等效的十六進位表示 | `to_hex(2147483647)` | `7fffffff` |
| `translate(`_`string`_ `text`, _`from`_`text`, _`to`_ `text`\) | `text` | 字串中與 from 集合中相符合的任何字元都將替換為 to 集合中的相對應字元。如果 from 長於 to，則會刪除 from 中出現的額外字元。 | `translate('12345', '143', 'ax')` | `a2x5` |

concat，concat\_ws 和 format 函數是可變參數，因此可以將值連接或格式化成標記為 VARIADIC 關鍵字的陣列（請參閱[第 37.4.5 節](../../server-programming/extending-sql/user-defined-procedures.md#37-4-5-sql-functions-with-variable-numbers-of-arguments)）。陣列的元素被視為它們是函數的單獨普通參數。如果 variadic 陣列參數為 NULL，則 concat 和 concat\_ws 回傳 NULL，但 format 將 NULL 視為零元素陣列。

另請參閱[第 9.20 節](aggregate-functions.md)中的彙總函數 string\_agg。

#### **Table 9.10. Built-in Conversions**

| Conversion Name [\[a\]](https://www.postgresql.org/docs/10/static/functions-string.html#ftn.id-1.5.8.9.10.2.1.1.1.1) | Source Encoding | Destination Encoding |
| :--- | :--- | :--- |
| `ascii_to_mic` | `SQL_ASCII` | `MULE_INTERNAL` |
| `ascii_to_utf8` | `SQL_ASCII` | `UTF8` |
| `big5_to_euc_tw` | `BIG5` | `EUC_TW` |
| `big5_to_mic` | `BIG5` | `MULE_INTERNAL` |
| `big5_to_utf8` | `BIG5` | `UTF8` |
| `euc_cn_to_mic` | `EUC_CN` | `MULE_INTERNAL` |
| `euc_cn_to_utf8` | `EUC_CN` | `UTF8` |
| `euc_jp_to_mic` | `EUC_JP` | `MULE_INTERNAL` |
| `euc_jp_to_sjis` | `EUC_JP` | `SJIS` |
| `euc_jp_to_utf8` | `EUC_JP` | `UTF8` |
| `euc_kr_to_mic` | `EUC_KR` | `MULE_INTERNAL` |
| `euc_kr_to_utf8` | `EUC_KR` | `UTF8` |
| `euc_tw_to_big5` | `EUC_TW` | `BIG5` |
| `euc_tw_to_mic` | `EUC_TW` | `MULE_INTERNAL` |
| `euc_tw_to_utf8` | `EUC_TW` | `UTF8` |
| `gb18030_to_utf8` | `GB18030` | `UTF8` |
| `gbk_to_utf8` | `GBK` | `UTF8` |
| `iso_8859_10_to_utf8` | `LATIN6` | `UTF8` |
| `iso_8859_13_to_utf8` | `LATIN7` | `UTF8` |
| `iso_8859_14_to_utf8` | `LATIN8` | `UTF8` |
| `iso_8859_15_to_utf8` | `LATIN9` | `UTF8` |
| `iso_8859_16_to_utf8` | `LATIN10` | `UTF8` |
| `iso_8859_1_to_mic` | `LATIN1` | `MULE_INTERNAL` |
| `iso_8859_1_to_utf8` | `LATIN1` | `UTF8` |
| `iso_8859_2_to_mic` | `LATIN2` | `MULE_INTERNAL` |
| `iso_8859_2_to_utf8` | `LATIN2` | `UTF8` |
| `iso_8859_2_to_windows_1250` | `LATIN2` | `WIN1250` |
| `iso_8859_3_to_mic` | `LATIN3` | `MULE_INTERNAL` |
| `iso_8859_3_to_utf8` | `LATIN3` | `UTF8` |
| `iso_8859_4_to_mic` | `LATIN4` | `MULE_INTERNAL` |
| `iso_8859_4_to_utf8` | `LATIN4` | `UTF8` |
| `iso_8859_5_to_koi8_r` | `ISO_8859_5` | `KOI8R` |
| `iso_8859_5_to_mic` | `ISO_8859_5` | `MULE_INTERNAL` |
| `iso_8859_5_to_utf8` | `ISO_8859_5` | `UTF8` |
| `iso_8859_5_to_windows_1251` | `ISO_8859_5` | `WIN1251` |
| `iso_8859_5_to_windows_866` | `ISO_8859_5` | `WIN866` |
| `iso_8859_6_to_utf8` | `ISO_8859_6` | `UTF8` |
| `iso_8859_7_to_utf8` | `ISO_8859_7` | `UTF8` |
| `iso_8859_8_to_utf8` | `ISO_8859_8` | `UTF8` |
| `iso_8859_9_to_utf8` | `LATIN5` | `UTF8` |
| `johab_to_utf8` | `JOHAB` | `UTF8` |
| `koi8_r_to_iso_8859_5` | `KOI8R` | `ISO_8859_5` |
| `koi8_r_to_mic` | `KOI8R` | `MULE_INTERNAL` |
| `koi8_r_to_utf8` | `KOI8R` | `UTF8` |
| `koi8_r_to_windows_1251` | `KOI8R` | `WIN1251` |
| `koi8_r_to_windows_866` | `KOI8R` | `WIN866` |
| `koi8_u_to_utf8` | `KOI8U` | `UTF8` |
| `mic_to_ascii` | `MULE_INTERNAL` | `SQL_ASCII` |
| `mic_to_big5` | `MULE_INTERNAL` | `BIG5` |
| `mic_to_euc_cn` | `MULE_INTERNAL` | `EUC_CN` |
| `mic_to_euc_jp` | `MULE_INTERNAL` | `EUC_JP` |
| `mic_to_euc_kr` | `MULE_INTERNAL` | `EUC_KR` |
| `mic_to_euc_tw` | `MULE_INTERNAL` | `EUC_TW` |
| `mic_to_iso_8859_1` | `MULE_INTERNAL` | `LATIN1` |
| `mic_to_iso_8859_2` | `MULE_INTERNAL` | `LATIN2` |
| `mic_to_iso_8859_3` | `MULE_INTERNAL` | `LATIN3` |
| `mic_to_iso_8859_4` | `MULE_INTERNAL` | `LATIN4` |
| `mic_to_iso_8859_5` | `MULE_INTERNAL` | `ISO_8859_5` |
| `mic_to_koi8_r` | `MULE_INTERNAL` | `KOI8R` |
| `mic_to_sjis` | `MULE_INTERNAL` | `SJIS` |
| `mic_to_windows_1250` | `MULE_INTERNAL` | `WIN1250` |
| `mic_to_windows_1251` | `MULE_INTERNAL` | `WIN1251` |
| `mic_to_windows_866` | `MULE_INTERNAL` | `WIN866` |
| `sjis_to_euc_jp` | `SJIS` | `EUC_JP` |
| `sjis_to_mic` | `SJIS` | `MULE_INTERNAL` |
| `sjis_to_utf8` | `SJIS` | `UTF8` |
| `tcvn_to_utf8` | `WIN1258` | `UTF8` |
| `uhc_to_utf8` | `UHC` | `UTF8` |
| `utf8_to_ascii` | `UTF8` | `SQL_ASCII` |
| `utf8_to_big5` | `UTF8` | `BIG5` |
| `utf8_to_euc_cn` | `UTF8` | `EUC_CN` |
| `utf8_to_euc_jp` | `UTF8` | `EUC_JP` |
| `utf8_to_euc_kr` | `UTF8` | `EUC_KR` |
| `utf8_to_euc_tw` | `UTF8` | `EUC_TW` |
| `utf8_to_gb18030` | `UTF8` | `GB18030` |
| `utf8_to_gbk` | `UTF8` | `GBK` |
| `utf8_to_iso_8859_1` | `UTF8` | `LATIN1` |
| `utf8_to_iso_8859_10` | `UTF8` | `LATIN6` |
| `utf8_to_iso_8859_13` | `UTF8` | `LATIN7` |
| `utf8_to_iso_8859_14` | `UTF8` | `LATIN8` |
| `utf8_to_iso_8859_15` | `UTF8` | `LATIN9` |
| `utf8_to_iso_8859_16` | `UTF8` | `LATIN10` |
| `utf8_to_iso_8859_2` | `UTF8` | `LATIN2` |
| `utf8_to_iso_8859_3` | `UTF8` | `LATIN3` |
| `utf8_to_iso_8859_4` | `UTF8` | `LATIN4` |
| `utf8_to_iso_8859_5` | `UTF8` | `ISO_8859_5` |
| `utf8_to_iso_8859_6` | `UTF8` | `ISO_8859_6` |
| `utf8_to_iso_8859_7` | `UTF8` | `ISO_8859_7` |
| `utf8_to_iso_8859_8` | `UTF8` | `ISO_8859_8` |
| `utf8_to_iso_8859_9` | `UTF8` | `LATIN5` |
| `utf8_to_johab` | `UTF8` | `JOHAB` |
| `utf8_to_koi8_r` | `UTF8` | `KOI8R` |
| `utf8_to_koi8_u` | `UTF8` | `KOI8U` |
| `utf8_to_sjis` | `UTF8` | `SJIS` |
| `utf8_to_tcvn` | `UTF8` | `WIN1258` |
| `utf8_to_uhc` | `UTF8` | `UHC` |
| `utf8_to_windows_1250` | `UTF8` | `WIN1250` |
| `utf8_to_windows_1251` | `UTF8` | `WIN1251` |
| `utf8_to_windows_1252` | `UTF8` | `WIN1252` |
| `utf8_to_windows_1253` | `UTF8` | `WIN1253` |
| `utf8_to_windows_1254` | `UTF8` | `WIN1254` |
| `utf8_to_windows_1255` | `UTF8` | `WIN1255` |
| `utf8_to_windows_1256` | `UTF8` | `WIN1256` |
| `utf8_to_windows_1257` | `UTF8` | `WIN1257` |
| `utf8_to_windows_866` | `UTF8` | `WIN866` |
| `utf8_to_windows_874` | `UTF8` | `WIN874` |
| `windows_1250_to_iso_8859_2` | `WIN1250` | `LATIN2` |
| `windows_1250_to_mic` | `WIN1250` | `MULE_INTERNAL` |
| `windows_1250_to_utf8` | `WIN1250` | `UTF8` |
| `windows_1251_to_iso_8859_5` | `WIN1251` | `ISO_8859_5` |
| `windows_1251_to_koi8_r` | `WIN1251` | `KOI8R` |
| `windows_1251_to_mic` | `WIN1251` | `MULE_INTERNAL` |
| `windows_1251_to_utf8` | `WIN1251` | `UTF8` |
| `windows_1251_to_windows_866` | `WIN1251` | `WIN866` |
| `windows_1252_to_utf8` | `WIN1252` | `UTF8` |
| `windows_1256_to_utf8` | `WIN1256` | `UTF8` |
| `windows_866_to_iso_8859_5` | `WIN866` | `ISO_8859_5` |
| `windows_866_to_koi8_r` | `WIN866` | `KOI8R` |
| `windows_866_to_mic` | `WIN866` | `MULE_INTERNAL` |
| `windows_866_to_utf8` | `WIN866` | `UTF8` |
| `windows_866_to_windows_1251` | `WIN866` | `WIN` |
| `windows_874_to_utf8` | `WIN874` | `UTF8` |
| `euc_jis_2004_to_utf8` | `EUC_JIS_2004` | `UTF8` |
| `utf8_to_euc_jis_2004` | `UTF8` | `EUC_JIS_2004` |
| `shift_jis_2004_to_utf8` | `SHIFT_JIS_2004` | `UTF8` |
| `utf8_to_shift_jis_2004` | `UTF8` | `SHIFT_JIS_2004` |
| `euc_jis_2004_to_shift_jis_2004` | `EUC_JIS_2004` | `SHIFT_JIS_2004` |
| `shift_jis_2004_to_euc_jis_2004` | `SHIFT_JIS_2004` | `EUC_JIS_2004` |
| [\[a\]](https://www.postgresql.org/docs/10/static/functions-string.html#id-1.5.8.9.10.2.1.1.1.1) 轉換名稱遵循標準命名方式：原始碼的正式名稱，所有非字母數字字元替換為底線，後接_to_，後接類似處理的目標編碼名稱。因此，名稱可能會偏離慣用的編碼名稱。 |  |  |

## 9.4.1. `format`

函數格式化輸出根據格式字串的輸出，其格式類似於 C 函數 sprintf。

```text
format(formatstr text [, formatarg "any" [, ...] ])
```

formatstr 是一個格式字串，指定如何格式化結果。格式字串中的文字將直接複製到結果中，除非使用格式標示符。格式標示符充當字串中的佔位符，定義後續函數參數應如何格式化並插入結果中。每個 formatarg 參數根據其資料型別的一般輸出規則轉換為文字，然後根據格式標示符進行格式化並插入到結果字串中。

格式標示符由 % 字元引入並具有其語法

```text
%[position][flags][width]type
```

組件段落的位置：position（選擇性）

形式為 n$ 的字串，其中 n 是要輸入參數的索引。索引 1 表示 formatstr 之後的第一個參數。如果省略該位置，則預設使用 sequence.flags 中的下一個參數（選擇性）

控制格式標示符輸出格式的其他選項。目前唯一支援的標示是減號（ - ），這將使格式標示符的輸出向左對齊。除非還指定了 width，否則這沒有效果。（選擇性）

指定用於顯示格式標示符輸出的最小字元數。輸出在左側或右側（取決於 - 標示）填充，並根據需要填充空格以填充寬度。寬度太小不會導致截斷輸出，但會被忽略。可以使用以下任何一種來指定寬度：正整數；星號（_）使用下一個函數參數作為寬度；或者_ n$ 形式的字串，以使用第 n 個函數參數作為寬度。

如果寬度來自函數參數，則該參數在用於格式標示符值的參數之前使用。如果 width 參數為負，則結果在長度為 abs\(width\).type（必要）的段落內保持對齊（就像指定了 - 標誌一樣）。

用於産生格式標示符輸出的格式轉換型別。支援以下型別：

* `s` 將參數值格式化為簡單字串。空值被視為空字串。
* `I` 將參數值視為 SQL 標示符，必要時對其進行雙引號。值為 null（相當於 quote\_ident）是一個錯誤。
* `L` 引用參數值作為 SQL 文字。空值顯示為字串 NULL，不帶引號（相當於 quote\_nullable）。

除了上面描述的格式標示符之外，特殊序列 %% 可用於輸出文字 % 字元。

以下是基本格式轉換的一些範例：

```text
SELECT format('Hello %s', 'World');
Result: Hello World

SELECT format('Testing %s, %s, %s, %%', 'one', 'two', 'three');
Result: Testing one, two, three, %

SELECT format('INSERT INTO %I VALUES(%L)', 'Foo bar', E'O\'Reilly');
Result: INSERT INTO "Foo bar" VALUES('O''Reilly')

SELECT format('INSERT INTO %I VALUES(%L)', 'locations', E'C:\\Program Files');
Result: INSERT INTO locations VALUES(E'C:\\Program Files')
```

以下是使用寬度欄位和 - 標示的範例：

```text
SELECT format('|%10s|', 'foo');
Result: |       foo|

SELECT format('|%-10s|', 'foo');
Result: |foo       |

SELECT format('|%*s|', 10, 'foo');
Result: |       foo|

SELECT format('|%*s|', -10, 'foo');
Result: |foo       |

SELECT format('|%-*s|', 10, 'foo');
Result: |foo       |

SELECT format('|%-*s|', -10, 'foo');
Result: |foo       |
```

這些範例顯示了 position 欄位的使用：

```text
SELECT format('Testing %3$s, %2$s, %1$s', 'one', 'two', 'three');
Result: Testing three, two, one

SELECT format('|%*2$s|', 'foo', 10, 'bar');
Result: |       bar|

SELECT format('|%1$*2$s|', 'foo', 10, 'bar');
Result: |       foo|
```

與標準 C 函數 sprintf 不同，PostgreSQL 的格式函數允許將具有和不具有位置欄位的格式標示符混合在相同的格式字串中。沒有位置欄位的格式標示符始終使用最後一個參數消耗後的下一個參數。此外，format 函數不要求在格式字串中使用所有函數參數。例如：

```text
SELECT format('Testing %3$s, %2$s, %s', 'one', 'two', 'three');
Result: Testing three, two, three
```

%I 和 %L 格式標示符對於安全地建構動態 SQL 語句特別有用。詳見[範例 42.1](../../server-programming/pl-pgsql-sql-procedural-language/basic-statements.md)。

