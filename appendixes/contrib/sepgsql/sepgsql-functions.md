# F.40.6. sepgsql 函式

<a id="SEPGSQL-FUNCTIONS"></a>

## F.40.6. sepgsql 函式 [#](#sepgsql-functions) <a href="#sepgsql-functions" id="sepgsql-functions"></a>

[表 F.32](#sepgsql-functions-table) 列出可用的函式。

<a id="SEPGSQL-FUNCTIONS-TABLE"></a>

### 表 F.32. sepgsql 函式 [#](#sepgsql-functions-table) <a href="#sepgsql-functions-table" id="sepgsql-functions-table"></a>

<table border="1" class="table" summary="sepgsql 函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_getcon</code> ()
        → <code class="returnvalue">text</code>
</p>
<p>
        傳回用戶端網域，也就是用戶端目前的安全標籤。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_setcon</code> ( <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        若安全政策允許，將目前工作階段的用戶端網域切換到新的網域。
        它也接受 <code class="literal">NULL</code> 輸入，作為轉換回用戶端原本網域的要求。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_mcstrans_in</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        若 mcstrans 常駐程式正在執行，將給定的限定格式 MLS/MCS 範圍轉換為原始格式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_mcstrans_out</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        若 mcstrans 常駐程式正在執行，將給定的原始格式 MLS/MCS 範圍轉換為限定格式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sepgsql_restorecon</code> ( <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        為目前資料庫內的所有物件設定初始安全標籤。引數可以是 <code class="literal">NULL</code>，或是用來取代系統預設值的 specfile 名稱。
       </p></td></tr></tbody></table>

<br>

[返回 F.40. sepgsql — 以 SELinux 標籤為基礎的強制存取控制（MAC）安全模組](../sepgsql.md#sepgsql)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sepgsql.html)（原文版本：18.6；核對日期：2026-10-22）
