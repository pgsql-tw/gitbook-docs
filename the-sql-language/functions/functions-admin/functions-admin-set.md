# 9.28.1. 組態設定函式

<a id="FUNCTIONS-ADMIN-SET"></a>

## 9.28.1. 組態設定函式 [#](#functions-admin-set) <a href="#functions-admin-set" id="functions-admin-set"></a>

<a id="id-1.5.8.34.3.2"></a><a id="id-1.5.8.34.3.3"></a><a id="id-1.5.8.34.3.4"></a>

[表 9.95](#functions-admin-set-table) 列出可用來查詢與修改執行時期組態參數的函式。

<a id="FUNCTIONS-ADMIN-SET-TABLE"></a>

### 表 9.95. 組態設定函式 [#](#functions-admin-set-table) <a href="#functions-admin-set-table" id="functions-admin-set-table"></a>

<table border="1" class="table" summary="Configuration Settings Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.3.6.2.2.1.1.1.1"></a>
<code class="function">current_setting</code> ( <em class="parameter"><code>setting_name</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>missing_ok</code></em> <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳設定 <em class="parameter"><code>setting_name</code></em> 目前的值。如果沒有這個設定，<code class="function">current_setting</code> 會拋出錯誤，除非有提供 <em class="parameter"><code>missing_ok</code></em> 且其值為 <code class="literal">true</code>（此時會回傳 NULL）。這個函式對應於 <acronym class="acronym">SQL</acronym> 指令 <a class="xref" href="../../../reference/sql-commands/sql-show.md"><span class="refentrytitle">SHOW</span></a>。
       </p>
<p>
<code class="literal">current_setting('datestyle')</code>
        → <code class="returnvalue">ISO, MDY</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.3.6.2.2.2.1.1.1"></a>
<code class="function">set_config</code> (
          <em class="parameter"><code>setting_name</code></em> <code class="type">text</code>,
          <em class="parameter"><code>new_value</code></em> <code class="type">text</code>,
          <em class="parameter"><code>is_local</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將參數 <em class="parameter"><code>setting_name</code></em> 設定為 <em class="parameter"><code>new_value</code></em>，並回傳該值。如果 <em class="parameter"><code>is_local</code></em> 為 <code class="literal">true</code>，新值只會在目前的交易期間生效。如果你希望新值在目前工作階段的其餘時間都生效，請改用 <code class="literal">false</code>。這個函式對應於 SQL 指令 <a class="xref" href="../../../reference/sql-commands/sql-set.md"><span class="refentrytitle">SET</span></a>。
       </p>
<p>
<code class="function">set_config</code> 接受以 NULL 值作為 <em class="parameter"><code>new_value</code></em>，但由於設定不能為 NULL，這會被解讀為將該設定重設為預設值的請求。
       </p>
<p>
<code class="literal">set_config('log_statement_stats', 'off', false)</code>
        → <code class="returnvalue">off</code>
</p></td></tr></tbody></table>

<br>

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
