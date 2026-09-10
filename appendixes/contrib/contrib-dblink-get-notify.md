<a id="id-1.11.7.21.19.1"></a>

## dblink_get_notify

dblink_get_notify — 擷取連線上的非同步通知

## 語法

```

dblink_get_notify() returns setof (notify_name text, be_pid int, extra text)
dblink_get_notify(text connname) returns setof (notify_name text, be_pid int, extra text)
```

<a id="id-1.11.7.21.19.5"></a>

## 說明

`dblink_get_notify` 從未命名連線，或指定的具名連線擷取通知。若要透過
dblink 接收通知，必須先使用 `dblink_exec` 發出 `LISTEN`。詳情請參閱
[LISTEN](../../reference/sql-commands/sql-listen.md) 和 [NOTIFY](../../reference/sql-commands/sql-notify.md)。

<a id="id-1.11.7.21.19.6"></a>

## 引數

*`connname`*
:   要從中取得通知的具名連線名稱。

<a id="id-1.11.7.21.19.7"></a>

## 傳回值

傳回 `setof (notify_name text, be_pid int, extra text)`；若沒有通知則傳回空集合。

<a id="id-1.11.7.21.19.8"></a>

## 範例

```

SELECT dblink_exec('LISTEN virtual');
 dblink_exec
-------------
 LISTEN
(1 row)

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------+--------+-------
(0 rows)

NOTIFY virtual;
NOTIFY

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------+--------+-------
 virtual     |   1229 |
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-get-notify.html)
