# 9.27.7. 資料有效性檢查函式

<a id="FUNCTIONS-INFO-VALIDITY"></a>

## 9.27.7. 資料有效性檢查函式 [#](#functions-info-validity) <a href="#functions-info-validity" id="functions-info-validity"></a>

[表 9.83](#functions-info-validity-table) 所列的函式有助於檢查擬輸入資料的有效性。

<a id="FUNCTIONS-INFO-VALIDITY-TABLE"></a>

### 表 9.83. 資料有效性檢查函式 [#](#functions-info-validity-table) <a href="#functions-info-validity-table" id="functions-info-validity-table"></a>

<table border="1" class="table" summary="Data Validity Checking Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.9.3.2.2.1.1.1.1"></a>
<code class="function">pg_input_is_valid</code> (
          <em class="parameter"><code>string</code></em> <code class="type">text</code>,
          <em class="parameter"><code>type</code></em> <code class="type">text</code>
        )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        測試給定的 <em class="parameter"><code>string</code></em> 對於指定的資料型別而言是否為有效的輸入，並回傳 true 或 false。
       </p>
<p>
        只有在該資料型別的輸入函式已經更新為將無效輸入以<span class="quote">「<span class="quote">軟性</span>」</span>錯誤回報時，這個函式才能如預期般運作。否則，無效的輸入會中止交易，就如同直接將字串轉型為該型別一樣。
        </p>
<p>
<code class="literal">pg_input_is_valid('42', 'integer')</code>
         → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">pg_input_is_valid('42000000000', 'integer')</code>
         → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">pg_input_is_valid('1234.567', 'numeric(7,4)')</code>
         → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.9.3.2.2.2.1.1.1"></a>
<code class="function">pg_input_error_info</code> (
          <em class="parameter"><code>string</code></em> <code class="type">text</code>,
          <em class="parameter"><code>type</code></em> <code class="type">text</code>
        )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>message</code></em> <code class="type">text</code>,
        <em class="parameter"><code>detail</code></em> <code class="type">text</code>,
        <em class="parameter"><code>hint</code></em> <code class="type">text</code>,
        <em class="parameter"><code>sql_error_code</code></em> <code class="type">text</code> )
       </p>
<p>
        測試給定的 <em class="parameter"><code>string</code></em> 對於指定的資料型別而言是否為有效的輸入；如果不是，則回傳原本會拋出之錯誤的詳細資訊。如果輸入有效，結果為 NULL。其輸入與 <code class="function">pg_input_is_valid</code> 相同。
       </p>
<p>
        只有在該資料型別的輸入函式已經更新為將無效輸入以<span class="quote">「<span class="quote">軟性</span>」</span>錯誤回報時，這個函式才能如預期般運作。否則，無效的輸入會中止交易，就如同直接將字串轉型為該型別一樣。
       </p>
<p>
<code class="literal">SELECT * FROM pg_input_error_info('42000000000', 'integer')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
                       message                        | detail | hint | sql_error_code
------------------------------------------------------+--------+------+----------------
 value "42000000000" is out of range for type integer |        |      | 22003
</pre><p>
</p></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
