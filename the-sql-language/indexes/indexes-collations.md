## 11.11. 索引與定序 [#](#INDEXES-COLLATIONS)

每個索引欄位只能支援一種定序。如果需要多種定序，可能必須建立多個索引。

考慮下列陳述式：

```

CREATE TABLE test1c (
    id integer,
    content varchar COLLATE "x"
);

CREATE INDEX test1c_content_index ON test1c (content);
```

索引會自動使用底層欄位的定序。因此，下列形式的查詢：

```

SELECT * FROM test1c WHERE content > constant;
```

可以使用此索引，因為比較運算預設會使用欄位的定序。不過，此索引無法加速涉及其他定序的查詢。例如，如果也需要下列形式的查詢：

```

SELECT * FROM test1c WHERE content > constant COLLATE "y";
```

就可以另外建立支援 `"y"` 定序的索引，如下所示：

```

CREATE INDEX test1c_content_y_index ON test1c (content COLLATE "y");
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes-collations.html)（原文版本：18.6；核對日期：2026-09-07）
