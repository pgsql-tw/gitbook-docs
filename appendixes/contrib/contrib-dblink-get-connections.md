<a id="id-1.11.7.21.15.1"></a>

## dblink_get_connections

dblink_get_connections — 回傳所有已開啟具名 dblink 連線的名稱

## 語法

```

dblink_get_connections() returns text[]
```

<a id="id-1.11.7.21.15.5"></a>

## 說明

`dblink_get_connections` 會回傳一個陣列，包含所有已開啟具名 `dblink` 連線的名稱。

<a id="id-1.11.7.21.15.6"></a>

## 回傳值

回傳包含連線名稱的文字陣列；若沒有連線則回傳 NULL。

<a id="id-1.11.7.21.15.7"></a>

## 範例

```

SELECT dblink_get_connections();
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-get-connections.html)（原文版本：18.6；核對日期：2026-09-07）
