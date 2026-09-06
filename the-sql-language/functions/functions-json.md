## 9.16. JSON Functions and Operators [#](#FUNCTIONS-JSON)

[9.16.1. Processing and Creating JSON Data](functions-json.md#FUNCTIONS-JSON-PROCESSING)

[9.16.2. The SQL/JSON Path Language](functions-json.md#FUNCTIONS-SQLJSON-PATH)

[9.16.3. SQL/JSON Query Functions](functions-json.md#SQLJSON-QUERY-FUNCTIONS)

[9.16.4. JSON_TABLE](functions-json.md#FUNCTIONS-SQLJSON-TABLE)

<a id="id-1.5.8.22.2"></a><a id="id-1.5.8.22.3"></a>

This section describes:

* functions and operators for processing and creating JSON data
* the SQL/JSON path language
* the SQL/JSON query functions

To provide native support for JSON data types within the SQL environment,
PostgreSQL implements the
*SQL/JSON data model*.
This model comprises sequences of items. Each item can hold SQL scalar
values, with an additional SQL/JSON null value, and composite data structures
that use JSON arrays and objects. The model is a formalization of the implied
data model in the JSON specification
[RFC 7159](https://datatracker.ietf.org/doc/html/rfc7159).

SQL/JSON allows you to handle JSON data alongside regular SQL data,
with transaction support, including:

* Uploading JSON data into the database and storing it in
  regular SQL columns as character or binary strings.
* Generating JSON objects and arrays from relational data.
* Querying JSON data using SQL/JSON query functions and
  SQL/JSON path language expressions.

To learn more about the SQL/JSON standard, see
[[sqltr-19075-6]](../../bibliography.md#SQLTR-19075-6). For details on JSON types
supported in PostgreSQL,
see [Section 8.14](../datatype/datatype-json.md).

<a id="FUNCTIONS-JSON-PROCESSING"></a>

### 9.16.1. Processing and Creating JSON Data [#](#FUNCTIONS-JSON-PROCESSING)

[Table 9.47](functions-json.md#FUNCTIONS-JSON-OP-TABLE) shows the operators that
are available for use with JSON data types (see [Section 8.14](../datatype/datatype-json.md)).
In addition, the usual comparison operators shown in [Table 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) are available for
`jsonb`, though not for `json`. The comparison
operators follow the ordering rules for B-tree operations outlined in
[Section 8.14.4](../datatype/datatype-json.md#JSON-INDEXING).
See also [Section 9.21](functions-aggregate.md) for the aggregate
function `json_agg` which aggregates record
values as JSON, the aggregate function
`json_object_agg` which aggregates pairs of values
into a JSON object, and their `jsonb` equivalents,
`jsonb_agg` and `jsonb_object_agg`.

<a id="FUNCTIONS-JSON-OP-TABLE"></a>

**Table 9.47. `json` and `jsonb` Operators**

<table border="1" class="table" summary="json and jsonb Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Extracts <em class="parameter"><code>n</code></em>'th element of JSON array
        (array elements are indexed from zero, but negative integers count
        from the end).
       </p>
<p>
<code class="literal">'[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -&gt; 2</code>
        → <code class="returnvalue">{"c":"baz"}</code>
</p>
<p>
<code class="literal">'[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -&gt; -3</code>
        → <code class="returnvalue">{"a":"foo"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Extracts JSON object field with the given key.
       </p>
<p>
<code class="literal">'{"a": {"b":"foo"}}'::json -&gt; 'a'</code>
        → <code class="returnvalue">{"b":"foo"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        Extracts <em class="parameter"><code>n</code></em>'th element of JSON array,
        as <code class="type">text</code>.
       </p>
<p>
<code class="literal">'[1,2,3]'::json -&gt;&gt; 2</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">-&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        Extracts JSON object field with the given key, as <code class="type">text</code>.
       </p>
<p>
<code class="literal">'{"a":1,"b":2}'::json -&gt;&gt; 'b'</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">#&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">#&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Extracts JSON sub-object at the specified path, where path elements
        can be either field keys or array indexes.
       </p>
<p>
<code class="literal">'{"a": {"b": ["foo","bar"]}}'::json #&gt; '{a,b,1}'</code>
        → <code class="returnvalue">"bar"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">json</code> <code class="literal">#&gt;&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="type">jsonb</code> <code class="literal">#&gt;&gt;</code> <code class="type">text[]</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        Extracts JSON sub-object at the specified path as <code class="type">text</code>.
       </p>
<p>
<code class="literal">'{"a": {"b": ["foo","bar"]}}'::json #&gt;&gt; '{a,b,1}'</code>
        → <code class="returnvalue">bar</code>
</p></td></tr></tbody></table>

<br>

### Note

The field/element/path extraction operators return NULL, rather than
failing, if the JSON input does not have the right structure to match
the request; for example if no such key or array element exists.

Some further operators exist only for `jsonb`, as shown
in [Table 9.48](functions-json.md#FUNCTIONS-JSONB-OP-TABLE).
[Section 8.14.4](../datatype/datatype-json.md#JSON-INDEXING)
describes how these operators can be used to effectively search indexed
`jsonb` data.

<a id="FUNCTIONS-JSONB-OP-TABLE"></a>

**Table 9.48. Additional `jsonb` Operators**

<table border="1" class="table" summary="Additional jsonb Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">@&gt;</code> <code class="type">jsonb</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the first JSON value contain the second?
        (See <a class="xref" href="../datatype/datatype-json.md#JSON-CONTAINMENT">Section 8.14.3</a> for details about containment.)
       </p>
<p>
<code class="literal">'{"a":1, "b":2}'::jsonb @&gt; '{"b":2}'::jsonb</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">&lt;@</code> <code class="type">jsonb</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the first JSON value contained in the second?
       </p>
<p>
<code class="literal">'{"b":2}'::jsonb &lt;@ '{"a":1, "b":2}'::jsonb</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">?</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does the text string exist as a top-level key or array element within
        the JSON value?
       </p>
<p>
<code class="literal">'{"a":1, "b":2}'::jsonb ? 'b'</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">'["a", "b", "c"]'::jsonb ? 'b'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">?|</code> <code class="type">text[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Do any of the strings in the text array exist as top-level keys or
        array elements?
       </p>
<p>
<code class="literal">'{"a":1, "b":2, "c":3}'::jsonb ?| array['b', 'd']</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">?&amp;</code> <code class="type">text[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Do all of the strings in the text array exist as top-level keys or
        array elements?
       </p>
<p>
<code class="literal">'["a", "b", "c"]'::jsonb ?&amp; array['a', 'b']</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">||</code> <code class="type">jsonb</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Concatenates two <code class="type">jsonb</code> values.
        Concatenating two arrays generates an array containing all the
        elements of each input.  Concatenating two objects generates an
        object containing the union of their
        keys, taking the second object's value when there are duplicate keys.
        All other cases are treated by converting a non-array input into a
        single-element array, and then proceeding as for two arrays.
        Does not operate recursively: only the top-level array or object
        structure is merged.
       </p>
<p>
<code class="literal">'["a", "b"]'::jsonb || '["a", "d"]'::jsonb</code>
        → <code class="returnvalue">["a", "b", "a", "d"]</code>
</p>
<p>
<code class="literal">'{"a": "b"}'::jsonb || '{"c": "d"}'::jsonb</code>
        → <code class="returnvalue">{"a": "b", "c": "d"}</code>
</p>
<p>
<code class="literal">'[1, 2]'::jsonb || '3'::jsonb</code>
        → <code class="returnvalue">[1, 2, 3]</code>
</p>
<p>
<code class="literal">'{"a": "b"}'::jsonb || '42'::jsonb</code>
        → <code class="returnvalue">[{"a": "b"}, 42]</code>
</p>
<p>
        To append an array to another array as a single entry, wrap it
        in an additional layer of array, for example:
       </p>
<p>
<code class="literal">'[1, 2]'::jsonb || jsonb_build_array('[3, 4]'::jsonb)</code>
        → <code class="returnvalue">[1, 2, [3, 4]]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-</code> <code class="type">text</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Deletes a key (and its value) from a JSON object, or matching string
        value(s) from a JSON array.
       </p>
<p>
<code class="literal">'{"a": "b", "c": "d"}'::jsonb - 'a'</code>
        → <code class="returnvalue">{"c": "d"}</code>
</p>
<p>
<code class="literal">'["a", "b", "c", "b"]'::jsonb - 'b'</code>
        → <code class="returnvalue">["a", "c"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-</code> <code class="type">text[]</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Deletes all matching keys or array elements from the left operand.
       </p>
<p>
<code class="literal">'{"a": "b", "c": "d"}'::jsonb - '{a,c}'::text[]</code>
        → <code class="returnvalue">{}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">-</code> <code class="type">integer</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Deletes the array element with specified index (negative
        integers count from the end).  Throws an error if JSON value
        is not an array.
       </p>
<p>
<code class="literal">'["a", "b"]'::jsonb - 1 </code>
        → <code class="returnvalue">["a"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">#-</code> <code class="type">text[]</code>
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Deletes the field or array element at the specified path, where path
        elements can be either field keys or array indexes.
       </p>
<p>
<code class="literal">'["a", {"b":1}]'::jsonb #- '{1,b}'</code>
        → <code class="returnvalue">["a", {}]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">@?</code> <code class="type">jsonpath</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does JSON path return any item for the specified JSON value?
        (This is useful only with SQL-standard JSON path expressions, not
        <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">predicate check
        expressions</a>, since those always return a value.)
       </p>
<p>
<code class="literal">'{"a":[1,2,3,4,5]}'::jsonb @? '$.a[*] ? (@ &gt; 2)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">jsonb</code> <code class="literal">@@</code> <code class="type">jsonpath</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns the result of a JSON path predicate check for the
        specified JSON value.
        (This is useful only
        with <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">predicate
        check expressions</a>, not SQL-standard JSON path expressions,
        since it will return <code class="literal">NULL</code> if the path result is
        not a single boolean value.)
       </p>
<p>
<code class="literal">'{"a":[1,2,3,4,5]}'::jsonb @@ '$.a[*] &gt; 2'</code>
        → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

### Note

The `jsonpath` operators `@?`
and `@@` suppress the following errors: missing object
field or array element, unexpected JSON item type, datetime and numeric
errors. The `jsonpath`-related functions described below can
also be told to suppress these types of errors. This behavior might be
helpful when searching JSON document collections of varying structure.

[Table 9.49](functions-json.md#FUNCTIONS-JSON-CREATION-TABLE) shows the functions that are
available for constructing `json` and `jsonb` values.
Some functions in this table have a `RETURNING` clause,
which specifies the data type returned. It must be one of `json`,
`jsonb`, `bytea`, a character string type (`text`,
`char`, or `varchar`), or a type
that can be cast to `json`.
By default, the `json` type is returned.

<a id="FUNCTIONS-JSON-CREATION-TABLE"></a>

**Table 9.49. JSON Creation Functions**

<table border="1" class="table" summary="JSON Creation Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.1.1.1.1"></a>
<code class="function">to_json</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.1.1.2.1"></a>
<code class="function">to_jsonb</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Converts any SQL value to <code class="type">json</code> or <code class="type">jsonb</code>.
        Arrays and composites are converted recursively to arrays and
        objects (multidimensional arrays become arrays of arrays in JSON).
        Otherwise, if there is a cast from the SQL data type
        to <code class="type">json</code>, the cast function will be used to perform the
        conversion;<a class="footnote" href="#ftn.id-1.5.8.22.8.9.2.2.1.1.3.4"><sup class="footnote" id="id-1.5.8.22.8.9.2.2.1.1.3.4">[a]</sup></a>
        otherwise, a scalar JSON value is produced.  For any scalar other than
        a number, a Boolean, or a null value, the text representation will be
        used, with escaping as necessary to make it a valid JSON string value.
       </p>
<p>
<code class="literal">to_json('Fred said "Hi."'::text)</code>
        → <code class="returnvalue">"Fred said \"Hi.\""</code>
</p>
<p>
<code class="literal">to_jsonb(row(42, 'Fred said "Hi."'::text))</code>
        → <code class="returnvalue">{"f1": 42, "f2": "Fred said \"Hi.\""}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.2.1.1.1"></a>
<code class="function">array_to_json</code> ( <code class="type">anyarray</code> [<span class="optional">, <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">json</code>
</p>
<p>
        Converts an SQL array to a JSON array.  The behavior is the same
        as <code class="function">to_json</code> except that line feeds will be added
        between top-level array elements if the optional boolean parameter is
        true.
       </p>
<p>
<code class="literal">array_to_json('{{1,5},{99,100}}'::int[])</code>
        → <code class="returnvalue">[[1,5],[99,100]]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.3.1.1.1"></a>
<code class="function">json_array</code> (
         [<span class="optional"> { <em class="replaceable"><code>value_expression</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> </span>] } [<span class="optional">, ...</span>] </span>]
         [<span class="optional"> { <code class="literal">NULL</code> | <code class="literal">ABSENT</code> } <code class="literal">ON NULL</code> </span>]
         [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
        </p>
<p class="func_signature">
<code class="function">json_array</code> (
         [<span class="optional"> <em class="replaceable"><code>query_expression</code></em> </span>]
         [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
        </p>
<p>
         Constructs a JSON array from either a series of
         <em class="replaceable"><code>value_expression</code></em> parameters or from the results
         of <em class="replaceable"><code>query_expression</code></em>,
         which must be a SELECT query returning a single column. If
         <code class="literal">ABSENT ON NULL</code> is specified, NULL values are ignored.
         This is always the case if a
         <em class="replaceable"><code>query_expression</code></em> is used.
        </p>
<p>
<code class="literal">json_array(1,true,json '{"a":null}')</code>
         → <code class="returnvalue">[1, true, {"a":null}]</code>
</p>
<p>
<code class="literal">json_array(SELECT * FROM (VALUES(1),(2)) t)</code>
         → <code class="returnvalue">[1, 2]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.4.1.1.1"></a>
<code class="function">row_to_json</code> ( <code class="type">record</code> [<span class="optional">, <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">json</code>
</p>
<p>
        Converts an SQL composite value to a JSON object.  The behavior is the
        same as <code class="function">to_json</code> except that line feeds will be
        added between top-level elements if the optional boolean parameter is
        true.
       </p>
<p>
<code class="literal">row_to_json(row(1,'foo'))</code>
        → <code class="returnvalue">{"f1":1,"f2":"foo"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.5.1.1.1"></a>
<code class="function">json_build_array</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.5.1.2.1"></a>
<code class="function">jsonb_build_array</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Builds a possibly-heterogeneously-typed JSON array out of a variadic
        argument list.  Each argument is converted as
        per <code class="function">to_json</code> or <code class="function">to_jsonb</code>.
       </p>
<p>
<code class="literal">json_build_array(1, 2, 'foo', 4, 5)</code>
        → <code class="returnvalue">[1, 2, "foo", 4, 5]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.6.1.1.1"></a>
<code class="function">json_build_object</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.6.1.2.1"></a>
<code class="function">jsonb_build_object</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Builds a JSON object out of a variadic argument list.  By convention,
        the argument list consists of alternating keys and values.  Key
        arguments are coerced to text; value arguments are converted as
        per <code class="function">to_json</code> or <code class="function">to_jsonb</code>.
       </p>
<p>
<code class="literal">json_build_object('foo', 1, 2, row(3,'bar'))</code>
        → <code class="returnvalue">{"foo" : 1, "2" : {"f1":3,"f2":"bar"}}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.7.1.1.1"></a>
<code class="function">json_object</code> (
         [<span class="optional"> { <em class="replaceable"><code>key_expression</code></em> { <code class="literal">VALUE</code> | ':' }
          <em class="replaceable"><code>value_expression</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] }[<span class="optional">, ...</span>] </span>]
         [<span class="optional"> { <code class="literal">NULL</code> | <code class="literal">ABSENT</code> } <code class="literal">ON NULL</code> </span>]
         [<span class="optional"> { <code class="literal">WITH</code> | <code class="literal">WITHOUT</code> } <code class="literal">UNIQUE</code> [<span class="optional"> <code class="literal">KEYS</code> </span>] </span>]
         [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>])
        </p>
<p>
         Constructs a JSON object of all the key/value pairs given,
         or an empty object if none are given.
         <em class="replaceable"><code>key_expression</code></em> is a scalar expression
         defining the <acronym class="acronym">JSON</acronym> key, which is
         converted to the <code class="type">text</code> type.
         It cannot be <code class="literal">NULL</code> nor can it
         belong to a type that has a cast to the <code class="type">json</code> type.
         If <code class="literal">WITH UNIQUE KEYS</code> is specified, there must not
         be any duplicate <em class="replaceable"><code>key_expression</code></em>.
         Any pair for which the <em class="replaceable"><code>value_expression</code></em>
         evaluates to <code class="literal">NULL</code> is omitted from the output
         if <code class="literal">ABSENT ON NULL</code> is specified;
         if <code class="literal">NULL ON NULL</code> is specified or the clause
         omitted, the key is included with value <code class="literal">NULL</code>.
        </p>
<p>
<code class="literal">json_object('code' VALUE 'P123', 'title': 'Jaws')</code>
         → <code class="returnvalue">{"code" : "P123", "title" : "Jaws"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.8.1.1.1"></a>
<code class="function">json_object</code> ( <code class="type">text[]</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.8.1.2.1"></a>
<code class="function">jsonb_object</code> ( <code class="type">text[]</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Builds a JSON object out of a text array.  The array must have either
        exactly one dimension with an even number of members, in which case
        they are taken as alternating key/value pairs, or two dimensions
        such that each inner array has exactly two elements, which
        are taken as a key/value pair.  All values are converted to JSON
        strings.
       </p>
<p>
<code class="literal">json_object('{a, 1, b, "def", c, 3.5}')</code>
        → <code class="returnvalue">{"a" : "1", "b" : "def", "c" : "3.5"}</code>
</p>
<p><code class="literal">json_object('{{a, 1}, {b, "def"}, {c, 3.5}}')</code>
        → <code class="returnvalue">{"a" : "1", "b" : "def", "c" : "3.5"}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">json_object</code> ( <em class="parameter"><code>keys</code></em> <code class="type">text[]</code>, <em class="parameter"><code>values</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<code class="function">jsonb_object</code> ( <em class="parameter"><code>keys</code></em> <code class="type">text[]</code>, <em class="parameter"><code>values</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        This form of <code class="function">json_object</code> takes keys and values
        pairwise from separate text arrays.  Otherwise it is identical to
        the one-argument form.
       </p>
<p>
<code class="literal">json_object('{a,b}', '{1,2}')</code>
        → <code class="returnvalue">{"a": "1", "b": "2"}</code>
</p></td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.10.1.1.1"></a>
<code class="function">json</code> (
         <em class="replaceable"><code>expression</code></em>
         [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>]</span>]
         [<span class="optional"> { <code class="literal">WITH</code> | <code class="literal">WITHOUT</code> } <code class="literal">UNIQUE</code> [<span class="optional"> <code class="literal">KEYS</code> </span>]</span>] )
         → <code class="returnvalue">json</code>
</p>
<p>
         Converts a given expression specified as <code class="type">text</code> or
         <code class="type">bytea</code> string (in UTF8 encoding) into a JSON
         value.  If <em class="replaceable"><code>expression</code></em> is NULL, an
         <acronym class="acronym">SQL</acronym> null value is returned.
         If <code class="literal">WITH UNIQUE</code> is specified, the
         <em class="replaceable"><code>expression</code></em> must not contain any duplicate
         object keys.
        </p>
<p>
<code class="literal">json('{"a":123, "b":[true,"foo"], "a":"bar"}')</code>
         → <code class="returnvalue">{"a":123, "b":[true,"foo"], "a":"bar"}</code>
</p>
</td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.9.2.2.11.1.1.1"></a>
<code class="function">json_scalar</code> ( <em class="replaceable"><code>expression</code></em> )
       </p>
<p>
        Converts a given SQL scalar value into a JSON scalar value.
        If the input is NULL, an <acronym class="acronym">SQL</acronym> null is returned. If
        the input is number or a boolean value, a corresponding JSON number
        or boolean value is returned. For any other value, a JSON string is
        returned.
       </p>
<p>
<code class="literal">json_scalar(123.45)</code>
        → <code class="returnvalue">123.45</code>
</p>
<p>
<code class="literal">json_scalar(CURRENT_TIMESTAMP)</code>
        → <code class="returnvalue">"2022-05-10T10:51:04.62128-04:00"</code>
</p></td></tr><tr><td class="func_table_entry">
<p class="func_signature">
<code class="function">json_serialize</code> (
        <em class="replaceable"><code>expression</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>]
        [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>] )
       </p>
<p>
        Converts an SQL/JSON expression into a character or binary string. The
        <em class="replaceable"><code>expression</code></em> can be of any JSON type, any
        character string type, or <code class="type">bytea</code> in UTF8 encoding.
        The returned type used in <code class="literal"> RETURNING</code> can be any
        character string type or <code class="type">bytea</code>. The default is
        <code class="type">text</code>.
       </p>
<p>
<code class="literal">json_serialize('{ "a" : 1 } ' RETURNING bytea)</code>
        → <code class="returnvalue">\x7b20226122203a2031207d20</code>
</p></td></tr></tbody><tbody class="footnotes"><tr><td colspan="1"><div class="footnote" id="ftn.id-1.5.8.22.8.9.2.2.1.1.3.4"><p><a class="para" href="#id-1.5.8.22.8.9.2.2.1.1.3.4"><sup class="para">[a] </sup></a>
          For example, the <a class="xref" href="../../appendixes/contrib/hstore.md">hstore</a> extension has a cast
          from <code class="type">hstore</code> to <code class="type">json</code>, so that
          <code class="type">hstore</code> values converted via the JSON creation functions
          will be represented as JSON objects, not as primitive string values.
         </p></div></td></tr></tbody></table>

<br>

[Table 9.50](functions-json.md#FUNCTIONS-SQLJSON-MISC) details SQL/JSON
facilities for testing JSON.

<a id="FUNCTIONS-SQLJSON-MISC"></a>

**Table 9.50. SQL/JSON Testing Functions**

<table border="1" class="table" summary="SQL/JSON Testing Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function signature
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
      </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.11.2.2.1.1.1.1"></a>
<em class="replaceable"><code>expression</code></em> <code class="literal">IS</code> [<span class="optional"> <code class="literal">NOT</code> </span>] <code class="literal">JSON</code>
        [<span class="optional"> { <code class="literal">VALUE</code> | <code class="literal">SCALAR</code> | <code class="literal">ARRAY</code> | <code class="literal">OBJECT</code> } </span>]
        [<span class="optional"> { <code class="literal">WITH</code> | <code class="literal">WITHOUT</code> } <code class="literal">UNIQUE</code> [<span class="optional"> <code class="literal">KEYS</code> </span>] </span>]
       </p>
<p>
        This predicate tests whether <em class="replaceable"><code>expression</code></em> can be
        parsed as JSON, possibly of a specified type.
        If <code class="literal">SCALAR</code> or <code class="literal">ARRAY</code> or
        <code class="literal">OBJECT</code> is specified, the
        test is whether or not the JSON is of that particular type. If
        <code class="literal">WITH UNIQUE KEYS</code> is specified, then any object in the
        <em class="replaceable"><code>expression</code></em> is also tested to see if it
        has duplicate keys.
       </p>
<p>
</p><pre class="programlisting">
SELECT js,
  js IS JSON "json?",
  js IS JSON SCALAR "scalar?",
  js IS JSON OBJECT "object?",
  js IS JSON ARRAY "array?"
FROM (VALUES
      ('123'), ('"abc"'), ('{"a": "b"}'), ('[1,2]'),('abc')) foo(js);
     js     | json? | scalar? | object? | array?
------------+-------+---------+---------+--------
 123        | t     | t       | f       | f
 "abc"      | t     | t       | f       | f
 {"a": "b"} | t     | f       | t       | f
 [1,2]      | t     | f       | f       | t
 abc        | f     | f       | f       | f
</pre><p>
</p>
<p>
</p><pre class="programlisting">
SELECT js,
  js IS JSON OBJECT "object?",
  js IS JSON ARRAY "array?",
  js IS JSON ARRAY WITH UNIQUE KEYS "array w. UK?",
  js IS JSON ARRAY WITHOUT UNIQUE KEYS "array w/o UK?"
FROM (VALUES ('[{"a":"1"},
 {"b":"2","b":"3"}]')) foo(js);
-[ RECORD 1 ]-+--------------------
js            | [{"a":"1"},        +
              |  {"b":"2","b":"3"}]
object?       | f
array?        | t
array w. UK?  | f
array w/o UK? | t
</pre><p>
</p></td></tr></tbody></table>

<br>

[Table 9.51](functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE) shows the functions that
are available for processing `json` and `jsonb` values.

<a id="FUNCTIONS-JSON-PROCESSING-TABLE"></a>

**Table 9.51. JSON Processing Functions**

<table border="1" class="table" summary="JSON Processing Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.1.1.1.1"></a>
<code class="function">json_array_elements</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.1.1.2.1"></a>
<code class="function">jsonb_array_elements</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof jsonb</code>
</p>
<p>
        Expands the top-level JSON array into a set of JSON values.
       </p>
<p>
<code class="literal">select * from json_array_elements('[1,true, [2,false]]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
   value
-----------
 1
 true
 [2,false]
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.2.1.1.1"></a>
<code class="function">json_array_elements_text</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.2.1.2.1"></a>
<code class="function">jsonb_array_elements_text</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        Expands the top-level JSON array into a set of <code class="type">text</code> values.
       </p>
<p>
<code class="literal">select * from json_array_elements_text('["foo", "bar"]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
   value
-----------
 foo
 bar
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.3.1.1.1"></a>
<code class="function">json_array_length</code> ( <code class="type">json</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.3.1.2.1"></a>
<code class="function">jsonb_array_length</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the number of elements in the top-level JSON array.
       </p>
<p>
<code class="literal">json_array_length('[1,2,3,{"f1":1,"f2":[5,6]},4]')</code>
        → <code class="returnvalue">5</code>
</p>
<p>
<code class="literal">jsonb_array_length('[]')</code>
        → <code class="returnvalue">0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.4.1.1.1"></a>
<code class="function">json_each</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">json</code> )
       </p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.4.1.2.1"></a>
<code class="function">jsonb_each</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">jsonb</code> )
       </p>
<p>
        Expands the top-level JSON object into a set of key/value pairs.
       </p>
<p>
<code class="literal">select * from json_each('{"a":"foo", "b":"bar"}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 key | value
-----+-------
 a   | "foo"
 b   | "bar"
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.5.1.1.1"></a>
<code class="function">json_each_text</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">text</code> )
       </p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.5.1.2.1"></a>
<code class="function">jsonb_each_text</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>key</code></em> <code class="type">text</code>,
        <em class="parameter"><code>value</code></em> <code class="type">text</code> )
       </p>
<p>
        Expands the top-level JSON object into a set of key/value pairs.
        The returned <em class="parameter"><code>value</code></em>s will be of
        type <code class="type">text</code>.
       </p>
<p>
<code class="literal">select * from json_each_text('{"a":"foo", "b":"bar"}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 key | value
-----+-------
 a   | foo
 b   | bar
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.6.1.1.1"></a>
<code class="function">json_extract_path</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">json</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.6.1.2.1"></a>
<code class="function">jsonb_extract_path</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Extracts JSON sub-object at the specified path.
        (This is functionally equivalent to the <code class="literal">#&gt;</code>
        operator, but writing the path out as a variadic list can be more
        convenient in some cases.)
       </p>
<p>
<code class="literal">json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"foo"}}', 'f4', 'f6')</code>
        → <code class="returnvalue">"foo"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.7.1.1.1"></a>
<code class="function">json_extract_path_text</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">json</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.7.1.2.1"></a>
<code class="function">jsonb_extract_path_text</code> ( <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code>, <code class="literal">VARIADIC</code> <em class="parameter"><code>path_elems</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Extracts JSON sub-object at the specified path as <code class="type">text</code>.
        (This is functionally equivalent to the <code class="literal">#&gt;&gt;</code>
        operator.)
       </p>
<p>
<code class="literal">json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"foo"}}', 'f4', 'f6')</code>
        → <code class="returnvalue">foo</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.8.1.1.1"></a>
<code class="function">json_object_keys</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.8.1.2.1"></a>
<code class="function">jsonb_object_keys</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        Returns the set of keys in the top-level JSON object.
       </p>
<p>
<code class="literal">select * from json_object_keys('{"f1":"abc","f2":{"f3":"a", "f4":"b"}}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 json_object_keys
------------------
 f1
 f2
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.9.1.1.1"></a>
<code class="function">json_populate_record</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">json</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.9.1.2.1"></a>
<code class="function">jsonb_populate_record</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        Expands the top-level JSON object to a row having the composite type
        of the <em class="parameter"><code>base</code></em> argument.  The JSON object
        is scanned for fields whose names match column names of the output row
        type, and their values are inserted into those columns of the output.
        (Fields that do not correspond to any output column name are ignored.)
        In typical use, the value of <em class="parameter"><code>base</code></em> is just
        <code class="literal">NULL</code>, which means that any output columns that do
        not match any object field will be filled with nulls.  However,
        if <em class="parameter"><code>base</code></em> isn't <code class="literal">NULL</code> then
        the values it contains will be used for unmatched columns.
       </p>
<p>
        To convert a JSON value to the SQL type of an output column, the
        following rules are applied in sequence:
        </p><div class="itemizedlist"><ul class="itemizedlist compact" style="list-style-type: disc; "><li class="listitem"><p>
           A JSON null value is converted to an SQL null in all cases.
          </p></li><li class="listitem"><p>
           If the output column is of type <code class="type">json</code>
           or <code class="type">jsonb</code>, the JSON value is just reproduced exactly.
          </p></li><li class="listitem"><p>
           If the output column is a composite (row) type, and the JSON value
           is a JSON object, the fields of the object are converted to columns
           of the output row type by recursive application of these rules.
          </p></li><li class="listitem"><p>
           Likewise, if the output column is an array type and the JSON value
           is a JSON array, the elements of the JSON array are converted to
           elements of the output array by recursive application of these
           rules.
          </p></li><li class="listitem"><p>
           Otherwise, if the JSON value is a string, the contents of the
           string are fed to the input conversion function for the column's
           data type.
          </p></li><li class="listitem"><p>
           Otherwise, the ordinary text representation of the JSON value is
           fed to the input conversion function for the column's data type.
          </p></li></ul></div><p>
</p>
<p>
        While the example below uses a constant JSON value, typical use would
        be to reference a <code class="type">json</code> or <code class="type">jsonb</code> column
        laterally from another table in the query's <code class="literal">FROM</code>
        clause.  Writing <code class="function">json_populate_record</code> in
        the <code class="literal">FROM</code> clause is good practice, since all of the
        extracted columns are available for use without duplicate function
        calls.
       </p>
<p>
<code class="literal">create type subrowtype as (d int, e text);</code>
<code class="literal">create type myrowtype as (a int, b text[], c subrowtype);</code>
</p>
<p>
<code class="literal">select * from json_populate_record(null::myrowtype,
         '{"a": 1, "b": ["2", "a b"], "c": {"d": 4, "e": "a  b c"}, "x": "foo"}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a |   b       |      c
---+-----------+-------------
 1 | {2,"a b"} | (4,"a b c")
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.10.1.1.1"></a>
<code class="function">jsonb_populate_record_valid</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">json</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Function for testing <code class="function">jsonb_populate_record</code>.  Returns
        <code class="literal">true</code> if the input <code class="function">jsonb_populate_record</code>
        would finish without an error for the given input JSON object; that is, it's
        valid input, <code class="literal">false</code> otherwise.
       </p>
<p>
<code class="literal">create type jsb_char2 as (a char(2));</code>
</p>
<p>
<code class="literal">select jsonb_populate_record_valid(NULL::jsb_char2, '{"a": "aaa"}');</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 jsonb_populate_record_valid
-----------------------------
 f
(1 row)
</pre><p>
<code class="literal">select * from jsonb_populate_record(NULL::jsb_char2, '{"a": "aaa"}') q;</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
ERROR:  value too long for type character(2)
</pre><p>
<code class="literal">select jsonb_populate_record_valid(NULL::jsb_char2, '{"a": "aa"}');</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 jsonb_populate_record_valid
-----------------------------
 t
(1 row)
</pre><p>
<code class="literal">select * from jsonb_populate_record(NULL::jsb_char2, '{"a": "aa"}') q;</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a
----
 aa
(1 row)
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.11.1.1.1"></a>
<code class="function">json_populate_recordset</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">json</code> )
        → <code class="returnvalue">setof anyelement</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.11.1.2.1"></a>
<code class="function">jsonb_populate_recordset</code> ( <em class="parameter"><code>base</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>from_json</code></em> <code class="type">jsonb</code> )
        → <code class="returnvalue">setof anyelement</code>
</p>
<p>
        Expands the top-level JSON array of objects to a set of rows having
        the composite type of the <em class="parameter"><code>base</code></em> argument.
        Each element of the JSON array is processed as described above
        for <code class="function">json[b]_populate_record</code>.
       </p>
<p>
<code class="literal">create type twoints as (a int, b int);</code>
</p>
<p>
<code class="literal">select * from json_populate_recordset(null::twoints, '[{"a":1,"b":2}, {"a":3,"b":4}]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a | b
---+---
 1 | 2
 3 | 4
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.12.1.1.1"></a>
<code class="function">json_to_record</code> ( <code class="type">json</code> )
        → <code class="returnvalue">record</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.12.1.2.1"></a>
<code class="function">jsonb_to_record</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">record</code>
</p>
<p>
        Expands the top-level JSON object to a row having the composite type
        defined by an <code class="literal">AS</code> clause.  (As with all functions
        returning <code class="type">record</code>, the calling query must explicitly
        define the structure of the record with an <code class="literal">AS</code>
        clause.)  The output record is filled from fields of the JSON object,
        in the same way as described above
        for <code class="function">json[b]_populate_record</code>.  Since there is no
        input record value, unmatched columns are always filled with nulls.
       </p>
<p>
<code class="literal">create type myrowtype as (a int, b text);</code>
</p>
<p>
<code class="literal">select * from json_to_record('{"a":1,"b":[1,2,3],"c":[1,2,3],"e":"bar","r": {"a": 123, "b": "a b c"}}') as x(a int, b text, c int[], d text, r myrowtype)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a |    b    |    c    | d |       r
---+---------+---------+---+---------------
 1 | [1,2,3] | {1,2,3} |   | (123,"a b c")
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.13.1.1.1"></a>
<code class="function">json_to_recordset</code> ( <code class="type">json</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.13.1.2.1"></a>
<code class="function">jsonb_to_recordset</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        Expands the top-level JSON array of objects to a set of rows having
        the composite type defined by an <code class="literal">AS</code> clause.  (As
        with all functions returning <code class="type">record</code>, the calling query
        must explicitly define the structure of the record with
        an <code class="literal">AS</code> clause.)  Each element of the JSON array is
        processed as described above
        for <code class="function">json[b]_populate_record</code>.
       </p>
<p>
<code class="literal">select * from json_to_recordset('[{"a":1,"b":"foo"}, {"a":"2","c":"bar"}]') as x(a int, b text)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 a |  b
---+-----
 1 | foo
 2 |
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.14.1.1.1"></a>
<code class="function">jsonb_set</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">text[]</code>, <em class="parameter"><code>new_value</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>create_if_missing</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Returns <em class="parameter"><code>target</code></em>
        with the item designated by <em class="parameter"><code>path</code></em>
        replaced by <em class="parameter"><code>new_value</code></em>, or with
        <em class="parameter"><code>new_value</code></em> added if
        <em class="parameter"><code>create_if_missing</code></em> is true (which is the
        default) and the item designated by <em class="parameter"><code>path</code></em>
        does not exist.
        All earlier steps in the path must exist, or
        the <em class="parameter"><code>target</code></em> is returned unchanged.
        As with the path oriented operators, negative integers that
        appear in the <em class="parameter"><code>path</code></em> count from the end
        of JSON arrays.
        If the last path step is an array index that is out of range,
        and <em class="parameter"><code>create_if_missing</code></em> is true, the new
        value is added at the beginning of the array if the index is negative,
        or at the end of the array if it is positive.
       </p>
<p>
<code class="literal">jsonb_set('[{"f1":1,"f2":null},2,null,3]', '{0,f1}', '[2,3,4]', false)</code>
        → <code class="returnvalue">[{"f1": [2, 3, 4], "f2": null}, 2, null, 3]</code>
</p>
<p>
<code class="literal">jsonb_set('[{"f1":1,"f2":null},2]', '{0,f3}', '[2,3,4]')</code>
        → <code class="returnvalue">[{"f1": 1, "f2": null, "f3": [2, 3, 4]}, 2]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.15.1.1.1"></a>
<code class="function">jsonb_set_lax</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">text[]</code>, <em class="parameter"><code>new_value</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>create_if_missing</code></em> <code class="type">boolean</code> [<span class="optional">, <em class="parameter"><code>null_value_treatment</code></em> <code class="type">text</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        If <em class="parameter"><code>new_value</code></em> is not <code class="literal">NULL</code>,
        behaves identically to <code class="literal">jsonb_set</code>. Otherwise behaves
        according to the value
        of <em class="parameter"><code>null_value_treatment</code></em> which must be one
        of <code class="literal">'raise_exception'</code>,
        <code class="literal">'use_json_null'</code>, <code class="literal">'delete_key'</code>, or
        <code class="literal">'return_target'</code>. The default is
        <code class="literal">'use_json_null'</code>.
       </p>
<p>
<code class="literal">jsonb_set_lax('[{"f1":1,"f2":null},2,null,3]', '{0,f1}', null)</code>
        → <code class="returnvalue">[{"f1": null, "f2": null}, 2, null, 3]</code>
</p>
<p>
<code class="literal">jsonb_set_lax('[{"f1":99,"f2":null},2]', '{0,f3}', null, true, 'return_target')</code>
        → <code class="returnvalue">[{"f1": 99, "f2": null}, 2]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.16.1.1.1"></a>
<code class="function">jsonb_insert</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">text[]</code>, <em class="parameter"><code>new_value</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>insert_after</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Returns <em class="parameter"><code>target</code></em>
        with <em class="parameter"><code>new_value</code></em> inserted.  If the item
        designated by the <em class="parameter"><code>path</code></em> is an array
        element, <em class="parameter"><code>new_value</code></em> will be inserted before
        that item if <em class="parameter"><code>insert_after</code></em> is false (which
        is the default), or after it
        if <em class="parameter"><code>insert_after</code></em> is true.  If the item
        designated by the <em class="parameter"><code>path</code></em> is an object
        field, <em class="parameter"><code>new_value</code></em> will be inserted only if
        the object does not already contain that key.
        All earlier steps in the path must exist, or
        the <em class="parameter"><code>target</code></em> is returned unchanged.
        As with the path oriented operators, negative integers that
        appear in the <em class="parameter"><code>path</code></em> count from the end
        of JSON arrays.
        If the last path step is an array index that is out of range, the new
        value is added at the beginning of the array if the index is negative,
        or at the end of the array if it is positive.
       </p>
<p>
<code class="literal">jsonb_insert('{"a": [0,1,2]}', '{a, 1}', '"new_value"')</code>
        → <code class="returnvalue">{"a": [0, "new_value", 1, 2]}</code>
</p>
<p>
<code class="literal">jsonb_insert('{"a": [0,1,2]}', '{a, 1}', '"new_value"', true)</code>
        → <code class="returnvalue">{"a": [0, 1, "new_value", 2]}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.17.1.1.1"></a>
<code class="function">json_strip_nulls</code> ( <em class="parameter"><code>target</code></em> <code class="type">json</code> [<span class="optional">,<em class="parameter"><code>strip_in_arrays</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">json</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.17.1.2.1"></a>
<code class="function">jsonb_strip_nulls</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code> [<span class="optional">,<em class="parameter"><code>strip_in_arrays</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Deletes all object fields that have null values from the given JSON
        value, recursively.
        If <em class="parameter"><code>strip_in_arrays</code></em> is true (the default is false),
        null array elements are also stripped.
        Otherwise they are not stripped. Bare null values are never stripped.
       </p>
<p>
<code class="literal">json_strip_nulls('[{"f1":1, "f2":null}, 2, null, 3]')</code>
        → <code class="returnvalue">[{"f1":1},2,null,3]</code>
</p>
<p>
<code class="literal">jsonb_strip_nulls('[1,2,null,3,4]', true)</code>
        → <code class="returnvalue">[1,2,3,4]</code>
</p>
</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.18.1.1.1"></a>
<code class="function">jsonb_path_exists</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Checks whether the JSON path returns any item for the specified JSON
        value.
        (This is useful only with SQL-standard JSON path expressions, not
        <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">predicate check
        expressions</a>, since those always return a value.)
        If the <em class="parameter"><code>vars</code></em> argument is specified, it must
        be a JSON object, and its fields provide named values to be
        substituted into the <code class="type">jsonpath</code> expression.
        If the <em class="parameter"><code>silent</code></em> argument is specified and
        is <code class="literal">true</code>, the function suppresses the same errors
        as the <code class="literal">@?</code> and <code class="literal">@@</code> operators do.
       </p>
<p>
<code class="literal">jsonb_path_exists('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.19.1.1.1"></a>
<code class="function">jsonb_path_match</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns the SQL boolean result of a JSON path predicate check
        for the specified JSON value.
        (This is useful only
        with <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">predicate
        check expressions</a>, not SQL-standard JSON path expressions,
        since it will either fail or return <code class="literal">NULL</code> if the
        path result is not a single boolean value.)
        The optional <em class="parameter"><code>vars</code></em>
        and <em class="parameter"><code>silent</code></em> arguments act the same as
        for <code class="function">jsonb_path_exists</code>.
       </p>
<p>
<code class="literal">jsonb_path_match('{"a":[1,2,3,4,5]}', 'exists($.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max))', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.20.1.1.1"></a>
<code class="function">jsonb_path_query</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">setof jsonb</code>
</p>
<p>
        Returns all JSON items returned by the JSON path for the specified
        JSON value.
        For SQL-standard JSON path expressions it returns the JSON
        values selected from <em class="parameter"><code>target</code></em>.
        For <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS">predicate
        check expressions</a> it returns the result of the predicate
        check: <code class="literal">true</code>, <code class="literal">false</code>,
        or <code class="literal">null</code>.
        The optional <em class="parameter"><code>vars</code></em>
        and <em class="parameter"><code>silent</code></em> arguments act the same as
        for <code class="function">jsonb_path_exists</code>.
       </p>
<p>
<code class="literal">select * from jsonb_path_query('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 jsonb_path_query
------------------
 2
 3
 4
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.21.1.1.1"></a>
<code class="function">jsonb_path_query_array</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Returns all JSON items returned by the JSON path for the specified
        JSON value, as a JSON array.
        The parameters are the same as
        for <code class="function">jsonb_path_query</code>.
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">[2, 3, 4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.22.1.1.1"></a>
<code class="function">jsonb_path_query_first</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        Returns the first JSON item returned by the JSON path for the
        specified JSON value, or <code class="literal">NULL</code> if there are no
        results.
        The parameters are the same as
        for <code class="function">jsonb_path_query</code>.
       </p>
<p>
<code class="literal">jsonb_path_query_first('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.1.1"></a>
<code class="function">jsonb_path_exists_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.2.1"></a>
<code class="function">jsonb_path_match_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.3.1"></a>
<code class="function">jsonb_path_query_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">setof jsonb</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.4.1"></a>
<code class="function">jsonb_path_query_array_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.23.1.5.1"></a>
<code class="function">jsonb_path_query_first_tz</code> ( <em class="parameter"><code>target</code></em> <code class="type">jsonb</code>, <em class="parameter"><code>path</code></em> <code class="type">jsonpath</code> [<span class="optional">, <em class="parameter"><code>vars</code></em> <code class="type">jsonb</code> [<span class="optional">, <em class="parameter"><code>silent</code></em> <code class="type">boolean</code> </span>]</span>] )
        → <code class="returnvalue">jsonb</code>
</p>
<p>
        These functions act like their counterparts described above without
        the <code class="literal">_tz</code> suffix, except that these functions support
        comparisons of date/time values that require timezone-aware
        conversions.  The example below requires interpretation of the
        date-only value <code class="literal">2015-08-02</code> as a timestamp with time
        zone, so the result depends on the current
        <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE">TimeZone</a> setting.  Due to this dependency, these
        functions are marked as stable, which means these functions cannot be
        used in indexes.  Their counterparts are immutable, and so can be used
        in indexes; but they will throw errors if asked to make such
        comparisons.
       </p>
<p>
<code class="literal">jsonb_path_exists_tz('["2015-08-01 12:00:00-05"]', '$[*] ? (@.datetime() &lt; "2015-08-02".datetime())')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.24.1.1.1"></a>
<code class="function">jsonb_pretty</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Converts the given JSON value to pretty-printed, indented text.
       </p>
<p>
<code class="literal">jsonb_pretty('[{"f1":1,"f2":null}, 2]')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
[
    {
        "f1": 1,
        "f2": null
    },
    2
]
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.25.1.1.1"></a>
<code class="function">json_typeof</code> ( <code class="type">json</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.8.13.2.2.25.1.2.1"></a>
<code class="function">jsonb_typeof</code> ( <code class="type">jsonb</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the type of the top-level JSON value as a text string.
        Possible types are
        <code class="literal">object</code>, <code class="literal">array</code>,
        <code class="literal">string</code>, <code class="literal">number</code>,
        <code class="literal">boolean</code>, and <code class="literal">null</code>.
        (The <code class="literal">null</code> result should not be confused
        with an SQL NULL; see the examples.)
       </p>
<p>
<code class="literal">json_typeof('-123.4')</code>
        → <code class="returnvalue">number</code>
</p>
<p>
<code class="literal">json_typeof('null'::json)</code>
        → <code class="returnvalue">null</code>
</p>
<p>
<code class="literal">json_typeof(NULL::json) IS NULL</code>
        → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-SQLJSON-PATH"></a>

### 9.16.2. The SQL/JSON Path Language [#](#FUNCTIONS-SQLJSON-PATH)

<a id="id-1.5.8.22.9.2"></a>

SQL/JSON path expressions specify item(s) to be retrieved
from a JSON value, similarly to XPath expressions used
for access to XML content. In PostgreSQL,
path expressions are implemented as the `jsonpath`
data type and can use any elements described in
[Section 8.14.7](../datatype/datatype-json.md#DATATYPE-JSONPATH).

JSON query functions and operators
pass the provided path expression to the *path engine*
for evaluation. If the expression matches the queried JSON data,
the corresponding JSON item, or set of items, is returned.
If there is no match, the result will be `NULL`,
`false`, or an error, depending on the function.
Path expressions are written in the SQL/JSON path language
and can include arithmetic expressions and functions.

A path expression consists of a sequence of elements allowed
by the `jsonpath` data type.
The path expression is normally evaluated from left to right, but
you can use parentheses to change the order of operations.
If the evaluation is successful, a sequence of JSON items is produced,
and the evaluation result is returned to the JSON query function
that completes the specified computation.

To refer to the JSON value being queried (the
*context item*), use the `$` variable
in the path expression. The first element of a path must always
be `$`. It can be followed by one or more
[accessor operators](../datatype/datatype-json.md#TYPE-JSONPATH-ACCESSORS),
which go down the JSON structure level by level to retrieve sub-items
of the context item. Each accessor operator acts on the
result(s) of the previous evaluation step, producing zero, one, or more
output items from each input item.

For example, suppose you have some JSON data from a GPS tracker that you
would like to parse, such as:

```

SELECT '{
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
}' AS json \gset
```

(The above example can be copied-and-pasted
into psql to set things up for the following
examples. Then psql will
expand `:'json'` into a suitably-quoted string
constant containing the JSON value.)

To retrieve the available track segments, you need to use the
`.key` accessor
operator to descend through surrounding JSON objects, for example:

```

=> select jsonb_path_query(:'json', '$.track.segments');
                                                                         jsonb_path_query
-----------------------------------------------------------​-----------------------------------------------------------​---------------------------------------------
 [{"HR": 73, "location": [47.763, 13.4034], "start time": "2018-10-14 10:05:14"}, {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}]
```

To retrieve the contents of an array, you typically use the
`[*]` operator.
The following example will return the location coordinates for all
the available track segments:

```

=> select jsonb_path_query(:'json', '$.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

Here we started with the whole JSON input value (`$`),
then the `.track` accessor selected the JSON object
associated with the `"track"` object key, then
the `.segments` accessor selected the JSON array
associated with the `"segments"` key within that
object, then the `[*]` accessor selected each element
of that array (producing a series of items), then
the `.location` accessor selected the JSON array
associated with the `"location"` key within each of
those objects. In this example, each of those objects had
a `"location"` key; but if any of them did not,
the `.location` accessor would have simply produced no
output for that input item.

To return the coordinates of the first segment only, you can
specify the corresponding subscript in the `[]`
accessor operator. Recall that JSON array indexes are 0-relative:

```

=> select jsonb_path_query(:'json', '$.track.segments[0].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
```

The result of each path evaluation step can be processed
by one or more of the `jsonpath` operators and methods
listed in [Section 9.16.2.3](functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS).
Each method name must be preceded by a dot. For example,
you can get the size of an array:

```

=> select jsonb_path_query(:'json', '$.track.segments.size()');
 jsonb_path_query
------------------
 2
```

More examples of using `jsonpath` operators
and methods within path expressions appear below in
[Section 9.16.2.3](functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS).

A path can also contain
*filter expressions* that work similarly to the
`WHERE` clause in SQL. A filter expression begins with
a question mark and provides a condition in parentheses:

```

? (condition)
```

Filter expressions must be written just after the path evaluation step
to which they should apply. The result of that step is filtered to include
only those items that satisfy the provided condition. SQL/JSON defines
three-valued logic, so the condition can
produce `true`, `false`,
or `unknown`. The `unknown` value
plays the same role as SQL `NULL` and can be tested
for with the `is unknown` predicate. Further path
evaluation steps use only those items for which the filter expression
returned `true`.

The functions and operators that can be used in filter expressions are
listed in [Table 9.53](functions-json.md#FUNCTIONS-SQLJSON-FILTER-EX-TABLE). Within a
filter expression, the `@` variable denotes the value
being considered (i.e., one result of the preceding path step). You can
write accessor operators after `@` to retrieve component
items.

For example, suppose you would like to retrieve all heart rate values higher
than 130. You can achieve this as follows:

```

=> select jsonb_path_query(:'json', '$.track.segments[*].HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

To get the start times of segments with such values, you have to
filter out irrelevant segments before selecting the start times, so the
filter expression is applied to the previous step, and the path used
in the condition is different:

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

You can use several filter expressions in sequence, if required.
The following example selects start times of all segments that
contain locations with relevant coordinates and high heart rate values:

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4) ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

Using filter expressions at different nesting levels is also allowed.
The following example first filters all segments by location, and then
returns high heart rate values for these segments, if available:

```

=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4).HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

You can also nest filter expressions within each other.
This example returns the size of the track if it contains any
segments with high heart rate values, or an empty sequence otherwise:

```

=> select jsonb_path_query(:'json', '$.track ? (exists(@.segments[*] ? (@.HR > 130))).segments.size()');
 jsonb_path_query
------------------
 2
```

<a id="FUNCTIONS-SQLJSON-DEVIATIONS"></a>

#### 9.16.2.1. Deviations from the SQL Standard [#](#FUNCTIONS-SQLJSON-DEVIATIONS)

PostgreSQL's implementation of the SQL/JSON path
language has the following deviations from the SQL/JSON standard.

<a id="FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS"></a>

##### 9.16.2.1.1. Boolean Predicate Check Expressions [#](#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS)

As an extension to the SQL standard,
a PostgreSQL path expression can be a
Boolean predicate, whereas the SQL standard allows predicates only within
filters. While SQL-standard path expressions return the relevant
element(s) of the queried JSON value, predicate check expressions
return the single three-valued `jsonb` result of the
predicate: `true`,
`false`, or `null`.
For example, we could write this SQL-standard filter expression:

```

=> select jsonb_path_query(:'json', '$.track.segments ?(@[*].HR > 130)');
                                jsonb_path_query
-----------------------------------------------------------​----------------------
 {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}
```

The similar predicate check expression simply
returns `true`, indicating that a match exists:

```

=> select jsonb_path_query(:'json', '$.track.segments[*].HR > 130');
 jsonb_path_query
------------------
 true
```

### Note

Predicate check expressions are required in the
`@@` operator (and the
`jsonb_path_match` function), and should not be used
with the `@?` operator (or the
`jsonb_path_exists` function).

<a id="FUNCTIONS-SQLJSON-REGULAR-EXPRESSION-DEVIATION"></a>

##### 9.16.2.1.2. Regular Expression Interpretation [#](#FUNCTIONS-SQLJSON-REGULAR-EXPRESSION-DEVIATION)

There are minor differences in the interpretation of regular
expression patterns used in `like_regex` filters, as
described in [Section 9.16.2.4](functions-json.md#JSONPATH-REGULAR-EXPRESSIONS).

<a id="FUNCTIONS-SQLJSON-STRICT-AND-LAX-MODES"></a>

#### 9.16.2.2. Strict and Lax Modes [#](#FUNCTIONS-SQLJSON-STRICT-AND-LAX-MODES)

When you query JSON data, the path expression may not match the
actual JSON data structure. An attempt to access a non-existent
member of an object or element of an array is defined as a
structural error. SQL/JSON path expressions have two modes
of handling structural errors:

* lax (default) — the path engine implicitly adapts
  the queried data to the specified path.
  Any structural errors that cannot be fixed as described below
  are suppressed, producing no match.
* strict — if a structural error occurs, an error is raised.

Lax mode facilitates matching of a JSON document and path
expression when the JSON data does not conform to the expected schema.
If an operand does not match the requirements of a particular operation,
it can be automatically wrapped as an SQL/JSON array, or unwrapped by
converting its elements into an SQL/JSON sequence before performing
the operation. Also, comparison operators automatically unwrap their
operands in lax mode, so you can compare SQL/JSON arrays
out-of-the-box. An array of size 1 is considered equal to its sole element.
Automatic unwrapping is not performed when:

* The path expression contains `type()` or
  `size()` methods that return the type
  and the number of elements in the array, respectively.
* The queried JSON data contain nested arrays. In this case, only
  the outermost array is unwrapped, while all the inner arrays
  remain unchanged. Thus, implicit unwrapping can only go one
  level down within each path evaluation step.

For example, when querying the GPS data listed above, you can
abstract from the fact that it stores an array of segments
when using lax mode:

```

=> select jsonb_path_query(:'json', 'lax $.track.segments.location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

In strict mode, the specified path must exactly match the structure of
the queried JSON document, so using this path
expression will cause an error:

```

=> select jsonb_path_query(:'json', 'strict $.track.segments.location');
ERROR:  jsonpath member accessor can only be applied to an object
```

To get the same result as in lax mode, you have to explicitly unwrap the
`segments` array:

```

=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

The unwrapping behavior of lax mode can lead to surprising results. For
instance, the following query using the `.**` accessor
selects every `HR` value twice:

```

=> select jsonb_path_query(:'json', 'lax $.**.HR');
 jsonb_path_query
------------------
 73
 135
 73
 135
```

This happens because the `.**` accessor selects both
the `segments` array and each of its elements, while
the `.HR` accessor automatically unwraps arrays when
using lax mode. To avoid surprising results, we recommend using
the `.**` accessor only in strict mode. The
following query selects each `HR` value just once:

```

=> select jsonb_path_query(:'json', 'strict $.**.HR');
 jsonb_path_query
------------------
 73
 135
```

The unwrapping of arrays can also lead to unexpected results. Consider this
example, which selects all the `location` arrays:

```

=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

As expected it returns the full arrays. But applying a filter expression
causes the arrays to be unwrapped to evaluate each item, returning only the
items that match the expression:

```

=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
------------------
 47.763
 47.706
(2 rows)
```

This despite the fact that the full arrays are selected by the path
expression. Use strict mode to restore selecting the arrays:

```

=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

<a id="FUNCTIONS-SQLJSON-PATH-OPERATORS"></a>

#### 9.16.2.3. SQL/JSON Path Operators and Methods [#](#FUNCTIONS-SQLJSON-PATH-OPERATORS)

[Table 9.52](functions-json.md#FUNCTIONS-SQLJSON-OP-TABLE) shows the operators and
methods available in `jsonpath`. Note that while the unary
operators and methods can be applied to multiple values resulting from a
preceding path step, the binary operators (addition etc.) can only be
applied to single values. In lax mode, methods applied to an array will be
executed for each value in the array. The exceptions are
`.type()` and `.size()`, which apply to
the array itself.

<a id="FUNCTIONS-SQLJSON-OP-TABLE"></a>

**Table 9.52. `jsonpath` Operators and Methods**

<table border="1" class="table" summary="jsonpath Operators and Methods"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator/Method
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">+</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Addition
       </p>
<p>
<code class="literal">jsonb_path_query('[2]', '$[0] + 3')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">+</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Unary plus (no operation); unlike addition, this can iterate over
        multiple values
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": [2,3,4]}', '+ $.x')</code>
        → <code class="returnvalue">[2, 3, 4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Subtraction
       </p>
<p>
<code class="literal">jsonb_path_query('[2]', '7 - $[0]')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">-</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Negation; unlike subtraction, this can iterate over
        multiple values
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": [2,3,4]}', '- $.x')</code>
        → <code class="returnvalue">[-2, -3, -4]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">*</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Multiplication
       </p>
<p>
<code class="literal">jsonb_path_query('[4]', '2 * $[0]')</code>
        → <code class="returnvalue">8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">/</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Division
       </p>
<p>
<code class="literal">jsonb_path_query('[8.5]', '$[0] / 2')</code>
        → <code class="returnvalue">4.2500000000000000</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">%</code> <em class="replaceable"><code>number</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Modulo (remainder)
       </p>
<p>
<code class="literal">jsonb_path_query('[32]', '$[0] % 10')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">type()</code>
        → <code class="returnvalue"><em class="replaceable"><code>string</code></em></code>
</p>
<p>
        Type of the JSON item (see <code class="function">json_typeof</code>)
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "2", {}]', '$[*].type()')</code>
        → <code class="returnvalue">["number", "string", "object"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">size()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Size of the JSON item (number of array elements, or 1 if not an
        array)
       </p>
<p>
<code class="literal">jsonb_path_query('{"m": [11, 15]}', '$.m.size()')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">boolean()</code>
        → <code class="returnvalue"><em class="replaceable"><code>boolean</code></em></code>
</p>
<p>
        Boolean value converted from a JSON boolean, number, or string
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "yes", false]', '$[*].boolean()')</code>
        → <code class="returnvalue">[true, true, false]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">string()</code>
        → <code class="returnvalue"><em class="replaceable"><code>string</code></em></code>
</p>
<p>
        String value converted from a JSON boolean, number, string, or
        datetime
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1.23, "xyz", false]', '$[*].string()')</code>
        → <code class="returnvalue">["1.23", "xyz", "false"]</code>
</p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp().string()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">double()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Approximate floating-point number converted from a JSON number or
        string
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "1.9"}', '$.len.double() * 2')</code>
        → <code class="returnvalue">3.8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">ceiling()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Nearest integer greater than or equal to the given number
       </p>
<p>
<code class="literal">jsonb_path_query('{"h": 1.3}', '$.h.ceiling()')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">floor()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Nearest integer less than or equal to the given number
       </p>
<p>
<code class="literal">jsonb_path_query('{"h": 1.7}', '$.h.floor()')</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>number</code></em> <code class="literal">.</code> <code class="literal">abs()</code>
        → <code class="returnvalue"><em class="replaceable"><code>number</code></em></code>
</p>
<p>
        Absolute value of the given number
       </p>
<p>
<code class="literal">jsonb_path_query('{"z": -0.3}', '$.z.abs()')</code>
        → <code class="returnvalue">0.3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">bigint()</code>
        → <code class="returnvalue"><em class="replaceable"><code>bigint</code></em></code>
</p>
<p>
        Big integer value converted from a JSON number or string
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "9876543219"}', '$.len.bigint()')</code>
        → <code class="returnvalue">9876543219</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">decimal( [ <em class="replaceable"><code>precision</code></em> [ , <em class="replaceable"><code>scale</code></em> ] ] )</code>
        → <code class="returnvalue"><em class="replaceable"><code>decimal</code></em></code>
</p>
<p>
        Rounded decimal value converted from a JSON number or string
        (<code class="literal">precision</code> and <code class="literal">scale</code> must be
        integer values)
       </p>
<p>
<code class="literal">jsonb_path_query('1234.5678', '$.decimal(6, 2)')</code>
        → <code class="returnvalue">1234.57</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">integer()</code>
        → <code class="returnvalue"><em class="replaceable"><code>integer</code></em></code>
</p>
<p>
        Integer value converted from a JSON number or string
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "12345"}', '$.len.integer()')</code>
        → <code class="returnvalue">12345</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">.</code> <code class="literal">number()</code>
        → <code class="returnvalue"><em class="replaceable"><code>numeric</code></em></code>
</p>
<p>
        Numeric value converted from a JSON number or string
       </p>
<p>
<code class="literal">jsonb_path_query('{"len": "123.45"}', '$.len.number()')</code>
        → <code class="returnvalue">123.45</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">datetime()</code>
        → <code class="returnvalue"><em class="replaceable"><code>datetime_type</code></em></code>
        (see note)
       </p>
<p>
        Date/time value converted from a string
       </p>
<p>
<code class="literal">jsonb_path_query('["2015-8-1", "2015-08-12"]', '$[*] ? (@.datetime() &lt; "2015-08-2".datetime())')</code>
        → <code class="returnvalue">"2015-8-1"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">datetime(<em class="replaceable"><code>template</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>datetime_type</code></em></code>
        (see note)
       </p>
<p>
        Date/time value converted from a string using the
        specified <code class="function">to_timestamp</code> template
       </p>
<p>
<code class="literal">jsonb_path_query_array('["12:30", "18:40"]', '$[*].datetime("HH24:MI")')</code>
        → <code class="returnvalue">["12:30:00", "18:40:00"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">date()</code>
        → <code class="returnvalue"><em class="replaceable"><code>date</code></em></code>
</p>
<p>
        Date value converted from a string
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15"', '$.date()')</code>
        → <code class="returnvalue">"2023-08-15"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time()</code>
        → <code class="returnvalue"><em class="replaceable"><code>time without time zone</code></em></code>
</p>
<p>
        Time without time zone value converted from a string
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56"', '$.time()')</code>
        → <code class="returnvalue">"12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>time without time zone</code></em></code>
</p>
<p>
        Time without time zone value converted from a string, with fractional
        seconds adjusted to the given precision
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56.789"', '$.time(2)')</code>
        → <code class="returnvalue">"12:34:56.79"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time_tz()</code>
        → <code class="returnvalue"><em class="replaceable"><code>time with time zone</code></em></code>
</p>
<p>
        Time with time zone value converted from a string
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56 +05:30"', '$.time_tz()')</code>
        → <code class="returnvalue">"12:34:56+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">time_tz(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>time with time zone</code></em></code>
</p>
<p>
        Time with time zone value converted from a string, with fractional
        seconds adjusted to the given precision
       </p>
<p>
<code class="literal">jsonb_path_query('"12:34:56.789 +05:30"', '$.time_tz(2)')</code>
        → <code class="returnvalue">"12:34:56.79+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp()</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp without time zone</code></em></code>
</p>
<p>
        Timestamp without time zone value converted from a string
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp without time zone</code></em></code>
</p>
<p>
        Timestamp without time zone value converted from a string, with
        fractional seconds adjusted to the given precision
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56.789"', '$.timestamp(2)')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56.79"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp_tz()</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp with time zone</code></em></code>
</p>
<p>
        Timestamp with time zone value converted from a string
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56 +05:30"', '$.timestamp_tz()')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">.</code> <code class="literal">timestamp_tz(<em class="replaceable"><code>precision</code></em>)</code>
        → <code class="returnvalue"><em class="replaceable"><code>timestamp with time zone</code></em></code>
</p>
<p>
        Timestamp with time zone value converted from a string, with fractional
        seconds adjusted to the given precision
       </p>
<p>
<code class="literal">jsonb_path_query('"2023-08-15 12:34:56.789 +05:30"', '$.timestamp_tz(2)')</code>
        → <code class="returnvalue">"2023-08-15T12:34:56.79+05:30"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>object</code></em> <code class="literal">.</code> <code class="literal">keyvalue()</code>
        → <code class="returnvalue"><em class="replaceable"><code>array</code></em></code>
</p>
<p>
        The object's key-value pairs, represented as an array of objects
        containing three fields: <code class="literal">"key"</code>,
        <code class="literal">"value"</code>, and <code class="literal">"id"</code>;
        <code class="literal">"id"</code> is a unique identifier of the object the
        key-value pair belongs to
       </p>
<p>
<code class="literal">jsonb_path_query_array('{"x": "20", "y": 32}', '$.keyvalue()')</code>
        → <code class="returnvalue">[{"id": 0, "key": "x", "value": "20"}, {"id": 0, "key": "y", "value": 32}]</code>
</p></td></tr></tbody></table>

<br>

### Note

The result type of the `datetime()` and
`datetime(template)`
methods can be `date`, `timetz`, `time`,
`timestamptz`, or `timestamp`.
Both methods determine their result type dynamically.

The `datetime()` method sequentially tries to
match its input string to the ISO formats
for `date`, `timetz`, `time`,
`timestamptz`, and `timestamp`. It stops on
the first matching format and emits the corresponding data type.

The `datetime(template)`
method determines the result type according to the fields used in the
provided template string.

The `datetime()` and
`datetime(template)` methods
use the same parsing rules as the `to_timestamp` SQL
function does (see [Section 9.8](functions-formatting.md)), with three
exceptions. First, these methods don't allow unmatched template
patterns. Second, only the following separators are allowed in the
template string: minus sign, period, solidus (slash), comma, apostrophe,
semicolon, colon and space. Third, separators in the template string
must exactly match the input string.

If different date/time types need to be compared, an implicit cast is
applied. A `date` value can be cast to `timestamp`
or `timestamptz`, `timestamp` can be cast to
`timestamptz`, and `time` to `timetz`.
However, all but the first of these conversions depend on the current
[TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) setting, and thus can only be performed
within timezone-aware `jsonpath` functions. Similarly, other
date/time-related methods that convert strings to date/time types
also do this casting, which may involve the current
[TimeZone](../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE) setting. Therefore, these conversions can
also only be performed within timezone-aware `jsonpath`
functions.

[Table 9.53](functions-json.md#FUNCTIONS-SQLJSON-FILTER-EX-TABLE) shows the available
filter expression elements.

<a id="FUNCTIONS-SQLJSON-FILTER-EX-TABLE"></a>

**Table 9.53. `jsonpath` Filter Expression Elements**

<table border="1" class="table" summary="jsonpath Filter Expression Elements"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Predicate/Value
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">==</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Equality comparison (this, and the other comparison operators, work on
        all JSON scalar values)
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == 1)')</code>
        → <code class="returnvalue">[1, 1]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == "a")')</code>
        → <code class="returnvalue">["a"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">!=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;&gt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Non-equality comparison
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 1, 3]', '$[*] ? (@ != 1)')</code>
        → <code class="returnvalue">[2, 3]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;&gt; "b")')</code>
        → <code class="returnvalue">["a", "c"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Less-than comparison
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &lt; 2)')</code>
        → <code class="returnvalue">[1]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&lt;=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Less-than-or-equal-to comparison
       </p>
<p>
<code class="literal">jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;= "b")')</code>
        → <code class="returnvalue">["a", "b"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&gt;</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Greater-than comparison
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt; 2)')</code>
        → <code class="returnvalue">[3]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>value</code></em> <code class="literal">&gt;=</code> <em class="replaceable"><code>value</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Greater-than-or-equal-to comparison
       </p>
<p>
<code class="literal">jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt;= 2)')</code>
        → <code class="returnvalue">[2, 3]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">true</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        JSON constant <code class="literal">true</code>
</p>
<p>
<code class="literal">jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == true)')</code>
        → <code class="returnvalue">{"name": "Chris", "parent": true}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">false</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        JSON constant <code class="literal">false</code>
</p>
<p>
<code class="literal">jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == false)')</code>
        → <code class="returnvalue">{"name": "John", "parent": false}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">null</code>
        → <code class="returnvalue"><em class="replaceable"><code>value</code></em></code>
</p>
<p>
        JSON constant <code class="literal">null</code> (note that, unlike in SQL,
        comparison to <code class="literal">null</code> works normally)
       </p>
<p>
<code class="literal">jsonb_path_query('[{"name": "Mary", "job": null}, {"name": "Michael", "job": "driver"}]', '$[*] ? (@.job == null) .name')</code>
        → <code class="returnvalue">"Mary"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">&amp;&amp;</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Boolean AND
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &gt; 1 &amp;&amp; @ &lt; 5)')</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">||</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Boolean OR
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &lt; 1 || @ &gt; 5)')</code>
        → <code class="returnvalue">7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">!</code> <em class="replaceable"><code>boolean</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Boolean NOT
       </p>
<p>
<code class="literal">jsonb_path_query('[1, 3, 7]', '$[*] ? (!(@ &lt; 5))')</code>
        → <code class="returnvalue">7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>boolean</code></em> <code class="literal">is unknown</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether a Boolean condition is <code class="literal">unknown</code>.
       </p>
<p>
<code class="literal">jsonb_path_query('[-1, 2, 7, "foo"]', '$[*] ? ((@ &gt; 0) is unknown)')</code>
        → <code class="returnvalue">"foo"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">like_regex</code> <em class="replaceable"><code>string</code></em> [<span class="optional"> <code class="literal">flag</code> <em class="replaceable"><code>string</code></em> </span>]
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether the first operand matches the regular expression
        given by the second operand, optionally with modifications
        described by a string of <code class="literal">flag</code> characters (see
        <a class="xref" href="functions-json.md#JSONPATH-REGULAR-EXPRESSIONS">Section 9.16.2.4</a>).
       </p>
<p>
<code class="literal">jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c")')</code>
        → <code class="returnvalue">["abc", "abdacb"]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c" flag "i")')</code>
        → <code class="returnvalue">["abc", "aBdC", "abdacb"]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>string</code></em> <code class="literal">starts with</code> <em class="replaceable"><code>string</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether the second operand is an initial substring of the first
        operand.
       </p>
<p>
<code class="literal">jsonb_path_query('["John Smith", "Mary Stone", "Bob Johnson"]', '$[*] ? (@ starts with "John")')</code>
        → <code class="returnvalue">"John Smith"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">exists</code> <code class="literal">(</code> <em class="replaceable"><code>path_expression</code></em> <code class="literal">)</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether a path expression matches at least one SQL/JSON item.
        Returns <code class="literal">unknown</code> if the path expression would result
        in an error; the second example uses this to avoid a no-such-key error
        in strict mode.
       </p>
<p>
<code class="literal">jsonb_path_query('{"x": [1, 2], "y": [2, 4]}', 'strict $.* ? (exists (@ ? (@[*] &gt; 2)))')</code>
        → <code class="returnvalue">[2, 4]</code>
</p>
<p>
<code class="literal">jsonb_path_query_array('{"value": 41}', 'strict $ ? (exists (@.name)) .name')</code>
        → <code class="returnvalue">[]</code>
</p></td></tr></tbody></table>

<br>

<a id="JSONPATH-REGULAR-EXPRESSIONS"></a>

#### 9.16.2.4. SQL/JSON Regular Expressions [#](#JSONPATH-REGULAR-EXPRESSIONS)

<a id="id-1.5.8.22.9.23.2"></a>

SQL/JSON path expressions allow matching text to a regular expression
with the `like_regex` filter. For example, the
following SQL/JSON path query would case-insensitively match all
strings in an array that start with an English vowel:

```

$[*] ? (@ like_regex "^[aeiou]" flag "i")
```

The optional `flag` string may include one or more of
the characters
`i` for case-insensitive match,
`m` to allow `^`
and `$` to match at newlines,
`s` to allow `.` to match a newline,
and `q` to quote the whole pattern (reducing the
behavior to a simple substring match).

The SQL/JSON standard borrows its definition for regular expressions
from the `LIKE_REGEX` operator, which in turn uses the
XQuery standard. PostgreSQL does not currently support the
`LIKE_REGEX` operator. Therefore,
the `like_regex` filter is implemented using the
POSIX regular expression engine described in
[Section 9.7.3](functions-matching.md#FUNCTIONS-POSIX-REGEXP). This leads to various minor
discrepancies from standard SQL/JSON behavior, which are cataloged in
[Section 9.7.3.8](functions-matching.md#POSIX-VS-XQUERY).
Note, however, that the flag-letter incompatibilities described there
do not apply to SQL/JSON, as it translates the XQuery flag letters to
match what the POSIX engine expects.

Keep in mind that the pattern argument of `like_regex`
is a JSON path string literal, written according to the rules given in
[Section 8.14.7](../datatype/datatype-json.md#DATATYPE-JSONPATH). This means in particular that any
backslashes you want to use in the regular expression must be doubled.
For example, to match string values of the root document that contain
only digits:

```

$.* ? (@ like_regex "^\\d+$")
```

<a id="SQLJSON-QUERY-FUNCTIONS"></a>

### 9.16.3. SQL/JSON Query Functions [#](#SQLJSON-QUERY-FUNCTIONS)

SQL/JSON functions `JSON_EXISTS()`,
`JSON_QUERY()`, and `JSON_VALUE()`
described in [Table 9.54](functions-json.md#FUNCTIONS-SQLJSON-QUERYING) can be used
to query JSON documents. Each of these functions apply a
*`path_expression`* (an SQL/JSON path query) to a
*`context_item`* (the document). See
[Section 9.16.2](functions-json.md#FUNCTIONS-SQLJSON-PATH) for more details on what
the *`path_expression`* can contain. The
*`path_expression`* can also reference variables,
whose values are specified with their respective names in the
`PASSING` clause that is supported by each function.
*`context_item`* can be a `jsonb` value
or a character string that can be successfully cast to `jsonb`.

<a id="FUNCTIONS-SQLJSON-QUERYING"></a>

**Table 9.54. SQL/JSON Query Functions**

<table border="1" class="table" summary="SQL/JSON Query Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function signature
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
      </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.10.3.2.2.1.1.1.1"></a>
</p><pre class="synopsis">
<code class="function">JSON_EXISTS</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>]
[<span class="optional">{ <code class="literal">TRUE</code> | <code class="literal">FALSE</code> |<code class="literal"> UNKNOWN</code> | <code class="literal">ERROR</code> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">boolean</code>
</pre><p class="func_signature">
</p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
        Returns true if the SQL/JSON <em class="replaceable"><code>path_expression</code></em>
        applied to the <em class="replaceable"><code>context_item</code></em> yields any
        items, false otherwise.
       </p></li><li class="listitem"><p>
        The <code class="literal">ON ERROR</code> clause specifies the behavior if
        an error occurs during <em class="replaceable"><code>path_expression</code></em>
        evaluation.  Specifying <code class="literal">ERROR</code> will cause an error to
        be thrown with the appropriate message.  Other options include
        returning <code class="type">boolean</code> values <code class="literal">FALSE</code> or
        <code class="literal">TRUE</code> or the value <code class="literal">UNKNOWN</code> which
        is actually an SQL NULL. The default when no <code class="literal">ON ERROR</code>
        clause is specified is to return the <code class="type">boolean</code> value
        <code class="literal">FALSE</code>.
       </p></li></ul></div>
<p>
        Examples:
       </p>
<p>
<code class="literal">JSON_EXISTS(jsonb '{"key1": [1,2,3]}', 'strict $.key1[*] ? (@ &gt; $x)' PASSING 2 AS x)</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">JSON_EXISTS(jsonb '{"a": [1,2,3]}', 'lax $.a[5]' ERROR ON ERROR)</code>
        → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">JSON_EXISTS(jsonb '{"a": [1,2,3]}', 'strict $.a[5]' ERROR ON ERROR)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
ERROR:  jsonpath array subscript is out of bounds
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.10.3.2.2.2.1.1.1"></a>
</p><pre class="synopsis">
<code class="function">JSON_QUERY</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>]
[<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>]
[<span class="optional"> { <code class="literal">WITHOUT</code> | <code class="literal">WITH</code> { <code class="literal">CONDITIONAL</code> | [<span class="optional"><code class="literal">UNCONDITIONAL</code></span>] } } [<span class="optional"> <code class="literal">ARRAY</code> </span>] <code class="literal">WRAPPER</code> </span>]
[<span class="optional"> { <code class="literal">KEEP</code> | <code class="literal">OMIT</code> } <code class="literal">QUOTES</code> [<span class="optional"> <code class="literal">ON SCALAR STRING</code> </span>] </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">EMPTY</code> { [<span class="optional"> <code class="literal">ARRAY</code> </span>] | <code class="literal">OBJECT</code> } | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON EMPTY</code> </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">EMPTY</code> { [<span class="optional"> <code class="literal">ARRAY</code> </span>] | <code class="literal">OBJECT</code> } | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">jsonb</code>
</pre><p class="func_signature">
</p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
        Returns the result of applying the SQL/JSON
        <em class="replaceable"><code>path_expression</code></em> to the
        <em class="replaceable"><code>context_item</code></em>.
       </p></li><li class="listitem"><p>
         By default, the result is returned as a value of type <code class="type">jsonb</code>,
         though the <code class="literal">RETURNING</code> clause can be used to return
         as some other type to which it can be successfully coerced.
       </p></li><li class="listitem"><p>
        If the path expression may return multiple values, it might be necessary
        to wrap those values using the <code class="literal">WITH WRAPPER</code> clause to
        make it a valid JSON string, because the default behavior is to not wrap
        them, as if <code class="literal">WITHOUT WRAPPER</code> were specified. The
        <code class="literal">WITH WRAPPER</code> clause is by default taken to mean
        <code class="literal">WITH UNCONDITIONAL WRAPPER</code>, which means that even a
        single result value will be wrapped. To apply the wrapper only when
        multiple values are present, specify <code class="literal">WITH CONDITIONAL WRAPPER</code>.
        Getting multiple values in result will be treated as an error if
        <code class="literal">WITHOUT WRAPPER</code> is specified.
       </p></li><li class="listitem"><p>
        If the result is a scalar string, by default, the returned value will
        be surrounded by quotes, making it a valid JSON value.  It can be made
        explicit by specifying <code class="literal">KEEP QUOTES</code>.  Conversely,
        quotes can be omitted by specifying <code class="literal">OMIT QUOTES</code>.
        To ensure that the result is a valid JSON value, <code class="literal">OMIT QUOTES</code>
        cannot be specified when <code class="literal">WITH WRAPPER</code> is also
        specified.
       </p></li><li class="listitem"><p>
        The <code class="literal">ON EMPTY</code> clause specifies the behavior if
        evaluating <em class="replaceable"><code>path_expression</code></em> yields an empty
        set. The <code class="literal">ON ERROR</code> clause specifies the behavior
        if an error occurs when evaluating <em class="replaceable"><code>path_expression</code></em>,
        when coercing the result value to the <code class="literal">RETURNING</code> type,
        or when evaluating the <code class="literal">ON EMPTY</code> expression if the
        <em class="replaceable"><code>path_expression</code></em> evaluation returns an empty
        set.
       </p></li><li class="listitem"><p>
        For both <code class="literal">ON EMPTY</code> and <code class="literal">ON ERROR</code>,
        specifying <code class="literal">ERROR</code> will cause an error to be thrown with
        the appropriate message. Other options include returning an SQL NULL, an
        empty array (<code class="literal">EMPTY [<span class="optional">ARRAY</span>]</code>),
        an empty object (<code class="literal">EMPTY OBJECT</code>), or a user-specified
        expression (<code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em>)
        that can be coerced to jsonb or the type specified in <code class="literal">RETURNING</code>.
        The default when <code class="literal">ON EMPTY</code> or <code class="literal">ON ERROR</code>
        is not specified is to return an SQL NULL value.
       </p></li></ul></div>
<p>
        Examples:
       </p>
<p>
<code class="literal">JSON_QUERY(jsonb '[1,[2,3],null]', 'lax $[*][$off]' PASSING 1 AS off WITH CONDITIONAL WRAPPER)</code>
        → <code class="returnvalue">3</code>
</p>
<p>
<code class="literal">JSON_QUERY(jsonb '{"a": "[1, 2]"}', 'lax $.a' OMIT QUOTES)</code>
        → <code class="returnvalue">[1, 2]</code>
</p>
<p>
<code class="literal">JSON_QUERY(jsonb '{"a": "[1, 2]"}', 'lax $.a' RETURNING int[] OMIT QUOTES ERROR ON ERROR)</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
ERROR:  malformed array literal: "[1, 2]"
DETAIL:  Missing "]" after array dimensions.
</pre><p>
</p>
</td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.22.10.3.2.2.3.1.1.1"></a>
</p><pre class="synopsis">
<code class="function">JSON_VALUE</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>]
[<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON EMPTY</code> </span>]
[<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">text</code>
</pre><p class="func_signature">
</p>
<div class="itemizedlist"><ul class="itemizedlist" style="list-style-type: disc; "><li class="listitem"><p>
        Returns the result of applying the SQL/JSON
        <em class="replaceable"><code>path_expression</code></em> to the
        <em class="replaceable"><code>context_item</code></em>.
       </p></li><li class="listitem"><p>
        Only use <code class="function">JSON_VALUE()</code> if the extracted value is
        expected to be a single <acronym class="acronym">SQL/JSON</acronym> scalar item;
        getting multiple values will be treated as an error. If you expect that
        extracted value might be an object or an array, use the
        <code class="function">JSON_QUERY</code> function instead.
       </p></li><li class="listitem"><p>
        By default, the result, which must be a single scalar value, is
        returned as a value of type <code class="type">text</code>, though the
        <code class="literal">RETURNING</code> clause can be used to return as some
        other type to which it can be successfully coerced.
       </p></li><li class="listitem"><p>
        The <code class="literal">ON ERROR</code> and <code class="literal">ON EMPTY</code>
        clauses have similar semantics as mentioned in the description of
        <code class="function">JSON_QUERY</code>, except the set of values returned in
        lieu of throwing an error is different.
       </p></li><li class="listitem"><p>
        Note that scalar strings returned by <code class="function">JSON_VALUE</code>
        always have their quotes removed, equivalent to specifying
        <code class="literal">OMIT QUOTES</code> in <code class="function">JSON_QUERY</code>.
       </p></li></ul></div>
<p>
        Examples:
       </p>
<p>
<code class="literal">JSON_VALUE(jsonb '"123.45"', '$' RETURNING float)</code>
        → <code class="returnvalue">123.45</code>
</p>
<p>
<code class="literal">JSON_VALUE(jsonb '"03:04 2015-02-01"', '$.datetime("HH24:MI YYYY-MM-DD")' RETURNING date)</code>
        → <code class="returnvalue">2015-02-01</code>
</p>
<p>
<code class="literal">JSON_VALUE(jsonb '[1,2]', 'strict $[$off]' PASSING 1 as off)</code>
        → <code class="returnvalue">2</code>
</p>
<p>
<code class="literal">JSON_VALUE(jsonb '[1,2]', 'strict $[*]' DEFAULT 9 ON ERROR)</code>
        → <code class="returnvalue">9</code>
</p>
</td></tr></tbody></table>

<br>

### Note

The *`context_item`* expression is converted to
`jsonb` by an implicit cast if the expression is not already of
type `jsonb`. Note, however, that any parsing errors that occur
during that conversion are thrown unconditionally, that is, are not
handled according to the (specified or implicit) `ON ERROR`
clause.

### Note

`JSON_VALUE()` returns an SQL NULL if
*`path_expression`* returns a JSON
`null`, whereas `JSON_QUERY()` returns
the JSON `null` as is.

<a id="FUNCTIONS-SQLJSON-TABLE"></a>

### 9.16.4. JSON_TABLE [#](#FUNCTIONS-SQLJSON-TABLE)

<a id="id-1.5.8.22.11.2"></a>

`JSON_TABLE` is an SQL/JSON function which
queries JSON data
and presents the results as a relational view, which can be accessed as a
regular SQL table. You can use `JSON_TABLE` inside
the `FROM` clause of a `SELECT`,
`UPDATE`, or `DELETE` and as data source
in a `MERGE` statement.

Taking JSON data as input, `JSON_TABLE` uses a JSON path
expression to extract a part of the provided data to use as a
*row pattern* for the constructed view. Each SQL/JSON
value given by the row pattern serves as source for a separate row in the
constructed view.

To split the row pattern into columns, `JSON_TABLE`
provides the `COLUMNS` clause that defines the
schema of the created view. For each column, a separate JSON path expression
can be specified to be evaluated against the row pattern to get an SQL/JSON
value that will become the value for the specified column in a given output
row.

JSON data stored at a nested level of the row pattern can be extracted using
the `NESTED PATH` clause. Each
`NESTED PATH` clause can be used to generate one or more
columns using the data from a nested level of the row pattern. Those
columns can be specified using a `COLUMNS` clause that
looks similar to the top-level COLUMNS clause. Rows constructed from
NESTED COLUMNS are called *child rows* and are joined
against the row constructed from the columns specified in the parent
`COLUMNS` clause to get the row in the final view. Child
columns themselves may contain a `NESTED PATH`
specification thus allowing to extract data located at arbitrary nesting
levels. Columns produced by multiple `NESTED PATH`s at the
same level are considered to be *siblings* of each
other and their rows after joining with the parent row are combined using
UNION.

The rows produced by `JSON_TABLE` are laterally
joined to the row that generated them, so you do not have to explicitly join
the constructed view with the original table holding JSON
data.

The syntax is:

```

JSON_TABLE (
    context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...] ]
    COLUMNS ( json_table_column [, ...] )
    [ { ERROR | EMPTY [ARRAY]} ON ERROR ]
)


where json_table_column is:

  name FOR ORDINALITY
  | name type
        [ FORMAT JSON [ENCODING UTF8]]
        [ PATH path_expression ]
        [ { WITHOUT | WITH { CONDITIONAL | [UNCONDITIONAL] } } [ ARRAY ] WRAPPER ]
        [ { KEEP | OMIT } QUOTES [ ON SCALAR STRING ] ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON EMPTY ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON ERROR ]
  | name type EXISTS [ PATH path_expression ]
        [ { ERROR | TRUE | FALSE | UNKNOWN } ON ERROR ]
  | NESTED [ PATH ] path_expression [ AS json_path_name ] COLUMNS ( json_table_column [, ...] )
```

Each syntax element is described below in more detail.

`context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...]]`
:   The *`context_item`* specifies the input document
    to query, the *`path_expression`* is an SQL/JSON
    path expression defining the query, and *`json_path_name`*
    is an optional name for the *`path_expression`*.
    The optional `PASSING` clause provides data values for
    the variables mentioned in the *`path_expression`*.
    The result of the input data evaluation using the aforementioned elements
    is called the *row pattern*, which is used as the
    source for row values in the constructed view.

`COLUMNS` ( *`json_table_column`* [, ...] )
:   The `COLUMNS` clause defining the schema of the
    constructed view. In this clause, you can specify each column to be
    filled with an SQL/JSON value obtained by applying a JSON path expression
    against the row pattern. *`json_table_column`* has
    the following variants:

    *`name`* `FOR ORDINALITY`
    :   Adds an ordinality column that provides sequential row numbering starting
        from 1. Each `NESTED PATH` (see below) gets its own
        counter for any nested ordinality columns.

    `name type [FORMAT JSON [ENCODING UTF8]] [ PATH path_expression ]`
    :   Inserts an SQL/JSON value obtained by applying
        *`path_expression`* against the row pattern into
        the view's output row after coercing it to specified
        *`type`*.

        Specifying `FORMAT JSON` makes it explicit that you
        expect the value to be a valid `json` object. It only
        makes sense to specify `FORMAT JSON` if
        *`type`* is one of `bpchar`,
        `bytea`, `character varying`, `name`,
        `json`, `jsonb`, `text`, or a domain over
        these types.

        Optionally, you can specify `WRAPPER` and
        `QUOTES` clauses to format the output. Note that
        specifying `OMIT QUOTES` overrides
        `FORMAT JSON` if also specified, because unquoted
        literals do not constitute valid `json` values.

        Optionally, you can use `ON EMPTY` and
        `ON ERROR` clauses to specify whether to throw the error
        or return the specified value when the result of JSON path evaluation is
        empty and when an error occurs during JSON path evaluation or when
        coercing the SQL/JSON value to the specified type, respectively. The
        default for both is to return a `NULL` value.

        ### Note

        This clause is internally turned into and has the same semantics as
        `JSON_VALUE` or `JSON_QUERY`.
        The latter if the specified type is not a scalar type or if either of
        `FORMAT JSON`, `WRAPPER`, or
        `QUOTES` clause is present.

    *`name`* *`type`* `EXISTS` [ `PATH` *`path_expression`* ]
    :   Inserts a boolean value obtained by applying
        *`path_expression`* against the row pattern
        into the view's output row after coercing it to specified
        *`type`*.

        The value corresponds to whether applying the `PATH`
        expression to the row pattern yields any values.

        The specified *`type`* should have a cast from the
        `boolean` type.

        Optionally, you can use `ON ERROR` to specify whether to
        throw the error or return the specified value when an error occurs during
        JSON path evaluation or when coercing SQL/JSON value to the specified
        type. The default is to return a boolean value
        `FALSE`.

        ### Note

        This clause is internally turned into and has the same semantics as
        `JSON_EXISTS`.

    `NESTED [ PATH ]` *`path_expression`* [ `AS` *`json_path_name`* ] `COLUMNS` ( *`json_table_column`* [, ...] )
    :   Extracts SQL/JSON values from nested levels of the row pattern,
        generates one or more columns as defined by the `COLUMNS`
        subclause, and inserts the extracted SQL/JSON values into those
        columns. The *`json_table_column`*
        expression in the `COLUMNS` subclause uses the same
        syntax as in the parent `COLUMNS` clause.

        The `NESTED PATH` syntax is recursive,
        so you can go down multiple nested levels by specifying several
        `NESTED PATH` subclauses within each other.
        It allows to unnest the hierarchy of JSON objects and arrays
        in a single function invocation rather than chaining several
        `JSON_TABLE` expressions in an SQL statement.

    ### Note

    In each variant of *`json_table_column`* described
    above, if the `PATH` clause is omitted, path expression
    `$.name` is used, where
    *`name`* is the provided column name.

`AS` *`json_path_name`*
:   The optional *`json_path_name`* serves as an
    identifier of the provided *`path_expression`*.
    The name must be unique and distinct from the column names.

{ `ERROR` | `EMPTY` } `ON ERROR`
:   The optional `ON ERROR` can be used to specify how to
    handle errors when evaluating the top-level
    *`path_expression`*. Use `ERROR`
    if you want the errors to be thrown and `EMPTY` to
    return an empty table, that is, a table containing 0 rows. Note that
    this clause does not affect the errors that occur when evaluating
    columns, for which the behavior depends on whether the
    `ON ERROR` clause is specified against a given column.

Examples

In the examples that follow, the following table containing JSON data
will be used:

```

CREATE TABLE my_films ( js jsonb );

INSERT INTO my_films VALUES (
'{ "favorites" : [
   { "kind" : "comedy", "films" : [
     { "title" : "Bananas",
       "director" : "Woody Allen"},
     { "title" : "The Dinner Game",
       "director" : "Francis Veber" } ] },
   { "kind" : "horror", "films" : [
     { "title" : "Psycho",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "thriller", "films" : [
     { "title" : "Vertigo",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "drama", "films" : [
     { "title" : "Yojimbo",
       "director" : "Akira Kurosawa" } ] }
  ] }');
```

The following query shows how to use `JSON_TABLE` to
turn the JSON objects in the `my_films` table
to a view containing columns for the keys `kind`,
`title`, and `director` contained in
the original JSON along with an ordinality column:

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*]' COLUMNS (
   id FOR ORDINALITY,
   kind text PATH '$.kind',
   title text PATH '$.films[*].title' WITH WRAPPER,
   director text PATH '$.films[*].director' WITH WRAPPER)) AS jt;
```

```

 id |   kind   |             title              |             director
----+----------+--------------------------------+----------------------------------
  1 | comedy   | ["Bananas", "The Dinner Game"] | ["Woody Allen", "Francis Veber"]
  2 | horror   | ["Psycho"]                     | ["Alfred Hitchcock"]
  3 | thriller | ["Vertigo"]                    | ["Alfred Hitchcock"]
  4 | drama    | ["Yojimbo"]                    | ["Akira Kurosawa"]
(4 rows)
```

The following is a modified version of the above query to show the
usage of `PASSING` arguments in the filter specified in
the top-level JSON path expression and the various options for the
individual columns:

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
     COLUMNS (
     id FOR ORDINALITY,
     kind text PATH '$.kind',
     title text FORMAT JSON PATH '$.films[*].title' OMIT QUOTES,
     director text PATH '$.films[*].director' KEEP QUOTES)) AS jt;
```

```

 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

The following is a modified version of the above query to show the usage
of `NESTED PATH` for populating title and director
columns, illustrating how they are joined to the parent columns id and
kind:

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```

 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

The following is the same query but without the filter in the root
path:

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*]'
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```

 id |   kind   |      title      |      director
----+----------+-----------------+--------------------
  1 | comedy   | Bananas         | "Woody Allen"
  1 | comedy   | The Dinner Game | "Francis Veber"
  2 | horror   | Psycho          | "Alfred Hitchcock"
  3 | thriller | Vertigo         | "Alfred Hitchcock"
  4 | drama    | Yojimbo         | "Akira Kurosawa"
(5 rows)
```

The following shows another query using a different `JSON`
object as input. It shows the UNION "sibling join" between
`NESTED` paths `$.movies[*]` and
`$.books[*]` and also the usage of
`FOR ORDINALITY` column at `NESTED`
levels (columns `movie_id`, `book_id`,
and `author_id`):

```

SELECT * FROM JSON_TABLE (
'{"favorites":
    [{"movies":
      [{"name": "One", "director": "John Doe"},
       {"name": "Two", "director": "Don Joe"}],
     "books":
      [{"name": "Mystery", "authors": [{"name": "Brown Dan"}]},
       {"name": "Wonder", "authors": [{"name": "Jun Murakami"}, {"name":"Craig Doe"}]}]
}]}'::json, '$.favorites[*]'
COLUMNS (
  user_id FOR ORDINALITY,
  NESTED '$.movies[*]'
    COLUMNS (
    movie_id FOR ORDINALITY,
    mname text PATH '$.name',
    director text),
  NESTED '$.books[*]'
    COLUMNS (
      book_id FOR ORDINALITY,
      bname text PATH '$.name',
      NESTED '$.authors[*]'
        COLUMNS (
          author_id FOR ORDINALITY,
          author_name text PATH '$.name'))));
```

```

 user_id | movie_id | mname | director | book_id |  bname  | author_id | author_name
---------+----------+-------+----------+---------+---------+-----------+--------------
       1 |        1 | One   | John Doe |         |         |           |
       1 |        2 | Two   | Don Joe  |         |         |           |
       1 |          |       |          |       1 | Mystery |         1 | Brown Dan
       1 |          |       |          |       2 | Wonder  |         1 | Jun Murakami
       1 |          |       |          |       2 | Wonder  |         2 | Craig Doe
(5 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-json.html)（英文原文，待翻譯）
