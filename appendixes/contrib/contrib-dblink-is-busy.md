<a id="id-1.11.7.21.18.1"></a>

## dblink_is_busy

dblink_is_busy — 檢查連線是否正在執行非同步查詢

## 語法

```

dblink_is_busy(text connname) returns int
```

<a id="id-1.11.7.21.18.5"></a>

## 說明

`dblink_is_busy` 測試非同步查詢是否正在進行。

<a id="id-1.11.7.21.18.6"></a>

## 引數

*`connname`*
:   要檢查的連線名稱。

<a id="id-1.11.7.21.18.7"></a>

## 回傳值

連線忙碌時回傳 1，否則回傳 0。此函式回傳 0 時，可保證 `dblink_get_result` 不會封鎖。

<a id="id-1.11.7.21.18.8"></a>

## 範例

```

SELECT dblink_is_busy('dtest1');
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-is-busy.html)（原文版本：18.6；核對日期：2026-09-06）
