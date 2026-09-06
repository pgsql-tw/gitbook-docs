## 53.25. `pg_settings` [#](#VIEW-PG-SETTINGS)

<a id="id-1.10.5.29.2"></a>

The view `pg_settings` provides access to
run-time parameters of the server. It is essentially an alternative
interface to the [`SHOW`](../../reference/sql-commands/sql-show.md)
and [`SET`](../../reference/sql-commands/sql-set.md) commands.
It also provides access to some facts about each parameter that are
not directly available from [`SHOW`](../../reference/sql-commands/sql-show.md), such as minimum and
maximum values.

<a id="id-1.10.5.29.4"></a>

**Table 53.25. `pg_settings` Columns**

<table border="1" class="table" summary="pg_settings Columns"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       Column Type
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       Run-time configuration parameter name
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">setting</code> <code class="type">text</code>
</p>
<p>
       Current value of the parameter
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">unit</code> <code class="type">text</code>
</p>
<p>
       Implicit unit of the parameter
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">category</code> <code class="type">text</code>
</p>
<p>
       Logical group of the parameter
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">short_desc</code> <code class="type">text</code>
</p>
<p>
       A brief description of the parameter
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extra_desc</code> <code class="type">text</code>
</p>
<p>
       Additional, more detailed, description of the parameter
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">context</code> <code class="type">text</code>
</p>
<p>
       Context required to set the parameter's value (see below)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">vartype</code> <code class="type">text</code>
</p>
<p>
       Parameter type (<code class="literal">bool</code>, <code class="literal">enum</code>,
       <code class="literal">integer</code>, <code class="literal">real</code>, or <code class="literal">string</code>)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">source</code> <code class="type">text</code>
</p>
<p>
       Source of the current parameter value
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_val</code> <code class="type">text</code>
</p>
<p>
       Minimum allowed value of the parameter (null for non-numeric
       values)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_val</code> <code class="type">text</code>
</p>
<p>
       Maximum allowed value of the parameter (null for non-numeric
       values)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">enumvals</code> <code class="type">text[]</code>
</p>
<p>
       Allowed values of an enum parameter (null for non-enum
       values)
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">boot_val</code> <code class="type">text</code>
</p>
<p>
       Parameter value assumed at server startup if the parameter is
       not otherwise set
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reset_val</code> <code class="type">text</code>
</p>
<p>
       Value that <a class="link" href="../../reference/sql-commands/sql-reset.md"><code class="command">RESET</code></a> would reset the parameter to
       in the current session
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sourcefile</code> <code class="type">text</code>
</p>
<p>
       Configuration file the current value was set in (null for
       values set from sources other than configuration files, or when
       examined by a user who neither is a superuser nor has privileges of
       <code class="literal">pg_read_all_settings</code>); helpful when using
       <code class="literal">include</code> directives in configuration files
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sourceline</code> <code class="type">int4</code>
</p>
<p>
       Line number within the configuration file the current value was
       set at (null for values set from sources other than configuration files,
       or when examined by a user who neither is a superuser nor has privileges of
       <code class="literal">pg_read_all_settings</code>).
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pending_restart</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> if the value has been changed in the
       configuration file but needs a restart; or <code class="literal">false</code>
       otherwise.
      </p></td></tr></tbody></table>

<br>

There are several possible values of `context`.
In order of decreasing difficulty of changing the setting, they are:

`internal`
:   These settings cannot be changed directly; they reflect internally
    determined values. Some of them may be adjustable by rebuilding the
    server with different configuration options, or by changing options
    supplied to initdb.

`postmaster`
:   These settings can only be applied when the server starts, so any change
    requires restarting the server. Values for these settings are typically
    stored in the `postgresql.conf` file, or passed on
    the command line when starting the server. Of course, settings with any
    of the lower `context` types can also be
    set at server start time.

`sighup`
:   Changes to these settings can be made in
    `postgresql.conf` without restarting the server.
    Send a SIGHUP signal to the postmaster to
    cause it to re-read `postgresql.conf` and apply
    the changes. The postmaster will also forward the
    SIGHUP signal to its child processes so that
    they all pick up the new value.

`superuser-backend`
:   Changes to these settings can be made in
    `postgresql.conf` without restarting the server.
    They can also be set for a particular session in the connection request
    packet (for example, via libpq's `PGOPTIONS`
    environment variable), but only if the connecting user is a superuser
    or has been granted the appropriate `SET` privilege.
    However, these settings never change in a session after it is started.
    If you change them in `postgresql.conf`, send a
    SIGHUP signal to the postmaster to cause it to
    re-read `postgresql.conf`. The new values will only
    affect subsequently-launched sessions.

`backend`
:   Changes to these settings can be made in
    `postgresql.conf` without restarting the server.
    They can also be set for a particular session in the connection request
    packet (for example, via libpq's `PGOPTIONS`
    environment variable); any user can make such a change for their session.
    However, these settings never change in a session after it is started.
    If you change them in `postgresql.conf`, send a
    SIGHUP signal to the postmaster to cause it to
    re-read `postgresql.conf`. The new values will only
    affect subsequently-launched sessions.

`superuser`
:   These settings can be set from `postgresql.conf`,
    or within a session via the `SET` command; but only superusers
    and users with the appropriate `SET` privilege
    can change them via `SET`. Changes in
    `postgresql.conf` will affect existing sessions
    only if no session-local value has been established with `SET`.

`user`
:   These settings can be set from `postgresql.conf`,
    or within a session via the `SET` command. Any user is
    allowed to change their session-local value. Changes in
    `postgresql.conf` will affect existing sessions
    only if no session-local value has been established with `SET`.

See [Section 19.1](../../server-administration/runtime-config/config-setting.md) for more information about the various
ways to change these parameters.

This view cannot be inserted into or deleted from, but it can be updated. An
`UPDATE` applied to a row of `pg_settings`
is equivalent to executing the `SET` command on that named
parameter. The change only affects the value used by the current
session. If an `UPDATE` is issued within a transaction
that is later aborted, the effects of the `UPDATE` command
disappear when the transaction is rolled back. Once the surrounding
transaction is committed, the effects will persist until the end of the
session, unless overridden by another `UPDATE` or
`SET`.

This view does not
display [customized options](../../server-administration/runtime-config/runtime-config-custom.md)
unless the extension module that defines them has been loaded by the
backend process executing the query (e.g., via a mention in
[shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES),
a call to a C function in the extension, or the
[`LOAD`](../../reference/sql-commands/sql-load.md) command).
For example, since [archive modules](../../server-programming/archive-modules/README.md)
are normally loaded only by the archiver process not regular sessions,
this view will not display any customized options defined by such modules
unless special action is taken to load them into the backend process
executing the query.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-settings.html)（英文原文，待翻譯）
