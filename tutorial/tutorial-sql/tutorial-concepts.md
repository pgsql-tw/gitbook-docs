## 2.2. Concepts [#](#TUTORIAL-CONCEPTS)

<a id="id-1.4.4.3.2.1"></a>
<a id="id-1.4.4.3.2.2"></a>
<a id="id-1.4.4.3.2.3"></a>
<a id="id-1.4.4.3.2.4"></a>
<a id="id-1.4.4.3.2.5"></a>
PostgreSQL is a *relational
database management system* (RDBMS).
That means it is a system for managing data stored in
*relations*. Relation is essentially a
mathematical term for *table*. The notion of
storing data in tables is so commonplace today that it might
seem inherently obvious, but there are a number of other ways of
organizing databases. Files and directories on Unix-like
operating systems form an example of a hierarchical database. A
more modern development is the object-oriented database.

<a id="id-1.4.4.3.3.1"></a>
<a id="id-1.4.4.3.3.2"></a>
Each table is a named collection of *rows*.
Each row of a given table has the same set of named
*columns*,
and each column is of a specific data type. Whereas columns have
a fixed order in each row, it is important to remember that SQL
does not guarantee the order of the rows within the table in any
way (although they can be explicitly sorted for display).

<a id="id-1.4.4.3.4.1"></a>
<a id="id-1.4.4.3.4.2"></a>
Tables are grouped into databases, and a collection of databases
managed by a single PostgreSQL server
instance constitutes a database *cluster*.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-concepts.html)（英文原文，待翻譯）
