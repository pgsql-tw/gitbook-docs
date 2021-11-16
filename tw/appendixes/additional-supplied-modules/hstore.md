# F.16. hstore

This module implements the `hstore` data type for storing sets of key/value pairs within a single PostgreSQL value. This can be useful in various scenarios, such as rows with many attributes that are rarely examined, or semi-structured data. Keys and values are simply text strings.

This module is considered “trusted”, that is, it can be installed by non-superusers who have `CREATE` privilege on the current database.

## F.16.1. `hstore` External Representation

The text representation of an `hstore`, used for input and output, includes zero or more _`key`_ `=>` _`value`_ pairs separated by commas. Some examples:

```
k => v
foo => bar, baz => whatever
"1-a" => "anything at all"
```

The order of the pairs is not significant (and may not be reproduced on output). Whitespace between pairs or around the `=>` sign is ignored. Double-quote keys and values that include whitespace, commas, `=`s or `>`s. To include a double quote or a backslash in a key or value, escape it with a backslash.

Each key in an `hstore` is unique. If you declare an `hstore` with duplicate keys, only one will be stored in the `hstore` and there is no guarantee as to which will be kept:

```
SELECT 'a=>1,a=>2'::hstore;
  hstore
----------
 "a"=>"1"
```

A value (but not a key) can be an SQL `NULL`. For example:

```
key => NULL
```

The `NULL` keyword is case-insensitive. Double-quote the `NULL` to treat it as the ordinary string “NULL”.

#### Note

Keep in mind that the `hstore` text format, when used for input, applies _before_ any required quoting or escaping. If you are passing an `hstore` literal via a parameter, then no additional processing is needed. But if you're passing it as a quoted literal constant, then any single-quote characters and (depending on the setting of the `standard_conforming_strings` configuration parameter) backslash characters need to be escaped correctly. See [Section 4.1.2.1](https://www.postgresql.org/docs/14/sql-syntax-lexical.html#SQL-SYNTAX-STRINGS) for more on the handling of string constants.

On output, double quotes always surround keys and values, even when it's not strictly necessary.

## F.16.2. `hstore` Operators and Functions

The operators provided by the `hstore` module are shown in [Table F.7](https://www.postgresql.org/docs/14/hstore.html#HSTORE-OP-TABLE), the functions in [Table F.8](https://www.postgresql.org/docs/14/hstore.html#HSTORE-FUNC-TABLE).

#### **Table F.7. `hstore` Operators**

| <p>Operator</p><p>Description</p><p>Example(s)</p>                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>hstore</code> <code>-></code> <code>text</code> → <code>text</code></p><p>Returns value associated with given key, or <code>NULL</code> if not present.</p><p><code>'a=>x, b=>y'::hstore -> 'a'</code> → <code>x</code></p>                                                         |
| <p><code>hstore</code> <code>-></code> <code>text[]</code> → <code>text[]</code></p><p>Returns values associated with given keys, or <code>NULL</code> if not present.</p><p><code>'a=>x, b=>y, c=>z'::hstore -> ARRAY['c','a']</code> → <code>{"z","x"}</code></p>                          |
| <p><code>hstore</code> <code>||</code> <code>hstore</code> → <code>hstore</code></p><p>Concatenates two <code>hstore</code>s.</p><p><code>'a=>b, c=>d'::hstore || 'c=>x, d=>q'::hstore</code> → <code>"a"=>"b", "c"=>"x", "d"=>"q"</code></p>                                                |
| <p><code>hstore</code> <code>?</code> <code>text</code> → <code>boolean</code></p><p>Does <code>hstore</code> contain key?</p><p><code>'a=>1'::hstore ? 'a'</code> → <code>t</code></p>                                                                                                      |
| <p><code>hstore</code> <code>?&#x26;</code> <code>text[]</code> → <code>boolean</code></p><p>Does <code>hstore</code> contain all the specified keys?</p><p><code>'a=>1,b=>2'::hstore ?&#x26; ARRAY['a','b']</code> → <code>t</code></p>                                                     |
| <p><code>hstore</code> <code>?|</code> <code>text[]</code> → <code>boolean</code></p><p>Does <code>hstore</code> contain any of the specified keys?</p><p><code>'a=>1,b=>2'::hstore ?| ARRAY['b','c']</code> → <code>t</code></p>                                                            |
| <p><code>hstore</code> <code>@></code> <code>hstore</code> → <code>boolean</code></p><p>Does left operand contain right?</p><p><code>'a=>b, b=>1, c=>NULL'::hstore @> 'b=>1'</code> → <code>t</code></p>                                                                                     |
| <p><code>hstore</code> <code>&#x3C;@</code> <code>hstore</code> → <code>boolean</code></p><p>Is left operand contained in right?</p><p><code>'a=>c'::hstore &#x3C;@ 'a=>b, b=>1, c=>NULL'</code> → <code>f</code></p>                                                                        |
| <p><code>hstore</code> <code>-</code> <code>text</code> → <code>hstore</code></p><p>Deletes key from left operand.</p><p><code>'a=>1, b=>2, c=>3'::hstore - 'b'::text</code> → <code>"a"=>"1", "c"=>"3"</code></p>                                                                           |
| <p><code>hstore</code> <code>-</code> <code>text[]</code> → <code>hstore</code></p><p>Deletes keys from left operand.</p><p><code>'a=>1, b=>2, c=>3'::hstore - ARRAY['a','b']</code> → <code>"c"=>"3"</code></p>                                                                             |
| <p><code>hstore</code> <code>-</code> <code>hstore</code> → <code>hstore</code></p><p>Deletes pairs from left operand that match pairs in the right operand.</p><p><code>'a=>1, b=>2, c=>3'::hstore - 'a=>4, b=>2'::hstore</code> → <code>"a"=>"1", "c"=>"3"</code></p>                      |
| <p><code>anyelement</code> <code>#=</code> <code>hstore</code> → <code>anyelement</code></p><p>Replaces fields in the left operand (which must be a composite type) with matching values from <code>hstore</code>.</p><p><code>ROW(1,3) #= 'f1=>11'::hstore</code> → <code>(11,3)</code></p> |
| <p><code>%%</code> <code>hstore</code> → <code>text[]</code></p><p>Converts <code>hstore</code> to an array of alternating keys and values.</p><p><code>%% 'a=>foo, b=>bar'::hstore</code> → <code>{a,foo,b,bar}</code></p>                                                                  |
| <p><code>%#</code> <code>hstore</code> → <code>text[]</code></p><p>Converts <code>hstore</code> to a two-dimensional key/value array.</p><p><code>%# 'a=>foo, b=>bar'::hstore</code> → <code>{{a,foo},{b,bar}}</code></p>                                                                    |

#### **Table F.8. `hstore` Functions**

| <p>Function</p><p>Description</p><p>Example(s)</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>hstore</code> ( <code>record</code> ) → <code>hstore</code></p><p>Constructs an <code>hstore</code> from a record or row.</p><p><code>hstore(ROW(1,2))</code> → <code>"f1"=>"1", "f2"=>"2"</code></p>                                                                                                                                                                                                                                                                                                                           |
| <p><code>hstore</code> ( <code>text[]</code> ) → <code>hstore</code></p><p>Constructs an <code>hstore</code> from an array, which may be either a key/value array, or a two-dimensional array.</p><p><code>hstore(ARRAY['a','1','b','2'])</code> → <code>"a"=>"1", "b"=>"2"</code></p><p><code>hstore(ARRAY[['c','3'],['d','4']])</code> → <code>"c"=>"3", "d"=>"4"</code></p>                                                                                                                                                           |
| <p><code>hstore</code> ( <code>text[]</code>, <code>text[]</code> ) → <code>hstore</code></p><p>Constructs an <code>hstore</code> from separate key and value arrays.</p><p><code>hstore(ARRAY['a','b'], ARRAY['1','2'])</code> → <code>"a"=>"1", "b"=>"2"</code></p>                                                                                                                                                                                                                                                                    |
| <p><code>hstore</code> ( <code>text</code>, <code>text</code> ) → <code>hstore</code></p><p>Makes a single-item <code>hstore</code>.</p><p><code>hstore('a', 'b')</code> → <code>"a"=>"b"</code></p>                                                                                                                                                                                                                                                                                                                                     |
| <p><code>akeys</code> ( <code>hstore</code> ) → <code>text[]</code></p><p>Extracts an <code>hstore</code>'s keys as an array.</p><p><code>akeys('a=>1,b=>2')</code> → <code>{a,b}</code></p>                                                                                                                                                                                                                                                                                                                                             |
| <p><code>skeys</code> ( <code>hstore</code> ) → <code>setof text</code></p><p>Extracts an <code>hstore</code>'s keys as a set.</p><p><code>skeys('a=>1,b=>2')</code> →</p>                                                                                                                                                                                                                                                                                                                                                               |
| <p><code>avals</code> ( <code>hstore</code> ) → <code>text[]</code></p><p>Extracts an <code>hstore</code>'s values as an array.</p><p><code>avals('a=>1,b=>2')</code> → <code>{1,2}</code></p>                                                                                                                                                                                                                                                                                                                                           |
| <p><code>svals</code> ( <code>hstore</code> ) → <code>setof text</code></p><p>Extracts an <code>hstore</code>'s values as a set.</p><p><code>svals('a=>1,b=>2')</code> →</p>                                                                                                                                                                                                                                                                                                                                                             |
| <p><code>hstore_to_array</code> ( <code>hstore</code> ) → <code>text[]</code></p><p>Extracts an <code>hstore</code>'s keys and values as an array of alternating keys and values.</p><p><code>hstore_to_array('a=>1,b=>2')</code> → <code>{a,1,b,2}</code></p>                                                                                                                                                                                                                                                                           |
| <p><code>hstore_to_matrix</code> ( <code>hstore</code> ) → <code>text[]</code></p><p>Extracts an <code>hstore</code>'s keys and values as a two-dimensional array.</p><p><code>hstore_to_matrix('a=>1,b=>2')</code> → <code>{{a,1},{b,2}}</code></p>                                                                                                                                                                                                                                                                                     |
| <p><code>hstore_to_json</code> ( <code>hstore</code> ) → <code>json</code></p><p>Converts an <code>hstore</code> to a <code>json</code> value, converting all non-null values to JSON strings.</p><p>This function is used implicitly when an <code>hstore</code> value is cast to <code>json</code>.</p><p><code>hstore_to_json('"a key"=>1, b=>t, c=>null, d=>12345, e=>012345, f=>1.234, g=>2.345e+4')</code> → <code>{"a key": "1", "b": "t", "c": null, "d": "12345", "e": "012345", "f": "1.234", "g": "2.345e+4"}</code></p>      |
| <p><code>hstore_to_jsonb</code> ( <code>hstore</code> ) → <code>jsonb</code></p><p>Converts an <code>hstore</code> to a <code>jsonb</code> value, converting all non-null values to JSON strings.</p><p>This function is used implicitly when an <code>hstore</code> value is cast to <code>jsonb</code>.</p><p><code>hstore_to_jsonb('"a key"=>1, b=>t, c=>null, d=>12345, e=>012345, f=>1.234, g=>2.345e+4')</code> → <code>{"a key": "1", "b": "t", "c": null, "d": "12345", "e": "012345", "f": "1.234", "g": "2.345e+4"}</code></p> |
| <p><code>hstore_to_json_loose</code> ( <code>hstore</code> ) → <code>json</code></p><p>Converts an <code>hstore</code> to a <code>json</code> value, but attempts to distinguish numerical and Boolean values so they are unquoted in the JSON.</p><p><code>hstore_to_json_loose('"a key"=>1, b=>t, c=>null, d=>12345, e=>012345, f=>1.234, g=>2.345e+4')</code> → <code>{"a key": 1, "b": true, "c": null, "d": 12345, "e": "012345", "f": 1.234, "g": 2.345e+4}</code></p>                                                             |
| <p><code>hstore_to_jsonb_loose</code> ( <code>hstore</code> ) → <code>jsonb</code></p><p>Converts an <code>hstore</code> to a <code>jsonb</code> value, but attempts to distinguish numerical and Boolean values so they are unquoted in the JSON.</p><p><code>hstore_to_jsonb_loose('"a key"=>1, b=>t, c=>null, d=>12345, e=>012345, f=>1.234, g=>2.345e+4')</code> → <code>{"a key": 1, "b": true, "c": null, "d": 12345, "e": "012345", "f": 1.234, "g": 2.345e+4}</code></p>                                                         |
| <p><code>slice</code> ( <code>hstore</code>, <code>text[]</code> ) → <code>hstore</code></p><p>Extracts a subset of an <code>hstore</code> containing only the specified keys.</p><p><code>slice('a=>1,b=>2,c=>3'::hstore, ARRAY['b','c','x'])</code> → <code>"b"=>"2", "c"=>"3"</code></p>                                                                                                                                                                                                                                              |
| <p><code>each</code> ( <code>hstore</code> ) → <code>setof record</code> ( <em><code>key</code></em> <code>text</code>, <em><code>value</code></em> <code>text</code> )</p><p>Extracts an <code>hstore</code>'s keys and values as a set of records.</p><p><code>select * from each('a=>1,b=>2')</code> →</p>                                                                                                                                                                                                                            |
| <p><code>exist</code> ( <code>hstore</code>, <code>text</code> ) → <code>boolean</code></p><p>Does <code>hstore</code> contain key?</p><p><code>exist('a=>1', 'a')</code> → <code>t</code></p>                                                                                                                                                                                                                                                                                                                                           |
| <p><code>defined</code> ( <code>hstore</code>, <code>text</code> ) → <code>boolean</code></p><p>Does <code>hstore</code> contain a non-<code>NULL</code> value for key?</p><p><code>defined('a=>NULL', 'a')</code> → <code>f</code></p>                                                                                                                                                                                                                                                                                                  |
| <p><code>delete</code> ( <code>hstore</code>, <code>text</code> ) → <code>hstore</code></p><p>Deletes pair with matching key.</p><p><code>delete('a=>1,b=>2', 'b')</code> → <code>"a"=>"1"</code></p>                                                                                                                                                                                                                                                                                                                                    |
| <p><code>delete</code> ( <code>hstore</code>, <code>text[]</code> ) → <code>hstore</code></p><p>Deletes pairs with matching keys.</p><p><code>delete('a=>1,b=>2,c=>3', ARRAY['a','b'])</code> → <code>"c"=>"3"</code></p>                                                                                                                                                                                                                                                                                                                |
| <p><code>delete</code> ( <code>hstore</code>, <code>hstore</code> ) → <code>hstore</code></p><p>Deletes pairs matching those in the second argument.</p><p><code>delete('a=>1,b=>2', 'a=>4,b=>2'::hstore)</code> → <code>"a"=>"1"</code></p>                                                                                                                                                                                                                                                                                             |
| <p><code>populate_record</code> ( <code>anyelement</code>, <code>hstore</code> ) → <code>anyelement</code></p><p>Replaces fields in the left operand (which must be a composite type) with matching values from <code>hstore</code>.</p><p><code>populate_record(ROW(1,2), 'f1=>42'::hstore)</code> → <code>(42,2)</code></p>                                                                                                                                                                                                            |

In addition to these operators and functions, values of the `hstore` type can be subscripted, allowing them to act like associative arrays. Only a single subscript of type `text` can be specified; it is interpreted as a key and the corresponding value is fetched or stored. For example,

```
CREATE TABLE mytable (h hstore);
INSERT INTO mytable VALUES ('a=>b, c=>d');
SELECT h['a'] FROM mytable;
 h
---
 b
(1 row)

UPDATE mytable SET h['c'] = 'new';
SELECT h FROM mytable;
          h
----------------------
 "a"=>"b", "c"=>"new"
(1 row)
```

A subscripted fetch returns `NULL` if the subscript is `NULL` or that key does not exist in the `hstore`. (Thus, a subscripted fetch is not greatly different from the `->` operator.) A subscripted update fails if the subscript is `NULL`; otherwise, it replaces the value for that key, adding an entry to the `hstore` if the key does not already exist.

## F.16.3. Indexes

`hstore` has GiST and GIN index support for the `@>`, `?`, `?&` and `?|` operators. For example:

```
CREATE INDEX hidx ON testhstore USING GIST (h);

CREATE INDEX hidx ON testhstore USING GIN (h);
```

`gist_hstore_ops` GiST opclass approximates a set of key/value pairs as a bitmap signature. Its optional integer parameter `siglen` determines the signature length in bytes. The default length is 16 bytes. Valid values of signature length are between 1 and 2024 bytes. Longer signatures lead to a more precise search (scanning a smaller fraction of the index and fewer heap pages), at the cost of a larger index.

Example of creating such an index with a signature length of 32 bytes:

```
CREATE INDEX hidx ON testhstore USING GIST (h gist_hstore_ops(siglen=32));
```

`hstore` also supports `btree` or `hash` indexes for the `=` operator. This allows `hstore` columns to be declared `UNIQUE`, or to be used in `GROUP BY`, `ORDER BY` or `DISTINCT` expressions. The sort ordering for `hstore` values is not particularly useful, but these indexes may be useful for equivalence lookups. Create indexes for `=` comparisons as follows:

```
CREATE INDEX hidx ON testhstore USING BTREE (h);

CREATE INDEX hidx ON testhstore USING HASH (h);
```

## F.16.4. Examples

Add a key, or update an existing key with a new value:

```
UPDATE tab SET h['c'] = '3';
```

Another way to do the same thing is:

```
UPDATE tab SET h = h || hstore('c', '3');
```

If multiple keys are to be added or changed in one operation, the concatenation approach is more efficient than subscripting:

```
UPDATE tab SET h = h || hstore(array['q', 'w'], array['11', '12']);
```

Delete a key:

```
UPDATE tab SET h = delete(h, 'k1');
```

Convert a `record` to an `hstore`:

```
CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT hstore(t) FROM test AS t;
                   hstore                    
---------------------------------------------
 "col1"=>"123", "col2"=>"foo", "col3"=>"bar"
(1 row)
```

Convert an `hstore` to a predefined `record` type:

```
CREATE TABLE test (col1 integer, col2 text, col3 text);

SELECT * FROM populate_record(null::test,
                              '"col1"=>"456", "col2"=>"zzz"');
 col1 | col2 | col3 
------+------+------
  456 | zzz  | 
(1 row)
```

Modify an existing record using the values from an `hstore`:

```
CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT (r).* FROM (SELECT t #= '"col3"=>"baz"' AS r FROM test t) s;
 col1 | col2 | col3 
------+------+------
  123 | foo  | baz
(1 row)
```

## F.16.5. Statistics

The `hstore` type, because of its intrinsic liberality, could contain a lot of different keys. Checking for valid keys is the task of the application. The following examples demonstrate several techniques for checking keys and obtaining statistics.

Simple example:

```
SELECT * FROM each('aaa=>bq, b=>NULL, ""=>1');
```

Using a table:

```
CREATE TABLE stat AS SELECT (each(h)).key, (each(h)).value FROM testhstore;
```

Online statistics:

```
SELECT key, count(*) FROM
  (SELECT (each(h)).key FROM testhstore) AS stat
  GROUP BY key
  ORDER BY count DESC, key;
    key    | count
-----------+-------
 line      |   883
 query     |   207
 pos       |   203
 node      |   202
 space     |   197
 status    |   195
 public    |   194
 title     |   190
 org       |   189
...................
```

## F.16.6. Compatibility

As of PostgreSQL 9.0, `hstore` uses a different internal representation than previous versions. This presents no obstacle for dump/restore upgrades since the text representation (used in the dump) is unchanged.

In the event of a binary upgrade, upward compatibility is maintained by having the new code recognize old-format data. This will entail a slight performance penalty when processing data that has not yet been modified by the new code. It is possible to force an upgrade of all values in a table column by doing an `UPDATE` statement as follows:

```
UPDATE tablename SET hstorecol = hstorecol || '';
```

Another way to do it is:

```
ALTER TABLE tablename ALTER hstorecol TYPE hstore USING hstorecol || '';
```

The `ALTER TABLE` method requires an `ACCESS EXCLUSIVE` lock on the table, but does not result in bloating the table with old row versions.

## F.16.7. Transforms

Additional extensions are available that implement transforms for the `hstore` type for the languages PL/Perl and PL/Python. The extensions for PL/Perl are called `hstore_plperl` and `hstore_plperlu`, for trusted and untrusted PL/Perl. If you install these transforms and specify them when creating a function, `hstore` values are mapped to Perl hashes. The extensions for PL/Python are called `hstore_plpythonu`, `hstore_plpython2u`, and `hstore_plpython3u` (see [Section 46.1](https://www.postgresql.org/docs/14/plpython-python23.html) for the PL/Python naming convention). If you use them, `hstore` values are mapped to Python dictionaries.

#### Caution

It is strongly recommended that the transform extensions be installed in the same schema as `hstore`. Otherwise there are installation-time security hazards if a transform extension's schema contains objects defined by a hostile user.

## F.16.8. Authors

Oleg Bartunov `<`[`oleg@sai.msu.su`](mailto:oleg@sai.msu.su)`>`, Moscow, Moscow University, Russia

Teodor Sigaev `<`[`teodor@sigaev.ru`](mailto:teodor@sigaev.ru)`>`, Moscow, Delta-Soft Ltd., Russia

Additional enhancements by Andrew Gierth `<`[`andrew@tao11.riddles.org.uk`](mailto:andrew@tao11.riddles.org.uk)`>`, United Kingdom
