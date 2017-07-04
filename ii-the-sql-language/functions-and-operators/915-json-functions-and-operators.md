# 9.15. JSON函式及運算子[^1]

[Table 9.43](https://www.postgresql.org/docs/10/static/functions-json.html#functions-json-op-table)shows the operators that are available for use with the two JSON data types \(see[Section 8.14](https://www.postgresql.org/docs/10/static/datatype-json.html)\).

**Table 9.43. **`json`**and**`jsonb`**Operators**

### Note

There are parallel variants of these operators for both the`json`and`jsonb`types. The field/element/path extraction operators return the same type as their left-hand input \(either`json`or`jsonb`\), except for those specified as returning`text`, which coerce the value to text. The field/element/path extraction operators return NULL, rather than failing, if the JSON input does not have the right structure to match the request; for example if no such element exists. The field/element/path extraction operators that accept integer JSON array subscripts all support negative subscripting from the end of arrays.

The standard comparison operators shown in[Table 9.1](https://www.postgresql.org/docs/10/static/functions-comparison.html#functions-comparison-op-table)are available for`jsonb`, but not for`json`. They follow the ordering rules for B-tree operations outlined at[Section 8.14.4](https://www.postgresql.org/docs/10/static/datatype-json.html#json-indexing).

Some further operators also exist only for`jsonb`, as shown in[Table 9.44](https://www.postgresql.org/docs/10/static/functions-json.html#functions-jsonb-op-table). Many of these operators can be indexed by`jsonb`operator classes. For a full description of`jsonb`containment and existence semantics, see[Section 8.14.3](https://www.postgresql.org/docs/10/static/datatype-json.html#json-containment).[Section 8.14.4](https://www.postgresql.org/docs/10/static/datatype-json.html#json-indexing)describes how these operators can be used to effectively index`jsonb`data.

**Table 9.44. Additional**`jsonb`**Operators**

### Note

The`||`operator concatenates the elements at the top level of each of its operands. It does not operate recursively. For example, if both operands are objects with a common key field name, the value of the field in the result will just be the value from the right hand operand.

[Table 9.45](https://www.postgresql.org/docs/10/static/functions-json.html#functions-json-creation-table)shows the functions that are available for creating`json`and`jsonb`values. \(There are no equivalent functions for`jsonb`, of the`row_to_json`and`array_to_json`functions. However, the`to_jsonb`function supplies much the same functionality as these functions would.\)

**Table 9.45. JSON Creation Functions**

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

