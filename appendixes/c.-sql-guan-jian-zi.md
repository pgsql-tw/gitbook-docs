# C. SQL 關鍵字

[Table C.1](c.-sql-guan-jian-zi.md#table-c-1-sql-key-words) lists all tokens that are key words in the SQL standard and in PostgreSQL 11devel. Background information can be found in [Section 4.1.1](../the-sql-language/sql-syntax/lexical-structure.md#4-1-1-identifier-he-zi-keyword). (For space reasons, only the latest two versions of the SQL standard, and SQL-92 for historical comparison, are included. The differences between those and the other intermediate standard versions are small.)

SQL distinguishes between _reserved_ and _non-reserved_ key words. According to the standard, reserved key words are the only real key words; they are never allowed as identifiers. Non-reserved key words only have a special meaning in particular contexts and can be used as identifiers in other contexts. Most non-reserved key words are actually the names of built-in tables and functions specified by SQL. The concept of non-reserved key words essentially only exists to declare that some predefined meaning is attached to a word in some contexts.

In the PostgreSQL parser life is a bit more complicated. There are several different classes of tokens ranging from those that can never be used as an identifier to those that have absolutely no special status in the parser as compared to an ordinary identifier. (The latter is usually the case for functions specified by SQL.) Even reserved key words are not completely reserved in PostgreSQL, but can be used as column labels (for example, `SELECT 55 AS CHECK`, even though `CHECK` is a reserved key word).

In [Table C.1](https://www.postgresql.org/docs/devel/static/sql-keywords-appendix.html#KEYWORDS-TABLE) in the column for PostgreSQL we classify as “non-reserved” those key words that are explicitly known to the parser but are allowed as column or table names. Some key words that are otherwise non-reserved cannot be used as function or data type names and are marked accordingly. (Most of these words represent built-in functions or data types with special syntax. The function or type is still available but it cannot be redefined by the user.) Labeled “reserved” are those tokens that are not allowed as column or table names. Some reserved key words are allowable as names for functions or data types; this is also shown in the table. If not so marked, a reserved key word is only allowed as an “AS” column label name.

As a general rule, if you get spurious parser errors for commands that contain any of the listed key words as an identifier you should try to quote the identifier to see if the problem goes away.

It is important to understand before studying [Table C.1](https://www.postgresql.org/docs/devel/static/sql-keywords-appendix.html#KEYWORDS-TABLE) that the fact that a key word is not reserved in PostgreSQL does not mean that the feature related to the word is not implemented. Conversely, the presence of a key word does not indicate the existence of a feature.

#### **Table C.1. SQL Key Words**

| Key Word                | PostgreSQL                                | SQL:2011     | SQL:2008     | SQL-92       |
| ----------------------- | ----------------------------------------- | ------------ | ------------ | ------------ |
| `A`                     |                                           | non-reserved | non-reserved |              |
| `ABORT`                 | non-reserved                              |              |              |              |
| `ABS`                   |                                           | reserved     | reserved     |              |
| `ABSENT`                |                                           | non-reserved | non-reserved |              |
| `ABSOLUTE`              | non-reserved                              | non-reserved | non-reserved | reserved     |
| `ACCESS`                | non-reserved                              |              |              |              |
| `ACCORDING`             |                                           | non-reserved | non-reserved |              |
| `ACTION`                | non-reserved                              | non-reserved | non-reserved | reserved     |
| `ADA`                   |                                           | non-reserved | non-reserved | non-reserved |
| `ADD`                   | non-reserved                              | non-reserved | non-reserved | reserved     |
| `ADMIN`                 | non-reserved                              | non-reserved | non-reserved |              |
| `AFTER`                 | non-reserved                              | non-reserved | non-reserved |              |
| `AGGREGATE`             | non-reserved                              |              |              |              |
| `ALL`                   | reserved                                  | reserved     | reserved     | reserved     |
| `ALLOCATE`              |                                           | reserved     | reserved     | reserved     |
| `ALSO`                  | non-reserved                              |              |              |              |
| `ALTER`                 | non-reserved                              | reserved     | reserved     | reserved     |
| `ALWAYS`                | non-reserved                              | non-reserved | non-reserved |              |
| `ANALYSE`               | reserved                                  |              |              |              |
| `ANALYZE`               | reserved                                  |              |              |              |
| `AND`                   | reserved                                  | reserved     | reserved     | reserved     |
| `ANY`                   | reserved                                  | reserved     | reserved     | reserved     |
| `ARE`                   |                                           | reserved     | reserved     | reserved     |
| `ARRAY`                 | reserved                                  | reserved     | reserved     |              |
| `ARRAY_AGG`             |                                           | reserved     | reserved     |              |
| `ARRAY_MAX_CARDINALITY` |                                           | reserved     |              |              |
| `AS`                    | reserved                                  | reserved     | reserved     | reserved     |
| `ASC`                   | reserved                                  | non-reserved | non-reserved | reserved     |
| `ASENSITIVE`            |                                           | reserved     | reserved     |              |
| `ASSERTION`             | non-reserved                              | non-reserved | non-reserved | reserved     |
| `ASSIGNMENT`            | non-reserved                              | non-reserved | non-reserved |              |
| `ASYMMETRIC`            | reserved                                  | reserved     | reserved     |              |
| `AT`                    | non-reserved                              | reserved     | reserved     | reserved     |
| `ATOMIC`                |                                           | reserved     | reserved     |              |
| `ATTACH`                | non-reserved                              |              |              |              |
| `ATTRIBUTE`             | non-reserved                              | non-reserved | non-reserved |              |
| `ATTRIBUTES`            |                                           | non-reserved | non-reserved |              |
| `AUTHORIZATION`         | reserved (can be function or type)        | reserved     | reserved     | reserved     |
| `AVG`                   |                                           | reserved     | reserved     | reserved     |
| `BACKWARD`              | non-reserved                              |              |              |              |
| `BASE64`                |                                           | non-reserved | non-reserved |              |
| `BEFORE`                | non-reserved                              | non-reserved | non-reserved |              |
| `BEGIN`                 | non-reserved                              | reserved     | reserved     | reserved     |
| `BEGIN_FRAME`           |                                           | reserved     |              |              |
| `BEGIN_PARTITION`       |                                           | reserved     |              |              |
| `BERNOULLI`             |                                           | non-reserved | non-reserved |              |
| `BETWEEN`               | non-reserved (cannot be function or type) | reserved     | reserved     | reserved     |
| `BIGINT`                | non-reserved (cannot be function or type) | reserved     | reserved     |              |
| `BINARY`                | reserved (can be function or type)        | reserved     | reserved     |              |
| `BIT`                   | non-reserved (cannot be function or type) |              |              | reserved     |
| `BIT_LENGTH`            |                                           |              |              | reserved     |
| `BLOB`                  |                                           | reserved     | reserved     |              |
| `BLOCKED`               |                                           | non-reserved | non-reserved |              |
| `BOM`                   |                                           | non-reserved | non-reserved |              |
| `BOOLEAN`               | non-reserved (cannot be function or type) | reserved     | reserved     |              |
| `BOTH`                  | reserved                                  | reserved     | reserved     | reserved     |
| `BREADTH`               |                                           | non-reserved | non-reserved |              |
| `BY`                    | non-reserved                              | reserved     | reserved     | reserved     |

| `C`                                |                                           | non-reserved | non-reserved | non-reserved |
| ---------------------------------- | ----------------------------------------- | ------------ | ------------ | ------------ |
| `CACHE`                            | non-reserved                              |              |              |              |
| `CALL`                             |                                           | reserved     | reserved     |              |
| `CALLED`                           | non-reserved                              | reserved     | reserved     |              |
| `CARDINALITY`                      |                                           | reserved     | reserved     |              |
| `CASCADE`                          | non-reserved                              | non-reserved | non-reserved | reserved     |
| `CASCADED`                         | non-reserved                              | reserved     | reserved     | reserved     |
| `CASE`                             | reserved                                  | reserved     | reserved     | reserved     |
| `CAST`                             | reserved                                  | reserved     | reserved     | reserved     |
| `CATALOG`                          | non-reserved                              | non-reserved | non-reserved | reserved     |
| `CATALOG_NAME`                     |                                           | non-reserved | non-reserved | non-reserved |
| `CEIL`                             |                                           | reserved     | reserved     |              |
| `CEILING`                          |                                           | reserved     | reserved     |              |
| `CHAIN`                            | non-reserved                              | non-reserved | non-reserved |              |
| `CHAR`                             | non-reserved (cannot be function or type) | reserved     | reserved     | reserved     |
| `CHARACTER`                        | non-reserved (cannot be function or type) | reserved     | reserved     | reserved     |
| `CHARACTERISTICS`                  | non-reserved                              | non-reserved | non-reserved |              |
| `CHARACTERS`                       |                                           | non-reserved | non-reserved |              |
| `CHARACTER_LENGTH`                 |                                           | reserved     | reserved     | reserved     |
| `CHARACTER_SET_CATALOG`            |                                           | non-reserved | non-reserved | non-reserved |
| `CHARACTER_SET_NAME`               |                                           | non-reserved | non-reserved | non-reserved |
| `CHARACTER_SET_SCHEMA`             |                                           | non-reserved | non-reserved | non-reserved |
| `CHAR_LENGTH`                      |                                           | reserved     | reserved     | reserved     |
| `CHECK`                            | reserved                                  | reserved     | reserved     | reserved     |
| `CHECKPOINT`                       | non-reserved                              |              |              |              |
| `CLASS`                            | non-reserved                              |              |              |              |
| `CLASS_ORIGIN`                     |                                           | non-reserved | non-reserved | non-reserved |
| `CLOB`                             |                                           | reserved     | reserved     |              |
| `CLOSE`                            | non-reserved                              | reserved     | reserved     | reserved     |
| `CLUSTER`                          | non-reserved                              |              |              |              |
| `COALESCE`                         | non-reserved (cannot be function or type) | reserved     | reserved     | reserved     |
| `COBOL`                            |                                           | non-reserved | non-reserved | non-reserved |
| `COLLATE`                          | reserved                                  | reserved     | reserved     | reserved     |
| `COLLATION`                        | reserved (can be function or type)        | non-reserved | non-reserved | reserved     |
| `COLLATION_CATALOG`                |                                           | non-reserved | non-reserved | non-reserved |
| `COLLATION_NAME`                   |                                           | non-reserved | non-reserved | non-reserved |
| `COLLATION_SCHEMA`                 |                                           | non-reserved | non-reserved | non-reserved |
| `COLLECT`                          |                                           | reserved     | reserved     |              |
| `COLUMN`                           | reserved                                  | reserved     | reserved     | reserved     |
| `COLUMNS`                          | non-reserved                              | non-reserved | non-reserved |              |
| `COLUMN_NAME`                      |                                           | non-reserved | non-reserved | non-reserved |
| `COMMAND_FUNCTION`                 |                                           | non-reserved | non-reserved | non-reserved |
| `COMMAND_FUNCTION_CODE`            |                                           | non-reserved | non-reserved |              |
| `COMMENT`                          | non-reserved                              |              |              |              |
| `COMMENTS`                         | non-reserved                              |              |              |              |
| `COMMIT`                           | non-reserved                              | reserved     | reserved     | reserved     |
| `COMMITTED`                        | non-reserved                              | non-reserved | non-reserved | non-reserved |
| `CONCURRENTLY`                     | reserved (can be function or type)        |              |              |              |
| `CONDITION`                        |                                           | reserved     | reserved     |              |
| `CONDITION_NUMBER`                 |                                           | non-reserved | non-reserved | non-reserved |
| `CONFIGURATION`                    | non-reserved                              |              |              |              |
| `CONFLICT`                         | non-reserved                              |              |              |              |
| `CONNECT`                          |                                           | reserved     | reserved     | reserved     |
| `CONNECTION`                       | non-reserved                              | non-reserved | non-reserved | reserved     |
| `CONNECTION_NAME`                  |                                           | non-reserved | non-reserved | non-reserved |
| `CONSTRAINT`                       | reserved                                  | reserved     | reserved     | reserved     |
| `CONSTRAINTS`                      | non-reserved                              | non-reserved | non-reserved | reserved     |
| `CONSTRAINT_CATALOG`               |                                           | non-reserved | non-reserved | non-reserved |
| `CONSTRAINT_NAME`                  |                                           | non-reserved | non-reserved | non-reserved |
| `CONSTRAINT_SCHEMA`                |                                           | non-reserved | non-reserved | non-reserved |
| `CONSTRUCTOR`                      |                                           | non-reserved | non-reserved |              |
| `CONTAINS`                         |                                           | reserved     | non-reserved |              |
| `CONTENT`                          | non-reserved                              | non-reserved | non-reserved |              |
| `CONTINUE`                         | non-reserved                              | non-reserved | non-reserved | reserved     |
| `CONTROL`                          |                                           | non-reserved | non-reserved |              |
| `CONVERSION`                       | non-reserved                              |              |              |              |
| `CONVERT`                          |                                           | reserved     | reserved     | reserved     |
| `COPY`                             | non-reserved                              |              |              |              |
| `CORR`                             |                                           | reserved     | reserved     |              |
| `CORRESPONDING`                    |                                           | reserved     | reserved     | reserved     |
| `COST`                             | non-reserved                              |              |              |              |
| `COUNT`                            |                                           | reserved     | reserved     | reserved     |
| `COVAR_POP`                        |                                           | reserved     | reserved     |              |
| `COVAR_SAMP`                       |                                           | reserved     | reserved     |              |
| `CREATE`                           | reserved                                  | reserved     | reserved     | reserved     |
| `CROSS`                            | reserved (can be function or type)        | reserved     | reserved     | reserved     |
| `CSV`                              | non-reserved                              |              |              |              |
| `CUBE`                             | non-reserved                              | reserved     | reserved     |              |
| `CUME_DIST`                        |                                           | reserved     | reserved     |              |
| `CURRENT`                          | non-reserved                              | reserved     | reserved     | reserved     |
| `CURRENT_CATALOG`                  | reserved                                  | reserved     | reserved     |              |
| `CURRENT_DATE`                     | reserved                                  | reserved     | reserved     | reserved     |
| `CURRENT_DEFAULT_TRANSFORM_GROUP`  |                                           | reserved     | reserved     |              |
| `CURRENT_PATH`                     |                                           | reserved     | reserved     |              |
| `CURRENT_ROLE`                     | reserved                                  | reserved     | reserved     |              |
| `CURRENT_ROW`                      |                                           | reserved     |              |              |
| `CURRENT_SCHEMA`                   | reserved (can be function or type)        | reserved     | reserved     |              |
| `CURRENT_TIME`                     | reserved                                  | reserved     | reserved     | reserved     |
| `CURRENT_TIMESTAMP`                | reserved                                  | reserved     | reserved     | reserved     |
| `CURRENT_TRANSFORM_GROUP_FOR_TYPE` |                                           | reserved     | reserved     |              |
| `CURRENT_USER`                     | reserved                                  | reserved     | reserved     | reserved     |
| `CURSOR`                           | non-reserved                              | reserved     | reserved     | reserved     |
| `CURSOR_NAME`                      |                                           | non-reserved | non-reserved | non-reserved |
| `CYCLE`                            | non-reserved                              | reserved     | reserved     |              |
| `DATA`                             | non-reserved                              | non-reserved | non-reserved | non-reserved |
