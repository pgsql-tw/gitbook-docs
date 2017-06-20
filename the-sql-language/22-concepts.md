# 2.2. 概念[^1]

PostgreSQLis a_relational database management system_\(RDBMS\). That means it is a system for managing data stored in_relations_. Relation is essentially a mathematical term for_table_. The notion of storing data in tables is so commonplace today that it might seem inherently obvious, but there are a number of other ways of organizing databases. Files and directories on Unix-like operating systems form an example of a hierarchical database. A more modern development is the object-oriented database.

Each table is a named collection of_rows_. Each row of a given table has the same set of named_columns_, and each column is of a specific data type. Whereas columns have a fixed order in each row, it is important to remember that SQL does not guarantee the order of the rows within the table in any way \(although they can be explicitly sorted for display\).

Tables are grouped into databases, and a collection of databases managed by a singlePostgreSQLserver instance constitutes a database_cluster_.

---

[^1]: [PostgreSQL: Documentation: 10: 2.2. Concepts](https://www.postgresql.org/docs/10/static/tutorial-concepts.html)

