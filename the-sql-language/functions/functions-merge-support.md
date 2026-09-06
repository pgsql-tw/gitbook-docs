## 9.23. Merge Support Functions [#](#FUNCTIONS-MERGE-SUPPORT)

<a id="id-1.5.8.29.2"></a>

PostgreSQL includes one merge support function
that may be used in the `RETURNING` list of a
[MERGE](../../reference/sql-commands/sql-merge.md) command to identify the action taken for each
row; see [Table 9.68](functions-merge-support.md#FUNCTIONS-MERGE-SUPPORT-TABLE).

<a id="FUNCTIONS-MERGE-SUPPORT-TABLE"></a>

**Table 9.68. Merge Support Functions**

<table border="1" class="table" summary="Merge Support Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
       Function
      </p>
<p>
       Description
      </p></th></tr></thead><tbody><tr><td class="func_table_entry" id="MERGE-ACTION"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.29.4.2.2.1.1.1.1"></a>
<code class="function">merge_action</code> ( )
       → <code class="returnvalue">text</code>
</p>
<p>
       Returns the merge action command executed for the current row.  This
       will be <code class="literal">'INSERT'</code>, <code class="literal">'UPDATE'</code>, or
       <code class="literal">'DELETE'</code>.
      </p></td></tr></tbody></table>

<br>

Example:

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

Note that this function can only be used in the `RETURNING`
list of a `MERGE` command. It is an error to use it in any
other part of a query.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-merge-support.html)（英文原文，待翻譯）
