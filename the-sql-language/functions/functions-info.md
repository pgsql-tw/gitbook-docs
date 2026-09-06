## 9.27. System Information Functions and Operators [#](#FUNCTIONS-INFO)

[9.27.1. Session Information Functions](functions-info.md#FUNCTIONS-INFO-SESSION)

[9.27.2. Access Privilege Inquiry Functions](functions-info.md#FUNCTIONS-INFO-ACCESS)

[9.27.3. Schema Visibility Inquiry Functions](functions-info.md#FUNCTIONS-INFO-SCHEMA)

[9.27.4. System Catalog Information Functions](functions-info.md#FUNCTIONS-INFO-CATALOG)

[9.27.5. Object Information and Addressing Functions](functions-info.md#FUNCTIONS-INFO-OBJECT)

[9.27.6. Comment Information Functions](functions-info.md#FUNCTIONS-INFO-COMMENT)

[9.27.7. Data Validity Checking Functions](functions-info.md#FUNCTIONS-INFO-VALIDITY)

[9.27.8. Transaction ID and Snapshot Information Functions](functions-info.md#FUNCTIONS-INFO-SNAPSHOT)

[9.27.9. Committed Transaction Information Functions](functions-info.md#FUNCTIONS-INFO-COMMIT-TIMESTAMP)

[9.27.10. Control Data Functions](functions-info.md#FUNCTIONS-INFO-CONTROLDATA)

[9.27.11. Version Information Functions](functions-info.md#FUNCTIONS-INFO-VERSION)

[9.27.12. WAL Summarization Information Functions](functions-info.md#FUNCTIONS-INFO-WAL-SUMMARY)

The functions described in this section are used to obtain various
information about a PostgreSQL installation.

<a id="FUNCTIONS-INFO-SESSION"></a>

### 9.27.1. Session Information Functions [#](#FUNCTIONS-INFO-SESSION)

[Table 9.71](functions-info.md#FUNCTIONS-INFO-SESSION-TABLE) shows several
functions that extract session and system information.

In addition to the functions listed in this section, there are a number of
functions related to the statistics system that also provide system
information. See [Section 27.2.26](../../server-administration/monitoring/monitoring-stats.md#MONITORING-STATS-FUNCTIONS) for more
information.

<a id="FUNCTIONS-INFO-SESSION-TABLE"></a>

**Table 9.71. Session Information Functions**

<table border="1" class="table" summary="Session Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.1.1.1.1"></a>
<code class="function">current_catalog</code>
        → <code class="returnvalue">name</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.1.1.2.1"></a>
<code class="function">current_database</code> ()
        → <code class="returnvalue">name</code>
</p>
<p>
        Returns the name of the current database.  (Databases are
        called <span class="quote">“<span class="quote">catalogs</span>”</span> in the SQL standard,
        so <code class="function">current_catalog</code> is the standard's
        spelling.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.2.1.1.1"></a>
<code class="function">current_query</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the text of the currently executing query, as submitted
        by the client (which might contain more than one statement).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.3.1.1.1"></a>
<code class="function">current_role</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        This is equivalent to <code class="function">current_user</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.4.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.4.1.1.2"></a>
<code class="function">current_schema</code>
        → <code class="returnvalue">name</code>
</p>
<p class="func_signature">
<code class="function">current_schema</code> ()
        → <code class="returnvalue">name</code>
</p>
<p>
        Returns the name of the schema that is first in the search path (or a
        null value if the search path is empty).  This is the schema that will
        be used for any tables or other named objects that are created without
        specifying a target schema.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.5.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.5.1.1.2"></a>
<code class="function">current_schemas</code> ( <em class="parameter"><code>include_implicit</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">name[]</code>
</p>
<p>
        Returns an array of the names of all schemas presently in the
        effective search path, in their priority order.  (Items in the current
        <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH">search_path</a> setting that do not correspond to
        existing, searchable schemas are omitted.)  If the Boolean argument
        is <code class="literal">true</code>, then implicitly-searched system schemas
        such as <code class="literal">pg_catalog</code> are included in the result.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.6.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.6.1.1.2"></a>
<code class="function">current_user</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        Returns the user name of the current execution context.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.7.1.1.1"></a>
<code class="function">inet_client_addr</code> ()
        → <code class="returnvalue">inet</code>
</p>
<p>
        Returns the IP address of the current client,
        or <code class="literal">NULL</code> if the current connection is via a
        Unix-domain socket.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.8.1.1.1"></a>
<code class="function">inet_client_port</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the IP port number of the current client,
        or <code class="literal">NULL</code> if the current connection is via a
        Unix-domain socket.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.9.1.1.1"></a>
<code class="function">inet_server_addr</code> ()
        → <code class="returnvalue">inet</code>
</p>
<p>
        Returns the IP address on which the server accepted the current
        connection,
        or <code class="literal">NULL</code> if the current connection is via a
        Unix-domain socket.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.10.1.1.1"></a>
<code class="function">inet_server_port</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the IP port number on which the server accepted the current
        connection,
        or <code class="literal">NULL</code> if the current connection is via a
        Unix-domain socket.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.11.1.1.1"></a>
<code class="function">pg_backend_pid</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the process ID of the server process attached to the current
        session.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.12.1.1.1"></a>
<code class="function">pg_blocking_pids</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        Returns an array of the process ID(s) of the sessions that are
        blocking the server process with the specified process ID from
        acquiring a lock, or an empty array if there is no such server process
        or it is not blocked.
       </p>
<p>
        One server process blocks another if it either holds a lock that
        conflicts with the blocked process's lock request (hard block), or is
        waiting for a lock that would conflict with the blocked process's lock
        request and is ahead of it in the wait queue (soft block).  When using
        parallel queries the result always lists client-visible process IDs
        (that is, <code class="function">pg_backend_pid</code> results) even if the
        actual lock is held or awaited by a child worker process.  As a result
        of that, there may be duplicated PIDs in the result.  Also note that
        when a prepared transaction holds a conflicting lock, it will be
        represented by a zero process ID.
       </p>
<p>
        Frequent calls to this function could have some impact on database
        performance, because it needs exclusive access to the lock manager's
        shared state for a short time.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.13.1.1.1"></a>
<code class="function">pg_conf_load_time</code> ()
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Returns the time when the server configuration files were last loaded.
        If the current session was alive at the time, this will be the time
        when the session itself re-read the configuration files (so the
        reading will vary a little in different sessions).  Otherwise it is
        the time when the postmaster process re-read the configuration files.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.2"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.3"></a>
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.14.1.1.4"></a>
<code class="function">pg_current_logfile</code> ( [<span class="optional"> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the path name of the log file currently in use by the logging
        collector.  The path includes the <a class="xref" href="../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-DIRECTORY">log_directory</a>
        directory and the individual log file name.  The result
        is <code class="literal">NULL</code> if the logging collector is disabled.
        When multiple log files exist, each in a different
        format, <code class="function">pg_current_logfile</code> without an argument
        returns the path of the file having the first format found in the
        ordered list: <code class="literal">stderr</code>,
        <code class="literal">csvlog</code>, <code class="literal">jsonlog</code>.
        <code class="literal">NULL</code> is returned if no log file has any of these
        formats.
        To request information about a specific log file format, supply
        either <code class="literal">csvlog</code>, <code class="literal">jsonlog</code> or
        <code class="literal">stderr</code> as the
        value of the optional parameter. The result is <code class="literal">NULL</code>
        if the log format requested is not configured in
        <a class="xref" href="../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-DESTINATION">log_destination</a>.
        The result reflects the contents of
        the <code class="filename">current_logfiles</code> file.
       </p>
<p>
        This function is restricted to superusers and roles with privileges of
        the <code class="literal">pg_monitor</code> role by default, but other users can
        be granted EXECUTE to run the function.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.15.1.1.1"></a>
<code class="function">pg_get_loaded_modules</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>module_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>version</code></em> <code class="type">text</code>,
        <em class="parameter"><code>file_name</code></em> <code class="type">text</code> )
       </p>
<p>
        Returns a list of the loadable modules that are loaded into the
        current server session.  The <em class="parameter"><code>module_name</code></em>
        and <em class="parameter"><code>version</code></em> fields are NULL unless the
        module author supplied values for them using
        the <code class="literal">PG_MODULE_MAGIC_EXT</code> macro.
        The <em class="parameter"><code>file_name</code></em> field gives the file
        name of the module (shared library).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.16.1.1.1"></a>
<code class="function">pg_my_temp_schema</code> ()
        → <code class="returnvalue">oid</code>
</p>
<p>
        Returns the OID of the current session's temporary schema, or zero if
        it has none (because it has not created any temporary tables).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.17.1.1.1"></a>
<code class="function">pg_is_other_temp_schema</code> ( <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns true if the given OID is the OID of another session's
        temporary schema.  (This can be useful, for example, to exclude other
        sessions' temporary tables from a catalog display.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.18.1.1.1"></a>
<code class="function">pg_jit_available</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns true if a <acronym class="acronym">JIT</acronym> compiler extension is
        available (see <a class="xref" href="../../server-administration/jit/README.md">Chapter 30</a>) and the
        <a class="xref" href="../../server-administration/runtime-config/runtime-config-query.md#GUC-JIT">jit</a> configuration parameter is set to
        <code class="literal">on</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.19.1.1.1"></a>
<code class="function">pg_numa_available</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Returns true if the server has been compiled with <acronym class="acronym">NUMA</acronym> support.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.20.1.1.1"></a>
<code class="function">pg_listening_channels</code> ()
        → <code class="returnvalue">setof text</code>
</p>
<p>
        Returns the set of names of asynchronous notification channels that
        the current session is listening to.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.21.1.1.1"></a>
<code class="function">pg_notification_queue_usage</code> ()
        → <code class="returnvalue">double precision</code>
</p>
<p>
        Returns the fraction (0–1) of the asynchronous notification
        queue's maximum size that is currently occupied by notifications that
        are waiting to be processed.
        See <a class="xref" href="../../reference/sql-commands/sql-listen.md"><span class="refentrytitle">LISTEN</span></a> and <a class="xref" href="../../reference/sql-commands/sql-notify.md"><span class="refentrytitle">NOTIFY</span></a>
        for more information.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.22.1.1.1"></a>
<code class="function">pg_postmaster_start_time</code> ()
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Returns the time when the server started.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.23.1.1.1"></a>
<code class="function">pg_safe_snapshot_blocking_pids</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        Returns an array of the process ID(s) of the sessions that are blocking
        the server process with the specified process ID from acquiring a safe
        snapshot, or an empty array if there is no such server process or it
        is not blocked.
       </p>
<p>
        A session running a <code class="literal">SERIALIZABLE</code> transaction blocks
        a <code class="literal">SERIALIZABLE READ ONLY DEFERRABLE</code> transaction
        from acquiring a snapshot until the latter determines that it is safe
        to avoid taking any predicate locks.  See
        <a class="xref" href="../mvcc/transaction-iso.md#XACT-SERIALIZABLE">Section 13.2.3</a> for more information about
        serializable and deferrable transactions.
       </p>
<p>
        Frequent calls to this function could have some impact on database
        performance, because it needs access to the predicate lock manager's
        shared state for a short time.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.24.1.1.1"></a>
<code class="function">pg_trigger_depth</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the current nesting level
        of <span class="productname">PostgreSQL</span> triggers (0 if not called,
        directly or indirectly, from inside a trigger).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.25.1.1.1"></a>
<code class="function">session_user</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        Returns the session user's name.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.26.1.1.1"></a>
<code class="function">system_user</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the authentication method and the identity (if any) that the
        user presented during the authentication cycle before they were
        assigned a database role. It is represented as
        <code class="literal">auth_method:identity</code> or
        <code class="literal">NULL</code> if the user has not been authenticated (for
        example if <a class="link" href="../../server-administration/client-authentication/auth-trust.md">Trust authentication</a> has
        been used).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.3.4.2.2.27.1.1.1"></a>
<code class="function">user</code>
        → <code class="returnvalue">name</code>
</p>
<p>
        This is equivalent to <code class="function">current_user</code>.
       </p></td></tr></tbody></table>

<br>

### Note

`current_catalog`,
`current_role`,
`current_schema`,
`current_user`,
`session_user`,
and `user` have special syntactic status
in SQL: they must be called without trailing
parentheses. In PostgreSQL, parentheses can optionally be used with
`current_schema`, but not with the others.

The `session_user` is normally the user who initiated
the current database connection; but superusers can change this setting
with [SET SESSION AUTHORIZATION](../../reference/sql-commands/sql-set-session-authorization.md).
The `current_user` is the user identifier
that is applicable for permission checking. Normally it is equal
to the session user, but it can be changed with
[SET ROLE](../../reference/sql-commands/sql-set-role.md).
It also changes during the execution of
functions with the attribute `SECURITY DEFINER`.
In Unix parlance, the session user is the “real user” and
the current user is the “effective user”.
`current_role` and `user` are
synonyms for `current_user`. (The SQL standard draws
a distinction between `current_role`
and `current_user`, but PostgreSQL
does not, since it unifies users and roles into a single kind of entity.)

<a id="FUNCTIONS-INFO-ACCESS"></a>

### 9.27.2. Access Privilege Inquiry Functions [#](#FUNCTIONS-INFO-ACCESS)

<a id="id-1.5.8.33.4.2"></a>

[Table 9.72](functions-info.md#FUNCTIONS-INFO-ACCESS-TABLE) lists functions that
allow querying object access privileges programmatically.
(See [Section 5.8](../ddl/ddl-priv.md) for more information about
privileges.)
In these functions, the user whose privileges are being inquired about
can be specified by name or by OID
(`pg_authid`.`oid`), or if
the name is given as `public` then the privileges of the
PUBLIC pseudo-role are checked. Also, the *`user`*
argument can be omitted entirely, in which case
the `current_user` is assumed.
The object that is being inquired about can be specified either by name or
by OID, too. When specifying by name, a schema name can be included if
relevant.
The access privilege of interest is specified by a text string, which must
evaluate to one of the appropriate privilege keywords for the object's type
(e.g., `SELECT`). Optionally, `WITH GRANT
OPTION` can be added to a privilege type to test whether the
privilege is held with grant option. Also, multiple privilege types can be
listed separated by commas, in which case the result will be true if any of
the listed privileges is held. (Case of the privilege string is not
significant, and extra whitespace is allowed between but not within
privilege names.)
Some examples:

```

SELECT has_table_privilege('myschema.mytable', 'select');
SELECT has_table_privilege('joe', 'mytable', 'INSERT, SELECT WITH GRANT OPTION');
```

<a id="FUNCTIONS-INFO-ACCESS-TABLE"></a>

**Table 9.72. Access Privilege Inquiry Functions**

<table border="1" class="table" summary="Access Privilege Inquiry Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.1.1.1.1"></a>
<code class="function">has_any_column_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for any column of table?
        This succeeds either if the privilege is held for the whole table, or
        if there is a column-level grant of the privilege for at least one
        column.
        Allowable privilege types are
        <code class="literal">SELECT</code>, <code class="literal">INSERT</code>,
        <code class="literal">UPDATE</code>, and <code class="literal">REFERENCES</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.2.1.1.1"></a>
<code class="function">has_column_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>column</code></em> <code class="type">text</code> or <code class="type">smallint</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for the specified table column?
        This succeeds either if the privilege is held for the whole table, or
        if there is a column-level grant of the privilege for the column.
        The column can be specified by name or by attribute number
        (<code class="structname">pg_attribute</code>.<code class="structfield">attnum</code>).
        Allowable privilege types are
        <code class="literal">SELECT</code>, <code class="literal">INSERT</code>,
        <code class="literal">UPDATE</code>, and <code class="literal">REFERENCES</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.3.1.1.1"></a>
<code class="function">has_database_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>database</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for database?
        Allowable privilege types are
        <code class="literal">CREATE</code>,
        <code class="literal">CONNECT</code>,
        <code class="literal">TEMPORARY</code>, and
        <code class="literal">TEMP</code> (which is equivalent to
        <code class="literal">TEMPORARY</code>).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.4.1.1.1"></a>
<code class="function">has_foreign_data_wrapper_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>fdw</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for foreign-data wrapper?
        The only allowable privilege type is <code class="literal">USAGE</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.5.1.1.1"></a>
<code class="function">has_function_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>function</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for function?
        The only allowable privilege type is <code class="literal">EXECUTE</code>.
       </p>
<p>
        When specifying a function by name rather than by OID, the allowed
        input is the same as for the <code class="type">regprocedure</code> data type (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>).
        An example is:
</p><pre class="programlisting">
SELECT has_function_privilege('joeuser', 'myfunc(int, text)', 'execute');
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.6.1.1.1"></a>
<code class="function">has_language_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>language</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for language?
        The only allowable privilege type is <code class="literal">USAGE</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.7.1.1.1"></a>
<code class="function">has_largeobject_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>largeobject</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for large object?
        Allowable privilege types are
        <code class="literal">SELECT</code> and <code class="literal">UPDATE</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.8.1.1.1"></a>
<code class="function">has_parameter_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>parameter</code></em> <code class="type">text</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for configuration parameter?
        The parameter name is case-insensitive.
        Allowable privilege types are <code class="literal">SET</code>
        and <code class="literal">ALTER SYSTEM</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.9.1.1.1"></a>
<code class="function">has_schema_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>schema</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for schema?
        Allowable privilege types are
        <code class="literal">CREATE</code> and
        <code class="literal">USAGE</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.10.1.1.1"></a>
<code class="function">has_sequence_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>sequence</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for sequence?
        Allowable privilege types are
        <code class="literal">USAGE</code>,
        <code class="literal">SELECT</code>, and
        <code class="literal">UPDATE</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.11.1.1.1"></a>
<code class="function">has_server_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>server</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for foreign server?
        The only allowable privilege type is <code class="literal">USAGE</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.12.1.1.1"></a>
<code class="function">has_table_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for table?
        Allowable privilege types
        are <code class="literal">SELECT</code>, <code class="literal">INSERT</code>,
        <code class="literal">UPDATE</code>, <code class="literal">DELETE</code>,
        <code class="literal">TRUNCATE</code>, <code class="literal">REFERENCES</code>,
        <code class="literal">TRIGGER</code>, and <code class="literal">MAINTAIN</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.13.1.1.1"></a>
<code class="function">has_tablespace_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>tablespace</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for tablespace?
        The only allowable privilege type is <code class="literal">CREATE</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.14.1.1.1"></a>
<code class="function">has_type_privilege</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>type</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for data type?
        The only allowable privilege type is <code class="literal">USAGE</code>.
        When specifying a type by name rather than by OID, the allowed input
        is the same as for the <code class="type">regtype</code> data type (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.15.1.1.1"></a>
<code class="function">pg_has_role</code> (
          [<span class="optional"> <em class="parameter"><code>user</code></em> <code class="type">name</code> or <code class="type">oid</code>, </span>]
          <em class="parameter"><code>role</code></em> <code class="type">text</code> or <code class="type">oid</code>,
          <em class="parameter"><code>privilege</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does user have privilege for role?
        Allowable privilege types are
        <code class="literal">MEMBER</code>, <code class="literal">USAGE</code>,
        and <code class="literal">SET</code>.
        <code class="literal">MEMBER</code> denotes direct or indirect membership in
        the role without regard to what specific privileges may be conferred.
        <code class="literal">USAGE</code> denotes whether the privileges of the role
        are immediately available without doing <code class="command">SET ROLE</code>,
        while <code class="literal">SET</code> denotes whether it is possible to change
        to the role using the <code class="literal">SET ROLE</code> command.
        <code class="literal">WITH ADMIN OPTION</code> or <code class="literal">WITH GRANT
        OPTION</code> can be added to any of these privilege types to
        test whether the <code class="literal">ADMIN</code> privilege is held (all
        six spellings test the same thing).
        This function does not allow the special case of
        setting <em class="parameter"><code>user</code></em> to <code class="literal">public</code>,
        because the PUBLIC pseudo-role can never be a member of real roles.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.4.2.2.16.1.1.1"></a>
<code class="function">row_security_active</code> (
          <em class="parameter"><code>table</code></em> <code class="type">text</code> or <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is row-level security active for the specified table in the context of
        the current user and current environment?
       </p></td></tr></tbody></table>

<br>

[Table 9.73](functions-info.md#FUNCTIONS-ACLITEM-OP-TABLE) shows the operators
available for the `aclitem` type, which is the catalog
representation of access privileges. See [Section 5.8](../ddl/ddl-priv.md)
for information about how to read access privilege values.

<a id="FUNCTIONS-ACLITEM-OP-TABLE"></a>

**Table 9.73. `aclitem` Operators**

<table border="1" class="table" summary="aclitem Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
         Operator
        </p>
<p>
         Description
        </p>
<p>
         Example(s)
        </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.6.2.2.1.1.1.1"></a>
<code class="type">aclitem</code> <code class="literal">=</code> <code class="type">aclitem</code>
         → <code class="returnvalue">boolean</code>
</p>
<p>
         Are <code class="type">aclitem</code>s equal?  (Notice that
         type <code class="type">aclitem</code> lacks the usual set of comparison
         operators; it has only equality.  In turn, <code class="type">aclitem</code>
         arrays can only be compared for equality.)
        </p>
<p>
<code class="literal">'calvin=r*w/hobbes'::aclitem = 'calvin=r*w*/hobbes'::aclitem</code>
         → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.6.2.2.2.1.1.1"></a>
<code class="type">aclitem[]</code> <code class="literal">@&gt;</code> <code class="type">aclitem</code>
         → <code class="returnvalue">boolean</code>
</p>
<p>
         Does array contain the specified privileges?  (This is true if there
         is an array entry that matches the <code class="type">aclitem</code>'s grantee and
         grantor, and has at least the specified set of privileges.)
        </p>
<p>
<code class="literal">'{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] @&gt; 'calvin=r*/hobbes'::aclitem</code>
         → <code class="returnvalue">t</code>
</p></td></tr></tbody></table>

<br>

[Table 9.74](functions-info.md#FUNCTIONS-ACLITEM-FN-TABLE) shows some additional
functions to manage the `aclitem` type.

<a id="FUNCTIONS-ACLITEM-FN-TABLE"></a>

**Table 9.74. `aclitem` Functions**

<table border="1" class="table" summary="aclitem Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.1.1.1.1"></a>
<code class="function">acldefault</code> (
          <em class="parameter"><code>type</code></em> <code class="type">"char"</code>,
          <em class="parameter"><code>ownerId</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">aclitem[]</code>
</p>
<p>
        Constructs an <code class="type">aclitem</code> array holding the default access
        privileges for an object of type <em class="parameter"><code>type</code></em> belonging
        to the role with OID <em class="parameter"><code>ownerId</code></em>.  This represents
        the access privileges that will be assumed when an object's
        <acronym class="acronym">ACL</acronym> entry is null. (The default access privileges
        are described in <a class="xref" href="../ddl/ddl-priv.md">Section 5.8</a>.)
        The <em class="parameter"><code>type</code></em> parameter must be one of
        'c' for <code class="literal">COLUMN</code>,
        'r' for <code class="literal">TABLE</code> and table-like objects,
        's' for <code class="literal">SEQUENCE</code>,
        'd' for <code class="literal">DATABASE</code>,
        'f' for <code class="literal">FUNCTION</code> or <code class="literal">PROCEDURE</code>,
        'l' for <code class="literal">LANGUAGE</code>,
        'L' for <code class="literal">LARGE OBJECT</code>,
        'n' for <code class="literal">SCHEMA</code>,
        'p' for <code class="literal">PARAMETER</code>,
        't' for <code class="literal">TABLESPACE</code>,
        'F' for <code class="literal">FOREIGN DATA WRAPPER</code>,
        'S' for <code class="literal">FOREIGN SERVER</code>,
        or
        'T' for <code class="literal">TYPE</code> or <code class="literal">DOMAIN</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.2.1.1.1"></a>
<code class="function">aclexplode</code> ( <code class="type">aclitem[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>grantor</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>grantee</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>privilege_type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>is_grantable</code></em> <code class="type">boolean</code> )
       </p>
<p>
        Returns the <code class="type">aclitem</code> array as a set of rows.
        If the grantee is the pseudo-role PUBLIC, it is represented by zero in
        the <em class="parameter"><code>grantee</code></em> column.  Each granted privilege is
        represented as <code class="literal">SELECT</code>, <code class="literal">INSERT</code>,
        etc (see <a class="xref" href="../ddl/ddl-priv.md#PRIVILEGE-ABBREVS-TABLE">Table 5.1</a> for a full list).
        Note that each privilege is broken out as a separate row, so
        only one keyword appears in the <em class="parameter"><code>privilege_type</code></em>
        column.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.4.8.2.2.3.1.1.1"></a>
<code class="function">makeaclitem</code> (
          <em class="parameter"><code>grantee</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>grantor</code></em> <code class="type">oid</code>,
          <em class="parameter"><code>privileges</code></em> <code class="type">text</code>,
          <em class="parameter"><code>is_grantable</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">aclitem</code>
</p>
<p>
        Constructs an <code class="type">aclitem</code> with the given properties.
        <em class="parameter"><code>privileges</code></em> is a comma-separated list of
        privilege names such as <code class="literal">SELECT</code>,
        <code class="literal">INSERT</code>, etc, all of which are set in the
        result.  (Case of the privilege string is not significant, and
        extra whitespace is allowed between but not within privilege
        names.)
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-SCHEMA"></a>

### 9.27.3. Schema Visibility Inquiry Functions [#](#FUNCTIONS-INFO-SCHEMA)

[Table 9.75](functions-info.md#FUNCTIONS-INFO-SCHEMA-TABLE) shows functions that
determine whether a certain object is *visible* in the
current schema search path.
For example, a table is said to be visible if its
containing schema is in the search path and no table of the same
name appears earlier in the search path. This is equivalent to the
statement that the table can be referenced by name without explicit
schema qualification. Thus, to list the names of all visible tables:

```

SELECT relname FROM pg_class WHERE pg_table_is_visible(oid);
```

For functions and operators, an object in the search path is said to be
visible if there is no object of the same name *and argument data
type(s)* earlier in the path. For operator classes and families,
both the name and the associated index access method are considered.

<a id="id-1.5.8.33.5.3"></a><a id="FUNCTIONS-INFO-SCHEMA-TABLE"></a>

**Table 9.75. Schema Visibility Inquiry Functions**

<table border="1" class="table" summary="Schema Visibility Inquiry Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.1.1.1.1"></a>
<code class="function">pg_collation_is_visible</code> ( <em class="parameter"><code>collation</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is collation visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.2.1.1.1"></a>
<code class="function">pg_conversion_is_visible</code> ( <em class="parameter"><code>conversion</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is conversion visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.3.1.1.1"></a>
<code class="function">pg_function_is_visible</code> ( <em class="parameter"><code>function</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is function visible in search path?
        (This also works for procedures and aggregates.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.4.1.1.1"></a>
<code class="function">pg_opclass_is_visible</code> ( <em class="parameter"><code>opclass</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is operator class visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.5.1.1.1"></a>
<code class="function">pg_operator_is_visible</code> ( <em class="parameter"><code>operator</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is operator visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.6.1.1.1"></a>
<code class="function">pg_opfamily_is_visible</code> ( <em class="parameter"><code>opclass</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is operator family visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.7.1.1.1"></a>
<code class="function">pg_statistics_obj_is_visible</code> ( <em class="parameter"><code>stat</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is statistics object visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.8.1.1.1"></a>
<code class="function">pg_table_is_visible</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is table visible in search path?
        (This works for all types of relations, including views, materialized
        views, indexes, sequences and foreign tables.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.9.1.1.1"></a>
<code class="function">pg_ts_config_is_visible</code> ( <em class="parameter"><code>config</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is text search configuration visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.10.1.1.1"></a>
<code class="function">pg_ts_dict_is_visible</code> ( <em class="parameter"><code>dict</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is text search dictionary visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.11.1.1.1"></a>
<code class="function">pg_ts_parser_is_visible</code> ( <em class="parameter"><code>parser</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is text search parser visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.12.1.1.1"></a>
<code class="function">pg_ts_template_is_visible</code> ( <em class="parameter"><code>template</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is text search template visible in search path?
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.5.4.2.2.13.1.1.1"></a>
<code class="function">pg_type_is_visible</code> ( <em class="parameter"><code>type</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is type (or domain) visible in search path?
       </p></td></tr></tbody></table>

<br>

All these functions require object OIDs to identify the object to be
checked. If you want to test an object by name, it is convenient to use
the OID alias types (`regclass`, `regtype`,
`regprocedure`, `regoperator`, `regconfig`,
or `regdictionary`),
for example:

```

SELECT pg_type_is_visible('myschema.widget'::regtype);
```

Note that it would not make much sense to test a non-schema-qualified
type name in this way — if the name can be recognized at all, it must be visible.

<a id="FUNCTIONS-INFO-CATALOG"></a>

### 9.27.4. System Catalog Information Functions [#](#FUNCTIONS-INFO-CATALOG)

[Table 9.76](functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE) lists functions that
extract information from the system catalogs.

<a id="FUNCTIONS-INFO-CATALOG-TABLE"></a>

**Table 9.76. System Catalog Information Functions**

<table border="1" class="table" summary="System Catalog Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry" id="FORMAT-TYPE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.1.1.1.1"></a>
<code class="function">format_type</code> ( <em class="parameter"><code>type</code></em> <code class="type">oid</code>, <em class="parameter"><code>typemod</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the SQL name for a data type that is identified by its type
        OID and possibly a type modifier.  Pass NULL for the type modifier if
        no specific modifier is known.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.2.1.1.1"></a>
<code class="function">pg_basetype</code> ( <code class="type">regtype</code> )
        → <code class="returnvalue">regtype</code>
</p>
<p>
        Returns the OID of the base type of a domain identified by its
        type OID.  If the argument is the OID of a non-domain type,
        returns the argument as-is.  Returns NULL if the argument is
        not a valid type OID.  If there's a chain of domain dependencies,
        it will recurse until finding the base type.
       </p>
<p>
        Assuming <code class="literal">CREATE DOMAIN mytext AS text</code>:
       </p>
<p>
<code class="literal">pg_basetype('mytext'::regtype)</code>
        → <code class="returnvalue">text</code>
</p></td></tr><tr><td class="func_table_entry" id="PG-CHAR-TO-ENCODING"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.3.1.1.1"></a>
<code class="function">pg_char_to_encoding</code> ( <em class="parameter"><code>encoding</code></em> <code class="type">name</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Converts the supplied encoding name into an integer representing the
        internal identifier used in some system catalog tables.
        Returns <code class="literal">-1</code> if an unknown encoding name is provided.
       </p></td></tr><tr><td class="func_table_entry" id="PG-ENCODING-TO-CHAR"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.4.1.1.1"></a>
<code class="function">pg_encoding_to_char</code> ( <em class="parameter"><code>encoding</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">name</code>
</p>
<p>
        Converts the integer used as the internal identifier of an encoding in some
        system catalog tables into a human-readable string.
        Returns an empty string if an invalid encoding number is provided.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.5.1.1.1"></a>
<code class="function">pg_get_catalog_foreign_keys</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>fktable</code></em> <code class="type">regclass</code>,
          <em class="parameter"><code>fkcols</code></em> <code class="type">text[]</code>,
          <em class="parameter"><code>pktable</code></em> <code class="type">regclass</code>,
          <em class="parameter"><code>pkcols</code></em> <code class="type">text[]</code>,
          <em class="parameter"><code>is_array</code></em> <code class="type">boolean</code>,
          <em class="parameter"><code>is_opt</code></em> <code class="type">boolean</code> )
       </p>
<p>
        Returns a set of records describing the foreign key relationships
        that exist within the <span class="productname">PostgreSQL</span> system
        catalogs.
        The <em class="parameter"><code>fktable</code></em> column contains the name of the
        referencing catalog, and the <em class="parameter"><code>fkcols</code></em> column
        contains the name(s) of the referencing column(s).  Similarly,
        the <em class="parameter"><code>pktable</code></em> column contains the name of the
        referenced catalog, and the <em class="parameter"><code>pkcols</code></em> column
        contains the name(s) of the referenced column(s).
        If <em class="parameter"><code>is_array</code></em> is true, the last referencing
        column is an array, each of whose elements should match some entry
        in the referenced catalog.
        If <em class="parameter"><code>is_opt</code></em> is true, the referencing column(s)
        are allowed to contain zeroes instead of a valid reference.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.6.1.1.1"></a>
<code class="function">pg_get_constraintdef</code> ( <em class="parameter"><code>constraint</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the creating command for a constraint.
        (This is a decompiled reconstruction, not the original text
        of the command.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.7.1.1.1"></a>
<code class="function">pg_get_expr</code> ( <em class="parameter"><code>expr</code></em> <code class="type">pg_node_tree</code>, <em class="parameter"><code>relation</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Decompiles the internal form of an expression stored in the system
        catalogs, such as the default value for a column.  If the expression
        might contain Vars, specify the OID of the relation they refer to as
        the second parameter; if no Vars are expected, passing zero is
        sufficient.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.8.1.1.1"></a>
<code class="function">pg_get_functiondef</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the creating command for a function or procedure.
        (This is a decompiled reconstruction, not the original text
        of the command.)
        The result is a complete <code class="command">CREATE OR REPLACE FUNCTION</code>
        or <code class="command">CREATE OR REPLACE PROCEDURE</code> statement.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.9.1.1.1"></a>
<code class="function">pg_get_function_arguments</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the argument list of a function or procedure, in the form
        it would need to appear in within <code class="command">CREATE FUNCTION</code>
        (including default values).
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.10.1.1.1"></a>
<code class="function">pg_get_function_identity_arguments</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the argument list necessary to identify a function or
        procedure, in the form it would need to appear in within commands such
        as <code class="command">ALTER FUNCTION</code>.  This form omits default values.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.11.1.1.1"></a>
<code class="function">pg_get_function_result</code> ( <em class="parameter"><code>func</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the <code class="literal">RETURNS</code> clause of a function, in
        the form it would need to appear in within <code class="command">CREATE
        FUNCTION</code>.  Returns <code class="literal">NULL</code> for a procedure.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.12.1.1.1"></a>
<code class="function">pg_get_indexdef</code> ( <em class="parameter"><code>index</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>column</code></em> <code class="type">integer</code>, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the creating command for an index.
        (This is a decompiled reconstruction, not the original text
        of the command.)  If <em class="parameter"><code>column</code></em> is supplied and is
        not zero, only the definition of that column is reconstructed.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.13.1.1.1"></a>
<code class="function">pg_get_keywords</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>word</code></em> <code class="type">text</code>,
        <em class="parameter"><code>catcode</code></em> <code class="type">"char"</code>,
        <em class="parameter"><code>barelabel</code></em> <code class="type">boolean</code>,
        <em class="parameter"><code>catdesc</code></em> <code class="type">text</code>,
        <em class="parameter"><code>baredesc</code></em> <code class="type">text</code> )
       </p>
<p>
        Returns a set of records describing the SQL keywords recognized by the
        server.  The <em class="parameter"><code>word</code></em> column contains the
        keyword.  The <em class="parameter"><code>catcode</code></em> column contains a
        category code: <code class="literal">U</code> for an unreserved
        keyword, <code class="literal">C</code> for a keyword that can be a column
        name, <code class="literal">T</code> for a keyword that can be a type or
        function name, or <code class="literal">R</code> for a fully reserved keyword.
        The <em class="parameter"><code>barelabel</code></em> column
        contains <code class="literal">true</code> if the keyword can be used as
        a <span class="quote">“<span class="quote">bare</span>”</span> column label in <code class="command">SELECT</code> lists,
        or <code class="literal">false</code> if it can only be used
        after <code class="literal">AS</code>.
        The <em class="parameter"><code>catdesc</code></em> column contains a
        possibly-localized string describing the keyword's category.
        The <em class="parameter"><code>baredesc</code></em> column contains a
        possibly-localized string describing the keyword's column label status.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.14.1.1.1"></a>
<code class="function">pg_get_partition_constraintdef</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the definition of a partition constraint.
        (This is a decompiled reconstruction, not the original text
        of the command.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.15.1.1.1"></a>
<code class="function">pg_get_partkeydef</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the definition of a partitioned table's partition
        key, in the form it would have in the <code class="literal">PARTITION
        BY</code> clause of <code class="command">CREATE TABLE</code>.
        (This is a decompiled reconstruction, not the original text
        of the command.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.16.1.1.1"></a>
<code class="function">pg_get_ruledef</code> ( <em class="parameter"><code>rule</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the creating command for a rule.
        (This is a decompiled reconstruction, not the original text
        of the command.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.17.1.1.1"></a>
<code class="function">pg_get_serial_sequence</code> ( <em class="parameter"><code>table</code></em> <code class="type">text</code>, <em class="parameter"><code>column</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the name of the sequence associated with a column,
        or NULL if no sequence is associated with the column.
        If the column is an identity column, the associated sequence is the
        sequence internally created for that column.
        For columns created using one of the serial types
        (<code class="type">serial</code>, <code class="type">smallserial</code>, <code class="type">bigserial</code>),
        it is the sequence created for that serial column definition.
        In the latter case, the association can be modified or removed
        with <code class="command">ALTER SEQUENCE OWNED BY</code>.
        (This function probably should have been
        called <code class="function">pg_get_owned_sequence</code>; its current name
        reflects the fact that it has historically been used with serial-type
        columns.)  The first parameter is a table name with optional
        schema, and the second parameter is a column name.  Because the first
        parameter potentially contains both schema and table names, it is
        parsed per usual SQL rules, meaning it is lower-cased by default.
        The second parameter, being just a column name, is treated literally
        and so has its case preserved.  The result is suitably formatted
        for passing to the sequence functions (see
        <a class="xref" href="functions-sequence.md">Section 9.17</a>).
       </p>
<p>
        A typical use is in reading the current value of the sequence for an
        identity or serial column, for example:
</p><pre class="programlisting">
SELECT currval(pg_get_serial_sequence('sometable', 'id'));
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.18.1.1.1"></a>
<code class="function">pg_get_statisticsobjdef</code> ( <em class="parameter"><code>statobj</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the creating command for an extended statistics object.
        (This is a decompiled reconstruction, not the original text
        of the command.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.19.1.1.1"></a>
<code class="function">pg_get_triggerdef</code> ( <em class="parameter"><code>trigger</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the creating command for a trigger.
        (This is a decompiled reconstruction, not the original text
        of the command.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.20.1.1.1"></a>
<code class="function">pg_get_userbyid</code> ( <em class="parameter"><code>role</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">name</code>
</p>
<p>
        Returns a role's name given its OID.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.21.1.1.1"></a>
<code class="function">pg_get_viewdef</code> ( <em class="parameter"><code>view</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the underlying <code class="command">SELECT</code> command for a
        view or materialized view.  (This is a decompiled reconstruction, not
        the original text of the command.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pg_get_viewdef</code> ( <em class="parameter"><code>view</code></em> <code class="type">oid</code>, <em class="parameter"><code>wrap_column</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the underlying <code class="command">SELECT</code> command for a
        view or materialized view.  (This is a decompiled reconstruction, not
        the original text of the command.)  In this form of the function,
        pretty-printing is always enabled, and long lines are wrapped to try
        to keep them shorter than the specified number of columns.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">pg_get_viewdef</code> ( <em class="parameter"><code>view</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>pretty</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reconstructs the underlying <code class="command">SELECT</code> command for a
        view or materialized view, working from a textual name for the view
        rather than its OID.  (This is deprecated; use the OID variant
        instead.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.24.1.1.1"></a>
<code class="function">pg_index_column_has_property</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>column</code></em> <code class="type">integer</code>, <em class="parameter"><code>property</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether an index column has the named property.
        Common index column properties are listed in
        <a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEX-COLUMN-PROPS">Table 9.77</a>.
        (Note that extension access methods can define additional property
        names for their indexes.)
        <code class="literal">NULL</code> is returned if the property name is not known
        or does not apply to the particular object, or if the OID or column
        number does not identify a valid object.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.25.1.1.1"></a>
<code class="function">pg_index_has_property</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>property</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether an index has the named property.
        Common index properties are listed in
        <a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEX-PROPS">Table 9.78</a>.
        (Note that extension access methods can define additional property
        names for their indexes.)
        <code class="literal">NULL</code> is returned if the property name is not known
        or does not apply to the particular object, or if the OID does not
        identify a valid object.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.26.1.1.1"></a>
<code class="function">pg_indexam_has_property</code> ( <em class="parameter"><code>am</code></em> <code class="type">oid</code>, <em class="parameter"><code>property</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether an index access method has the named property.
        Access method properties are listed in
        <a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEXAM-PROPS">Table 9.79</a>.
        <code class="literal">NULL</code> is returned if the property name is not known
        or does not apply to the particular object, or if the OID does not
        identify a valid object.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.27.1.1.1"></a>
<code class="function">pg_options_to_table</code> ( <em class="parameter"><code>options_array</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>option_name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>option_value</code></em> <code class="type">text</code> )
       </p>
<p>
        Returns the set of storage options represented by a value from
        <code class="structname">pg_class</code>.<code class="structfield">reloptions</code> or
        <code class="structname">pg_attribute</code>.<code class="structfield">attoptions</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.28.1.1.1"></a>
<code class="function">pg_settings_get_flags</code> ( <em class="parameter"><code>guc</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        Returns an array of the flags associated with the given GUC, or
        <code class="literal">NULL</code> if it does not exist. The result is
        an empty array if the GUC exists but there are no flags to show.
        Only the most useful flags listed in
        <a class="xref" href="functions-info.md#FUNCTIONS-PG-SETTINGS-FLAGS">Table 9.80</a> are exposed.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.29.1.1.1"></a>
<code class="function">pg_tablespace_databases</code> ( <em class="parameter"><code>tablespace</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">setof oid</code>
</p>
<p>
        Returns the set of OIDs of databases that have objects stored in the
        specified tablespace.  If this function returns any rows, the
        tablespace is not empty and cannot be dropped.  To identify the specific
        objects populating the tablespace, you will need to connect to the
        database(s) identified by <code class="function">pg_tablespace_databases</code>
        and query their <code class="structname">pg_class</code> catalogs.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.30.1.1.1"></a>
<code class="function">pg_tablespace_location</code> ( <em class="parameter"><code>tablespace</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the file system path that this tablespace is located in.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.31.1.1.1"></a>
<code class="function">pg_typeof</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">regtype</code>
</p>
<p>
        Returns the OID of the data type of the value that is passed to it.
        This can be helpful for troubleshooting or dynamically constructing
        SQL queries.  The function is declared as
        returning <code class="type">regtype</code>, which is an OID alias type (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); this means that it is the same as an
        OID for comparison purposes but displays as a type name.
       </p>
<p>
<code class="literal">pg_typeof(33)</code>
        → <code class="returnvalue">integer</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.32.1.1.1"></a>
<code class="function">COLLATION FOR</code> ( <code class="type">"any"</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the name of the collation of the value that is passed to it.
        The value is quoted and schema-qualified if necessary.  If no
        collation was derived for the argument expression,
        then <code class="literal">NULL</code> is returned.  If the argument is not of a
        collatable data type, then an error is raised.
       </p>
<p>
<code class="literal">collation for ('foo'::text)</code>
        → <code class="returnvalue">"default"</code>
</p>
<p>
<code class="literal">collation for ('foo' COLLATE "de_DE")</code>
        → <code class="returnvalue">"de_DE"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.33.1.1.1"></a>
<code class="function">to_regclass</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regclass</code>
</p>
<p>
        Translates a textual relation name to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regclass</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.34.1.1.1"></a>
<code class="function">to_regcollation</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regcollation</code>
</p>
<p>
        Translates a textual collation name to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regcollation</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.35.1.1.1"></a>
<code class="function">to_regnamespace</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regnamespace</code>
</p>
<p>
        Translates a textual schema name to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regnamespace</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.36.1.1.1"></a>
<code class="function">to_regoper</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regoper</code>
</p>
<p>
        Translates a textual operator name to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regoper</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found or is ambiguous.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.37.1.1.1"></a>
<code class="function">to_regoperator</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regoperator</code>
</p>
<p>
        Translates a textual operator name (with parameter types) to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regoperator</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.38.1.1.1"></a>
<code class="function">to_regproc</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regproc</code>
</p>
<p>
        Translates a textual function or procedure name to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regproc</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found or is ambiguous.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.39.1.1.1"></a>
<code class="function">to_regprocedure</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regprocedure</code>
</p>
<p>
        Translates a textual function or procedure name (with argument types) to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regprocedure</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.40.1.1.1"></a>
<code class="function">to_regrole</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regrole</code>
</p>
<p>
        Translates a textual role name to its OID.  A similar result is
        obtained by casting the string to type <code class="type">regrole</code> (see
        <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>); however, this function will return
        <code class="literal">NULL</code> rather than throwing an error if the name is
        not found.
       </p></td></tr><tr><td class="func_table_entry" id="TO-REGTYPE"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.41.1.1.1"></a>
<code class="function">to_regtype</code> ( <code class="type">text</code> )
        → <code class="returnvalue">regtype</code>
</p>
<p>
        Parses a string of text, extracts a potential type name from it,
        and translates that name into a type OID.  A syntax error in the
        string will result in an error; but if the string is a
        syntactically valid type name that happens not to be found in the
        catalogs, the result is <code class="literal">NULL</code>.  A similar result
        is obtained by casting the string to type <code class="type">regtype</code>
        (see <a class="xref" href="../datatype/datatype-oid.md">Section 8.19</a>), except that that will throw
        error for name not found.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.6.3.2.2.42.1.1.1"></a>
<code class="function">to_regtypemod</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Parses a string of text, extracts a potential type name from it,
        and translates its type modifier, if any.  A syntax error in the
        string will result in an error; but if the string is a
        syntactically valid type name that happens not to be found in the
        catalogs, the result is <code class="literal">NULL</code>.  The result is
        <code class="literal">-1</code> if no type modifier is present.
       </p>
<p>
<code class="function">to_regtypemod</code> can be combined with
        <a class="xref" href="functions-info.md#TO-REGTYPE">to_regtype</a> to produce appropriate inputs for
        <a class="xref" href="functions-info.md#FORMAT-TYPE">format_type</a>, allowing a string representing a
        type name to be canonicalized.
       </p>
<p>
<code class="literal">format_type(to_regtype('varchar(32)'), to_regtypemod('varchar(32)'))</code>
        → <code class="returnvalue">character varying(32)</code>
</p></td></tr></tbody></table>

<br>

Most of the functions that reconstruct (decompile) database objects
have an optional *`pretty`* flag, which
if `true` causes the result to
be “pretty-printed”. Pretty-printing suppresses unnecessary
parentheses and adds whitespace for legibility.
The pretty-printed format is more readable, but the default format
is more likely to be interpreted the same way by future versions of
PostgreSQL; so avoid using pretty-printed output
for dump purposes. Passing `false` for
the *`pretty`* parameter yields the same result as
omitting the parameter.

<a id="FUNCTIONS-INFO-INDEX-COLUMN-PROPS"></a>

**Table 9.77. Index Column Properties**

<table border="1" class="table" summary="Index Column Properties"><colgroup><col/><col/></colgroup><thead><tr><th>Name</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">asc</code></td><td>Does the column sort in ascending order on a forward scan?
      </td></tr><tr><td><code class="literal">desc</code></td><td>Does the column sort in descending order on a forward scan?
      </td></tr><tr><td><code class="literal">nulls_first</code></td><td>Does the column sort with nulls first on a forward scan?
      </td></tr><tr><td><code class="literal">nulls_last</code></td><td>Does the column sort with nulls last on a forward scan?
      </td></tr><tr><td><code class="literal">orderable</code></td><td>Does the column possess any defined sort ordering?
      </td></tr><tr><td><code class="literal">distance_orderable</code></td><td>Can the column be scanned in order by a <span class="quote">“<span class="quote">distance</span>”</span>
      operator, for example <code class="literal">ORDER BY col &lt;-&gt; constant</code> ?
      </td></tr><tr><td><code class="literal">returnable</code></td><td>Can the column value be returned by an index-only scan?
      </td></tr><tr><td><code class="literal">search_array</code></td><td>Does the column natively support <code class="literal">col = ANY(array)</code>
      searches?
      </td></tr><tr><td><code class="literal">search_nulls</code></td><td>Does the column support <code class="literal">IS NULL</code> and
      <code class="literal">IS NOT NULL</code> searches?
      </td></tr></tbody></table>

<br><a id="FUNCTIONS-INFO-INDEX-PROPS"></a>

**Table 9.78. Index Properties**

<table border="1" class="table" summary="Index Properties"><colgroup><col/><col/></colgroup><thead><tr><th>Name</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">clusterable</code></td><td>Can the index be used in a <code class="literal">CLUSTER</code> command?
      </td></tr><tr><td><code class="literal">index_scan</code></td><td>Does the index support plain (non-bitmap) scans?
      </td></tr><tr><td><code class="literal">bitmap_scan</code></td><td>Does the index support bitmap scans?
      </td></tr><tr><td><code class="literal">backward_scan</code></td><td>Can the scan direction be changed in mid-scan (to
             support <code class="literal">FETCH BACKWARD</code> on a cursor without
             needing materialization)?
      </td></tr></tbody></table>

<br><a id="FUNCTIONS-INFO-INDEXAM-PROPS"></a>

**Table 9.79. Index Access Method Properties**

<table border="1" class="table" summary="Index Access Method Properties"><colgroup><col/><col/></colgroup><thead><tr><th>Name</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">can_order</code></td><td>Does the access method support <code class="literal">ASC</code>,
      <code class="literal">DESC</code> and related keywords in
      <code class="literal">CREATE INDEX</code>?
      </td></tr><tr><td><code class="literal">can_unique</code></td><td>Does the access method support unique indexes?
      </td></tr><tr><td><code class="literal">can_multi_col</code></td><td>Does the access method support indexes with multiple columns?
      </td></tr><tr><td><code class="literal">can_exclude</code></td><td>Does the access method support exclusion constraints?
      </td></tr><tr><td><code class="literal">can_include</code></td><td>Does the access method support the <code class="literal">INCLUDE</code>
        clause of <code class="literal">CREATE INDEX</code>?
      </td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-SETTINGS-FLAGS"></a>

**Table 9.80. GUC Flags**

<table border="1" class="table" summary="GUC Flags"><colgroup><col/><col/></colgroup><thead><tr><th>Flag</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">EXPLAIN</code></td><td>Parameters with this flag are included in
       <code class="command">EXPLAIN (SETTINGS)</code> commands.
      </td></tr><tr><td><code class="literal">NO_SHOW_ALL</code></td><td>Parameters with this flag are excluded from
       <code class="command">SHOW ALL</code> commands.
      </td></tr><tr><td><code class="literal">NO_RESET</code></td><td>Parameters with this flag do not support
      <code class="command">RESET</code> commands.
      </td></tr><tr><td><code class="literal">NO_RESET_ALL</code></td><td>Parameters with this flag are excluded from
       <code class="command">RESET ALL</code> commands.
      </td></tr><tr><td><code class="literal">NOT_IN_SAMPLE</code></td><td>Parameters with this flag are not included in
       <code class="filename">postgresql.conf</code> by default.
      </td></tr><tr><td><code class="literal">RUNTIME_COMPUTED</code></td><td>Parameters with this flag are runtime-computed ones.
      </td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-OBJECT"></a>

### 9.27.5. Object Information and Addressing Functions [#](#FUNCTIONS-INFO-OBJECT)

[Table 9.81](functions-info.md#FUNCTIONS-INFO-OBJECT-TABLE) lists functions related to
database object identification and addressing.

<a id="FUNCTIONS-INFO-OBJECT-TABLE"></a>

**Table 9.81. Object Information and Addressing Functions**

<table border="1" class="table" summary="Object Information and Addressing Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.1.1.1.1"></a>
<code class="function">pg_get_acl</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">aclitem[]</code>
</p>
<p>
        Returns the <acronym class="acronym">ACL</acronym> for a database object, specified
        by catalog OID, object OID and sub-object ID. This function returns
        <code class="literal">NULL</code> values for undefined objects.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.2.1.1.1"></a>
<code class="function">pg_describe_object</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns a textual description of a database object identified by
        catalog OID, object OID, and sub-object ID (such as a column number
        within a table; the sub-object ID is zero when referring to a whole
        object).  This description is intended to be human-readable, and might
        be translated, depending on server configuration.  This is especially
        useful to determine the identity of an object referenced in the
        <code class="structname">pg_depend</code> catalog. This function returns
        <code class="literal">NULL</code> values for undefined objects.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.3.1.1.1"></a>
<code class="function">pg_identify_object</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>schema</code></em> <code class="type">text</code>,
        <em class="parameter"><code>name</code></em> <code class="type">text</code>,
        <em class="parameter"><code>identity</code></em> <code class="type">text</code> )
       </p>
<p>
        Returns a row containing enough information to uniquely identify the
        database object specified by catalog OID, object OID and sub-object
        ID.
        This information is intended to be machine-readable, and is never
        translated.
        <em class="parameter"><code>type</code></em> identifies the type of database object;
        <em class="parameter"><code>schema</code></em> is the schema name that the object
        belongs in, or <code class="literal">NULL</code> for object types that do not
        belong to schemas;
        <em class="parameter"><code>name</code></em> is the name of the object, quoted if
        necessary, if the name (along with schema name, if pertinent) is
        sufficient to uniquely identify the object,
        otherwise <code class="literal">NULL</code>;
        <em class="parameter"><code>identity</code></em> is the complete object identity, with
        the precise format depending on object type, and each name within the
        format being schema-qualified and quoted as necessary. Undefined
        objects are identified with <code class="literal">NULL</code> values.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.4.1.1.1"></a>
<code class="function">pg_identify_object_as_address</code> ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objid</code></em> <code class="type">oid</code>, <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>type</code></em> <code class="type">text</code>,
        <em class="parameter"><code>object_names</code></em> <code class="type">text[]</code>,
        <em class="parameter"><code>object_args</code></em> <code class="type">text[]</code> )
       </p>
<p>
        Returns a row containing enough information to uniquely identify the
        database object specified by catalog OID, object OID and sub-object
        ID.
        The returned information is independent of the current server, that
        is, it could be used to identify an identically named object in
        another server.
        <em class="parameter"><code>type</code></em> identifies the type of database object;
        <em class="parameter"><code>object_names</code></em> and
        <em class="parameter"><code>object_args</code></em>
        are text arrays that together form a reference to the object.
        These three values can be passed
        to <code class="function">pg_get_object_address</code> to obtain the internal
        address of the object.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.7.3.2.2.5.1.1.1"></a>
<code class="function">pg_get_object_address</code> ( <em class="parameter"><code>type</code></em> <code class="type">text</code>, <em class="parameter"><code>object_names</code></em> <code class="type">text[]</code>, <em class="parameter"><code>object_args</code></em> <code class="type">text[]</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>classid</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>objid</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>objsubid</code></em> <code class="type">integer</code> )
       </p>
<p>
        Returns a row containing enough information to uniquely identify the
        database object specified by a type code and object name and argument
        arrays.
        The returned values are the ones that would be used in system catalogs
        such as <code class="structname">pg_depend</code>; they can be passed to
        other system functions such as <code class="function">pg_describe_object</code>
        or <code class="function">pg_identify_object</code>.
        <em class="parameter"><code>classid</code></em> is the OID of the system catalog
        containing the object;
        <em class="parameter"><code>objid</code></em> is the OID of the object itself, and
        <em class="parameter"><code>objsubid</code></em> is the sub-object ID, or zero if none.
        This function is the inverse
        of <code class="function">pg_identify_object_as_address</code>.
        Undefined objects are identified with <code class="literal">NULL</code> values.
       </p></td></tr></tbody></table>

<br>

`pg_get_acl` is useful for retrieving and inspecting
the privileges associated with database objects without looking at
specific catalogs. For example, to retrieve all the granted privileges
on objects in the current database:

```

postgres=# SELECT
    (pg_identify_object(s.classid,s.objid,s.objsubid)).*,
    pg_catalog.pg_get_acl(s.classid,s.objid,s.objsubid) AS acl
FROM pg_catalog.pg_shdepend AS s
JOIN pg_catalog.pg_database AS d
    ON d.datname = current_database() AND
       d.oid = s.dbid
JOIN pg_catalog.pg_authid AS a
    ON a.oid = s.refobjid AND
       s.refclassid = 'pg_authid'::regclass
WHERE s.deptype = 'a';
-[ RECORD 1 ]-----------------------------------------
type     | table
schema   | public
name     | testtab
identity | public.testtab
acl      | {postgres=arwdDxtm/postgres,foo=r/postgres}
```

<a id="FUNCTIONS-INFO-COMMENT"></a>

### 9.27.6. Comment Information Functions [#](#FUNCTIONS-INFO-COMMENT)

<a id="id-1.5.8.33.8.2"></a>

The functions shown in [Table 9.82](functions-info.md#FUNCTIONS-INFO-COMMENT-TABLE)
extract comments previously stored with the [COMMENT](../../reference/sql-commands/sql-comment.md)
command. A null value is returned if no
comment could be found for the specified parameters.

<a id="FUNCTIONS-INFO-COMMENT-TABLE"></a>

**Table 9.82. Comment Information Functions**

<table border="1" class="table" summary="Comment Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.1.1.1.1"></a>
<code class="function">col_description</code> ( <em class="parameter"><code>table</code></em> <code class="type">oid</code>, <em class="parameter"><code>column</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the comment for a table column, which is specified by the OID
        of its table and its column number.
        (<code class="function">obj_description</code> cannot be used for table
        columns, since columns do not have OIDs of their own.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.2.1.1.1"></a>
<code class="function">obj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code>, <em class="parameter"><code>catalog</code></em> <code class="type">name</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the comment for a database object specified by its OID and the
        name of the containing system catalog.  For
        example, <code class="literal">obj_description(123456, 'pg_class')</code> would
        retrieve the comment for the table with OID 123456.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">obj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the comment for a database object specified by its OID alone.
        This is <span class="emphasis"><em>deprecated</em></span> since there is no guarantee
        that OIDs are unique across different system catalogs; therefore, the
        wrong comment might be returned.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.8.4.2.2.4.1.1.1"></a>
<code class="function">shobj_description</code> ( <em class="parameter"><code>object</code></em> <code class="type">oid</code>, <em class="parameter"><code>catalog</code></em> <code class="type">name</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the comment for a shared database object specified by its OID
        and the name of the containing system catalog.  This is just
        like <code class="function">obj_description</code> except that it is used for
        retrieving comments on shared objects (that is, databases, roles, and
        tablespaces).  Some system catalogs are global to all databases within
        each cluster, and the descriptions for objects in them are stored
        globally as well.
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-VALIDITY"></a>

### 9.27.7. Data Validity Checking Functions [#](#FUNCTIONS-INFO-VALIDITY)

The functions shown in [Table 9.83](functions-info.md#FUNCTIONS-INFO-VALIDITY-TABLE)
can be helpful for checking validity of proposed input data.

<a id="FUNCTIONS-INFO-VALIDITY-TABLE"></a>

**Table 9.83. Data Validity Checking Functions**

<table border="1" class="table" summary="Data Validity Checking Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.9.3.2.2.1.1.1.1"></a>
<code class="function">pg_input_is_valid</code> (
          <em class="parameter"><code>string</code></em> <code class="type">text</code>,
          <em class="parameter"><code>type</code></em> <code class="type">text</code>
        )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether the given <em class="parameter"><code>string</code></em> is valid
        input for the specified data type, returning true or false.
       </p>
<p>
        This function will only work as desired if the data type's input
        function has been updated to report invalid input as
        a <span class="quote">“<span class="quote">soft</span>”</span> error.  Otherwise, invalid input will abort
        the transaction, just as if the string had been cast to the type
        directly.
        </p>
<p>
<code class="literal">pg_input_is_valid('42', 'integer')</code>
         → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">pg_input_is_valid('42000000000', 'integer')</code>
         → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">pg_input_is_valid('1234.567', 'numeric(7,4)')</code>
         → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.9.3.2.2.2.1.1.1"></a>
<code class="function">pg_input_error_info</code> (
          <em class="parameter"><code>string</code></em> <code class="type">text</code>,
          <em class="parameter"><code>type</code></em> <code class="type">text</code>
        )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>message</code></em> <code class="type">text</code>,
        <em class="parameter"><code>detail</code></em> <code class="type">text</code>,
        <em class="parameter"><code>hint</code></em> <code class="type">text</code>,
        <em class="parameter"><code>sql_error_code</code></em> <code class="type">text</code> )
       </p>
<p>
        Tests whether the given <em class="parameter"><code>string</code></em> is valid
        input for the specified data type; if not, return the details of
        the error that would have been thrown.  If the input is valid, the
        results are NULL.  The inputs are the same as
        for <code class="function">pg_input_is_valid</code>.
       </p>
<p>
        This function will only work as desired if the data type's input
        function has been updated to report invalid input as
        a <span class="quote">“<span class="quote">soft</span>”</span> error.  Otherwise, invalid input will abort
        the transaction, just as if the string had been cast to the type
        directly.
       </p>
<p>
<code class="literal">SELECT * FROM pg_input_error_info('42000000000', 'integer')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
                       message                        | detail | hint | sql_error_code
------------------------------------------------------+--------+------+----------------
 value "42000000000" is out of range for type integer |        |      | 22003
</pre><p>
</p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-SNAPSHOT"></a>

### 9.27.8. Transaction ID and Snapshot Information Functions [#](#FUNCTIONS-INFO-SNAPSHOT)

The functions shown in [Table 9.84](functions-info.md#FUNCTIONS-PG-SNAPSHOT)
provide server transaction information in an exportable form. The main
use of these functions is to determine which transactions were committed
between two snapshots.

<a id="FUNCTIONS-PG-SNAPSHOT"></a>

**Table 9.84. Transaction ID and Snapshot Information Functions**

<table border="1" class="table" summary="Transaction ID and Snapshot Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.1.1.1.1"></a>
<code class="function">age</code>  ( <code class="type">xid</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the number of transactions between the supplied
        transaction id and the current transaction counter.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.2.1.1.1"></a>
<code class="function">mxid_age</code>  ( <code class="type">xid</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the number of multixacts IDs between the supplied
        multixact ID and the current multixacts counter.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.3.1.1.1"></a>
<code class="function">pg_current_xact_id</code> ()
        → <code class="returnvalue">xid8</code>
</p>
<p>
        Returns the current transaction's ID.  It will assign a new one if the
        current transaction does not have one already (because it has not
        performed any database updates);  see <a class="xref" href="../../internals/transactions/transaction-id.md">Section 67.1</a> for details.  If executed in a
        subtransaction, this will return the top-level transaction ID;
        see <a class="xref" href="../../internals/transactions/subxacts.md">Section 67.3</a> for details.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.4.1.1.1"></a>
<code class="function">pg_current_xact_id_if_assigned</code> ()
        → <code class="returnvalue">xid8</code>
</p>
<p>
        Returns the current transaction's ID, or <code class="literal">NULL</code> if no
        ID is assigned yet.  (It's best to use this variant if the transaction
        might otherwise be read-only, to avoid unnecessary consumption of an
        XID.)
        If executed in a subtransaction, this will return the top-level
        transaction ID.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.5.1.1.1"></a>
<code class="function">pg_xact_status</code> ( <code class="type">xid8</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Reports the commit status of a recent transaction.
        The result is one of <code class="literal">in progress</code>,
        <code class="literal">committed</code>, or <code class="literal">aborted</code>,
        provided that the transaction is recent enough that the system retains
        the commit status of that transaction.
        If it is old enough that no references to the transaction survive in
        the system and the commit status information has been discarded, the
        result is <code class="literal">NULL</code>.
        Applications might use this function, for example, to determine
        whether their transaction committed or aborted after the application
        and database server become disconnected while
        a <code class="literal">COMMIT</code> is in progress.
        Note that prepared transactions are reported as <code class="literal">in
        progress</code>; applications must check <a class="link" href="../../internals/views/view-pg-prepared-xacts.md"><code class="structname">pg_prepared_xacts</code></a>
        if they need to determine whether a transaction ID belongs to a
        prepared transaction.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.6.1.1.1"></a>
<code class="function">pg_current_snapshot</code> ()
        → <code class="returnvalue">pg_snapshot</code>
</p>
<p>
        Returns a current <em class="firstterm">snapshot</em>, a data structure
        showing which transaction IDs are now in-progress.
        Only top-level transaction IDs are included in the snapshot;
        subtransaction IDs are not shown;  see <a class="xref" href="../../internals/transactions/subxacts.md">Section 67.3</a>
        for details.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.7.1.1.1"></a>
<code class="function">pg_snapshot_xip</code> ( <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">setof xid8</code>
</p>
<p>
        Returns the set of in-progress transaction IDs contained in a snapshot.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.8.1.1.1"></a>
<code class="function">pg_snapshot_xmax</code> ( <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">xid8</code>
</p>
<p>
        Returns the <code class="structfield">xmax</code> of a snapshot.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.9.1.1.1"></a>
<code class="function">pg_snapshot_xmin</code> ( <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">xid8</code>
</p>
<p>
        Returns the <code class="structfield">xmin</code> of a snapshot.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.10.1.1.1"></a>
<code class="function">pg_visible_in_snapshot</code> ( <code class="type">xid8</code>, <code class="type">pg_snapshot</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is the given transaction ID <em class="firstterm">visible</em> according
        to this snapshot (that is, was it completed before the snapshot was
        taken)?  Note that this function will not give the correct answer for
        a subtransaction ID (subxid);  see <a class="xref" href="../../internals/transactions/subxacts.md">Section 67.3</a> for
        details.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.3.2.2.11.1.1.1"></a>
<code class="function">pg_get_multixact_members</code> ( <em class="parameter"><code>multixid</code></em> <code class="type">xid</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>mode</code></em> <code class="type">text</code> )
       </p>
<p>
        Returns the transaction ID and lock mode for each member of the
        specified multixact ID.  The lock modes <code class="literal">forupd</code>,
        <code class="literal">fornokeyupd</code>, <code class="literal">sh</code>, and
        <code class="literal">keysh</code> correspond to the row-level locks
        <code class="literal">FOR UPDATE</code>, <code class="literal">FOR NO KEY UPDATE</code>,
        <code class="literal">FOR SHARE</code>, and <code class="literal">FOR KEY SHARE</code>,
        respectively, as described in <a class="xref" href="../mvcc/explicit-locking.md#LOCKING-ROWS">Section 13.3.2</a>.  Two
        additional modes are specific to multixacts:
        <code class="literal">nokeyupd</code>, used by updates that do not modify key
        columns, and <code class="literal">upd</code>, used by updates or deletes that
        modify key columns.
       </p></td></tr></tbody></table>

<br>

The internal transaction ID type `xid` is 32 bits wide and
wraps around every 4 billion transactions. However,
the functions shown in [Table 9.84](functions-info.md#FUNCTIONS-PG-SNAPSHOT), except
`age`, `mxid_age`, and
`pg_get_multixact_members`, use a
64-bit type `xid8` that does not wrap around during the life
of an installation and can be converted to `xid` by casting if
required; see [Section 67.1](../../internals/transactions/transaction-id.md) for details.
The data type `pg_snapshot` stores information about
transaction ID visibility at a particular moment in time. Its components
are described in [Table 9.85](functions-info.md#FUNCTIONS-PG-SNAPSHOT-PARTS).
`pg_snapshot`'s textual representation is
`xmin:xmax:xip_list`.
For example `10:20:10,14,15` means
`xmin=10, xmax=20, xip_list=10, 14, 15`.

<a id="FUNCTIONS-PG-SNAPSHOT-PARTS"></a>

**Table 9.85. Snapshot Components**

<table border="1" class="table" summary="Snapshot Components"><colgroup><col/><col/></colgroup><thead><tr><th>Name</th><th>Description</th></tr></thead><tbody><tr><td><code class="structfield">xmin</code></td><td>
         Lowest transaction ID that was still active.  All transaction IDs
         less than <code class="structfield">xmin</code> are either committed and visible,
         or rolled back and dead.
       </td></tr><tr><td><code class="structfield">xmax</code></td><td>
         One past the highest completed transaction ID.  All transaction IDs
         greater than or equal to <code class="structfield">xmax</code> had not yet
         completed as of the time of the snapshot, and thus are invisible.
       </td></tr><tr><td><code class="structfield">xip_list</code></td><td>
        Transactions in progress at the time of the snapshot.  A transaction
        ID that is <code class="literal">xmin &lt;= <em class="replaceable"><code>X</code></em> &lt;
        xmax</code> and not in this list was already completed at the time
        of the snapshot, and thus is either visible or dead according to its
        commit status.  This list does not include the transaction IDs of
        subtransactions (subxids).
       </td></tr></tbody></table>

<br>

In releases of PostgreSQL before 13 there was
no `xid8` type, so variants of these functions were provided
that used `bigint` to represent a 64-bit XID, with a
correspondingly distinct snapshot data type `txid_snapshot`.
These older functions have `txid` in their names. They
are still supported for backward compatibility, but may be removed from a
future release. See [Table 9.86](functions-info.md#FUNCTIONS-TXID-SNAPSHOT).

<a id="FUNCTIONS-TXID-SNAPSHOT"></a>

**Table 9.86. Deprecated Transaction ID and Snapshot Information Functions**

<table border="1" class="table" summary="Deprecated Transaction ID and Snapshot Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.1.1.1.1"></a>
<code class="function">txid_current</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_current_xact_id()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.2.1.1.1"></a>
<code class="function">txid_current_if_assigned</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_current_xact_id_if_assigned()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.3.1.1.1"></a>
<code class="function">txid_current_snapshot</code> ()
        → <code class="returnvalue">txid_snapshot</code>
</p>
<p>
        See <code class="function">pg_current_snapshot()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.4.1.1.1"></a>
<code class="function">txid_snapshot_xip</code> ( <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">setof bigint</code>
</p>
<p>
        See <code class="function">pg_snapshot_xip()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.5.1.1.1"></a>
<code class="function">txid_snapshot_xmax</code> ( <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_snapshot_xmax()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.6.1.1.1"></a>
<code class="function">txid_snapshot_xmin</code> ( <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        See <code class="function">pg_snapshot_xmin()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.7.1.1.1"></a>
<code class="function">txid_visible_in_snapshot</code> ( <code class="type">bigint</code>, <code class="type">txid_snapshot</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        See <code class="function">pg_visible_in_snapshot()</code>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.10.7.2.2.8.1.1.1"></a>
<code class="function">txid_status</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        See <code class="function">pg_xact_status()</code>.
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-COMMIT-TIMESTAMP"></a>

### 9.27.9. Committed Transaction Information Functions [#](#FUNCTIONS-INFO-COMMIT-TIMESTAMP)

The functions shown in [Table 9.87](functions-info.md#FUNCTIONS-COMMIT-TIMESTAMP)
provide information about when past transactions were committed.
They only provide useful data when the
[track_commit_timestamp](../../server-administration/runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) configuration option is
enabled, and only for transactions that were committed after it was
enabled. Commit timestamp information is routinely removed during
vacuum.

<a id="FUNCTIONS-COMMIT-TIMESTAMP"></a>

**Table 9.87. Committed Transaction Information Functions**

<table border="1" class="table" summary="Committed Transaction Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.1.1.1.1"></a>
<code class="function">pg_xact_commit_timestamp</code> ( <code class="type">xid</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Returns the commit timestamp of a transaction.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.2.1.1.1"></a>
<code class="function">pg_xact_commit_timestamp_origin</code> ( <code class="type">xid</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>timestamp</code></em> <code class="type">timestamp with time zone</code>,
         <em class="parameter"><code>roident</code></em> <code class="type">oid</code>)
       </p>
<p>
         Returns the commit timestamp and replication origin of a transaction.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.3.1.1.1"></a>
<code class="function">pg_last_committed_xact</code> ()
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>timestamp</code></em> <code class="type">timestamp with time zone</code>,
        <em class="parameter"><code>roident</code></em> <code class="type">oid</code> )
       </p>
<p>
        Returns the transaction ID, commit timestamp and replication origin
        of the latest committed transaction.
       </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-CONTROLDATA"></a>

### 9.27.10. Control Data Functions [#](#FUNCTIONS-INFO-CONTROLDATA)

The functions shown in [Table 9.88](functions-info.md#FUNCTIONS-CONTROLDATA)
print information initialized during `initdb`, such
as the catalog version. They also show information about write-ahead
logging and checkpoint processing. This information is cluster-wide,
not specific to any one database. These functions provide most of the same
information, from the same source, as the
[pg_controldata](../../reference/reference-server/app-pgcontroldata.md) application.

<a id="FUNCTIONS-CONTROLDATA"></a>

**Table 9.88. Control Data Functions**

<table border="1" class="table" summary="Control Data Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.1.1.1.1"></a>
<code class="function">pg_control_checkpoint</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        Returns information about current checkpoint state, as shown in
        <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-CHECKPOINT">Table 9.89</a>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.2.1.1.1"></a>
<code class="function">pg_control_system</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        Returns information about current control file state, as shown in
        <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-SYSTEM">Table 9.90</a>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.3.1.1.1"></a>
<code class="function">pg_control_init</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        Returns information about cluster initialization state, as shown in
        <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-INIT">Table 9.91</a>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.12.3.2.2.4.1.1.1"></a>
<code class="function">pg_control_recovery</code> ()
        → <code class="returnvalue">record</code>
</p>
<p>
        Returns information about recovery state, as shown in
        <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-RECOVERY">Table 9.92</a>.
       </p></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-CHECKPOINT"></a>

**Table 9.89. `pg_control_checkpoint` Output Columns**

<table border="1" class="table" summary="pg_control_checkpoint Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>Column Name</th><th>Data Type</th></tr></thead><tbody><tr><td><code class="structfield">checkpoint_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">redo_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">redo_wal_file</code></td><td><code class="type">text</code></td></tr><tr><td><code class="structfield">timeline_id</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">prev_timeline_id</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">full_page_writes</code></td><td><code class="type">boolean</code></td></tr><tr><td><code class="structfield">next_xid</code></td><td><code class="type">text</code></td></tr><tr><td><code class="structfield">next_oid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">next_multixact_id</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">next_multi_offset</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_xid_dbid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">oldest_active_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_multi_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">oldest_multi_dbid</code></td><td><code class="type">oid</code></td></tr><tr><td><code class="structfield">oldest_commit_ts_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">newest_commit_ts_xid</code></td><td><code class="type">xid</code></td></tr><tr><td><code class="structfield">checkpoint_time</code></td><td><code class="type">timestamp with time zone</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-SYSTEM"></a>

**Table 9.90. `pg_control_system` Output Columns**

<table border="1" class="table" summary="pg_control_system Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>Column Name</th><th>Data Type</th></tr></thead><tbody><tr><td><code class="structfield">pg_control_version</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">catalog_version_no</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">system_identifier</code></td><td><code class="type">bigint</code></td></tr><tr><td><code class="structfield">pg_control_last_modified</code></td><td><code class="type">timestamp with time zone</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-INIT"></a>

**Table 9.91. `pg_control_init` Output Columns**

<table border="1" class="table" summary="pg_control_init Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>Column Name</th><th>Data Type</th></tr></thead><tbody><tr><td><code class="structfield">max_data_alignment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">database_block_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">blocks_per_segment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">wal_block_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">bytes_per_wal_segment</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_identifier_length</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_index_columns</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">max_toast_chunk_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">large_object_chunk_size</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">float8_pass_by_value</code></td><td><code class="type">boolean</code></td></tr><tr><td><code class="structfield">data_page_checksum_version</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">default_char_signedness</code></td><td><code class="type">boolean</code></td></tr></tbody></table>

<br><a id="FUNCTIONS-PG-CONTROL-RECOVERY"></a>

**Table 9.92. `pg_control_recovery` Output Columns**

<table border="1" class="table" summary="pg_control_recovery Output Columns"><colgroup><col/><col/></colgroup><thead><tr><th>Column Name</th><th>Data Type</th></tr></thead><tbody><tr><td><code class="structfield">min_recovery_end_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">min_recovery_end_timeline</code></td><td><code class="type">integer</code></td></tr><tr><td><code class="structfield">backup_start_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">backup_end_lsn</code></td><td><code class="type">pg_lsn</code></td></tr><tr><td><code class="structfield">end_of_backup_record_required</code></td><td><code class="type">boolean</code></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-VERSION"></a>

### 9.27.11. Version Information Functions [#](#FUNCTIONS-INFO-VERSION)

The functions shown in [Table 9.93](functions-info.md#FUNCTIONS-VERSION)
print version information.

<a id="FUNCTIONS-VERSION"></a>

**Table 9.93. Version Information Functions**

<table border="1" class="table" summary="Version Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.1.1.1.1"></a>
<code class="function">version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns a string describing the <span class="productname">PostgreSQL</span>
        server's version.  You can also get this information from
        <a class="xref" href="../../server-administration/runtime-config/runtime-config-preset.md#GUC-SERVER-VERSION">server_version</a>, or for a machine-readable
        version use <a class="xref" href="../../server-administration/runtime-config/runtime-config-preset.md#GUC-SERVER-VERSION-NUM">server_version_num</a>.  Software
        developers should use <code class="varname">server_version_num</code> (available
        since 8.2) or <a class="xref" href="../../client-interfaces/libpq/libpq-status.md#LIBPQ-PQSERVERVERSION"><code class="function">PQserverVersion</code></a> instead of
        parsing the text version.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.2.1.1.1"></a>
<code class="function">unicode_version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns a string representing the version of Unicode used by
        <span class="productname">PostgreSQL</span>.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.13.3.2.2.3.1.1.1"></a>
<code class="function">icu_unicode_version</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns a string representing the version of Unicode used by ICU, if
        the server was built with ICU support; otherwise returns
        <code class="literal">NULL</code> </p></td></tr></tbody></table>

<br>

<a id="FUNCTIONS-INFO-WAL-SUMMARY"></a>

### 9.27.12. WAL Summarization Information Functions [#](#FUNCTIONS-INFO-WAL-SUMMARY)

The functions shown in [Table 9.94](functions-info.md#FUNCTIONS-WAL-SUMMARY)
print information about the status of WAL summarization.
See [summarize_wal](../../server-administration/runtime-config/runtime-config-wal.md#GUC-SUMMARIZE-WAL).

<a id="FUNCTIONS-WAL-SUMMARY"></a>

**Table 9.94. WAL Summarization Information Functions**

<table border="1" class="table" summary="WAL Summarization Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.14.3.2.2.1.1.1.1"></a>
<code class="function">pg_available_wal_summaries</code> ()
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>tli</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>start_lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>end_lsn</code></em> <code class="type">pg_lsn</code> )
       </p>
<p>
        Returns information about the WAL summary files present in the
        data directory, under <code class="literal">pg_wal/summaries</code>.
        One row will be returned per WAL summary file. Each file summarizes
        WAL on the indicated TLI within the indicated LSN range. This function
        might be useful to determine whether enough WAL summaries are present
        on the server to take an incremental backup based on some prior
        backup whose start LSN is known.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.14.3.2.2.2.1.1.1"></a>
<code class="function">pg_wal_summary_contents</code> ( <em class="parameter"><code>tli</code></em> <code class="type">bigint</code>, <em class="parameter"><code>start_lsn</code></em> <code class="type">pg_lsn</code>, <em class="parameter"><code>end_lsn</code></em> <code class="type">pg_lsn</code> )
        → <code class="returnvalue">setof record</code>
        ( <em class="parameter"><code>relfilenode</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>reltablespace</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>reldatabase</code></em> <code class="type">oid</code>,
        <em class="parameter"><code>relforknumber</code></em> <code class="type">smallint</code>,
        <em class="parameter"><code>relblocknumber</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>is_limit_block</code></em> <code class="type">boolean</code> )
       </p>
<p>
        Returns one information about the contents of a single WAL summary file
        identified by TLI and starting and ending LSNs. Each row with
        <code class="literal">is_limit_block</code> false indicates that the block
        identified by the remaining output columns was modified by at least
        one WAL record within the range of records summarized by this file.
        Each row with <code class="literal">is_limit_block</code> true indicates either
        that (a) the relation fork was truncated to the length given by
        <code class="literal">relblocknumber</code> within the relevant range of WAL
        records or (b) that the relation fork was created or dropped within
        the relevant range of WAL records; in such cases,
        <code class="literal">relblocknumber</code> will be zero.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.14.3.2.2.3.1.1.1"></a>
<code class="function">pg_get_wal_summarizer_state</code> ()
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>summarized_tli</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>summarized_lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>pending_lsn</code></em> <code class="type">pg_lsn</code>,
        <em class="parameter"><code>summarizer_pid</code></em> <code class="type">int</code> )
       </p>
<p>
        Returns information about the progress of the WAL summarizer. If the
        WAL summarizer has never run since the instance was started, then
        <code class="literal">summarized_tli</code> and <code class="literal">summarized_lsn</code>
        will be <code class="literal">0</code> and <code class="literal">0/0</code> respectively;
        otherwise, they will be the TLI and ending LSN of the last WAL summary
        file written to disk. If the WAL summarizer is currently running,
        <code class="literal">pending_lsn</code> will be the ending LSN of the last
        record that it has consumed, which must always be greater than or
        equal to <code class="literal">summarized_lsn</code>; if the WAL summarizer is
        not running, it will be equal to <code class="literal">summarized_lsn</code>.
        <code class="literal">summarizer_pid</code> is the PID of the WAL summarizer
        process, if it is running, and otherwise NULL.
       </p>
<p>
        As a special exception, the WAL summarizer will refuse to generate
        WAL summary files if run on WAL generated under
        <code class="literal">wal_level=minimal</code>, since such summaries would be
        unsafe to use as the basis for an incremental backup. In this case,
        the fields above will continue to advance as if summaries were being
        generated, but nothing will be written to disk. Once the summarizer
        reaches WAL generated while <code class="literal">wal_level</code> was set
        to <code class="literal">replica</code> or higher, it will resume writing
        summaries to disk.
       </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（英文原文，待翻譯）
