# 51.13. pg\_constraint

The catalog `pg_constraint` stores check, primary key, unique, foreign key, and exclusion constraints on tables. \(Column constraints are not treated specially. Every column constraint is equivalent to some table constraint.\) Not-null constraints are represented in the `pg_attribute` catalog, not here.

User-defined constraint triggers \(created with `CREATE CONSTRAINT TRIGGER`\) also give rise to an entry in this table.

Check constraints on domains are stored here, too.

**Table 51.13. `pg_constraint` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `oid` | `oid` |   | Row identifier \(hidden attribute; must be explicitly selected\) |
| `conname` | `name` |   | Constraint name \(not necessarily unique!\) |
| `connamespace` | `oid` | [`pg_namespace`](https://www.postgresql.org/docs/10/static/catalog-pg-namespace.html).oid | The OID of the namespace that contains this constraint |
| `contype` | `char` |   | `c` = check constraint, `f` = foreign key constraint, `p` = primary key constraint, `u` = unique constraint, `t` = constraint trigger, `x` = exclusion constraint |
| `condeferrable` | `bool` |   | Is the constraint deferrable? |
| `condeferred` | `bool` |   | Is the constraint deferred by default? |
| `convalidated` | `bool` |   | Has the constraint been validated? Currently, can only be false for foreign keys and CHECK constraints |
| `conrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | The table this constraint is on; 0 if not a table constraint |
| `contypid` | `oid` | [`pg_type`](https://www.postgresql.org/docs/10/static/catalog-pg-type.html).oid | The domain this constraint is on; 0 if not a domain constraint |
| `conindid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | The index supporting this constraint, if it's a unique, primary key, foreign key, or exclusion constraint; else 0 |
| `confrelid` | `oid` | [`pg_class`](https://www.postgresql.org/docs/10/static/catalog-pg-class.html).oid | If a foreign key, the referenced table; else 0 |
| `confupdtype` | `char` |   | Foreign key update action code: `a` = no action, `r` = restrict, `c` = cascade, `n` = set null, `d` = set default |
| `confdeltype` | `char` |   | Foreign key deletion action code: `a` = no action, `r` = restrict, `c` = cascade, `n` = set null, `d` = set default |
| `confmatchtype` | `char` |   | Foreign key match type: `f` = full, `p` = partial, `s` = simple |
| `conislocal` | `bool` |   | This constraint is defined locally for the relation. Note that a constraint can be locally defined and inherited simultaneously. |
| `coninhcount` | `int4` |   | The number of direct inheritance ancestors this constraint has. A constraint with a nonzero number of ancestors cannot be dropped nor renamed. |
| `connoinherit` | `bool` |   | This constraint is defined locally for the relation. It is a non-inheritable constraint. |
| `conkey` | `int2[]` | [`pg_attribute`](https://www.postgresql.org/docs/10/static/catalog-pg-attribute.html).attnum | If a table constraint \(including foreign keys, but not constraint triggers\), list of the constrained columns |
| `confkey` | `int2[]` | [`pg_attribute`](https://www.postgresql.org/docs/10/static/catalog-pg-attribute.html).attnum | If a foreign key, list of the referenced columns |
| `conpfeqop` | `oid[]` | [`pg_operator`](https://www.postgresql.org/docs/10/static/catalog-pg-operator.html).oid | If a foreign key, list of the equality operators for PK = FK comparisons |
| `conppeqop` | `oid[]` | [`pg_operator`](https://www.postgresql.org/docs/10/static/catalog-pg-operator.html).oid | If a foreign key, list of the equality operators for PK = PK comparisons |
| `conffeqop` | `oid[]` | [`pg_operator`](https://www.postgresql.org/docs/10/static/catalog-pg-operator.html).oid | If a foreign key, list of the equality operators for FK = FK comparisons |
| `conexclop` | `oid[]` | [`pg_operator`](https://www.postgresql.org/docs/10/static/catalog-pg-operator.html).oid | If an exclusion constraint, list of the per-column exclusion operators |
| `conbin` | `pg_node_tree` |   | If a check constraint, an internal representation of the expression |
| `consrc` | `text` |   | If a check constraint, a human-readable representation of the expression |

In the case of an exclusion constraint, `conkey` is only useful for constraint elements that are simple column references. For other cases, a zero appears in `conkey` and the associated index must be consulted to discover the expression that is constrained. \(`conkey` thus has the same contents as `pg_index`.`indkey` for the index.\)

#### Note

`consrc` is not updated when referenced objects change; for example, it won't track renaming of columns. Rather than relying on this field, it's best to use `pg_get_constraintdef()` to extract the definition of a check constraint.

#### Note

`pg_class.relchecks` needs to agree with the number of check-constraint entries found in this table for each relation.

