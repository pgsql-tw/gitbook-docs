## 13.6. Caveats [#](#MVCC-CAVEATS)

Some DDL commands, currently only [`TRUNCATE`](../../reference/sql-commands/sql-truncate.md) and the
table-rewriting forms of [`ALTER TABLE`](../../reference/sql-commands/sql-altertable.md), are not
MVCC-safe. This means that after the truncation or rewrite commits, the
table will appear empty to concurrent transactions, if they are using a
snapshot taken before the DDL command committed. This will only be an
issue for a transaction that did not access the table in question
before the DDL command started — any transaction that has done so
would hold at least an `ACCESS SHARE` table lock,
which would block the DDL command until that transaction completes.
So these commands will not cause any apparent inconsistency in the
table contents for successive queries on the target table, but they
could cause visible inconsistency between the contents of the target
table and other tables in the database.

Support for the Serializable transaction isolation level has not yet
been added to hot standby replication targets (described in
[Section 26.4](../../server-administration/high-availability/hot-standby.md)). The strictest isolation level currently
supported in hot standby mode is Repeatable Read. While performing all
permanent database writes within Serializable transactions on the
primary will ensure that all standbys will eventually reach a consistent
state, a Repeatable Read transaction run on the standby can sometimes
see a transient state that is inconsistent with any serial execution
of the transactions on the primary.

Internal access to the system catalogs is not done using the isolation
level of the current transaction. This means that newly created database
objects such as tables are visible to concurrent Repeatable Read and
Serializable transactions, even though the rows they contain are not. In
contrast, queries that explicitly examine the system catalogs don't see
rows representing concurrently created database objects, in the higher
isolation levels.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/mvcc-caveats.html)（英文原文，待翻譯）
