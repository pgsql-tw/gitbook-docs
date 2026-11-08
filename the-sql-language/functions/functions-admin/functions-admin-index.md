# 9.28.8. 索引維護函式

<a id="FUNCTIONS-ADMIN-INDEX"></a>

## 9.28.8. 索引維護函式 [#](#functions-admin-index) <a href="#functions-admin-index" id="functions-admin-index"></a>

[表 9.107](#functions-admin-index-table) 列出可用於索引維護工作的函式。（請注意，這些維護工作通常由 autovacuum 自動完成；只有在特殊情況下才需要使用這些函式。）這些函式不能在復原期間執行。這些函式只限超級使用者與該索引的擁有者使用。

<a id="FUNCTIONS-ADMIN-INDEX-TABLE"></a>

### 表 9.107. 索引維護函式 [#](#functions-admin-index-table) <a href="#functions-admin-index-table" id="functions-admin-index-table"></a>

<table border="1" class="table" summary="Index Maintenance Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.1.1.1.1"></a>
<code class="function">brin_summarize_new_values</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        掃描指定的 BRIN 索引，找出基礎資料表中目前尚未被該索引摘要的頁面範圍；對於每個這樣的範圍，會掃描那些資料表頁面來建立新的摘要索引 tuple（值組）。回傳插入索引中的新頁面範圍摘要數量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.2.1.1.1"></a>
<code class="function">brin_summarize_range</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>blockNumber</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        如果涵蓋指定區塊的頁面範圍尚未被摘要，就對它進行摘要。這與 <code class="function">brin_summarize_new_values</code> 類似，差別在於它只處理涵蓋指定資料表區塊編號的頁面範圍。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.3.1.1.1"></a>
<code class="function">brin_desummarize_range</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code>, <em class="parameter"><code>blockNumber</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        移除摘要涵蓋指定資料表區塊之頁面範圍的 BRIN 索引 tuple（值組），如果有的話。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.10.3.2.2.4.1.1.1"></a>
<code class="function">gin_clean_pending_list</code> ( <em class="parameter"><code>index</code></em> <code class="type">regclass</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        將指定 GIN 索引之<span class="quote">「<span class="quote">pending</span>」</span>清單中的項目批次移入主要的 GIN 資料結構，藉此清理該清單。回傳從 pending 清單中移除的頁面數。如果引數是在停用 <code class="literal">fastupdate</code> 選項的情況下建立的 GIN 索引，就不會進行任何清理，結果為零，因為該索引沒有 pending 清單。關於 pending 清單與 <code class="literal">fastupdate</code> 選項的詳細資訊，請參閱<a class="xref" href="../../../internals/indextypes/gin.md#GIN-FAST-UPDATE">第 65.4.4.1 節</a>與<a class="xref" href="../../../internals/indextypes/gin.md#gin-tips">第 65.4.5 節</a>。
       </p></td></tr></tbody></table>

<br>

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
