## 18.12. Registering Event Log on Windows [#](#EVENT-LOG-REGISTRATION)

<a id="id-1.6.5.15.2"></a>

To register a Windows
event log library with the operating system,
issue this command:

```

regsvr32 pgsql_library_directory/pgevent.dll
```

This creates registry entries used by the event viewer, under the default
event source named `PostgreSQL`.

To specify a different event source name (see
[event_source](../runtime-config/runtime-config-logging.md#GUC-EVENT-SOURCE)), use the `/n`
and `/i` options:

```

regsvr32 /n /i:event_source_name pgsql_library_directory/pgevent.dll
```

To unregister the event log library from
the operating system, issue this command:

```

regsvr32 /u [/i:event_source_name] pgsql_library_directory/pgevent.dll
```

### Note

To enable event logging in the database server, modify
[log_destination](../runtime-config/runtime-config-logging.md#GUC-LOG-DESTINATION) to include
`eventlog` in `postgresql.conf`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-log-registration.html)（英文原文，待翻譯）
