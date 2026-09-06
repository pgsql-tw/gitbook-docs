# Part III. Server Administration

<a id="id-1.6.2"></a>

This part covers topics that are of interest to a
PostgreSQL administrator. This includes
installation, configuration of the server, management of users
and databases, and maintenance tasks. Anyone running
PostgreSQL server, even for
personal use, but especially in production, should be familiar
with these topics.

The information attempts to be in the order in which
a new user should read it. The chapters are self-contained and
can be read individually as desired. The information is presented
in a narrative form in topical units. Readers looking for a complete
description of a command are encouraged to review the
[Part VI](../reference/README.md).

The first few chapters are written so they can be understood
without prerequisite knowledge, so new users who need to set
up their own server can begin their exploration. The rest of this
part is about tuning and management; that material
assumes that the reader is familiar with the general use of
the PostgreSQL database system. Readers are
encouraged review the [Part I](../tutorial/README.md) and [Part II](../the-sql-language/README.md) parts for additional information.

**Table of Contents**

[16. Installation from Binaries](install-binaries/README.md)

[17. Installation from Source Code](installation/README.md)
:   [17.1. Requirements](installation/install-requirements.md)

    [17.2. Getting the Source](installation/install-getsource.md)

    [17.3. Building and Installation with Autoconf and Make](installation/install-make.md)

    [17.4. Building and Installation with Meson](installation/install-meson.md)

    [17.5. Post-Installation Setup](installation/install-post.md)

    [17.6. Supported Platforms](installation/supported-platforms.md)

    [17.7. Platform-Specific Notes](installation/installation-platform-notes.md)

[18. Server Setup and Operation](runtime/README.md)
:   [18.1. The PostgreSQL User Account](runtime/postgres-user.md)

    [18.2. Creating a Database Cluster](runtime/creating-cluster.md)

    [18.3. Starting the Database Server](runtime/server-start.md)

    [18.4. Managing Kernel Resources](runtime/kernel-resources.md)

    [18.5. Shutting Down the Server](runtime/server-shutdown.md)

    [18.6. Upgrading a PostgreSQL Cluster](runtime/upgrading.md)

    [18.7. Preventing Server Spoofing](runtime/preventing-server-spoofing.md)

    [18.8. Encryption Options](runtime/encryption-options.md)

    [18.9. Secure TCP/IP Connections with SSL](runtime/ssl-tcp.md)

    [18.10. Secure TCP/IP Connections with GSSAPI Encryption](runtime/gssapi-enc.md)

    [18.11. Secure TCP/IP Connections with SSH Tunnels](runtime/ssh-tunnels.md)

    [18.12. Registering Event Log on Windows](runtime/event-log-registration.md)

[19. Server Configuration](runtime-config/README.md)
:   [19.1. Setting Parameters](runtime-config/config-setting.md)

    [19.2. File Locations](runtime-config/runtime-config-file-locations.md)

    [19.3. Connections and Authentication](runtime-config/runtime-config-connection.md)

    [19.4. Resource Consumption](runtime-config/runtime-config-resource.md)

    [19.5. Write Ahead Log](runtime-config/runtime-config-wal.md)

    [19.6. Replication](runtime-config/runtime-config-replication.md)

    [19.7. Query Planning](runtime-config/runtime-config-query.md)

    [19.8. Error Reporting and Logging](runtime-config/runtime-config-logging.md)

    [19.9. Run-time Statistics](runtime-config/runtime-config-statistics.md)

    [19.10. Vacuuming](runtime-config/runtime-config-vacuum.md)

    [19.11. Client Connection Defaults](runtime-config/runtime-config-client.md)

    [19.12. Lock Management](runtime-config/runtime-config-locks.md)

    [19.13. Version and Platform Compatibility](runtime-config/runtime-config-compatible.md)

    [19.14. Error Handling](runtime-config/runtime-config-error-handling.md)

    [19.15. Preset Options](runtime-config/runtime-config-preset.md)

    [19.16. Customized Options](runtime-config/runtime-config-custom.md)

    [19.17. Developer Options](runtime-config/runtime-config-developer.md)

    [19.18. Short Options](runtime-config/runtime-config-short.md)

[20. Client Authentication](client-authentication/README.md)
:   [20.1. The `pg_hba.conf` File](client-authentication/auth-pg-hba-conf.md)

    [20.2. User Name Maps](client-authentication/auth-username-maps.md)

    [20.3. Authentication Methods](client-authentication/auth-methods.md)

    [20.4. Trust Authentication](client-authentication/auth-trust.md)

    [20.5. Password Authentication](client-authentication/auth-password.md)

    [20.6. GSSAPI Authentication](client-authentication/gssapi-auth.md)

    [20.7. SSPI Authentication](client-authentication/sspi-auth.md)

    [20.8. Ident Authentication](client-authentication/auth-ident.md)

    [20.9. Peer Authentication](client-authentication/auth-peer.md)

    [20.10. LDAP Authentication](client-authentication/auth-ldap.md)

    [20.11. RADIUS Authentication](client-authentication/auth-radius.md)

    [20.12. Certificate Authentication](client-authentication/auth-cert.md)

    [20.13. PAM Authentication](client-authentication/auth-pam.md)

    [20.14. BSD Authentication](client-authentication/auth-bsd.md)

    [20.15. OAuth Authorization/Authentication](client-authentication/auth-oauth.md)

    [20.16. Authentication Problems](client-authentication/client-authentication-problems.md)

[21. Database Roles](user-manag/README.md)
:   [21.1. Database Roles](user-manag/database-roles.md)

    [21.2. Role Attributes](user-manag/role-attributes.md)

    [21.3. Role Membership](user-manag/role-membership.md)

    [21.4. Dropping Roles](user-manag/role-removal.md)

    [21.5. Predefined Roles](user-manag/predefined-roles.md)

    [21.6. Function Security](user-manag/perm-functions.md)

[22. Managing Databases](managing-databases/README.md)
:   [22.1. Overview](managing-databases/manage-ag-overview.md)

    [22.2. Creating a Database](managing-databases/manage-ag-createdb.md)

    [22.3. Template Databases](managing-databases/manage-ag-templatedbs.md)

    [22.4. Database Configuration](managing-databases/manage-ag-config.md)

    [22.5. Destroying a Database](managing-databases/manage-ag-dropdb.md)

    [22.6. Tablespaces](managing-databases/manage-ag-tablespaces.md)

[23. Localization](charset/README.md)
:   [23.1. Locale Support](charset/locale.md)

    [23.2. Collation Support](charset/collation.md)

    [23.3. Character Set Support](charset/multibyte.md)

[24. Routine Database Maintenance Tasks](maintenance/README.md)
:   [24.1. Routine Vacuuming](maintenance/routine-vacuuming.md)

    [24.2. Routine Reindexing](maintenance/routine-reindex.md)

    [24.3. Log File Maintenance](maintenance/logfile-maintenance.md)

[25. Backup and Restore](backup/README.md)
:   [25.1. SQL Dump](backup/backup-dump.md)

    [25.2. File System Level Backup](backup/backup-file.md)

    [25.3. Continuous Archiving and Point-in-Time Recovery (PITR)](backup/continuous-archiving.md)

[26. High Availability, Load Balancing, and Replication](high-availability/README.md)
:   [26.1. Comparison of Different Solutions](high-availability/different-replication-solutions.md)

    [26.2. Log-Shipping Standby Servers](high-availability/warm-standby.md)

    [26.3. Failover](high-availability/warm-standby-failover.md)

    [26.4. Hot Standby](high-availability/hot-standby.md)

[27. Monitoring Database Activity](monitoring/README.md)
:   [27.1. Standard Unix Tools](monitoring/monitoring-ps.md)

    [27.2. The Cumulative Statistics System](monitoring/monitoring-stats.md)

    [27.3. Viewing Locks](monitoring/monitoring-locks.md)

    [27.4. Progress Reporting](monitoring/progress-reporting.md)

    [27.5. Dynamic Tracing](monitoring/dynamic-trace.md)

    [27.6. Monitoring Disk Usage](monitoring/diskusage.md)

[28. Reliability and the Write-Ahead Log](wal/README.md)
:   [28.1. Reliability](wal/wal-reliability.md)

    [28.2. Data Checksums](wal/checksums.md)

    [28.3. Write-Ahead Logging (WAL)](wal/wal-intro.md)

    [28.4. Asynchronous Commit](wal/wal-async-commit.md)

    [28.5. WAL Configuration](wal/wal-configuration.md)

    [28.6. WAL Internals](wal/wal-internals.md)

[29. Logical Replication](logical-replication/README.md)
:   [29.1. Publication](logical-replication/logical-replication-publication.md)

    [29.2. Subscription](logical-replication/logical-replication-subscription.md)

    [29.3. Logical Replication Failover](logical-replication/logical-replication-failover.md)

    [29.4. Row Filters](logical-replication/logical-replication-row-filter.md)

    [29.5. Column Lists](logical-replication/logical-replication-col-lists.md)

    [29.6. Generated Column Replication](logical-replication/logical-replication-gencols.md)

    [29.7. Conflicts](logical-replication/logical-replication-conflicts.md)

    [29.8. Restrictions](logical-replication/logical-replication-restrictions.md)

    [29.9. Architecture](logical-replication/logical-replication-architecture.md)

    [29.10. Monitoring](logical-replication/logical-replication-monitoring.md)

    [29.11. Security](logical-replication/logical-replication-security.md)

    [29.12. Configuration Settings](logical-replication/logical-replication-config.md)

    [29.13. Upgrade](logical-replication/logical-replication-upgrade.md)

    [29.14. Quick Setup](logical-replication/logical-replication-quick-setup.md)

[30. Just-in-Time Compilation (JIT)](jit/README.md)
:   [30.1. What Is JIT compilation?](jit/jit-reason.md)

    [30.2. When to JIT?](jit/jit-decision.md)

    [30.3. Configuration](jit/jit-configuration.md)

    [30.4. Extensibility](jit/jit-extensibility.md)

[31. Regression Tests](regress/README.md)
:   [31.1. Running the Tests](regress/regress-run.md)

    [31.2. Test Evaluation](regress/regress-evaluation.md)

    [31.3. Variant Comparison Files](regress/regress-variant.md)

    [31.4. TAP Tests](regress/regress-tap.md)

    [31.5. Test Coverage Examination](regress/regress-coverage.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/admin.html)（英文原文，待翻譯）
