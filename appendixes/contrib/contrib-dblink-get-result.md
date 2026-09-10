<a id="id-1.11.7.21.20.1"></a>

## dblink_get_result

dblink_get_result — 取得非同步查詢結果

## 語法

```

dblink_get_result(text connname [, bool fail_on_error]) returns setof record
```

<a id="id-1.11.7.21.20.5"></a>

## 說明

`dblink_get_result` 收集先前以 `dblink_send_query` 傳送之非同步查詢的
結果。若查詢尚未完成，`dblink_get_result` 會等待至其完成。

<a id="id-1.11.7.21.20.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱。

*`fail_on_error`*
:   若為 true（省略時的預設值），連線遠端引發的錯誤也會在本端引發
    錯誤。若為 false，遠端錯誤會在本端以 NOTICE 回報，且此函式不傳回
    資料列。

<a id="id-1.11.7.21.20.7"></a>

## 傳回值

對於非同步查詢（亦即傳回資料列的 SQL 陳述式），此函式會傳回查詢產生的
資料列。使用此函式時，你必須如 `dblink` 先前所述，指定預期的欄位集合。

對於非同步命令（亦即不傳回資料列的 SQL 陳述式），此函式傳回單一資料列，
其中包含一個存有命令狀態字串的 text 欄位。仍須在呼叫的 `FROM` 子句中
指定結果將有單一 text 欄位。

<a id="id-1.11.7.21.20.8"></a>

## 注意事項

若 `dblink_send_query` 傳回 1，*必須*呼叫此函式。每個已傳送的查詢都必須
呼叫一次，並額外呼叫一次以取得空集合結果，之後才可再次使用該連線。

使用 `dblink_send_query` 和 `dblink_get_result` 時，dblink 會先擷取完整的
遠端查詢結果，才將其中任何部分傳回本端查詢處理器。若查詢傳回大量資料列，
可能導致本端 session 暫時出現記憶體膨脹。較好的作法可能是使用
`dblink_open` 將此類查詢開啟為游標，之後每次擷取可管理數量的資料列。
或者可使用一般的 `dblink()`，它會將大型結果集暫存至磁碟，以避免記憶體膨脹。

<a id="id-1.11.7.21.20.9"></a>

## 範例

```

contrib_regression=# SELECT dblink_connect('dtest1', 'dbname=contrib_regression');
 dblink_connect
----------------
 OK
(1 row)

contrib_regression=# SELECT * FROM
contrib_regression-# dblink_send_query('dtest1', 'select * from foo where f1 < 3') AS t1;
 t1
----
  1
(1 row)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 |     f3
----+----+------------
  0 | a  | {a0,b0,c0}
  1 | b  | {a1,b1,c1}
  2 | c  | {a2,b2,c2}
(3 rows)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 | f3
----+----+----
(0 rows)

contrib_regression=# SELECT * FROM
contrib_regression-# dblink_send_query('dtest1', 'select * from foo where f1 < 3; select * from foo where f1 > 6') AS t1;
 t1
----
  1
(1 row)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 |     f3
----+----+------------
  0 | a  | {a0,b0,c0}
  1 | b  | {a1,b1,c1}
  2 | c  | {a2,b2,c2}
(3 rows)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 |      f3
----+----+---------------
  7 | h  | {a7,b7,c7}
  8 | i  | {a8,b8,c8}
  9 | j  | {a9,b9,c9}
 10 | k  | {a10,b10,c10}
(4 rows)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 | f3
----+----+----
(0 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-get-result.html)
