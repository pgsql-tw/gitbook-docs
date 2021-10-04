# 9.14. UUID Functions

PostgreSQL 提供了一個產成 UUID 的函數：

```text
gen_random_uuid () → uuid
```

此函數回傳版本 4（隨機）的 UUID。這是最常用的 UUID 樣式，適用於大多數的應用。

[uuid-ossp](../../appendixes/additional-supplied-modules/uuid-ossp.md) 模組提供了其他函數，這些函數實作了用於產生成其他 UUID 的標準演算法。

PostgreSQL 還提供了 [Table 9.1](comparison-functions-and-operators.md#table-9-1-comparison-operators) 中列出的用於 UUID 常用的比較運算子。

