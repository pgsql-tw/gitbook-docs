### 28.2.3. Statistics Functions

Other ways of looking at the statistics can be set up by writing queries that use the same underlying statistics access functions used by the standard views shown above. For details such as the functions' names, consult the definitions of the standard views. \(For example, inpsqlyou could issue`\d+ pg_stat_activity`.\) The access functions for per-database statistics take a database OID as an argument to identify which database to report on. The per-table and per-index functions take a table or index OID. The functions for per-function statistics take a function OID. Note that only tables, indexes, and functions in the current database can be seen with these functions.

Additional functions related to statistics collection are listed in[Table 28.19](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-FUNCS-TABLE).

**Table 28.19. Additional Statistics Functions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `pg_backend_pid()` | `integer` | Process ID of the server process handling the current session |
| `pg_stat_get_activity`\(`integer`\) | `setof record` | Returns a record of information about the backend with the specified PID, or one record for each active backend in the system if`NULL`is specified. The fields returned are a subset of those in the`pg_stat_activity`view. |
| `pg_stat_get_snapshot_timestamp()` | `timestamp with time zone` | Returns the timestamp of the current statistics snapshot |
| `pg_stat_clear_snapshot()` | `void` | Discard the current statistics snapshot |
| `pg_stat_reset()` | `void` | Reset all statistics counters for the current database to zero \(requires superuser privileges by default, but EXECUTE for this function can be granted to others.\) |
| `pg_stat_reset_shared`\(text\) | `void` | Reset some cluster-wide statistics counters to zero, depending on the argument \(requires superuser privileges by default, but EXECUTE for this function can be granted to others\). Calling`pg_stat_reset_shared('bgwriter')`will zero all the counters shown in the`pg_stat_bgwriter`view. Calling`pg_stat_reset_shared('archiver')`will zero all the counters shown in the`pg_stat_archiver`view. |
| `pg_stat_reset_single_table_counters`\(oid\) | `void` | Reset statistics for a single table or index in the current database to zero \(requires superuser privileges by default, but EXECUTE for this function can be granted to others\) |
| `pg_stat_reset_single_function_counters`\(oid\) | `void` | Reset statistics for a single function in the current database to zero \(requires superuser privileges by default, but EXECUTE for this function can be granted to others\) |

  


`pg_stat_get_activity`, the underlying function of the`pg_stat_activity`view, returns a set of records containing all the available information about each backend process. Sometimes it may be more convenient to obtain just a subset of this information. In such cases, an older set of per-backend statistics access functions can be used; these are shown in[Table 28.20](https://www.postgresql.org/docs/10/static/monitoring-stats.html#MONITORING-STATS-BACKEND-FUNCS-TABLE). These access functions use a backend ID number, which ranges from one to the number of currently active backends. The function`pg_stat_get_backend_idset`provides a convenient way to generate one row for each active backend for invoking these functions. For example, to show thePIDs and current queries of all backends:

```
    SELECT pg_stat_get_backend_pid(s.backendid) AS pid,
       pg_stat_get_backend_activity(s.backendid) AS query
    FROM (SELECT pg_stat_get_backend_idset() AS backendid) AS s;
```

**Table 28.20. Per-Backend Statistics Functions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `pg_stat_get_backend_idset()` | `setof integer` | Set of currently active backend ID numbers \(from 1 to the number of active backends\) |
| `pg_stat_get_backend_activity(integer)` | `text` | Text of this backend's most recent query |
| `pg_stat_get_backend_activity_start(integer)` | `timestamp with time zone` | Time when the most recent query was started |
| `pg_stat_get_backend_client_addr(integer)` | `inet` | IP address of the client connected to this backend |
| `pg_stat_get_backend_client_port(integer)` | `integer` | TCP port number that the client is using for communication |
| `pg_stat_get_backend_dbid(integer)` | `oid` | OID of the database this backend is connected to |
| `pg_stat_get_backend_pid(integer)` | `integer` | Process ID of this backend |
| `pg_stat_get_backend_start(integer)` | `timestamp with time zone` | Time when this process was started |
| `pg_stat_get_backend_userid(integer)` | `oid` | OID of the user logged into this backend |
| `pg_stat_get_backend_wait_event_type(integer)` | `text` | Wait event type name if backend is currently waiting, otherwise NULL. See[Table 28.4](https://www.postgresql.org/docs/10/static/monitoring-stats.html#WAIT-EVENT-TABLE)for details. |
| `pg_stat_get_backend_wait_event(integer)` | `text` | Wait event name if backend is currently waiting, otherwise NULL. See[Table 28.4](https://www.postgresql.org/docs/10/static/monitoring-stats.html#WAIT-EVENT-TABLE)for details. |
| `pg_stat_get_backend_xact_start(integer)` | `timestamp with time zone` | Time when the current transaction was started |



