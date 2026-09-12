<a id="FUNCTIONS-BITSTRING"></a>

## 9.6. 位元字串函式與運算子 [#](#FUNCTIONS-BITSTRING)

<a id="id-1.5.8.12.2"></a>

本節說明用於檢查與操作位元字串的函式與運算子，也就是 `bit` 與 `bit varying` 型別的值。（雖然這些表格中只提到 `bit` 型別，但 `bit varying` 型別的值也可以互換使用。）位元字串支援[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子，以及[表 9.14](functions-bitstring.md#FUNCTIONS-BIT-STRING-OP-TABLE) 所列的運算子。

<a id="FUNCTIONS-BIT-STRING-OP-TABLE"></a>

**表 9.14. 位元字串運算子**

<table border="1" class="table" summary="Bit String Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bit</code> <code class="literal">||</code> <code class="type">bit</code>
        → <code class="returnvalue">bit</code>
</p>
<p>
        串接
       </p>
<p>
<code class="literal">B'10001' || B'011'</code>
        → <code class="returnvalue">10001011</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bit</code> <code class="literal">&amp;</code> <code class="type">bit</code>
        → <code class="returnvalue">bit</code>
</p>
<p>
        位元 AND（輸入必須等長）
       </p>
<p>
<code class="literal">B'10001' &amp; B'01101'</code>
        → <code class="returnvalue">00001</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bit</code> <code class="literal">|</code> <code class="type">bit</code>
        → <code class="returnvalue">bit</code>
</p>
<p>
        位元 OR（輸入必須等長）
       </p>
<p>
<code class="literal">B'10001' | B'01101'</code>
        → <code class="returnvalue">11101</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bit</code> <code class="literal">#</code> <code class="type">bit</code>
        → <code class="returnvalue">bit</code>
</p>
<p>
        位元互斥 OR（輸入必須等長）
       </p>
<p>
<code class="literal">B'10001' # B'01101'</code>
        → <code class="returnvalue">11100</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">~</code> <code class="type">bit</code>
        → <code class="returnvalue">bit</code>
</p>
<p>
        位元 NOT
       </p>
<p>
<code class="literal">~ B'10001'</code>
        → <code class="returnvalue">01110</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bit</code> <code class="literal">&lt;&lt;</code> <code class="type">integer</code>
        → <code class="returnvalue">bit</code>
</p>
<p>
        位元左移（字串長度保持不變）
       </p>
<p>
<code class="literal">B'10001' &lt;&lt; 3</code>
        → <code class="returnvalue">01000</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bit</code> <code class="literal">&gt;&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">bit</code>
</p>
<p>
        位元右移（字串長度保持不變）
       </p>
<p>
<code class="literal">B'10001' &gt;&gt; 2</code>
        → <code class="returnvalue">00100</code>
</p></td></tr></tbody></table>

<br>

有些可用於二進位字串的函式，也可以用於位元字串，如[表 9.15](functions-bitstring.md#FUNCTIONS-BIT-STRING-TABLE) 所示。

<a id="FUNCTIONS-BIT-STRING-TABLE"></a>

**表 9.15. 位元字串函式**

<table border="1" class="table" summary="Bit String Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.1.1.1.1"></a>
<code class="function">bit_count</code> ( <code class="type">bit</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳位元字串中被設定的位元數（也稱為 <span class="quote">“<span class="quote">popcount</span>”</span>）。
       </p>
<p>
<code class="literal">bit_count(B'10111')</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.2.1.1.1"></a>
<code class="function">bit_length</code> ( <code class="type">bit</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳位元字串中的位元數。
       </p>
<p>
<code class="literal">bit_length(B'10111')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.3.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.12.6.2.2.3.1.1.2"></a>
<code class="function">length</code> ( <code class="type">bit</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳位元字串中的位元數。
       </p>
<p>
<code class="literal">length(B'10111')</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.4.1.1.1"></a>
<code class="function">octet_length</code> ( <code class="type">bit</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳位元字串中的位元組數。
       </p>
<p>
<code class="literal">octet_length(B'1011111011')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.5.1.1.1"></a>
<code class="function">overlay</code> ( <em class="parameter"><code>bits</code></em> <code class="type">bit</code> <code class="literal">PLACING</code> <em class="parameter"><code>newsubstring</code></em> <code class="type">bit</code> <code class="literal">FROM</code> <em class="parameter"><code>start</code></em> <code class="type">integer</code> [<span class="optional"> <code class="literal">FOR</code> <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">bit</code>
</p>
<p>
        將 <em class="parameter"><code>bits</code></em> 中從第 <em class="parameter"><code>start</code></em> 個位元開始、延伸 <em class="parameter"><code>count</code></em> 個位元的子字串，替換為 <em class="parameter"><code>newsubstring</code></em>。如果省略 <em class="parameter"><code>count</code></em>，預設為 <em class="parameter"><code>newsubstring</code></em> 的長度。
       </p>
<p>
<code class="literal">overlay(B'01010101010101010' placing B'11111' from 2 for 3)</code>
        → <code class="returnvalue">0111110101010101010</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.6.1.1.1"></a>
<code class="function">position</code> ( <em class="parameter"><code>substring</code></em> <code class="type">bit</code> <code class="literal">IN</code> <em class="parameter"><code>bits</code></em> <code class="type">bit</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳指定的 <em class="parameter"><code>substring</code></em> 在 <em class="parameter"><code>bits</code></em> 中第一次出現的起始索引；如果不存在則回傳零。
       </p>
<p>
<code class="literal">position(B'010' in B'000001101011')</code>
        → <code class="returnvalue">8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.7.1.1.1"></a>
<code class="function">substring</code> ( <em class="parameter"><code>bits</code></em> <code class="type">bit</code> [<span class="optional"> <code class="literal">FROM</code> <em class="parameter"><code>start</code></em> <code class="type">integer</code> </span>] [<span class="optional"> <code class="literal">FOR</code> <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">bit</code>
</p>
<p>
        擷取 <em class="parameter"><code>bits</code></em> 的子字串：如果有指定，就從第 <em class="parameter"><code>start</code></em> 個位元開始；如果有指定，就在 <em class="parameter"><code>count</code></em> 個位元之後停止。<em class="parameter"><code>start</code></em> 與 <em class="parameter"><code>count</code></em> 至少要提供其中一個。
       </p>
<p>
<code class="literal">substring(B'110010111111' from 3 for 2)</code>
        → <code class="returnvalue">00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.8.1.1.1"></a>
<code class="function">get_bit</code> ( <em class="parameter"><code>bits</code></em> <code class="type">bit</code>,
        <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        從位元字串中擷取第 <em class="parameter"><code>n</code></em> 個位元；第一個（最左邊的）位元是第 0 個位元。
       </p>
<p>
<code class="literal">get_bit(B'101010101010101010', 6)</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.12.6.2.2.9.1.1.1"></a>
<code class="function">set_bit</code> ( <em class="parameter"><code>bits</code></em> <code class="type">bit</code>,
        <em class="parameter"><code>n</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>newvalue</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">bit</code>
</p>
<p>
        將位元字串中的第 <em class="parameter"><code>n</code></em> 個位元設為 <em class="parameter"><code>newvalue</code></em>；第一個（最左邊的）位元是第 0 個位元。
       </p>
<p>
<code class="literal">set_bit(B'101010101010101010', 6, 0)</code>
        → <code class="returnvalue">101010001010101010</code>
</p></td></tr></tbody></table>

<br>

此外，整數值可以與 `bit` 型別互相轉換。將整數轉換為 `bit(n)` 時，會複製最右邊的 `n` 個位元。將整數轉換為比整數本身更寬的位元字串時，會在左邊進行符號延伸。一些範例：

```

44::bit(10)                    0000101100
44::bit(3)                     100
cast(-44 as bit(12))           111111010100
'1110'::bit(4)::integer        14
```

請注意，只轉換為「bit」表示轉換為 `bit(1)`，因此只會得到整數的最低有效位元。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-bitstring.html)（原文版本：18.6；核對日期：2026-09-11）
