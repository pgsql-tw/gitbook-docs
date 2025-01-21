# 9.14. UUID Functions

PostgreSQL 提供了一個產成 UUID 的函數：

```
gen_random_uuid () → uuid
```

此函數回傳 version 4（隨機）的 UUID。這是最常用的 UUID 樣式，適用於大多數的應用。

[uuid-ossp](../../appendixes/additional-supplied-modules/uuid-ossp.md) 模組提供了其他函數，這些函數實作了用於產生成其他 UUID 的標準演算法。

還有一些函數可以從 UUID 中得到其內含的資料：

```
uuid_extract_timestamp (uuid) → timestamp with time zone
```

這個函數可以從 UUID version 1 中取出時間戳記的資訊，其型別為 `timestamp with time zone。如果是 UUID 的其他版本，則會回傳 null。要注意的是，這個時間戳記並不一定等於 UUID 產生時的時間，它取決於該 UUID 是如何被產生的。`

```
uuid_extract_version (uuid) → smallint
```

這個函數可以識別 UUID 的版本，其版本標準就如 [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122) 之中所述。對於可能還有其他變體，則會回傳 null。舉例來說，如果有一個 UUID 是由 `gen_random_uuid 所產生，那麼此函數將會回傳 4。`

PostgreSQL 用於 UUID 常用的比較運算子請參考 [Table 9.1](comparison-functions-and-operators.md#table-9-1-comparison-operators) 。
