## 13.1. Introduction [#](#MVCC-INTRO)

<a id="id-1.5.12.4.2"></a><a id="id-1.5.12.4.3"></a><a id="id-1.5.12.4.4"></a><a id="id-1.5.12.4.5"></a>

PostgreSQL provides a rich set of tools
for developers to manage concurrent access to data. Internally,
data consistency is maintained by using a multiversion
model (Multiversion Concurrency Control, MVCC).
This means that each SQL statement sees
a snapshot of data (a *database version*)
as it was some
time ago, regardless of the current state of the underlying data.
This prevents statements from viewing inconsistent data produced
by concurrent transactions performing updates on the same
data rows, providing *transaction isolation*
for each database session. MVCC, by eschewing
the locking methodologies of traditional database systems,
minimizes lock contention in order to allow for reasonable
performance in multiuser environments.

The main advantage of using the MVCC model of
concurrency control rather than locking is that in
MVCC locks acquired for querying (reading) data
do not conflict with locks acquired for writing data, and so
reading never blocks writing and writing never blocks reading.
PostgreSQL maintains this guarantee
even when providing the strictest level of transaction
isolation through the use of an innovative *Serializable
Snapshot Isolation* (SSI) level.

Table- and row-level locking facilities are also available in
PostgreSQL for applications which don't
generally need full transaction isolation and prefer to explicitly
manage particular points of conflict. However, proper
use of MVCC will generally provide better
performance than locks. In addition, application-defined advisory
locks provide a mechanism for acquiring locks that are not tied
to a single transaction.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/mvcc-intro.html)（英文原文，待翻譯）
