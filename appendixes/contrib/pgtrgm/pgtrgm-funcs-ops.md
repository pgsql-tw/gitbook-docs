# F.35.2. 函式與運算子

<a id="PGTRGM-FUNCS-OPS"></a>

## F.35.2. 函式與運算子 [#](#pgtrgm-funcs-ops) <a href="#pgtrgm-funcs-ops" id="pgtrgm-funcs-ops"></a>

`pg_trgm` 模組提供的函式列於[表 F.26](#pgtrgm-func-table)，運算子則列於[表 F.27](#pgtrgm-op-table)。

<a id="PGTRGM-FUNC-TABLE"></a>

### 表 F.26. `pg_trgm` 函式 [#](#pgtrgm-func-table) <a href="#pgtrgm-func-table" id="pgtrgm-func-table"></a>

<table border="1" class="table" summary="pg_trgm 函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.1.1.1.1"></a>
<code class="function">similarity</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        傳回一個表示兩個引數相似程度的數字。結果的範圍從 0（表示兩個字串完全不相似）到 1（表示兩個字串完全相同）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.2.1.1.1"></a>
<code class="function">show_trgm</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        傳回給定字串中所有三元組所組成的陣列。（實務上，除了除錯之外很少用到。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.3.1.1.1"></a>
<code class="function">word_similarity</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        傳回一個數字，表示第一個字串的三元組集合，與第二個字串的有序三元組集合中任一連續範圍之間的最大相似度。詳細說明請參閱下文。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.4.1.1.1"></a>
<code class="function">strict_word_similarity</code> ( <code class="type">text</code>, <code class="type">text</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        與 <code class="function">word_similarity</code> 相同，但強制範圍邊界必須與單字邊界一致。由於我們沒有跨單字的三元組，此函式實際上傳回的是第一個字串與第二個字串中任一連續單字範圍之間的最大相似度。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.5.1.1.1"></a>
<code class="function">show_limit</code> ()
        → <code class="returnvalue">real</code>
</p>
<p>
        傳回 <code class="literal">%</code> 運算子目前使用的相似度門檻。此值設定兩個單字之間的最小相似度，達到此值才會被視為足夠相似，例如可視為彼此的拼寫錯誤。（<span class="emphasis"><em>已棄用</em></span>；請改用 <code class="command">SHOW</code>
<code class="varname">pg_trgm.similarity_threshold</code>。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.45.6.3.2.2.6.1.1.1"></a>
<code class="function">set_limit</code> ( <code class="type">real</code> )
        → <code class="returnvalue">real</code>
</p>
<p>
        設定 <code class="literal">%</code> 運算子目前使用的相似度門檻。門檻必須介於 0 與 1 之間（預設為 0.3）。傳回所傳入的同一個值。（<span class="emphasis"><em>已棄用</em></span>；請改用 <code class="command">SET</code>
<code class="varname">pg_trgm.similarity_threshold</code>。）
       </p></td></tr></tbody></table>

<br>

請看以下範例：

```

# SELECT word_similarity('word', 'two words');
 word_similarity
-----------------
             0.8
(1 row)
```

在第一個字串中，三元組集合為
`{" w"," wo","wor","ord","rd "}`。
在第二個字串中，有序三元組集合為
`{" t"," tw","two","wo "," w"," wo","wor","ord","rds","ds "}`。
第二個字串中最相似的有序三元組集合範圍是 `{" w"," wo","wor","ord"}`，相似度為
`0.8`。

此函式傳回的值，可大致理解為第一個字串與第二個字串任一子字串之間的最大相似度。不過，此函式不會在範圍的邊界加上填補。因此，除了不相符的單字邊界之外，第二個字串中額外出現的字元數量不會納入考量。

另一方面，`strict_word_similarity` 會在第二個字串中選取一個單字範圍。在上例中，`strict_word_similarity` 會選取單一單字 `'words'` 的範圍，其三元組集合為
`{" w"," wo","wor","ord","rds","ds "}`。

```

# SELECT strict_word_similarity('word', 'two words'), similarity('word', 'words');
 strict_word_similarity | similarity
------------------------+------------
               0.571429 |   0.571429
(1 row)
```

因此，`strict_word_similarity` 函式適用於找出與完整單字的相似度，而 `word_similarity` 較適合找出與單字局部的相似度。

<a id="PGTRGM-OP-TABLE"></a>

### 表 F.27. `pg_trgm` 運算子 [#](#pgtrgm-op-table) <a href="#pgtrgm-op-table" id="pgtrgm-op-table"></a>

<table border="1" class="table" summary="pg_trgm 運算子"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">%</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        傳回 <code class="literal">true</code> 的條件是：兩個引數的相似度大於由 <code class="varname">pg_trgm.similarity_threshold</code> 所設定的目前相似度門檻。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;%</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        傳回 <code class="literal">true</code> 的條件是：第一個引數中的三元組集合，與第二個引數中有序三元組集合的某個連續範圍之間的相似度，大於由 <code class="varname">pg_trgm.word_similarity_threshold</code> 參數所設定的目前單字相似度門檻。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">%&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="literal">&lt;%</code> 運算子的交換運算子。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;&lt;%</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        傳回 <code class="literal">true</code> 的條件是：第二個引數中有一個符合單字邊界的有序三元組集合連續範圍，且該範圍與第一個引數之三元組集合的相似度，大於由 <code class="varname">pg_trgm.strict_word_similarity_threshold</code> 參數所設定的目前嚴格單字相似度門檻。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">%&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="literal">&lt;&lt;%</code> 運算子的交換運算子。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        傳回兩個引數之間的<span class="quote">“<span class="quote">距離</span>”</span>，也就是 1 減去 <code class="function">similarity()</code> 的值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;&lt;-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        傳回兩個引數之間的<span class="quote">“<span class="quote">距離</span>”</span>，也就是 1 減去 <code class="function">word_similarity()</code> 的值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;-&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        <code class="literal">&lt;&lt;-&gt;</code> 運算子的交換運算子。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;&lt;&lt;-&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        傳回兩個引數之間的<span class="quote">“<span class="quote">距離</span>”</span>，也就是 1 減去 <code class="function">strict_word_similarity()</code> 的值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">&lt;-&gt;&gt;&gt;</code> <code class="type">text</code>
        → <code class="returnvalue">real</code>
</p>
<p>
        <code class="literal">&lt;&lt;&lt;-&gt;</code> 運算子的交換運算子。
       </p></td></tr></tbody></table>

<br>

譯註：上表說明 %、<%、<<% 等運算子在相似度「大於」目前門檻時傳回 true；但依 PostgreSQL 18 原始碼（contrib/pg_trgm/trgm_op.c），實際判斷條件是相似度「大於或等於」門檻。

[返回 F.35. pg_trgm — 支援以三元組比對文字相似度](../pgtrgm.md#pgtrgm)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgtrgm.html)（原文版本：18.6；核對日期：2026-10-23）
