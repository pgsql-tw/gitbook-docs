<a id="id-1.11.7.21.11.1"></a>

## dblink_exec

dblink_exec — 在遠端資料庫中執行指令

## 語法

```

dblink_exec(text connname, text sql [, bool fail_on_error]) returns text
dblink_exec(text connstr, text sql [, bool fail_on_error]) returns text
dblink_exec(text sql [, bool fail_on_error]) returns text
```

<a id="id-1.11.7.21.11.5"></a>

## 說明

`dblink_exec` 在遠端資料庫中執行指令（亦即不傳回資料列的任何 SQL 陳述式）。

提供兩個 `text` 引數時，第一個引數會先作為持續連線名稱查詢；若找到，指令會在該連線上執行。若找不到，第一個引數會如 `dblink_connect` 一樣被視為連線資訊字串，且只會在此指令期間建立所指連線。

<a id="id-1.11.7.21.11.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱；省略此參數可使用未命名連線。

*`connstr`*
:   如同先前 `dblink_connect` 所述的連線資訊字串。

*`sql`*
:   要在遠端資料庫執行的 SQL 指令，例如 `insert into foo values(0, 'a', '{"a0","b0","c0"}')`。

*`fail_on_error`*
:   若為 true（省略時的預設值），連線遠端引發的錯誤也會在本機引發錯誤。若為 false，遠端錯誤會在本機回報為 NOTICE，且函式傳回值設為 `ERROR`。

<a id="id-1.11.7.21.11.7"></a>

## 傳回值

傳回狀態，為指令的狀態字串或 `ERROR`。

<a id="id-1.11.7.21.11.8"></a>

## 範例

```

SELECT dblink_connect('dbname=dblink_test_standby');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_exec('insert into foo values(21, ''z'', ''{"a0","b0","c0"}'');');
   dblink_exec
-----------------
 INSERT 943366 1
(1 row)

SELECT dblink_connect('myconn', 'dbname=regression');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_exec('myconn', 'insert into foo values(21, ''z'', ''{"a0","b0","c0"}'');');
   dblink_exec
------------------
 INSERT 6432584 1
(1 row)

SELECT dblink_exec('myconn', 'insert into pg_class values (''foo'')',false);
NOTICE:  sql error
DETAIL:  ERROR:  null value in column "relnamespace" violates not-null constraint

 dblink_exec
-------------
 ERROR
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-exec.html)
