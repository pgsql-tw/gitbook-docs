## 29.6. Generated Column Replication [#](#LOGICAL-REPLICATION-GENCOLS)

Typically, a table at the subscriber will be defined the same as the
publisher table, so if the publisher table has a [`GENERATED column`](../../the-sql-language/ddl/ddl-generated-columns.md) then the subscriber table will
have a matching generated column. In this case, it is always the subscriber
table generated column value that is used.

For example, note below that subscriber table generated column value comes from the
subscriber column's calculation.

```

/* pub # */ CREATE TABLE tab_gen_to_gen (a int, b int GENERATED ALWAYS AS (a + 1) STORED);
/* pub # */ INSERT INTO tab_gen_to_gen VALUES (1),(2),(3);
/* pub # */ CREATE PUBLICATION pub1 FOR TABLE tab_gen_to_gen;
/* pub # */ SELECT * FROM tab_gen_to_gen;
 a | b
---+---
 1 | 2
 2 | 3
 3 | 4
(3 rows)

/* sub # */ CREATE TABLE tab_gen_to_gen (a int, b int GENERATED ALWAYS AS (a * 100) STORED);
/* sub # */ CREATE SUBSCRIPTION sub1 CONNECTION 'dbname=test_pub' PUBLICATION pub1;
/* sub # */ SELECT * from tab_gen_to_gen;
 a | b
---+----
 1 | 100
 2 | 200
 3 | 300
(3 rows)
```

In fact, prior to version 18.0, logical replication does not publish
`GENERATED` columns at all.

But, replicating a generated column to a regular column can sometimes be
desirable.

### Tip

This feature may be useful when replicating data to a
non-PostgreSQL database via output plugin, especially if the target database
does not support generated columns.

Generated columns are not published by default, but users can opt to
publish stored generated columns just like regular ones.

There are two ways to do this:

* Set the `PUBLICATION` parameter
  [`publish_generated_columns`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) to `stored`.
  This instructs PostgreSQL logical replication to publish current and
  future stored generated columns of the publication's tables.
* Specify a table [column list](logical-replication-col-lists.md)
  to explicitly nominate which stored generated columns will be published.

  ### Note

  When determining which table columns will be published, a column list
  takes precedence, overriding the effect of the
  `publish_generated_columns` parameter.

The following table summarizes behavior when there are generated columns
involved in the logical replication. Results are shown for when
publishing generated columns is not enabled, and for when it is
enabled.

<a id="LOGICAL-REPLICATION-GENCOLS-TABLE-SUMMARY"></a>

**Table 29.2. Replication Result Summary**

<table border="1" class="table" summary="Replication Result Summary"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>Publish generated columns?</th><th>Publisher table column</th><th>Subscriber table column</th><th>Result</th></tr></thead><tbody><tr><td>No</td><td>GENERATED</td><td>GENERATED</td><td>Publisher table column is not replicated. Use the subscriber table generated column value.</td></tr><tr><td>No</td><td>GENERATED</td><td>regular</td><td>Publisher table column is not replicated. Use the subscriber table regular column default value.</td></tr><tr><td>No</td><td>GENERATED</td><td>--missing--</td><td>Publisher table column is not replicated. Nothing happens.</td></tr><tr><td>Yes</td><td>GENERATED</td><td>GENERATED</td><td>ERROR. Not supported.</td></tr><tr><td>Yes</td><td>GENERATED</td><td>regular</td><td>Publisher table column value is replicated to the subscriber table column.</td></tr><tr><td>Yes</td><td>GENERATED</td><td>--missing--</td><td>ERROR. The column is reported as missing from the subscriber table.</td></tr></tbody></table>

<br>

### Warning

There's currently no support for subscriptions comprising several
publications where the same table has been published with different column
lists. See [Section 29.5](logical-replication-col-lists.md).

This same situation can occur if one publication is publishing generated
columns, while another publication in the same subscription is not
publishing generated columns for the same table.

### Note

If the subscriber is from a release prior to 18, then initial table
synchronization won't copy generated columns even if they are defined in
the publisher.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-gencols.html)（英文原文，待翻譯）
