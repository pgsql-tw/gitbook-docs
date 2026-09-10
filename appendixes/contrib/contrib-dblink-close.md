<a id="id-1.11.7.21.14.1"></a>

## dblink_close

dblink_close — 關閉遠端資料庫中的游標

## 語法

```

dblink_close(text cursorname [, bool fail_on_error]) returns text
dblink_close(text connname, text cursorname [, bool fail_on_error]) returns text
```

<a id="id-1.11.7.21.14.5"></a>

## 說明

`dblink_close` 關閉先前以 `dblink_open` 開啟的游標。

<a id="id-1.11.7.21.14.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱；省略此參數可使用未命名連線。

*`cursorname`*
:   要關閉的游標名稱。

*`fail_on_error`*
:   若為 true（省略時的預設值），連線遠端引發的錯誤也會在本機引發錯誤。若為 false，遠端錯誤會在本機回報為 NOTICE，且函式傳回值設為 `ERROR`。

<a id="id-1.11.7.21.14.7"></a>

## 傳回值

傳回狀態，為 `OK` 或 `ERROR`。

<a id="id-1.11.7.21.14.8"></a>

## 注意事項

若 `dblink_open` 啟動明確交易區塊，且這是此連線上最後一個仍開啟的游標，`dblink_close` 會發出相對應的 `COMMIT`。

<a id="id-1.11.7.21.14.9"></a>

## 範例

```

SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc');
 dblink_open
-------------
 OK
(1 row)

SELECT dblink_close('foo');
 dblink_close
--------------
 OK
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-close.html)
