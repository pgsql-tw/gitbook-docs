## 9.30. Event Trigger Functions [#](#FUNCTIONS-EVENT-TRIGGERS)

[9.30.1. Capturing Changes at Command End](functions-event-triggers.md#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)

[9.30.2. Processing Objects Dropped by a DDL Command](functions-event-triggers.md#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)

[9.30.3. Handling a Table Rewrite Event](functions-event-triggers.md#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

PostgreSQL provides these helper functions
to retrieve information from event triggers.

For more information about event triggers,
see [Chapter 38](../../server-programming/event-triggers/README.md).

<a id="PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS"></a>

### 9.30.1. Capturing Changes at Command End [#](#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)

<a id="id-1.5.8.36.4.2"></a>

```

pg_event_trigger_ddl_commands () → setof record
```

`pg_event_trigger_ddl_commands` returns a list of
DDL commands executed by each user action,
when invoked in a function attached to a
`ddl_command_end` event trigger. If called in any other
context, an error is raised.
`pg_event_trigger_ddl_commands` returns one row for each
base command executed; some commands that are a single SQL sentence
may return more than one row. This function returns the following
columns:

<table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">classid</code></td><td><code class="type">oid</code></td><td>OID of catalog the object belongs in</td></tr><tr><td><code class="literal">objid</code></td><td><code class="type">oid</code></td><td>OID of the object itself</td></tr><tr><td><code class="literal">objsubid</code></td><td><code class="type">integer</code></td><td>Sub-object ID (e.g., attribute number for a column)</td></tr><tr><td><code class="literal">command_tag</code></td><td><code class="type">text</code></td><td>Command tag</td></tr><tr><td><code class="literal">object_type</code></td><td><code class="type">text</code></td><td>Type of the object</td></tr><tr><td><code class="literal">schema_name</code></td><td><code class="type">text</code></td><td>
         Name of the schema the object belongs in, if any; otherwise <code class="literal">NULL</code>.
         No quoting is applied.
        </td></tr><tr><td><code class="literal">object_identity</code></td><td><code class="type">text</code></td><td>
         Text rendering of the object identity, schema-qualified. Each
         identifier included in the identity is quoted if necessary.
        </td></tr><tr><td><code class="literal">in_extension</code></td><td><code class="type">boolean</code></td><td>True if the command is part of an extension script</td></tr><tr><td><code class="literal">command</code></td><td><code class="type">pg_ddl_command</code></td><td>
         A complete representation of the command, in internal format.
         This cannot be output directly, but it can be passed to other
         functions to obtain different pieces of information about the
         command.
        </td></tr></tbody></table>

<a id="PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS"></a>

### 9.30.2. Processing Objects Dropped by a DDL Command [#](#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)

<a id="id-1.5.8.36.5.2"></a>

```

pg_event_trigger_dropped_objects () → setof record
```

`pg_event_trigger_dropped_objects` returns a list of all objects
dropped by the command in whose `sql_drop` event it is called.
If called in any other context, an error is raised.
This function returns the following columns:

<table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code class="literal">classid</code></td><td><code class="type">oid</code></td><td>OID of catalog the object belonged in</td></tr><tr><td><code class="literal">objid</code></td><td><code class="type">oid</code></td><td>OID of the object itself</td></tr><tr><td><code class="literal">objsubid</code></td><td><code class="type">integer</code></td><td>Sub-object ID (e.g., attribute number for a column)</td></tr><tr><td><code class="literal">original</code></td><td><code class="type">boolean</code></td><td>True if this was one of the root object(s) of the deletion</td></tr><tr><td><code class="literal">normal</code></td><td><code class="type">boolean</code></td><td>
         True if there was a normal dependency relationship
         in the dependency graph leading to this object
        </td></tr><tr><td><code class="literal">is_temporary</code></td><td><code class="type">boolean</code></td><td>
         True if this was a temporary object
        </td></tr><tr><td><code class="literal">object_type</code></td><td><code class="type">text</code></td><td>Type of the object</td></tr><tr><td><code class="literal">schema_name</code></td><td><code class="type">text</code></td><td>
         Name of the schema the object belonged in, if any; otherwise <code class="literal">NULL</code>.
         No quoting is applied.
        </td></tr><tr><td><code class="literal">object_name</code></td><td><code class="type">text</code></td><td>
         Name of the object, if the combination of schema and name can be
         used as a unique identifier for the object; otherwise <code class="literal">NULL</code>.
         No quoting is applied, and name is never schema-qualified.
        </td></tr><tr><td><code class="literal">object_identity</code></td><td><code class="type">text</code></td><td>
         Text rendering of the object identity, schema-qualified. Each
         identifier included in the identity is quoted if necessary.
        </td></tr><tr><td><code class="literal">address_names</code></td><td><code class="type">text[]</code></td><td>
         An array that, together with <code class="literal">object_type</code> and
         <code class="literal">address_args</code>, can be used by
         the <code class="function">pg_get_object_address</code> function to
         recreate the object address in a remote server containing an
         identically named object of the same kind.
        </td></tr><tr><td><code class="literal">address_args</code></td><td><code class="type">text[]</code></td><td>
         Complement for <code class="literal">address_names</code>
</td></tr></tbody></table>

The `pg_event_trigger_dropped_objects` function can be used
in an event trigger like this:

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
END;
$$;
CREATE EVENT TRIGGER test_event_trigger_for_drops
   ON sql_drop
   EXECUTE FUNCTION test_event_trigger_for_drops();
```

<a id="PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS"></a>

### 9.30.3. Handling a Table Rewrite Event [#](#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

The functions shown in
[Table 9.111](functions-event-triggers.md#FUNCTIONS-EVENT-TRIGGER-TABLE-REWRITE)
provide information about a table for which a
`table_rewrite` event has just been called.
If called in any other context, an error is raised.

<a id="FUNCTIONS-EVENT-TRIGGER-TABLE-REWRITE"></a>

**Table 9.111. Table Rewrite Information Functions**

<table border="1" class="table" summary="Table Rewrite Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.36.6.3.2.2.1.1.1.1"></a>
<code class="function">pg_event_trigger_table_rewrite_oid</code> ()
        → <code class="returnvalue">oid</code>
</p>
<p>
        Returns the OID of the table about to be rewritten.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.36.6.3.2.2.2.1.1.1"></a>
<code class="function">pg_event_trigger_table_rewrite_reason</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns a code explaining the reason(s) for rewriting. The value is
        a bitmap built from the following values: <code class="literal">1</code>
        (the table has changed its persistence), <code class="literal">2</code>
        (default value of a column has changed), <code class="literal">4</code>
        (a column has a new data type) and <code class="literal">8</code>
        (the table access method has changed).
       </p></td></tr></tbody></table>

<br>

These functions can be used in an event trigger like this:

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
   EXECUTE FUNCTION test_event_trigger_table_rewrite_oid();
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-event-triggers.html)（英文原文，待翻譯）
