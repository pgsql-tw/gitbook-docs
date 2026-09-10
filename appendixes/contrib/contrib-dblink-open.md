<a id="id-1.11.7.21.12.1"></a>

## dblink_open

dblink_open — 在遠端資料庫開啟游標

## 語法

```

dblink_open(text cursorname, text sql [, bool fail_on_error]) returns text
dblink_open(text connname, text cursorname, text sql [, bool fail_on_error]) returns text
```

<a id="id-1.11.7.21.12.5"></a>

## 說明

`dblink_open()` 在遠端資料庫開啟游標。之後可使用 `dblink_fetch()` 和
`dblink_close()` 操作該游標。

<a id="id-1.11.7.21.12.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱；省略此引數時使用未命名連線。

*`cursorname`*
:   要指派給此游標的名稱。

*`sql`*
:   要在遠端資料庫執行的 `SELECT` 陳述式，例如 `select * from pg_class`。

*`fail_on_error`*
:   若為 true（省略時的預設值），連線遠端引發的錯誤也會在本端引發
    錯誤。若為 false，遠端錯誤會在本端以 NOTICE 回報，且函式的傳回值會
    設為 `ERROR`。

<a id="id-1.11.7.21.12.7"></a>

## 傳回值

傳回狀態，為 `OK` 或 `ERROR`。

<a id="id-1.11.7.21.12.8"></a>

## 注意事項

由於游標只能在交易內持續存在，若遠端尚未位於交易中，`dblink_open` 會在
遠端啟動明確的交易區塊（`BEGIN`）。執行相對應的 `dblink_close` 時，會再次
關閉此交易。請注意，若你在 `dblink_open` 與 `dblink_close` 之間使用
`dblink_exec` 變更資料，然後發生錯誤或在 `dblink_close` 前使用
`dblink_disconnect`，交易會被中止，因而*遺失*你的變更。

<a id="id-1.11.7.21.12.9"></a>

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
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-open.html)
