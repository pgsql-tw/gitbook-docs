## Chapter 19. Server Configuration

**Table of Contents**

[19.1. Setting Parameters](config-setting.md)
:   [19.1.1. Parameter Names and Values](config-setting.md#CONFIG-SETTING-NAMES-VALUES)

    [19.1.2. Parameter Interaction via the Configuration File](config-setting.md#CONFIG-SETTING-CONFIGURATION-FILE)

    [19.1.3. Parameter Interaction via SQL](config-setting.md#CONFIG-SETTING-SQL)

    [19.1.4. Parameter Interaction via the Shell](config-setting.md#CONFIG-SETTING-SHELL)

    [19.1.5. Managing Configuration File Contents](config-setting.md#CONFIG-INCLUDES)

[19.2. File Locations](runtime-config-file-locations.md)

[19.3. Connections and Authentication](runtime-config-connection.md)
:   [19.3.1. Connection Settings](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SETTINGS)

    [19.3.2. TCP Settings](runtime-config-connection.md#RUNTIME-CONFIG-TCP-SETTINGS)

    [19.3.3. Authentication](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-AUTHENTICATION)

    [19.3.4. SSL](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SSL)

[19.4. Resource Consumption](runtime-config-resource.md)
:   [19.4.1. Memory](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY)

    [19.4.2. Disk](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-DISK)

    [19.4.3. Kernel Resource Usage](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-KERNEL)

    [19.4.4. Background Writer](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)

    [19.4.5. I/O](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-IO)

    [19.4.6. Worker Processes](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES)

[19.5. Write Ahead Log](runtime-config-wal.md)
:   [19.5.1. Settings](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SETTINGS)

    [19.5.2. Checkpoints](runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)

    [19.5.3. Archiving](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)

    [19.5.4. Recovery](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY)

    [19.5.5. Archive Recovery](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)

    [19.5.6. Recovery Target](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)

    [19.5.7. WAL Summarization](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)

[19.6. Replication](runtime-config-replication.md)
:   [19.6.1. Sending Servers](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SENDER)

    [19.6.2. Primary Server](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-PRIMARY)

    [19.6.3. Standby Servers](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)

    [19.6.4. Subscribers](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SUBSCRIBER)

[19.7. Query Planning](runtime-config-query.md)
:   [19.7.1. Planner Method Configuration](runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE)

    [19.7.2. Planner Cost Constants](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)

    [19.7.3. Genetic Query Optimizer](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO)

    [19.7.4. Other Planner Options](runtime-config-query.md#RUNTIME-CONFIG-QUERY-OTHER)

[19.8. Error Reporting and Logging](runtime-config-logging.md)
:   [19.8.1. Where to Log](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHERE)

    [19.8.2. When to Log](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHEN)

    [19.8.3. What to Log](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHAT)

    [19.8.4. Using CSV-Format Log Output](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG)

    [19.8.5. Using JSON-Format Log Output](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG)

    [19.8.6. Process Title](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-PROC-TITLE)

[19.9. Run-time Statistics](runtime-config-statistics.md)
:   [19.9.1. Cumulative Query and Index Statistics](runtime-config-statistics.md#RUNTIME-CONFIG-CUMULATIVE-STATISTICS)

    [19.9.2. Statistics Monitoring](runtime-config-statistics.md#RUNTIME-CONFIG-STATISTICS-MONITOR)

[19.10. Vacuuming](runtime-config-vacuum.md)
:   [19.10.1. Automatic Vacuuming](runtime-config-vacuum.md#RUNTIME-CONFIG-AUTOVACUUM)

    [19.10.2. Cost-based Vacuum Delay](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)

    [19.10.3. Default Behavior](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-DEFAULT)

    [19.10.4. Freezing](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-FREEZING)

[19.11. Client Connection Defaults](runtime-config-client.md)
:   [19.11.1. Statement Behavior](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-STATEMENT)

    [19.11.2. Locale and Formatting](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT)

    [19.11.3. Shared Library Preloading](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-PRELOAD)

    [19.11.4. Other Defaults](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-OTHER)

[19.12. Lock Management](runtime-config-locks.md)

[19.13. Version and Platform Compatibility](runtime-config-compatible.md)
:   [19.13.1. Previous PostgreSQL Versions](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-VERSION)

    [19.13.2. Platform and Client Compatibility](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

[19.14. Error Handling](runtime-config-error-handling.md)

[19.15. Preset Options](runtime-config-preset.md)

[19.16. Customized Options](runtime-config-custom.md)

[19.17. Developer Options](runtime-config-developer.md)

[19.18. Short Options](runtime-config-short.md)

<a id="id-1.6.6.2"></a>

There are many configuration parameters that affect the behavior of
the database system. In the first section of this chapter we
describe how to interact with configuration parameters. The subsequent sections
discuss each parameter in detail.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config.html)（英文原文，待翻譯）
