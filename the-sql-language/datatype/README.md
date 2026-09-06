## Chapter 8. Data Types

**Table of Contents**

[8.1. Numeric Types](datatype-numeric.md)
:   [8.1.1. Integer Types](datatype-numeric.md#DATATYPE-INT)

    [8.1.2. Arbitrary Precision Numbers](datatype-numeric.md#DATATYPE-NUMERIC-DECIMAL)

    [8.1.3. Floating-Point Types](datatype-numeric.md#DATATYPE-FLOAT)

    [8.1.4. Serial Types](datatype-numeric.md#DATATYPE-SERIAL)

[8.2. Monetary Types](datatype-money.md)

[8.3. Character Types](datatype-character.md)

[8.4. Binary Data Types](datatype-binary.md)
:   [8.4.1. `bytea` Hex Format](datatype-binary.md#DATATYPE-BINARY-BYTEA-HEX-FORMAT)

    [8.4.2. `bytea` Escape Format](datatype-binary.md#DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT)

[8.5. Date/Time Types](datatype-datetime.md)
:   [8.5.1. Date/Time Input](datatype-datetime.md#DATATYPE-DATETIME-INPUT)

    [8.5.2. Date/Time Output](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT)

    [8.5.3. Time Zones](datatype-datetime.md#DATATYPE-TIMEZONES)

    [8.5.4. Interval Input](datatype-datetime.md#DATATYPE-INTERVAL-INPUT)

    [8.5.5. Interval Output](datatype-datetime.md#DATATYPE-INTERVAL-OUTPUT)

[8.6. Boolean Type](datatype-boolean.md)

[8.7. Enumerated Types](datatype-enum.md)
:   [8.7.1. Declaration of Enumerated Types](datatype-enum.md#DATATYPE-ENUM-DECLARATION)

    [8.7.2. Ordering](datatype-enum.md#DATATYPE-ENUM-ORDERING)

    [8.7.3. Type Safety](datatype-enum.md#DATATYPE-ENUM-TYPE-SAFETY)

    [8.7.4. Implementation Details](datatype-enum.md#DATATYPE-ENUM-IMPLEMENTATION-DETAILS)

[8.8. Geometric Types](datatype-geometric.md)
:   [8.8.1. Points](datatype-geometric.md#DATATYPE-GEOMETRIC-POINTS)

    [8.8.2. Lines](datatype-geometric.md#DATATYPE-LINE)

    [8.8.3. Line Segments](datatype-geometric.md#DATATYPE-LSEG)

    [8.8.4. Boxes](datatype-geometric.md#DATATYPE-GEOMETRIC-BOXES)

    [8.8.5. Paths](datatype-geometric.md#DATATYPE-GEOMETRIC-PATHS)

    [8.8.6. Polygons](datatype-geometric.md#DATATYPE-POLYGON)

    [8.8.7. Circles](datatype-geometric.md#DATATYPE-CIRCLE)

[8.9. Network Address Types](datatype-net-types.md)
:   [8.9.1. `inet`](datatype-net-types.md#DATATYPE-INET)

    [8.9.2. `cidr`](datatype-net-types.md#DATATYPE-CIDR)

    [8.9.3. `inet` vs. `cidr`](datatype-net-types.md#DATATYPE-INET-VS-CIDR)

    [8.9.4. `macaddr`](datatype-net-types.md#DATATYPE-MACADDR)

    [8.9.5. `macaddr8`](datatype-net-types.md#DATATYPE-MACADDR8)

[8.10. Bit String Types](datatype-bit.md)

[8.11. Text Search Types](datatype-textsearch.md)
:   [8.11.1. `tsvector`](datatype-textsearch.md#DATATYPE-TSVECTOR)

    [8.11.2. `tsquery`](datatype-textsearch.md#DATATYPE-TSQUERY)

[8.12. UUID Type](datatype-uuid.md)

[8.13. XML Type](datatype-xml.md)
:   [8.13.1. Creating XML Values](datatype-xml.md#DATATYPE-XML-CREATING)

    [8.13.2. Encoding Handling](datatype-xml.md#DATATYPE-XML-ENCODING-HANDLING)

    [8.13.3. Accessing XML Values](datatype-xml.md#DATATYPE-XML-ACCESSING-XML-VALUES)

[8.14. JSON Types](datatype-json.md)
:   [8.14.1. JSON Input and Output Syntax](datatype-json.md#JSON-KEYS-ELEMENTS)

    [8.14.2. Designing JSON Documents](datatype-json.md#JSON-DOC-DESIGN)

    [8.14.3. `jsonb` Containment and Existence](datatype-json.md#JSON-CONTAINMENT)

    [8.14.4. `jsonb` Indexing](datatype-json.md#JSON-INDEXING)

    [8.14.5. `jsonb` Subscripting](datatype-json.md#JSONB-SUBSCRIPTING)

    [8.14.6. Transforms](datatype-json.md#DATATYPE-JSON-TRANSFORMS)

    [8.14.7. jsonpath Type](datatype-json.md#DATATYPE-JSONPATH)

[8.15. Arrays](arrays.md)
:   [8.15.1. Declaration of Array Types](arrays.md#ARRAYS-DECLARATION)

    [8.15.2. Array Value Input](arrays.md#ARRAYS-INPUT)

    [8.15.3. Accessing Arrays](arrays.md#ARRAYS-ACCESSING)

    [8.15.4. Modifying Arrays](arrays.md#ARRAYS-MODIFYING)

    [8.15.5. Searching in Arrays](arrays.md#ARRAYS-SEARCHING)

    [8.15.6. Array Input and Output Syntax](arrays.md#ARRAYS-IO)

[8.16. Composite Types](rowtypes.md)
:   [8.16.1. Declaration of Composite Types](rowtypes.md#ROWTYPES-DECLARING)

    [8.16.2. Constructing Composite Values](rowtypes.md#ROWTYPES-CONSTRUCTING)

    [8.16.3. Accessing Composite Types](rowtypes.md#ROWTYPES-ACCESSING)

    [8.16.4. Modifying Composite Types](rowtypes.md#ROWTYPES-MODIFYING)

    [8.16.5. Using Composite Types in Queries](rowtypes.md#ROWTYPES-USAGE)

    [8.16.6. Composite Type Input and Output Syntax](rowtypes.md#ROWTYPES-IO-SYNTAX)

[8.17. Range Types](rangetypes.md)
:   [8.17.1. Built-in Range and Multirange Types](rangetypes.md#RANGETYPES-BUILTIN)

    [8.17.2. Examples](rangetypes.md#RANGETYPES-EXAMPLES)

    [8.17.3. Inclusive and Exclusive Bounds](rangetypes.md#RANGETYPES-INCLUSIVITY)

    [8.17.4. Infinite (Unbounded) Ranges](rangetypes.md#RANGETYPES-INFINITE)

    [8.17.5. Range Input/Output](rangetypes.md#RANGETYPES-IO)

    [8.17.6. Constructing Ranges and Multiranges](rangetypes.md#RANGETYPES-CONSTRUCT)

    [8.17.7. Discrete Range Types](rangetypes.md#RANGETYPES-DISCRETE)

    [8.17.8. Defining New Range Types](rangetypes.md#RANGETYPES-DEFINING)

    [8.17.9. Indexing](rangetypes.md#RANGETYPES-INDEXING)

    [8.17.10. Constraints on Ranges](rangetypes.md#RANGETYPES-CONSTRAINT)

[8.18. Domain Types](domains.md)

[8.19. Object Identifier Types](datatype-oid.md)

[8.20. `pg_lsn` Type](datatype-pg-lsn.md)

[8.21. Pseudo-Types](datatype-pseudo.md)

<a id="id-1.5.7.2"></a><a id="id-1.5.7.3"></a>

PostgreSQL has a rich set of native data
types available to users. Users can add new types to
PostgreSQL using the [CREATE TYPE](../../reference/sql-commands/sql-createtype.md) command.

[Table 8.1](README.md#DATATYPE-TABLE) shows all the built-in general-purpose data
types. Most of the alternative names listed in the
“Aliases” column are the names used internally by
PostgreSQL for historical reasons. In
addition, some internally used or deprecated types are available,
but are not listed here.

<a id="DATATYPE-TABLE"></a>

**Table 8.1. Data Types**

<table border="1" class="table" summary="Data Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>Name</th><th>Aliases</th><th>Description</th></tr></thead><tbody><tr><td><code class="type">bigint</code></td><td><code class="type">int8</code></td><td>signed eight-byte integer</td></tr><tr><td><code class="type">bigserial</code></td><td><code class="type">serial8</code></td><td>autoincrementing eight-byte integer</td></tr><tr><td><code class="type">bit [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td> </td><td>fixed-length bit string</td></tr><tr><td><code class="type">bit varying [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td><code class="type">varbit [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td>variable-length bit string</td></tr><tr><td><code class="type">boolean</code></td><td><code class="type">bool</code></td><td>logical Boolean (true/false)</td></tr><tr><td><code class="type">box</code></td><td> </td><td>rectangular box on a plane</td></tr><tr><td><code class="type">bytea</code></td><td> </td><td>binary data (<span class="quote">“<span class="quote">byte array</span>”</span>)</td></tr><tr><td><code class="type">character [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td><code class="type">char [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td>fixed-length character string</td></tr><tr><td><code class="type">character varying [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td><code class="type">varchar [ (<em class="replaceable"><code>n</code></em>) ]</code></td><td>variable-length character string</td></tr><tr><td><code class="type">cidr</code></td><td> </td><td>IPv4 or IPv6 network address</td></tr><tr><td><code class="type">circle</code></td><td> </td><td>circle on a plane</td></tr><tr><td><code class="type">date</code></td><td> </td><td>calendar date (year, month, day)</td></tr><tr><td><code class="type">double precision</code></td><td><code class="type">float</code>, <code class="type">float8</code></td><td>double precision floating-point number (8 bytes)</td></tr><tr><td><code class="type">inet</code></td><td> </td><td>IPv4 or IPv6 host address</td></tr><tr><td><code class="type">integer</code></td><td><code class="type">int</code>, <code class="type">int4</code></td><td>signed four-byte integer</td></tr><tr><td><code class="type">interval [ <em class="replaceable"><code>fields</code></em> ] [ (<em class="replaceable"><code>p</code></em>) ]</code></td><td> </td><td>time span</td></tr><tr><td><code class="type">json</code></td><td> </td><td>textual JSON data</td></tr><tr><td><code class="type">jsonb</code></td><td> </td><td>binary JSON data, decomposed</td></tr><tr><td><code class="type">line</code></td><td> </td><td>infinite line on a plane</td></tr><tr><td><code class="type">lseg</code></td><td> </td><td>line segment on a plane</td></tr><tr><td><code class="type">macaddr</code></td><td> </td><td>MAC (Media Access Control) address</td></tr><tr><td><code class="type">macaddr8</code></td><td> </td><td>MAC (Media Access Control) address (EUI-64 format)</td></tr><tr><td><code class="type">money</code></td><td> </td><td>currency amount</td></tr><tr><td><code class="type">numeric [ (<em class="replaceable"><code>p</code></em>,
         <em class="replaceable"><code>s</code></em>) ]</code></td><td><code class="type">decimal [ (<em class="replaceable"><code>p</code></em>,
         <em class="replaceable"><code>s</code></em>) ]</code></td><td>exact numeric of selectable precision</td></tr><tr><td><code class="type">path</code></td><td> </td><td>geometric path on a plane</td></tr><tr><td><code class="type">pg_lsn</code></td><td> </td><td><span class="productname">PostgreSQL</span> Log Sequence Number</td></tr><tr><td><code class="type">pg_snapshot</code></td><td> </td><td>user-level transaction ID snapshot</td></tr><tr><td><code class="type">point</code></td><td> </td><td>geometric point on a plane</td></tr><tr><td><code class="type">polygon</code></td><td> </td><td>closed geometric path on a plane</td></tr><tr><td><code class="type">real</code></td><td><code class="type">float4</code></td><td>single precision floating-point number (4 bytes)</td></tr><tr><td><code class="type">smallint</code></td><td><code class="type">int2</code></td><td>signed two-byte integer</td></tr><tr><td><code class="type">smallserial</code></td><td><code class="type">serial2</code></td><td>autoincrementing two-byte integer</td></tr><tr><td><code class="type">serial</code></td><td><code class="type">serial4</code></td><td>autoincrementing four-byte integer</td></tr><tr><td><code class="type">text</code></td><td> </td><td>variable-length character string</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td> </td><td>time of day (no time zone)</td></tr><tr><td><code class="type">time [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td><code class="type">timetz</code></td><td>time of day, including time zone</td></tr><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] [ without time zone ]</code></td><td> </td><td>date and time (no time zone)</td></tr><tr><td><code class="type">timestamp [ (<em class="replaceable"><code>p</code></em>) ] with time zone</code></td><td><code class="type">timestamptz</code></td><td>date and time, including time zone</td></tr><tr><td><code class="type">tsquery</code></td><td> </td><td>text search query</td></tr><tr><td><code class="type">tsvector</code></td><td> </td><td>text search document</td></tr><tr><td><code class="type">txid_snapshot</code></td><td> </td><td>user-level transaction ID snapshot (deprecated; see <code class="type">pg_snapshot</code>)</td></tr><tr><td><code class="type">uuid</code></td><td> </td><td>universally unique identifier</td></tr><tr><td><code class="type">xml</code></td><td> </td><td>XML data</td></tr></tbody></table>

<br>

### Compatibility

The following types (or spellings thereof) are specified by
SQL: `bigint`, `bit`, `bit
varying`, `boolean`, `char`,
`character varying`, `character`,
`varchar`, `date`, `double
precision`, `integer`, `interval`,
`numeric`, `decimal`, `real`,
`smallint`, `time` (with or without time zone),
`timestamp` (with or without time zone),
`xml`.

Each data type has an external representation determined by its input
and output functions. Many of the built-in types have
obvious external formats. However, several types are either unique
to PostgreSQL, such as geometric
paths, or have several possible formats, such as the date
and time types.
Some of the input and output functions are not invertible, i.e.,
the result of an output function might lose accuracy when compared to
the original input.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype.html)（英文原文，待翻譯）
