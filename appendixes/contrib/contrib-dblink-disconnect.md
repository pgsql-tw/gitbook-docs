<a id="id-1.11.7.21.9.1"></a>

## dblink_disconnect

dblink_disconnect — 關閉與遠端資料庫的持續連線

## 語法

```

dblink_disconnect() returns text
dblink_disconnect(text connname) returns text
```

<a id="id-1.11.7.21.9.5"></a>

## 說明

`dblink_disconnect()` 會關閉先前由 `dblink_connect()` 開啟的連線。不帶引數的形式會關閉未具名連線。

<a id="id-1.11.7.21.9.6"></a>

## 引數

*`connname`*
:   要關閉的具名連線名稱。

<a id="id-1.11.7.21.9.7"></a>

## 回傳值

回傳狀態，固定為 `OK`（因為任何錯誤都會使函式拋出錯誤，而不會正常回傳）。

<a id="id-1.11.7.21.9.8"></a>

## 範例

```

SELECT dblink_disconnect();
 dblink_disconnect
-------------------
 OK
(1 row)

SELECT dblink_disconnect('myconn');
 dblink_disconnect
-------------------
 OK
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-disconnect.html)（原文版本：18.6；核對日期：2026-09-07）
