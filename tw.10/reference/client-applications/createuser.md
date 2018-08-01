---
description: 版本：10
---

# createuser

createuser — 定義一個新的 PostgreSQL 使用者帳戶

### 語法

`createuser` \[_`connection-option`_...\] \[_`option`_...\] \[_`username`_\]

### 說明

createuser 建立一個新的 PostgreSQL 使用者（或更確切地說，一個角色）。只有具有 CREATEROLE 權限使用者或超級使用者才能建立新的使用者，因此必須由可以作為超級用戶或具有 CREATEROLE 權限的使用者進行連線使用 createuser。

如果要建立新的超級使用者，則必須以超級使用者身份進行連線，而不僅僅是擁有 CREATEROLE 權限。作為超級使用者意味著能夠繞過資料庫中的所有存取權限檢查，因此不應輕易授予超級使用者權限。

createuser 是 SQL 指令 CREATE ROLE 封裝的工具。透過此實用工具建立使用者和透過其他方法存取伺服器之間沒有任何區別。

### 選項

createuser accepts the following command-line arguments:

_`username`_

Specifies the name of the PostgreSQL user to be created. This name must be different from all existing roles in this PostgreSQL installation.

`-c` _`number`_  
`--connection-limit=`_`number`_

Set a maximum number of connections for the new user. The default is to set no limit.

`-d`  
`--createdb`

The new user will be allowed to create databases.

`-D`  
`--no-createdb`

The new user will not be allowed to create databases. This is the default.

`-e`  
`--echo`

Echo the commands that createuser generates and sends to the server.

`-E`  
`--encrypted`

This option is obsolete but still accepted for backward compatibility.

`-g` _`role`_  
`--role=`_`role`_

Indicates role to which this role will be added immediately as a new member. Multiple roles to which this role will be added as a member can be specified by writing multiple `-g` switches.

`-i`  
`--inherit`

The new role will automatically inherit privileges of roles it is a member of. This is the default.

`-I`  
`--no-inherit`

The new role will not automatically inherit privileges of roles it is a member of.

`--interactive`

Prompt for the user name if none is specified on the command line, and also prompt for whichever of the options `-d`/`-D`, `-r`/`-R`, `-s`/`-S` is not specified on the command line. \(This was the default behavior up to PostgreSQL 9.1.\)

`-l`  
`--login`

The new user will be allowed to log in \(that is, the user name can be used as the initial session user identifier\). This is the default.

`-L`  
`--no-login`

The new user will not be allowed to log in. \(A role without login privilege is still useful as a means of managing database permissions.\)

`-P`  
`--pwprompt`

If given, createuser will issue a prompt for the password of the new user. This is not necessary if you do not plan on using password authentication.

`-r`  
`--createrole`

The new user will be allowed to create new roles \(that is, this user will have `CREATEROLE` privilege\).

`-R`  
`--no-createrole`

The new user will not be allowed to create new roles. This is the default.

`-s`  
`--superuser`

The new user will be a superuser.

`-S`  
`--no-superuser`

The new user will not be a superuser. This is the default.

`-V`  
`--version`

Print the createuser version and exit.

`--replication`

The new user will have the `REPLICATION` privilege, which is described more fully in the documentation for [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html).

`--no-replication`

The new user will not have the `REPLICATION` privilege, which is described more fully in the documentation for [CREATE ROLE](https://www.postgresql.org/docs/10/static/sql-createrole.html).

`-?`  
`--help`

Show help about createuser command line arguments, and exit.

createuser also accepts the following command-line arguments for connection parameters:

`-h` _`host`_  
`--host=`_`host`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.

`-p` _`port`_  
`--port=`_`port`_

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections.

`-U` _`username`_  
`--username=`_`username`_

User name to connect as \(not the user name to create\).

`-w`  
`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`  
`--password`

Force createuser to prompt for a password \(for connecting to the server, not for the password of the new user\).

This option is never essential, since createuser will automatically prompt for a password if the server demands password authentication. However, createuser will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.

### 環境變數

`PGHOST`  
`PGPORT`  
`PGUSER`

預設連線參數

與大多數其他 PostgreSQL 工具程式一樣，此工具也使用 libpq 支援的環境變數（請參閱[第 33.14 節](../../client-interfaces/libpq-c-library/environment-variables.md)）。

### 例外

如果遇到困難，請參閱 CREATE ROLE 和 psql 以討論潛在問題和錯誤訊息。資料庫伺服器必須在目標主機上運行。此外，將套用 libpq 前端函式庫使用的任何預鉆水連線設定和環境變數。

### 範例

要在預設的資料庫伺服器上建立使用者 joe：

```text
$ createuser joe
```

要在預設的資料庫伺服器上建立使用者 joe，並提示輸入一些其他的屬性：

```text
$ createuser --interactive joe
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

要使用主機 eden 上的伺服器（連接埠 5000）建立相同的使用者 joe，並明確指定屬性，屬性請查看基礎指令：

```text
$ createuser -h eden -p 5000 -S -D -R -e joe
CREATE ROLE joe NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
```

要以超級使用者身份建立使用者 joe，並立即指定密碼：

```text
$ createuser -P -s -e joe
Enter password for new role: xyzzy
Enter it again: xyzzy
CREATE ROLE joe PASSWORD 'md5b5f5ba1a423792b526f799ae4eb3d59e' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;
```

在上面的範例中，新密碼在鍵入時實際上並未顯示，但為了清楚起見，我們顯示了鍵入的內容。如您所見，密碼在發送到用戶端之前已經加密過。

### 參閱

[dropuser](dropuser.md), [CREATE ROLE](../sql-commands/create-role.md)

