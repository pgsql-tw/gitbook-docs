<a id="BKI-COMMANDS"></a>

# 74.4. BKI Commands

`create` <em class="replaceable"><code>tablename</code></em> <em class="replaceable"><code>tableoid</code></em> [`bootstrap`] [`shared_relation`] [`rowtype_oid` <em class="replaceable"><code>oid</code></em>] (<em class="replaceable"><code>name1</code></em> = <em class="replaceable"><code>type1</code></em> [`FORCE NOT NULL` | `FORCE NULL` ] [, <em class="replaceable"><code>name2</code></em> = <em class="replaceable"><code>type2</code></em> [`FORCE NOT NULL` | `FORCE NULL` ], ...])

Create a table named <em class="replaceable"><code>tablename</code></em>, and having the OID <em class="replaceable"><code>tableoid</code></em>, with the columns given in parentheses.

The following column types are supported directly by `bootstrap.c`: `bool`, `bytea`, `char` (1 byte), `name`, `int2`, `int4`, `regproc`, `regclass`, `regtype`, `text`, `oid`, `tid`, `xid`, `cid`, `int2vector`, `oidvector`, `_int4` (array), `_text` (array), `_oid` (array), `_char` (array), `_aclitem` (array). Although it is possible to create tables containing columns of other types, this cannot be done until after `pg_type` has been created and filled with appropriate entries. (That effectively means that only these column types can be used in bootstrap catalogs, but non-bootstrap catalogs can contain any built-in type.)

When `bootstrap` is specified, the table will only be created on disk; nothing is entered into `pg_class`, `pg_attribute`, etc., for it. Thus the table will not be accessible by ordinary SQL operations until such entries are made the hard way (with `insert` commands). This option is used for creating `pg_class` etc. themselves.

The table is created as shared if `shared_relation` is specified. The table's row type OID (`pg_type` OID) can optionally be specified via the `rowtype_oid` clause; if not specified, an OID is automatically generated for it. (The `rowtype_oid` clause is useless if `bootstrap` is specified, but it can be provided anyway for documentation.)

`open` <em class="replaceable"><code>tablename</code></em>

Open the table named <em class="replaceable"><code>tablename</code></em> for insertion of data. Any currently open table is closed.

`close` <em class="replaceable"><code>tablename</code></em>

Close the open table. The name of the table must be given as a cross-check.

`insert` `(` [<em class="replaceable"><code>oid&#95;value</code></em>] <em class="replaceable"><code>value1</code></em> <em class="replaceable"><code>value2</code></em> ... `)`

Insert a new row into the open table using <em class="replaceable"><code>value1</code></em>, <em class="replaceable"><code>value2</code></em>, etc., for its column values.

NULL values can be specified using the special key word `_null_`. Values that do not look like identifiers or digit strings must be single-quoted. (To include a single quote in a value, write it twice. Escape-string-style backslash escapes are allowed in the string, too.)

`declare` [`unique`] `index` <em class="replaceable"><code>indexname</code></em> <em class="replaceable"><code>indexoid</code></em> `on` <em class="replaceable"><code>tablename</code></em> `using` <em class="replaceable"><code>amname</code></em> `(` <em class="replaceable"><code>opclass1</code></em> <em class="replaceable"><code>name1</code></em> [, ...] `)`

Create an index named <em class="replaceable"><code>indexname</code></em>, having OID <em class="replaceable"><code>indexoid</code></em>, on the table named <em class="replaceable"><code>tablename</code></em>, using the <em class="replaceable"><code>amname</code></em> access method. The fields to index are called <em class="replaceable"><code>name1</code></em>, <em class="replaceable"><code>name2</code></em> etc., and the operator classes to use are <em class="replaceable"><code>opclass1</code></em>, <em class="replaceable"><code>opclass2</code></em> etc., respectively. The index file is created and appropriate catalog entries are made for it, but the index contents are not initialized by this command.

`declare toast` <em class="replaceable"><code>toasttableoid</code></em> <em class="replaceable"><code>toastindexoid</code></em> `on` <em class="replaceable"><code>tablename</code></em>

Create a TOAST table for the table named <em class="replaceable"><code>tablename</code></em>. The TOAST table is assigned OID <em class="replaceable"><code>toasttableoid</code></em> and its index is assigned OID <em class="replaceable"><code>toastindexoid</code></em>. As with `declare index`, filling of the index is postponed.

`build indices`

Fill in the indices that have previously been declared.

---

原文：[PostgreSQL 15.19 Documentation](bki-commands.md)（英文原文，待翻譯）
