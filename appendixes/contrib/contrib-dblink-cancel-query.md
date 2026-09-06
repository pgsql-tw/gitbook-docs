<a id="id-1.11.7.21.21.1"></a>

## dblink_cancel_query

dblink_cancel_query — 取消具名連線上執行中的查詢

## 語法

```

dblink_cancel_query(text connname) returns text
```

<a id="id-1.11.7.21.21.5"></a>

## 說明

`dblink_cancel_query` 會嘗試取消具名連線上正在執行的查詢。請注意，這不一定會成功（例如遠端查詢可能已經完成）。取消請求只是提高查詢很快以失敗結束的機率。你仍然必須完成正常的查詢協定，例如呼叫 `dblink_get_result`。

<a id="id-1.11.7.21.21.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱。

<a id="id-1.11.7.21.21.7"></a>

## 回傳值

若已送出取消請求，則回傳 `OK`；失敗時則回傳錯誤訊息文字。

<a id="id-1.11.7.21.21.8"></a>

## 範例

```

SELECT dblink_cancel_query('dtest1');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-cancel-query.html)（原文版本：18.6；核對日期：2026-09-07）
