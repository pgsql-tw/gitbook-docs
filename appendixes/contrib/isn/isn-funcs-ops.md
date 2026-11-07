# F.20.3. 函式與運算子

<a id="ISN-FUNCS-OPS"></a>

## F.20.3. 函式與運算子 [#](#isn-funcs-ops) <a href="#isn-funcs-ops" id="isn-funcs-ops"></a>

`isn` 模組提供標準比較運算子，以及所有這些資料型別的 B-tree 與雜湊索引支援。此外，還有數個專用函式，列於[表 F.11](#isn-functions)。在此表中，`isn` 表示模組的任何一種資料型別。

<a id="ISN-FUNCTIONS"></a>

### 表 F.11. `isn` 函式 [#](#isn-functions) <a href="#isn-functions" id="isn-functions"></a>

<table border="1" class="table" summary="isn Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.30.7.3.2.2.1.1.1.1"></a>
<code class="function">make_valid</code> ( <code class="type">isn</code> )
        → <code class="returnvalue">isn</code>
</p>
<p>
        清除值的無效檢查碼旗標。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.30.7.3.2.2.2.1.1.1"></a>
<code class="function">is_valid</code> ( <code class="type">isn</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢查是否存在無效檢查碼旗標。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.30.7.3.2.2.3.1.1.1"></a>
<code class="function">isn_weak</code> ( <code class="type">boolean</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        設定弱輸入模式，並傳回新設定。此函式是為了向後相容而保留。建議透過 <code class="varname">isn.weak</code> 組態參數設定弱模式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">isn_weak</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        傳回弱模式目前的狀態。此函式是為了向後相容而保留。建議透過 <code class="varname">isn.weak</code> 組態參數檢查弱模式。
       </p></td></tr></tbody></table>

<br>

[返回 F.20. isn — 國際標準號碼的資料型別（ISBN、EAN、UPC 等）](../isn.md#isn)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/isn.html)
