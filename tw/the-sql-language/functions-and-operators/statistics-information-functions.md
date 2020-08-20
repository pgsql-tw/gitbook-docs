# 9.29. Statistics Information Functions

PostgreSQL provides a function to inspect complex statistics defined using the `CREATE STATISTICS` command.

## 9.29.1. Inspecting MCV Lists

`pg_mcv_list_items` returns a list of all items stored in a multi-column MCV list, and returns the following columns:

| Name | Type | Description |
| :--- | :--- | :--- |
| `index` | `int` | index of the item in the MCV list |
| `values` | `text[]` | values stored in the MCV item |
| `nulls` | `boolean[]` | flags identifying `NULL` values |
| `frequency` | `double precision` | frequency of this MCV item |
| `base_frequency` | `double precision` | base frequency of this MCV item |

The `pg_mcv_list_items` function can be used like this:

```text
SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts';
```

Values of the `pg_mcv_list` can be obtained only from the `pg_statistic_ext_data.stxdmcv` column.

