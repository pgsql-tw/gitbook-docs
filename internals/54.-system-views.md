# 54. System Views

In addition to the system catalogs, PostgreSQL provides a number of built-in views. Some system views provide convenient access to some commonly used queries on the system catalogs. Other views provide access to internal server state.

The information schema ([Chapter 37](https://www.postgresql.org/docs/15/information-schema.html)) provides an alternative set of views which overlap the functionality of the system views. Since the information schema is SQL-standard whereas the views described here are PostgreSQL-specific, it's usually better to use the information schema if it provides all the information you need.

[Table 54.1](https://www.postgresql.org/docs/15/views-overview.html#VIEW-TABLE) lists the system views described here. More detailed documentation of each view follows below. There are some additional views that provide access to accumulated statistics; they are described in [Table 28.2](https://www.postgresql.org/docs/15/monitoring-stats.html#MONITORING-STATS-VIEWS-TABLE).
