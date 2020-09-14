# 9.15. JSON 函式及運算子

本節描述的內容為：

* 用於處理和建立 JSON 資料的函數和運算子
* SQL/JSON 路徑語言

要了解有關 SQL/JSON 標準的更多資訊，請參閱 \[[sqltr-19075-6](../../bibliography.md#sqltr-19075-6-sql-technical-report-part-6-sql-support-for-javascript-object-notation-json-first-edition-2017)\]。有關於 PostgreSQL 支援的 JSON 型別的詳細資訊，請參閱[第 8.14 節](../data-types/json-types.md)。

## 9.15.1. Processing and Creating JSON Data

[Table 9.44](json-functions-and-operators.md#table-9-44-json-and-jsonb-operators) 列出了可用於 JSON 資料型別的運算子（請參閱[第 8.14 節](../data-types/json-types.md)）。

#### **Table 9.44. `json` and `jsonb` Operators**

| Operator | Right Operand Type | Return type | Description | Example | Example Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `->` | `int` | `json` or `jsonb` | Get JSON array element \(indexed from zero, negative integers count from the end\) | `'[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json->2` | `{"c":"baz"}` |
| `->` | `text` | `json` or `jsonb` | Get JSON object field by key | `'{"a": {"b":"foo"}}'::json->'a'` | `{"b":"foo"}` |
| `->>` | `int` | `text` | Get JSON array element as `text` | `'[1,2,3]'::json->>2` | `3` |
| `->>` | `text` | `text` | Get JSON object field as `text` | `'{"a":1,"b":2}'::json->>'b'` | `2` |
| `#>` | `text[]` | `json` or `jsonb` | Get JSON object at the specified path | `'{"a": {"b":{"c": "foo"}}}'::json#>'{a,b}'` | `{"c": "foo"}` |
| `#>>` | `text[]` | `text` | Get JSON object at the specified path as `text` | `'{"a":[1,2,3],"b":[4,5,6]}'::json#>>'{a,2}'` | `3` |

{% hint style="info" %}
這些運算子都有 json 和 jsonb 型別共用的變形。欄位/元素/路徑提取運算子回傳與其左側輸入相同的類型（json 或 jsonb），但指定為回傳 text 的運算符除外，這些運算子將結果強制轉換為 text。如果 JSON 輸入的結構不符合要求，則欄位/元素/路徑提取運算子將回傳 NULL 而不會失敗。例如，如果不存在這樣的元素。接受整數 JSON 陣列索引的欄位/元素/路徑提取運算子均支援表示從陣列末尾開始的負數索引值。
{% endhint %}

The standard comparison operators shown in [Table 9.1](https://www.postgresql.org/docs/12/functions-comparison.html#FUNCTIONS-COMPARISON-OP-TABLE) are available for `jsonb`, but not for `json`. They follow the ordering rules for B-tree operations outlined at [Section 8.14.4](https://www.postgresql.org/docs/12/datatype-json.html#JSON-INDEXING).

Some further operators also exist only for `jsonb`, as shown in [Table 9.45](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-JSONB-OP-TABLE). Many of these operators can be indexed by `jsonb` operator classes. For a full description of `jsonb` containment and existence semantics, see [Section 8.14.3](https://www.postgresql.org/docs/12/datatype-json.html#JSON-CONTAINMENT). [Section 8.14.4](https://www.postgresql.org/docs/12/datatype-json.html#JSON-INDEXING) describes how these operators can be used to effectively index `jsonb` data.

#### **Table 9.45. Additional `jsonb` Operators**

| Operator | Right Operand Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `@>` | `jsonb` | Does the left JSON value contain the right JSON path/value entries at the top level? | `'{"a":1, "b":2}'::jsonb @> '{"b":2}'::jsonb` |
| `<@` | `jsonb` | Are the left JSON path/value entries contained at the top level within the right JSON value? | `'{"b":2}'::jsonb <@ '{"a":1, "b":2}'::jsonb` |
| `?` | `text` | Does the _string_ exist as a top-level key within the JSON value? | `'{"a":1, "b":2}'::jsonb ? 'b'` |
| `?|` | `text[]` | Do any of these array _strings_ exist as top-level keys? | `'{"a":1, "b":2, "c":3}'::jsonb ?| array['b', 'c']` |
| `?&` | `text[]` | Do all of these array _strings_ exist as top-level keys? | `'["a", "b"]'::jsonb ?& array['a', 'b']` |
| `||` | `jsonb` | Concatenate two `jsonb` values into a new `jsonb` value | `'["a", "b"]'::jsonb || '["c", "d"]'::jsonb` |
| `-` | `text` | Delete key/value pair or _string_ element from left operand. Key/value pairs are matched based on their key value. | `'{"a": "b"}'::jsonb - 'a'` |
| `-` | `text[]` | Delete multiple key/value pairs or _string_ elements from left operand. Key/value pairs are matched based on their key value. | `'{"a": "b", "c": "d"}'::jsonb - '{a,c}'::text[]` |
| `-` | `integer` | Delete the array element with specified index \(Negative integers count from the end\). Throws an error if top level container is not an array. | `'["a", "b"]'::jsonb - 1` |
| `#-` | `text[]` | Delete the field or element with specified path \(for JSON arrays, negative integers count from the end\) | `'["a", {"b":1}]'::jsonb #- '{1,b}'` |
| `@?` | `jsonpath` | Does JSON path return any item for the specified JSON value? | `'{"a":[1,2,3,4,5]}'::jsonb @? '$.a[*] ? (@ > 2)'` |
| `@@` | `jsonpath` | Returns the result of JSON path predicate check for the specified JSON value. Only the first item of the result is taken into account. If the result is not Boolean, then `null` is returned. | `'{"a":[1,2,3,4,5]}'::jsonb @@ '$.a[*] > 2'` |

#### Note

The `||` operator concatenates the elements at the top level of each of its operands. It does not operate recursively. For example, if both operands are objects with a common key field name, the value of the field in the result will just be the value from the right hand operand.

#### Note

The `@?` and `@@` operators suppress the following errors: lacking object field or array element, unexpected JSON item type, and numeric errors. This behavior might be helpful while searching over JSON document collections of varying structure.

[Table 9.46](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-JSON-CREATION-TABLE) shows the functions that are available for creating `json` and `jsonb` values. \(There are no equivalent functions for `jsonb`, of the `row_to_json` and `array_to_json` functions. However, the `to_jsonb` function supplies much the same functionality as these functions would.\)

#### **Table 9.46. JSON Creation Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
      <th style="text-align:left">Example Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>to_json(anyelement)</code>
        </p>
        <p><code>to_jsonb(anyelement)</code>
        </p>
      </td>
      <td style="text-align:left">Returns the value as <code>json</code> or <code>jsonb</code>. Arrays and
        composites are converted (recursively) to arrays and objects; otherwise,
        if there is a cast from the type to <code>json</code>, the cast function
        will be used to perform the conversion; otherwise, a scalar value is produced.
        For any scalar type other than a number, a Boolean, or a null value, the
        text representation will be used, in such a fashion that it is a valid <code>json</code> or <code>jsonb</code> value.</td>
      <td
      style="text-align:left"><code>to_json(&apos;Fred said &quot;Hi.&quot;&apos;::text)</code>
        </td>
        <td style="text-align:left"><code>&quot;Fred said \&quot;Hi.\&quot;&quot;</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>array_to_json(anyarray [, pretty_bool])</code>
      </td>
      <td style="text-align:left">Returns the array as a JSON array. A PostgreSQL multidimensional array
        becomes a JSON array of arrays. Line feeds will be added between dimension-1
        elements if <em><code>pretty_bool</code></em> is true.</td>
      <td style="text-align:left"><code>array_to_json(&apos;{{1,5},{99,100}}&apos;::int[])</code>
      </td>
      <td style="text-align:left"><code>[[1,5],[99,100]]</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>row_to_json(record [, pretty_bool])</code>
      </td>
      <td style="text-align:left">Returns the row as a JSON object. Line feeds will be added between level-1
        elements if <em><code>pretty_bool</code></em> is true.</td>
      <td style="text-align:left"><code>row_to_json(row(1,&apos;foo&apos;))</code>
      </td>
      <td style="text-align:left"><code>{&quot;f1&quot;:1,&quot;f2&quot;:&quot;foo&quot;}</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_build_array(VARIADIC &quot;any&quot;)</code>
        </p>
        <p><code>jsonb_build_array(VARIADIC &quot;any&quot;)</code>
        </p>
      </td>
      <td style="text-align:left">Builds a possibly-heterogeneously-typed JSON array out of a variadic argument
        list.</td>
      <td style="text-align:left"><code>json_build_array(1,2,&apos;3&apos;,4,5)</code>
      </td>
      <td style="text-align:left"><code>[1, 2, &quot;3&quot;, 4, 5]</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_build_object(VARIADIC &quot;any&quot;)</code>
        </p>
        <p><code>jsonb_build_object(VARIADIC &quot;any&quot;)</code>
        </p>
      </td>
      <td style="text-align:left">Builds a JSON object out of a variadic argument list. By convention, the
        argument list consists of alternating keys and values.</td>
      <td style="text-align:left"><code>json_build_object(&apos;foo&apos;,1,&apos;bar&apos;,2)</code>
      </td>
      <td style="text-align:left"><code>{&quot;foo&quot;: 1, &quot;bar&quot;: 2}</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_object(text[])</code>
        </p>
        <p><code>jsonb_object(text[])</code>
        </p>
      </td>
      <td style="text-align:left">Builds a JSON object out of a text array. The array must have either exactly
        one dimension with an even number of members, in which case they are taken
        as alternating key/value pairs, or two dimensions such that each inner
        array has exactly two elements, which are taken as a key/value pair.</td>
      <td
      style="text-align:left">
        <p><code>json_object(&apos;{a, 1, b, &quot;def&quot;, c, 3.5}&apos;)</code>
        </p>
        <p><code>json_object(&apos;{{a, 1},{b, &quot;def&quot;},{c, 3.5}}&apos;)</code>
        </p>
        </td>
        <td style="text-align:left"><code>{&quot;a&quot;: &quot;1&quot;, &quot;b&quot;: &quot;def&quot;, &quot;c&quot;: &quot;3.5&quot;}</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_object(keys text[], values text[])</code>
        </p>
        <p><code>jsonb_object(keys text[], values text[])</code>
        </p>
      </td>
      <td style="text-align:left">This form of <code>json_object</code> takes keys and values pairwise from
        two separate arrays. In all other respects it is identical to the one-argument
        form.</td>
      <td style="text-align:left"><code>json_object(&apos;{a, b}&apos;, &apos;{1,2}&apos;)</code>
      </td>
      <td style="text-align:left"><code>{&quot;a&quot;: &quot;1&quot;, &quot;b&quot;: &quot;2&quot;}</code>
      </td>
    </tr>
  </tbody>
</table>

#### Note

`array_to_json` and `row_to_json` have the same behavior as `to_json` except for offering a pretty-printing option. The behavior described for `to_json` likewise applies to each individual value converted by the other JSON creation functions.

#### Note

The [hstore](https://www.postgresql.org/docs/12/hstore.html) extension has a cast from `hstore` to `json`, so that `hstore` values converted via the JSON creation functions will be represented as JSON objects, not as primitive string values.

[Table 9.47](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-JSON-PROCESSING-TABLE) shows the functions that are available for processing `json` and `jsonb` values.

#### **Table 9.47. JSON Processing Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Return Type</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
      <th style="text-align:left">Example Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>json_array_length(json)</code>
        </p>
        <p><code>jsonb_array_length(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>int</code>
      </td>
      <td style="text-align:left">Returns the number of elements in the outermost JSON array.</td>
      <td style="text-align:left"><code>json_array_length(&apos;[1,2,3,{&quot;f1&quot;:1,&quot;f2&quot;:[5,6]},4]&apos;)</code>
      </td>
      <td style="text-align:left"><code>5</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_each(json)</code>
        </p>
        <p><code>jsonb_each(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left">
        <p><code>setof key text, value json</code>
        </p>
        <p><code>setof key text, value jsonb</code>
        </p>
      </td>
      <td style="text-align:left">Expands the outermost JSON object into a set of key/value pairs.</td>
      <td
      style="text-align:left"><code>select * from json_each(&apos;{&quot;a&quot;:&quot;foo&quot;, &quot;b&quot;:&quot;bar&quot;}&apos;)</code>
        </td>
        <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_each_text(json)</code>
        </p>
        <p><code>jsonb_each_text(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>setof key text, value text</code>
      </td>
      <td style="text-align:left">Expands the outermost JSON object into a set of key/value pairs. The returned
        values will be of type <code>text</code>.</td>
      <td style="text-align:left"><code>select * from json_each_text(&apos;{&quot;a&quot;:&quot;foo&quot;, &quot;b&quot;:&quot;bar&quot;}&apos;)</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_extract_path(from_json json, VARIADIC path_elems text[])</code>
        </p>
        <p><code>jsonb_extract_path(from_json jsonb, VARIADIC path_elems text[])</code>
        </p>
      </td>
      <td style="text-align:left">
        <p><code>json</code>
        </p>
        <p><code>jsonb</code>
        </p>
      </td>
      <td style="text-align:left">Returns JSON value pointed to by <em><code>path_elems</code></em> (equivalent
        to <code>#&gt;</code> operator).</td>
      <td style="text-align:left"><code>json_extract_path(&apos;{&quot;f2&quot;:{&quot;f3&quot;:1},&quot;f4&quot;:{&quot;f5&quot;:99,&quot;f6&quot;:&quot;foo&quot;}}&apos;,&apos;f4&apos;)</code>
      </td>
      <td style="text-align:left"><code>{&quot;f5&quot;:99,&quot;f6&quot;:&quot;foo&quot;}</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_extract_path_text(from_json json, VARIADIC path_elems text[])</code>
        </p>
        <p><code>jsonb_extract_path_text(from_json jsonb, VARIADIC path_elems text[])</code>
        </p>
      </td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Returns JSON value pointed to by <em><code>path_elems</code></em> as <code>text</code> (equivalent
        to <code>#&gt;&gt;</code> operator).</td>
      <td style="text-align:left"><code>json_extract_path_text(&apos;{&quot;f2&quot;:{&quot;f3&quot;:1},&quot;f4&quot;:{&quot;f5&quot;:99,&quot;f6&quot;:&quot;foo&quot;}}&apos;,&apos;f4&apos;, &apos;f6&apos;)</code>
      </td>
      <td style="text-align:left"><code>foo</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_object_keys(json)</code>
        </p>
        <p><code>jsonb_object_keys(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>setof text</code>
      </td>
      <td style="text-align:left">Returns set of keys in the outermost JSON object.</td>
      <td style="text-align:left"><code>json_object_keys(&apos;{&quot;f1&quot;:&quot;abc&quot;,&quot;f2&quot;:{&quot;f3&quot;:&quot;a&quot;, &quot;f4&quot;:&quot;b&quot;}}&apos;)</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_populate_record(base anyelement, from_json json)</code>
        </p>
        <p><code>jsonb_populate_record(base anyelement, from_json jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>anyelement</code>
      </td>
      <td style="text-align:left">Expands the object in <em><code>from_json</code></em> to a row whose columns
        match the record type defined by <em><code>base</code></em> (see note below).</td>
      <td
      style="text-align:left"><code>select * from json_populate_record(null::myrowtype, &apos;{&quot;a&quot;: 1, &quot;b&quot;: [&quot;2&quot;, &quot;a b&quot;], &quot;c&quot;: {&quot;d&quot;: 4, &quot;e&quot;: &quot;a b c&quot;}}&apos;)</code>
        </td>
        <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_populate_recordset(base anyelement, from_json json)</code>
        </p>
        <p><code>jsonb_populate_recordset(base anyelement, from_json jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>setof anyelement</code>
      </td>
      <td style="text-align:left">Expands the outermost array of objects in <em><code>from_json</code></em> to
        a set of rows whose columns match the record type defined by <em><code>base</code></em> (see
        note below).</td>
      <td style="text-align:left"><code>select * from json_populate_recordset(null::myrowtype, &apos;[{&quot;a&quot;:1,&quot;b&quot;:2},{&quot;a&quot;:3,&quot;b&quot;:4}]&apos;)</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_array_elements(json)</code>
        </p>
        <p><code>jsonb_array_elements(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left">
        <p><code>setof json</code>
        </p>
        <p><code>setof jsonb</code>
        </p>
      </td>
      <td style="text-align:left">Expands a JSON array to a set of JSON values.</td>
      <td style="text-align:left"><code>select * from json_array_elements(&apos;[1,true, [2,false]]&apos;)</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_array_elements_text(json)</code>
        </p>
        <p><code>jsonb_array_elements_text(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>setof text</code>
      </td>
      <td style="text-align:left">Expands a JSON array to a set of <code>text</code> values.</td>
      <td style="text-align:left"><code>select * from json_array_elements_text(&apos;[&quot;foo&quot;, &quot;bar&quot;]&apos;)</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_typeof(json)</code>
        </p>
        <p><code>jsonb_typeof(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Returns the type of the outermost JSON value as a text string. Possible
        types are <code>object</code>, <code>array</code>, <code>string</code>, <code>number</code>, <code>boolean</code>,
        and <code>null</code>.</td>
      <td style="text-align:left"><code>json_typeof(&apos;-123.4&apos;)</code>
      </td>
      <td style="text-align:left"><code>number</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_to_record(json)</code>
        </p>
        <p><code>jsonb_to_record(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>record</code>
      </td>
      <td style="text-align:left">Builds an arbitrary record from a JSON object (see note below). As with
        all functions returning <code>record</code>, the caller must explicitly
        define the structure of the record with an <code>AS</code> clause.</td>
      <td
      style="text-align:left"><code>select * from json_to_record(&apos;{&quot;a&quot;:1,&quot;b&quot;:[1,2,3],&quot;c&quot;:[1,2,3],&quot;e&quot;:&quot;bar&quot;,&quot;r&quot;: {&quot;a&quot;: 123, &quot;b&quot;: &quot;a b c&quot;}}&apos;) as x(a int, b text, c int[], d text, r myrowtype)</code>
        </td>
        <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_to_recordset(json)</code>
        </p>
        <p><code>jsonb_to_recordset(jsonb)</code>
        </p>
      </td>
      <td style="text-align:left"><code>setof record</code>
      </td>
      <td style="text-align:left">Builds an arbitrary set of records from a JSON array of objects (see note
        below). As with all functions returning <code>record</code>, the caller
        must explicitly define the structure of the record with an <code>AS</code> clause.</td>
      <td
      style="text-align:left"><code>select * from json_to_recordset(&apos;[{&quot;a&quot;:1,&quot;b&quot;:&quot;foo&quot;},{&quot;a&quot;:&quot;2&quot;,&quot;c&quot;:&quot;bar&quot;}]&apos;) as x(a int, b text);</code>
        </td>
        <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>json_strip_nulls(from_json json)</code>
        </p>
        <p><code>jsonb_strip_nulls(from_json jsonb)</code>
        </p>
      </td>
      <td style="text-align:left">
        <p><code>json</code>
        </p>
        <p><code>jsonb</code>
        </p>
      </td>
      <td style="text-align:left">Returns <em><code>from_json</code></em> with all object fields that have
        null values omitted. Other null values are untouched.</td>
      <td style="text-align:left"><code>json_strip_nulls(&apos;[{&quot;f1&quot;:1,&quot;f2&quot;:null},2,null,3]&apos;)</code>
      </td>
      <td style="text-align:left"><code>[{&quot;f1&quot;:1},2,null,3]</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_set(target jsonb, path text[], new_value jsonb [, create_missing boolean])</code>
      </td>
      <td style="text-align:left"><code>jsonb</code>
      </td>
      <td style="text-align:left">Returns <em><code>target</code></em> with the section designated by <em><code>path</code></em> replaced
        by <em><code>new_value</code></em>, or with <em><code>new_value</code></em> added
        if <em><code>create_missing</code></em> is true (default is <code>true</code>)
        and the item designated by <em><code>path</code></em> does not exist. As
        with the path oriented operators, negative integers that appear in <em><code>path</code></em> count
        from the end of JSON arrays.</td>
      <td style="text-align:left">
        <p><code>jsonb_set(&apos;[{&quot;f1&quot;:1,&quot;f2&quot;:null},2,null,3]&apos;, &apos;{0,f1}&apos;,&apos;[2,3,4]&apos;, false)</code>
        </p>
        <p><code>jsonb_set(&apos;[{&quot;f1&quot;:1,&quot;f2&quot;:null},2]&apos;, &apos;{0,f3}&apos;,&apos;[2,3,4]&apos;)</code>
        </p>
      </td>
      <td style="text-align:left">
        <p><code>[{&quot;f1&quot;:[2,3,4],&quot;f2&quot;:null},2,null,3]</code>
        </p>
        <p><code>[{&quot;f1&quot;: 1, &quot;f2&quot;: null, &quot;f3&quot;: [2, 3, 4]}, 2]</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_insert(target jsonb, path text[], new_value jsonb [, insert_after boolean])</code>
      </td>
      <td style="text-align:left"><code>jsonb</code>
      </td>
      <td style="text-align:left">Returns <em><code>target</code></em> with <em><code>new_value</code></em> inserted.
        If <em><code>target</code></em> section designated by <em><code>path</code></em> is
        in a JSONB array, <em><code>new_value</code></em> will be inserted before
        target or after if <em><code>insert_after</code></em> is true (default is <code>false</code>).
        If <em><code>target</code></em> section designated by <em><code>path</code></em> is
        in JSONB object, <em><code>new_value</code></em> will be inserted only if <em><code>target</code></em> does
        not exist. As with the path oriented operators, negative integers that
        appear in <em><code>path</code></em> count from the end of JSON arrays.</td>
      <td
      style="text-align:left">
        <p><code>jsonb_insert(&apos;{&quot;a&quot;: [0,1,2]}&apos;, &apos;{a, 1}&apos;, &apos;&quot;new_value&quot;&apos;)</code>
        </p>
        <p><code>jsonb_insert(&apos;{&quot;a&quot;: [0,1,2]}&apos;, &apos;{a, 1}&apos;, &apos;&quot;new_value&quot;&apos;, true)</code>
        </p>
        </td>
        <td style="text-align:left">
          <p><code>{&quot;a&quot;: [0, &quot;new_value&quot;, 1, 2]}</code>
          </p>
          <p><code>{&quot;a&quot;: [0, 1, &quot;new_value&quot;, 2]}</code>
          </p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_pretty(from_json jsonb)</code>
      </td>
      <td style="text-align:left"><code>text</code>
      </td>
      <td style="text-align:left">Returns <em><code>from_json</code></em> as indented JSON text.</td>
      <td style="text-align:left"><code>jsonb_pretty(&apos;[{&quot;f1&quot;:1,&quot;f2&quot;:null},2,null,3]&apos;)</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_path_exists(target jsonb, path jsonpath [, vars jsonb [, silent bool]])</code>
      </td>
      <td style="text-align:left"><code>boolean</code>
      </td>
      <td style="text-align:left">Checks whether JSON path returns any item for the specified JSON value.</td>
      <td
      style="text-align:left"><code>jsonb_path_exists(&apos;{&quot;a&quot;:[1,2,3,4,5]}&apos;, &apos;$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)&apos;, &apos;{&quot;min&quot;:2,&quot;max&quot;:4}&apos;)</code>
        </td>
        <td style="text-align:left"><code>true</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_path_match(target jsonb, path jsonpath [, vars jsonb [, silent bool]])</code>
      </td>
      <td style="text-align:left"><code>boolean</code>
      </td>
      <td style="text-align:left">Returns the result of JSON path predicate check for the specified JSON
        value. Only the first item of the result is taken into account. If the
        result is not Boolean, then <code>null</code> is returned.</td>
      <td style="text-align:left"><code>jsonb_path_match(&apos;{&quot;a&quot;:[1,2,3,4,5]}&apos;, &apos;exists($.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max))&apos;, &apos;{&quot;min&quot;:2,&quot;max&quot;:4}&apos;)</code>
      </td>
      <td style="text-align:left"><code>true</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_path_query(target jsonb, path jsonpath [, vars jsonb [, silent bool]])</code>
      </td>
      <td style="text-align:left"><code>setof jsonb</code>
      </td>
      <td style="text-align:left">Gets all JSON items returned by JSON path for the specified JSON value.</td>
      <td
      style="text-align:left"><code>select * from jsonb_path_query(&apos;{&quot;a&quot;:[1,2,3,4,5]}&apos;, &apos;$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)&apos;, &apos;{&quot;min&quot;:2,&quot;max&quot;:4}&apos;);</code>
        </td>
        <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_path_query_array(target jsonb, path jsonpath [, vars jsonb [, silent bool]])</code>
      </td>
      <td style="text-align:left"><code>jsonb</code>
      </td>
      <td style="text-align:left">Gets all JSON items returned by JSON path for the specified JSON value
        and wraps result into an array.</td>
      <td style="text-align:left"><code>jsonb_path_query_array(&apos;{&quot;a&quot;:[1,2,3,4,5]}&apos;, &apos;$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)&apos;, &apos;{&quot;min&quot;:2,&quot;max&quot;:4}&apos;)</code>
      </td>
      <td style="text-align:left"><code>[2, 3, 4]</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>jsonb_path_query_first(target jsonb, path jsonpath [, vars jsonb [, silent bool]])</code>
      </td>
      <td style="text-align:left"><code>jsonb</code>
      </td>
      <td style="text-align:left">Gets the first JSON item returned by JSON path for the specified JSON
        value. Returns <code>NULL</code> on no results.</td>
      <td style="text-align:left"><code>jsonb_path_query_first(&apos;{&quot;a&quot;:[1,2,3,4,5]}&apos;, &apos;$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)&apos;, &apos;{&quot;min&quot;:2,&quot;max&quot;:4}&apos;)</code>
      </td>
      <td style="text-align:left"><code>2</code>
      </td>
    </tr>
  </tbody>
</table>

#### Note

Many of these functions and operators will convert Unicode escapes in JSON strings to the appropriate single character. This is a non-issue if the input is type `jsonb`, because the conversion was already done; but for `json` input, this may result in throwing an error, as noted in [Section 8.14](https://www.postgresql.org/docs/12/datatype-json.html).

#### Note

The functions `json[b]_populate_record`, `json[b]_populate_recordset`, `json[b]_to_record` and `json[b]_to_recordset` operate on a JSON object, or array of objects, and extract the values associated with keys whose names match column names of the output row type. Object fields that do not correspond to any output column name are ignored, and output columns that do not match any object field will be filled with nulls. To convert a JSON value to the SQL type of an output column, the following rules are applied in sequence:

* A JSON null value is converted to a SQL null in all cases.
* If the output column is of type `json` or `jsonb`, the JSON value is just reproduced exactly.
* If the output column is a composite \(row\) type, and the JSON value is a JSON object, the fields of the object are converted to columns of the output row type by recursive application of these rules.
* Likewise, if the output column is an array type and the JSON value is a JSON array, the elements of the JSON array are converted to elements of the output array by recursive application of these rules.
* Otherwise, if the JSON value is a string literal, the contents of the string are fed to the input conversion function for the column's data type.
* Otherwise, the ordinary text representation of the JSON value is fed to the input conversion function for the column's data type.

While the examples for these functions use constants, the typical use would be to reference a table in the `FROM` clause and use one of its `json` or `jsonb` columns as an argument to the function. Extracted key values can then be referenced in other parts of the query, like `WHERE` clauses and target lists. Extracting multiple values in this way can improve performance over extracting them separately with per-key operators.

#### Note

All the items of the `path` parameter of `jsonb_set` as well as `jsonb_insert` except the last item must be present in the `target`. If `create_missing` is false, all items of the `path` parameter of `jsonb_set` must be present. If these conditions are not met the `target` is returned unchanged.

If the last path item is an object key, it will be created if it is absent and given the new value. If the last path item is an array index, if it is positive the item to set is found by counting from the left, and if negative by counting from the right - `-1` designates the rightmost element, and so on. If the item is out of the range -array\_length .. array\_length -1, and create\_missing is true, the new value is added at the beginning of the array if the item is negative, and at the end of the array if it is positive.

#### Note

The `json_typeof` function's `null` return value should not be confused with a SQL NULL. While calling `json_typeof('null'::json)` will return `null`, calling `json_typeof(NULL::json)` will return a SQL NULL.

#### Note

If the argument to `json_strip_nulls` contains duplicate field names in any object, the result could be semantically somewhat different, depending on the order in which they occur. This is not an issue for `jsonb_strip_nulls` since `jsonb` values never have duplicate object field names.

#### Note

The `jsonb_path_exists`, `jsonb_path_match`, `jsonb_path_query`, `jsonb_path_query_array`, and `jsonb_path_query_first` functions have optional `vars` and `silent` arguments.

If the _`vars`_ argument is specified, it provides an object containing named variables to be substituted into a `jsonpath` expression.

If the _`silent`_ argument is specified and has the `true` value, these functions suppress the same errors as the `@?` and `@@` operators.

See also [Section 9.20](https://www.postgresql.org/docs/12/functions-aggregate.html) for the aggregate function `json_agg` which aggregates record values as JSON, and the aggregate function `json_object_agg` which aggregates pairs of values into a JSON object, and their `jsonb` equivalents, `jsonb_agg` and `jsonb_object_agg`.

## 9.15.2. The SQL/JSON Path Language

SQL/JSON path expressions specify the items to be retrieved from the JSON data, similar to XPath expressions used for SQL access to XML. In PostgreSQL, path expressions are implemented as the `jsonpath` data type and can use any elements described in [Section 8.14.6](https://www.postgresql.org/docs/12/datatype-json.html#DATATYPE-JSONPATH).

JSON query functions and operators pass the provided path expression to the _path engine_ for evaluation. If the expression matches the queried JSON data, the corresponding SQL/JSON item is returned. Path expressions are written in the SQL/JSON path language and can also include arithmetic expressions and functions. Query functions treat the provided expression as a text string, so it must be enclosed in single quotes.

A path expression consists of a sequence of elements allowed by the `jsonpath` data type. The path expression is evaluated from left to right, but you can use parentheses to change the order of operations. If the evaluation is successful, a sequence of SQL/JSON items \(_SQL/JSON sequence_\) is produced, and the evaluation result is returned to the JSON query function that completes the specified computation.

To refer to the JSON data to be queried \(the _context item_\), use the `$` sign in the path expression. It can be followed by one or more [accessor operators](https://www.postgresql.org/docs/12/datatype-json.html#TYPE-JSONPATH-ACCESSORS), which go down the JSON structure level by level to retrieve the content of context item. Each operator that follows deals with the result of the previous evaluation step.

For example, suppose you have some JSON data from a GPS tracker that you would like to parse, such as:

```text
{
  "track": {
    "segments": [
      {
        "location":   [ 47.763, 13.4034 ],
        "start time": "2018-10-14 10:05:14",
        "HR": 73
      },
      {
        "location":   [ 47.706, 13.2635 ],
        "start time": "2018-10-14 10:39:21",
        "HR": 135
      }
    ]
  }
}
```

To retrieve the available track segments, you need to use the `.`_`key`_ accessor operator for all the preceding JSON objects:

```text
'$.track.segments'
```

If the item to retrieve is an element of an array, you have to unnest this array using the `[*]` operator. For example, the following path will return location coordinates for all the available track segments:

```text
'$.track.segments[*].location'
```

To return the coordinates of the first segment only, you can specify the corresponding subscript in the `[]` accessor operator. Note that the SQL/JSON arrays are 0-relative:

```text
'$.track.segments[0].location'
```

The result of each path evaluation step can be processed by one or more `jsonpath` operators and methods listed in [Section 9.15.2.3](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-PATH-OPERATORS). Each method name must be preceded by a dot. For example, you can get an array size:

```text
'$.track.segments.size()'
```

For more examples of using `jsonpath` operators and methods within path expressions, see [Section 9.15.2.3](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-PATH-OPERATORS).

When defining the path, you can also use one or more _filter expressions_ that work similar to the `WHERE` clause in SQL. A filter expression begins with a question mark and provides a condition in parentheses:

```text
? (condition)
```

Filter expressions must be specified right after the path evaluation step to which they are applied. The result of this step is filtered to include only those items that satisfy the provided condition. SQL/JSON defines three-valued logic, so the condition can be `true`, `false`, or `unknown`. The `unknown` value plays the same role as SQL `NULL` and can be tested for with the `is unknown` predicate. Further path evaluation steps use only those items for which filter expressions return `true`.

Functions and operators that can be used in filter expressions are listed in [Table 9.49](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-FILTER-EX-TABLE). The path evaluation result to be filtered is denoted by the `@` variable. To refer to a JSON element stored at a lower nesting level, add one or more accessor operators after `@`.

Suppose you would like to retrieve all heart rate values higher than 130. You can achieve this using the following expression:

```text
'$.track.segments[*].HR ? (@ > 130)'
```

To get the start time of segments with such values instead, you have to filter out irrelevant segments before returning the start time, so the filter expression is applied to the previous step, and the path used in the condition is different:

```text
'$.track.segments[*] ? (@.HR > 130)."start time"'
```

You can use several filter expressions on the same nesting level, if required. For example, the following expression selects all segments that contain locations with relevant coordinates and high heart rate values:

```text
'$.track.segments[*] ? (@.location[1] < 13.4) ? (@.HR > 130)."start time"'
```

Using filter expressions at different nesting levels is also allowed. The following example first filters all segments by location, and then returns high heart rate values for these segments, if available:

```text
'$.track.segments[*] ? (@.location[1] < 13.4).HR ? (@ > 130)'
```

You can also nest filter expressions within each other:

```text
'$.track ? (exists(@.segments[*] ? (@.HR > 130))).segments.size()'
```

This expression returns the size of the track if it contains any segments with high heart rate values, or an empty sequence otherwise.

PostgreSQL's implementation of SQL/JSON path language has the following deviations from the SQL/JSON standard:

* `.datetime()` item method is not implemented yet mainly because immutable `jsonpath` functions and operators cannot reference session timezone, which is used in some datetime operations. Datetime support will be added to `jsonpath` in future versions of PostgreSQL.
* A path expression can be a Boolean predicate, although the SQL/JSON standard allows predicates only in filters. This is necessary for implementation of the `@@` operator. For example, the following `jsonpath` expression is valid in PostgreSQL:

  ```text
  '$.track.segments[*].HR < 70'
  ```

* There are minor differences in the interpretation of regular expression patterns used in `like_regex` filters, as described in [Section 9.15.2.2](https://www.postgresql.org/docs/12/functions-json.html#JSONPATH-REGULAR-EXPRESSIONS).

### **9.15.2.1. Strict And Lax Modes**

When you query JSON data, the path expression may not match the actual JSON data structure. An attempt to access a non-existent member of an object or element of an array results in a structural error. SQL/JSON path expressions have two modes of handling structural errors:

* lax \(default\) — the path engine implicitly adapts the queried data to the specified path. Any remaining structural errors are suppressed and converted to empty SQL/JSON sequences.
* strict — if a structural error occurs, an error is raised.

The lax mode facilitates matching of a JSON document structure and path expression if the JSON data does not conform to the expected schema. If an operand does not match the requirements of a particular operation, it can be automatically wrapped as an SQL/JSON array or unwrapped by converting its elements into an SQL/JSON sequence before performing this operation. Besides, comparison operators automatically unwrap their operands in the lax mode, so you can compare SQL/JSON arrays out-of-the-box. An array of size 1 is considered equal to its sole element. Automatic unwrapping is not performed only when:

* The path expression contains `type()` or `size()` methods that return the type and the number of elements in the array, respectively.
* The queried JSON data contain nested arrays. In this case, only the outermost array is unwrapped, while all the inner arrays remain unchanged. Thus, implicit unwrapping can only go one level down within each path evaluation step.

For example, when querying the GPS data listed above, you can abstract from the fact that it stores an array of segments when using the lax mode:

```text
'lax $.track.segments.location'
```

In the strict mode, the specified path must exactly match the structure of the queried JSON document to return an SQL/JSON item, so using this path expression will cause an error. To get the same result as in the lax mode, you have to explicitly unwrap the `segments` array:

```text
'strict $.track.segments[*].location'
```

### **9.15.2.2. Regular Expressions**

SQL/JSON path expressions allow matching text to a regular expression with the `like_regex` filter. For example, the following SQL/JSON path query would case-insensitively match all strings in an array that start with an English vowel:

```text
'$[*] ? (@ like_regex "^[aeiou]" flag "i")'
```

The optional `flag` string may include one or more of the characters `i` for case-insensitive match, `m` to allow `^` and `$` to match at newlines, `s` to allow `.` to match a newline, and `q` to quote the whole pattern \(reducing the behavior to a simple substring match\).

The SQL/JSON standard borrows its definition for regular expressions from the `LIKE_REGEX` operator, which in turn uses the XQuery standard. PostgreSQL does not currently support the `LIKE_REGEX` operator. Therefore, the `like_regex` filter is implemented using the POSIX regular expression engine described in [Section 9.7.3](https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP). This leads to various minor discrepancies from standard SQL/JSON behavior, which are cataloged in [Section 9.7.3.8](https://www.postgresql.org/docs/12/functions-matching.html#POSIX-VS-XQUERY). Note, however, that the flag-letter incompatibilities described there do not apply to SQL/JSON, as it translates the XQuery flag letters to match what the POSIX engine expects.

Keep in mind that the pattern argument of `like_regex` is a JSON path string literal, written according to the rules given in [Section 8.14.6](https://www.postgresql.org/docs/12/datatype-json.html#DATATYPE-JSONPATH). This means in particular that any backslashes you want to use in the regular expression must be doubled. For example, to match strings that contain only digits:

```text
'$ ? (@ like_regex "^\\d+$")'
```

### **9.15.2.3. SQL/JSON Path Operators And Methods**

[Table 9.48](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-OP-TABLE) shows the operators and methods available in `jsonpath`. [Table 9.49](https://www.postgresql.org/docs/12/functions-json.html#FUNCTIONS-SQLJSON-FILTER-EX-TABLE) shows the available filter expression elements.

#### **Table 9.48. `jsonpath` Operators and Methods**

| Operator/Method | Description | Example JSON | Example Query | Result |
| :--- | :--- | :--- | :--- | :--- |
| `+` \(unary\) | Plus operator that iterates over the SQL/JSON sequence | `{"x": [2.85, -14.7, -9.4]}` | `+ $.x.floor()` | `2, -15, -10` |
| `-` \(unary\) | Minus operator that iterates over the SQL/JSON sequence | `{"x": [2.85, -14.7, -9.4]}` | `- $.x.floor()` | `-2, 15, 10` |
| `+` \(binary\) | Addition | `[2]` | `2 + $[0]` | `4` |
| `-` \(binary\) | Subtraction | `[2]` | `4 - $[0]` | `2` |
| `*` | Multiplication | `[4]` | `2 * $[0]` | `8` |
| `/` | Division | `[8]` | `$[0] / 2` | `4` |
| `%` | Modulus | `[32]` | `$[0] % 10` | `2` |
| `type()` | Type of the SQL/JSON item | `[1, "2", {}]` | `$[*].type()` | `"number", "string", "object"` |
| `size()` | Size of the SQL/JSON item | `{"m": [11, 15]}` | `$.m.size()` | `2` |
| `double()` | Approximate floating-point number converted from an SQL/JSON number or a string | `{"len": "1.9"}` | `$.len.double() * 2` | `3.8` |
| `ceiling()` | Nearest integer greater than or equal to the SQL/JSON number | `{"h": 1.3}` | `$.h.ceiling()` | `2` |
| `floor()` | Nearest integer less than or equal to the SQL/JSON number | `{"h": 1.3}` | `$.h.floor()` | `1` |
| `abs()` | Absolute value of the SQL/JSON number | `{"z": -0.3}` | `$.z.abs()` | `0.3` |
| `keyvalue()` | Sequence of object's key-value pairs represented as array of items containing three fields \(`"key"`, `"value"`, and `"id"`\). `"id"` is a unique identifier of the object key-value pair belongs to. | `{"x": "20", "y": 32}` | `$.keyvalue()` | `{"key": "x", "value": "20", "id": 0}, {"key": "y", "value": 32, "id": 0}` |

#### **Table 9.49. `jsonpath` Filter Expression Elements**

| Value/Predicate | Description | Example JSON | Example Query | Result |
| :--- | :--- | :--- | :--- | :--- |
| `==` | Equality operator | `[1, 2, 1, 3]` | `$[*] ? (@ == 1)` | `1, 1` |
| `!=` | Non-equality operator | `[1, 2, 1, 3]` | `$[*] ? (@ != 1)` | `2, 3` |
| `<>` | Non-equality operator \(same as `!=`\) | `[1, 2, 1, 3]` | `$[*] ? (@ <> 1)` | `2, 3` |
| `<` | Less-than operator | `[1, 2, 3]` | `$[*] ? (@ < 2)` | `1` |
| `<=` | Less-than-or-equal-to operator | `[1, 2, 3]` | `$[*] ? (@ <= 2)` | `1, 2` |
| `>` | Greater-than operator | `[1, 2, 3]` | `$[*] ? (@ > 2)` | `3` |
| `>=` | Greater-than-or-equal-to operator | `[1, 2, 3]` | `$[*] ? (@ >= 2)` | `2, 3` |
| `true` | Value used to perform comparison with JSON `true` literal | `[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]` | `$[*] ? (@.parent == true)` | `{"name": "Chris", "parent": true}` |
| `false` | Value used to perform comparison with JSON `false` literal | `[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]` | `$[*] ? (@.parent == false)` | `{"name": "John", "parent": false}` |
| `null` | Value used to perform comparison with JSON `null` value | `[{"name": "Mary", "job": null}, {"name": "Michael", "job": "driver"}]` | `$[*] ? (@.job == null) .name` | `"Mary"` |
| `&&` | Boolean AND | `[1, 3, 7]` | `$[*] ? (@ > 1 && @ < 5)` | `3` |
| `||` | Boolean OR | `[1, 3, 7]` | `$[*] ? (@ < 1 || @ > 5)` | `7` |
| `!` | Boolean NOT | `[1, 3, 7]` | `$[*] ? (!(@ < 5))` | `7` |
| `like_regex` | Tests whether the first operand matches the regular expression given by the second operand, optionally with modifications described by a string of `flag` characters \(see [Section 9.15.2.2](https://www.postgresql.org/docs/12/functions-json.html#JSONPATH-REGULAR-EXPRESSIONS)\) | `["abc", "abd", "aBdC", "abdacb", "babc"]` | `$[*] ? (@ like_regex "^ab.*c" flag "i")` | `"abc", "aBdC", "abdacb"` |
| `starts with` | Tests whether the second operand is an initial substring of the first operand | `["John Smith", "Mary Stone", "Bob Johnson"]` | `$[*] ? (@ starts with "John")` | `"John Smith"` |
| `exists` | Tests whether a path expression matches at least one SQL/JSON item | `{"x": [1, 2], "y": [2, 4]}` | `strict $.* ? (exists (@ ? (@[*] > 2)))` | `2, 4` |
| `is unknown` | Tests whether a Boolean condition is `unknown` | `[-1, 2, 7, "infinity"]` | `$[*] ? ((@ > 0) is unknown)` | `"infinity"` |

