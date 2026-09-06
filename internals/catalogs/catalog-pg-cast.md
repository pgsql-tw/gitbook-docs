## 52.10. `pg_cast` [#](#CATALOG-PG-CAST)

<a id="id-1.10.4.12.2"></a>

The catalog `pg_cast` stores data type conversion
paths, both built-in and user-defined.

It should be noted that `pg_cast` does not represent
every type conversion that the system knows how to perform; only those that
cannot be deduced from some generic rule. For example, casting between a
domain and its base type is not explicitly represented in
`pg_cast`. Another important exception is that
“automatic I/O conversion casts”, those performed using a data
type's own I/O functions to convert to or from `text` or other
string types, are not explicitly represented in
`pg_cast`.

<a id="id-1.10.4.12.5"></a>

**Table 52.10. `pg_cast` Columns**

<table border="1" class="table" summary="pg_cast Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       Row identifier
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castsource</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the source data type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">casttarget</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       OID of the target data type
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castfunc</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the function to use to perform this cast.  Zero is
       stored if the cast method doesn't require a function.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castcontext</code> <code class="type">char</code>
</p>
<p>
       Indicates what contexts the cast can be invoked in.
       <code class="literal">e</code> means only as an explicit cast (using
       <code class="literal">CAST</code> or <code class="literal">::</code> syntax).
       <code class="literal">a</code> means implicitly in assignment
       to a target column, as well as explicitly.
       <code class="literal">i</code> means implicitly in expressions, as well as the
       other cases.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castmethod</code> <code class="type">char</code>
</p>
<p>
       Indicates how the cast is performed.
       <code class="literal">f</code> means that the function specified in the <code class="structfield">castfunc</code> field is used.
       <code class="literal">i</code> means that the input/output functions are used.
       <code class="literal">b</code> means that the types are binary-coercible, thus no conversion is required.
      </p></td></tr></tbody></table>

<br>

The cast functions listed in `pg_cast` must
always take the cast source type as their first argument type, and
return the cast destination type as their result type. A cast
function can have up to three arguments. The second argument,
if present, must be type `integer`; it receives the type
modifier associated with the destination type, or -1
if there is none. The third argument,
if present, must be type `boolean`; it receives `true`
if the cast is an explicit cast, `false` otherwise.

It is legitimate to create a `pg_cast` entry
in which the source and target types are the same, if the associated
function takes more than one argument. Such entries represent
“length coercion functions” that coerce values of the type
to be legal for a particular type modifier value.

When a `pg_cast` entry has different source and
target types and a function that takes more than one argument, it
represents converting from one type to another and applying a length
coercion in a single step. When no such entry is available, coercion
to a type that uses a type modifier involves two steps, one to
convert between data types and a second to apply the modifier.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-cast.html)（英文原文，待翻譯）
