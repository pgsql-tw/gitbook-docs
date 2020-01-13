# 51.33. pg\_opclass

The catalog `pg_opclass` defines index access method operator classes. Each operator class defines semantics for index columns of a particular data type and a particular index access method. An operator class essentially specifies that a particular operator family is applicable to a particular indexable column data type. The set of operators from the family that are actually usable with the indexed column are whichever ones accept the column's data type as their left-hand input.

Operator classes are described at length in [Section 37.14](https://www.postgresql.org/docs/10/static/xindex.html).

**Table 51.33. `pg_opclass` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `oid` | `oid` |  | Row identifier \(hidden attribute; must be explicitly selected\) |
| `opcmethod` | `oid` | [`pg_am`](https://www.postgresql.org/docs/10/static/catalog-pg-am.html).oid | Index access method operator class is for |
| `opcname` | `name` |  | Name of this operator class |
| `opcnamespace` | `oid` | [`pg_namespace`](https://www.postgresql.org/docs/10/static/catalog-pg-namespace.html).oid | Namespace of this operator class |
| `opcowner` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/10/static/catalog-pg-authid.html).oid | Owner of the operator class |
| `opcfamily` | `oid` | [`pg_opfamily`](https://www.postgresql.org/docs/10/static/catalog-pg-opfamily.html).oid | Operator family containing the operator class |
| `opcintype` | `oid` | [`pg_type`](https://www.postgresql.org/docs/10/static/catalog-pg-type.html).oid | Data type that the operator class indexes |
| `opcdefault` | `bool` |  | True if this operator class is the default for `opcintype` |
| `opckeytype` | `oid` | [`pg_type`](https://www.postgresql.org/docs/10/static/catalog-pg-type.html).oid | Type of data stored in index, or zero if same as `opcintype` |

An operator class's `opcmethod` must match the `opfmethod` of its containing operator family. Also, there must be no more than one `pg_opclass` row having `opcdefault` true for any given combination of `opcmethod` and `opcintype`.

