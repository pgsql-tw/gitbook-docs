# 21.5. Default Roles

PostgreSQL provides a set of default roles which provide access to certain, commonly needed, privileged capabilities and information. Administrators can GRANT these roles to users and/or other roles in their environment, providing those users with access to the specified capabilities and information.

The default roles are described in [Table 21.1](https://www.postgresql.org/docs/10/static/default-roles.html#DEFAULT-ROLES-TABLE). Note that the specific permissions for each of the default roles may change in the future as additional capabilities are added. Administrators should monitor the release notes for changes.

**Table 21.1. Default Roles**

| Role | Allowed Access |
| --- | --- | --- | --- | --- | --- |
| pg\_read\_all\_settings | Read all configuration variables, even those normally visible only to superusers. |
| pg\_read\_all\_stats | Read all pg\_stat\_\* views and use various statistics related extensions, even those normally visible only to superusers. |
| pg\_stat\_scan\_tables | Execute monitoring functions that may take `ACCESS SHARE` locks on tables, potentially for a long time. |
| pg\_signal\_backend | Send signals to other backends \(eg: cancel query, terminate\). |
| pg\_monitor | Read/execute various monitoring views and functions. This role is a member of `pg_read_all_settings`, `pg_read_all_stats` and `pg_stat_scan_tables`. |

The `pg_monitor`, `pg_read_all_settings`, `pg_read_all_stats` and `pg_stat_scan_tables` roles are intended to allow administrators to easily configure a role for the purpose of monitoring the database server. They grant a set of common privileges allowing the role to read various useful configuration settings, statistics and other system information normally restricted to superusers.

Care should be taken when granting these roles to ensure they are only used where needed to perform the desired monitoring.

Administrators can grant access to these roles to users using the GRANT command:

```text
GRANT pg_signal_backend TO admin_user;
```

