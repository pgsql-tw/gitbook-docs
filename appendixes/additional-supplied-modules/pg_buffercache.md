# F.24. pg\_buffercache

pg\_buffercache 延伸功能提供了一個即時檢查共享緩衝區配置情況的方法。

該模塊提供了一個 C 函數的 pg\_buffercache\_pages，該函數回傳一組記錄，以及一個檢視表 pg\_buffercache，該檢視表封裝了該函數以便於使用。

預設情況下，僅限於超級使用者和 pg\_monitor 角色的成員使用。也可以使用 GRANT 將存取權限授予其他角色。

## F.24.1. The `pg_buffercache` View

[Table F.15](pg\_buffercache.md#table-f-15-pg\_buffercache-columns) 中列出了此檢視表的欄位定義。

#### **Table F.15. `pg_buffercache` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>bufferid</code> <code>integer</code></p><p>ID, in the range 1..<code>shared_buffers</code></p>                                                                                                                      |
| <p><code>relfilenode</code> <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-class.html"><code>pg_class</code></a>.<code>relfilenode</code>)</p><p>Filenode number of the relation</p>    |
| <p><code>reltablespace</code> <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-tablespace.html"><code>pg_tablespace</code></a>.<code>oid</code>)</p><p>Tablespace OID of the relation</p> |
| <p><code>reldatabase</code> <code>oid</code> (references <a href="https://www.postgresql.org/docs/13/catalog-pg-database.html"><code>pg_database</code></a>.<code>oid</code>)</p><p>Database OID of the relation</p>         |
| <p><code>relforknumber</code> <code>smallint</code></p><p>Fork number within the relation; see <code>include/common/relpath.h</code></p>                                                                                     |
| <p><code>relblocknumber</code> <code>bigint</code></p><p>Page number within the relation</p>                                                                                                                                 |
| <p><code>isdirty</code> <code>boolean</code></p><p>Is the page dirty?</p>                                                                                                                                                    |
| <p><code>usagecount</code> <code>smallint</code></p><p>Clock-sweep access count</p>                                                                                                                                          |
| <p><code>pinning_backends</code> <code>integer</code></p><p>Number of backends pinning this buffer</p>                                                                                                                       |

There is one row for each buffer in the shared cache. Unused buffers are shown with all fields null except `bufferid`. Shared system catalogs are shown as belonging to database zero.

Because the cache is shared by all the databases, there will normally be pages from relations not belonging to the current database. This means that there may not be matching join rows in `pg_class` for some rows, or that there could even be incorrect joins. If you are trying to join against `pg_class`, it's a good idea to restrict the join to rows having `reldatabase` equal to the current database's OID or zero.

Since buffer manager locks are not taken to copy the buffer state data that the view will display, accessing `pg_buffercache` view has less impact on normal buffer activity but it doesn't provide a consistent set of results across all buffers. However, we ensure that the information of each buffer is self-consistent.

## F.24.2. Sample Output

```
regression=# SELECT n.nspname, c.relname, count(*) AS buffers
             FROM pg_buffercache b JOIN pg_class c
             ON b.relfilenode = pg_relation_filenode(c.oid) AND
                b.reldatabase IN (0, (SELECT oid FROM pg_database
                                      WHERE datname = current_database()))
             JOIN pg_namespace n ON n.oid = c.relnamespace
             GROUP BY n.nspname, c.relname
             ORDER BY 3 DESC
             LIMIT 10;

  nspname   |        relname         | buffers
------------+------------------------+---------
 public     | delete_test_table      |     593
 public     | delete_test_table_pkey |     494
 pg_catalog | pg_attribute           |     472
 public     | quad_poly_tbl          |     353
 public     | tenk2                  |     349
 public     | tenk1                  |     349
 public     | gin_test_idx           |     306
 pg_catalog | pg_largeobject         |     206
 public     | gin_test_tbl           |     188
 public     | spgist_text_tbl        |     182
(10 rows)
```

## F.24.3. Authors

Mark Kirkwood `<`[`markir@paradise.net.nz`](mailto:markir@paradise.net.nz)`>`

Design suggestions: Neil Conway `<`[`neilc@samurai.com`](mailto:neilc@samurai.com)`>`

Debugging advice: Tom Lane `<`[`tgl@sss.pgh.pa.us`](mailto:tgl@sss.pgh.pa.us)`>`
