## 44.5. Trigger Functions [#](#PLPYTHON-TRIGGER)

<a id="id-1.8.11.13.2"></a>

When a function is used as a trigger, the dictionary
`TD` contains trigger-related values:

`TD["event"]`
:   contains the event as a string:
    `INSERT`, `UPDATE`,
    `DELETE`, or `TRUNCATE`.

`TD["when"]`
:   contains one of `BEFORE`, `AFTER`, or
    `INSTEAD OF`.

`TD["level"]`
:   contains `ROW` or `STATEMENT`.

`TD["new"]`<br>`TD["old"]`
:   For a row-level trigger, one or both of these fields contain
    the respective trigger rows, depending on the trigger event.

`TD["name"]`
:   contains the trigger name.

`TD["table_name"]`
:   contains the name of the table on which the trigger occurred.

`TD["table_schema"]`
:   contains the schema of the table on which the trigger occurred.

`TD["relid"]`
:   contains the OID of the table on which the trigger occurred.

`TD["args"]`
:   If the `CREATE TRIGGER` command
    included arguments, they are available in `TD["args"][0]` to
    `TD["args"][n-1]`.

If `TD["when"]` is `BEFORE` or
`INSTEAD OF` and
`TD["level"]` is `ROW`, you can
return `None` or `"OK"` from the
Python function to indicate the row is unmodified,
`"SKIP"` to abort the event, or if `TD["event"]`
is `INSERT` or `UPDATE` you can return
`"MODIFY"` to indicate you've modified the new row.
Otherwise the return value is ignored.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-trigger.html)（英文原文，待翻譯）
