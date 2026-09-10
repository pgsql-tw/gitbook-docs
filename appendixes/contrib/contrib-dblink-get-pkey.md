<a id="id-1.11.7.21.22.1"></a>

## dblink_get_pkey

dblink_get_pkey — 傳回關聯主鍵欄位的位置及欄位名稱

## 語法

```

dblink_get_pkey(text relname) returns setof dblink_pkey_results
```

<a id="id-1.11.7.21.22.5"></a>

## 說明

`dblink_get_pkey` 提供本端資料庫中關聯主鍵的資訊。這有時可用於產生要傳送至
遠端資料庫的查詢。

<a id="id-1.11.7.21.22.6"></a>

## 引數

*`relname`*
:   本端關聯的名稱，例如 `foo` 或 `myschema.mytab`。名稱混合大小寫或含有
    特殊字元時，請加上雙引號，例如 `"FooBar"`；未加引號時，字串會折疊為
    小寫。

<a id="id-1.11.7.21.22.7"></a>

## 傳回值

主鍵的每個欄位傳回一筆資料列；若關聯沒有主鍵，則不傳回資料列。結果的資料列型別定義為：

```

CREATE TYPE dblink_pkey_results AS (position int, colname text);
```

`position` 欄位依序從 1 到 *`N`*；它是該欄位在主鍵中的序號，而非在資料表
欄位中的序號。

<a id="id-1.11.7.21.22.8"></a>

## 範例

```

CREATE TABLE foobar (
    f1 int,
    f2 int,
    f3 int,
    PRIMARY KEY (f1, f2, f3)
);
CREATE TABLE

SELECT * FROM dblink_get_pkey('foobar');
 position | colname
----------+---------
        1 | f1
        2 | f2
        3 | f3
(3 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/contrib-dblink-get-pkey.html)
