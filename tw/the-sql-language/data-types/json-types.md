# 8.14. JSON 型別

JSON data types are for storing JSON \(JavaScript Object Notation\) data, as specified in [RFC 7159](https://tools.ietf.org/html/rfc7159). Such data can also be stored as `text`, but the JSON data types have the advantage of enforcing that each stored value is valid according to the JSON rules. There are also assorted JSON-specific functions and operators available for data stored in these data types; see [Section 9.15](https://www.postgresql.org/docs/12/functions-json.html).

PostgreSQL offers two types for storing JSON data: `json` and `jsonb`. To implement efficient query mechanisms for these data types, PostgreSQL also provides the `jsonpath` data type described in [Section 8.14.6](https://www.postgresql.org/docs/12/datatype-json.html#DATATYPE-JSONPATH).

The `json` and `jsonb` data types accept _almost_ identical sets of values as input. The major practical difference is one of efficiency. The `json` data type stores an exact copy of the input text, which processing functions must reparse on each execution; while `jsonb` data is stored in a decomposed binary format that makes it slightly slower to input due to added conversion overhead, but significantly faster to process, since no reparsing is needed. `jsonb` also supports indexing, which can be a significant advantage.

Because the `json` type stores an exact copy of the input text, it will preserve semantically-insignificant white space between tokens, as well as the order of keys within JSON objects. Also, if a JSON object within the value contains the same key more than once, all the key/value pairs are kept. \(The processing functions consider the last value as the operative one.\) By contrast, `jsonb` does not preserve white space, does not preserve the order of object keys, and does not keep duplicate object keys. If duplicate keys are specified in the input, only the last value is kept.

In general, most applications should prefer to store JSON data as `jsonb`, unless there are quite specialized needs, such as legacy assumptions about ordering of object keys.

PostgreSQL allows only one character set encoding per database. It is therefore not possible for the JSON types to conform rigidly to the JSON specification unless the database encoding is UTF8. Attempts to directly include characters that cannot be represented in the database encoding will fail; conversely, characters that can be represented in the database encoding but not in UTF8 will be allowed.

RFC 7159 permits JSON strings to contain Unicode escape sequences denoted by `\u`_`XXXX`_. In the input function for the `json` type, Unicode escapes are allowed regardless of the database encoding, and are checked only for syntactic correctness \(that is, that four hex digits follow `\u`\). However, the input function for `jsonb` is stricter: it disallows Unicode escapes for non-ASCII characters \(those above `U+007F`\) unless the database encoding is UTF8. The `jsonb` type also rejects `\u0000` \(because that cannot be represented in PostgreSQL's `text` type\), and it insists that any use of Unicode surrogate pairs to designate characters outside the Unicode Basic Multilingual Plane be correct. Valid Unicode escapes are converted to the equivalent ASCII or UTF8 character for storage; this includes folding surrogate pairs into a single character.

#### Note

Many of the JSON processing functions described in [Section 9.15](https://www.postgresql.org/docs/12/functions-json.html) will convert Unicode escapes to regular characters, and will therefore throw the same types of errors just described even if their input is of type `json` not `jsonb`. The fact that the `json` input function does not make these checks may be considered a historical artifact, although it does allow for simple storage \(without processing\) of JSON Unicode escapes in a non-UTF8 database encoding. In general, it is best to avoid mixing Unicode escapes in JSON with a non-UTF8 database encoding, if possible.

When converting textual JSON input into `jsonb`, the primitive types described by RFC 7159 are effectively mapped onto native PostgreSQL types, as shown in [Table 8.23](https://www.postgresql.org/docs/12/datatype-json.html#JSON-TYPE-MAPPING-TABLE). Therefore, there are some minor additional constraints on what constitutes valid `jsonb` data that do not apply to the `json` type, nor to JSON in the abstract, corresponding to limits on what can be represented by the underlying data type. Notably, `jsonb` will reject numbers that are outside the range of the PostgreSQL `numeric` data type, while `json` will not. Such implementation-defined restrictions are permitted by RFC 7159. However, in practice such problems are far more likely to occur in other implementations, as it is common to represent JSON's `number` primitive type as IEEE 754 double precision floating point \(which RFC 7159 explicitly anticipates and allows for\). When using JSON as an interchange format with such systems, the danger of losing numeric precision compared to data originally stored by PostgreSQL should be considered.

Conversely, as noted in the table there are some minor restrictions on the input format of JSON primitive types that do not apply to the corresponding PostgreSQL types.

#### **Table 8.23. JSON Primitive Types and Corresponding PostgreSQL Types**

| JSON primitive type | PostgreSQL type | Notes |
| :--- | :--- | :--- |
| `string` | `text` | `\u0000` is disallowed, as are non-ASCII Unicode escapes if database encoding is not UTF8 |
| `number` | `numeric` | `NaN` and `infinity` values are disallowed |
| `boolean` | `boolean` | Only lowercase `true` and `false` spellings are accepted |
| `null` | \(none\) | SQL `NULL` is a different concept |

## 8.14.1. JSON Input and Output Syntax

The input/output syntax for the JSON data types is as specified in RFC 7159.

The following are all valid `json` \(or `jsonb`\) expressions:

```text
-- Simple scalar/primitive value
-- Primitive values can be numbers, quoted strings, true, false, or null
SELECT '5'::json;

-- Array of zero or more elements (elements need not be of same type)
SELECT '[1, 2, "foo", null]'::json;

-- Object containing pairs of keys and values
-- Note that object keys must always be quoted strings
SELECT '{"bar": "baz", "balance": 7.77, "active": false}'::json;

-- Arrays and objects can be nested arbitrarily
SELECT '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json;
```

As previously stated, when a JSON value is input and then printed without any additional processing, `json` outputs the same text that was input, while `jsonb` does not preserve semantically-insignificant details such as whitespace. For example, note the differences here:

```text
SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::json;
                      json                       
-------------------------------------------------
 {"bar": "baz", "balance": 7.77, "active":false}
(1 row)

SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::jsonb;
                      jsonb                       
--------------------------------------------------
 {"bar": "baz", "active": false, "balance": 7.77}
(1 row)
```

One semantically-insignificant detail worth noting is that in `jsonb`, numbers will be printed according to the behavior of the underlying `numeric` type. In practice this means that numbers entered with `E` notation will be printed without it, for example:

```text
SELECT '{"reading": 1.230e-5}'::json, '{"reading": 1.230e-5}'::jsonb;
         json          |          jsonb          
-----------------------+-------------------------
 {"reading": 1.230e-5} | {"reading": 0.00001230}
(1 row)
```

However, `jsonb` will preserve trailing fractional zeroes, as seen in this example, even though those are semantically insignificant for purposes such as equality checks.

For the list of built-in functions and operators available for constructing and processing JSON values, see [Section 9.15](https://www.postgresql.org/docs/12/functions-json.html).

## 8.14.2. Designing JSON Documents

Representing data as JSON can be considerably more flexible than the traditional relational data model, which is compelling in environments where requirements are fluid. It is quite possible for both approaches to co-exist and complement each other within the same application. However, even for applications where maximal flexibility is desired, it is still recommended that JSON documents have a somewhat fixed structure. The structure is typically unenforced \(though enforcing some business rules declaratively is possible\), but having a predictable structure makes it easier to write queries that usefully summarize a set of “documents” \(datums\) in a table.

JSON data is subject to the same concurrency-control considerations as any other data type when stored in a table. Although storing large documents is practicable, keep in mind that any update acquires a row-level lock on the whole row. Consider limiting JSON documents to a manageable size in order to decrease lock contention among updating transactions. Ideally, JSON documents should each represent an atomic datum that business rules dictate cannot reasonably be further subdivided into smaller datums that could be modified independently.

## 8.14.3. `jsonb` Containment and Existence

Testing _containment_ is an important capability of `jsonb`. There is no parallel set of facilities for the `json` type. Containment tests whether one `jsonb` document has contained within it another one. These examples return true except as noted:

```text
-- Simple scalar/primitive values contain only the identical value:
SELECT '"foo"'::jsonb @> '"foo"'::jsonb;

-- The array on the right side is contained within the one on the left:
SELECT '[1, 2, 3]'::jsonb @> '[1, 3]'::jsonb;

-- Order of array elements is not significant, so this is also true:
SELECT '[1, 2, 3]'::jsonb @> '[3, 1]'::jsonb;

-- Duplicate array elements don't matter either:
SELECT '[1, 2, 3]'::jsonb @> '[1, 2, 2]'::jsonb;

-- The object with a single pair on the right side is contained
-- within the object on the left side:
SELECT '{"product": "PostgreSQL", "version": 9.4, "jsonb": true}'::jsonb @> '{"version": 9.4}'::jsonb;

-- The array on the right side is not considered contained within the
-- array on the left, even though a similar array is nested within it:
SELECT '[1, 2, [1, 3]]'::jsonb @> '[1, 3]'::jsonb;  -- yields false

-- But with a layer of nesting, it is contained:
SELECT '[1, 2, [1, 3]]'::jsonb @> '[[1, 3]]'::jsonb;

-- Similarly, containment is not reported here:
SELECT '{"foo": {"bar": "baz"}}'::jsonb @> '{"bar": "baz"}'::jsonb;  -- yields false

-- A top-level key and an empty object is contained:
SELECT '{"foo": {"bar": "baz"}}'::jsonb @> '{"foo": {}}'::jsonb;
```

The general principle is that the contained object must match the containing object as to structure and data contents, possibly after discarding some non-matching array elements or object key/value pairs from the containing object. But remember that the order of array elements is not significant when doing a containment match, and duplicate array elements are effectively considered only once.

As a special exception to the general principle that the structures must match, an array may contain a primitive value:

```text
-- This array contains the primitive string value:
SELECT '["foo", "bar"]'::jsonb @> '"bar"'::jsonb;

-- This exception is not reciprocal -- non-containment is reported here:
SELECT '"bar"'::jsonb @> '["bar"]'::jsonb;  -- yields false
```

`jsonb` also has an _existence_ operator, which is a variation on the theme of containment: it tests whether a string \(given as a `text` value\) appears as an object key or array element at the top level of the `jsonb` value. These examples return true except as noted:

```text
-- String exists as array element:
SELECT '["foo", "bar", "baz"]'::jsonb ? 'bar';

-- String exists as object key:
SELECT '{"foo": "bar"}'::jsonb ? 'foo';

-- Object values are not considered:
SELECT '{"foo": "bar"}'::jsonb ? 'bar';  -- yields false

-- As with containment, existence must match at the top level:
SELECT '{"foo": {"bar": "baz"}}'::jsonb ? 'bar'; -- yields false

-- A string is considered to exist if it matches a primitive JSON string:
SELECT '"foo"'::jsonb ? 'foo';
```

JSON objects are better suited than arrays for testing containment or existence when there are many keys or elements involved, because unlike arrays they are internally optimized for searching, and do not need to be searched linearly.

#### Tip

Because JSON containment is nested, an appropriate query can skip explicit selection of sub-objects. As an example, suppose that we have a `doc` column containing objects at the top level, with most objects containing `tags` fields that contain arrays of sub-objects. This query finds entries in which sub-objects containing both `"term":"paris"` and `"term":"food"` appear, while ignoring any such keys outside the `tags` array:

```text
SELECT doc->'site_name' FROM websites
  WHERE doc @> '{"tags":[{"term":"paris"}, {"term":"food"}]}';
```

One could accomplish the same thing with, say,

```text
SELECT doc->'site_name' FROM websites
  WHERE doc->'tags' @> '[{"term":"paris"}, {"term":"food"}]';
```

but that approach is less flexible, and often less efficient as well.

On the other hand, the JSON existence operator is not nested: it will only look for the specified key or array element at top level of the JSON value.

The various containment and existence operators, along with all other JSON operators and functions are documented in [Section 9.15](https://www.postgresql.org/docs/12/functions-json.html).

## 8.14.4. `jsonb` Indexing

GIN indexes can be used to efficiently search for keys or key/value pairs occurring within a large number of `jsonb` documents \(datums\). Two GIN “operator classes” are provided, offering different performance and flexibility trade-offs.

The default GIN operator class for `jsonb` supports queries with top-level key-exists operators `?`, `?&` and `?|` operators and path/value-exists operator `@>`. \(For details of the semantics that these operators implement, see [Table 9.45](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-JSONB-OP-TABLE).\) An example of creating an index with this operator class is:

```text
CREATE INDEX idxgin ON api USING GIN (jdoc);
```

The non-default GIN operator class `jsonb_path_ops` supports indexing the `@>` operator only. An example of creating an index with this operator class is:

```text
CREATE INDEX idxginp ON api USING GIN (jdoc jsonb_path_ops);
```

Consider the example of a table that stores JSON documents retrieved from a third-party web service, with a documented schema definition. A typical document is:

```text
{
    "guid": "9c36adc1-7fb5-4d5b-83b4-90356a46061a",
    "name": "Angela Barton",
    "is_active": true,
    "company": "Magnafone",
    "address": "178 Howard Place, Gulf, Washington, 702",
    "registered": "2009-11-07T08:53:22 +08:00",
    "latitude": 19.793713,
    "longitude": 86.513373,
    "tags": [
        "enim",
        "aliquip",
        "qui"
    ]
}
```

We store these documents in a table named `api`, in a `jsonb` column named `jdoc`. If a GIN index is created on this column, queries like the following can make use of the index:

```text
-- Find documents in which the key "company" has value "Magnafone"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"company": "Magnafone"}';
```

However, the index could not be used for queries like the following, because though the operator `?` is indexable, it is not applied directly to the indexed column `jdoc`:

```text
-- Find documents in which the key "tags" contains key or array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc -> 'tags' ? 'qui';
```

Still, with appropriate use of expression indexes, the above query can use an index. If querying for particular items within the `"tags"` key is common, defining an index like this may be worthwhile:

```text
CREATE INDEX idxgintags ON api USING GIN ((jdoc -> 'tags'));
```

Now, the `WHERE` clause `jdoc -> 'tags' ? 'qui'` will be recognized as an application of the indexable operator `?` to the indexed expression `jdoc -> 'tags'`. \(More information on expression indexes can be found in [Section 11.7](https://www.postgresql.org/docs/12/indexes-expressional.html).\)

Also, GIN index supports `@@` and `@?` operators, which perform `jsonpath` matching.

```text
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @@ '$.tags[*] == "qui"';
```

```text
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @@ '$.tags[*] ? (@ == "qui")';
```

GIN index extracts statements of following form out of `jsonpath`: _`accessors_chain`_ = _`const`_. Accessors chain may consist of `.key`, `[*]`, and `[`_`index`_\] accessors. `jsonb_ops` additionally supports `.*` and `.**` accessors.

Another approach to querying is to exploit containment, for example:

```text
-- Find documents in which the key "tags" contains array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"tags": ["qui"]}';
```

A simple GIN index on the `jdoc` column can support this query. But note that such an index will store copies of every key and value in the `jdoc` column, whereas the expression index of the previous example stores only data found under the `tags` key. While the simple-index approach is far more flexible \(since it supports queries about any key\), targeted expression indexes are likely to be smaller and faster to search than a simple index.

Although the `jsonb_path_ops` operator class supports only queries with the `@>`, `@@` and `@?` operators, it has notable performance advantages over the default operator class `jsonb_ops`. A `jsonb_path_ops` index is usually much smaller than a `jsonb_ops` index over the same data, and the specificity of searches is better, particularly when queries contain keys that appear frequently in the data. Therefore search operations typically perform better than with the default operator class.

The technical difference between a `jsonb_ops` and a `jsonb_path_ops` GIN index is that the former creates independent index items for each key and value in the data, while the latter creates index items only for each value in the data. [\[6\]](https://www.postgresql.org/docs/12/datatype-json.html#ftn.id-1.5.7.22.18.9.3) Basically, each `jsonb_path_ops` index item is a hash of the value and the key\(s\) leading to it; for example to index `{"foo": {"bar": "baz"}}`, a single index item would be created incorporating all three of `foo`, `bar`, and `baz` into the hash value. Thus a containment query looking for this structure would result in an extremely specific index search; but there is no way at all to find out whether `foo` appears as a key. On the other hand, a `jsonb_ops` index would create three index items representing `foo`, `bar`, and `baz` separately; then to do the containment query, it would look for rows containing all three of these items. While GIN indexes can perform such an AND search fairly efficiently, it will still be less specific and slower than the equivalent `jsonb_path_ops` search, especially if there are a very large number of rows containing any single one of the three index items.

A disadvantage of the `jsonb_path_ops` approach is that it produces no index entries for JSON structures not containing any values, such as `{"a": {}}`. If a search for documents containing such a structure is requested, it will require a full-index scan, which is quite slow. `jsonb_path_ops` is therefore ill-suited for applications that often perform such searches.

`jsonb` also supports `btree` and `hash` indexes. These are usually useful only if it's important to check equality of complete JSON documents. The `btree` ordering for `jsonb` datums is seldom of great interest, but for completeness it is:

```text
Object > Array > Boolean > Number > String > Null

Object with n pairs > object with n - 1 pairs

Array with n elements > array with n - 1 elements
```

Objects with equal numbers of pairs are compared in the order:

```text
key-1, value-1, key-2 ...
```

Note that object keys are compared in their storage order; in particular, since shorter keys are stored before longer keys, this can lead to results that might be unintuitive, such as:

```text
{ "aa": 1, "c": 1} > {"b": 1, "d": 1}
```

Similarly, arrays with equal numbers of elements are compared in the order:

```text
element-1, element-2 ...
```

Primitive JSON values are compared using the same comparison rules as for the underlying PostgreSQL data type. Strings are compared using the default database collation.

## 8.14.5. Transforms

Additional extensions are available that implement transforms for the `jsonb` type for different procedural languages.

The extensions for PL/Perl are called `jsonb_plperl` and `jsonb_plperlu`. If you use them, `jsonb` values are mapped to Perl arrays, hashes, and scalars, as appropriate.

The extensions for PL/Python are called `jsonb_plpythonu`, `jsonb_plpython2u`, and `jsonb_plpython3u` \(see [Section 45.1](https://www.postgresql.org/docs/12/plpython-python23.html) for the PL/Python naming convention\). If you use them, `jsonb` values are mapped to Python dictionaries, lists, and scalars, as appropriate.

## 8.14.6. jsonpath Type

The `jsonpath` type implements support for the SQL/JSON path language in PostgreSQL to efficiently query JSON data. It provides a binary representation of the parsed SQL/JSON path expression that specifies the items to be retrieved by the path engine from the JSON data for further processing with the SQL/JSON query functions.

The semantics of SQL/JSON path predicates and operators generally follow SQL. At the same time, to provide a most natural way of working with JSON data, SQL/JSON path syntax uses some of the JavaScript conventions:

* Dot \(`.`\) is used for member access.
* Square brackets \(`[]`\) are used for array access.
* SQL/JSON arrays are 0-relative, unlike regular SQL arrays that start from 1.

An SQL/JSON path expression is typically written in an SQL query as an SQL character string literal, so it must be enclosed in single quotes, and any single quotes desired within the value must be doubled \(see [Section 4.1.2.1](https://www.postgresql.org/docs/12/sql-syntax-lexical.html#SQL-SYNTAX-STRINGS)\). Some forms of path expressions require string literals within them. These embedded string literals follow JavaScript/ECMAScript conventions: they must be surrounded by double quotes, and backslash escapes may be used within them to represent otherwise-hard-to-type characters. In particular, the way to write a double quote within an embedded string literal is `\"`, and to write a backslash itself, you must write `\\`. Other special backslash sequences include those recognized in JSON strings: `\b`, `\f`, `\n`, `\r`, `\t`, `\v` for various ASCII control characters, and `\u`_`NNNN`_ for a Unicode character identified by its 4-hex-digit code point. The backslash syntax also includes two cases not allowed by JSON: `\x`_`NN`_ for a character code written with only two hex digits, and `\u{`_`N...`_} for a character code written with 1 to 6 hex digits.

A path expression consists of a sequence of path elements, which can be the following:

* Path literals of JSON primitive types: Unicode text, numeric, true, false, or null.
* Path variables listed in [Table 8.24](https://www.postgresql.org/docs/12/datatype-json.html#TYPE-JSONPATH-VARIABLES).
* Accessor operators listed in [Table 8.25](https://www.postgresql.org/docs/12/datatype-json.html#TYPE-JSONPATH-ACCESSORS).
* `jsonpath` operators and methods listed in [Section 9.15.2.3](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-PATH-OPERATORS)
* Parentheses, which can be used to provide filter expressions or define the order of path evaluation.

For details on using `jsonpath` expressions with SQL/JSON query functions, see [Section 9.15.2](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-PATH).

#### **Table 8.24. `jsonpath` Variables**

| Variable | Description |
| :--- | :--- |
| `$` | A variable representing the JSON text to be queried \(the _context item_\). |
| `$varname` | A named variable. Its value can be set by the parameter _`vars`_ of several JSON processing functions. See [Table 9.47](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-JSON-PROCESSING-TABLE) and its notes for details. |
| `@` | A variable representing the result of path evaluation in filter expressions. |

#### **Table 8.25. `jsonpath` Accessors**

<table>
  <thead>
    <tr>
      <th style="text-align:left">Accessor Operator</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>.</code><em><code>key</code></em>
        </p>
        <p><code>.&quot;$</code><em><code>varname</code></em>&quot;</p>
      </td>
      <td style="text-align:left">Member accessor that returns an object member with the specified key.
        If the key name is a named variable starting with <code>$</code> or does
        not meet the JavaScript rules of an identifier, it must be enclosed in
        double quotes as a character string literal.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>.*</code>
      </td>
      <td style="text-align:left">Wildcard member accessor that returns the values of all members located
        at the top level of the current object.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>.**</code>
      </td>
      <td style="text-align:left">Recursive wildcard member accessor that processes all levels of the JSON
        hierarchy of the current object and returns all the member values, regardless
        of their nesting level. This is a PostgreSQL extension of the SQL/JSON
        standard.</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>.**{</code><em><code>level</code></em>}</p>
        <p><code>.**{</code><em><code>start_level</code></em> to <em><code>end_level</code></em>}</p>
      </td>
      <td style="text-align:left">Same as <code>.**</code>, but with a filter over nesting levels of JSON
        hierarchy. Nesting levels are specified as integers. Zero level corresponds
        to the current object. To access the lowest nesting level, you can use
        the <code>last</code> keyword. This is a PostgreSQL extension of the SQL/JSON
        standard.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>[</code><em><code>subscript</code></em>, ...]</td>
      <td style="text-align:left">
        <p>Array element accessor. <em><code>subscript</code></em> can be given in
          two forms: <em><code>index</code></em> or <em><code>start_index</code></em> to <em><code>end_index</code></em>.
          The first form returns a single array element by its index. The second
          form returns an array slice by the range of indexes, including the elements
          that correspond to the provided <em><code>start_index</code></em> and <em><code>end_index</code></em>.</p>
        <p>The specified <em><code>index</code></em> can be an integer, as well as
          an expression returning a single numeric value, which is automatically
          cast to integer. Zero index corresponds to the first array element. You
          can also use the <code>last</code> keyword to denote the last array element,
          which is useful for handling arrays of unknown length.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>[*]</code>
      </td>
      <td style="text-align:left">Wildcard array element accessor that returns all array elements.</td>
    </tr>
  </tbody>
</table>

[\[6\]](https://www.postgresql.org/docs/12/datatype-json.html#id-1.5.7.22.18.9.3) For this purpose, the term “value” includes array elements, though JSON terminology sometimes considers array elements distinct from values within objects.

