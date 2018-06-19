---
description: 版本：10
---

# dropuser

dropuser — 移除 PostgreSQL 使用者帳戶

### 語法

`dropuser` \[_`connection-option`_...\] \[_`option`_...\] \[_`username`_\]

### 說明

dropuser 移除現有的 PostgreSQL 使用者。只有具有 CREATEROLE 權限的超級使用者或一般使用者才能移除 PostgreSQL 使用者。（但要移除超級使用者，您還必須自己是超級使用者。）

dropuser 是 SQL 指令 [DROP ROLE](../sql-commands/drop-role.md) 的一個封裝。透過此實用工具和透過存取伺服器的其他方法移除使用者，之間沒有區別。

### Options

dropuser accepts the following command-line arguments:

_`username`_

Specifies the name of the PostgreSQL user to be removed. You will be prompted for a name if none is specified on the command line and the `-i`/`--interactive` option is used.

`-e`  
`--echo`

Echo the commands that dropuser generates and sends to the server.

`-i`  
`--interactive`

Prompt for confirmation before actually removing the user, and prompt for the user name if none is specified on the command line.

`-V`  
`--version`

Print the dropuser version and exit.

`--if-exists`

Do not throw an error if the user does not exist. A notice is issued in this case.

`-?`  
`--help`

Show help about dropuser command line arguments, and exit.

dropuser also accepts the following command-line arguments for connection parameters:

`-h` _`host`_  
`--host=`_`host`_

Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.

`-p` _`port`_  
`--port=`_`port`_

Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections.

`-U` _`username`_  
`--username=`_`username`_

User name to connect as \(not the user name to drop\).

`-w`  
`--no-password`

Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.

`-W`  
`--password`

Force dropuser to prompt for a password before connecting to a database.

This option is never essential, since dropuser will automatically prompt for a password if the server demands password authentication. However, dropuser will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W`to avoid the extra connection attempt.

### 環境變數

`PGHOST`  
`PGPORT`  
`PGUSER`

預設連線參數

與其他大多數 PostgreSQL 實用工具一樣，此工具也使用 libpq 支援的環境變數（請參閱[第 33.14 節](../../client-interfaces/libpq-c-library/33.14.-environment-variables.md)）。

### 診斷

如果遇到困難，請參閱 [DROP ROLE](../sql-commands/drop-role.md) 和 [psql](psql.md)，以便討論潛在問題和錯誤訊息。資料庫伺服器必須在目標主機上運行。此外，libpq 前端函式庫使用的任何預設連線設定和環境變數都將適用。

### 範例

要從預設資料庫伺服器中移除使用者 joe：

```text
$ dropuser joe
```

使用主機 eden 的連接埠 5000 上的服務移除使用者 joe，驗證並查看基礎指令：

```text
$ dropuser -p 5000 -h eden -i -e joe
Role "joe" will be permanently removed.
Are you sure? (y/n) y
DROP ROLE joe;
```

### 參閱

[createuser](createuser.md), [DROP ROLE](../sql-commands/drop-role.md)

