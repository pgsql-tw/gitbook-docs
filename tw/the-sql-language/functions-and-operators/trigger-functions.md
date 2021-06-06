# 9.28. 觸發函式

While many uses of triggers involve user-written trigger functions, PostgreSQL provides a few built-in trigger functions that can be used directly in user-defined triggers. These are summarized in [Table 9.97](https://www.postgresql.org/docs/13/functions-trigger.html#BUILTIN-TRIGGERS-TABLE). \(Additional built-in trigger functions exist, which implement foreign key constraints and deferred index constraints. Those are not documented here since users need not use them directly.\)

For more information about creating triggers, see [CREATE TRIGGER](https://www.postgresql.org/docs/13/sql-createtrigger.html).

#### **Table 9.97. Built-In Trigger Functions**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
        <p>Example Usage</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>suppress_redundant_updates_trigger</code> ( ) &#x2192; <code>trigger</code>
        </p>
        <p>Suppresses do-nothing update operations. See below for details.</p>
        <p><code>CREATE TRIGGER ... suppress_redundant_updates_trigger()</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tsvector_update_trigger</code> ( ) &#x2192; <code>trigger</code>
        </p>
        <p>Automatically updates a <code>tsvector</code> column from associated plain-text
          document column(s). The text search configuration to use is specified by
          name as a trigger argument. See <a href="https://www.postgresql.org/docs/13/textsearch-features.html#TEXTSEARCH-UPDATE-TRIGGERS">Section 12.4.3</a> for
          details.</p>
        <p><code>CREATE TRIGGER ... tsvector_update_trigger(tsvcol, &apos;pg_catalog.swedish&apos;, title, body)</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>tsvector_update_trigger_column</code> ( ) &#x2192; <code>trigger</code>
        </p>
        <p>Automatically updates a <code>tsvector</code> column from associated plain-text
          document column(s). The text search configuration to use is taken from
          a <code>regconfig</code> column of the table. See <a href="https://www.postgresql.org/docs/13/textsearch-features.html#TEXTSEARCH-UPDATE-TRIGGERS">Section 12.4.3</a> for
          details.</p>
        <p><code>CREATE TRIGGER ... tsvector_update_trigger_column(tsvcol, tsconfigcol, title, body)</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

當作用於資料列層級的 BEFORE UPDATE 觸發器時，suppress\_redundant\_updates\_trigger 函數將阻止任何不實際變更資料表資料的 UPDATE 行為發生。這會替代掉無論如何都會正常執行的實體資料更新行為，無論是否發生資料變更。（這種行為使 UPDATE 執行得更快，因為不需要重覆進行相關的檢查，並且在某些情況下也很有用。）

理想情況下，您應該避免執行實際上不會變更資料的 UPDATE。多餘的 UPDATE 可能會花費大量不必要的時間，尤其是當有大量索引要更改，並且棄置的資料空間必須時常被清理時。然而，在客戶端程式中檢測這種情況並不是這麼容易，甚至是不可能的，而且撰寫表示式來檢測也容易出錯。另一種方法則是使用 suppress\_redundant\_updates\_trigger，它會跳過不改變資料的 UPDATE。觸發器為每筆資料花費很少但非常重要的時間，因此如果UPDATE 條件的大多數資料確實發生了變化，則使用此觸發器將使更新執行得比平均的情況更慢。

The `suppress_redundant_updates_trigger` function can be added to a table like this:

```text
CREATE TRIGGER z_min_update
BEFORE UPDATE ON tablename
FOR EACH ROW EXECUTE FUNCTION suppress_redundant_updates_trigger();
```

In most cases, you need to fire this trigger last for each row, so that it does not override other triggers that might wish to alter the row. Bearing in mind that triggers fire in name order, you would therefore choose a trigger name that comes after the name of any other trigger you might have on the table. \(Hence the “z” prefix in the example.\)

