# 5.4. 系統欄位[^1]

very table has several_system columns_that are implicitly defined by the system. Therefore, these names cannot be used as names of user-defined columns. \(Note that these restrictions are separate from whether the name is a key word or not; quoting a name will not allow you to escape these restrictions.\) You do not really need to be concerned about these columns; just know they exist.



`oid`

The object identifier \(object ID\) of a row. This column is only present if the table was created using`WITH OIDS`, or if the[default\_with\_oids](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#guc-default-with-oids)configuration variable was set at the time. This column is of type`oid`\(same name as the column\); see[Section 8.18](https://www.postgresql.org/docs/10/static/datatype-oid.html)for more information about the type.

`tableoid`



The OID of the table containing this row. This column is particularly handy for queries that select from inheritance hierarchies \(see[Section 5.9](https://www.postgresql.org/docs/10/static/ddl-inherit.html)\), since without it, it's difficult to tell which individual table a row came from. The`tableoid`can be joined against the`oid`column of`pg_class`to obtain the table name.

`xmin`



The identity \(transaction ID\) of the inserting transaction for this row version. \(A row version is an individual state of a row; each update of a row creates a new row version for the same logical row.\)

`cmin`



The command identifier \(starting at zero\) within the inserting transaction.

`xmax`



The identity \(transaction ID\) of the deleting transaction, or zero for an undeleted row version. It is possible for this column to be nonzero in a visible row version. That usually indicates that the deleting transaction hasn't committed yet, or that an attempted deletion was rolled back.

`cmax`



The command identifier within the deleting transaction, or zero.

`ctid`



The physical location of the row version within its table. Note that although the`ctid`can be used to locate the row version very quickly, a row's`ctid`will change if it is updated or moved by`VACUUM FULL`. Therefore`ctid`is useless as a long-term row identifier. The OID, or even better a user-defined serial number, should be used to identify logical rows.

OIDs are 32-bit quantities and are assigned from a single cluster-wide counter. In a large or long-lived database, it is possible for the counter to wrap around. Hence, it is bad practice to assume that OIDs are unique, unless you take steps to ensure that this is the case. If you need to identify the rows in a table, using a sequence generator is strongly recommended. However, OIDs can be used as well, provided that a few additional precautions are taken:

* A unique constraint should be created on the OID column of each table for which the OID will be used to identify rows. When such a unique constraint \(or unique index\) exists, the system takes care not to generate an OID matching an already-existing row. \(Of course, this is only possible if the table contains fewer than 232\(4 billion\) rows, and in practice the table size had better be much less than that, or performance might suffer.\)

* OIDs should never be assumed to be unique across tables; use the combination of`tableoid`and row OID if you need a database-wide identifier.

* Of course, the tables in question must be created`WITH OIDS`. As ofPostgreSQL8.1,`WITHOUT OIDS`is the default.

Transaction identifiers are also 32-bit quantities. In a long-lived database it is possible for transaction IDs to wrap around. This is not a fatal problem given appropriate maintenance procedures; see[Chapter 24](https://www.postgresql.org/docs/10/static/maintenance.html)for details. It is unwise, however, to depend on the uniqueness of transaction IDs over the long term \(more than one billion transactions\).

Command identifiers are also 32-bit quantities. This creates a hard limit of 232\(4 billion\)SQLcommands within a single transaction. In practice this limit is not a problem — note that the limit is on the number ofSQLcommands, not the number of rows processed. Also, only commands that actually modify the database contents will consume a command identifier.

---



[^1]: [PostgreSQL: Documentation: 10: 5.4. System Columns](https://www.postgresql.org/docs/10/static/ddl-system-columns.html)

