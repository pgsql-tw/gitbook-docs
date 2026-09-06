## Appendix K. PostgreSQL Limits

[Table K.1](README.md#LIMITS-TABLE) describes various hard limits of
PostgreSQL. However, practical limits, such as
performance limitations or available disk space may apply before absolute
hard limits are reached.

<a id="LIMITS-TABLE"></a>

**Table K.1. PostgreSQL Limitations**

<table border="1" class="table" summary="PostgreSQL Limitations"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Item</th><th>Upper Limit</th><th>Comment</th></tr></thead><tbody><tr><td>database size</td><td>unlimited</td><td> </td></tr><tr><td>number of databases</td><td>4,294,950,911</td><td> </td></tr><tr><td>relations per database</td><td>1,431,650,303</td><td> </td></tr><tr><td>relation size</td><td>32 TB</td><td>with the default <code class="symbol">BLCKSZ</code> of 8192 bytes</td></tr><tr><td>rows per table</td><td>limited by the number of tuples that can fit onto 4,294,967,295 pages</td><td> </td></tr><tr><td>columns per table</td><td>1,600</td><td>further limited by tuple size fitting on a single page; see note
     below</td></tr><tr><td>columns in a result set</td><td>1,664</td><td> </td></tr><tr><td>field size</td><td>1 GB</td><td> </td></tr><tr><td>indexes per table</td><td>unlimited</td><td>constrained by maximum relations per database</td></tr><tr><td>columns per index</td><td>32</td><td>can be increased by recompiling <span class="productname">PostgreSQL</span></td></tr><tr><td>partition keys</td><td>32</td><td>can be increased by recompiling <span class="productname">PostgreSQL</span></td></tr><tr><td>identifier length</td><td>63 bytes</td><td>can be increased by recompiling <span class="productname">PostgreSQL</span></td></tr><tr><td>function arguments</td><td>100</td><td>can be increased by recompiling <span class="productname">PostgreSQL</span></td></tr><tr><td>query parameters</td><td>65,535</td><td> </td></tr></tbody></table>

<br>

The maximum number of columns for a table is further reduced as the tuple
being stored must fit in a single 8192-byte heap page. For example,
excluding the tuple header, a tuple made up of 1,600 `int` columns
would consume 6400 bytes and could be stored in a heap page, but a tuple of
1,600 `bigint` columns would consume 12800 bytes and would
therefore not fit inside a heap page.
Variable-length fields of
types such as `text`, `varchar`, and `char`
can have their values stored out of line in the table's TOAST table when the
values are large enough to require it. Only an 18-byte pointer must remain
inside the tuple in the table's heap. For shorter length variable-length
fields, either a 4-byte or 1-byte field header is used and the value is
stored inside the heap tuple.

Columns that have been dropped from the table also contribute to the maximum
column limit. Moreover, although the dropped column values for newly
created tuples are internally marked as null in the tuple's null bitmap, the
null bitmap also occupies space.

Each table can store a theoretical maximum of 2^32 out-of-line values; see
[Section 66.2](../../internals/storage/storage-toast.md) for a detailed discussion of out-of-line
storage. This limit arises from the use of a 32-bit OID to identify each
such value. The practical limit is significantly less than the theoretical
limit, because as the OID space fills up, finding an OID that is still free
can become expensive, in turn slowing down INSERT/UPDATE statements.
Typically, this is only an issue for tables containing many terabytes
of data; partitioning is a possible workaround.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/limits.html)（英文原文，待翻譯）
