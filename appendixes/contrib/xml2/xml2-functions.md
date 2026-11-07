# F.50.2. 函式說明

<a id="XML2-FUNCTIONS"></a>

## F.50.2. 函式說明 [#](#xml2-functions) <a href="#xml2-functions" id="xml2-functions"></a>

[表 F.37](#xml2-functions-table) 列出此模組提供的函式。這些函式提供簡單直接的 XML 剖析與 XPath 查詢。

<a id="XML2-FUNCTIONS-TABLE"></a>

### 表 F.37. `xml2` 函式 [#](#xml2-functions-table) <a href="#xml2-functions-table" id="xml2-functions-table"></a>

<table border="1" class="table" summary="xml2 函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xml_valid</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        剖析給定的文件，若該文件是格式正確（well-formed）的 XML 則傳回 true。（注意：這是標準 PostgreSQL 函式 <code class="function">xml_is_well_formed()</code> 的別名。名稱 <code class="function">xml_valid()</code> 在技術上並不正確，因為在 XML 中，有效（validity）與格式正確（well-formedness）的意義不同。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_string</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        對提供的文件執行 XPath 查詢，並將結果轉換為 <code class="type">text</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_number</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        對提供的文件執行 XPath 查詢，並將結果轉換為 <code class="type">real</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_bool</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        對提供的文件執行 XPath 查詢，並將結果轉換為 <code class="type">boolean</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_nodeset</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code>, <em class="parameter"><code>toptag</code></em> <code class="type">text</code>, <em class="parameter"><code>itemtag</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        對文件執行查詢，並以 XML 標籤包裝結果。若結果為多值，輸出看起來會像這樣：
</p><pre class="synopsis">
&lt;toptag&gt;
&lt;itemtag&gt;Value 1 which could be an XML fragment&lt;/itemtag&gt;
&lt;itemtag&gt;Value 2....&lt;/itemtag&gt;
&lt;/toptag&gt;
</pre><p>
        若 <em class="parameter"><code>toptag</code></em> 或 <em class="parameter"><code>itemtag</code></em> 為空字串，則會省略相應的標籤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_nodeset</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code>, <em class="parameter"><code>itemtag</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        與 <code class="function">xpath_nodeset(document, query, toptag, itemtag)</code> 相同，但結果會省略 <em class="parameter"><code>toptag</code></em>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_nodeset</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        與 <code class="function">xpath_nodeset(document, query, toptag, itemtag)</code> 相同，但結果會省略兩個標籤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_list</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code>, <em class="parameter"><code>separator</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        對文件執行查詢，並傳回以指定分隔符號分隔的多個值，例如 <code class="literal">Value
        1,Value 2,Value 3</code>（當 <em class="parameter"><code>separator</code></em> 為 <code class="literal">,</code> 時）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">xpath_list</code> ( <em class="parameter"><code>document</code></em> <code class="type">text</code>, <em class="parameter"><code>query</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        這是上述函式的包裝函式，使用 <code class="literal">,</code> 作為分隔符號。
       </p></td></tr></tbody></table>

<br>

[返回 F.50. xml2 — XPath 查詢與 XSLT 功能](../xml2.md#xml2)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xml2.html)（原文版本：18.6；核對日期：2026-10-22）
