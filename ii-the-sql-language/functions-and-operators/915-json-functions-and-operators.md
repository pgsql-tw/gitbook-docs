# 9.15. JSON函式及運算子[^1]

[Table 9.43](https://www.postgresql.org/docs/10/static/functions-json.html#functions-json-op-table)shows the operators that are available for use with the two JSON data types \(see[Section 8.14](https://www.postgresql.org/docs/10/static/datatype-json.html)\).

**Table 9.43. **`json`**and**`jsonb`**Operators**

| Operator | Right Operand Type | Description | Example | Example Result |
| :--- | :--- | :--- | :--- | :--- |
| `->` | `int` | Get JSON array element \(indexed from zero, negative integers count from the end\) | `'[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json->2` | `{"c":"baz"}` |
| `->` | `text` | Get JSON object field by key | `'{"a": {"b":"foo"}}'::json->'a'` | `{"b":"foo"}` |
| `->>` | `int` | Get JSON array element as`text` | `'[1,2,3]'::json->>2` | `3` |
| `->>` | `text` | Get JSON object field as`text` | `'{"a":1,"b":2}'::json->>'b'` | `2` |
| `#>` | `text[]` | Get JSON object at specified path | `'{"a": {"b":{"c": "foo"}}}'::json#>'{a,b}'` | `{"c": "foo"}` |
| `#>>` | `text[]` | Get JSON object at specified path as`text` | `'{"a":[1,2,3],"b":[4,5,6]}'::json#>>'{a,2}'` | `3` |

### Note

There are parallel variants of these operators for both the`json`and`jsonb`types. The field/element/path extraction operators return the same type as their left-hand input \(either`json`or`jsonb`\), except for those specified as returning`text`, which coerce the value to text. The field/element/path extraction operators return NULL, rather than failing, if the JSON input does not have the right structure to match the request; for example if no such element exists. The field/element/path extraction operators that accept integer JSON array subscripts all support negative subscripting from the end of arrays.

The standard comparison operators shown in[Table 9.1](https://www.postgresql.org/docs/10/static/functions-comparison.html#functions-comparison-op-table)are available for`jsonb`, but not for`json`. They follow the ordering rules for B-tree operations outlined at[Section 8.14.4](https://www.postgresql.org/docs/10/static/datatype-json.html#json-indexing).

Some further operators also exist only for`jsonb`, as shown in[Table 9.44](https://www.postgresql.org/docs/10/static/functions-json.html#functions-jsonb-op-table). Many of these operators can be indexed by`jsonb`operator classes. For a full description of`jsonb`containment and existence semantics, see[Section 8.14.3](https://www.postgresql.org/docs/10/static/datatype-json.html#json-containment).[Section 8.14.4](https://www.postgresql.org/docs/10/static/datatype-json.html#json-indexing)describes how these operators can be used to effectively index`jsonb`data.

**Table 9.44. Additional**`jsonb`**Operators**

|  |  |  |  | Operator | Right Operand Type | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
|  |  |  |  | `@>` | `jsonb` | Does the left JSON value contain the right JSON path/value entries at the top level? | `'{"a":1, "b":2}'::jsonb @> '{"b":2}'::jsonb` |
|  |  |  |  | `<@` | `jsonb` | Are the left JSON path/value entries contained at the top level within the right JSON value? | `'{"b":2}'::jsonb <@ '{"a":1, "b":2}'::jsonb` |
|  |  |  |  | `?` | `text` | Does the\_string\_exist as a top-level key within the JSON value? | `'{"a":1, "b":2}'::jsonb ? 'b'` |
|  |  | \`? | \` | `text[]` | Do any of these array\_strings\_exist as top-level keys? | \`'{"a":1, "b":2, "c":3}'::jsonb ? | array\['b', 'c'\]\` |
|  |  |  |  | `?&` | `text[]` | Do all of these array\_strings\_exist as top-level keys? | `'["a", "b"]'::jsonb ?& array['a', 'b']` |
| \` |  | \` | `jsonb` | Concatenate two`jsonb`values into a new`jsonb`value | \`'\["a", "b"\]'::jsonb |  | '\["c", "d"\]'::jsonb\` |
|  |  |  |  | `-` | `text` | Delete key/value pair or\_string\_element from left operand. Key/value pairs are matched based on their key value. | `'{"a": "b"}'::jsonb - 'a'` |
|  |  |  |  | `-` | `text[]` | Delete multiple key/value pairs or\_string\_elements from left operand. Key/value pairs are matched based on their key value. | `'{"a": "b", "c": "d"}'::jsonb - '{a,c}'::text[]` |
|  |  |  |  | `-` | `integer` | Delete the array element with specified index \(Negative integers count from the end\). Throws an error if top level container is not an array. | `'["a", "b"]'::jsonb - 1` |
|  |  |  |  | `#-` | `text[]` | Delete the field or element with specified path \(for JSON arrays, negative integers count from the end\) | `'["a", {"b":1}]'::jsonb #- '{1,b}'` |

### Note

The`||`operator concatenates the elements at the top level of each of its operands. It does not operate recursively. For example, if both operands are objects with a common key field name, the value of the field in the result will just be the value from the right hand operand.

[Table 9.45](https://www.postgresql.org/docs/10/static/functions-json.html#functions-json-creation-table)shows the functions that are available for creating`json`and`jsonb`values. \(There are no equivalent functions for`jsonb`, of the`row_to_json`and`array_to_json`functions. However, the`to_jsonb`function supplies much the same functionality as these functions would.\)

**Table 9.45. JSON Creation Functions**

| Function | Description | Example | Example Result |
| :--- | :--- | :--- | :--- |
| `to_json(anyelement)to_jsonb(anyelement)` | Returns the value as`json`or`jsonb`. Arrays and composites are converted \(recursively\) to arrays and objects; otherwise, if there is a cast from the type to`json`, the cast function will be used to perform the conversion; otherwise, a scalar value is produced. For any scalar type other than a number, a Boolean, or a null value, the text representation will be used, in such a fashion that it is a valid`json`or`jsonb`value. | `to_json('Fred said "Hi."'::text)` | `"Fred said \"Hi.\""` |
| `array_to_json(anyarray [, pretty_bool])` | Returns the array as a JSON array. A PostgreSQL multidimensional array becomes a JSON array of arrays. Line feeds will be added between dimension-1 elements if\_`pretty_bool`\_is true. | `array_to_json('{ {1,5},{99,100} }'::int[])` | `[[1,5],[99,100]]` |
| `row_to_json(record [, pretty_bool])` | Returns the row as a JSON object. Line feeds will be added between level-1 elements if\_`pretty_bool`\_is true. | `row_to_json(row(1,'foo'))` | `{"f1":1,"f2":"foo"}` |
| `json_build_array(VARIADIC "any")jsonb_build_array(VARIADIC "any")` | Builds a possibly-heterogeneously-typed JSON array out of a variadic argument list. | `json_build_array(1,2,'3',4,5)` | `[1, 2, "3", 4, 5]` |
| `json_build_object(VARIADIC "any")jsonb_build_object(VARIADIC "any")` | Builds a JSON object out of a variadic argument list. By convention, the argument list consists of alternating keys and values. | `json_build_object('foo',1,'bar',2)` | `{"foo": 1, "bar": 2}` |
| `json_object(text[])jsonb_object(text[])` | Builds a JSON object out of a text array. The array must have either exactly one dimension with an even number of members, in which case they are taken as alternating key/value pairs, or two dimensions such that each inner array has exactly two elements, which are taken as a key/value pair. | `json_object('{a, 1, b, "def", c, 3.5}')json_object('{ {a, 1},{b, "def"},{c, 3.5} }')` | `{"a": "1", "b": "def", "c": "3.5"}` |
| `json_object(keys text[], values text[])jsonb_object(keys text[], values text[])` | This form of`json_object`takes keys and values pairwise from two separate arrays. In all other respects it is identical to the one-argument form. | `json_object('{a, b}', '{1,2}')` | `{"a": "1", "b": "2"}` |

### Note

`array_to_json`and`row_to_json`have the same behavior as`to_json`except for offering a pretty-printing option. The behavior described for`to_json`likewise applies to each individual value converted by the other JSON creation functions.

### Note

The[hstore](https://www.postgresql.org/docs/10/static/hstore.html)extension has a cast from`hstore`to`json`, so that`hstore`values converted via the JSON creation functions will be represented as JSON objects, not as primitive string values.

[Table 9.46](https://www.postgresql.org/docs/10/static/functions-json.html#functions-json-processing-table)shows the functions that are available for processing`json`and`jsonb`values.

**Table 9.46. JSON Processing Functions**

### Note

Many of these functions and operators will convert Unicode escapes in JSON strings to the appropriate single character. This is a non-issue if the input is type`jsonb`, because the conversion was already done; but for`json`input, this may result in throwing an error, as noted in[Section 8.14](https://www.postgresql.org/docs/10/static/datatype-json.html).

### Note

In`json_populate_record`,`json_populate_recordset`,`json_to_record`and`json_to_recordset`, type coercion from the JSON is“best effort”and may not result in desired values for some types. JSON keys are matched to identical column names in the target row type. JSON fields that do not appear in the target row type will be omitted from the output, and target columns that do not match any JSON field will simply be NULL.

### Note

All the items of the`path`parameter of`jsonb_set`as well as`jsonb_insert`except the last item must be present in the`target`. If`create_missing`is false, all items of the`path`parameter of`jsonb_set`must be present. If these conditions are not met the`target`is returned unchanged.

If the last path item is an object key, it will be created if it is absent and given the new value. If the last path item is an array index, if it is positive the item to set is found by counting from the left, and if negative by counting from the right -`-1`designates the rightmost element, and so on. If the item is out of the range -array\_length .. array\_length -1, and create\_missing is true, the new value is added at the beginning of the array if the item is negative, and at the end of the array if it is positive.

### Note

The`json_typeof`function's`null`return value should not be confused with a SQL NULL. While calling`json_typeof('null'::json)`will return`null`, calling`json_typeof(NULL::json)`will return a SQL NULL.

### Note

If the argument to`json_strip_nulls`contains duplicate field names in any object, the result could be semantically somewhat different, depending on the order in which they occur. This is not an issue for`jsonb_strip_nulls`since`jsonb`values never have duplicate object field names.

See also[Section 9.20](https://www.postgresql.org/docs/10/static/functions-aggregate.html)for the aggregate function`json_agg`which aggregates record values as JSON, and the aggregate function`json_object_agg`which aggregates pairs of values into a JSON object, and their`jsonb`equivalents,`jsonb_agg`and`jsonb_object_agg`.

---

[^1]:  [PostgreSQL: Documentation: 10: 9.15. JSON Functions and Operators](https://www.postgresql.org/docs/10/static/functions-json.html)

