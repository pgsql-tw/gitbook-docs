# II. SQL查詢語言[^1]

This part describes the use of theSQLlanguage inPostgreSQL. We start with describing the general syntax ofSQL, then explain how to create the structures to hold data, how to populate the database, and how to query it. The middle part lists the available data types and functions for use inSQLcommands. The rest treats several aspects that are important for tuning a database for optimal performance.

The information in this part is arranged so that a novice user can follow it start to end to gain a full understanding of the topics without having to refer forward too many times. The chapters are intended to be self-contained, so that advanced users can read the chapters individually as they choose. The information in this part is presented in a narrative fashion in topical units. Readers looking for a complete description of a particular command should see[Part VI](https://www.postgresql.org/docs/10/static/reference.html).

Readers of this part should know how to connect to aPostgreSQLdatabase and issueSQLcommands. Readers that are unfamiliar with these issues are encouraged to read[Part I](https://www.postgresql.org/docs/10/static/tutorial.html)first.SQLcommands are typically entered using thePostgreSQLinteractive terminalpsql, but other programs that have similar functionality can be used as well.

---

[^1]: [PostgreSQL: Documentation: 10: Part II. The SQL Language](https://www.postgresql.org/docs/10/static/sql.html)

