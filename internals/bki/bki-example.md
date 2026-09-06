## 68.6. BKI 範例 [#](#BKI-EXAMPLE)

以下命令序列會建立 OID 為 420 的資料表 `test_table`，其中包含 `oid`、`cola` 和 `colb` 三個欄位，型別分別為 `oid`、`int4` 和 `text`，並在資料表中插入兩筆資料列：

```

create test_table 420 (oid = oid, cola = int4, colb = text)
open test_table
insert ( 421 1 'value 1' )
insert ( 422 2 _null_ )
close test_table
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/bki-example.html)（原文版本：18.6；核對日期：2026-09-07）
