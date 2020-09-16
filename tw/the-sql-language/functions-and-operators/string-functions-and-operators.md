# 9.4. 字串函式及運算子

This section describes functions and operators for examining and manipulating string values. Strings in this context include values of the types `character`, `character varying`, and `text`. Unless otherwise noted, all of the functions listed below work on all of these types, but be wary of potential effects of automatic space-padding when using the `character` type. Some functions also exist natively for the bit-string types.

SQL defines some string functions that use key words, rather than commas, to separate arguments. Details are in [Table 9.9](https://www.postgresql.org/docs/12/functions-string.html#FUNCTIONS-STRING-SQL). PostgreSQL also provides versions of these functions that use the regular function invocation syntax \(see [Table 9.10](https://www.postgresql.org/docs/12/functions-string.html#FUNCTIONS-STRING-OTHER)\).

{% hint style="info" %}
在 PostgreSQL 8.3 之前的版本中，由於存在從這些資料型別到文字的隱式強制轉換，這些函數也將默默接受幾種非字串資料型別的值。這些強制轉換已被刪除，因為它們經常引起令人驚訝的結果。但是，字串連接運算子（\|\|）仍然接受非字串輸入，只要至少一個輸入為字串型別即可，如 Table 9.9 所示。對於其他情況，如果您需要複製以前的行為，請在查詢語句中明確加入型別轉換。
{% endhint %}

#### **Table 9.9. SQL String Functions and Operators**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| _`string`_ `||` _`string`_ | `text` | String concatenation | `'Post' || 'greSQL'` | `PostgreSQL` |
| _`string`_ `||` _`non-string`_ or _`non-string`_ `||` _`string`_ | `text` | String concatenation with one non-string input | `'Value: ' || 42` | `Value: 42` |
| `bit_length(`_`string`_\) | `int` | Number of bits in string | `bit_length('jose')` | `32` |
| `char_length(`_`string`_\) or `character_length(`_`string`_\) | `int` | Number of characters in string | `char_length('jose')` | `4` |
| `lower(`_`string`_\) | `text` | Convert string to lower case | `lower('TOM')` | `tom` |
| `octet_length(`_`string`_\) | `int` | Number of bytes in string | `octet_length('jose')` | `4` |
| `overlay(`_`string`_ placing _`string`_ from `int` \[for `int`\]\) | `text` | Replace substring | `overlay('Txxxxas' placing 'hom' from 2 for 4)` | `Thomas` |
| `position(`_`substring`_ in _`string`_\) | `int` | Location of specified substring | `position('om' in 'Thomas')` | `3` |
| `substring(`_`string`_ \[from `int`\] \[for `int`\]\) | `text` | Extract substring | `substring('Thomas' from 2 for 3)` | `hom` |
| `substring(`_`string`_ from _`pattern`_\) | `text` | Extract substring matching POSIX regular expression. See [Section 9.7](https://www.postgresql.org/docs/12/functions-matching.html) for more information on pattern matching. | `substring('Thomas' from '...$')` | `mas` |
| `substring(`_`string`_ from _`pattern`_ for _`escape`_\) | `text` | Extract substring matching SQL regular expression. See [Section 9.7](https://www.postgresql.org/docs/12/functions-matching.html) for more information on pattern matching. | `substring('Thomas' from '%#"o_a#"_' for '#')` | `oma` |
| `trim([leading | trailing | both] [`_`characters`_\] from _`string`_\) | `text` | Remove the longest string containing only characters from _`characters`_ \(a space by default\) from the start, end, or both ends \(`both` is the default\) of _`string`_ | `trim(both 'xyz' from 'yxTomxx')` | `Tom` |
| `trim([leading | trailing | both] [from]` _`string`_ \[, _`characters`_\] \) | `text` | Non-standard syntax for `trim()` | `trim(both from 'yxTomxx', 'xyz')` | `Tom` |
| `upper(`_`string`_\) | `text` | Convert string to upper case | `upper('tom')` | `TOM` |

Additional string manipulation functions are available and are listed in [Table 9.10](https://www.postgresql.org/docs/12/functions-string.html#FUNCTIONS-STRING-OTHER). Some of them are used internally to implement the SQL-standard string functions listed in [Table 9.9](https://www.postgresql.org/docs/12/functions-string.html#FUNCTIONS-STRING-SQL).

#### **Table 9.10. Other String Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Return Type</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
      <th style="text-align:left">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><code>ascii(</code><em><code>string</code></em>)</td>
      <td style="text-align:left"><code>int</code>
      </td>
      <td style="text-align:left">ASCII code of the first character of the argument. For UTF8 returns the
        Unicode code point of the character. For other multibyte encodings, the
        argument must be an ASCII character.</td>
      <td style="text-align:left"><code>ascii(&apos;x&apos;)</code>
      </td>
      <td style="text-align:left"><code>120</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>btrim(</code><em><code>string</code></em>  <code>text</code> [, <em><code>characters</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Remove the longest string consisting only of characters in <em><code>characters</code></em> (a
          space by default) from the start and end of <em><code>string</code></em>
        </td>
        <td style="text-align:left"><code>btrim(&apos;xyxtrimyyx&apos;, &apos;xyz&apos;)</code>
        </td>
        <td style="text-align:left"><code>trim</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>chr(int</code>)</td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Character with the given code. For UTF8 the argument is treated as a Unicode
        code point. For other multibyte encodings the argument must designate an
        ASCII character. The NULL (0) character is not allowed because text data
        types cannot store such bytes.</td>
      <td style="text-align:left"><code>chr(65)</code>
      </td>
      <td style="text-align:left"><code>A</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>concat(</code><em><code>str</code></em>  <code>&quot;any&quot;</code> [, <em><code>str</code></em>  <code>&quot;any&quot;</code> [,
        ...] ])</td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Concatenate the text representations of all the arguments. NULL arguments
        are ignored.</td>
      <td style="text-align:left"><code>concat(&apos;abcde&apos;, 2, NULL, 22)</code>
      </td>
      <td style="text-align:left"><code>abcde222</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>concat_ws(</code><em><code>sep</code></em>  <code>text</code>, <em><code>str</code></em>  <code>&quot;any&quot;</code> [, <em><code>str</code></em>  <code>&quot;any&quot;</code> [,
        ...] ])</td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Concatenate all but the first argument with separators. The first argument
        is used as the separator string. NULL arguments are ignored.</td>
      <td style="text-align:left"><code>concat_ws(&apos;,&apos;, &apos;abcde&apos;, 2, NULL, 22)</code>
      </td>
      <td style="text-align:left"><code>abcde,2,22</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>convert(</code><em><code>string</code></em>  <code>bytea</code>, <em><code>src_encoding</code></em>  <code>name</code>, <em><code>dest_encoding</code></em>  <code>name</code>)</td>
      <td
      style="text-align:left"><code>bytea</code>
        </td>
        <td style="text-align:left">Convert string to <em><code>dest_encoding</code></em>. The original encoding
          is specified by <em><code>src_encoding</code></em>. The <em><code>string</code></em> must
          be valid in this encoding. Conversions can be defined by <code>CREATE CONVERSION</code>.
          Also there are some predefined conversions. See <a href="https://www.postgresql.org/docs/12/functions-string.html#CONVERSION-NAMES">Table 9.11</a> for
          available conversions.</td>
        <td style="text-align:left"><code>convert(&apos;text_in_utf8&apos;, &apos;UTF8&apos;, &apos;LATIN1&apos;)</code>
        </td>
        <td style="text-align:left"><code>text_in_utf8</code> represented in Latin-1 encoding (ISO 8859-1)</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>convert_from(</code><em><code>string</code></em>  <code>bytea</code>, <em><code>src_encoding</code></em>  <code>name</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Convert string to the database encoding. The original encoding is specified
          by <em><code>src_encoding</code></em>. The <em><code>string</code></em> must
          be valid in this encoding.</td>
        <td style="text-align:left"><code>convert_from(&apos;text_in_utf8&apos;, &apos;UTF8&apos;)</code>
        </td>
        <td style="text-align:left"><code>text_in_utf8</code> represented in the current database encoding</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>convert_to(</code><em><code>string</code></em>  <code>text</code>, <em><code>dest_encoding</code></em>  <code>name</code>)</td>
      <td
      style="text-align:left"><code>bytea</code>
        </td>
        <td style="text-align:left">Convert string to <em><code>dest_encoding</code></em>.</td>
        <td style="text-align:left"><code>convert_to(&apos;some text&apos;, &apos;UTF8&apos;)</code>
        </td>
        <td style="text-align:left"><code>some text</code> represented in the UTF8 encoding</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>decode(</code><em><code>string</code></em>  <code>text</code>, <em><code>format</code></em>  <code>text</code>)</td>
      <td
      style="text-align:left"><code>bytea</code>
        </td>
        <td style="text-align:left">Decode binary data from textual representation in <em><code>string</code></em>.
          Options for <em><code>format</code></em> are same as in <code>encode</code>.</td>
        <td
        style="text-align:left"><code>decode(&apos;MTIzAAE=&apos;, &apos;base64&apos;)</code>
          </td>
          <td style="text-align:left"><code>\x3132330001</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>encode(</code><em><code>data</code></em>  <code>bytea</code>, <em><code>format</code></em>  <code>text</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Encode binary data into a textual representation. Supported formats are: <code>base64</code>, <code>hex</code>, <code>escape</code>. <code>escape</code> converts
          zero bytes and high-bit-set bytes to octal sequences (<code>\</code><em><code>nnn</code></em>)
          and doubles backslashes.</td>
        <td style="text-align:left"><code>encode(&apos;123\000\001&apos;, &apos;base64&apos;)</code>
        </td>
        <td style="text-align:left"><code>MTIzAAE=</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>format</code>(<em><code>formatstr</code></em>  <code>text</code> [, <em><code>formatarg</code></em>  <code>&quot;any&quot;</code> [,
        ...] ])</td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Format arguments according to a format string. This function is similar
        to the C function <code>sprintf</code>. See <a href="https://www.postgresql.org/docs/12/functions-string.html#FUNCTIONS-STRING-FORMAT">Section 9.4.1</a>.</td>
      <td
      style="text-align:left"><code>format(&apos;Hello %s, %1$s&apos;, &apos;World&apos;)</code>
        </td>
        <td style="text-align:left"><code>Hello World, World</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>initcap(</code><em><code>string</code></em>)</td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Convert the first letter of each word to upper case and the rest to lower
        case. Words are sequences of alphanumeric characters separated by non-alphanumeric
        characters.</td>
      <td style="text-align:left"><code>initcap(&apos;hi THOMAS&apos;)</code>
      </td>
      <td style="text-align:left"><code>Hi Thomas</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>left(</code><em><code>str</code></em>  <code>text</code>, <em><code>n</code></em>  <code>int</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Return first <em><code>n</code></em> characters in the string. When <em><code>n</code></em> is
          negative, return all but last |<em><code>n</code></em>| characters.</td>
        <td
        style="text-align:left"><code>left(&apos;abcde&apos;, 2)</code>
          </td>
          <td style="text-align:left"><code>ab</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>length(</code><em><code>string</code></em>)</td>
      <td style="text-align:left"><code>int</code>
      </td>
      <td style="text-align:left">Number of characters in <em><code>string</code></em>
      </td>
      <td style="text-align:left"><code>length(&apos;jose&apos;)</code>
      </td>
      <td style="text-align:left"><code>4</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>length(</code><em><code>string</code></em>  <code>bytea</code>, <em><code>encoding</code></em>  <code>name</code> )</td>
      <td
      style="text-align:left"><code>int</code>
        </td>
        <td style="text-align:left">Number of characters in <em><code>string</code></em> in the given <em><code>encoding</code></em>.
          The <em><code>string</code></em> must be valid in this encoding.</td>
        <td
        style="text-align:left"><code>length(&apos;jose&apos;, &apos;UTF8&apos;)</code>
          </td>
          <td style="text-align:left"><code>4</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>lpad(</code><em><code>string</code></em>  <code>text</code>, <em><code>length</code></em>  <code>int</code> [, <em><code>fill</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Fill up the <em><code>string</code></em> to length <em><code>length</code></em> by
          prepending the characters <em><code>fill</code></em> (a space by default).
          If the <em><code>string</code></em> is already longer than <em><code>length</code></em> then
          it is truncated (on the right).</td>
        <td style="text-align:left"><code>lpad(&apos;hi&apos;, 5, &apos;xy&apos;)</code>
        </td>
        <td style="text-align:left"><code>xyxhi</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>ltrim(</code><em><code>string</code></em>  <code>text</code> [, <em><code>characters</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Remove the longest string containing only characters from <em><code>characters</code></em> (a
          space by default) from the start of <em><code>string</code></em>
        </td>
        <td style="text-align:left"><code>ltrim(&apos;zzzytest&apos;, &apos;xyz&apos;)</code>
        </td>
        <td style="text-align:left"><code>test</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>md5(</code><em><code>string</code></em>)</td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Calculates the MD5 hash of <em><code>string</code></em>, returning the
        result in hexadecimal</td>
      <td style="text-align:left"><code>md5(&apos;abc&apos;)</code>
      </td>
      <td style="text-align:left"><code>900150983cd24fb0 d6963f7d28e17f72</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>parse_ident(</code><em><code>qualified_identifier</code></em>  <code>text</code> [, <em><code>strictmode</code></em>  <code>boolean</code> DEFAULT
        true ] )</td>
      <td style="text-align:left"><code>text[]</code>
      </td>
      <td style="text-align:left">Split <em><code>qualified_identifier</code></em> into an array of identifiers,
        removing any quoting of individual identifiers. By default, extra characters
        after the last identifier are considered an error; but if the second parameter
        is <code>false</code>, then such extra characters are ignored. (This behavior
        is useful for parsing names for objects like functions.) Note that this
        function does not truncate over-length identifiers. If you want truncation
        you can cast the result to <code>name[]</code>.</td>
      <td style="text-align:left"><code>parse_ident(&apos;&quot;SomeSchema&quot;.someTable&apos;)</code>
      </td>
      <td style="text-align:left"><code>{SomeSchema,sometable}</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>pg_client_encoding()</code>
      </td>
      <td style="text-align:left"><code>name</code>
      </td>
      <td style="text-align:left">Current client encoding name</td>
      <td style="text-align:left"><code>pg_client_encoding()</code>
      </td>
      <td style="text-align:left"><code>SQL_ASCII</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>quote_ident(</code><em><code>string</code></em>  <code>text</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Return the given string suitably quoted to be used as an identifier in
          an SQL statement string. Quotes are added only if necessary (i.e., if the
          string contains non-identifier characters or would be case-folded). Embedded
          quotes are properly doubled. See also <a href="https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE">Example 42.1</a>.</td>
        <td
        style="text-align:left"><code>quote_ident(&apos;Foo bar&apos;)</code>
          </td>
          <td style="text-align:left"><code>&quot;Foo bar&quot;</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>quote_literal(</code><em><code>string</code></em>  <code>text</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Return the given string suitably quoted to be used as a string literal
          in an SQL statement string. Embedded single-quotes and backslashes are
          properly doubled. Note that <code>quote_literal</code> returns null on null
          input; if the argument might be null, <code>quote_nullable</code> is often
          more suitable. See also <a href="https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE">Example 42.1</a>.</td>
        <td
        style="text-align:left"><code>quote_literal(E&apos;O\&apos;Reilly&apos;)</code>
          </td>
          <td style="text-align:left"><code>&apos;O&apos;&apos;Reilly&apos;</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>quote_literal(</code><em><code>value</code></em>  <code>anyelement</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Coerce the given value to text and then quote it as a literal. Embedded
          single-quotes and backslashes are properly doubled.</td>
        <td style="text-align:left"><code>quote_literal(42.5)</code>
        </td>
        <td style="text-align:left"><code>&apos;42.5&apos;</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>quote_nullable(</code><em><code>string</code></em>  <code>text</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Return the given string suitably quoted to be used as a string literal
          in an SQL statement string; or, if the argument is null, return <code>NULL</code>.
          Embedded single-quotes and backslashes are properly doubled. See also
          <a
          href="https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE">Example 42.1</a>.</td>
        <td style="text-align:left"><code>quote_nullable(NULL)</code>
        </td>
        <td style="text-align:left"><code>NULL</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>quote_nullable(</code><em><code>value</code></em>  <code>anyelement</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Coerce the given value to text and then quote it as a literal; or, if
          the argument is null, return <code>NULL</code>. Embedded single-quotes and
          backslashes are properly doubled.</td>
        <td style="text-align:left"><code>quote_nullable(42.5)</code>
        </td>
        <td style="text-align:left"><code>&apos;42.5&apos;</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>regexp_match(</code><em><code>string</code></em>  <code>text</code>, <em><code>pattern</code></em>  <code>text</code> [, <em><code>flags</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text[]</code>
        </td>
        <td style="text-align:left">Return captured substring(s) resulting from the first match of a POSIX
          regular expression to the <em><code>string</code></em>. See <a href="https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP">Section 9.7.3</a> for
          more information.</td>
        <td style="text-align:left"><code>regexp_match(&apos;foobarbequebaz&apos;, &apos;(bar)(beque)&apos;)</code>
        </td>
        <td style="text-align:left"><code>{bar,beque}</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>regexp_matches(</code><em><code>string</code></em>  <code>text</code>, <em><code>pattern</code></em>  <code>text</code> [, <em><code>flags</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>setof text[]</code>
        </td>
        <td style="text-align:left">Return captured substring(s) resulting from matching a POSIX regular expression
          to the <em><code>string</code></em>. See <a href="https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP">Section 9.7.3</a> for
          more information.</td>
        <td style="text-align:left"><code>regexp_matches(&apos;foobarbequebaz&apos;, &apos;ba.&apos;, &apos;g&apos;)</code>
        </td>
        <td style="text-align:left">
          <p><code>{bar}</code>
          </p>
          <p><code>{baz}</code>(2 rows)</p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>regexp_replace(</code><em><code>string</code></em>  <code>text</code>, <em><code>pattern</code></em>  <code>text</code>, <em><code>replacement</code></em>  <code>text</code> [, <em><code>flags</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Replace substring(s) matching a POSIX regular expression. See <a href="https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP">Section 9.7.3</a> for
          more information.</td>
        <td style="text-align:left"><code>regexp_replace(&apos;Thomas&apos;, &apos;.[mN]a.&apos;, &apos;M&apos;)</code>
        </td>
        <td style="text-align:left"><code>ThM</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>regexp_split_to_array(</code><em><code>string</code></em>  <code>text</code>, <em><code>pattern</code></em>  <code>text</code> [, <em><code>flags</code></em>  <code>text</code> ])</td>
      <td
      style="text-align:left"><code>text[]</code>
        </td>
        <td style="text-align:left">Split <em><code>string</code></em> using a POSIX regular expression as the
          delimiter. See <a href="https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP">Section 9.7.3</a> for
          more information.</td>
        <td style="text-align:left"><code>regexp_split_to_array(&apos;hello world&apos;, &apos;\s+&apos;)</code>
        </td>
        <td style="text-align:left"><code>{hello,world}</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>regexp_split_to_table(</code><em><code>string</code></em>  <code>text</code>, <em><code>pattern</code></em>  <code>text</code> [, <em><code>flags</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>setof text</code>
        </td>
        <td style="text-align:left">Split <em><code>string</code></em> using a POSIX regular expression as the
          delimiter. See <a href="https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP">Section 9.7.3</a> for
          more information.</td>
        <td style="text-align:left"><code>regexp_split_to_table(&apos;hello world&apos;, &apos;\s+&apos;)</code>
        </td>
        <td style="text-align:left">
          <p><code>hello</code>
          </p>
          <p><code>world</code>(2 rows)</p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>repeat(</code><em><code>string</code></em>  <code>text</code>, <em><code>number</code></em>  <code>int</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Repeat <em><code>string</code></em> the specified <em><code>number</code></em> of
          times</td>
        <td style="text-align:left"><code>repeat(&apos;Pg&apos;, 4)</code>
        </td>
        <td style="text-align:left"><code>PgPgPgPg</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>replace(</code><em><code>string</code></em>  <code>text</code>, <em><code>from</code></em>  <code>text</code>, <em><code>to</code></em>  <code>text</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Replace all occurrences in <em><code>string</code></em> of substring <em><code>from</code></em> with
          substring <em><code>to</code></em>
        </td>
        <td style="text-align:left"><code>replace(&apos;abcdefabcdef&apos;, &apos;cd&apos;, &apos;XX&apos;)</code>
        </td>
        <td style="text-align:left"><code>abXXefabXXef</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>reverse(</code><em><code>str</code></em>)</td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Return reversed string.</td>
      <td style="text-align:left"><code>reverse(&apos;abcde&apos;)</code>
      </td>
      <td style="text-align:left"><code>edcba</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>right(</code><em><code>str</code></em>  <code>text</code>, <em><code>n</code></em>  <code>int</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Return last <em><code>n</code></em> characters in the string. When <em><code>n</code></em> is
          negative, return all but first |<em><code>n</code></em>| characters.</td>
        <td
        style="text-align:left"><code>right(&apos;abcde&apos;, 2)</code>
          </td>
          <td style="text-align:left"><code>de</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>rpad(</code><em><code>string</code></em>  <code>text</code>, <em><code>length</code></em>  <code>int</code> [, <em><code>fill</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Fill up the <em><code>string</code></em> to length <em><code>length</code></em> by
          appending the characters <em><code>fill</code></em> (a space by default).
          If the <em><code>string</code></em> is already longer than <em><code>length</code></em> then
          it is truncated.</td>
        <td style="text-align:left"><code>rpad(&apos;hi&apos;, 5, &apos;xy&apos;)</code>
        </td>
        <td style="text-align:left"><code>hixyx</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>rtrim(</code><em><code>string</code></em>  <code>text</code> [, <em><code>characters</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Remove the longest string containing only characters from <em><code>characters</code></em> (a
          space by default) from the end of <em><code>string</code></em>
        </td>
        <td style="text-align:left"><code>rtrim(&apos;testxxzx&apos;, &apos;xyz&apos;)</code>
        </td>
        <td style="text-align:left"><code>test</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>split_part(</code><em><code>string</code></em>  <code>text</code>, <em><code>delimiter</code></em>  <code>text</code>, <em><code>field</code></em>  <code>int</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Split <em><code>string</code></em> on <em><code>delimiter</code></em> and
          return the given field (counting from one)</td>
        <td style="text-align:left"><code>split_part(&apos;abc~@~def~@~ghi&apos;, &apos;~@~&apos;, 2)</code>
        </td>
        <td style="text-align:left"><code>def</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>strpos(</code><em><code>string</code></em>, <em><code>substring</code></em>)</td>
      <td
      style="text-align:left"><code>int</code>
        </td>
        <td style="text-align:left">Location of specified substring (same as <code>position(</code><em><code>substring</code></em> in <em><code>string</code></em>),
          but note the reversed argument order)</td>
        <td style="text-align:left"><code>strpos(&apos;high&apos;, &apos;ig&apos;)</code>
        </td>
        <td style="text-align:left"><code>2</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>substr(</code><em><code>string</code></em>, <em><code>from</code></em> [, <em><code>count</code></em>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">&#x56DE;&#x50B3;&#x5B50;&#x5B57;&#x4E32;&#xFF08;&#x8207; substring(<code>string</code> from <code>from</code> for <code>count</code>)
          &#x76F8;&#x540C;&#xFF09;</td>
        <td style="text-align:left"><code>substr(&apos;alphabet&apos;, 3, 2)</code>
        </td>
        <td style="text-align:left"><code>ph</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>starts_with(</code><em><code>string</code></em>, <em><code>prefix</code></em>)</td>
      <td
      style="text-align:left"><code>bool</code>
        </td>
        <td style="text-align:left">Returns true if <em><code>string</code></em> starts with <em><code>prefix</code></em>.</td>
        <td
        style="text-align:left"><code>starts_with(&apos;alphabet&apos;, &apos;alph&apos;)</code>
          </td>
          <td style="text-align:left"><code>t</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>to_ascii(</code><em><code>string</code></em>  <code>text</code> [, <em><code>encoding</code></em>  <code>text</code>])</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Convert <em><code>string</code></em> to ASCII from another encoding (only
          supports conversion from <code>LATIN1</code>, <code>LATIN2</code>, <code>LATIN9</code>,
          and <code>WIN1250</code> encodings)</td>
        <td style="text-align:left"><code>to_ascii(&apos;Karel&apos;)</code>
        </td>
        <td style="text-align:left"><code>Karel</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>to_hex(</code><em><code>number</code></em>  <code>int</code> or <code>bigint</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Convert <em><code>number</code></em> to its equivalent hexadecimal representation</td>
        <td
        style="text-align:left"><code>to_hex(2147483647)</code>
          </td>
          <td style="text-align:left"><code>7fffffff</code>
          </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>translate(</code><em><code>string</code></em>  <code>text</code>, <em><code>from</code></em>  <code>text</code>, <em><code>to</code></em>  <code>text</code>)</td>
      <td
      style="text-align:left"><code>text</code>
        </td>
        <td style="text-align:left">Any character in <em><code>string</code></em> that matches a character in
          the <em><code>from</code></em> set is replaced by the corresponding character
          in the <em><code>to</code></em> set. If <em><code>from</code></em> is longer
          than <em><code>to</code></em>, occurrences of the extra characters in <em><code>from</code></em> are
          removed.</td>
        <td style="text-align:left"><code>translate(&apos;12345&apos;, &apos;143&apos;, &apos;ax&apos;)</code>
        </td>
        <td style="text-align:left"><code>a2x5</code>
        </td>
    </tr>
  </tbody>
</table>

The `concat`, `concat_ws` and `format` functions are variadic, so it is possible to pass the values to be concatenated or formatted as an array marked with the `VARIADIC` keyword \(see [Section 37.5.5](https://www.postgresql.org/docs/12/xfunc-sql.html#XFUNC-SQL-VARIADIC-FUNCTIONS)\). The array's elements are treated as if they were separate ordinary arguments to the function. If the variadic array argument is NULL, `concat` and `concat_ws` return NULL, but `format` treats a NULL as a zero-element array.

See also the aggregate function `string_agg` in [Section 9.20](https://www.postgresql.org/docs/12/functions-aggregate.html).

#### **Table 9.11. Built-in Conversions**

| Conversion Name [\[a\]](https://www.postgresql.org/docs/12/functions-string.html#ftn.id-1.5.8.9.10.2.1.1.1.1) | Source Encoding | Destination Encoding |
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
| `windows_1258_to_utf8` | `WIN1258` | `UTF8` |
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
| `utf8_to_windows_1258` | `UTF8` | `WIN1258` |
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
| [\[a\]](https://www.postgresql.org/docs/12/functions-string.html#id-1.5.8.9.10.2.1.1.1.1) The conversion names follow a standard naming scheme: The official name of the source encoding with all non-alphanumeric characters replaced by underscores, followed by `_to_`, followed by the similarly processed destination encoding name. Therefore, the names might deviate from the customary encoding names. |  |  |

## 9.4.1. `format`

The function `format` produces output formatted according to a format string, in a style similar to the C function `sprintf`.

```text
format(formatstr text [, formatarg "any" [, ...] ])
```

_`formatstr`_ is a format string that specifies how the result should be formatted. Text in the format string is copied directly to the result, except where _format specifiers_ are used. Format specifiers act as placeholders in the string, defining how subsequent function arguments should be formatted and inserted into the result. Each _`formatarg`_ argument is converted to text according to the usual output rules for its data type, and then formatted and inserted into the result string according to the format specifier\(s\).

Format specifiers are introduced by a `%` character and have the form

```text
%[position][flags][width]type
```

where the component fields are:_`position`_ \(optional\)

A string of the form _`n`_$ where _`n`_ is the index of the argument to print. Index 1 means the first argument after _`formatstr`_. If the _`position`_ is omitted, the default is to use the next argument in sequence._`flags`_ \(optional\)

Additional options controlling how the format specifier's output is formatted. Currently the only supported flag is a minus sign \(`-`\) which will cause the format specifier's output to be left-justified. This has no effect unless the _`width`_ field is also specified._`width`_ \(optional\)

Specifies the _minimum_ number of characters to use to display the format specifier's output. The output is padded on the left or right \(depending on the `-` flag\) with spaces as needed to fill the width. A too-small width does not cause truncation of the output, but is simply ignored. The width may be specified using any of the following: a positive integer; an asterisk \(`*`\) to use the next function argument as the width; or a string of the form `*`_`n`_$ to use the _`n`_th function argument as the width.

If the width comes from a function argument, that argument is consumed before the argument that is used for the format specifier's value. If the width argument is negative, the result is left aligned \(as if the `-` flag had been specified\) within a field of length `abs`\(_`width`_\)._`type`_ \(required\)

The type of format conversion to use to produce the format specifier's output. The following types are supported:

* `s` formats the argument value as a simple string. A null value is treated as an empty string.
* `I` treats the argument value as an SQL identifier, double-quoting it if necessary. It is an error for the value to be null \(equivalent to `quote_ident`\).
* `L` quotes the argument value as an SQL literal. A null value is displayed as the string `NULL`, without quotes \(equivalent to `quote_nullable`\).

In addition to the format specifiers described above, the special sequence `%%` may be used to output a literal `%` character.

Here are some examples of the basic format conversions:

```text
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

These examples show use of _`position`_ fields:

```text
SELECT format('Testing %3$s, %2$s, %1$s', 'one', 'two', 'three');
Result: Testing three, two, one

SELECT format('|%*2$s|', 'foo', 10, 'bar');
Result: |       bar|

SELECT format('|%1$*2$s|', 'foo', 10, 'bar');
Result: |       foo|
```

Unlike the standard C function `sprintf`, PostgreSQL's `format` function allows format specifiers with and without _`position`_ fields to be mixed in the same format string. A format specifier without a _`position`_ field always uses the next argument after the last argument consumed. In addition, the `format` function does not require all function arguments to be used in the format string. For example:

```text
SELECT format('Testing %3$s, %2$s, %s', 'one', 'two', 'three');
Result: Testing three, two, three
```

The `%I` and `%L` format specifiers are particularly useful for safely constructing dynamic SQL statements. See [Example 42.1](https://www.postgresql.org/docs/12/plpgsql-statements.html#PLPGSQL-QUOTE-LITERAL-EXAMPLE).

