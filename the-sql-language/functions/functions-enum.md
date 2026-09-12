<a id="FUNCTIONS-ENUM"></a>

## 9.10. 列舉支援函式 [#](#FUNCTIONS-ENUM)

對於列舉型別（說明於[第 8.7 節](../datatype/datatype-enum.md)），有幾個函式可以讓程式寫得更簡潔，而不必把列舉型別的特定值寫死在程式中。這些函式列於[表 9.35](functions-enum.md#FUNCTIONS-ENUM-TABLE)。範例假設有一個如下建立的列舉型別：

```

CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow', 'green', 'blue', 'purple');
```

<a id="FUNCTIONS-ENUM-TABLE"></a>

**表 9.35. 列舉支援函式**

<table border="1" class="table" summary="Enum Support Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.16.3.2.2.1.1.1.1"></a>
<code class="function">enum_first</code> ( <code class="type">anyenum</code> )
        → <code class="returnvalue">anyenum</code>
</p>
<p>
        回傳輸入列舉型別的第一個值。
       </p>
<p>
<code class="literal">enum_first(null::rainbow)</code>
        → <code class="returnvalue">red</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.16.3.2.2.2.1.1.1"></a>
<code class="function">enum_last</code> ( <code class="type">anyenum</code> )
        → <code class="returnvalue">anyenum</code>
</p>
<p>
        回傳輸入列舉型別的最後一個值。
       </p>
<p>
<code class="literal">enum_last(null::rainbow)</code>
        → <code class="returnvalue">purple</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.16.3.2.2.3.1.1.1"></a>
<code class="function">enum_range</code> ( <code class="type">anyenum</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        以有序陣列的形式回傳輸入列舉型別的所有值。
       </p>
<p>
<code class="literal">enum_range(null::rainbow)</code>
        → <code class="returnvalue">{red,orange,yellow,​green,blue,purple}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">enum_range</code> ( <code class="type">anyenum</code>, <code class="type">anyenum</code> )
        → <code class="returnvalue">anyarray</code>
</p>
<p>
        以有序陣列的形式回傳兩個給定列舉值之間的範圍。這兩個值必須來自同一個列舉型別。如果第一個參數為 null，結果會從該列舉型別的第一個值開始。如果第二個參數為 null，結果會在該列舉型別的最後一個值結束。
       </p>
<p>
<code class="literal">enum_range('orange'::rainbow, 'green'::rainbow)</code>
        → <code class="returnvalue">{orange,yellow,green}</code>
</p>
<p>
<code class="literal">enum_range(NULL, 'green'::rainbow)</code>
        → <code class="returnvalue">{red,orange,​yellow,green}</code>
</p>
<p>
<code class="literal">enum_range('orange'::rainbow, NULL)</code>
        → <code class="returnvalue">{orange,yellow,green,​blue,purple}</code>
</p></td></tr></tbody></table>

<br>

請注意，除了雙引數形式的 `enum_range` 之外，這些函式都不理會傳給它們的具體值；它們只在意其宣告的資料型別。傳入 null 或該型別的特定值都可以，結果相同。比起像範例中那樣套用在寫死的型別名稱上，更常見的做法是將這些函式套用到資料表欄位或函式引數上。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-enum.html)（原文版本：18.6；核對日期：2026-09-11）
