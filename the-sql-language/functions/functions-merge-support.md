<a id="FUNCTIONS-MERGE-SUPPORT"></a>

## 9.23. 合併支援函式 [#](#FUNCTIONS-MERGE-SUPPORT)

<a id="id-1.5.8.29.2"></a>

PostgreSQL 包含一個合併支援函式，可以在 [MERGE](../../reference/sql-commands/sql-merge.md) 命令的 `RETURNING` 清單中使用，用來識別對每一筆資料列所採取的動作；請參閱[表 9.68](functions-merge-support.md#FUNCTIONS-MERGE-SUPPORT-TABLE)。

<a id="FUNCTIONS-MERGE-SUPPORT-TABLE"></a>

**表 9.68. 合併支援函式**

<table border="1" class="table" summary="Merge Support Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
       函式
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="func_table_entry" id="MERGE-ACTION"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.29.4.2.2.1.1.1.1"></a>
<code class="function">merge_action</code> ( )
       → <code class="returnvalue">text</code>
</p>
<p>
       回傳對目前資料列所執行的合併動作命令。其值會是 <code class="literal">'INSERT'</code>、<code class="literal">'UPDATE'</code> 或 <code class="literal">'DELETE'</code>。
      </p></td></tr></tbody></table>

<br>

範例：

```

MERGE INTO products p
  USING stock s ON p.product_id = s.product_id
  WHEN MATCHED AND s.quantity > 0 THEN
    UPDATE SET in_stock = true, quantity = s.quantity
  WHEN MATCHED THEN
    UPDATE SET in_stock = false, quantity = 0
  WHEN NOT MATCHED THEN
    INSERT (product_id, in_stock, quantity)
      VALUES (s.product_id, true, s.quantity)
  RETURNING merge_action(), p.*;

 merge_action | product_id | in_stock | quantity
--------------+------------+----------+----------
 UPDATE       |       1001 | t        |       50
 UPDATE       |       1002 | f        |        0
 INSERT       |       1003 | t        |       10
```

請注意，這個函式只能在 `MERGE` 命令的 `RETURNING` 清單中使用。在查詢的任何其他部分使用它都是錯誤。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-merge-support.html)（原文版本：18.6；核對日期：2026-09-11）
