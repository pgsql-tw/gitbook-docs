<a id="SQL-MOVE"></a><a id="id-1.9.3.157.1"></a><a id="id-1.9.3.157.2"></a>

# MOVE

MOVE — position a cursor

## Synopsis

```

MOVE [ direction ] [ FROM | IN ] cursor_name

where direction can be one of:

    NEXT
    PRIOR
    FIRST
    LAST
    ABSOLUTE count
    RELATIVE count
    count
    ALL
    FORWARD
    FORWARD count
    FORWARD ALL
    BACKWARD
    BACKWARD count
    BACKWARD ALL
```

<a id="id-1.9.3.157.6"></a>

## Description

`MOVE` repositions a cursor without retrieving any data. `MOVE` works exactly like the `FETCH` command, except it only positions the cursor and does not return rows.

The parameters for the `MOVE` command are identical to those of the `FETCH` command; refer to [FETCH](fetch.md) for details on syntax and usage.

<a id="id-1.9.3.157.7"></a>

## Outputs

On successful completion, a `MOVE` command returns a command tag of the form

```

MOVE count
```

The <em class="replaceable"><code>count</code></em> is the number of rows that a `FETCH` command with the same parameters would have returned (possibly zero).

<a id="id-1.9.3.157.8"></a>

## Examples

```

BEGIN WORK;
DECLARE liahona CURSOR FOR SELECT * FROM films;

-- Skip the first 5 rows:
MOVE FORWARD 5 IN liahona;
MOVE 5

-- Fetch the 6th row from the cursor liahona:
FETCH 1 FROM liahona;
 code  | title  | did | date_prod  |  kind  |  len
-------+--------+-----+------------+--------+-------
 P_303 | 48 Hrs | 103 | 1982-10-22 | Action | 01:37
(1 row)

-- Close the cursor liahona and end the transaction:
CLOSE liahona;
COMMIT WORK;
```

<a id="id-1.9.3.157.9"></a>

## Compatibility

There is no `MOVE` statement in the SQL standard.

<a id="id-1.9.3.157.10"></a>

## See Also

[CLOSE](close.md), [DECLARE](declare.md), [FETCH](fetch.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-move.html)（英文原文，待翻譯）
