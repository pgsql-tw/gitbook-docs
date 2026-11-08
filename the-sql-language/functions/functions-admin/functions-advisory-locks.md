# 9.28.10. 諮詢鎖函式

<a id="FUNCTIONS-ADVISORY-LOCKS"></a>

## 9.28.10. 諮詢鎖函式 [#](#functions-advisory-locks) <a href="#functions-advisory-locks" id="functions-advisory-locks"></a>

[表 9.109](#functions-advisory-locks-table) 所列的函式用於管理諮詢鎖。關於這些函式的正確用法，詳情請參閱[第 13.3.5 節](../../mvcc/explicit-locking.md#advisory-locks)。

這些函式全都是用來鎖定由應用程式定義的資源，資源可以用單一個 64 位元的鍵值，或兩個 32 位元的鍵值來識別（請注意，這兩種鍵空間不會重疊）。如果另一個工作階段已經在相同的資源識別符號上持有衝突的鎖，這些函式會視函式的性質，等待資源變為可用，或是回傳 `false` 結果。鎖可以是共享鎖或排他鎖：共享鎖不會與同一資源上的其他共享鎖衝突，只會與排他鎖衝突。鎖可以在工作階段層級取得（會一直持有，直到被釋放或工作階段結束），或在交易層級取得（會一直持有，直到目前的交易結束；無法手動釋放）。多次的工作階段層級鎖請求會堆疊，因此如果同一個資源識別符號被鎖定了三次，就必須發出三次解鎖請求，才能在工作階段結束前釋放該資源。

<a id="FUNCTIONS-ADVISORY-LOCKS-TABLE"></a>

### 表 9.109. 諮詢鎖函式 [#](#functions-advisory-locks-table) <a href="#functions-advisory-locks-table" id="functions-advisory-locks-table"></a>

<table border="1" class="table" summary="Advisory Lock Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.1.1.1.1"></a>
<code class="function">pg_advisory_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個排他的工作階段層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.2.1.1.1"></a>
<code class="function">pg_advisory_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個共享的工作階段層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.3.1.1.1"></a>
<code class="function">pg_advisory_unlock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_unlock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        釋放先前取得的排他工作階段層級諮詢鎖。如果成功釋放該鎖，就回傳 <code class="literal">true</code>。如果並未持有該鎖，就回傳 <code class="literal">false</code>，此外伺服器還會回報一則 SQL 警告。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.4.1.1.1"></a>
<code class="function">pg_advisory_unlock_all</code> ()
        → <code class="returnvalue">void</code>
</p>
<p>
        釋放目前工作階段所持有的所有工作階段層級諮詢鎖。（這個函式會在工作階段結束時自動隱含地呼叫，即使用戶端並未正常中斷連線也是如此。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.5.1.1.1"></a>
<code class="function">pg_advisory_unlock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_unlock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        釋放先前取得的共享工作階段層級諮詢鎖。如果成功釋放該鎖，就回傳 <code class="literal">true</code>。如果並未持有該鎖，就回傳 <code class="literal">false</code>，此外伺服器還會回報一則 SQL 警告。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.6.1.1.1"></a>
<code class="function">pg_advisory_xact_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_xact_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個排他的交易層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.7.1.1.1"></a>
<code class="function">pg_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">void</code>
</p>
<p class="func_signature">
<code class="function">pg_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        取得一個共享的交易層級諮詢鎖，必要時會等待。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.8.1.1.1"></a>
<code class="function">pg_try_advisory_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個排他的工作階段層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.9.1.1.1"></a>
<code class="function">pg_try_advisory_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個共享的工作階段層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.10.1.1.1"></a>
<code class="function">pg_try_advisory_xact_lock</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_xact_lock</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個排他的交易層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.34.12.4.2.2.11.1.1.1"></a>
<code class="function">pg_try_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="function">pg_try_advisory_xact_lock_shared</code> ( <em class="parameter"><code>key1</code></em> <code class="type">integer</code>, <em class="parameter"><code>key2</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果可以取得，就取得一個共享的交易層級諮詢鎖。這會立即取得鎖並回傳 <code class="literal">true</code>，或者在無法立即取得鎖時，不等待而直接回傳 <code class="literal">false</code>。
       </p></td></tr></tbody></table>

<br>

[返回 9.28. 系統管理函式](../functions-admin.md#functions-admin)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-admin.html)（原文版本：18.6；核對日期：2026-09-11）
