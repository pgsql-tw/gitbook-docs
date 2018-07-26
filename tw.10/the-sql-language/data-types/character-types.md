# 8.3. 文字型別

**Table 8.4. Character Types**

| Name | Description |
| --- | --- | --- | --- |
| `character varying(`_`n`_\), `varchar(`_`n`_\) | variable-length with limit |
| `character(`_`n`_\), `char(`_`n`_\) | fixed-length, blank padded |
| `text` | variable unlimited length |

[Table 8.4](https://www.postgresql.org/docs/10/static/datatype-character.html#DATATYPE-CHARACTER-TABLE) shows the general-purpose character types available in PostgreSQL.

SQL defines two primary character types: `character varying(`_`n`_\) and `character(`_`n`_\), where _`n`_ is a positive integer. Both of these types can store strings up to _`n`_ characters \(not bytes\) in length. An attempt to store a longer string into a column of these types will result in an error, unless the excess characters are all spaces, in which case the string will be truncated to the maximum length. \(This somewhat bizarre exception is required by the SQL standard.\) If the string to be stored is shorter than the declared length, values of type `character` will be space-padded; values of type `character varying` will simply store the shorter string.

If one explicitly casts a value to `character varying(`_`n`_\) or `character(`_`n`_\), then an over-length value will be truncated to _`n`_ characters without raising an error. \(This too is required by the SQL standard.\)

The notations `varchar(`_`n`_\) and `char(`_`n`_\) are aliases for `character varying(`_`n`_\) and `character(`_`n`_\), respectively. `character` without length specifier is equivalent to `character(1)`. If `character varying` is used without length specifier, the type accepts strings of any size. The latter is a PostgreSQL extension.

In addition, PostgreSQL provides the `text` type, which stores strings of any length. Although the type `text` is not in the SQL standard, several other SQL database management systems have it as well.

Values of type `character` are physically padded with spaces to the specified width _`n`_, and are stored and displayed that way. However, trailing spaces are treated as semantically insignificant and disregarded when comparing two values of type `character`. In collations where whitespace is significant, this behavior can produce unexpected results; for example `SELECT 'a '::CHAR(2) collate "C" < E'a\n'::CHAR(2)` returns true, even though `C` locale would consider a space to be greater than a newline. Trailing spaces are removed when converting a `character` value to one of the other string types. Note that trailing spaces _are_ semantically significant in `character varying` and `text` values, and when using pattern matching, that is `LIKE` and regular expressions.

The storage requirement for a short string \(up to 126 bytes\) is 1 byte plus the actual string, which includes the space padding in the case of `character`. Longer strings have 4 bytes of overhead instead of 1. Long strings are compressed by the system automatically, so the physical requirement on disk might be less. Very long values are also stored in background tables so that they do not interfere with rapid access to shorter column values. In any case, the longest possible character string that can be stored is about 1 GB. \(The maximum value that will be allowed for _`n`_ in the data type declaration is less than that. It wouldn't be useful to change this because with multibyte character encodings the number of characters and bytes can be quite different. If you desire to store long strings with no specific upper limit, use `text` or `character varying` without a length specifier, rather than making up an arbitrary length limit.\)

#### Tip

There is no performance difference among these three types, apart from increased storage space when using the blank-padded type, and a few extra CPU cycles to check the length when storing into a length-constrained column. While `character(`_`n`_\) has performance advantages in some other database systems, there is no such advantage in PostgreSQL; in fact `character(`_`n`_\) is usually the slowest of the three because of its additional storage costs. In most situations `text` or `character varying` should be used instead.

Refer to [Section 4.1.2.1](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#SQL-SYNTAX-STRINGS) for information about the syntax of string literals, and to [Chapter 9](https://www.postgresql.org/docs/10/static/functions.html) for information about available operators and functions. The database character set determines the character set used to store textual values; for more information on character set support, refer to [Section 23.3](https://www.postgresql.org/docs/10/static/multibyte.html).

**Example 8.1. Using the Character Types**

```text
CREATE TABLE test1 (a character(4));
INSERT INTO test1 VALUES ('ok');
SELECT a, char_length(a) FROM test1; -- (1)
  a   | char_length
------+-------------
 ok   |           2

CREATE TABLE test2 (b varchar(5));
INSERT INTO test2 VALUES ('ok');
INSERT INTO test2 VALUES ('good      ');
INSERT INTO test2 VALUES ('too long');
ERROR:  value too long for type character varying(5)
INSERT INTO test2 VALUES ('too long'::varchar(5)); -- explicit truncation
SELECT b, char_length(b) FROM test2;
   b   | char_length
-------+-------------
 ok    |           2
 good  |           5
 too l |           5
```

| [\(1\)](https://www.postgresql.org/docs/10/static/datatype-character.html#co.datatype-char) | The `char_length` function is discussed in [Section 9.4](https://www.postgresql.org/docs/10/static/functions-string.html). |
| --- |


There are two other fixed-length character types in PostgreSQL, shown in [Table 8.5](https://www.postgresql.org/docs/10/static/datatype-character.html#DATATYPE-CHARACTER-SPECIAL-TABLE). The `name` type exists _only_ for the storage of identifiers in the internal system catalogs and is not intended for use by the general user. Its length is currently defined as 64 bytes \(63 usable characters plus terminator\) but should be referenced using the constant `NAMEDATALEN` in `C`source code. The length is set at compile time \(and is therefore adjustable for special uses\); the default maximum length might change in a future release. The type `"char"` \(note the quotes\) is different from `char(1)` in that it only uses one byte of storage. It is internally used in the system catalogs as a simplistic enumeration type.

**Table 8.5. Special Character Types**

| Name | Storage Size | Description |
| --- | --- | --- |
| `"char"` | 1 byte | single-byte internal type |
| `name` | 64 bytes | internal type for object names |

