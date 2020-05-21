---
description: 版本：11
---

# CREATE TRIGGER

CREATE TRIGGER — 宣告一個新的觸發器

## 語法

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

## 說明

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

此外，觸發器定義可以指定布林 WHEN 條件，將對其進行測試以查看是否應觸發觸發器。在資料列級觸發器中，WHEN 條件可以檢查資料列的欄位舊值和新值。語句級觸發器也可以具有 WHEN 條件，儘管該功能對它們沒有那麼有用，因為條件不能引用資料表中的任何值。

如果為同一事件定義了多個相同類型的觸發器，則按名稱的字母順序觸發它們。

指定 CONSTRAINT 選項時，此指令將建令限制條件觸發器。除了可以使用 [SET CONSTRAINTS ](set-constraints.md)調整觸發器觸發的時機之外，其他與一般觸發器相同。限制條件觸發器必須是普通資料表（而不是外部資料表）上的 AFTER ROW 觸發器。 它們可以在語句結尾引發觸發事件，也可以在包含事務結束時觸發；在後面的情況下，他們會被延後。透過使用 SET CONSTRAINTS，也可以強制立即觸發待處理的延遲觸發器。當限制條件時，限制條件觸發器會引發例外處理。

REFERENCING 選項啟用轉換關連的集合，轉換關連是包含目前 SQL 語句插入，刪除或修改的所有資料列的子集。此功能允許觸發器查看語句的全域檢視圖，而不是一次只能查看一個資料列。此選項僅適用於非限制條件觸發器的 AFTER 觸發器；另外，如果觸發器是 UPDATE 觸發器，則它不能指定 column\_name 列表。OLD TABLE 只能指定一次，並且只能用於可以在 UPDATE 或 DELETE上 觸發的觸發器；它建立一個轉換關係，其中包含語句更新或刪除的所有資料列的先前版本。類似地，NEW TABLE 只能指定一次，並且只能用於可以在 UPDATE 或 INSERT 上觸發的觸發器；它建立一個轉換關連，包含語句更新或插入的所有資料列的新版本。

SELECT 不會修改任何資料列，因此您無法建立 SELECT 觸發器。規則和檢視表需要除錯以提供可行的解決方案時，就需要 SELECT 觸發器。

有關觸發器的更多訊息，請參閱[第 38 章](../../server-programming/triggers.md)。

## Parameters

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

## Notes

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

## 範例

每當要更新資料表 accounts 的資料列時，執行函數 check\_account\_update：

```text
CREATE TRIGGER check_update
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    EXECUTE PROCEDURE check_account_update();
```

一樣，但只有在 UPDATE 命令中將欄位 balance 作為更新標的時才執行該函數：

```text
CREATE TRIGGER check_update
    BEFORE UPDATE OF balance ON accounts
    FOR EACH ROW
    EXECUTE PROCEDURE check_account_update();
```

如果欄位 balance 實際上已變更其值，則此語法才會執行該函數：

```text
CREATE TRIGGER check_update
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    WHEN (OLD.balance IS DISTINCT FROM NEW.balance)
    EXECUTE PROCEDURE check_account_update();
```

呼叫函數來記錄 accounts 的更新，但僅在變更了某些內容時：

```text
CREATE TRIGGER log_update
    AFTER UPDATE ON accounts
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE PROCEDURE log_account_update();
```

對每一個資料列執行函數 view\_insert\_row，資料列被插入到檢視表中時：

```text
CREATE TRIGGER view_insert
    INSTEAD OF INSERT ON my_view
    FOR EACH ROW
    EXECUTE PROCEDURE view_insert_row();
```

對每個語句執行函數 check\_transfer\_balances\_to\_zero 以確認所傳輸的資料列與淨值的差異：

```text
CREATE TRIGGER transfer_insert
    AFTER INSERT ON transfer
    REFERENCING NEW TABLE AS inserted
    FOR EACH STATEMENT
    EXECUTE PROCEDURE check_transfer_balances_to_zero();
```

對每一個資料列執行 check\_matching\_pairs 函數以確認同時對相對應的資料列對進行變更（透過相同的語句）：

```text
CREATE TRIGGER paired_items_update
    AFTER UPDATE ON paired_items
    REFERENCING NEW TABLE AS newtab OLD TABLE AS oldtab
    FOR EACH ROW
    EXECUTE PROCEDURE check_matching_pairs();
```

[第 38.4 節](../../server-programming/extending-sql/user-defined-procedures.md)中有使用 C 撰寫的觸發器函數完整範例。

## 相容性

PostgreSQL 中的 CREATE TRIGGER 語句只實作了 SQL 標準的一部份。 目前還缺少以下功能：

* While transition table names for `AFTER` triggers are specified using the `REFERENCING` clause in the standard way, the row variables used in `FOR EACH ROW` triggers may not be specified in a `REFERENCING` clause. They are available in a manner that is dependent on the language in which the trigger function is written, but is fixed for any one language. Some languages effectively behave as though there is a `REFERENCING` clause containing `OLD ROW AS OLD NEW ROW AS NEW`.
* The standard allows transition tables to be used with column-specific `UPDATE` triggers, but then the set of rows that should be visible in the transition tables depends on the trigger's column list. This is not currently implemented by PostgreSQL.
* PostgreSQL only allows the execution of a user-defined function for the triggered action. The standard allows the execution of a number of other SQL commands, such as `CREATE TABLE`, as the triggered action. This limitation is not hard to work around by creating a user-defined function that executes the desired commands.

SQL specifies that multiple triggers should be fired in time-of-creation order. PostgreSQL uses name order, which was judged to be more convenient.

SQL specifies that `BEFORE DELETE` triggers on cascaded deletes fire _after_ the cascaded `DELETE` completes. The PostgreSQL behavior is for `BEFORE DELETE` to always fire before the delete action, even a cascading one. This is considered more consistent. There is also nonstandard behavior if `BEFORE` triggers modify rows or prevent updates during an update that is caused by a referential action. This can lead to constraint violations or stored data that does not honor the referential constraint.

The ability to specify multiple actions for a single trigger using `OR` is a PostgreSQL extension of the SQL standard.

The ability to fire triggers for `TRUNCATE` is a PostgreSQL extension of the SQL standard, as is the ability to define statement-level triggers on views.

`CREATE CONSTRAINT TRIGGER` is a PostgreSQL extension of the SQL standard.

## 參閱

[ALTER TRIGGER](alter-trigger.md), [DROP TRIGGER](drop-trigger.md), [CREATE FUNCTION](create-function.md), [SET CONSTRAINTS](set-constraints.md)

