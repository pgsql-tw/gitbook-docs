<a id="id-1.11.7.21.13.1"></a>

## dblink_fetch

dblink_fetch — 從遠端資料庫的已開啟游標傳回資料列

## 語法

```

dblink_fetch(text cursorname, int howmany [, bool fail_on_error]) returns setof record
dblink_fetch(text connname, text cursorname, int howmany [, bool fail_on_error]) returns setof record
```

<a id="id-1.11.7.21.13.5"></a>

## 說明

`dblink_fetch` 從先前由 `dblink_open` 建立的游標擷取資料列。

<a id="id-1.11.7.21.13.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱；省略此引數時使用未命名連線。

*`cursorname`*
:   要從中擷取資料的游標名稱。

*`howmany`*
:   要擷取的最大資料列數。從目前的游標位置開始，向前擷取接下來的
    *`howmany`* 筆資料列。游標到達結尾後，不再產生任何資料列。

*`fail_on_error`*
:   若為 true（省略時的預設值），連線遠端引發的錯誤也會在本端引發
    錯誤。若為 false，遠端錯誤會在本端以 NOTICE 回報，且此函式不傳回
    資料列。

<a id="id-1.11.7.21.13.7"></a>

## 傳回值

此函式傳回從游標擷取的資料列。使用此函式時，你必須如 `dblink`
先前所述，指定預期的欄位集合。

<a id="id-1.11.7.21.13.8"></a>

## 注意事項

若 `FROM` 子句指定的傳回欄位數與遠端游標實際傳回的欄位數不符，便會引發
錯誤。即使如此，遠端游標仍會向前推進，推進的資料列數與未發生該錯誤時
相同。遠端 `FETCH` 完成後，本端查詢發生的任何其他錯誤也同樣如此。

<a id="id-1.11.7.21.13.9"></a>

## 範例

```

SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc where proname like ''bytea%''');
 dblink_open
-------------
 OK
(1 row)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname |  source
----------+----------
 byteacat | byteacat
 byteacmp | byteacmp
 byteaeq  | byteaeq
 byteage  | byteage
 byteagt  | byteagt
(5 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname  |  source
-----------+-----------
 byteain   | byteain
 byteale   | byteale
 bytealike | bytealike
 bytealt   | bytealt
 byteane   | byteane
(5 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
  funcname  |   source
------------+------------
 byteanlike | byteanlike
 byteaout   | byteaout
(2 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname | source
----------+--------
(0 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-fetch.html)
