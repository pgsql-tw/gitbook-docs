# 8.6. 布林型別[^1]

PostgreSQLprovides the standardSQLtypeboolean; see[Table 8-19](https://www.postgresql.org/docs/current/static/datatype-boolean.html#DATATYPE-BOOLEAN-TABLE). Thebooleantype can have several states:"true","false", and a third state,"unknown", which is represented by theSQLnull value.



Table 8-19. Boolean Data Type

| Name | Storage Size | Description |
| :--- | :--- | :--- |
| boolean | 1 byte | state of true or false |

Valid literal values for the"true"state are:

| TRUE |
| :--- |
| 't' |
| 'true' |
| 'y' |
| 'yes' |
| 'on' |
| '1' |

For the

"false"

state, the following values can be used:

| FALSE |
| :--- |
| 'f' |
| 'false' |
| 'n' |
| 'no' |
| 'off' |
| '0' |

Leading or trailing whitespace is ignored, and case does not matter. The key words

TRUE

and

FALSE

are the preferred \(

SQL

-compliant\) usage.

[Example 8-2](https://www.postgresql.org/docs/current/static/datatype-boolean.html#DATATYPE-BOOLEAN-EXAMPLE)shows thatbooleanvalues are output using the letterstandf.



Example 8-2. Using thebooleanType

```
CREATE TABLE test1 (a boolean, b text);
INSERT INTO test1 VALUES (TRUE, 'sic est');
INSERT INTO test1 VALUES (FALSE, 'non est');
SELECT * FROM test1;
 a |    b
---+---------
 t | sic est
 f | non est

SELECT * FROM test1 WHERE a;
 a |    b
---+---------
 t | sic est

```

---

  


[^1]: [PostgreSQL: Documentation: 9.6: Boolean Type](https://www.postgresql.org/docs/current/static/datatype-boolean.html)

