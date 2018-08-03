# 62.2. Built-in Operator Classes

The core PostgreSQL distribution includes the GiST operator classes shown in [Table 62.1](https://www.postgresql.org/docs/10/static/gist-builtin-opclasses.html#GIST-BUILTIN-OPCLASSES-TABLE). \(Some of the optional modules described in [Appendix F](https://www.postgresql.org/docs/10/static/contrib.html) provide additional GiST operator classes.\)

#### **Table 62.1. Built-in GiST Operator Classes**

| Name | Indexed Data Type | Indexable Operators | Ordering Operators |
| :--- | :--- | :--- | :--- |
| `box_ops` | `box` | `&&` `&>` `&<` `&<|` `>>` `<<` `<<|` `<@` `@>` `@` `|&>` `|>>` `~` `~=` |  |
| `circle_ops` | `circle` | `&&` `&>` `&<` `&<|` `>>` `<<` `<<|` `<@` `@>` `@` `|&>` `|>>` `~` `~=` | `<->` |
| `inet_ops` | `inet`, `cidr` | `&&` `>>` `>>=` `>` `>=` `<>` `<<` `<<=` `<` `<=` `=` |  |
| `point_ops` | `point` | `>>` `>^` `<<` `<@` `<@` `<@` `<^` `~=` | `<->` |
| `poly_ops` | `polygon` | `&&` `&>` `&<` `&<|` `>>` `<<` `<<|` `<@` `@>` `@` `|&>` `|>>` `~` `~=` | `<->` |
| `range_ops` | any range type | `&&` `&>` `&<` `>>` `<<` `<@` `-|-` `=` `@>` `@>` |  |
| `tsquery_ops` | `tsquery` | `<@` `@>` |  |
| `tsvector_ops` | `tsvector` | `@@` |  |

For historical reasons, the `inet_ops` operator class is not the default class for types `inet` and `cidr`. To use it, mention the class name in `CREATE INDEX`, for example

```text
CREATE INDEX ON my_table USING GIST (my_inet_column inet_ops);
```

