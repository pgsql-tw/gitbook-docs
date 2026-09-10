<a id="id-1.11.7.21.16.1"></a>

## dblink_error_message

dblink_error_message — 取得具名連線上的最新錯誤訊息

## 語法

```

dblink_error_message(text connname) returns text
```

<a id="id-1.11.7.21.16.5"></a>

## 說明

`dblink_error_message` 會擷取指定連線最新的遠端錯誤訊息。

<a id="id-1.11.7.21.16.6"></a>

## 引數

*`connname`*
:   要使用的連線名稱。

<a id="id-1.11.7.21.16.7"></a>

## 回傳值

傳回最新錯誤訊息；若此連線未發生錯誤，則傳回 `OK`。

<a id="id-1.11.7.21.16.8"></a>

## 注意事項

當 `dblink_send_query` 啟動非同步查詢時，與該連線相關的錯誤訊息可能要到
消費伺服器回應訊息後才會更新。因此，通常應在 `dblink_error_message` 前呼叫
`dblink_is_busy` 或 `dblink_get_result`，以便看見非同步查詢產生的任何錯誤。

<a id="id-1.11.7.21.16.9"></a>

## 範例

```

SELECT dblink_error_message('dtest1');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-error-message.html)（原文版本：18.6；核對日期：2026-09-10）
