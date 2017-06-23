# 9.4. 字串函式及運算子[^1]

This section describes functions and operators for examining and manipulating string values. Strings in this context include values of the types`character`,`character varying`, and`text`. Unless otherwise noted, all of the functions listed below work on all of these types, but be wary of potential effects of automatic space-padding when using the`character`type. Some functions also exist natively for the bit-string types.

SQLdefines some string functions that use key words, rather than commas, to separate arguments. Details are in[Table 9.8](https://www.postgresql.org/docs/10/static/functions-string.html#functions-string-sql).PostgreSQLalso provides versions of these functions that use the regular function invocation syntax \(see[Table 9.9](https://www.postgresql.org/docs/10/static/functions-string.html#functions-string-other)\).

### Note

BeforePostgreSQL8.3, these functions would silently accept values of several non-string data types as well, due to the presence of implicit coercions from those data types to`text`. Those coercions have been removed because they frequently caused surprising behaviors. However, the string concatenation operator \(`||`\) still accepts non-string input, so long as at least one input is of a string type, as shown in[Table 9.8](https://www.postgresql.org/docs/10/static/functions-string.html#functions-string-sql). For other cases, insert an explicit coercion to`text`if you need to duplicate the previous behavior.

**Table 9.8. SQLString Functions and Operators**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| _`string`_`||`_`string`_ | `text` | String concatenation | `'Post' || 'greSQL'` | `PostgreSQL` |
| _`string`_`||`_`non-string`_or_`non-string`_`||`_`string`_ | `text` | String concatenation with one non-string input | `'Value: ' || 42` | `Value: 42` |
| `bit_length(`_`string`_\) | `int` | Number of bits in string | `bit_length('jose')` | `32` |
| `char_length(`_`string`_\)or`character_length(`_`string`_\) | `int` | Number of characters in string | `char_length('jose')` | `4` |
| `lower(`_`string`_\) | `text` | Convert string to lower case | `lower('TOM')` | `tom` |
| `octet_length(`_`string`_\) | `int` | Number of bytes in string | `octet_length('jose')` | `4` |
| `overlay(`_`string`_placing_`string`_from`int`\[for`int`\]\) | `text` | Replace substring | `overlay('Txxxxas' placing 'hom' from 2 for 4)` | `Thomas` |
| `position(`_`substring`_in_`string`_\) | `int` | Location of specified substring | `position('om' in 'Thomas')` | `3` |
| `substring(`_`string`_\[from`int`\] \[for`int`\]\) | `text` | Extract substring | `substring('Thomas' from 2 for 3)` | `hom` |
| `substring(`_`string`_from_`pattern`_\) | `text` | Extract substring matching POSIX regular expression. See[Section 9.7](https://www.postgresql.org/docs/10/static/functions-matching.html)for more information on pattern matching. | `substring('Thomas' from '...$')` | `mas` |
| `substring(`_`string`_from_`pattern`_for_`escape`_\) | `text` | Extract substring matchingSQLregular expression. See[Section 9.7](https://www.postgresql.org/docs/10/static/functions-matching.html)for more information on pattern matching. | `substring('Thomas' from '%#"o_a#"_' for '#')` | `oma` |
| `trim([leading | trailing | both] [`_`characters`_\] from_`string`_\) | `text` | Remove the longest string containing only characters from_`characters`_\(a space by default\) from the start, end, or both ends \(`both`is the default\) of_`string`_ | `trim(both 'xyz' from 'yxTomxx')` | `Tom` |
| `trim([leading | trailing | both] [from]`_`string`_\[,_`characters`_\] \) | `text` | Non-standard syntax for`trim()` | `trim(both from 'yxTomxx', 'xyz')` | `Tom` |
| `upper(`_`string`_\) | `text` | Convert string to upper case | `upper('tom')` | `TOM` |

  


Additional string manipulation functions are available and are listed in[Table 9.9](https://www.postgresql.org/docs/10/static/functions-string.html#functions-string-other). Some of them are used internally to implement theSQL-standard string functions listed in[Table 9.8](https://www.postgresql.org/docs/10/static/functions-string.html#functions-string-sql).

**Table 9.9. Other String Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `ascii(`_`string`_\) | `int` | ASCIIcode of the first character of the argument. ForUTF8returns the Unicode code point of the character. For other multibyte encodings, the argument must be anASCIIcharacter. | `ascii('x')` | `120` |
| `btrim(`_`string`_`text`\[,_`characters`_`text`\]\) | `text` | Remove the longest string consisting only of characters in_`characters`_\(a space by default\) from the start and end of_`string`_ | `btrim('xyxtrimyyx', 'xyz')` | `trim` |
| `chr(int`\) | `text` | Character with the given code. ForUTF8the argument is treated as a Unicode code point. For other multibyte encodings the argument must designate anASCIIcharacter. The NULL \(0\) character is not allowed because text data types cannot store such bytes. | `chr(65)` | `A` |
| `concat(`_`str`_`"any"`\[,_`str`_`"any"`\[, ...\] \]\) | `text` | Concatenate the text representations of all the arguments. NULL arguments are ignored. | `concat('abcde', 2, NULL, 22)` | `abcde222` |
| `concat_ws(`_`sep`_`text`,_`str`_`"any"`\[,_`str`_`"any"`\[, ...\] \]\) | `text` | Concatenate all but the first argument with separators. The first argument is used as the separator string. NULL arguments are ignored. | `concat_ws(',', 'abcde', 2, NULL, 22)` | `abcde,2,22` |
| `convert(`_`string`_`bytea`,_`src_encoding`_`name`,_`dest_encoding`_`name`\) | `bytea` | Convert string to_`dest_encoding`_. The original encoding is specified by_`src_encoding`_. The_`string`_must be valid in this encoding. Conversions can be defined by`CREATE CONVERSION`. Also there are some predefined conversions. See[Table 9.10](https://www.postgresql.org/docs/10/static/functions-string.html#conversion-names)for available conversions. | `convert('text_in_utf8', 'UTF8', 'LATIN1')` | `text_in_utf8`represented in Latin-1 encoding \(ISO 8859-1\) |
| `convert_from(`_`string`_`bytea`,_`src_encoding`_`name`\) | `text` | Convert string to the database encoding. The original encoding is specified by_`src_encoding`_. The_`string`_must be valid in this encoding. | `convert_from('text_in_utf8', 'UTF8')` | `text_in_utf8`represented in the current database encoding |
| `convert_to(`_`string`_`text`,_`dest_encoding`_`name`\) | `bytea` | Convert string to_`dest_encoding`_. | `convert_to('some text', 'UTF8')` | `some text`represented in the UTF8 encoding |
| `decode(`_`string`_`text`,_`format`_`text`\) | `bytea` | Decode binary data from textual representation in_`string`_. Options for_`format`_are same as in`encode`. | `decode('MTIzAAE=', 'base64')` | `\x3132330001` |
| `encode(`_`data`_`bytea`,_`format`_`text`\) | `text` | Encode binary data into a textual representation. Supported formats are:`base64`,`hex`,`escape`.`escape`converts zero bytes and high-bit-set bytes to octal sequences \(`\`_`nnn`_\) and doubles backslashes. | `encode(E'123\\000\\001', 'base64')` | `MTIzAAE=` |
| `format`\(_`formatstr`_`text`\[,_`formatarg`_`"any"`\[, ...\] \]\) | `text` | Format arguments according to a format string. This function is similar to the C function`sprintf`. See[Section 9.4.1](https://www.postgresql.org/docs/10/static/functions-string.html#functions-string-format). | `format('Hello %s, %1$s', 'World')` | `Hello World, World` |
| `initcap(`_`string`_\) | `text` | Convert the first letter of each word to upper case and the rest to lower case. Words are sequences of alphanumeric characters separated by non-alphanumeric characters. | `initcap('hi THOMAS')` | `Hi Thomas` |
| `left(`_`str`_`text`,_`n`_`int`\) | `text` | Return first_`n`_characters in the string. When_`n`_is negative, return all but last \|_`n`_\| characters. | `left('abcde', 2)` | `ab` |
| `length(`_`string`_\) | `int` | Number of characters in_`string`_ | `length('jose')` | `4` |
| `length(`_`string`_`bytea`,_`encoding`_`name`\) | `int` | Number of characters in_`string`_in the given_`encoding`_. The_`string`_must be valid in this encoding. | `length('jose', 'UTF8')` | `4` |
| `lpad(`_`string`_`text`,_`length`_`int`\[,_`fill`_`text`\]\) | `text` | Fill up the_`string`_to length_`length`_by prepending the characters_`fill`_\(a space by default\). If the_`string`_is already longer than_`length`_then it is truncated \(on the right\). | `lpad('hi', 5, 'xy')` | `xyxhi` |
| `ltrim(`_`string`_`text`\[,_`characters`_`text`\]\) | `text` | Remove the longest string containing only characters from_`characters`_\(a space by default\) from the start of_`string`_ | `ltrim('zzzytest', 'xyz')` | `test` |
| `md5(`_`string`_\) | `text` | Calculates the MD5 hash of_`string`_, returning the result in hexadecimal | `md5('abc')` | `900150983cd24fb0 d6963f7d28e17f72` |
| `parse_ident(`_`qualified_identifier`_`text`\[,_`strictmode`_`boolean`DEFAULT true \] \) | `text[]` | Split_`qualified_identifier`_into an array of identifiers, removing any quoting of individual identifiers. By default, extra characters after the last identifier are considered an error; but if the second parameter is`false`, then such extra characters are ignored. \(This behavior is useful for parsing names for objects like functions.\) Note that this function does not truncate over-length identifiers. If you want truncation you can cast the result to`name[]`. | `parse_ident('"SomeSchema".someTable')` | `{SomeSchema,sometable}` |
| `pg_client_encoding()` | `name` | Current client encoding name | `pg_client_encoding()` | `SQL_ASCII` |
| `quote_ident(`_`string`_`text`\) | `text` | Return the given string suitably quoted to be used as an identifier in anSQLstatement string. Quotes are added only if necessary \(i.e., if the string contains non-identifier characters or would be case-folded\). Embedded quotes are properly doubled. See also[Example 42.1](https://www.postgresql.org/docs/10/static/plpgsql-statements.html#plpgsql-quote-literal-example). | `quote_ident('Foo bar')` | `"Foo bar"` |
| `quote_literal(`_`string`_`text`\) | `text` | Return the given string suitably quoted to be used as a string literal in anSQLstatement string. Embedded single-quotes and backslashes are properly doubled. Note that`quote_literal`returns null on null input; if the argument might be null,`quote_nullable`is often more suitable. See also[Example 42.1](https://www.postgresql.org/docs/10/static/plpgsql-statements.html#plpgsql-quote-literal-example). | `quote_literal(E'O\'Reilly')` | `'O''Reilly'` |
| `quote_literal(`_`value`_`anyelement`\) | `text` | Coerce the given value to text and then quote it as a literal. Embedded single-quotes and backslashes are properly doubled. | `quote_literal(42.5)` | `'42.5'` |
| `quote_nullable(`_`string`_`text`\) | `text` | Return the given string suitably quoted to be used as a string literal in anSQLstatement string; or, if the argument is null, return`NULL`. Embedded single-quotes and backslashes are properly doubled. See also[Example 42.1](https://www.postgresql.org/docs/10/static/plpgsql-statements.html#plpgsql-quote-literal-example). | `quote_nullable(NULL)` | `NULL` |
| `quote_nullable(`_`value`_`anyelement`\) | `text` | Coerce the given value to text and then quote it as a literal; or, if the argument is null, return`NULL`. Embedded single-quotes and backslashes are properly doubled. | `quote_nullable(42.5)` | `'42.5'` |
| `regexp_match(`_`string`_`text`,_`pattern`_`text`\[,_`flags`_`text`\]\) | `text[]` | Return captured substring\(s\) resulting from the first match of a POSIX regular expression to the_`string`_. See[Section 9.7.3](https://www.postgresql.org/docs/10/static/functions-matching.html#functions-posix-regexp)for more information. | `regexp_match('foobarbequebaz', '(bar)(beque)')` | `{bar,beque}` |
| `regexp_matches(`_`string`_`text`,_`pattern`_`text`\[,_`flags`_`text`\]\) | `setof text[]` | Return captured substring\(s\) resulting from matching a POSIX regular expression to the_`string`_. See[Section 9.7.3](https://www.postgresql.org/docs/10/static/functions-matching.html#functions-posix-regexp)for more information. | `regexp_matches('foobarbequebaz', 'ba.', 'g')` | `{bar}{baz}`\(2 rows\) |
| `regexp_replace(`_`string`_`text`,_`pattern`_`text`,_`replacement`_`text`\[,_`flags`_`text`\]\) | `text` | Replace substring\(s\) matching a POSIX regular expression. See[Section 9.7.3](https://www.postgresql.org/docs/10/static/functions-matching.html#functions-posix-regexp)for more information. | `regexp_replace('Thomas', '.[mN]a.', 'M')` | `ThM` |
| `regexp_split_to_array(`_`string`_`text`,_`pattern`_`text`\[,_`flags`_`text`\]\) | `text[]` | Split_`string`_using a POSIX regular expression as the delimiter. See[Section 9.7.3](https://www.postgresql.org/docs/10/static/functions-matching.html#functions-posix-regexp)for more information. | `regexp_split_to_array('hello world', E'\\s+')` | `{hello,world}` |
| `regexp_split_to_table(`_`string`_`text`,_`pattern`_`text`\[,_`flags`_`text`\]\) | `setof text` | Split_`string`_using a POSIX regular expression as the delimiter. See[Section 9.7.3](https://www.postgresql.org/docs/10/static/functions-matching.html#functions-posix-regexp)for more information. | `regexp_split_to_table('hello world', E'\\s+')` | `helloworld`\(2 rows\) |
| `repeat(`_`string`_`text`,_`number`_`int`\) | `text` | Repeat_`string`_the specified_`number`_of times | `repeat('Pg', 4)` | `PgPgPgPg` |
| `replace(`_`string`_`text`,_`from`_`text`,_`to`_`text`\) | `text` | Replace all occurrences in_`string`_of substring_`from`_with substring_`to`_ | `replace('abcdefabcdef', 'cd', 'XX')` | `abXXefabXXef` |
| `reverse(`_`str`_\) | `text` | Return reversed string. | `reverse('abcde')` | `edcba` |
| `right(`_`str`_`text`,_`n`_`int`\) | `text` | Return last_`n`_characters in the string. When_`n`_is negative, return all but first \|_`n`_\| characters. | `right('abcde', 2)` | `de` |
| `rpad(`_`string`_`text`,_`length`_`int`\[,_`fill`_`text`\]\) | `text` | Fill up the_`string`_to length_`length`_by appending the characters_`fill`_\(a space by default\). If the_`string`_is already longer than_`length`_then it is truncated. | `rpad('hi', 5, 'xy')` | `hixyx` |
| `rtrim(`_`string`_`text`\[,_`characters`_`text`\]\) | `text` | Remove the longest string containing only characters from_`characters`_\(a space by default\) from the end of_`string`_ | `rtrim('testxxzx', 'xyz')` | `test` |
| `split_part(`_`string`_`text`,_`delimiter`_`text`,_`field`_`int`\) | `text` | Split_`string`_on_`delimiter`_and return the given field \(counting from one\) | `split_part('abc~@~def~@~ghi', '~@~', 2)` | `def` |
| `strpos(`_`string`_,_`substring`_\) | `int` | Location of specified substring \(same as`position(`_`substring`_in_`string`_\), but note the reversed argument order\) | `strpos('high', 'ig')` | `2` |
| `substr(`_`string`_,_`from`_\[,_`count`_\]\) | `text` | Extract substring \(same as`substring(`_`string`_from_`from`_for_`count`_\)\) | `substr('alphabet', 3, 2)` | `ph` |
| `to_ascii(`_`string`_`text`\[,_`encoding`_`text`\]\) | `text` | Convert_`string`_toASCIIfrom another encoding \(only supports conversion from`LATIN1`,`LATIN2`,`LATIN9`, and`WIN1250`encodings\) | `to_ascii('Karel')` | `Karel` |
| `to_hex(`_`number`_`int`or`bigint`\) | `text` | Convert_`number`_to its equivalent hexadecimal representation | `to_hex(2147483647)` | `7fffffff` |
| `translate(`_`string`_`text`,_`from`_`text`,_`to`_`text`\) | `text` | Any character in_`string`_that matches a character in the_`from`_set is replaced by the corresponding character in the_`to`_set. If_`from`_is longer than_`to`_, occurrences of the extra characters in_`from`_are removed. | `translate('12345', '143', 'ax')` | `a2x5` |

  


The`concat`,`concat_ws`and`format`functions are variadic, so it is possible to pass the values to be concatenated or formatted as an array marked with the`VARIADIC`keyword \(see[Section 37.4.5](https://www.postgresql.org/docs/10/static/xfunc-sql.html#xfunc-sql-variadic-functions)\). The array's elements are treated as if they were separate ordinary arguments to the function. If the variadic array argument is NULL,`concat`and`concat_ws`return NULL, but`format`treats a NULL as a zero-element array.

See also the aggregate function`string_agg`in[Section 9.20](https://www.postgresql.org/docs/10/static/functions-aggregate.html).

**Table 9.10. Built-in Conversions**

| Conversion Name | [\[a\]](https://www.postgresql.org/docs/10/static/functions-string.html#ftn.idm46249855369248) | Source Encoding | Destination Encoding |
| :--- | :--- | :--- | :--- |
|  | `ascii_to_mic` | `SQL_ASCII` | `MULE_INTERNAL` |
|  | `ascii_to_utf8` | `SQL_ASCII` | `UTF8` |
|  | `big5_to_euc_tw` | `BIG5` | `EUC_TW` |
|  | `big5_to_mic` | `BIG5` | `MULE_INTERNAL` |
|  | `big5_to_utf8` | `BIG5` | `UTF8` |
|  | `euc_cn_to_mic` | `EUC_CN` | `MULE_INTERNAL` |
|  | `euc_cn_to_utf8` | `EUC_CN` | `UTF8` |
|  | `euc_jp_to_mic` | `EUC_JP` | `MULE_INTERNAL` |
|  | `euc_jp_to_sjis` | `EUC_JP` | `SJIS` |
|  | `euc_jp_to_utf8` | `EUC_JP` | `UTF8` |
|  | `euc_kr_to_mic` | `EUC_KR` | `MULE_INTERNAL` |
|  | `euc_kr_to_utf8` | `EUC_KR` | `UTF8` |
|  | `euc_tw_to_big5` | `EUC_TW` | `BIG5` |
|  | `euc_tw_to_mic` | `EUC_TW` | `MULE_INTERNAL` |
|  | `euc_tw_to_utf8` | `EUC_TW` | `UTF8` |
|  | `gb18030_to_utf8` | `GB18030` | `UTF8` |
|  | `gbk_to_utf8` | `GBK` | `UTF8` |
|  | `iso_8859_10_to_utf8` | `LATIN6` | `UTF8` |
|  | `iso_8859_13_to_utf8` | `LATIN7` | `UTF8` |
|  | `iso_8859_14_to_utf8` | `LATIN8` | `UTF8` |
|  | `iso_8859_15_to_utf8` | `LATIN9` | `UTF8` |
|  | `iso_8859_16_to_utf8` | `LATIN10` | `UTF8` |
|  | `iso_8859_1_to_mic` | `LATIN1` | `MULE_INTERNAL` |
|  | `iso_8859_1_to_utf8` | `LATIN1` | `UTF8` |
|  | `iso_8859_2_to_mic` | `LATIN2` | `MULE_INTERNAL` |
|  | `iso_8859_2_to_utf8` | `LATIN2` | `UTF8` |
|  | `iso_8859_2_to_windows_1250` | `LATIN2` | `WIN1250` |
|  | `iso_8859_3_to_mic` | `LATIN3` | `MULE_INTERNAL` |
|  | `iso_8859_3_to_utf8` | `LATIN3` | `UTF8` |
|  | `iso_8859_4_to_mic` | `LATIN4` | `MULE_INTERNAL` |
|  | `iso_8859_4_to_utf8` | `LATIN4` | `UTF8` |
|  | `iso_8859_5_to_koi8_r` | `ISO_8859_5` | `KOI8R` |
|  | `iso_8859_5_to_mic` | `ISO_8859_5` | `MULE_INTERNAL` |
|  | `iso_8859_5_to_utf8` | `ISO_8859_5` | `UTF8` |
|  | `iso_8859_5_to_windows_1251` | `ISO_8859_5` | `WIN1251` |
|  | `iso_8859_5_to_windows_866` | `ISO_8859_5` | `WIN866` |
|  | `iso_8859_6_to_utf8` | `ISO_8859_6` | `UTF8` |
|  | `iso_8859_7_to_utf8` | `ISO_8859_7` | `UTF8` |
|  | `iso_8859_8_to_utf8` | `ISO_8859_8` | `UTF8` |
|  | `iso_8859_9_to_utf8` | `LATIN5` | `UTF8` |
|  | `johab_to_utf8` | `JOHAB` | `UTF8` |
|  | `koi8_r_to_iso_8859_5` | `KOI8R` | `ISO_8859_5` |
|  | `koi8_r_to_mic` | `KOI8R` | `MULE_INTERNAL` |
|  | `koi8_r_to_utf8` | `KOI8R` | `UTF8` |
|  | `koi8_r_to_windows_1251` | `KOI8R` | `WIN1251` |
|  | `koi8_r_to_windows_866` | `KOI8R` | `WIN866` |
|  | `koi8_u_to_utf8` | `KOI8U` | `UTF8` |
|  | `mic_to_ascii` | `MULE_INTERNAL` | `SQL_ASCII` |
|  | `mic_to_big5` | `MULE_INTERNAL` | `BIG5` |
|  | `mic_to_euc_cn` | `MULE_INTERNAL` | `EUC_CN` |
|  | `mic_to_euc_jp` | `MULE_INTERNAL` | `EUC_JP` |
|  | `mic_to_euc_kr` | `MULE_INTERNAL` | `EUC_KR` |
|  | `mic_to_euc_tw` | `MULE_INTERNAL` | `EUC_TW` |
|  | `mic_to_iso_8859_1` | `MULE_INTERNAL` | `LATIN1` |
|  | `mic_to_iso_8859_2` | `MULE_INTERNAL` | `LATIN2` |
|  | `mic_to_iso_8859_3` | `MULE_INTERNAL` | `LATIN3` |
|  | `mic_to_iso_8859_4` | `MULE_INTERNAL` | `LATIN4` |
|  | `mic_to_iso_8859_5` | `MULE_INTERNAL` | `ISO_8859_5` |
|  | `mic_to_koi8_r` | `MULE_INTERNAL` | `KOI8R` |
|  | `mic_to_sjis` | `MULE_INTERNAL` | `SJIS` |
|  | `mic_to_windows_1250` | `MULE_INTERNAL` | `WIN1250` |
|  | `mic_to_windows_1251` | `MULE_INTERNAL` | `WIN1251` |
|  | `mic_to_windows_866` | `MULE_INTERNAL` | `WIN866` |
|  | `sjis_to_euc_jp` | `SJIS` | `EUC_JP` |
|  | `sjis_to_mic` | `SJIS` | `MULE_INTERNAL` |
|  | `sjis_to_utf8` | `SJIS` | `UTF8` |
|  | `tcvn_to_utf8` | `WIN1258` | `UTF8` |
|  | `uhc_to_utf8` | `UHC` | `UTF8` |
|  | `utf8_to_ascii` | `UTF8` | `SQL_ASCII` |
|  | `utf8_to_big5` | `UTF8` | `BIG5` |
|  | `utf8_to_euc_cn` | `UTF8` | `EUC_CN` |
|  | `utf8_to_euc_jp` | `UTF8` | `EUC_JP` |
|  | `utf8_to_euc_kr` | `UTF8` | `EUC_KR` |
|  | `utf8_to_euc_tw` | `UTF8` | `EUC_TW` |
|  | `utf8_to_gb18030` | `UTF8` | `GB18030` |
|  | `utf8_to_gbk` | `UTF8` | `GBK` |
|  | `utf8_to_iso_8859_1` | `UTF8` | `LATIN1` |
|  | `utf8_to_iso_8859_10` | `UTF8` | `LATIN6` |
|  | `utf8_to_iso_8859_13` | `UTF8` | `LATIN7` |
|  | `utf8_to_iso_8859_14` | `UTF8` | `LATIN8` |
|  | `utf8_to_iso_8859_15` | `UTF8` | `LATIN9` |
|  | `utf8_to_iso_8859_16` | `UTF8` | `LATIN10` |
|  | `utf8_to_iso_8859_2` | `UTF8` | `LATIN2` |
|  | `utf8_to_iso_8859_3` | `UTF8` | `LATIN3` |
|  | `utf8_to_iso_8859_4` | `UTF8` | `LATIN4` |
|  | `utf8_to_iso_8859_5` | `UTF8` | `ISO_8859_5` |
|  | `utf8_to_iso_8859_6` | `UTF8` | `ISO_8859_6` |
|  | `utf8_to_iso_8859_7` | `UTF8` | `ISO_8859_7` |
|  | `utf8_to_iso_8859_8` | `UTF8` | `ISO_8859_8` |
|  | `utf8_to_iso_8859_9` | `UTF8` | `LATIN5` |
|  | `utf8_to_johab` | `UTF8` | `JOHAB` |
|  | `utf8_to_koi8_r` | `UTF8` | `KOI8R` |
|  | `utf8_to_koi8_u` | `UTF8` | `KOI8U` |
|  | `utf8_to_sjis` | `UTF8` | `SJIS` |
|  | `utf8_to_tcvn` | `UTF8` | `WIN1258` |
|  | `utf8_to_uhc` | `UTF8` | `UHC` |
|  | `utf8_to_windows_1250` | `UTF8` | `WIN1250` |
|  | `utf8_to_windows_1251` | `UTF8` | `WIN1251` |
|  | `utf8_to_windows_1252` | `UTF8` | `WIN1252` |
|  | `utf8_to_windows_1253` | `UTF8` | `WIN1253` |
|  | `utf8_to_windows_1254` | `UTF8` | `WIN1254` |
|  | `utf8_to_windows_1255` | `UTF8` | `WIN1255` |
|  | `utf8_to_windows_1256` | `UTF8` | `WIN1256` |
|  | `utf8_to_windows_1257` | `UTF8` | `WIN1257` |
|  | `utf8_to_windows_866` | `UTF8` | `WIN866` |
|  | `utf8_to_windows_874` | `UTF8` | `WIN874` |
|  | `windows_1250_to_iso_8859_2` | `WIN1250` | `LATIN2` |
|  | `windows_1250_to_mic` | `WIN1250` | `MULE_INTERNAL` |
|  | `windows_1250_to_utf8` | `WIN1250` | `UTF8` |
|  | `windows_1251_to_iso_8859_5` | `WIN1251` | `ISO_8859_5` |
|  | `windows_1251_to_koi8_r` | `WIN1251` | `KOI8R` |
|  | `windows_1251_to_mic` | `WIN1251` | `MULE_INTERNAL` |
|  | `windows_1251_to_utf8` | `WIN1251` | `UTF8` |
|  | `windows_1251_to_windows_866` | `WIN1251` | `WIN866` |
|  | `windows_1252_to_utf8` | `WIN1252` | `UTF8` |
|  | `windows_1256_to_utf8` | `WIN1256` | `UTF8` |
|  | `windows_866_to_iso_8859_5` | `WIN866` | `ISO_8859_5` |
|  | `windows_866_to_koi8_r` | `WIN866` | `KOI8R` |
|  | `windows_866_to_mic` | `WIN866` | `MULE_INTERNAL` |
|  | `windows_866_to_utf8` | `WIN866` | `UTF8` |
|  | `windows_866_to_windows_1251` | `WIN866` | `WIN` |
|  | `windows_874_to_utf8` | `WIN874` | `UTF8` |
|  | `euc_jis_2004_to_utf8` | `EUC_JIS_2004` | `UTF8` |
|  | `utf8_to_euc_jis_2004` | `UTF8` | `EUC_JIS_2004` |
|  | `shift_jis_2004_to_utf8` | `SHIFT_JIS_2004` | `UTF8` |
|  | `utf8_to_shift_jis_2004` | `UTF8` | `SHIFT_JIS_2004` |
|  | `euc_jis_2004_to_shift_jis_2004` | `EUC_JIS_2004` | `SHIFT_JIS_2004` |
|  | `shift_jis_2004_to_euc_jis_2004` | `SHIFT_JIS_2004` | `EUC_JIS_2004` |
|  |  |  | [\[a\]](https://www.postgresql.org/docs/10/static/functions-string.html#idm46249855369248)The conversion names follow a standard naming scheme: The official name of the source encoding with all non-alphanumeric characters replaced by underscores, followed by`_to_`, followed by the similarly processed destination encoding name. Therefore, the names might deviate from the customary encoding names. |

  


### 9.4.1. `format`



The function`format`produces output formatted according to a format string, in a style similar to the C function`sprintf`.

```
format
(
formatstr
text
 [, 
formatarg
"any"
 [, ...] ])

```

_`formatstr`_is a format string that specifies how the result should be formatted. Text in the format string is copied directly to the result, except where_format specifiers_are used. Format specifiers act as placeholders in the string, defining how subsequent function arguments should be formatted and inserted into the result. Each_`formatarg`_argument is converted to text according to the usual output rules for its data type, and then formatted and inserted into the result string according to the format specifier\(s\).

Format specifiers are introduced by a`%`character and have the form

```
%[
position
][
flags
][
width
]
type
```

where the component fields are:

_`position`_

\(optional\)

A string of the form_`n`_$where_`n`_is the index of the argument to print. Index 1 means the first argument after_`formatstr`_. If the_`position`_is omitted, the default is to use the next argument in sequence.

_`flags`_

\(optional\)

Additional options controlling how the format specifier's output is formatted. Currently the only supported flag is a minus sign \(`-`\) which will cause the format specifier's output to be left-justified. This has no effect unless the_`width`_field is also specified.

_`width`_

\(optional\)

Specifies the_minimum_number of characters to use to display the format specifier's output. The output is padded on the left or right \(depending on the`-`flag\) with spaces as needed to fill the width. A too-small width does not cause truncation of the output, but is simply ignored. The width may be specified using any of the following: a positive integer; an asterisk \(`*`\) to use the next function argument as the width; or a string of the form`*`_`n`_$to use the_`n`_th function argument as the width.

If the width comes from a function argument, that argument is consumed before the argument that is used for the format specifier's value. If the width argument is negative, the result is left aligned \(as if the`-`flag had been specified\) within a field of length`abs`\(_`width`_\).

_`type`_

\(required\)

The type of format conversion to use to produce the format specifier's output. The following types are supported:

* `s`formats the argument value as a simple string. A null value is treated as an empty string.

* `I`treats the argument value as an SQL identifier, double-quoting it if necessary. It is an error for the value to be null \(equivalent to`quote_ident`\).

* `L`quotes the argument value as an SQL literal. A null value is displayed as the string`NULL`, without quotes \(equivalent to`quote_nullable`\).

In addition to the format specifiers described above, the special sequence`%%`may be used to output a literal`%`character.

Here are some examples of the basic format conversions:

```
SELECT format('Hello %s', 'World');

Result: 
Hello World


SELECT format('Testing %s, %s, %s, %%', 'one', 'two', 'three');

Result: 
Testing one, two, three, %


SELECT format('INSERT INTO %I VALUES(%L)', 'Foo bar', E'O\'Reilly');

Result: 
INSERT INTO "Foo bar" VALUES('O''Reilly')


SELECT format('INSERT INTO %I VALUES(%L)', 'locations', E'C:\\Program Files');

Result: 
INSERT INTO locations VALUES(E'C:\\Program Files')
```

Here are examples using_`width`_fields and the`-`flag:

```
SELECT format('|%10s|', 'foo');

Result: 
|       foo|


SELECT format('|%-10s|', 'foo');

Result: 
|foo       |


SELECT format('|%*s|', 10, 'foo');

Result: 
|       foo|


SELECT format('|%*s|', -10, 'foo');

Result: 
|foo       |


SELECT format('|%-*s|', 10, 'foo');

Result: 
|foo       |


SELECT format('|%-*s|', -10, 'foo');

Result: 
|foo       |
```

These examples show use of_`position`_fields:

```
SELECT format('Testing %3$s, %2$s, %1$s', 'one', 'two', 'three');

Result: 
Testing three, two, one


SELECT format('|%*2$s|', 'foo', 10, 'bar');

Result: 
|       bar|


SELECT format('|%1$*2$s|', 'foo', 10, 'bar');

Result: 
|       foo|
```

Unlike the standard C function`sprintf`,PostgreSQL's`format`function allows format specifiers with and without_`position`_fields to be mixed in the same format string. A format specifier without a_`position`_field always uses the next argument after the last argument consumed. In addition, the`format`function does not require all function arguments to be used in the format string. For example:

```
SELECT format('Testing %3$s, %2$s, %s', 'one', 'two', 'three');

Result: 
Testing three, two, three
```

The`%I`and`%L`format specifiers are particularly useful for safely constructing dynamic SQL statements. See[Example 42.1](https://www.postgresql.org/docs/10/static/plpgsql-statements.html#plpgsql-quote-literal-example).

---



[^1]:  [PostgreSQL: Documentation: 10: 9.4. String Functions and Operators](https://www.postgresql.org/docs/10/static/functions-string.html)

