## 第 38 章 事件觸發程序

**目錄**

[38.1. 事件觸發程序行為概觀](event-trigger-definition.md)
:   [38.1.1. login](event-trigger-definition.md#EVENT-TRIGGER-LOGIN)

    [38.1.2. ddl_command_start](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_START)

    [38.1.3. ddl_command_end](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_END)

    [38.1.4. sql_drop](event-trigger-definition.md#EVENT-TRIGGER-SQL_DROP)

    [38.1.5. table_rewrite](event-trigger-definition.md#EVENT-TRIGGER-TABLE_REWRITE)

    [38.1.6. 中止交易中的事件觸發程序](event-trigger-definition.md#EVENT-TRIGGER-ABORTED-TRANSACTIONS)

    [38.1.7. 建立事件觸發程序](event-trigger-definition.md#EVENT-TRIGGER-CREATING)

[38.2. 以 C 撰寫事件觸發程序函式](event-trigger-interface.md)

[38.3. 完整的事件觸發程序範例](event-trigger-example.md)

[38.4. 資料表重寫事件觸發程序範例](event-trigger-table-rewrite-example.md)

[38.5. 資料庫登入事件觸發程序範例](event-trigger-database-login-example.md)

<a id="id-1.8.5.2"></a>

為了補充[第 37 章](../triggers/README.md)所討論的觸發程序機制，PostgreSQL 也提供了事件觸發程序。與只附加在單一資料表上、只能擷取 DML 事件的一般觸發程序不同，事件觸發程序是針對特定資料庫全域生效的，並且能夠擷取 DDL 事件。

和一般觸發程序一樣，事件觸發程序可以用任何支援事件觸發程序的程序語言撰寫，也可以用 C 撰寫，但不能用純 SQL 撰寫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/event-triggers.html)（原文版本：18.6；核對日期：2026-09-15）
