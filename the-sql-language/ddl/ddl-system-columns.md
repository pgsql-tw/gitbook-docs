## 5.6. System Columns [#](#DDL-SYSTEM-COLUMNS)

Every table has several *system columns* that are
implicitly defined by the system. Therefore, these names cannot be
used as names of user-defined columns. (Note that these
restrictions are separate from whether the name is a key word or
not; quoting a name will not allow you to escape these
restrictions.) You do not really need to be concerned about these
columns; just know they exist.

<a id="id-1.5.4.8.3"></a>

<a id="DDL-SYSTEM-COLUMNS-TABLEOID"></a>

`tableoid` [#](#DDL-SYSTEM-COLUMNS-TABLEOID)
:   <a id="id-1.5.4.8.4.1.2.1"></a>

    The OID of the table containing this row. This column is
    particularly handy for queries that select from partitioned
    tables (see [Section 5.12](ddl-partitioning.md)) or inheritance
    hierarchies (see [Section 5.11](ddl-inherit.md)), since without it,
    it's difficult to tell which individual table a row came from. The
    `tableoid` can be joined against the
    `oid` column of
    `pg_class` to obtain the table name.
<a id="DDL-SYSTEM-COLUMNS-XMIN"></a>

`xmin` [#](#DDL-SYSTEM-COLUMNS-XMIN)
:   <a id="id-1.5.4.8.4.2.2.1"></a>

    The identity (transaction ID) of the inserting transaction for
    this row version. (A row version is an individual state of a
    row; each update of a row creates a new row version for the same
    logical row.)
<a id="DDL-SYSTEM-COLUMNS-CMIN"></a>

`cmin` [#](#DDL-SYSTEM-COLUMNS-CMIN)
:   <a id="id-1.5.4.8.4.3.2.1"></a>

    The command identifier (starting at zero) within the inserting
    transaction.
<a id="DDL-SYSTEM-COLUMNS-XMAX"></a>

`xmax` [#](#DDL-SYSTEM-COLUMNS-XMAX)
:   <a id="id-1.5.4.8.4.4.2.1"></a>

    The identity (transaction ID) of the deleting transaction, or
    zero for an undeleted row version. It is possible for this column to
    be nonzero in a visible row version. That usually indicates that the
    deleting transaction hasn't committed yet, or that an attempted
    deletion was rolled back.
<a id="DDL-SYSTEM-COLUMNS-CMAX"></a>

`cmax` [#](#DDL-SYSTEM-COLUMNS-CMAX)
:   <a id="id-1.5.4.8.4.5.2.1"></a>

    The command identifier within the deleting transaction, or zero.
<a id="DDL-SYSTEM-COLUMNS-CTID"></a>

`ctid` [#](#DDL-SYSTEM-COLUMNS-CTID)
:   <a id="id-1.5.4.8.4.6.2.1"></a>

    The physical location of the row version within its table. Note that
    although the `ctid` can be used to
    locate the row version very quickly, a row's
    `ctid` will change if it is
    updated or moved by `VACUUM FULL`. Therefore
    `ctid` should not be used as a row
    identifier. A primary key should be used to identify logical rows.

Transaction identifiers are also 32-bit quantities. In a
long-lived database it is possible for transaction IDs to wrap
around. This is not a fatal problem given appropriate maintenance
procedures; see [Chapter 24](../../server-administration/maintenance/README.md) for details. It is
unwise, however, to depend on the uniqueness of transaction IDs
over the long term (more than one billion transactions).

Command identifiers are also 32-bit quantities. This creates a hard limit
of 232 (4 billion) SQL commands
within a single transaction. In practice this limit is not a
problem — note that the limit is on the number of
SQL commands, not the number of rows processed.
Also, only commands that actually modify the database contents will
consume a command identifier.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ddl-system-columns.html)（英文原文，待翻譯）
