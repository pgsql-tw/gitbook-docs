# pg\_ctl

pg\_ctl — initialize, start, stop, or control a PostgreSQL server

### 語法

`pg_ctl` `init[db]` \[`-D` _`datadir`_] \[`-s`] \[`-o` _`initdb-options`_]

`pg_ctl` `start` \[`-D` _`datadir`_] \[`-l` _`filename`_] \[`-W`] \[`-t` _`seconds`_] \[`-s`] \[`-o` _`options`_] \[`-p` _`path`_] \[`-c`]

`pg_ctl` `stop` \[`-D` _`datadir`_] \[`-m` `s[mart]` | `f[ast]` | `i[mmediate]` ] \[`-W`] \[`-t` _`seconds`_] \[`-s`]

`pg_ctl` `restart` \[`-D` _`datadir`_] \[`-m` `s[mart]` | `f[ast]` | `i[mmediate]` ] \[`-W`] \[`-t` _`seconds`_] \[`-s`] \[`-o` _`options`_] \[`-c`]

`pg_ctl` `reload` \[`-D` _`datadir`_] \[`-s`]

`pg_ctl` `status` \[`-D` _`datadir`_]

`pg_ctl` `promote` \[`-D` _`datadir`_] \[`-W`] \[`-t` _`seconds`_] \[`-s`]

`pg_ctl` `logrotate` \[`-D` _`datadir`_] \[`-s`]

`pg_ctl` `kill` _`signal_name`_ _`process_id`_

On Microsoft Windows, also:

`pg_ctl` `register` \[`-D` _`datadir`_] \[`-N` _`servicename`_] \[`-U` _`username`_] \[`-P` _`password`_] \[`-S` `a[uto]` | `d[emand]` ] \[`-e` _`source`_] \[`-W`] \[`-t` _`seconds`_] \[`-s`] \[`-o` _`options`_]

`pg_ctl` `unregister` \[`-N` _`servicename`_]

### 說明

pg\_ctl 是一個工具程式用於初始化 PostgreSQL 資料庫叢集，啟動、停止或重新啟動 PostgreSQL 資料庫伺服器（[postgres](postgres.md)）或顯示正在執行中的伺服器狀態。儘管可以手動啟動伺服器，但是 pg\_ctl 封裝了諸如重導向日誌輸出以及與終端和程序群組正確分離之類的任務。它還提供了方便的選項以進行可管理的關機程序。

init 或 initdb 模式將建立一個新的 PostgreSQL 資料庫叢集，也就是將由單一個伺服器實例管理的資料庫集合。此模式會呼叫 initdb 指令。有關詳細資訊，請參閱 [initdb](initdb.md)。

`start` mode launches a new server. The server is started in the background, and its standard input is attached to `/dev/null` (or `nul` on Windows). On Unix-like systems, by default, the server's standard output and standard error are sent to pg\_ctl's standard output (not standard error). The standard output of pg\_ctl should then be redirected to a file or piped to another process such as a log rotating program like rotatelogs; otherwise `postgres` will write its output to the controlling terminal (from the background) and will not leave the shell's process group. On Windows, by default the server's standard output and standard error are sent to the terminal. These default behaviors can be changed by using `-l` to append the server's output to a log file. Use of either `-l` or output redirection is recommended.

`stop` mode shuts down the server that is running in the specified data directory. Three different shutdown methods can be selected with the `-m` option. “Smart” mode disallows new connections, then waits for all existing clients to disconnect and any online backup to finish. If the server is in hot standby, recovery and streaming replication will be terminated once all clients have disconnected. “Fast” mode (the default) does not wait for clients to disconnect and will terminate an online backup in progress. All active transactions are rolled back and clients are forcibly disconnected, then the server is shut down. “Immediate” mode will abort all server processes immediately, without a clean shutdown. This choice will lead to a crash-recovery cycle during the next server start.

`restart` mode effectively executes a stop followed by a start. This allows changing the `postgres` command-line options, or changing configuration-file options that cannot be changed without restarting the server. If relative paths were used on the command line during server start, `restart` might fail unless pg\_ctl is executed in the same current directory as it was during server start.

`reload` mode simply sends the `postgres` server process a SIGHUP signal, causing it to reread its configuration files (`postgresql.conf`, `pg_hba.conf`, etc.). This allows changing configuration-file options that do not require a full server restart to take effect.

`status` mode checks whether a server is running in the specified data directory. If it is, the server's PID and the command line options that were used to invoke it are displayed. If the server is not running, pg\_ctl returns an exit status of 3. If an accessible data directory is not specified, pg\_ctl returns an exit status of 4.

`promote` mode commands the standby server that is running in the specified data directory to end standby mode and begin read-write operations.

`logrotate` mode rotates the server log file. For details on how to use this mode with external log rotation tools, see [Section 24.3](https://www.postgresql.org/docs/13/logfile-maintenance.html).

`kill` mode sends a signal to a specified process. This is primarily valuable on Microsoft Windows which does not have a built-in kill command. Use `--help` to see a list of supported signal names.

`register` mode registers the PostgreSQL server as a system service on Microsoft Windows. The `-S` option allows selection of service start type, either “auto” (start service automatically on system startup) or “demand” (start service on demand).

`unregister` mode unregisters a system service on Microsoft Windows. This undoes the effects of the `register` command.

### Options

`-c`\
`--core-files`

Attempt to allow server crashes to produce core files, on platforms where this is possible, by lifting any soft resource limit placed on core files. This is useful in debugging or diagnosing problems by allowing a stack trace to be obtained from a failed server process.

`-D`` `_`datadir`_\
`--pgdata=`_`datadir`_

Specifies the file system location of the database configuration files. If this option is omitted, the environment variable `PGDATA` is used.

`-l`` `_`filename`_\
`--log=`_`filename`_

Append the server log output to _`filename`_. If the file does not exist, it is created. The umask is set to 077, so access to the log file is disallowed to other users by default.

`-m`` `_`mode`_\
`--mode=`_`mode`_

Specifies the shutdown mode. _`mode`_ can be `smart`, `fast`, or `immediate`, or the first letter of one of these three. If this option is omitted, `fast` is the default.

`-o`` `_`options`_\
`--options=`_`options`_

Specifies options to be passed directly to the `postgres` command. `-o` can be specified multiple times, with all the given options being passed through.

The _`options`_ should usually be surrounded by single or double quotes to ensure that they are passed through as a group.

`-o`` `_`initdb-options`_\
`--options=`_`initdb-options`_

Specifies options to be passed directly to the `initdb` command. `-o` can be specified multiple times, with all the given options being passed through.

The _`initdb-options`_ should usually be surrounded by single or double quotes to ensure that they are passed through as a group.

`-p`` `_`path`_

Specifies the location of the `postgres` executable. By default the `postgres` executable is taken from the same directory as `pg_ctl`, or failing that, the hard-wired installation directory. It is not necessary to use this option unless you are doing something unusual and get errors that the `postgres` executable was not found.

In `init` mode, this option analogously specifies the location of the `initdb` executable.

`-s`\
`--silent`

Print only errors, no informational messages.

`-t`` `_`seconds`_\
`--timeout=`_`seconds`_

Specifies the maximum number of seconds to wait when waiting for an operation to complete (see option `-w`). Defaults to the value of the `PGCTLTIMEOUT` environment variable or, if not set, to 60 seconds.

`-V`\
`--version`

Print the pg\_ctl version and exit.

`-w`\
`--wait`

Wait for the operation to complete. This is supported for the modes `start`, `stop`, `restart`, `promote`, and `register`, and is the default for those modes.

When waiting, `pg_ctl` repeatedly checks the server's PID file, sleeping for a short amount of time between checks. Startup is considered complete when the PID file indicates that the server is ready to accept connections. Shutdown is considered complete when the server removes the PID file. `pg_ctl` returns an exit code based on the success of the startup or shutdown.

If the operation does not complete within the timeout (see option `-t`), then `pg_ctl` exits with a nonzero exit status. But note that the operation might continue in the background and eventually succeed.

`-W`\
`--no-wait`

Do not wait for the operation to complete. This is the opposite of the option `-w`.

If waiting is disabled, the requested action is triggered, but there is no feedback about its success. In that case, the server log file or an external monitoring system would have to be used to check the progress and success of the operation.

In prior releases of PostgreSQL, this was the default except for the `stop` mode.

`-?`\
`--help`

Show help about pg\_ctl command line arguments, and exit.

If an option is specified that is valid, but not relevant to the selected operating mode, pg\_ctl ignores it.

#### Options for Windows

`-e`` `_`source`_

Name of the event source for pg\_ctl to use for logging to the event log when running as a Windows service. The default is `PostgreSQL`. Note that this only controls messages sent from pg\_ctl itself; once started, the server will use the event source specified by its [event\_source](https://www.postgresql.org/docs/13/runtime-config-logging.html#GUC-EVENT-SOURCE) parameter. Should the server fail very early in startup, before that parameter has been set, it might also log using the default event source name `PostgreSQL`.

`-N`` `_`servicename`_

Name of the system service to register. This name will be used as both the service name and the display name. The default is `PostgreSQL`.

`-P`` `_`password`_

Password for the user to run the service as.

`-S`` `_`start-type`_

Start type of the system service. _`start-type`_ can be `auto`, or `demand`, or the first letter of one of these two. If this option is omitted, `auto` is the default.

`-U`` `_`username`_

User name for the user to run the service as. For domain users, use the format `DOMAIN\username`.

### Environment

`PGCTLTIMEOUT`

Default limit on the number of seconds to wait when waiting for startup or shutdown to complete. If not set, the default is 60 seconds.

`PGDATA`

Default data directory location.

Most `pg_ctl` modes require knowing the data directory location; therefore, the `-D` option is required unless `PGDATA` is set.

`pg_ctl`, like most other PostgreSQL utilities, also uses the environment variables supported by libpq (see [Section 33.14](https://www.postgresql.org/docs/13/libpq-envars.html)).

For additional variables that affect the server, see [postgres](https://www.postgresql.org/docs/13/app-postgres.html).

### Files

`postmaster.pid`

pg\_ctl examines this file in the data directory to determine whether the server is currently running.

`postmaster.opts`

If this file exists in the data directory, pg\_ctl (in `restart` mode) will pass the contents of the file as options to postgres, unless overridden by the `-o` option. The contents of this file are also displayed in `status` mode.

### Examples

#### Starting the Server

To start the server, waiting until the server is accepting connections:

```
$ pg_ctl start
```

To start the server using port 5433, and running without `fsync`, use:

```
$ pg_ctl -o "-F -p 5433" start
```

#### Stopping the Server

To stop the server, use:

```
$ pg_ctl stop
```

The `-m` option allows control over _how_ the server shuts down:

```
$ pg_ctl stop -m smart
```

#### Restarting the Server

Restarting the server is almost equivalent to stopping the server and starting it again, except that by default, `pg_ctl` saves and reuses the command line options that were passed to the previously-running instance. To restart the server using the same options as before, use:

```
$ pg_ctl restart
```

But if `-o` is specified, that replaces any previous options. To restart using port 5433, disabling `fsync` upon restart:

```
$ pg_ctl -o "-F -p 5433" restart
```

#### Showing the Server Status

Here is sample status output from pg\_ctl:

```
$ pg_ctl status

pg_ctl: server is running (PID: 13718)
/usr/local/pgsql/bin/postgres "-D" "/usr/local/pgsql/data" "-p" "5433" "-B" "128"
```

The second line is the command that would be invoked in restart mode.

### 參閱

[initdb](initdb.md), [postgres](postgres.md)