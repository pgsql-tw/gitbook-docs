## 8.21. Pseudo-Types [#](#DATATYPE-PSEUDO)

<a id="id-1.5.7.29.2"></a><a id="id-1.5.7.29.3"></a><a id="id-1.5.7.29.4"></a><a id="id-1.5.7.29.5"></a><a id="id-1.5.7.29.6"></a><a id="id-1.5.7.29.7"></a><a id="id-1.5.7.29.8"></a><a id="id-1.5.7.29.9"></a><a id="id-1.5.7.29.10"></a><a id="id-1.5.7.29.11"></a><a id="id-1.5.7.29.12"></a><a id="id-1.5.7.29.13"></a><a id="id-1.5.7.29.14"></a><a id="id-1.5.7.29.15"></a><a id="id-1.5.7.29.16"></a><a id="id-1.5.7.29.17"></a><a id="id-1.5.7.29.18"></a><a id="id-1.5.7.29.19"></a><a id="id-1.5.7.29.20"></a><a id="id-1.5.7.29.21"></a><a id="id-1.5.7.29.22"></a><a id="id-1.5.7.29.23"></a><a id="id-1.5.7.29.24"></a><a id="id-1.5.7.29.25"></a><a id="id-1.5.7.29.26"></a>

The PostgreSQL type system contains a
number of special-purpose entries that are collectively called
*pseudo-types*. A pseudo-type cannot be used as a
column data type, but it can be used to declare a function's
argument or result type. Each of the available pseudo-types is
useful in situations where a function's behavior does not
correspond to simply taking or returning a value of a specific
SQL data type. [Table 8.27](datatype-pseudo.md#DATATYPE-PSEUDOTYPES-TABLE) lists the existing
pseudo-types.

<a id="DATATYPE-PSEUDOTYPES-TABLE"></a>

**Table 8.27. Pseudo-Types**

<table border="1" class="table" summary="Pseudo-Types"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Name</th><th>Description</th></tr></thead><tbody><tr><td><code class="type">any</code></td><td>Indicates that a function accepts any input data type.</td></tr><tr><td><code class="type">anyelement</code></td><td>Indicates that a function accepts any data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a>).</td></tr><tr><td><code class="type">anyarray</code></td><td>Indicates that a function accepts any array data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a>).</td></tr><tr><td><code class="type">anynonarray</code></td><td>Indicates that a function accepts any non-array data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a>).</td></tr><tr><td><code class="type">anyenum</code></td><td>Indicates that a function accepts any enum data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a> and
        <a class="xref" href="datatype-enum.md">Section 8.7</a>).</td></tr><tr><td><code class="type">anyrange</code></td><td>Indicates that a function accepts any range data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a> and
        <a class="xref" href="rangetypes.md">Section 8.17</a>).</td></tr><tr><td><code class="type">anymultirange</code></td><td>Indicates that a function accepts any multirange data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a> and
        <a class="xref" href="rangetypes.md">Section 8.17</a>).</td></tr><tr><td><code class="type">anycompatible</code></td><td>Indicates that a function accepts any data type,
        with automatic promotion of multiple arguments to a common data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a>).</td></tr><tr><td><code class="type">anycompatiblearray</code></td><td>Indicates that a function accepts any array data type,
        with automatic promotion of multiple arguments to a common data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a>).</td></tr><tr><td><code class="type">anycompatiblenonarray</code></td><td>Indicates that a function accepts any non-array data type,
        with automatic promotion of multiple arguments to a common data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a>).</td></tr><tr><td><code class="type">anycompatiblerange</code></td><td>Indicates that a function accepts any range data type,
        with automatic promotion of multiple arguments to a common data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a> and
        <a class="xref" href="rangetypes.md">Section 8.17</a>).</td></tr><tr><td><code class="type">anycompatiblemultirange</code></td><td>Indicates that a function accepts any multirange data type,
        with automatic promotion of multiple arguments to a common data type
        (see <a class="xref" href="../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC">Section 36.2.5</a> and
        <a class="xref" href="rangetypes.md">Section 8.17</a>).</td></tr><tr><td><code class="type">cstring</code></td><td>Indicates that a function accepts or returns a null-terminated C string.</td></tr><tr><td><code class="type">internal</code></td><td>Indicates that a function accepts or returns a server-internal
        data type.</td></tr><tr><td><code class="type">language_handler</code></td><td>A procedural language call handler is declared to return <code class="type">language_handler</code>.</td></tr><tr><td><code class="type">fdw_handler</code></td><td>A foreign-data wrapper handler is declared to return <code class="type">fdw_handler</code>.</td></tr><tr><td><code class="type">table_am_handler</code></td><td>A table access method handler is declared to return <code class="type">table_am_handler</code>.</td></tr><tr><td><code class="type">index_am_handler</code></td><td>An index access method handler is declared to return <code class="type">index_am_handler</code>.</td></tr><tr><td><code class="type">tsm_handler</code></td><td>A tablesample method handler is declared to return <code class="type">tsm_handler</code>.</td></tr><tr><td><code class="type">record</code></td><td>Identifies a function taking or returning an unspecified row type.</td></tr><tr><td><code class="type">trigger</code></td><td>A trigger function is declared to return <code class="type">trigger.</code></td></tr><tr><td><code class="type">event_trigger</code></td><td>An event trigger function is declared to return <code class="type">event_trigger.</code></td></tr><tr><td><code class="type">pg_ddl_command</code></td><td>Identifies a representation of DDL commands that is available to event triggers.</td></tr><tr><td><code class="type">void</code></td><td>Indicates that a function returns no value.</td></tr><tr><td><code class="type">unknown</code></td><td>Identifies a not-yet-resolved type, e.g., of an undecorated
         string literal.</td></tr></tbody></table>

<br>

Functions coded in C (whether built-in or dynamically loaded) can be
declared to accept or return any of these pseudo-types. It is up to
the function author to ensure that the function will behave safely
when a pseudo-type is used as an argument type.

Functions coded in procedural languages can use pseudo-types only as
allowed by their implementation languages. At present most procedural
languages forbid use of a pseudo-type as an argument type, and allow
only `void` and `record` as a result type (plus
`trigger` or `event_trigger` when the function is used
as a trigger or event trigger). Some also support polymorphic functions
using the polymorphic pseudo-types, which are shown above and discussed
in detail in [Section 36.2.5](../../server-programming/extend/extend-type-system.md#EXTEND-TYPES-POLYMORPHIC).

The `internal` pseudo-type is used to declare functions
that are meant only to be called internally by the database
system, and not by direct invocation in an SQL
query. If a function has at least one `internal`-type
argument then it cannot be called from SQL. To
preserve the type safety of this restriction it is important to
follow this coding rule: do not create any function that is
declared to return `internal` unless it has at least one
`internal` argument.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-pseudo.html)（英文原文，待翻譯）
