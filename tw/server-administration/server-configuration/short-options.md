# 19.18. Short Options

For convenience there are also single letter command-line option switches available for some parameters. They are described in [Table 19.2](https://www.postgresql.org/docs/12/runtime-config-short.html#RUNTIME-CONFIG-SHORT-TABLE). Some of these options exist for historical reasons, and their presence as a single-letter option does not necessarily indicate an endorsement to use the option heavily.

## **Table 19.2. Short Option Key**

| Short Option | Equivalent |
| :--- | :--- |
| `-B` _`x`_ | `shared_buffers =` _`x`_ |
| `-d` _`x`_ | `log_min_messages = DEBUG`_`x`_ |
| `-e` | `datestyle = euro` |
| `-fb`, `-fh`, `-fi`, `-fm`, `-fn`, `-fo`, `-fs`, `-ft` | `enable_bitmapscan = off`, `enable_hashjoin = off`, `enable_indexscan = off`, `enable_mergejoin = off`, `enable_nestloop = off`, `enable_indexonlyscan = off`, `enable_seqscan = off`, `enable_tidscan = off` |
| `-F` | `fsync = off` |
| `-h` _`x`_ | `listen_addresses =` _`x`_ |
| `-i` | `listen_addresses = '*'` |
| `-k` _`x`_ | `unix_socket_directories =` _`x`_ |
| `-l` | `ssl = on` |
| `-N` _`x`_ | `max_connections =` _`x`_ |
| `-O` | `allow_system_table_mods = on` |
| `-p` _`x`_ | `port =` _`x`_ |
| `-P` | `ignore_system_indexes = on` |
| `-s` | `log_statement_stats = on` |
| `-S` _`x`_ | `work_mem =` _`x`_ |
| `-tpa`, `-tpl`, `-te` | `log_parser_stats = on`, `log_planner_stats = on`, `log_executor_stats = on` |
| `-W` _`x`_ | `post_auth_delay =` _`x`_ |

