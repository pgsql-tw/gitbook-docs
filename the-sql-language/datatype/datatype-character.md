## 8.3. Character Types [#](#DATATYPE-CHARACTER)

<a id="id-1.5.7.11.2"></a><a id="id-1.5.7.11.3"></a><a id="id-1.5.7.11.4"></a><a id="id-1.5.7.11.5"></a><a id="id-1.5.7.11.6"></a><a id="id-1.5.7.11.7"></a><a id="id-1.5.7.11.8"></a><a id="id-1.5.7.11.9"></a><a id="DATATYPE-CHARACTER-TABLE"></a>

**Table 8.4. Character Types**

<table border="1" class="table" summary="Character Types"><colgroup><col/><col/></colgroup><thead><tr><th>Name</th><th>Description</th></tr></thead><tbody><tr><td><code class="type">character varying(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">varchar(<em class="replaceable"><code>n</code></em>)</code></td><td>variable-length with limit</td></tr><tr><td><code class="type">character(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">char(<em class="replaceable"><code>n</code></em>)</code>, <code class="type">bpchar(<em class="replaceable"><code>n</code></em>)</code></td><td>fixed-length, blank-padded</td></tr><tr><td><code class="type">bpchar</code></td><td>variable unlimited length, blank-trimmed</td></tr><tr><td><code class="type">text</code></td><td>variable unlimited length</td></tr></tbody></table>

<br>

[Table 8.4](datatype-character.md#DATATYPE-CHARACTER-TABLE) shows the
general-purpose character types available in
PostgreSQL.

SQL defines two primary character types:
`character varying(n)` and
`character(n)`, where *`n`*
is a positive integer. Both of these types can store strings up to
*`n`* characters (not bytes) in length. An attempt to store a
longer string into a column of these types will result in an
error, unless the excess characters are all spaces, in which case
the string will be truncated to the maximum length. (This somewhat
bizarre exception is required by the SQL
standard.)
However, if one explicitly casts a value to `character
varying(n)` or
`character(n)`, then an over-length
value will be truncated to *`n`* characters without
raising an error. (This too is required by the
SQL standard.)
If the string to be stored is shorter than the declared
length, values of type `character` will be space-padded;
values of type `character varying` will simply store the
shorter
string.

In addition, PostgreSQL provides the
`text` type, which stores strings of any length.
Although the `text` type is not in the
SQL standard, several other SQL database
management systems have it as well.
`text` is PostgreSQL's native
string data type, in that most built-in functions operating on strings
are declared to take or return `text` not `character
varying`. For many purposes, `character varying`
acts as though it were a [domain](domains.md)
over `text`.

The type name `varchar` is an alias for `character
varying`, while `bpchar` (with length specifier) and
`char` are aliases for `character`. The
`varchar` and `char` aliases are defined in the
SQL standard; `bpchar` is a
PostgreSQL extension.

If specified, the length *`n`* must be greater
than zero and cannot exceed 10,485,760. If `character
varying` (or `varchar`) is used without
length specifier, the type accepts strings of any length. If
`bpchar` lacks a length specifier, it also accepts strings
of any length, but trailing spaces are semantically insignificant.
If `character` (or `char`) lacks a specifier,
it is equivalent to `character(1)`.

Values of type `character` are physically padded
with spaces to the specified width *`n`*, and are
stored and displayed that way. However, trailing spaces are treated as
semantically insignificant and disregarded when comparing two values
of type `character`. In collations where whitespace
is significant, this behavior can produce unexpected results;
for example `SELECT 'a '::CHAR(2) collate "C" <
E'a\n'::CHAR(2)` returns true, even though `C`
locale would consider a space to be greater than a newline.
Trailing spaces are removed when converting a `character` value
to one of the other string types. Note that trailing spaces
*are* semantically significant in
`character varying` and `text` values, and
when using pattern matching, that is `LIKE` and
regular expressions.

The characters that can be stored in any of these data types are
determined by the database character set, which is selected when
the database is created. Regardless of the specific character set,
the character with code zero (sometimes called NUL) cannot be stored.
For more information refer to [Section 23.3](../../server-administration/charset/multibyte.md).

The storage requirement for a short string (up to 126 bytes) is 1 byte
plus the actual string, which includes the space padding in the case of
`character`. Longer strings have 4 bytes of overhead instead
of 1. Long strings are compressed by the system automatically, so
the physical requirement on disk might be less. Very long values are also
stored in background tables so that they do not interfere with rapid
access to shorter column values. In any case, the longest
possible character string that can be stored is about 1 GB. (The
maximum value that will be allowed for *`n`* in the data
type declaration is less than that. It wouldn't be useful to
change this because with multibyte character encodings the number of
characters and bytes can be quite different. If you desire to
store long strings with no specific upper limit, use
`text` or `character varying` without a length
specifier, rather than making up an arbitrary length limit.)

### Tip

There is no performance difference among these three types,
apart from increased storage space when using the blank-padded
type, and a few extra CPU cycles to check the length when storing into
a length-constrained column. While
`character(n)` has performance
advantages in some other database systems, there is no such advantage in
PostgreSQL; in fact
`character(n)` is usually the slowest of
the three because of its additional storage costs. In most situations
`text` or `character varying` should be used
instead.

Refer to [Section 4.1.2.1](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS) for information about
the syntax of string literals, and to [Chapter 9](../functions/README.md)
for information about available operators and functions.

<a id="id-1.5.7.11.21"></a>

**Example 8.1. Using the Character Types**

```

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

<table border="0" summary="Callout list"><tr><td align="left" valign="top" width="5%"><p><a href="#co.datatype-char">(1)</a> </p></td><td align="left" valign="top"><p>
       The <code class="function">char_length</code> function is discussed in
       <a class="xref" href="../functions/functions-string.md">Section 9.4</a>.
      </p></td></tr></table>

<br>

There are two other fixed-length character types in
PostgreSQL, shown in [Table 8.5](datatype-character.md#DATATYPE-CHARACTER-SPECIAL-TABLE).
These are not intended for general-purpose use, only for use
in the internal system catalogs.
The `name` type is used to store identifiers. Its
length is currently defined as 64 bytes (63 usable characters plus
terminator) but should be referenced using the constant
`NAMEDATALEN` in `C` source code.
The length is set at compile time (and
is therefore adjustable for special uses); the default maximum
length might change in a future release. The type `"char"`
(note the quotes) is different from `char(1)` in that it
only uses one byte of storage, and therefore can store only a single
ASCII character. It is used in the system
catalogs as a simplistic enumeration type.

<a id="DATATYPE-CHARACTER-SPECIAL-TABLE"></a>

**Table 8.5. Special Character Types**

<table border="1" class="table" summary="Special Character Types"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Name</th><th>Storage Size</th><th>Description</th></tr></thead><tbody><tr><td><code class="type">"char"</code></td><td>1 byte</td><td>single-byte internal type</td></tr><tr><td><code class="type">name</code></td><td>64 bytes</td><td>internal type for object names</td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-character.html)（英文原文，待翻譯）
