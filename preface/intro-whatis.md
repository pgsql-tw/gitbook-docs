## 1.  What Is PostgreSQL? [#](#INTRO-WHATIS)

PostgreSQL is an object-relational
database management system (ORDBMS) based on
[POSTGRES, Version 4.2](https://dsf.berkeley.edu/postgres.html),
developed at the University of California at Berkeley Computer Science
Department. POSTGRES pioneered many concepts that only became
available in some commercial database systems much later.

PostgreSQL is an open-source descendant
of this original Berkeley code. It supports a large part of the SQL
standard and offers many modern features:

* [complex queries](../the-sql-language/README.md)
* [foreign keys](../the-sql-language/ddl/ddl-constraints.md#DDL-CONSTRAINTS-FK)
* [triggers](../server-programming/triggers/README.md)
* [updatable views](../reference/sql-commands/sql-createview.md#SQL-CREATEVIEW-UPDATABLE-VIEWS)
* [transactional integrity](../the-sql-language/mvcc/transaction-iso.md)
* [multiversion concurrency control](../the-sql-language/mvcc/README.md)

Also, PostgreSQL can be extended by the
user in many ways, for example by adding new

* [data types](../the-sql-language/datatype/README.md)
* [functions](../the-sql-language/functions/README.md)
* [operators](../the-sql-language/functions/README.md)
* [aggregate functions](../the-sql-language/functions/functions-aggregate.md)
* [index methods](../the-sql-language/indexes/README.md)
* [procedural languages](../server-programming/README.md)

And because of the liberal license,
PostgreSQL can be used, modified, and
distributed by anyone free of charge for any purpose, be it
private, commercial, or academic.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/intro-whatis.html)（英文原文，待翻譯）
