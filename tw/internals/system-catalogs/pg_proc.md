---
description: 版本：11
---

# 52.39. pg\_proc

The catalog `pg_proc` stores information about functions, procedures, aggregate functions, and window functions \(collectively also known as routines\). See [CREATE FUNCTION](https://www.postgresql.org/docs/11/sql-createfunction.html), [CREATE PROCEDURE](https://www.postgresql.org/docs/11/sql-createprocedure.html), and [Section 38.3](https://www.postgresql.org/docs/11/xfunc.html) for more information.

If `prokind` indicates that the entry is for an aggregate function, there should be a matching row in `pg_aggregate`.

**Table 52.39. `pg_proc` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `oid` | `oid` |  | Row identifier \(hidden attribute; must be explicitly selected\) |
| `proname` | `name` |  | Name of the function |
| `pronamespace` | `oid` | [`pg_namespace`](https://www.postgresql.org/docs/11/catalog-pg-namespace.html).oid | The OID of the namespace that contains this function |
| `proowner` | `oid` | [`pg_authid`](https://www.postgresql.org/docs/11/catalog-pg-authid.html).oid | Owner of the function |
| `prolang` | `oid` | [`pg_language`](https://www.postgresql.org/docs/11/catalog-pg-language.html).oid | Implementation language or call interface of this function |
| `procost` | `float4` |  | Estimated execution cost \(in units of [cpu\_operator\_cost](https://www.postgresql.org/docs/11/runtime-config-query.html#GUC-CPU-OPERATOR-COST)\); if `proretset`, this is cost per row returned |
| `prorows` | `float4` |  | Estimated number of result rows \(zero if not `proretset`\) |
| `provariadic` | `oid` | [`pg_type`](https://www.postgresql.org/docs/11/catalog-pg-type.html).oid | Data type of the variadic array parameter's elements, or zero if the function does not have a variadic parameter |
| `protransform` | `regproc` | [`pg_proc`](https://www.postgresql.org/docs/11/catalog-pg-proc.html).oid | Calls to this function can be simplified by this other function \(see [Section 38.10.10](https://www.postgresql.org/docs/11/xfunc-c.html#XFUNC-TRANSFORM-FUNCTIONS)\) |
| `prokind` | `char` |  | `f` for a normal function, `p` for a procedure, `a` for an aggregate function, or `w` for a window function |
| `prosecdef` | `bool` |  | Function is a security definer \(i.e., a “setuid” function\) |
| `proleakproof` | `bool` |  | The function has no side effects. No information about the arguments is conveyed except via the return value. Any function that might throw an error depending on the values of its arguments is not leak-proof. |
| `proisstrict` | `bool` |  | Function returns null if any call argument is null. In that case the function won't actually be called at all. Functions that are not “strict” must be prepared to handle null inputs. |
| `proretset` | `bool` |  | Function returns a set \(i.e., multiple values of the specified data type\) |
| `provolatile` | `char` |  | `provolatile` tells whether the function's result depends only on its input arguments, or is affected by outside factors. It is `i` for “immutable” functions, which always deliver the same result for the same inputs. It is `s` for “stable” functions, whose results \(for fixed inputs\) do not change within a scan. It is `v` for “volatile” functions, whose results might change at any time. \(Use `v` also for functions with side-effects, so that calls to them cannot get optimized away.\) |
| `proparallel` | `char` |  | `proparallel` tells whether the function can be safely run in parallel mode. It is `s` for functions which are safe to run in parallel mode without restriction. It is `r` for functions which can be run in parallel mode, but their execution is restricted to the parallel group leader; parallel worker processes cannot invoke these functions. It is `u` for functions which are unsafe in parallel mode; the presence of such a function forces a serial execution plan. |
| `pronargs` | `int2` |  | Number of input arguments |
| `pronargdefaults` | `int2` |  | Number of arguments that have defaults |
| `prorettype` | `oid` | [`pg_type`](https://www.postgresql.org/docs/11/catalog-pg-type.html).oid | Data type of the return value |
| `proargtypes` | `oidvector` | [`pg_type`](https://www.postgresql.org/docs/11/catalog-pg-type.html).oid | An array with the data types of the function arguments. This includes only input arguments \(including `INOUT` and `VARIADIC` arguments\), and thus represents the call signature of the function. |
| `proallargtypes` | `oid[]` | [`pg_type`](https://www.postgresql.org/docs/11/catalog-pg-type.html).oid | An array with the data types of the function arguments. This includes all arguments \(including `OUT` and `INOUT` arguments\); however, if all the arguments are `IN` arguments, this field will be null. Note that subscripting is 1-based, whereas for historical reasons `proargtypes` is subscripted from 0. |
| `proargmodes` | `char[]` |  | An array with the modes of the function arguments, encoded as `i` for `IN` arguments, `o` for `OUT` arguments, `b` for `INOUT` arguments, `v` for `VARIADIC` arguments, `t` for `TABLE` arguments. If all the arguments are `IN` arguments, this field will be null. Note that subscripts correspond to positions of `proallargtypes` not `proargtypes`. |
| `proargnames` | `text[]` |  | An array with the names of the function arguments. Arguments without a name are set to empty strings in the array. If none of the arguments have a name, this field will be null. Note that subscripts correspond to positions of `proallargtypes` not `proargtypes`. |
| `proargdefaults` | `pg_node_tree` |  | Expression trees \(in `nodeToString()` representation\) for default values. This is a list with `pronargdefaults` elements, corresponding to the last _`N`_ _input_ arguments \(i.e., the last _`N`_ `proargtypes` positions\). If none of the arguments have defaults, this field will be null. |
| `protrftypes` | `oid[]` |  | Data type OIDs for which to apply transforms. |
| `prosrc` | `text` |  | This tells the function handler how to invoke the function. It might be the actual source code of the function for interpreted languages, a link symbol, a file name, or just about anything else, depending on the implementation language/call convention. |
| `probin` | `text` |  | Additional information about how to invoke the function. Again, the interpretation is language-specific. |
| `proconfig` | `text[]` |  | Function's local settings for run-time configuration variables |
| `proacl` | `aclitem[]` |  | Access privileges; see [GRANT](https://www.postgresql.org/docs/11/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/11/sql-revoke.html) for details |

For compiled functions, both built-in and dynamically loaded, `prosrc` contains the function's C-language name \(link symbol\). For all other currently-known language types, `prosrc` contains the function's source text. `probin` is unused except for dynamically-loaded C functions, for which it gives the name of the shared library file containing the function.

