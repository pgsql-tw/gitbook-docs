# 18.12. Registering Event Log on Windows

To register a Windows event log library with the operating system, issue this command:

<pre><code><strong>regsvr32 pgsql_library_directory/pgevent.dll
</strong></code></pre>

This creates registry entries used by the event viewer, under the default event source named `PostgreSQL`.

To specify a different event source name (see [event\_source](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-EVENT-SOURCE)), use the `/n` and `/i` options:

<pre><code><strong>regsvr32 /n /i:event_source_name pgsql_library_directory/pgevent.dll
</strong></code></pre>

To unregister the event log library from the operating system, issue this command:

<pre><code><strong>regsvr32 /u [/i:event_source_name] pgsql_library_directory/pgevent.dll
</strong></code></pre>

#### Note

To enable event logging in the database server, modify [log\_destination](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-DESTINATION) to include `eventlog` in `postgresql.conf`.
