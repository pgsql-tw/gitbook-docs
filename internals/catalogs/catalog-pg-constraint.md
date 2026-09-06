## 52.13. `pg_constraint` [#](#CATALOG-PG-CONSTRAINT)

<a id="id-1.10.4.15.2"></a>

The catalog `pg_constraint` stores check, not-null,
primary key, unique, foreign key, and exclusion constraints on tables.
(Column constraints are not treated specially. Every column constraint is
equivalent to some table constraint.)

User-defined constraint triggers (created with [`CREATE CONSTRAINT TRIGGER`](../../reference/sql-commands/sql-createtrigger.md)) also give rise to an entry in this table.

Check constraints on domains are stored here, too.

<a id="id-1.10.4.15.6"></a>

**Table 52.13. `pg_constraint` Columns**

<table border="1" class="table" summary="pg_constraint Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">conname</code> <code class="type">name</code>
</p>
<p>
       Constraint name (not necessarily unique!)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">connamespace</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The OID of the namespace that contains this constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">contype</code> <code class="type">char</code>
</p>
<p>
<code class="literal">c</code> = check constraint,
       <code class="literal">f</code> = foreign key constraint,
       <code class="literal">n</code> = not-null constraint,
       <code class="literal">p</code> = primary key constraint,
       <code class="literal">u</code> = unique constraint,
       <code class="literal">t</code> = constraint trigger,
       <code class="literal">x</code> = exclusion constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">condeferrable</code> <code class="type">bool</code>
</p>
<p>
       Is the constraint deferrable?
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">condeferred</code> <code class="type">bool</code>
</p>
<p>
       Is the constraint deferred by default?
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conenforced</code> <code class="type">bool</code>
</p>
<p>
       Is the constraint enforced?
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">convalidated</code> <code class="type">bool</code>
</p>
<p>
       Has the constraint been validated?
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The table this constraint is on; zero if not a table constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">contypid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The domain this constraint is on; zero if not a domain constraint
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conindid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The index supporting this constraint, if it's a unique, primary
       key, foreign key, or exclusion constraint; else zero
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conparentid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       The corresponding constraint of the parent partitioned table,
       if this is a constraint on a partition; else zero
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confrelid</code> <code class="type">oid</code>
       (references <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       If a foreign key, the referenced table; else zero
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confupdtype</code> <code class="type">char</code>
</p>
<p>
       Foreign key update action code:
       <code class="literal">a</code> = no action,
       <code class="literal">r</code> = restrict,
       <code class="literal">c</code> = cascade,
       <code class="literal">n</code> = set null,
       <code class="literal">d</code> = set default
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confdeltype</code> <code class="type">char</code>
</p>
<p>
       Foreign key deletion action code:
       <code class="literal">a</code> = no action,
       <code class="literal">r</code> = restrict,
       <code class="literal">c</code> = cascade,
       <code class="literal">n</code> = set null,
       <code class="literal">d</code> = set default
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confmatchtype</code> <code class="type">char</code>
</p>
<p>
       Foreign key match type:
       <code class="literal">f</code> = full,
       <code class="literal">p</code> = partial,
       <code class="literal">s</code> = simple
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conislocal</code> <code class="type">bool</code>
</p>
<p>
       This constraint is defined locally for the relation.  Note that a
       constraint can be locally defined and inherited simultaneously.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">coninhcount</code> <code class="type">int2</code>
</p>
<p>
       The number of direct inheritance ancestors this constraint has.
       A constraint with
       a nonzero number of ancestors cannot be dropped nor renamed.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">connoinherit</code> <code class="type">bool</code>
</p>
<p>
       This constraint is defined locally for the relation.  It is a
       non-inheritable constraint.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conperiod</code> <code class="type">bool</code>
</p>
<p>
       This constraint is defined with <code class="literal">WITHOUT OVERLAPS</code>
       (for primary keys and unique constraints) or <code class="literal">PERIOD</code>
       (for foreign keys).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conkey</code> <code class="type">int2[]</code>
       (references <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)
      </p>
<p>
       If a table constraint (including foreign keys, but not constraint
       triggers), list of the constrained columns
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confkey</code> <code class="type">int2[]</code>
       (references <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)
      </p>
<p>
       If a foreign key, list of the referenced columns
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conpfeqop</code> <code class="type">oid[]</code>
       (references <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       If a foreign key, list of the equality operators for PK = FK comparisons
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conppeqop</code> <code class="type">oid[]</code>
       (references <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       If a foreign key, list of the equality operators for PK = PK comparisons
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conffeqop</code> <code class="type">oid[]</code>
       (references <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       If a foreign key, list of the equality operators for FK = FK comparisons
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confdelsetcols</code> <code class="type">int2[]</code>
       (references <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>)
      </p>
<p>
       If a foreign key with a <code class="literal">SET NULL</code> or <code class="literal">SET
       DEFAULT</code> delete action, the columns that will be updated.
       If null, all of the referencing columns will be updated.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conexclop</code> <code class="type">oid[]</code>
       (references <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>)
      </p>
<p>
       If an exclusion constraint or <code class="literal">WITHOUT OVERLAPS</code>
       primary key/unique constraint, list of the per-column exclusion operators.
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conbin</code> <code class="type">pg_node_tree</code>
</p>
<p>
       If a check constraint, an internal representation of the
       expression.  (It's recommended to use
       <code class="function">pg_get_constraintdef()</code> to extract the definition of
       a check constraint.)
      </p></td></tr></tbody></table>

<br>

In the case of an exclusion constraint, `conkey`
is only useful for constraint elements that are simple column references.
For other cases, a zero appears in `conkey`
and the associated index must be consulted to discover the expression
that is constrained. (`conkey` thus has the
same contents as [`pg_index`](catalog-pg-index.md).`indkey` for the
index.)

### Note

`pg_class.relchecks` needs to agree with the
number of check-constraint entries found in this table for each
relation.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-constraint.html)（英文原文，待翻譯）
