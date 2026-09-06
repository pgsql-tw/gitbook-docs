## 68.6. BKI Example [#](#BKI-EXAMPLE)

The following sequence of commands will create the table
`test_table` with OID 420, having three columns
`oid`, `cola` and `colb`
of type `oid`, `int4` and `text`,
respectively, and insert two rows into the table:

```

create test_table 420 (oid = oid, cola = int4, colb = text)
open test_table
insert ( 421 1 'value 1' )
insert ( 422 2 _null_ )
close test_table
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/bki-example.html)（英文原文，待翻譯）
