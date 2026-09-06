## Chapter 13. Concurrency Control

**Table of Contents**

[13.1. Introduction](mvcc-intro.md)

[13.2. Transaction Isolation](transaction-iso.md)
:   [13.2.1. Read Committed Isolation Level](transaction-iso.md#XACT-READ-COMMITTED)

    [13.2.2. Repeatable Read Isolation Level](transaction-iso.md#XACT-REPEATABLE-READ)

    [13.2.3. Serializable Isolation Level](transaction-iso.md#XACT-SERIALIZABLE)

[13.3. Explicit Locking](explicit-locking.md)
:   [13.3.1. Table-Level Locks](explicit-locking.md#LOCKING-TABLES)

    [13.3.2. Row-Level Locks](explicit-locking.md#LOCKING-ROWS)

    [13.3.3. Page-Level Locks](explicit-locking.md#LOCKING-PAGES)

    [13.3.4. Deadlocks](explicit-locking.md#LOCKING-DEADLOCKS)

    [13.3.5. Advisory Locks](explicit-locking.md#ADVISORY-LOCKS)

[13.4. Data Consistency Checks at the Application Level](applevel-consistency.md)
:   [13.4.1. Enforcing Consistency with Serializable Transactions](applevel-consistency.md#SERIALIZABLE-CONSISTENCY)

    [13.4.2. Enforcing Consistency with Explicit Blocking Locks](applevel-consistency.md#NON-SERIALIZABLE-CONSISTENCY)

[13.5. Serialization Failure Handling](mvcc-serialization-failure-handling.md)

[13.6. Caveats](mvcc-caveats.md)

[13.7. Locking and Indexes](locking-indexes.md)

<a id="id-1.5.12.2"></a>

This chapter describes the behavior of the
PostgreSQL database system when two or
more sessions try to access the same data at the same time. The
goals in that situation are to allow efficient access for all
sessions while maintaining strict data integrity. Every developer
of database applications should be familiar with the topics covered
in this chapter.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/mvcc.html)（英文原文，待翻譯）
