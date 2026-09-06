## Chapter 38. Event Triggers

**Table of Contents**

[38.1. Overview of Event Trigger Behavior](event-trigger-definition.md)
:   [38.1.1. login](event-trigger-definition.md#EVENT-TRIGGER-LOGIN)

    [38.1.2. ddl_command_start](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_START)

    [38.1.3. ddl_command_end](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_END)

    [38.1.4. sql_drop](event-trigger-definition.md#EVENT-TRIGGER-SQL_DROP)

    [38.1.5. table_rewrite](event-trigger-definition.md#EVENT-TRIGGER-TABLE_REWRITE)

    [38.1.6. Event Triggers in Aborted Transactions](event-trigger-definition.md#EVENT-TRIGGER-ABORTED-TRANSACTIONS)

    [38.1.7. Creating Event Triggers](event-trigger-definition.md#EVENT-TRIGGER-CREATING)

[38.2. Writing Event Trigger Functions in C](event-trigger-interface.md)

[38.3. A Complete Event Trigger Example](event-trigger-example.md)

[38.4. A Table Rewrite Event Trigger Example](event-trigger-table-rewrite-example.md)

[38.5. A Database Login Event Trigger Example](event-trigger-database-login-example.md)

<a id="id-1.8.5.2"></a>

To supplement the trigger mechanism discussed in [Chapter 37](../triggers/README.md),
PostgreSQL also provides event triggers. Unlike regular
triggers, which are attached to a single table and capture only DML events,
event triggers are global to a particular database and are capable of
capturing DDL events.

Like regular triggers, event triggers can be written in any procedural
language that includes event trigger support, or in C, but not in plain
SQL.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-triggers.html)（英文原文，待翻譯）
