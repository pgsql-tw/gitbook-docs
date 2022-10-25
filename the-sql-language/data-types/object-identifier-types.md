# 8.19. 物件指標型別

Object identifiers (OIDs) are used internally by PostgreSQL as primary keys for various system tables. Type `oid` represents an object identifier. There are also several alias types for `oid`: `regproc`, `regprocedure`, `regoper`, `regoperator`, `regclass`, `regtype`, `regrole`, `regnamespace`, `regconfig`, and `regdictionary`. [Table 8.26](https://www.postgresql.org/docs/12/datatype-oid.html#DATATYPE-OID-TABLE) shows an overview.

The `oid` type is currently implemented as an unsigned four-byte integer. Therefore, it is not large enough to provide database-wide uniqueness in large databases, or even in large individual tables.

The `oid` type itself has few operations beyond comparison. It can be cast to integer, however, and then manipulated using the standard integer operators. (Beware of possible signed-versus-unsigned confusion if you do this.)

The OID alias types have no operations of their own except for specialized input and output routines. These routines are able to accept and display symbolic names for system objects, rather than the raw numeric value that type `oid` would use. The alias types allow simplified lookup of OID values for objects. For example, to examine the `pg_attribute` rows related to a table `mytable`, one could write:

```
SELECT * FROM pg_attribute WHERE attrelid = 'mytable'::regclass;
```

rather than:

```
SELECT * FROM pg_attribute
  WHERE attrelid = (SELECT oid FROM pg_class WHERE relname = 'mytable');
```

While that doesn't look all that bad by itself, it's still oversimplified. A far more complicated sub-select would be needed to select the right OID if there are multiple tables named `mytable` in different schemas. The `regclass` input converter handles the table lookup according to the schema path setting, and so it does the “right thing” automatically. Similarly, casting a table's OID to `regclass` is handy for symbolic display of a numeric OID.

#### **Table 8.26. Object Identifier Types**

| Name            | References     | Description                  | Value Example                             |
| --------------- | -------------- | ---------------------------- | ----------------------------------------- |
| `oid`           | any            | numeric object identifier    | `564182`                                  |
| `regproc`       | `pg_proc`      | function name                | `sum`                                     |
| `regprocedure`  | `pg_proc`      | function with argument types | `sum(int4)`                               |
| `regoper`       | `pg_operator`  | operator name                | `+`                                       |
| `regoperator`   | `pg_operator`  | operator with argument types | `*(integer,integer)` or `-(NONE,integer)` |
| `regclass`      | `pg_class`     | relation name                | `pg_type`                                 |
| `regtype`       | `pg_type`      | data type name               | `integer`                                 |
| `regrole`       | `pg_authid`    | role name                    | `smithee`                                 |
| `regnamespace`  | `pg_namespace` | namespace name               | `pg_catalog`                              |
| `regconfig`     | `pg_ts_config` | text search configuration    | `english`                                 |
| `regdictionary` | `pg_ts_dict`   | text search dictionary       | `simple`                                  |

All of the OID alias types for objects grouped by namespace accept schema-qualified names, and will display schema-qualified names on output if the object would not be found in the current search path without being qualified. The `regproc` and `regoper` alias types will only accept input names that are unique (not overloaded), so they are of limited use; for most uses `regprocedure` or `regoperator` are more appropriate. For `regoperator`, unary operators are identified by writing `NONE` for the unused operand.

An additional property of most of the OID alias types is the creation of dependencies. If a constant of one of these types appears in a stored expression (such as a column default expression or view), it creates a dependency on the referenced object. For example, if a column has a default expression `nextval('my_seq'::regclass)`, PostgreSQL understands that the default expression depends on the sequence `my_seq`; the system will not let the sequence be dropped without first removing the default expression. `regrole` is the only exception for the property. Constants of this type are not allowed in such expressions.

#### Note

The OID alias types do not completely follow transaction isolation rules. The planner also treats them as simple constants, which may result in sub-optimal planning.

Another identifier type used by the system is `xid`, or transaction (abbreviated xact) identifier. This is the data type of the system columns `xmin` and `xmax`. Transaction identifiers are 32-bit quantities.

A third identifier type used by the system is `cid`, or command identifier. This is the data type of the system columns `cmin` and `cmax`. Command identifiers are also 32-bit quantities.

A final identifier type used by the system is `tid`, or tuple identifier (row identifier). This is the data type of the system column `ctid`. A tuple ID is a pair (block number, tuple index within block) that identifies the physical location of the row within its table.

(The system columns are further explained in [Section 5.5](https://www.postgresql.org/docs/12/ddl-system-columns.html).)
