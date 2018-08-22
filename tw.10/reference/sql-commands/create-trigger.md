---
description: 版本：10
---

# CREATE TRIGGER

CREATE TRIGGER — 宣告一個新的觸發器

### 語法

```text
CREATE [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
    ON table_name
    [ FROM referenced_table_name ]
    [ NOT DEFERRABLE | [ DEFERRABLE ] [ INITIALLY IMMEDIATE | INITIALLY DEFERRED ] ]
    [ REFERENCING { { OLD | NEW } TABLE [ AS ] transition_relation_name } [ ... ] ]
    [ FOR [ EACH ] { ROW | STATEMENT } ]
    [ WHEN ( condition ) ]
    EXECUTE PROCEDURE function_name ( arguments )

where event can be one of:

    INSERT
    UPDATE [ OF column_name [, ... ] ]
    DELETE
    TRUNCATE
```

### 說明

CREATE TRIGGER 建立一個新的觸發器。觸發器將與指定的資料表，檢視表或外部資料表關聯，並在對該表執行某些操作時執行指定的函數。

可以指定觸發器在嘗試對某行執行操作之前（在檢查限制條件並嘗試執行 INSERT，UPDATE 或 DELETE 之前）；或者在操作完成後（在檢查限制條件並且 INSERT，UPDATE 或 DELETE 完成之後）；又或者代替操作（在檢視表上插入，更新或刪除的情況下）。如果觸發器在事件之前或之後觸發，則觸發器可以跳過目前資料列的操作，或者更改正在插入的資料列（僅適用於 INSERT 和 UPDATE 操作）。如果觸發器在事件發生後觸發，則所有更改（包括其他觸發器的效果）都對觸發器都是「可見」。

對於操作修改的每一個資料列，都會呼叫標記為 FOR EACH ROW 的觸發器一次。例如，影響 10 行的 DELETE 將導致目標關連上的任何 ON DELETE 觸發器被分別呼叫 10 次，每次刪除則執行一次。相反，標記為 FOR EACH STATEMENT 的觸發器僅對任何給予操作的執行一次，無論其修改多少資料列（特別是，修改零個資料列的操作仍將驅使執行任何適用的 FOR EACH STATEMENT 觸發器）。

指定用於觸發 INSTEAD OF 觸發事件的觸發器必須標記為 FOR EACH ROW，而且只能在檢視表上定義。 必須將檢視圖上的 BEFORE 和 AFTER 觸發器標記為每個語句。

此外，觸發器可以定義為觸發 TRUNCATE，儘管只有 FOR EACH STATEMENT。

下表總結了可以在資料表，檢視表和外部資料表上使用哪些類型的觸發器：

| When | Event | Row-level | Statement-level |
| :--- | :--- | :--- | :--- |
| `BEFORE` | `INSERT`/`UPDATE`/`DELETE` | Tables and foreign tables | Tables, views, and foreign tables |
| `TRUNCATE` | — | Tables |  |
| `AFTER` | `INSERT`/`UPDATE`/`DELETE` | Tables and foreign tables | Tables, views, and foreign tables |
| `TRUNCATE` | — | Tables |  |
| `INSTEAD OF` | `INSERT`/`UPDATE`/`DELETE` | Views | — |
| `TRUNCATE` | — | — |  |

Also, a trigger definition can specify a Boolean `WHEN` condition, which will be tested to see whether the trigger should be fired. In row-level triggers the `WHEN` condition can examine the old and/or new values of columns of the row. Statement-level triggers can also have `WHEN` conditions, although the feature is not so useful for them since the condition cannot refer to any values in the table.

If multiple triggers of the same kind are defined for the same event, they will be fired in alphabetical order by name.

When the `CONSTRAINT` option is specified, this command creates a _constraint trigger_. This is the same as a regular trigger except that the timing of the trigger firing can be adjusted using [SET CONSTRAINTS](https://www.postgresql.org/docs/10/static/sql-set-constraints.html). Constraint triggers must be `AFTER ROW` triggers on plain tables \(not foreign tables\). They can be fired either at the end of the statement causing the triggering event, or at the end of the containing transaction; in the latter case they are said to be _deferred_. A pending deferred-trigger firing can also be forced to happen immediately by using `SET CONSTRAINTS`. Constraint triggers are expected to raise an exception when the constraints they implement are violated.

The `REFERENCING` option enables collection of _transition relations_, which are row sets that include all of the rows inserted, deleted, or modified by the current SQL statement. This feature lets the trigger see a global view of what the statement did, not just one row at a time. This option is only allowed for an `AFTER` trigger that is not a constraint trigger; also, if the trigger is an `UPDATE` trigger, it must not specify a _`column_name`_ list. `OLD TABLE` may only be specified once, and only for a trigger that can fire on `UPDATE` or `DELETE`; it creates a transition relation containing the _before-images_ of all rows updated or deleted by the statement. Similarly, `NEW TABLE` may only be specified once, and only for a trigger that can fire on `UPDATE` or `INSERT`; it creates a transition relation containing the _after-images_ of all rows updated or inserted by the statement.

`SELECT` does not modify any rows so you cannot create `SELECT` triggers. Rules and views may provide workable solutions to problems that seem to need `SELECT` triggers.

Refer to [Chapter 38](https://www.postgresql.org/docs/10/static/triggers.html) for more information about triggers.

### Parameters

_`name`_

The name to give the new trigger. This must be distinct from the name of any other trigger for the same table. The name cannot be schema-qualified — the trigger inherits the schema of its table. For a constraint trigger, this is also the name to use when modifying the trigger's behavior using `SET CONSTRAINTS`.

`BEFORE`  
`AFTER`  
`INSTEAD OF`

Determines whether the function is called before, after, or instead of the event. A constraint trigger can only be specified as `AFTER`.

_`event`_

One of `INSERT`, `UPDATE`, `DELETE`, or `TRUNCATE`; this specifies the event that will fire the trigger. Multiple events can be specified using `OR`, except when transition relations are requested.

For `UPDATE` events, it is possible to specify a list of columns using this syntax:

```text
UPDATE OF column_name1 [, column_name2 ... ]
```

The trigger will only fire if at least one of the listed columns is mentioned as a target of the `UPDATE` command.

`INSTEAD OF UPDATE` events do not allow a list of columns. A column list cannot be specified when requesting transition relations, either.

_`table_name`_

The name \(optionally schema-qualified\) of the table, view, or foreign table the trigger is for.

_`referenced_table_name`_

The \(possibly schema-qualified\) name of another table referenced by the constraint. This option is used for foreign-key constraints and is not recommended for general use. This can only be specified for constraint triggers.

`DEFERRABLE`  
`NOT DEFERRABLE`  
`INITIALLY IMMEDIATE`  
`INITIALLY DEFERRED`

The default timing of the trigger. See the [CREATE TABLE](https://www.postgresql.org/docs/10/static/sql-createtable.html) documentation for details of these constraint options. This can only be specified for constraint triggers.

`REFERENCING`

This keyword immediately precedes the declaration of one or two relation names that provide access to the transition relations of the triggering statement.

`OLD TABLE`  
`NEW TABLE`

This clause indicates whether the following relation name is for the before-image transition relation or the after-image transition relation.

_`transition_relation_name`_

The \(unqualified\) name to be used within the trigger for this transition relation.

`FOR EACH ROW`  
`FOR EACH STATEMENT`

This specifies whether the trigger procedure should be fired once for every row affected by the trigger event, or just once per SQL statement. If neither is specified, `FOR EACH STATEMENT` is the default. Constraint triggers can only be specified `FOR EACH ROW`.

_`condition`_

A Boolean expression that determines whether the trigger function will actually be executed. If `WHEN` is specified, the function will only be called if the _`condition`_ returns `true`. In `FOR EACH ROW` triggers, the `WHEN` condition can refer to columns of the old and/or new row values by writing `OLD.`_`column_name`_ or `NEW.`_`column_name`_ respectively. Of course, `INSERT`triggers cannot refer to `OLD` and `DELETE` triggers cannot refer to `NEW`.

`INSTEAD OF` triggers do not support `WHEN` conditions.

Currently, `WHEN` expressions cannot contain subqueries.

Note that for constraint triggers, evaluation of the `WHEN` condition is not deferred, but occurs immediately after the row update operation is performed. If the condition does not evaluate to true then the trigger is not queued for deferred execution.

_`function_name`_

A user-supplied function that is declared as taking no arguments and returning type `trigger`, which is executed when the trigger fires.

_`arguments`_

An optional comma-separated list of arguments to be provided to the function when the trigger is executed. The arguments are literal string constants. Simple names and numeric constants can be written here, too, but they will all be converted to strings. Please check the description of the implementation language of the trigger function to find out how these arguments can be accessed within the function; it might be different from normal function arguments.

### Notes

To create a trigger on a table, the user must have the `TRIGGER` privilege on the table. The user must also have `EXECUTE` privilege on the trigger function.

Use [DROP TRIGGER](https://www.postgresql.org/docs/10/static/sql-droptrigger.html) to remove a trigger.

A column-specific trigger \(one defined using the `UPDATE OF` _`column_name`_ syntax\) will fire when any of its columns are listed as targets in the `UPDATE` command's `SET` list. It is possible for a column's value to change even when the trigger is not fired, because changes made to the row's contents by `BEFORE UPDATE` triggers are not considered. Conversely, a command such as `UPDATE ... SET x = x ...` will fire a trigger on column `x`, even though the column's value did not change.

In a `BEFORE` trigger, the `WHEN` condition is evaluated just before the function is or would be executed, so using `WHEN` is not materially different from testing the same condition at the beginning of the trigger function. Note in particular that the `NEW` row seen by the condition is the current value, as possibly modified by earlier triggers. Also, a `BEFORE` trigger's `WHEN`condition is not allowed to examine the system columns of the `NEW` row \(such as `oid`\), because those won't have been set yet.

In an `AFTER` trigger, the `WHEN` condition is evaluated just after the row update occurs, and it determines whether an event is queued to fire the trigger at the end of statement. So when an `AFTER` trigger's `WHEN` condition does not return true, it is not necessary to queue an event nor to re-fetch the row at end of statement. This can result in significant speedups in statements that modify many rows, if the trigger only needs to be fired for a few of the rows.

In some cases it is possible for a single SQL command to fire more than one kind of trigger. For instance an `INSERT` with an `ON CONFLICT DO UPDATE` clause may cause both insert and update operations, so it will fire both kinds of triggers as needed. The transition relations supplied to triggers are specific to their event type; thus an `INSERT` trigger will see only the inserted rows, while an `UPDATE` trigger will see only the updated rows.

Row updates or deletions caused by foreign-key enforcement actions, such as `ON UPDATE CASCADE` or `ON DELETE SET NULL`, are treated as part of the SQL command that caused them \(note that such actions are never deferred\). Relevant triggers on the affected table will be fired, so that this provides another way in which a SQL command might fire triggers not directly matching its type. In simple cases, triggers that request transition relations will see all changes caused in their table by a single original SQL command as a single transition relation. However, there are cases in which the presence of an `AFTER ROW` trigger that requests transition relations will cause the foreign-key enforcement actions triggered by a single SQL command to be split into multiple steps, each with its own transition relation\(s\). In such cases, any statement-level triggers that are present will be fired once per creation of a transition relation set, ensuring that the triggers see each affected row in a transition relation once and only once.

Statement-level triggers on a view are fired only if the action on the view is handled by a row-level `INSTEAD OF` trigger. If the action is handled by an `INSTEAD` rule, then whatever statements are emitted by the rule are executed in place of the original statement naming the view, so that the triggers that will be fired are those on tables named in the replacement statements. Similarly, if the view is automatically updatable, then the action is handled by automatically rewriting the statement into an action on the view's base table, so that the base table's statement-level triggers are the ones that are fired.

Modifying a partitioned table or a table with inheritance children fires statement-level triggers attached to the explicitly named table, but not statement-level triggers for its partitions or child tables. In contrast, row-level triggers are fired on the rows in affected partitions or child tables, even if they are not explicitly named in the query. If a statement-level trigger has been defined with transition relations named by a `REFERENCING` clause, then before and after images of rows are visible from all affected partitions or child tables. In the case of inheritance children, the row images include only columns that are present in the table that the trigger is attached to. Currently, row-level triggers with transition relations cannot be defined on partitions or inheritance child tables.

In PostgreSQL versions before 7.3, it was necessary to declare trigger functions as returning the placeholder type `opaque`, rather than `trigger`. To support loading of old dump files, `CREATE TRIGGER` will accept a function declared as returning `opaque`, but it will issue a notice and change the function's declared return type to `trigger`.

### Examples

Execute the function `check_account_update` whenever a row of the table `accounts` is about to be updated:

```text
CREATE TRIGGER check_update
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    EXECUTE PROCEDURE check_account_update();
```

The same, but only execute the function if column `balance` is specified as a target in the `UPDATE` command:

```text
CREATE TRIGGER check_update
    BEFORE UPDATE OF balance ON accounts
    FOR EACH ROW
    EXECUTE PROCEDURE check_account_update();
```

This form only executes the function if column `balance` has in fact changed value:

```text
CREATE TRIGGER check_update
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    WHEN (OLD.balance IS DISTINCT FROM NEW.balance)
    EXECUTE PROCEDURE check_account_update();
```

Call a function to log updates of `accounts`, but only if something changed:

```text
CREATE TRIGGER log_update
    AFTER UPDATE ON accounts
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE PROCEDURE log_account_update();
```

Execute the function `view_insert_row` for each row to insert rows into the tables underlying a view:

```text
CREATE TRIGGER view_insert
    INSTEAD OF INSERT ON my_view
    FOR EACH ROW
    EXECUTE PROCEDURE view_insert_row();
```

Execute the function `check_transfer_balances_to_zero` for each statement to confirm that the `transfer` rows offset to a net of zero:

```text
CREATE TRIGGER transfer_insert
    AFTER INSERT ON transfer
    REFERENCING NEW TABLE AS inserted
    FOR EACH STATEMENT
    EXECUTE PROCEDURE check_transfer_balances_to_zero();
```

Execute the function `check_matching_pairs` for each row to confirm that changes are made to matching pairs at the same time \(by the same statement\):

```text
CREATE TRIGGER paired_items_update
    AFTER UPDATE ON paired_items
    REFERENCING NEW TABLE AS newtab OLD TABLE AS oldtab
    FOR EACH ROW
    EXECUTE PROCEDURE check_matching_pairs();
```

[Section 38.4](https://www.postgresql.org/docs/10/static/trigger-example.html) contains a complete example of a trigger function written in C.

### Compatibility

The `CREATE TRIGGER` statement in PostgreSQL implements a subset of the SQL standard. The following functionalities are currently missing:

* While transition table names for `AFTER` triggers are specified using the `REFERENCING` clause in the standard way, the row variables used in `FOR EACH ROW` triggers may not be specified in a `REFERENCING` clause. They are available in a manner that is dependent on the language in which the trigger function is written, but is fixed for any one language. Some languages effectively behave as though there is a `REFERENCING` clause containing `OLD ROW AS OLD NEW ROW AS NEW`.
* The standard allows transition tables to be used with column-specific `UPDATE` triggers, but then the set of rows that should be visible in the transition tables depends on the trigger's column list. This is not currently implemented by PostgreSQL.
* PostgreSQL only allows the execution of a user-defined function for the triggered action. The standard allows the execution of a number of other SQL commands, such as `CREATE TABLE`, as the triggered action. This limitation is not hard to work around by creating a user-defined function that executes the desired commands.

SQL specifies that multiple triggers should be fired in time-of-creation order. PostgreSQL uses name order, which was judged to be more convenient.

SQL specifies that `BEFORE DELETE` triggers on cascaded deletes fire _after_ the cascaded `DELETE` completes. The PostgreSQL behavior is for `BEFORE DELETE` to always fire before the delete action, even a cascading one. This is considered more consistent. There is also nonstandard behavior if `BEFORE` triggers modify rows or prevent updates during an update that is caused by a referential action. This can lead to constraint violations or stored data that does not honor the referential constraint.

The ability to specify multiple actions for a single trigger using `OR` is a PostgreSQL extension of the SQL standard.

The ability to fire triggers for `TRUNCATE` is a PostgreSQL extension of the SQL standard, as is the ability to define statement-level triggers on views.

`CREATE CONSTRAINT TRIGGER` is a PostgreSQL extension of the SQL standard.

### 參閱

[ALTER TRIGGER](alter-trigger.md), [DROP TRIGGER](drop-trigger.md), [CREATE FUNCTION](create-function.md), [SET CONSTRAINTS](set-constraints.md)

