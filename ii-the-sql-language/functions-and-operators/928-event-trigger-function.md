# 9.28. 事件觸發函式[^1]

PostgreSQLprovides these helper functions to retrieve information from event triggers.

For more information about event triggers, see[Chapter 39](https://www.postgresql.org/docs/10/static/event-triggers.html).

### 9.28.1. Capturing Changes at Command End



`pg_event_trigger_ddl_commands`returns a list ofDDLcommands executed by each user action, when invoked in a function attached to a`ddl_command_end`event trigger. If called in any other context, an error is raised.`pg_event_trigger_ddl_commands`returns one row for each base command executed; some commands that are a single SQL sentence may return more than one row. This function returns the following columns:

| Name | Type | Description |
| :--- | :--- | :--- |
| `classid` | `Oid` | OID of catalog the object belongs in |
| `objid` | `Oid` | OID of the object in the catalog |
| `objsubid` | `integer` | Object sub-id \(e.g. attribute number for columns\) |
| `command_tag` | `text` | command tag |
| `object_type` | `text` | Type of the object |
| `schema_name` | `text` | Name of the schema the object belongs in, if any; otherwise`NULL`. No quoting is applied. |
| `object_identity` | `text` | Text rendering of the object identity, schema-qualified. Each and every identifier present in the identity is quoted if necessary. |
| `in_extension` | `bool` | whether the command is part of an extension script |
| `command` | `pg_ddl_command` | A complete representation of the command, in internal format. This cannot be output directly, but it can be passed to other functions to obtain different pieces of information about the command. |

### 9.28.2. Processing Objects Dropped by a DDL Command



`pg_event_trigger_dropped_objects`returns a list of all objects dropped by the command in whose`sql_drop`event it is called. If called in any other context,`pg_event_trigger_dropped_objects`raises an error.`pg_event_trigger_dropped_objects`returns the following columns:

| Name | Type | Description |
| :--- | :--- | :--- |
| `classid` | `Oid` | OID of catalog the object belonged in |
| `objid` | `Oid` | OID the object had within the catalog |
| `objsubid` | `int32` | Object sub-id \(e.g. attribute number for columns\) |
| `original` | `bool` | Flag used to identify the root object\(s\) of the deletion |
| `normal` | `bool` | Flag indicating that there's a normal dependency relationship in the dependency graph leading to this object |
| `is_temporary` | `bool` | Flag indicating that the object was a temporary object. |
| `object_type` | `text` | Type of the object |
| `schema_name` | `text` | Name of the schema the object belonged in, if any; otherwise`NULL`. No quoting is applied. |
| `object_name` | `text` | Name of the object, if the combination of schema and name can be used as a unique identifier for the object; otherwise`NULL`. No quoting is applied, and name is never schema-qualified. |
| `object_identity` | `text` | Text rendering of the object identity, schema-qualified. Each and every identifier present in the identity is quoted if necessary. |
| `address_names` | `text[]` | An array that, together with`object_type`and`address_args`, can be used by the`pg_get_object_address()`to recreate the object address in a remote server containing an identically named object of the same kind. |
| `address_args` | `text[]` | Complement for`address_names`above. |

The`pg_event_trigger_dropped_objects`function can be used in an event trigger like this:

```
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
   EXECUTE PROCEDURE test_event_trigger_for_drops();

```

### 9.28.3. Handling a Table Rewrite Event

The functions shown in[Table 9.90](https://www.postgresql.org/docs/10/static/functions-event-triggers.html#functions-event-trigger-table-rewrite)provide information about a table for which a`table_rewrite`event has just been called. If called in any other context, an error is raised.

**Table 9.90. Table Rewrite information**

| Name | Return Type | Description |
| :--- | :--- | :--- |
| `pg_event_trigger_table_rewrite_oid()` | `Oid` | The OID of the table about to be rewritten. |
| `pg_event_trigger_table_rewrite_reason()` | `int` | The reason code\(s\) explaining the reason for rewriting. The exact meaning of the codes is release dependent. |

  


The`pg_event_trigger_table_rewrite_oid`function can be used in an event trigger like this:

```
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
   EXECUTE PROCEDURE test_event_trigger_table_rewrite_oid();
```

---



[^1]:  [PostgreSQL: Documentation: 10: 9.28. Event Trigger Functions](https://www.postgresql.org/docs/10/static/functions-event-triggers.html)

