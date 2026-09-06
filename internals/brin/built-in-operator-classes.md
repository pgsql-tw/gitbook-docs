# 67.2. Built-in Operator Classes

The core PostgreSQL distribution includes the BRIN operator classes shown in [Table 67.1](https://www.postgresql.org/docs/12/brin-builtin-opclasses.html#BRIN-BUILTIN-OPCLASSES-TABLE).

The _minmax_ operator classes store the minimum and the maximum values appearing in the indexed column within the range. The _inclusion_ operator classes store a value which includes the values in the indexed column within the range.

#### **Table 67.1. Built-in BRIN Operator Classes**

| Name                     | Indexed Data Type             | Indexable Operators                                                 |
| ------------------------ | ----------------------------- | ------------------------------------------------------------------- |
| `int8_minmax_ops`        | `bigint`                      | `<` `<=` `=` `>=` `>`                                               |
| `bit_minmax_ops`         | `bit`                         | `<` `<=` `=` `>=` `>`                                               |
| `varbit_minmax_ops`      | `bit varying`                 | `<` `<=` `=` `>=` `>`                                               |
| `box_inclusion_ops`      | `box`                         | `<<` `&<` `&&` `&>` `>>` `~=` `@>` `<@` `&<\|` `<<\|` `\|>>` `\|&>` |
| `bytea_minmax_ops`       | `bytea`                       | `<` `<=` `=` `>=` `>`                                               |
| `bpchar_minmax_ops`      | `character`                   | `<` `<=` `=` `>=` `>`                                               |
| `char_minmax_ops`        | `"char"`                      | `<` `<=` `=` `>=` `>`                                               |
| `date_minmax_ops`        | `date`                        | `<` `<=` `=` `>=` `>`                                               |
| `float8_minmax_ops`      | `double precision`            | `<` `<=` `=` `>=` `>`                                               |
| `inet_minmax_ops`        | `inet`                        | `<` `<=` `=` `>=` `>`                                               |
| `network_inclusion_ops`  | `inet`                        | `&&` `>>=` `<<=` `=` `>>` `<<`                                      |
| `int4_minmax_ops`        | `integer`                     | `<` `<=` `=` `>=` `>`                                               |
| `interval_minmax_ops`    | `interval`                    | `<` `<=` `=` `>=` `>`                                               |
| `macaddr_minmax_ops`     | `macaddr`                     | `<` `<=` `=` `>=` `>`                                               |
| `macaddr8_minmax_ops`    | `macaddr8`                    | `<` `<=` `=` `>=` `>`                                               |
| `name_minmax_ops`        | `name`                        | `<` `<=` `=` `>=` `>`                                               |
| `numeric_minmax_ops`     | `numeric`                     | `<` `<=` `=` `>=` `>`                                               |
| `pg_lsn_minmax_ops`      | `pg_lsn`                      | `<` `<=` `=` `>=` `>`                                               |
| `oid_minmax_ops`         | `oid`                         | `<` `<=` `=` `>=` `>`                                               |
| `range_inclusion_ops`    | `any range type`              | `<<` `&<` `&&` `&>` `>>` `@>` `<@` `-\|-` `=` `<` `<=` `=` `>` `>=` |
| `float4_minmax_ops`      | `real`                        | `<` `<=` `=` `>=` `>`                                               |
| `int2_minmax_ops`        | `smallint`                    | `<` `<=` `=` `>=` `>`                                               |
| `text_minmax_ops`        | `text`                        | `<` `<=` `=` `>=` `>`                                               |
| `tid_minmax_ops`         | `tid`                         | `<` `<=` `=` `>=` `>`                                               |
| `timestamp_minmax_ops`   | `timestamp without time zone` | `<` `<=` `=` `>=` `>`                                               |
| `timestamptz_minmax_ops` | `timestamp with time zone`    | `<` `<=` `=` `>=` `>`                                               |
| `time_minmax_ops`        | `time without time zone`      | `<` `<=` `=` `>=` `>`                                               |
| `timetz_minmax_ops`      | `time with time zone`         | `<` `<=` `=` `>=` `>`                                               |
| `uuid_minmax_ops`        | `uuid`                        | `<` `<=` `=` `>=` `>`                                               |
