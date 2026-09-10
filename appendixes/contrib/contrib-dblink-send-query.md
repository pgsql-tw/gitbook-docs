<a id="id-1.11.7.21.17.1"></a>

## dblink_send_query

dblink_send_query — 將非同步查詢傳送至遠端資料庫

## 語法

```

dblink_send_query(text connname, text sql) returns int
```

<a id="id-1.11.7.21.17.5"></a>

## 說明

`dblink_send_query` 會先建立要非同步執行的查詢，然後傳送至遠端資料庫；亦即不會立即等待結果。該連線不得已有正在進行的非同步查詢。

成功派送非同步查詢後，可使用 `dblink_is_busy` 檢查完成狀態，最後以 `dblink_get_result` 收集結果。也可使用 `dblink_cancel_query` 嘗試取消進行中的非同步查詢。

<a id="id-1.11.7.21.17.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱。

*`sql`*
:   要在遠端資料庫執行的 SQL 陳述式，例如 `select * from pg_class`。

<a id="id-1.11.7.21.17.7"></a>

## 回傳值

若成功派送查詢則傳回 1，否則傳回 0。

<a id="id-1.11.7.21.17.8"></a>

## 範例

```

SELECT dblink_send_query('dtest1', 'SELECT * FROM foo WHERE f1 < 3');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-send-query.html)（原文版本：18.6；核對日期：2026-09-10）
