<a id="ECPG-SQL-CONNECT"></a>

## CONNECT

CONNECT — 建立資料庫連線

## 語法

```

CONNECT TO connection_target [ AS connection_name ] [ USER connection_user ]
CONNECT TO DEFAULT
CONNECT connection_user
DATABASE connection_target
```

<a id="id-1.7.5.20.4.3"></a>

## 說明

`CONNECT` 命令會在用戶端與 PostgreSQL 伺服器之間建立連線。

<a id="id-1.7.5.20.4.4"></a>

## 參數

<a id="ECPG-SQL-CONNECT-CONNECTION-TARGET"></a>

### *`connection_target`* [#](#ecpg-sql-connect-connection-target) <a href="#ecpg-sql-connect-connection-target" id="ecpg-sql-connect-connection-target"></a>

本參數請參閱[*`connection_target`*](ecpg-sql-connect-target.md#ecpg-sql-connect-connection-target)。

<a id="ECPG-SQL-CONNECT-CONNECTION-NAME"></a>

### *`connection_name`* [#](#ecpg-sql-connect-connection-name) <a href="#ecpg-sql-connect-connection-name" id="ecpg-sql-connect-connection-name"></a>

連線的選用識別字，讓其他命令可以參照此連線。可以是 SQL 識別字或主機變數。

<a id="ECPG-SQL-CONNECT-CONNECTION-USER"></a>

### *`connection_user`* [#](#ecpg-sql-connect-connection-user) <a href="#ecpg-sql-connect-connection-user" id="ecpg-sql-connect-connection-user"></a>

資料庫連線的使用者名稱。

此參數也可以同時指定使用者名稱與密碼，使用下列形式之一：`user_name/password`、`user_name IDENTIFIED BY password` 或 `user_name USING password`。

使用者名稱與密碼可以是 SQL 識別字、字串常數或主機變數。

<a id="ECPG-SQL-CONNECT-DEFAULT"></a>

### `DEFAULT` [#](#ecpg-sql-connect-default) <a href="#ecpg-sql-connect-default" id="ecpg-sql-connect-default"></a>

使用 libpq 所定義的所有預設連線參數。

<a id="id-1.7.5.20.4.5"></a>

## 範例

以下是指定連線參數的幾種不同寫法：

```

EXEC SQL CONNECT TO "connectdb" AS main;
EXEC SQL CONNECT TO "connectdb" AS second;
EXEC SQL CONNECT TO "unix:postgresql://200.46.204.71/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO "unix:postgresql://localhost/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO 'connectdb' AS main;
EXEC SQL CONNECT TO 'unix:postgresql://localhost/connectdb' AS main USER :user;
EXEC SQL CONNECT TO :db AS :id;
EXEC SQL CONNECT TO :db USER connectuser USING :pw;
EXEC SQL CONNECT TO @localhost AS main USER connectdb;
EXEC SQL CONNECT TO REGRESSDB1 as main;
EXEC SQL CONNECT TO AS main USER connectdb;
EXEC SQL CONNECT TO connectdb AS :id;
EXEC SQL CONNECT TO connectdb AS main USER connectuser/connectdb;
EXEC SQL CONNECT TO connectdb AS main;
EXEC SQL CONNECT TO connectdb@localhost AS main;
EXEC SQL CONNECT TO tcp:postgresql://localhost/ USER connectdb;
EXEC SQL CONNECT TO tcp:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO tcp:postgresql://localhost:20/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO unix:postgresql://localhost/ AS main USER connectdb;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb AS main USER connectuser;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser USING "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb?connect_timeout=14 USER connectuser;
```

以下範例程式示範如何使用主機變數指定連線參數：

```

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    char *dbname     = "testdb";    /* database name */
    char *user       = "testuser";  /* connection user name */
    char *connection = "tcp:postgresql://localhost:5432/testdb";
                                    /* connection string */
    char ver[256];                  /* buffer to store the version string */
EXEC SQL END DECLARE SECTION;

    ECPGdebug(1, stderr);

    EXEC SQL CONNECT TO :dbname USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    EXEC SQL CONNECT TO :connection USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    return 0;
}
```

<a id="id-1.7.5.20.4.6"></a>

## 相容性

SQL 標準規定了 `CONNECT`，但連線參數的格式則依各實作而定。

<a id="id-1.7.5.20.4.7"></a>

## 另請參閱

[DISCONNECT](ecpg-sql-disconnect.md), [SET CONNECTION](ecpg-sql-set-connection.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-connect.html)（原文版本：18.6；核對日期：2026-10-18）
