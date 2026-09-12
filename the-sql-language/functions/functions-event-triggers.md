<a id="FUNCTIONS-EVENT-TRIGGERS"></a>

## 9.30. 事件觸發程序函式 [#](#FUNCTIONS-EVENT-TRIGGERS)

[9.30.1. 在命令結束時擷取變更](functions-event-triggers.md#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)

[9.30.2. 處理被 DDL 命令刪除的物件](functions-event-triggers.md#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)

[9.30.3. 處理資料表改寫事件](functions-event-triggers.md#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

PostgreSQL 提供了這些輔助函式，用來從事件觸發程序中取得資訊。

關於事件觸發程序的更多資訊，請參閱[第 38 章](../../server-programming/event-triggers/README.md)。

<a id="PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS"></a>

### 9.30.1. 在命令結束時擷取變更 [#](#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)

<a id="id-1.5.8.36.4.2"></a>

```

pg_event_trigger_ddl_commands () → setof record
```

在附加到 `ddl_command_end` 事件觸發程序的函式中呼叫時，`pg_event_trigger_ddl_commands` 會回傳每個使用者動作所執行之 DDL 命令的清單。如果在任何其他情境中呼叫，就會引發錯誤。`pg_event_trigger_ddl_commands` 會為每個執行的基本命令回傳一筆資料列；有些屬於單一 SQL 語句的命令可能會回傳不只一筆資料列。這個函式回傳下列欄位：

<table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">classid</code></td><td><code class="type">oid</code></td><td>物件所屬之系統目錄的 OID</td></tr><tr><td><code class="literal">objid</code></td><td><code class="type">oid</code></td><td>物件本身的 OID</td></tr><tr><td><code class="literal">objsubid</code></td><td><code class="type">integer</code></td><td>子物件 ID（例如欄位的屬性編號）</td></tr><tr><td><code class="literal">command_tag</code></td><td><code class="type">text</code></td><td>命令標籤</td></tr><tr><td><code class="literal">object_type</code></td><td><code class="type">text</code></td><td>物件的類型</td></tr><tr><td><code class="literal">schema_name</code></td><td><code class="type">text</code></td><td>
         物件所屬綱要的名稱（如果有的話）；否則為 <code class="literal">NULL</code>。不加任何引號。
        </td></tr><tr><td><code class="literal">object_identity</code></td><td><code class="type">text</code></td><td>
         物件識別的文字表示，以綱要限定。識別中所包含的每個識別符號，必要時都會加上引號。
        </td></tr><tr><td><code class="literal">in_extension</code></td><td><code class="type">boolean</code></td><td>如果該命令是擴充功能指令碼的一部分，則為 true</td></tr><tr><td><code class="literal">command</code></td><td><code class="type">pg_ddl_command</code></td><td>
         命令以內部格式表示的完整內容。它無法直接輸出，但可以傳給其他函式，以取得關於該命令的各種資訊。
        </td></tr></tbody></table>

<a id="PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS"></a>

### 9.30.2. 處理被 DDL 命令刪除的物件 [#](#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)

<a id="id-1.5.8.36.5.2"></a>

```

pg_event_trigger_dropped_objects () → setof record
```

`pg_event_trigger_dropped_objects` 會回傳在其 `sql_drop` 事件中呼叫它的那個命令所刪除之所有物件的清單。如果在任何其他情境中呼叫，就會引發錯誤。這個函式回傳下列欄位：

<table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">classid</code></td><td><code class="type">oid</code></td><td>物件原本所屬之系統目錄的 OID</td></tr><tr><td><code class="literal">objid</code></td><td><code class="type">oid</code></td><td>物件本身的 OID</td></tr><tr><td><code class="literal">objsubid</code></td><td><code class="type">integer</code></td><td>子物件 ID（例如欄位的屬性編號）</td></tr><tr><td><code class="literal">original</code></td><td><code class="type">boolean</code></td><td>如果這是刪除操作的根物件之一，則為 true</td></tr><tr><td><code class="literal">normal</code></td><td><code class="type">boolean</code></td><td>
         如果在相依關係圖中，有一般的相依關係通往這個物件，則為 true
        </td></tr><tr><td><code class="literal">is_temporary</code></td><td><code class="type">boolean</code></td><td>
         如果這是暫時物件，則為 true
        </td></tr><tr><td><code class="literal">object_type</code></td><td><code class="type">text</code></td><td>物件的類型</td></tr><tr><td><code class="literal">schema_name</code></td><td><code class="type">text</code></td><td>
         物件原本所屬綱要的名稱（如果有的話）；否則為 <code class="literal">NULL</code>。不加任何引號。
        </td></tr><tr><td><code class="literal">object_name</code></td><td><code class="type">text</code></td><td>
         如果綱要與名稱的組合可以用作該物件的唯一識別碼，則為物件的名稱；否則為 <code class="literal">NULL</code>。不加任何引號，而且名稱永遠不會以綱要限定。
        </td></tr><tr><td><code class="literal">object_identity</code></td><td><code class="type">text</code></td><td>
         物件識別的文字表示，以綱要限定。識別中所包含的每個識別符號，必要時都會加上引號。
        </td></tr><tr><td><code class="literal">address_names</code></td><td><code class="type">text[]</code></td><td>
         一個陣列，可與 <code class="literal">object_type</code> 及 <code class="literal">address_args</code> 一起，讓 <code class="function">pg_get_object_address</code> 函式在包含同類同名物件的遠端伺服器中重建該物件位址。
        </td></tr><tr><td><code class="literal">address_args</code></td><td><code class="type">text[]</code></td><td>
         <code class="literal">address_names</code> 的補充
</td></tr></tbody></table>

`pg_event_trigger_dropped_objects` 函式可以像這樣在事件觸發程序中使用：

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

### 9.30.3. 處理資料表改寫事件 [#](#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

[表 9.111](functions-event-triggers.md#FUNCTIONS-EVENT-TRIGGER-TABLE-REWRITE) 所列的函式，提供剛觸發 `table_rewrite` 事件之資料表的相關資訊。如果在任何其他情境中呼叫，就會引發錯誤。

<a id="FUNCTIONS-EVENT-TRIGGER-TABLE-REWRITE"></a>

**表 9.111. 資料表改寫資訊函式**

<table border="1" class="table" summary="Table Rewrite Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.36.6.3.2.2.1.1.1.1"></a>
<code class="function">pg_event_trigger_table_rewrite_oid</code> ()
        → <code class="returnvalue">oid</code>
</p>
<p>
        回傳即將被改寫之資料表的 OID。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.36.6.3.2.2.2.1.1.1"></a>
<code class="function">pg_event_trigger_table_rewrite_reason</code> ()
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳說明改寫原因的代碼。其值是由下列值組成的點陣圖：<code class="literal">1</code>（資料表的持久性已改變）、<code class="literal">2</code>（欄位的預設值已改變）、<code class="literal">4</code>（欄位有新的資料型別）以及 <code class="literal">8</code>（資料表存取方法已改變）。
       </p></td></tr></tbody></table>

<br>

這些函式可以像這樣在事件觸發程序中使用：

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

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-event-triggers.html)（原文版本：18.6；核對日期：2026-09-11）
