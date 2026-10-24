<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET"></a>

## *`connection_target`* [#](#ecpg-sql-connect-connection-target) <a href="#ecpg-sql-connect-connection-target" id="ecpg-sql-connect-connection-target"></a>

*`connection_target`*
指定連線的目標伺服器，可採用下列幾種形式之一。

<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-DATABASE-NAME"></a>

### [ *`database_name`* ] [ `@`*`host`* ] [ `:`*`port`* ] [#](#ecpg-sql-connect-connection-target-database-name) <a href="#ecpg-sql-connect-connection-target-database-name" id="ecpg-sql-connect-connection-target-database-name"></a>

透過 TCP/IP 連線

<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-UNIX-DOMAIN-SOCKETS"></a>

### `unix:postgresql://`*`host`* [ `:`*`port`* ] `/` [ *`database_name`* ] [ `?`*`connection_option`* ] [#](#ecpg-sql-connect-connection-target-unix-domain-sockets) <a href="#ecpg-sql-connect-connection-target-unix-domain-sockets" id="ecpg-sql-connect-connection-target-unix-domain-sockets"></a>

透過 Unix 網域通訊端連線

<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-TCP-IP"></a>

### `tcp:postgresql://`*`host`* [ `:`*`port`* ] `/` [ *`database_name`* ] [ `?`*`connection_option`* ] [#](#ecpg-sql-connect-connection-target-tcp-ip) <a href="#ecpg-sql-connect-connection-target-tcp-ip" id="ecpg-sql-connect-connection-target-tcp-ip"></a>

透過 TCP/IP 連線

<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-CONSTANT"></a>

### SQL 字串常數 [#](#ecpg-sql-connect-connection-target-constant) <a href="#ecpg-sql-connect-connection-target-constant" id="ecpg-sql-connect-connection-target-constant"></a>

內容為上述任一形式的值

<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET-HOST-VARIABLE"></a>

### 主機變數 [#](#ecpg-sql-connect-connection-target-host-variable) <a href="#ecpg-sql-connect-connection-target-host-variable" id="ecpg-sql-connect-connection-target-host-variable"></a>

型別為 `char[]` 或 `VARCHAR[]`、內容為上述任一形式之值的主機變數

[返回 CONNECT](ecpg-sql-connect.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-connect.html)（原文版本：18.6；核對日期：2026-10-18）
