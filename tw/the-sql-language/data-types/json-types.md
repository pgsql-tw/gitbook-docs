# 8.14. JSON 型別

JSON 資料型別用於儲存 [RFC 7159](https://tools.ietf.org/html/rfc7159) 中所規範的 JSON（JavaScript Object Notation）資料。此類資料也可以儲存為 text，但是 JSON 資料型別的優點是可以根據 JSON 規則強制讓每個儲存的值必須是有效的值 。對於這些資料型別中儲存的資料，還提供了各種特定於 JSON 的函數和運算子。 另請參閱[第 9.15 節](../functions-and-operators/json-functions-and-operators.md)。

PostgreSQL 提供了兩種儲存 JSON 資料的型別：json 和 jsonb。為了對這些資料型別實作有效的查詢機制，PostgreSQL 還提供了 [8.14.6 節](json-types.md#8-14-6-jsonpath-type)中所描述的 jsonpath 資料型別。

json 和 jsonb 資料型別接受幾乎相同的內容集合作為輸入。實際主要的差別是效率。json 資料型別儲存與輸入字串完全相同的內容，處理函數必須在每次執行時重新解析；jsonb 資料型別則以分解後的二進位格式儲存，由於增加了轉換成本，因此資料輸入的速度稍慢，但由於後續不需要解析，因此處理速度明顯加快。jsonb 還支援索引處理，這是一個很大的優勢。

因為 json 型別儲存與輸入字串完全相同的內容，所以它將保留標記之間語義上無關的空白以及 JSON 物件中鍵的順序。另外，如果 JSON 內容物件包含相同的鍵不只一次，則所有鍵/值對都會保留。（處理函數會將最後一個值視為可用的值。）相比之下，jsonb 不會保留空白，不會保留物件中鍵的順序，也不會保留物件中重複的鍵。如果在輸入中指定了重複的鍵，則僅保留最後一個值。

通常，大多數應用程序應該將 JSON 資料儲存為 jsonb，除非有非常特殊的需求，例如關於物件中鍵的順序有一些傳統上的假設。

由於 PostgreSQL 每個資料庫只允許一種字元集的編碼。因此，除非資料庫編碼為 UTF8，否則 JSON 型別不可能嚴格符合 JSON 規範。嘗試直接使用資料庫編碼中無法表示的字元會失敗；相反，character 型別則允許使用可以在資料庫編碼中表示但不能以 UTF8 表示的字元。

RFC 7159 允許 JSON 字串包含 \uXXXX 所表示的 Unicode 轉譯序列。在 json 型別的輸入函數中，無論資料庫編碼如何，都允許 Unicode 轉譯，並且僅檢查語法正確性（即，四個十六進位數字跟在 \u 之後）。但是，jsonb 的輸入函數更嚴格：除非資料庫編碼為 UTF8，否則它不允許非 ASCII 字元（U+007F 以上的字元）使用 Unicode 轉譯。jsonb 型別也拒絕 \u0000（因為無法在 PostgreSQL 的 text 型別中表現），並且堅持認為使用 Unicode surrogate pair 對來指定 Unicode Basic Multilingual Plane 之外的字元都是正確的。有效的 Unicode 轉譯會轉換為等效的 ASCII 或 UTF8 字元進行儲存； 這包括將 surrogate pair 折疊為單個字元。

**注意**  
第 9.15 節中描述的許多 JSON 處理函數會將 Unicode 轉譯為一般字元，因此，即使輸入型別為 json 而不是 jsonb，它們也會拋出與上述類型相同的錯誤。json 輸入函數不進行這些檢查的事實可能被認為是歷史共業，儘管它確實允許以非 UTF8 資料庫編碼的形式簡單儲存（毋須處理）JSON Unicode 轉譯。 通常，如果可以的話，最好避免將 JSON 中的 Unicode 轉譯與非 UTF8 資料庫編碼混在一起。

將字串 JSON 輸入轉換為 jsonb 時，RFC 7159 描述的原始型別將會有效地對應到內建的 PostgreSQL 型別，如 Table 8.23 所示。因此，對於構成有效 jsonb 資料的內容存在一些較小的附加約束條件，這些約束條件既不適用於 json 型別，也不適用於抽象上 JSON，這對應於基礎資料型別可以表示的內容限制。值得注意的是，jsonb 會拒絕 PostgreSQL 數字資料型別範圍之外的數字，而 json 不會。RFC 7159 允許此類實作定義限制。但是，實際上，在其他實作中更容易出現此類問題，因為通常將 JSON 的數字基本型別表示為 IEEE 754 雙精確度浮點數（RFC 7159 明確預期了這一點且允許）。當使用 JSON 作為此類系統的交換格式時，應考慮與 PostgreSQL 最初儲存的資料相比較，可能會有失去數字精確度的風險。

相反，如下表中所示，JSON 基本型別的輸入格式有一些微小的限制，但並不適用於其相應的 PostgreSQL 資料型別。

#### **Table 8.23. JSON Primitive Types and Corresponding PostgreSQL Types**

| JSON primitive type | PostgreSQL type | Notes |
| :--- | :--- | :--- |
| `string` | `text` | 禁止使用 \u0000，如果資料庫編碼不是 UTF8，則不允許使用非 ASCII Unicode 轉譯 |
| `number` | `numeric` | 不允許使用 NaN 和 infinity |
| `boolean` | `boolean` | 僅接受小寫的 true 和 false |
| `null` | \(none\) | 與 SQL NULL 是不同的概念 |

## 8.14.1. JSON Input and Output Syntax

JSON 資料型別的輸入/輸出語法被規範在 RFC 7159 之中。

以下是所有有效的 json（或 jsonb）表示式：

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

如前所述，當輸入 JSON 內容然後在不進行任何其他處理的情況下進行輸出時，json 輸出與輸入相同的內容，而 jsonb 則不會保留與語義無關的細節，像是空格。例如，請注意此處的差別：

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

值得注意的一個語義無關的細節是，在 jsonb 中，數字將根據基本數字型別的行為進行輸出。實際上，這意味著使用 E 記號輸入的數字將不會以原輸出形式輸出，例如：

```text
SELECT '{"reading": 1.230e-5}'::json, '{"reading": 1.230e-5}'::jsonb;
         json          |          jsonb          
-----------------------+-------------------------
 {"reading": 1.230e-5} | {"reading": 0.00001230}
(1 row)
```

但是，jsonb 將保留小數尾巴的數字零，如在本範例中所示，即使它們在語義上無意義（例如，相等運算），也是如此。

有關可用於建構和處理 JSON 內容的內建函數和運算子的列表，請參閱[第 9.15 節](../functions-and-operators/json-functions-and-operators.md)。

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

jsonpath 型別實現了 PostgreSQL 中對 SQL/JSON 路徑語法的支援，以有效地查詢 JSON 資料。它提供以二元運算的形式來使用已解析的 SQL/JSON 路徑表示式，此表示式讓路徑引擎從 JSON 資料檢索的項目取出內容，以供 SQL/JSON 查詢函數進一步處理。

SQL / JSON 路徑 predicate 和運算子的語義基本遵循 SQL 標準。同時，為了提供使用 JSON 資料的更自然的方式，SQL/JSON 路徑語法使用了一些 JavaScript 約定：

* 點（.）用於資料成員存取。
* 中括號（\[ \]）用於陣列存取。
* 與從 1 開始的一般 SQL 陣列不同，SQL/JSON 陣列是 從 0 開始。

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

