# 9.4. 字串函式及運算子

本節介紹了用於檢查和操作字串的函數和運算子。在這種情況下，字串包括 character、character varying 和 text 型別的值。除非另有說明，否則下面列出的所有函數都可以在這些型別上使用，但是請注意在使用 character 型別時自動空格填充的潛在影響。其中有一些函數還支援對於位元型別的處理。

SQL 定義了一些使用關鍵字而不是逗號分隔參數的字串函數。詳情請見 [Table 9.9](string-functions-and-operators.md#table-9-9-sql-string-functions-and-operators)。PostgreSQL 還提供了使用一般函數呼叫的語法，這些功能的函數版本（請參見 [Table 9.10](string-functions-and-operators.md#table-9-10-other-string-functions)）。

{% hint style="info" %}
在 PostgreSQL 8.3 之前的版本中，由於存在從這些資料型別到文字的隱式強制轉換，這些函數也將默默接受幾種非字串資料型別的值。這些強制轉換已被刪除，因為它們經常引起令人驚訝的結果。但是，字串連接運算子（||）仍然接受非字串輸入，只要至少一個輸入為字串型別即可，如 Table 9.9 所示。對於其他情況，如果您需要複製以前的行為，請在查詢語句中明確加入型別轉換。
{% endhint %}

#### **Table 9.9. SQL String Functions and Operators**

| Function                                                                     | Return Type | Description                                                                                                                                                                  | Example                                         | Result       |
| ---------------------------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ------------ |
| _`string`_ `\|\|` _`string`_                                                 | `text`      | String concatenation                                                                                                                                                         | `'Post' \|\| 'greSQL'`                          | `PostgreSQL` |
| _`string`_ `\|\|` _`non-string`_ or _`non-string`_ `\|\|` _`string`_         | `text`      | String concatenation with one non-string input                                                                                                                               | `'Value: ' \|\| 42`                             | `Value: 42`  |
| `bit_length(`_`string`_)                                                     | `int`       | Number of bits in string                                                                                                                                                     | `bit_length('jose')`                            | `32`         |
| `char_length(`_`string`_) or `character_length(`_`string`_)                  | `int`       | Number of characters in string                                                                                                                                               | `char_length('jose')`                           | `4`          |
| `lower(`_`string`_)                                                          | `text`      | Convert string to lower case                                                                                                                                                 | `lower('TOM')`                                  | `tom`        |
| `octet_length(`_`string`_)                                                   | `int`       | Number of bytes in string                                                                                                                                                    | `octet_length('jose')`                          | `4`          |
| `overlay(`_`string`_ placing _`string`_ from `int` \[for `int`])             | `text`      | Replace substring                                                                                                                                                            | `overlay('Txxxxas' placing 'hom' from 2 for 4)` | `Thomas`     |
| `position(`_`substring`_ in _`string`_)                                      | `int`       | Location of specified substring                                                                                                                                              | `position('om' in 'Thomas')`                    | `3`          |
| `substring(`_`string`_ \[from `int`] \[for `int`])                           | `text`      | Extract substring                                                                                                                                                            | `substring('Thomas' from 2 for 3)`              | `hom`        |
| `substring(`_`string`_ from _`pattern`_)                                     | `text`      | Extract substring matching POSIX regular expression. See [Section 9.7](https://www.postgresql.org/docs/12/functions-matching.html) for more information on pattern matching. | `substring('Thomas' from '...$')`               | `mas`        |
| `substring(`_`string`_ from _`pattern`_ for _`escape`_)                      | `text`      | Extract substring matching SQL regular expression. See [Section 9.7](https://www.postgresql.org/docs/12/functions-matching.html) for more information on pattern matching.   | `substring('Thomas' from '%#"o_a#"_' for '#')`  | `oma`        |
| `trim([leading \| trailing \| both] [`_`characters`_] from _`string`_)       | `text`      | Remove the longest string containing only characters from _`characters`_ (a space by default) from the start, end, or both ends (`both` is the default) of _`string`_        | `trim(both 'xyz' from 'yxTomxx')`               | `Tom`        |
| `trim([leading \| trailing \| both] [from] `_`string`_ \[, _`characters`_] ) | `text`      | Non-standard syntax for `trim()`                                                                                                                                             | `trim(both from 'yxTomxx', 'xyz')`              | `Tom`        |
| `upper(`_`string`_)                                                          | `text`      | Convert string to upper case                                                                                                                                                 | `upper('tom')`                                  | `TOM`        |

其他字串操作的可用函數，在 [Table 9.10](string-functions-and-operators.md#table-9-10-other-string-functions) 中列出。其中一些用於內部實作的SQL標準字符串函數，則在 [Table 9.9](string-functions-and-operators.md#table-9-9-sql-string-functions-and-operators) 中列出。

#### **Table 9.10. Other String Functions**

| Function                                                                                              | Return Type    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Example                                          | Result                                                      |
| ----------------------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------- |
| `ascii(`_`string`_)                                                                                   | `int`          | ASCII code of the first character of the argument. For UTF8 returns the Unicode code point of the character. For other multibyte encodings, the argument must be an ASCII character.                                                                                                                                                                                                                                                                                                | `ascii('x')`                                     | `120`                                                       |
| `btrim(`_`string`_ `text` \[, _`characters`_ `text`])                                                 | `text`         | Remove the longest string consisting only of characters in _`characters`_ (a space by default) from the start and end of _`string`_                                                                                                                                                                                                                                                                                                                                                 | `btrim('xyxtrimyyx', 'xyz')`                     | `trim`                                                      |
| `chr(int`)                                                                                            | `text`         | Character with the given code. For UTF8 the argument is treated as a Unicode code point. For other multibyte encodings the argument must designate an ASCII character. The NULL (0) character is not allowed because text data types cannot store such bytes.                                                                                                                                                                                                                       | `chr(65)`                                        | `A`                                                         |
| `concat(`_`str`_ `"any"` \[, _`str`_ `"any"` \[, ...] ])                                              | `text`         | Concatenate the text representations of all the arguments. NULL arguments are ignored.                                                                                                                                                                                                                                                                                                                                                                                              | `concat('abcde', 2, NULL, 22)`                   | `abcde222`                                                  |
| `concat_ws(`_`sep`_ `text`, _`str`_ `"any"` \[, _`str`_ `"any"` \[, ...] ])                           | `text`         | Concatenate all but the first argument with separators. The first argument is used as the separator string. NULL arguments are ignored.                                                                                                                                                                                                                                                                                                                                             | `concat_ws(',', 'abcde', 2, NULL, 22)`           | `abcde,2,22`                                                |
| `convert(`_`string`_ `bytea`, _`src_encoding`_ `name`, _`dest_encoding`_ `name`)                      | `bytea`        | Convert string to _`dest_encoding`_. The original encoding is specified by _`src_encoding`_. The _`string`_ must be valid in this encoding. Conversions can be defined by `CREATE CONVERSION`. Also there are some predefined conversions. See [Table 9.11](https://www.postgresql.org/docs/12/functions-string.html#CONVERSION-NAMES) for available conversions.                                                                                                                   | `convert('text_in_utf8', 'UTF8', 'LATIN1')`      | `text_in_utf8` represented in Latin-1 encoding (ISO 8859-1) |
| `convert_from(`_`string`_ `bytea`, _`src_encoding`_ `name`)                                           | `text`         | Convert string to the database encoding. The original encoding is specified by _`src_encoding`_. The _`string`_ must be valid in this encoding.                                                                                                                                                                                                                                                                                                                                     | `convert_from('text_in_utf8', 'UTF8')`           | `text_in_utf8` represented in the current database encoding |
| `convert_to(`_`string`_ `text`, _`dest_encoding`_ `name`)                                             | `bytea`        | Convert string to _`dest_encoding`_.                                                                                                                                                                                                                                                                                                                                                                                                                                                | `convert_to('some text', 'UTF8')`                | `some text` represented in the UTF8 encoding                |
| `decode(`_`string`_ `text`, _`format`_ `text`)                                                        | `bytea`        | Decode binary data from textual representation in _`string`_. Options for _`format`_ are same as in `encode`.                                                                                                                                                                                                                                                                                                                                                                       | `decode('MTIzAAE=', 'base64')`                   | `\x3132330001`                                              |
| `encode(`_`data`_ `bytea`, _`format`_ `text`)                                                         | `text`         | Encode binary data into a textual representation. Supported formats are: `base64`, `hex`, `escape`. `escape` converts zero bytes and high-bit-set bytes to octal sequences (`\`_`nnn`_) and doubles backslashes.                                                                                                                                                                                                                                                                    | `encode('123\000\001', 'base64')`                | `MTIzAAE=`                                                  |
| `format`(_`formatstr`_ `text` \[, _`formatarg`_ `"any"` \[, ...] ])                                   | `text`         | Format arguments according to a format string. This function is similar to the C function `sprintf`. See [Section 9.4.1](https://www.postgresql.org/docs/12/functions-string.html#FUNCTIONS-STRING-FORMAT).                                                                                                                                                                                                                                                                         | `format('Hello %s, %1$s', 'World')`              | `Hello World, World`                                        |
| `initcap(`_`string`_)                                                                                 | `text`         | Convert the first letter of each word to upper case and the rest to lower case. Words are sequences of alphanumeric characters separated by non-alphanumeric characters.                                                                                                                                                                                                                                                                                                            | `initcap('hi THOMAS')`                           | `Hi Thomas`                                                 |
| `left(`_`str`_ `text`, _`n`_ `int`)                                                                   | `text`         | Return first _`n`_ characters in the string. When _`n`_ is negative, return all but last \|_`n`_\| characters.                                                                                                                                                                                                                                                                                                                                                                      | `left('abcde', 2)`                               | `ab`                                                        |
| `length(`_`string`_)                                                                                  | `int`          | Number of characters in _`string`_                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `length('jose')`                                 | `4`                                                         |
| `length(`_`string`_ `bytea`, _`encoding`_ `name` )                                                    | `int`          | Number of characters in _`string`_ in the given _`encoding`_. The _`string`_ must be valid in this encoding.                                                                                                                                                                                                                                                                                                                                                                        | `length('jose', 'UTF8')`                         | `4`                                                         |
| `lpad(`_`string`_ `text`, _`length`_ `int` \[, _`fill`_ `text`])                                      | `text`         | Fill up the _`string`_ to length _`length`_ by prepending the characters _`fill`_ (a space by default). If the _`string`_ is already longer than _`length`_ then it is truncated (on the right).                                                                                                                                                                                                                                                                                    | `lpad('hi', 5, 'xy')`                            | `xyxhi`                                                     |
| `ltrim(`_`string`_ `text` \[, _`characters`_ `text`])                                                 | `text`         | Remove the longest string containing only characters from _`characters`_ (a space by default) from the start of _`string`_                                                                                                                                                                                                                                                                                                                                                          | `ltrim('zzzytest', 'xyz')`                       | `test`                                                      |
| `md5(`_`string`_)                                                                                     | `text`         | Calculates the MD5 hash of _`string`_, returning the result in hexadecimal                                                                                                                                                                                                                                                                                                                                                                                                          | `md5('abc')`                                     | `900150983cd24fb0 d6963f7d28e17f72`                         |
| `parse_ident(`_`qualified_identifier`_ `text` \[, _`strictmode`_ `boolean` DEFAULT true ] )           | `text[]`       | Split _`qualified_identifier`_ into an array of identifiers, removing any quoting of individual identifiers. By default, extra characters after the last identifier are considered an error; but if the second parameter is `false`, then such extra characters are ignored. (This behavior is useful for parsing names for objects like functions.) Note that this function does not truncate over-length identifiers. If you want truncation you can cast the result to `name[]`. | `parse_ident('"SomeSchema".someTable')`          | `{SomeSchema,sometable}`                                    |
| `pg_client_encoding()`                                                                                | `name`         | Current client encoding name                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `pg_client_encoding()`                           | `SQL_ASCII`                                                 |
| `quote_ident(`_`string`_ `text`)                                                                      | `text`         | Return the given string suitably quoted to be used as an identifier in an SQL statement string. Quotes are added only if necessary (i.e., if the string contains non-identifier characters or would be case-folded). Embedded quotes are properly doubled. See also [Example 42.1](https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE).                                                                                                       | `quote_ident('Foo bar')`                         | `"Foo bar"`                                                 |
| `quote_literal(`_`string`_ `text`)                                                                    | `text`         | Return the given string suitably quoted to be used as a string literal in an SQL statement string. Embedded single-quotes and backslashes are properly doubled. Note that `quote_literal` returns null on null input; if the argument might be null, `quote_nullable` is often more suitable. See also [Example 42.1](https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE).                                                                    | `quote_literal(E'O\'Reilly')`                    | `'O''Reilly'`                                               |
| `quote_literal(`_`value`_ `anyelement`)                                                               | `text`         | Coerce the given value to text and then quote it as a literal. Embedded single-quotes and backslashes are properly doubled.                                                                                                                                                                                                                                                                                                                                                         | `quote_literal(42.5)`                            | `'42.5'`                                                    |
| `quote_nullable(`_`string`_ `text`)                                                                   | `text`         | Return the given string suitably quoted to be used as a string literal in an SQL statement string; or, if the argument is null, return `NULL`. Embedded single-quotes and backslashes are properly doubled. See also [Example 42.1](https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE).                                                                                                                                                      | `quote_nullable(NULL)`                           | `NULL`                                                      |
| `quote_nullable(`_`value`_ `anyelement`)                                                              | `text`         | Coerce the given value to text and then quote it as a literal; or, if the argument is null, return `NULL`. Embedded single-quotes and backslashes are properly doubled.                                                                                                                                                                                                                                                                                                             | `quote_nullable(42.5)`                           | `'42.5'`                                                    |
| `regexp_match(`_`string`_ `text`, _`pattern`_ `text` \[, _`flags`_ `text`])                           | `text[]`       | Return captured substring(s) resulting from the first match of a POSIX regular expression to the _`string`_. See [Section 9.7.3](https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP) for more information.                                                                                                                                                                                                                                           | `regexp_match('foobarbequebaz', '(bar)(beque)')` | `{bar,beque}`                                               |
| `regexp_matches(`_`string`_ `text`, _`pattern`_ `text` \[, _`flags`_ `text`])                         | `setof text[]` | Return captured substring(s) resulting from matching a POSIX regular expression to the _`string`_. See [Section 9.7.3](https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP) for more information.                                                                                                                                                                                                                                                     | `regexp_matches('foobarbequebaz', 'ba.', 'g')`   | <p><code>{bar}</code></p><p><code>{baz}</code>(2 rows)</p>  |
| `regexp_replace(`_`string`_ `text`, _`pattern`_ `text`, _`replacement`_ `text` \[, _`flags`_ `text`]) | `text`         | Replace substring(s) matching a POSIX regular expression. See [Section 9.7.3](https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP) for more information.                                                                                                                                                                                                                                                                                              | `regexp_replace('Thomas', '.[mN]a.', 'M')`       | `ThM`                                                       |
| `regexp_split_to_array(`_`string`_ `text`, _`pattern`_ `text` \[, _`flags`_ `text` ])                 | `text[]`       | Split _`string`_ using a POSIX regular expression as the delimiter. See [Section 9.7.3](https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP) for more information.                                                                                                                                                                                                                                                                                    | `regexp_split_to_array('hello world', '\s+')`    | `{hello,world}`                                             |
| `regexp_split_to_table(`_`string`_ `text`, _`pattern`_ `text` \[, _`flags`_ `text`])                  | `setof text`   | Split _`string`_ using a POSIX regular expression as the delimiter. See [Section 9.7.3](https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP) for more information.                                                                                                                                                                                                                                                                                    | `regexp_split_to_table('hello world', '\s+')`    | <p><code>hello</code></p><p><code>world</code>(2 rows)</p>  |
| `repeat(`_`string`_ `text`, _`number`_ `int`)                                                         | `text`         | Repeat _`string`_ the specified _`number`_ of times                                                                                                                                                                                                                                                                                                                                                                                                                                 | `repeat('Pg', 4)`                                | `PgPgPgPg`                                                  |
| `replace(`_`string`_ `text`, _`from`_ `text`, _`to`_ `text`)                                          | `text`         | Replace all occurrences in _`string`_ of substring _`from`_ with substring _`to`_                                                                                                                                                                                                                                                                                                                                                                                                   | `replace('abcdefabcdef', 'cd', 'XX')`            | `abXXefabXXef`                                              |
| `reverse(`_`str`_)                                                                                    | `text`         | Return reversed string.                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `reverse('abcde')`                               | `edcba`                                                     |
| `right(`_`str`_ `text`, _`n`_ `int`)                                                                  | `text`         | Return last _`n`_ characters in the string. When _`n`_ is negative, return all but first \|_`n`_\| characters.                                                                                                                                                                                                                                                                                                                                                                      | `right('abcde', 2)`                              | `de`                                                        |
| `rpad(`_`string`_ `text`, _`length`_ `int` \[, _`fill`_ `text`])                                      | `text`         | Fill up the _`string`_ to length _`length`_ by appending the characters _`fill`_ (a space by default). If the _`string`_ is already longer than _`length`_ then it is truncated.                                                                                                                                                                                                                                                                                                    | `rpad('hi', 5, 'xy')`                            | `hixyx`                                                     |
| `rtrim(`_`string`_ `text` \[, _`characters`_ `text`])                                                 | `text`         | Remove the longest string containing only characters from _`characters`_ (a space by default) from the end of _`string`_                                                                                                                                                                                                                                                                                                                                                            | `rtrim('testxxzx', 'xyz')`                       | `test`                                                      |
| `split_part(`_`string`_ `text`, _`delimiter`_ `text`, _`field`_ `int`)                                | `text`         | Split _`string`_ on _`delimiter`_ and return the given field (counting from one)                                                                                                                                                                                                                                                                                                                                                                                                    | `split_part('abc~@~def~@~ghi', '~@~', 2)`        | `def`                                                       |
| `strpos(`_`string`_, _`substring`_)                                                                   | `int`          | Location of specified substring (same as `position(`_`substring`_ in _`string`_), but note the reversed argument order)                                                                                                                                                                                                                                                                                                                                                             | `strpos('high', 'ig')`                           | `2`                                                         |
| `substr(`_`string`_, _`from`_ \[, _`count`_])                                                         | `text`         | 回傳子字串（與 substring(`string` from `from` for `count`) 相同）                                                                                                                                                                                                                                                                                                                                                                                                                             | `substr('alphabet', 3, 2)`                       | `ph`                                                        |
| `starts_with(`_`string`_, _`prefix`_)                                                                 | `bool`         | Returns true if _`string`_ starts with _`prefix`_.                                                                                                                                                                                                                                                                                                                                                                                                                                  | `starts_with('alphabet', 'alph')`                | `t`                                                         |
| `to_ascii(`_`string`_ `text` \[, _`encoding`_ `text`])                                                | `text`         | Convert _`string`_ to ASCII from another encoding (only supports conversion from `LATIN1`, `LATIN2`, `LATIN9`, and `WIN1250` encodings)                                                                                                                                                                                                                                                                                                                                             | `to_ascii('Karel')`                              | `Karel`                                                     |
| `to_hex(`_`number`_ `int` or `bigint`)                                                                | `text`         | Convert _`number`_ to its equivalent hexadecimal representation                                                                                                                                                                                                                                                                                                                                                                                                                     | `to_hex(2147483647)`                             | `7fffffff`                                                  |
| `translate(`_`string`_ `text`, _`from`_ `text`, _`to`_ `text`)                                        | `text`         | Any character in _`string`_ that matches a character in the _`from`_ set is replaced by the corresponding character in the _`to`_ set. If _`from`_ is longer than _`to`_, occurrences of the extra characters in _`from`_ are removed.                                                                                                                                                                                                                                              | `translate('12345', '143', 'ax')`                | `a2x5`                                                      |

concat、concat\_ws 和 format 函數是動態參數，因此可以將要連接或格式化的值以 VARIADIC 關鍵字標記的陣列（請參閱[第 37.5.5 節](../../server-programming/extending-sql/query-language-sql-functions.md#37-5-5-sql-functions-with-variable-numbers-of-arguments)）輸入。 將陣列的元素視為函數的一個普通參數。如果動態參數陣列參數為 NULL，則 concat 和 concat\_ws 回傳 NULL，但是 format 將 NULL 視為零元素陣列。

另請參閱[第 9.20 節](aggregate-functions.md)中的彙總函數 string\_agg。

#### **Table 9.11. Built-in Conversions**

| Conversion Name                  | Source Encoding  | Destination Encoding |
| -------------------------------- | ---------------- | -------------------- |
| `ascii_to_mic`                   | `SQL_ASCII`      | `MULE_INTERNAL`      |
| `ascii_to_utf8`                  | `SQL_ASCII`      | `UTF8`               |
| `big5_to_euc_tw`                 | `BIG5`           | `EUC_TW`             |
| `big5_to_mic`                    | `BIG5`           | `MULE_INTERNAL`      |
| `big5_to_utf8`                   | `BIG5`           | `UTF8`               |
| `euc_cn_to_mic`                  | `EUC_CN`         | `MULE_INTERNAL`      |
| `euc_cn_to_utf8`                 | `EUC_CN`         | `UTF8`               |
| `euc_jp_to_mic`                  | `EUC_JP`         | `MULE_INTERNAL`      |
| `euc_jp_to_sjis`                 | `EUC_JP`         | `SJIS`               |
| `euc_jp_to_utf8`                 | `EUC_JP`         | `UTF8`               |
| `euc_kr_to_mic`                  | `EUC_KR`         | `MULE_INTERNAL`      |
| `euc_kr_to_utf8`                 | `EUC_KR`         | `UTF8`               |
| `euc_tw_to_big5`                 | `EUC_TW`         | `BIG5`               |
| `euc_tw_to_mic`                  | `EUC_TW`         | `MULE_INTERNAL`      |
| `euc_tw_to_utf8`                 | `EUC_TW`         | `UTF8`               |
| `gb18030_to_utf8`                | `GB18030`        | `UTF8`               |
| `gbk_to_utf8`                    | `GBK`            | `UTF8`               |
| `iso_8859_10_to_utf8`            | `LATIN6`         | `UTF8`               |
| `iso_8859_13_to_utf8`            | `LATIN7`         | `UTF8`               |
| `iso_8859_14_to_utf8`            | `LATIN8`         | `UTF8`               |
| `iso_8859_15_to_utf8`            | `LATIN9`         | `UTF8`               |
| `iso_8859_16_to_utf8`            | `LATIN10`        | `UTF8`               |
| `iso_8859_1_to_mic`              | `LATIN1`         | `MULE_INTERNAL`      |
| `iso_8859_1_to_utf8`             | `LATIN1`         | `UTF8`               |
| `iso_8859_2_to_mic`              | `LATIN2`         | `MULE_INTERNAL`      |
| `iso_8859_2_to_utf8`             | `LATIN2`         | `UTF8`               |
| `iso_8859_2_to_windows_1250`     | `LATIN2`         | `WIN1250`            |
| `iso_8859_3_to_mic`              | `LATIN3`         | `MULE_INTERNAL`      |
| `iso_8859_3_to_utf8`             | `LATIN3`         | `UTF8`               |
| `iso_8859_4_to_mic`              | `LATIN4`         | `MULE_INTERNAL`      |
| `iso_8859_4_to_utf8`             | `LATIN4`         | `UTF8`               |
| `iso_8859_5_to_koi8_r`           | `ISO_8859_5`     | `KOI8R`              |
| `iso_8859_5_to_mic`              | `ISO_8859_5`     | `MULE_INTERNAL`      |
| `iso_8859_5_to_utf8`             | `ISO_8859_5`     | `UTF8`               |
| `iso_8859_5_to_windows_1251`     | `ISO_8859_5`     | `WIN1251`            |
| `iso_8859_5_to_windows_866`      | `ISO_8859_5`     | `WIN866`             |
| `iso_8859_6_to_utf8`             | `ISO_8859_6`     | `UTF8`               |
| `iso_8859_7_to_utf8`             | `ISO_8859_7`     | `UTF8`               |
| `iso_8859_8_to_utf8`             | `ISO_8859_8`     | `UTF8`               |
| `iso_8859_9_to_utf8`             | `LATIN5`         | `UTF8`               |
| `johab_to_utf8`                  | `JOHAB`          | `UTF8`               |
| `koi8_r_to_iso_8859_5`           | `KOI8R`          | `ISO_8859_5`         |
| `koi8_r_to_mic`                  | `KOI8R`          | `MULE_INTERNAL`      |
| `koi8_r_to_utf8`                 | `KOI8R`          | `UTF8`               |
| `koi8_r_to_windows_1251`         | `KOI8R`          | `WIN1251`            |
| `koi8_r_to_windows_866`          | `KOI8R`          | `WIN866`             |
| `koi8_u_to_utf8`                 | `KOI8U`          | `UTF8`               |
| `mic_to_ascii`                   | `MULE_INTERNAL`  | `SQL_ASCII`          |
| `mic_to_big5`                    | `MULE_INTERNAL`  | `BIG5`               |
| `mic_to_euc_cn`                  | `MULE_INTERNAL`  | `EUC_CN`             |
| `mic_to_euc_jp`                  | `MULE_INTERNAL`  | `EUC_JP`             |
| `mic_to_euc_kr`                  | `MULE_INTERNAL`  | `EUC_KR`             |
| `mic_to_euc_tw`                  | `MULE_INTERNAL`  | `EUC_TW`             |
| `mic_to_iso_8859_1`              | `MULE_INTERNAL`  | `LATIN1`             |
| `mic_to_iso_8859_2`              | `MULE_INTERNAL`  | `LATIN2`             |
| `mic_to_iso_8859_3`              | `MULE_INTERNAL`  | `LATIN3`             |
| `mic_to_iso_8859_4`              | `MULE_INTERNAL`  | `LATIN4`             |
| `mic_to_iso_8859_5`              | `MULE_INTERNAL`  | `ISO_8859_5`         |
| `mic_to_koi8_r`                  | `MULE_INTERNAL`  | `KOI8R`              |
| `mic_to_sjis`                    | `MULE_INTERNAL`  | `SJIS`               |
| `mic_to_windows_1250`            | `MULE_INTERNAL`  | `WIN1250`            |
| `mic_to_windows_1251`            | `MULE_INTERNAL`  | `WIN1251`            |
| `mic_to_windows_866`             | `MULE_INTERNAL`  | `WIN866`             |
| `sjis_to_euc_jp`                 | `SJIS`           | `EUC_JP`             |
| `sjis_to_mic`                    | `SJIS`           | `MULE_INTERNAL`      |
| `sjis_to_utf8`                   | `SJIS`           | `UTF8`               |
| `windows_1258_to_utf8`           | `WIN1258`        | `UTF8`               |
| `uhc_to_utf8`                    | `UHC`            | `UTF8`               |
| `utf8_to_ascii`                  | `UTF8`           | `SQL_ASCII`          |
| `utf8_to_big5`                   | `UTF8`           | `BIG5`               |
| `utf8_to_euc_cn`                 | `UTF8`           | `EUC_CN`             |
| `utf8_to_euc_jp`                 | `UTF8`           | `EUC_JP`             |
| `utf8_to_euc_kr`                 | `UTF8`           | `EUC_KR`             |
| `utf8_to_euc_tw`                 | `UTF8`           | `EUC_TW`             |
| `utf8_to_gb18030`                | `UTF8`           | `GB18030`            |
| `utf8_to_gbk`                    | `UTF8`           | `GBK`                |
| `utf8_to_iso_8859_1`             | `UTF8`           | `LATIN1`             |
| `utf8_to_iso_8859_10`            | `UTF8`           | `LATIN6`             |
| `utf8_to_iso_8859_13`            | `UTF8`           | `LATIN7`             |
| `utf8_to_iso_8859_14`            | `UTF8`           | `LATIN8`             |
| `utf8_to_iso_8859_15`            | `UTF8`           | `LATIN9`             |
| `utf8_to_iso_8859_16`            | `UTF8`           | `LATIN10`            |
| `utf8_to_iso_8859_2`             | `UTF8`           | `LATIN2`             |
| `utf8_to_iso_8859_3`             | `UTF8`           | `LATIN3`             |
| `utf8_to_iso_8859_4`             | `UTF8`           | `LATIN4`             |
| `utf8_to_iso_8859_5`             | `UTF8`           | `ISO_8859_5`         |
| `utf8_to_iso_8859_6`             | `UTF8`           | `ISO_8859_6`         |
| `utf8_to_iso_8859_7`             | `UTF8`           | `ISO_8859_7`         |
| `utf8_to_iso_8859_8`             | `UTF8`           | `ISO_8859_8`         |
| `utf8_to_iso_8859_9`             | `UTF8`           | `LATIN5`             |
| `utf8_to_johab`                  | `UTF8`           | `JOHAB`              |
| `utf8_to_koi8_r`                 | `UTF8`           | `KOI8R`              |
| `utf8_to_koi8_u`                 | `UTF8`           | `KOI8U`              |
| `utf8_to_sjis`                   | `UTF8`           | `SJIS`               |
| `utf8_to_windows_1258`           | `UTF8`           | `WIN1258`            |
| `utf8_to_uhc`                    | `UTF8`           | `UHC`                |
| `utf8_to_windows_1250`           | `UTF8`           | `WIN1250`            |
| `utf8_to_windows_1251`           | `UTF8`           | `WIN1251`            |
| `utf8_to_windows_1252`           | `UTF8`           | `WIN1252`            |
| `utf8_to_windows_1253`           | `UTF8`           | `WIN1253`            |
| `utf8_to_windows_1254`           | `UTF8`           | `WIN1254`            |
| `utf8_to_windows_1255`           | `UTF8`           | `WIN1255`            |
| `utf8_to_windows_1256`           | `UTF8`           | `WIN1256`            |
| `utf8_to_windows_1257`           | `UTF8`           | `WIN1257`            |
| `utf8_to_windows_866`            | `UTF8`           | `WIN866`             |
| `utf8_to_windows_874`            | `UTF8`           | `WIN874`             |
| `windows_1250_to_iso_8859_2`     | `WIN1250`        | `LATIN2`             |
| `windows_1250_to_mic`            | `WIN1250`        | `MULE_INTERNAL`      |
| `windows_1250_to_utf8`           | `WIN1250`        | `UTF8`               |
| `windows_1251_to_iso_8859_5`     | `WIN1251`        | `ISO_8859_5`         |
| `windows_1251_to_koi8_r`         | `WIN1251`        | `KOI8R`              |
| `windows_1251_to_mic`            | `WIN1251`        | `MULE_INTERNAL`      |
| `windows_1251_to_utf8`           | `WIN1251`        | `UTF8`               |
| `windows_1251_to_windows_866`    | `WIN1251`        | `WIN866`             |
| `windows_1252_to_utf8`           | `WIN1252`        | `UTF8`               |
| `windows_1256_to_utf8`           | `WIN1256`        | `UTF8`               |
| `windows_866_to_iso_8859_5`      | `WIN866`         | `ISO_8859_5`         |
| `windows_866_to_koi8_r`          | `WIN866`         | `KOI8R`              |
| `windows_866_to_mic`             | `WIN866`         | `MULE_INTERNAL`      |
| `windows_866_to_utf8`            | `WIN866`         | `UTF8`               |
| `windows_866_to_windows_1251`    | `WIN866`         | `WIN`                |
| `windows_874_to_utf8`            | `WIN874`         | `UTF8`               |
| `euc_jis_2004_to_utf8`           | `EUC_JIS_2004`   | `UTF8`               |
| `utf8_to_euc_jis_2004`           | `UTF8`           | `EUC_JIS_2004`       |
| `shift_jis_2004_to_utf8`         | `SHIFT_JIS_2004` | `UTF8`               |
| `utf8_to_shift_jis_2004`         | `UTF8`           | `SHIFT_JIS_2004`     |
| `euc_jis_2004_to_shift_jis_2004` | `EUC_JIS_2004`   | `SHIFT_JIS_2004`     |
| `shift_jis_2004_to_euc_jis_2004` | `SHIFT_JIS_2004` | `EUC_JIS_2004`       |

{% hint style="info" %}
轉換名稱遵循標準的命名規則：來源編碼的正式名稱，所有非字母數字字元均用下底線代替，接在 \_to\_\_\_ 之後，然後是經過類似處理的目標編碼名稱。因此，名稱可能與習慣的編碼名稱有所不同。
{% endhint %}

## 9.4.1. `format`

The function `format` produces output formatted according to a format string, in a style similar to the C function `sprintf`.

```
format(formatstr text [, formatarg "any" [, ...] ])
```

_`formatstr`_ is a format string that specifies how the result should be formatted. Text in the format string is copied directly to the result, except where _format specifiers_ are used. Format specifiers act as placeholders in the string, defining how subsequent function arguments should be formatted and inserted into the result. Each _`formatarg`_ argument is converted to text according to the usual output rules for its data type, and then formatted and inserted into the result string according to the format specifier(s).

Format specifiers are introduced by a `%` character and have the form

```
%[position][flags][width]type
```

where the component fields are:_`position`_ (optional)

A string of the form _`n`_$ where _`n`_ is the index of the argument to print. Index 1 means the first argument after _`formatstr`_. If the _`position`_ is omitted, the default is to use the next argument in sequence._`flags`_ (optional)

Additional options controlling how the format specifier's output is formatted. Currently the only supported flag is a minus sign (`-`) which will cause the format specifier's output to be left-justified. This has no effect unless the _`width`_ field is also specified._`width`_ (optional)

Specifies the _minimum_ number of characters to use to display the format specifier's output. The output is padded on the left or right (depending on the `-` flag) with spaces as needed to fill the width. A too-small width does not cause truncation of the output, but is simply ignored. The width may be specified using any of the following: a positive integer; an asterisk (`*`) to use the next function argument as the width; or a string of the form `*`_`n`_$ to use the \_`n`\_th function argument as the width.

If the width comes from a function argument, that argument is consumed before the argument that is used for the format specifier's value. If the width argument is negative, the result is left aligned (as if the `-` flag had been specified) within a field of length `abs`(_`width`_)._`type`_ (required)

The type of format conversion to use to produce the format specifier's output. The following types are supported:

* `s` formats the argument value as a simple string. A null value is treated as an empty string.
* `I` treats the argument value as an SQL identifier, double-quoting it if necessary. It is an error for the value to be null (equivalent to `quote_ident`).
* `L` quotes the argument value as an SQL literal. A null value is displayed as the string `NULL`, without quotes (equivalent to `quote_nullable`).

In addition to the format specifiers described above, the special sequence `%%` may be used to output a literal `%` character.

Here are some examples of the basic format conversions:

```
SELECT format('Hello %s', 'World');
Result: Hello World

SELECT format('Testing %s, %s, %s, %%', 'one', 'two', 'three');
Result: Testing one, two, three, %

SELECT format('INSERT INTO %I VALUES(%L)', 'Foo bar', E'O\'Reilly');
Result: INSERT INTO "Foo bar" VALUES('O''Reilly')

SELECT format('INSERT INTO %I VALUES(%L)', 'locations', 'C:\Program Files');
Result: INSERT INTO locations VALUES('C:\Program Files')
```

Here are examples using _`width`_ fields and the `-` flag:

```
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

These examples show use of _`position`_ fields:

```
SELECT format('Testing %3$s, %2$s, %1$s', 'one', 'two', 'three');
Result: Testing three, two, one

SELECT format('|%*2$s|', 'foo', 10, 'bar');
Result: |       bar|

SELECT format('|%1$*2$s|', 'foo', 10, 'bar');
Result: |       foo|
```

Unlike the standard C function `sprintf`, PostgreSQL's `format` function allows format specifiers with and without _`position`_ fields to be mixed in the same format string. A format specifier without a _`position`_ field always uses the next argument after the last argument consumed. In addition, the `format` function does not require all function arguments to be used in the format string. For example:

```
SELECT format('Testing %3$s, %2$s, %s', 'one', 'two', 'three');
Result: Testing three, two, three
```

The `%I` and `%L` format specifiers are particularly useful for safely constructing dynamic SQL statements. See [Example 42.1](https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE).
