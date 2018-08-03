# H.1. 用戶端介面



There are only two client interfaces included in the base PostgreSQL distribution:

* [libpq](https://www.postgresql.org/docs/10/static/libpq.html) is included because it is the primary C language interface, and because many other client interfaces are built on top of it.
* [ECPG](https://www.postgresql.org/docs/10/static/ecpg.html) is included because it depends on the server-side SQL grammar, and is therefore sensitive to changes in PostgreSQL itself.

All other language interfaces are external projects and are distributed separately. [Table H.1](https://www.postgresql.org/docs/10/static/external-interfaces.html#LANGUAGE-INTERFACE-TABLE) includes a list of some of these projects. Note that some of these packages might not be released under the same license as PostgreSQL. For more information on each language interface, including licensing terms, refer to its website and documentation.

**Table H.1. Externally Maintained Client Interfaces**

| Name | Language | Comments | Website |
| :--- | :--- | :--- | :--- |
| DBD::Pg | Perl | Perl DBI driver | [http://search.cpan.org/dist/DBD-Pg/](http://search.cpan.org/dist/DBD-Pg/) |
| JDBC | Java | Type 4 JDBC driver | [https://jdbc.postgresql.org/](https://jdbc.postgresql.org/) |
| libpqxx | C++ | New-style C++ interface | [http://pqxx.org/](http://pqxx.org/) |
| node-postgres | JavaScript | Node.js driver | [https://node-postgres.com/](https://node-postgres.com/) |
| Npgsql | .NET | .NET data provider | [http://www.npgsql.org/](http://www.npgsql.org/) |
| pgtcl | Tcl |   | [https://github.com/flightaware/Pgtcl](https://github.com/flightaware/Pgtcl) |
| pgtclng | Tcl |   | [http://sourceforge.net/projects/pgtclng/](http://sourceforge.net/projects/pgtclng/) |
| pq | Go | Pure Go driver for Go's database/sql | [https://github.com/lib/pq](https://github.com/lib/pq) |
| psqlODBC | ODBC | ODBC driver | [https://odbc.postgresql.org/](https://odbc.postgresql.org/) |
| psycopg | Python | DB API 2.0-compliant | [http://initd.org/psycopg/](http://initd.org/psycopg/) |

