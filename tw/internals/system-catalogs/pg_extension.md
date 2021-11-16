# 51.22. pg\_extension

目錄 pg\_extension 儲存有關已安裝延伸功能的資訊。有關延伸功能的詳細資訊，請參閱[第 37.17 節](../../server-programming/extending-sql/packaging-related-objects-into-an-extension.md)。

**Table 51.22. `pg_extension` Columns**

| Name             | Type     | References                               | Description                             |
| ---------------- | -------- | ---------------------------------------- | --------------------------------------- |
| `oid`            | `oid`    |                                          | 資料列指標ID                                 |
| `extname`        | `name`   |                                          | 延伸功能名稱                                  |
| `extowner`       | `oid`    | ``[`pg_authid`](pg\_authid.md).oid       | 延伸功能的擁有者                                |
| `extnamespace`   | `oid`    | ``[`pg_namespace`](pg\_namespace.md).oid | 延伸功能之中所導出物件的綱要名稱                        |
| `extrelocatable` | `bool`   |                                          | 如果延伸功能可以接受重新定位到另一個綱要之中，則為 True          |
| `extversion`     | `text`   |                                          | 延伸功能的版本名稱                               |
| `extconfig`      | `oid[]`  | ``[`pg_class`](pg\_class.md).oid         | 延伸功能組態資料表的 regclass OID 陣列，如果沒有，則為 NULL |
| `extcondition`   | `text[]` |                                          | 延伸功能組態資料表的 WHERE 子句過濾條件陣列，如果沒有，則為 NULL  |

請注意，與大多數帶有「namespace」欄位的目錄不同，extnamespace 並不暗指該延伸功能屬於該綱要(schema)。延伸功能並不在任何綱要之中。不過 extnamespace 指示包含大多數或所有延伸功能所屬物件的綱要。如果 extrelocatable 為 true，則此綱要實際上必須包含屬於該延伸功能的所有需要綱要的物件。\
