## WHENEVER

WHENEVER — specify the action to be taken when an SQL statement causes a specific class condition to be raised

## Synopsis

```

WHENEVER { NOT FOUND | SQLERROR | SQLWARNING } action
```

<a id="id-1.7.5.20.19.3"></a>

## Description

Define a behavior which is called on the special cases (Rows not
found, SQL warnings or errors) in the result of SQL execution.

<a id="id-1.7.5.20.19.4"></a>

## Parameters

See [Section 34.8.1](ecpg-errors.md#ECPG-WHENEVER) for a description of the
parameters.

<a id="id-1.7.5.20.19.5"></a>

## Examples

```

EXEC SQL WHENEVER NOT FOUND CONTINUE;
EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER NOT FOUND DO CONTINUE;
EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLWARNING DO warn();
EXEC SQL WHENEVER SQLERROR sqlprint;
EXEC SQL WHENEVER SQLERROR CALL print2();
EXEC SQL WHENEVER SQLERROR DO handle_error("select");
EXEC SQL WHENEVER SQLERROR DO sqlnotice(NULL, NONO);
EXEC SQL WHENEVER SQLERROR DO sqlprint();
EXEC SQL WHENEVER SQLERROR GOTO error_label;
EXEC SQL WHENEVER SQLERROR STOP;
```

A typical application is the use of `WHENEVER NOT FOUND
BREAK` to handle looping through result sets:

```

int
main(void)
{
    EXEC SQL CONNECT TO testdb AS con1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database(), 'hoge', 256;
    EXEC SQL OPEN cur;

    /* when end of result set reached, break out of while loop */
    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;
        ...
    }

    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

<a id="id-1.7.5.20.19.6"></a>

## Compatibility

`WHENEVER` is specified in the SQL standard, but
most of the actions are PostgreSQL extensions.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-whenever.html)（英文原文，待翻譯）
