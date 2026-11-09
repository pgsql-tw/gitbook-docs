# 9.30.3. 處理資料表改寫事件

<a id="PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS"></a>

## 9.30.3. 處理資料表改寫事件 [#](#pg-event-trigger-table-rewrite-functions) <a href="#pg-event-trigger-table-rewrite-functions" id="pg-event-trigger-table-rewrite-functions"></a>

[表 9.111](#functions-event-trigger-table-rewrite) 所列的函式，提供剛觸發 `table_rewrite` 事件之資料表的相關資訊。如果在任何其他情境中呼叫，就會引發錯誤。

<a id="FUNCTIONS-EVENT-TRIGGER-TABLE-REWRITE"></a>

### 表 9.111. 資料表改寫資訊函式 [#](#functions-event-trigger-table-rewrite) <a href="#functions-event-trigger-table-rewrite" id="functions-event-trigger-table-rewrite"></a>

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

[返回 9.30. 事件觸發程序函式](../functions-event-triggers.md#functions-event-triggers)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-event-triggers.html)（原文版本：18.6；核對日期：2026-09-11）
