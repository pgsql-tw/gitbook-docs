<a id="id-1.11.7.21.7.1"></a>

## dblink_connect

dblink_connect — 開啟至遠端資料庫的持續連線

## 語法

```

dblink_connect(text connstr) returns text
dblink_connect(text connname, text connstr) returns text
```

<a id="id-1.11.7.21.7.5"></a>

## 說明

`dblink_connect()` 建立至遠端 PostgreSQL 資料庫的連線。要連線的伺服器與資料庫以標準 libpq 連線字串識別。可選擇為連線指定名稱；可同時開啟多個具名連線，但同一時間只允許一個未命名連線。連線會持續到關閉或資料庫工作階段結束為止。

連線字串也可為既有外部伺服器名稱。定義外部伺服器時，建議使用外部資料包裝函式 `dblink_fdw`。請參閱下方範例，以及 [CREATE SERVER](../../reference/sql-commands/sql-createserver.md) 與 [CREATE USER MAPPING](../../reference/sql-commands/sql-createusermapping.md)。

<a id="id-1.11.7.21.7.6"></a>

## 引數

*`connname`*
:   此連線要使用的名稱；若省略，會開啟未命名連線並取代任何既有未命名連線。

*`connstr`*
:   libpq 樣式的連線資訊字串，例如 `hostaddr=127.0.0.1 port=5432 dbname=mydb user=postgres password=mypasswd options=-csearch_path=`。詳情請參閱[第 32.1.1 節](../../client-interfaces/libpq/libpq-connect.md#LIBPQ-CONNSTRING)。或者，指定外部伺服器名稱。

<a id="id-1.11.7.21.7.7"></a>

## 傳回值

傳回狀態，一律為 `OK`（因為任何錯誤都會使函式引發錯誤而非傳回）。

<a id="id-1.11.7.21.7.8"></a>

## 注意事項

若不受信任的使用者可存取未採用[安全 schema 使用模式](../../the-sql-language/ddl/ddl-schemas.md#DDL-SCHEMAS-PATTERNS)的資料庫，請在每個工作階段開始時從 `search_path` 移除可供公眾寫入的 schema。例如，可在 *`connstr`* 加入 `options=-csearch_path=`。此考量不僅適用於 `dblink`，也適用於所有執行任意 SQL 指令的介面。

外部資料包裝函式 `dblink_fdw` 有額外的布林選項 `use_scram_passthrough`，用以控制 `dblink` 是否使用 SCRAM 直通驗證連線至遠端資料庫。可為外部伺服器或使用者對應指定此選項；使用者對應設定會覆寫外部伺服器設定。使用 SCRAM 直通驗證時，`dblink` 會使用 SCRAM 雜湊秘密而非明文使用者密碼連線遠端伺服器，避免在 PostgreSQL 系統目錄中儲存明文使用者密碼。進一步的詳細資訊與限制，請參閱 postgres_fdw 對等的 [`use_scram_passthrough`](postgres-fdw.md#POSTGRES-FDW-OPTION-USE-SCRAM-PASSTHROUGH) 選項文件。

只有超級使用者可使用 `dblink_connect` 建立不使用密碼驗證、SCRAM 直通或 GSSAPI 驗證的連線。若非超級使用者需要此功能，請改用 `dblink_connect_u`。

選擇包含等號的連線名稱並不明智，因為這可能與其他 `dblink` 函式中的連線資訊字串混淆。

<a id="id-1.11.7.21.7.9"></a>

## 範例

```

SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_connect('myconn', 'dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

-- FOREIGN DATA WRAPPER functionality
-- Note: local connections that don't use SCRAM pass-through require password
--       authentication for this to work properly. Otherwise, you will receive
--       the following error from dblink_connect():
--       ERROR:  password is required
--       DETAIL:  Non-superuser cannot connect if the server does not request a password.
--       HINT:  Target server's authentication method must be changed.

CREATE SERVER fdtest FOREIGN DATA WRAPPER dblink_fdw OPTIONS (hostaddr '127.0.0.1', dbname 'contrib_regression');

CREATE USER regress_dblink_user WITH PASSWORD 'secret';
CREATE USER MAPPING FOR regress_dblink_user SERVER fdtest OPTIONS (user 'regress_dblink_user', password 'secret');
GRANT USAGE ON FOREIGN SERVER fdtest TO regress_dblink_user;
GRANT SELECT ON TABLE foo TO regress_dblink_user;

\set ORIGINAL_USER :USER
\c - regress_dblink_user
SELECT dblink_connect('myconn', 'fdtest');
 dblink_connect
----------------
 OK
(1 row)

SELECT * FROM dblink('myconn', 'SELECT * FROM foo') AS t(a int, b text, c text[]);
 a  | b |       c
----+---+---------------
  0 | a | {a0,b0,c0}
  1 | b | {a1,b1,c1}
  2 | c | {a2,b2,c2}
  3 | d | {a3,b3,c3}
  4 | e | {a4,b4,c4}
  5 | f | {a5,b5,c5}
  6 | g | {a6,b6,c6}
  7 | h | {a7,b7,c7}
  8 | i | {a8,b8,c8}
  9 | j | {a9,b9,c9}
 10 | k | {a10,b10,c10}
(11 rows)

\c - :ORIGINAL_USER
REVOKE USAGE ON FOREIGN SERVER fdtest FROM regress_dblink_user;
REVOKE SELECT ON TABLE foo FROM regress_dblink_user;
DROP USER MAPPING FOR regress_dblink_user SERVER fdtest;
DROP USER regress_dblink_user;
DROP SERVER fdtest;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-connect.html)
