# 53.3. pg\_am

The catalog `pg_am` stores information about relation access methods. There is one row for each access method supported by the system. Currently, only tables and indexes have access methods. The requirements for table and index access methods are discussed in detail in [Chapter 63](../table-access-method-interface-definition.md) and [Chapter 64](../index-access-method-interface-definition.md) respectively.

#### **Table 53.3. `pg_am` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>oid</code> <code>oid</code></p><p>Row identifier</p>                                                                                                                                                                                                                          |
| <p><code>amname</code> <code>name</code></p><p>Name of the access method</p>                                                                                                                                                                                                           |
| <p><code>amhandler</code> <code>regproc</code> (references <a href="pg_proc.md"><code>pg_proc</code></a>.<code>oid</code>)</p><p>OID of a handler function that is responsible for supplying information about the access method</p> |
| <p><code>amtype</code> <code>char</code></p><p><code>t</code> = table (including materialized views), <code>i</code> = index.</p>                                                                                                                                                      |

{% hint style="info" %}
#### Note

Before PostgreSQL 9.6, `pg_am` contained many additional columns representing properties of index access methods. That data is now only directly visible at the C code level. However, `pg_index_column_has_property()` and related functions have been added to allow SQL queries to inspect index access method properties; see [Table 9.71](../../the-sql-language/functions-and-operators/system-information-functions.md#FUNCTIONS-INFO-CATALOG-TABLE).
{% endhint %}
