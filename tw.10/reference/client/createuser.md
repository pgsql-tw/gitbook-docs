# createuser

createuser — define a new PostgreSQL user account

### Synopsis

`createuser` \[_`connection-option`_...\] \[_`option`_...\] \[_`username`_\]

### Description

createuser creates a new PostgreSQL user \(or more precisely, a role\). Only superusers and users with `CREATEROLE` privilege can create new users, so createuser must be invoked by someone who can connect as a superuser or a user with `CREATEROLE` privilege.

If you wish to create a new superuser, you must connect as a superuser, not merely with `CREATEROLE` privilege. Being a superuser implies the ability to bypass all access permission checks within the database, so superuserdom should not be granted lightly.

createuser is a wrapper around the SQL command [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html). There is no effective difference between creating users via this utility and via other methods for accessing the server.

### Options

createuser accepts the following command-line arguments:_`username`_

Specifies the name of the PostgreSQL user to be created. This name must be different from all existing roles in this PostgreSQL installation.`-c `_`number`_  
`--connection-limit=`_`number`_

Set a maximum number of connections for the new user. The default is to set no limit.`-d`  
`--createdb`

The new user will be allowed to create databases.`-D`  
`--no-createdb`

The new user will not be allowed to create databases. This is the default.`-e`  
`--echo`

Echo the commands that createuser generates and sends to the server.`-E`  
`--encrypted`

This option is obsolete but still accepted for backward compatibility.`-g `_`role`_  
`--role=`_`role`_

Indicates role to which this role will be added immediately as a new member. Multiple roles to which this role will be added as a member can be specified by writing multiple `-g` switches.`-i`  
`--inherit`

The new role will automatically inherit privileges of roles it is a member of. This is the default.`-I`  
`--no-inherit`

The new role will not automatically inherit privileges of roles it is a member of.`--interactive`

Prompt for the user name if none is specified on the command line, and also prompt for whichever of the options `-d`/`-D`, `-r`/`-R`, `-s`/`-S` is not specified on the command line. \(This was the default behavior up to PostgreSQL 9.1.\)`-l`  
`--login`

The new user will be allowed to log in \(that is, the user name can be used as the initial session user identifier\). This is the default.`-L`  
`--no-login`

The new user will not be allowed to log in. \(A role without login privilege is still useful as a means of managing database permissions.\)`-P`  
`--pwprompt`

If given, createuser will issue a prompt for the password of the new user. This is not necessary if you do not plan on using password authentication.`-r`  
`--createrole`

The new user will be allowed to create new roles \(that is, this user will have `CREATEROLE` privilege\).`-R`  
`--no-createrole`

The new user will not be allowed to create new roles. This is the default.`-s`  
`--superuser`

The new user will be a superuser.`-S`  
`--no-superuser`

The new user will not be a superuser. This is the default.`-V`  
`--version`

Print the createuser version and exit.`--replication`

The new user will have the `REPLICATION` privilege, which is described more fully in the documentation for [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html).`--no-replication`

The new user will not have the `REPLICATION` privilege, which is described more fully in the documentation for [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html).`-?`  
`--help`

Show help about createuser command line arguments, and exit.

createuser also accepts the following command-line arguments for connection parameters:`-h `_`host`_  
`--host=`_`host`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.`-p `_`port`_  
`--port=`_`port`_

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections.`-U `_`username`_  
`--username=`_`username`_

User name to connect as \(not the user name to create\).`-w`  
`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.`-W`  
`--password`

Force createuser to prompt for a password \(for connecting to the server, not for the password of the new user\).

This option is never essential, since createuser will automatically prompt for a password if the server demands password authentication. However, createuser will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

### Environment

`PGHOST`  
`PGPORT`  
`PGUSER`

Default connection parameters

This utility, like most other PostgreSQL utilities, also uses the environment variables supported by libpq \(see [Section 33.14](https://www.postgresql.org/docs/10/static/libpq-envars.html)\).

### Diagnostics

In case of difficulty, see [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html) and [psql](https://www.postgresql.org/docs/10/static/app-psql.html) for discussions of potential problems and error messages. The database server must be running at the targeted host. Also, any default connection settings and environment variables used by the libpq front-end library will apply.

### Examples

To create a user `joe` on the default database server:

```text
$ createuser joe
```

To create a user `joe` on the default database server with prompting for some additional attributes:

```text
$ createuser --interactive joe
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

To create the same user `joe` using the server on host `eden`, port 5000, with attributes explicitly specified, taking a look at the underlying command:

```text
$ createuser -h eden -p 5000 -S -D -R -e joe
CREATE ROLE joe NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
```

To create the user `joe` as a superuser, and assign a password immediately:

```text
$ createuser -P -s -e joe
Enter password for new role: xyzzy
Enter it again: xyzzy
CREATE ROLE joe PASSWORD 'md5b5f5ba1a423792b526f799ae4eb3d59e' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;
```

In the above example, the new password isn't actually echoed when typed, but we show what was typed for clarity. As you see, the password is encrypted before it is sent to the client.

### See Also

[dropuser](https://www.postgresql.org/docs/10/static/app-dropuser.html), [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html)

