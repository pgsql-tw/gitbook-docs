## 52.39. `pg_proc` [#](#CATALOG-PG-PROC)

<a id="id-1.10.4.41.2"></a>

The catalog `pg_proc` stores information about
functions, procedures, aggregate functions, and window functions
(collectively also known as routines). See [CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md), [CREATE PROCEDURE](../../reference/sql-commands/sql-createprocedure.md), and
[Section 36.3](../../server-programming/extend/xfunc.md) for more information.

If `prokind` indicates that the entry is for an
aggregate function, there should be a matching row in
[`pg_aggregate`](catalog-pg-aggregate.md).

<a id="id-1.10.4.41.5"></a>

**Table 52.39. `pg_proc` Columns**

<table border="1" class="table" summary="pg_proc Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">proname</code> <code class="type">name</code>
</p>
<p>
       Name of the function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pronamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the namespace that contains this function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proowner</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Owner of the function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prolang</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-language.md"><code class="structname">pg_language</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Implementation language or call interface of this function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">procost</code> <code class="type">float4</code>
</p>
<p>
       Estimated execution cost (in units of
       <a class="xref" href="../../server-administration/runtime-config/runtime-config-query.md#GUC-CPU-OPERATOR-COST">cpu_operator_cost</a>); if <code class="structfield">proretset</code>,
       this is cost per row returned
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prorows</code> <code class="type">float4</code>
</p>
<p>
       Estimated number of result rows (zero if not <code class="structfield">proretset</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">provariadic</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Data type of the variadic array parameter's elements,
       or zero if the function does not have a variadic parameter
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosupport</code> <code class="type">regproc</code>
       (references <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Planner support function for this function
       (see <a class="xref" href="../../server-programming/extend/xfunc-optimization.md">Section 36.11</a>), or zero if none
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prokind</code> <code class="type">char</code>
</p>
<p>
<code class="literal">f</code> for a normal function, <code class="literal">p</code>
       for a procedure, <code class="literal">a</code> for an aggregate function, or
       <code class="literal">w</code> for a window function
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosecdef</code> <code class="type">bool</code>
</p>
<p>
       Function is a security definer (i.e., a <span class="quote">“<span class="quote">setuid</span>”</span>
       function)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proleakproof</code> <code class="type">bool</code>
</p>
<p>
       The function has no side effects.  No information about the
       arguments is conveyed except via the return value.  Any function
       that might throw an error depending on the values of its arguments
       is not leakproof.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proisstrict</code> <code class="type">bool</code>
</p>
<p>
       Function returns null if any call argument is null.  In that
       case the function won't actually be called at all.  Functions
       that are not <span class="quote">“<span class="quote">strict</span>”</span> must be prepared to handle
       null inputs.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proretset</code> <code class="type">bool</code>
</p>
<p>
       Function returns a set (i.e., multiple values of the specified
       data type)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">provolatile</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">provolatile</code> tells whether the function's
       result depends only on its input arguments, or is affected by outside
       factors.
       It is <code class="literal">i</code> for <span class="quote">“<span class="quote">immutable</span>”</span> functions,
       which always deliver the same result for the same inputs.
       It is <code class="literal">s</code> for <span class="quote">“<span class="quote">stable</span>”</span> functions,
       whose results (for fixed inputs) do not change within a scan.
       It is <code class="literal">v</code> for <span class="quote">“<span class="quote">volatile</span>”</span> functions,
       whose results might change at any time.  (Use <code class="literal">v</code> also
       for functions with side-effects, so that calls to them cannot get
       optimized away.)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proparallel</code> <code class="type">char</code>
</p>
<p>
<code class="structfield">proparallel</code> tells whether the function
       can be safely run in parallel mode.
       It is <code class="literal">s</code> for functions which are safe to run in
       parallel mode without restriction.
       It is <code class="literal">r</code> for functions which can be run in parallel
       mode, but their execution is restricted to the parallel group leader;
       parallel worker processes cannot invoke these functions.
       It is <code class="literal">u</code> for functions which are unsafe in parallel
       mode; the presence of such a function forces a serial execution plan.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pronargs</code> <code class="type">int2</code>
</p>
<p>
       Number of input arguments
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pronargdefaults</code> <code class="type">int2</code>
</p>
<p>
       Number of arguments that have defaults
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prorettype</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       Data type of the return value
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargtypes</code> <code class="type">oidvector</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       An array of the data types of the function arguments.  This includes
       only input arguments (including <code class="literal">INOUT</code> and
       <code class="literal">VARIADIC</code> arguments), and thus represents
       the call signature of the function.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proallargtypes</code> <code class="type">oid[]</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       An array of the data types of the function arguments.  This includes
       all arguments (including <code class="literal">OUT</code> and
       <code class="literal">INOUT</code> arguments); however, if all the
       arguments are <code class="literal">IN</code> arguments, this field will be null.
       Note that subscripting is 1-based, whereas for historical reasons
       <code class="structfield">proargtypes</code> is subscripted from 0.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargmodes</code> <code class="type">char[]</code>
</p>
<p>
       An array of the modes of the function arguments, encoded as
       <code class="literal">i</code> for <code class="literal">IN</code> arguments,
       <code class="literal">o</code> for <code class="literal">OUT</code> arguments,
       <code class="literal">b</code> for <code class="literal">INOUT</code> arguments,
       <code class="literal">v</code> for <code class="literal">VARIADIC</code> arguments,
       <code class="literal">t</code> for <code class="literal">TABLE</code> arguments.
       If all the arguments are <code class="literal">IN</code> arguments,
       this field will be null.
       Note that subscripts correspond to positions of
       <code class="structfield">proallargtypes</code> not <code class="structfield">proargtypes</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargnames</code> <code class="type">text[]</code>
</p>
<p>
       An array of the names of the function arguments.
       Arguments without a name are set to empty strings in the array.
       If none of the arguments have a name, this field will be null.
       Note that subscripts correspond to positions of
       <code class="structfield">proallargtypes</code> not <code class="structfield">proargtypes</code>.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proargdefaults</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Expression trees (in <code class="function">nodeToString()</code> representation)
       for default values.  This is a list with
       <code class="structfield">pronargdefaults</code> elements, corresponding to the last
       <em class="replaceable"><code>N</code></em> <span class="emphasis"><em>input</em></span> arguments (i.e., the last
       <em class="replaceable"><code>N</code></em> <code class="structfield">proargtypes</code> positions).
       If none of the arguments have defaults, this field will be null.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">protrftypes</code> <code class="type">oid[]</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       An array of the argument/result data type(s) for which to apply
       transforms (from the function's <code class="literal">TRANSFORM</code>
       clause).  Null if none.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosrc</code> <code class="type">text</code>
</p>
<p>
       This tells the function handler how to invoke the function.  It
       might be the actual source code of the function for interpreted
       languages, a link symbol, a file name, or just about anything
       else, depending on the implementation language/call convention.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">probin</code> <code class="type">text</code>
</p>
<p>
       Additional information about how to invoke the function.
       Again, the interpretation is language-specific.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">prosqlbody</code> <code class="type">pg_node_tree</code>
</p>
<p>
       Pre-parsed SQL function body.  This is used for SQL-language
       functions when the body is given in SQL-standard notation
       rather than as a string literal.  It's null in other cases.
       </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proconfig</code> <code class="type">text[]</code>
</p>
<p>
       Function's local settings for run-time configuration variables
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">proacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       Access privileges; see <a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">Section 5.8</a> for details
      </p></td></tr></tbody></table>

<br>

For compiled functions, both built-in and dynamically loaded,
`prosrc` contains the function's C-language
name (link symbol).
For SQL-language functions, `prosrc` contains
the function's source text if that is specified as a string literal;
but if the function body is specified in SQL-standard style,
`prosrc` is unused (typically it's an empty
string) and `prosqlbody` contains the
pre-parsed definition.
For all other currently-known language types,
`prosrc` contains the function's source
text. `probin` is null except for
dynamically-loaded C functions, for which it gives the name of the
shared library file containing the function.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-proc.html)（英文原文，待翻譯）
