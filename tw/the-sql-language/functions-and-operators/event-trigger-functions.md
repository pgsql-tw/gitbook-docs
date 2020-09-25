# 9.29. 事件觸發函式

PostgreSQL provides these helper functions to retrieve information from event triggers.

For more information about event triggers, see [Chapter 39](https://www.postgresql.org/docs/12/event-triggers.html).

## 9.29.1. Capturing Changes at Command End

`pg_event_trigger_ddl_commands` returns a list of DDL commands executed by each user action, when invoked in a function attached to a `ddl_command_end` event trigger. If called in any other context, an error is raised. `pg_event_trigger_ddl_commands` returns one row for each base command executed; some commands that are a single SQL sentence may return more than one row. This function returns the following columns:

| Name | Type | Description |
| :--- | :--- | :--- |
| `classid` | `oid` | OID of catalog the object belongs in |
| `objid` | `oid` | OID of the object itself |
| `objsubid` | `integer` | Sub-object ID \(e.g. attribute number for a column\) |
| `command_tag` | `text` | Command tag |
| `object_type` | `text` | Type of the object |
| `schema_name` | `text` | Name of the schema the object belongs in, if any; otherwise `NULL`. No quoting is applied. |
| `object_identity` | `text` | Text rendering of the object identity, schema-qualified. Each identifier included in the identity is quoted if necessary. |
| `in_extension` | `bool` | True if the command is part of an extension script |
| `command` | `pg_ddl_command` | A complete representation of the command, in internal format. This cannot be output directly, but it can be passed to other functions to obtain different pieces of information about the command. |

## 9.29.2. Processing Objects Dropped by a DDL Command

`pg_event_trigger_dropped_objects` returns a list of all objects dropped by the command in whose `sql_drop` event it is called. If called in any other context, `pg_event_trigger_dropped_objects` raises an error. `pg_event_trigger_dropped_objects` returns the following columns:

| Name | Type | Description |
| :--- | :--- | :--- |
| `classid` | `oid` | OID of catalog the object belonged in |
| `objid` | `oid` | OID of the object itself |
| `objsubid` | `integer` | Sub-object ID \(e.g. attribute number for a column\) |
| `original` | `bool` | True if this was one of the root object\(s\) of the deletion |
| `normal` | `bool` | True if there was a normal dependency relationship in the dependency graph leading to this object |
| `is_temporary` | `bool` | True if this was a temporary object |
| `object_type` | `text` | Type of the object |
| `schema_name` | `text` | Name of the schema the object belonged in, if any; otherwise `NULL`. No quoting is applied. |
| `object_name` | `text` | Name of the object, if the combination of schema and name can be used as a unique identifier for the object; otherwise `NULL`. No quoting is applied, and name is never schema-qualified. |
| `object_identity` | `text` | Text rendering of the object identity, schema-qualified. Each identifier included in the identity is quoted if necessary. |
| `address_names` | `text[]` | An array that, together with `object_type` and `address_args`, can be used by the `pg_get_object_address()` function to recreate the object address in a remote server containing an identically named object of the same kind |
| `address_args` | `text[]` | Complement for `address_names` |

The `pg_event_trigger_dropped_objects` function can be used in an event trigger like this:

```text
CREATE FUNCTION test_event_trigger_for_drops()
        RETURNS event_trigger LANGUAGE plpgsql AS $$
DECLARE
    obj record;
BEGIN
    FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
    LOOP
        RAISE NOTICE '% dropped object: % %.% %',
                     tg_tag,
                     obj.object_type,
                     obj.schema_name,
                     obj.object_name,
                     obj.object_identity;
    END LOOP;
END
$$;
CREATE EVENT TRIGGER test_event_trigger_for_drops
   ON sql_drop
   EXECUTE FUNCTION test_event_trigger_for_drops();
```

## 9.29.3. Handling a Table Rewrite Event

The functions shown in [Table 9.96](https://www.postgresql.org/docs/12/functions-event-triggers.html#FUNCTIONS-EVENT-TRIGGER-TABLE-REWRITE) provide information about a table for which a `table_rewrite` event has just been called. If called in any other context, an error is raised.

#### **Table 9.96. Table Rewrite Information**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_event_trigger_table_rewrite_oid()` | `Oid` | The OID of the table about to be rewritten. |
| `pg_event_trigger_table_rewrite_reason()` | `int` | The reason code\(s\) explaining the reason for rewriting. The exact meaning of the codes is release dependent. |

The `pg_event_trigger_table_rewrite_oid` function can be used in an event trigger like this:

```text
CREATE FUNCTION test_event_trigger_table_rewrite_oid()
 RETURNS event_trigger
 LANGUAGE plpgsql AS
$$
BEGIN
  RAISE NOTICE 'rewriting table % for reason %',
                pg_event_trigger_table_rewrite_oid()::regclass,
                pg_event_trigger_table_rewrite_reason();
END;
$$;

CREATE EVENT TRIGGER test_table_rewrite_oid
                  ON table_rewrite
   EXECUTE FUNCTION test_event_trigger_table_rewrite_oid();
```

