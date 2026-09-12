<a id="FUNCTIONS-MATH"></a>

## 9.3. 數學函式與運算子 [#](#FUNCTIONS-MATH)

許多 PostgreSQL 型別都提供了數學運算子。對於沒有標準數學慣例的型別（例如日期／時間型別），我們會在後續各節中說明實際的行為。

[表 9.4](functions-math.md#FUNCTIONS-MATH-OP-TABLE) 列出了可用於標準數值型別的數學運算子。除非另有註明，顯示為接受 *`numeric_type`* 的運算子，適用於 `smallint`、`integer`、`bigint`、`numeric`、`real` 與 `double precision` 等所有型別。顯示為接受 *`integral_type`* 的運算子，適用於 `smallint`、`integer` 與 `bigint` 型別。除非另有註明，運算子的每種形式都回傳與其引數相同的資料型別。涉及多種引數資料型別的呼叫，例如 `integer` `+` `numeric`，會使用在這些清單中排在較後面的型別來解析。

<a id="FUNCTIONS-MATH-OP-TABLE"></a>

**表 9.4. 數學運算子**

<table border="1" class="table" summary="Mathematical Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">+</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        加法
       </p>
<p>
<code class="literal">2 + 3</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">+</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        單元加號（不做任何運算）
       </p>
<p>
<code class="literal">+ 3.5</code>
        → <code class="returnvalue">3.5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">-</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        減法
       </p>
<p>
<code class="literal">2 - 3</code>
        → <code class="returnvalue">-1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">-</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        取負
       </p>
<p>
<code class="literal">- (-4)</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">*</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        乘法
       </p>
<p>
<code class="literal">2 * 3</code>
        → <code class="returnvalue">6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">/</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        除法（對於整數型別，除法會將結果朝零截斷）
       </p>
<p>
<code class="literal">5.0 / 2</code>
        → <code class="returnvalue">2.5000000000000000</code>
</p>
<p>
<code class="literal">5 / 2</code>
        → <code class="returnvalue">2</code>
</p>
<p>
<code class="literal">(-5) / 2</code>
        → <code class="returnvalue">-2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">%</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        模數（餘數）；適用於 <code class="type">smallint</code>、<code class="type">integer</code>、<code class="type">bigint</code> 與 <code class="type">numeric</code>
</p>
<p>
<code class="literal">5 % 4</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">numeric</code> <code class="literal">^</code> <code class="type">numeric</code>
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="type">double precision</code> <code class="literal">^</code> <code class="type">double precision</code>
        → <code class="returnvalue">double precision</code>
</p>
<p>
        指數運算
       </p>
<p>
<code class="literal">2 ^ 3</code>
        → <code class="returnvalue">8</code>
</p>
<p>
        與一般的數學慣例不同，多次使用 <code class="literal">^</code> 時，預設會由左至右結合：
       </p>
<p>
<code class="literal">2 ^ 3 ^ 3</code>
        → <code class="returnvalue">512</code>
</p>
<p>
<code class="literal">2 ^ (3 ^ 3)</code>
        → <code class="returnvalue">134217728</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">|/</code> <code class="type">double precision</code>
        → <code class="returnvalue">double precision</code>
</p>
<p>
        平方根
       </p>
<p>
<code class="literal">|/ 25.0</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">||/</code> <code class="type">double precision</code>
        → <code class="returnvalue">double precision</code>
</p>
<p>
        立方根
       </p>
<p>
<code class="literal">||/ 64.0</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">@</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        絕對值
       </p>
<p>
<code class="literal">@ -5.0</code>
        → <code class="returnvalue">5.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">&amp;</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        位元 AND
       </p>
<p>
<code class="literal">91 &amp; 15</code>
        → <code class="returnvalue">11</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">|</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        位元 OR
       </p>
<p>
<code class="literal">32 | 3</code>
        → <code class="returnvalue">35</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">#</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        位元互斥 OR
       </p>
<p>
<code class="literal">17 # 5</code>
        → <code class="returnvalue">20</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">~</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        位元 NOT
       </p>
<p>
<code class="literal">~1</code>
        → <code class="returnvalue">-2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">&lt;&lt;</code> <code class="type">integer</code>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        位元左移
       </p>
<p>
<code class="literal">1 &lt;&lt; 4</code>
        → <code class="returnvalue">16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">&gt;&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        位元右移
       </p>
<p>
<code class="literal">8 &gt;&gt; 2</code>
        → <code class="returnvalue">2</code>
</p></td></tr></tbody></table>

<br>

[表 9.5](functions-math.md#FUNCTIONS-MATH-FUNC-TABLE) 列出了可用的數學函式。這些函式中有許多都以具有不同引數型別的多種形式提供。除非另有註明，函式的任何一種形式都回傳與其引數相同的資料型別；跨型別的情況，會以與上面運算子相同的方式解析。處理 `double precision` 資料的函式，大多是以主機系統的 C 函式庫為基礎實作的；因此，精確度以及在邊界情況下的行為，可能會依主機系統而有所不同。

<a id="FUNCTIONS-MATH-FUNC-TABLE"></a>

**表 9.5. 數學函式**

<table border="1" class="table" summary="Mathematical Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.1.1.1.1"></a>
<code class="function">abs</code> ( <em class="replaceable"><code>numeric_type</code></em> )
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        絕對值
       </p>
<p>
<code class="literal">abs(-17.4)</code>
        → <code class="returnvalue">17.4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.2.1.1.1"></a>
<code class="function">cbrt</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        立方根
       </p>
<p>
<code class="literal">cbrt(64.0)</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.3.1.1.1"></a>
<code class="function">ceil</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">ceil</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        大於或等於引數的最接近整數
       </p>
<p>
<code class="literal">ceil(42.2)</code>
        → <code class="returnvalue">43</code>
</p>
<p>
<code class="literal">ceil(-42.8)</code>
        → <code class="returnvalue">-42</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.4.1.1.1"></a>
<code class="function">ceiling</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">ceiling</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        大於或等於引數的最接近整數（與 <code class="function">ceil</code> 相同）
       </p>
<p>
<code class="literal">ceiling(95.3)</code>
        → <code class="returnvalue">96</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.5.1.1.1"></a>
<code class="function">degrees</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        將弧度轉換為度數
       </p>
<p>
<code class="literal">degrees(0.5)</code>
        → <code class="returnvalue">28.64788975654116</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.6.1.1.1"></a>
<code class="function">div</code> ( <em class="parameter"><code>y</code></em> <code class="type">numeric</code>,
        <em class="parameter"><code>x</code></em> <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em> 的整數商（朝零截斷）
       </p>
<p>
<code class="literal">div(9, 4)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.7.1.1.1"></a>
<code class="function">erf</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        誤差函數
       </p>
<p>
<code class="literal">erf(1.0)</code>
        → <code class="returnvalue">0.8427007929497149</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.8.1.1.1"></a>
<code class="function">erfc</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        互補誤差函數（<code class="literal">1 - erf(x)</code>，對於大的輸入不會損失精度）
       </p>
<p>
<code class="literal">erfc(1.0)</code>
        → <code class="returnvalue">0.15729920705028513</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.9.1.1.1"></a>
<code class="function">exp</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">exp</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        指數（<code class="literal">e</code> 的給定次方）
       </p>
<p>
<code class="literal">exp(1.0)</code>
        → <code class="returnvalue">2.7182818284590452</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-FACTORIAL"></a>
<code class="function">factorial</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        階乘
       </p>
<p>
<code class="literal">factorial(5)</code>
        → <code class="returnvalue">120</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.11.1.1.1"></a>
<code class="function">floor</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">floor</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        小於或等於引數的最接近整數
       </p>
<p>
<code class="literal">floor(42.8)</code>
        → <code class="returnvalue">42</code>
</p>
<p>
<code class="literal">floor(-42.8)</code>
        → <code class="returnvalue">-43</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.12.1.1.1"></a>
<code class="function">gamma</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        伽瑪函數
       </p>
<p>
<code class="literal">gamma(0.5)</code>
        → <code class="returnvalue">1.772453850905516</code>
</p>
<p>
<code class="literal">gamma(6)</code>
        → <code class="returnvalue">120</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.13.1.1.1"></a>
<code class="function">gcd</code> ( <em class="replaceable"><code>numeric_type</code></em>, <em class="replaceable"><code>numeric_type</code></em> )
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        最大公因數（能整除兩個輸入而沒有餘數的最大正數）；如果兩個輸入都是零，則回傳 <code class="literal">0</code>；適用於 <code class="type">integer</code>、<code class="type">bigint</code> 與 <code class="type">numeric</code>
</p>
<p>
<code class="literal">gcd(1071, 462)</code>
        → <code class="returnvalue">21</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.14.1.1.1"></a>
<code class="function">lcm</code> ( <em class="replaceable"><code>numeric_type</code></em>, <em class="replaceable"><code>numeric_type</code></em> )
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        最小公倍數（同時是兩個輸入之整數倍的最小嚴格正數）；如果任一輸入為零，則回傳 <code class="literal">0</code>；適用於 <code class="type">integer</code>、<code class="type">bigint</code> 與 <code class="type">numeric</code>
</p>
<p>
<code class="literal">lcm(1071, 462)</code>
        → <code class="returnvalue">23562</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.15.1.1.1"></a>
<code class="function">lgamma</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        伽瑪函數絕對值的自然對數
       </p>
<p>
<code class="literal">lgamma(1000)</code>
        → <code class="returnvalue">5905.220423209181</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.16.1.1.1"></a>
<code class="function">ln</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">ln</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        自然對數
       </p>
<p>
<code class="literal">ln(2.0)</code>
        → <code class="returnvalue">0.6931471805599453</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.17.1.1.1"></a>
<code class="function">log</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">log</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        以 10 為底的對數
       </p>
<p>
<code class="literal">log(100)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.18.1.1.1"></a>
<code class="function">log10</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">log10</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        以 10 為底的對數（與 <code class="function">log</code> 相同）
       </p>
<p>
<code class="literal">log10(1000)</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">log</code> ( <em class="parameter"><code>b</code></em> <code class="type">numeric</code>,
        <em class="parameter"><code>x</code></em> <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        <em class="parameter"><code>x</code></em> 以 <em class="parameter"><code>b</code></em> 為底的對數
</p>
<p>
<code class="literal">log(2.0, 64.0)</code>
       → <code class="returnvalue">6.0000000000000000</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.20.1.1.1"></a>
<code class="function">min_scale</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        精確表示所提供的值所需的最小小數位數（scale）
       </p>
<p>
<code class="literal">min_scale(8.4100)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.21.1.1.1"></a>
<code class="function">mod</code> ( <em class="parameter"><code>y</code></em> <em class="replaceable"><code>numeric_type</code></em>,
        <em class="parameter"><code>x</code></em> <em class="replaceable"><code>numeric_type</code></em> )
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em> 的餘數；適用於 <code class="type">smallint</code>、<code class="type">integer</code>、<code class="type">bigint</code> 與 <code class="type">numeric</code>
</p>
<p>
<code class="literal">mod(9, 4)</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.22.1.1.1"></a>
<code class="function">pi</code> (  )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        <span class="symbol_font">π</span> 的近似值
</p>
<p>
<code class="literal">pi()</code>
        → <code class="returnvalue">3.141592653589793</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.23.1.1.1"></a>
<code class="function">power</code> ( <em class="parameter"><code>a</code></em> <code class="type">numeric</code>,
        <em class="parameter"><code>b</code></em> <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">power</code> ( <em class="parameter"><code>a</code></em> <code class="type">double precision</code>,
        <em class="parameter"><code>b</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
<em class="parameter"><code>a</code></em> 的 <em class="parameter"><code>b</code></em> 次方
</p>
<p>
<code class="literal">power(9, 3)</code>
        → <code class="returnvalue">729</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.24.1.1.1"></a>
<code class="function">radians</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        將度數轉換為弧度
       </p>
<p>
<code class="literal">radians(45.0)</code>
        → <code class="returnvalue">0.7853981633974483</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.25.1.1.1"></a>
<code class="function">round</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">round</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        四捨五入到最接近的整數。對於 <code class="type">numeric</code>，恰好在中間的值會以遠離零的方向捨入。對於 <code class="type">double precision</code>，中間值的處理方式取決於平台，但<span class="quote">“<span class="quote">捨入到最接近的偶數</span>”</span>是最常見的規則。
       </p>
<p>
<code class="literal">round(42.4)</code>
        → <code class="returnvalue">42</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">round</code> ( <em class="parameter"><code>v</code></em> <code class="type">numeric</code>, <em class="parameter"><code>s</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        將 <em class="parameter"><code>v</code></em> 四捨五入到小數點後 <em class="parameter"><code>s</code></em> 位。恰好在中間的值會以遠離零的方向捨入。
       </p>
<p>
<code class="literal">round(42.4382, 2)</code>
        → <code class="returnvalue">42.44</code>
</p>
<p>
<code class="literal">round(1234.56, -1)</code>
        → <code class="returnvalue">1230</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.27.1.1.1"></a>
<code class="function">scale</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        引數的小數位數（scale，即小數部分的十進位位數）
       </p>
<p>
<code class="literal">scale(8.4100)</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.28.1.1.1"></a>
<code class="function">sign</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">sign</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        引數的正負號（-1、0 或 +1）
       </p>
<p>
<code class="literal">sign(-8.4)</code>
        → <code class="returnvalue">-1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.29.1.1.1"></a>
<code class="function">sqrt</code> ( <code class="type">numeric</code> )
         → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">sqrt</code> ( <code class="type">double precision</code> )
         → <code class="returnvalue">double precision</code>
</p>
<p>
        平方根
       </p>
<p>
<code class="literal">sqrt(2)</code>
        → <code class="returnvalue">1.4142135623730951</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.30.1.1.1"></a>
<code class="function">trim_scale</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        藉由移除尾端的零，減少值的小數位數（scale）
       </p>
<p>
<code class="literal">trim_scale(8.4100)</code>
        → <code class="returnvalue">8.41</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.31.1.1.1"></a>
<code class="function">trunc</code> ( <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p class="func_signature">
<code class="function">trunc</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        截斷為整數（朝零截斷）
       </p>
<p>
<code class="literal">trunc(42.8)</code>
        → <code class="returnvalue">42</code>
</p>
<p>
<code class="literal">trunc(-42.8)</code>
        → <code class="returnvalue">-42</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">trunc</code> ( <em class="parameter"><code>v</code></em> <code class="type">numeric</code>, <em class="parameter"><code>s</code></em> <code class="type">integer</code> )
       → <code class="returnvalue">numeric</code>
</p>
<p>
        將 <em class="parameter"><code>v</code></em> 截斷到小數點後 <em class="parameter"><code>s</code></em> 位
       </p>
<p>
<code class="literal">trunc(42.4382, 2)</code>
        → <code class="returnvalue">42.43</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.33.1.1.1"></a>
<code class="function">width_bucket</code> ( <em class="parameter"><code>operand</code></em> <code class="type">numeric</code>, <em class="parameter"><code>low</code></em> <code class="type">numeric</code>, <em class="parameter"><code>high</code></em> <code class="type">numeric</code>, <em class="parameter"><code>count</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<code class="function">width_bucket</code> ( <em class="parameter"><code>operand</code></em> <code class="type">double precision</code>, <em class="parameter"><code>low</code></em> <code class="type">double precision</code>, <em class="parameter"><code>high</code></em> <code class="type">double precision</code>, <em class="parameter"><code>count</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳 <em class="parameter"><code>operand</code></em> 在一個具有 <em class="parameter"><code>count</code></em> 個等寬桶、範圍從 <em class="parameter"><code>low</code></em> 到 <em class="parameter"><code>high</code></em> 的直方圖中所落入之桶的編號。這些桶的下界是包含的，上界則不包含。回傳值為 <code class="literal">0</code> 表示輸入小於 <em class="parameter"><code>low</code></em>，為 <code class="literal"><em class="parameter"><code>count</code></em>+1</code> 則表示輸入大於或等於 <em class="parameter"><code>high</code></em>。如果 <em class="parameter"><code>low</code></em> &gt; <em class="parameter"><code>high</code></em>，行為會鏡像反轉：桶 <code class="literal">1</code> 變成正好位於 <em class="parameter"><code>low</code></em> 之下的桶，而包含的界限則改為在上側。
       </p>
<p>
<code class="literal">width_bucket(5.35, 0.024, 10.06, 5)</code>
        → <code class="returnvalue">3</code>
</p>
<p>
<code class="literal">width_bucket(9, 10, 0, 10)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">width_bucket</code> ( <em class="parameter"><code>operand</code></em> <code class="type">anycompatible</code>, <em class="parameter"><code>thresholds</code></em> <code class="type">anycompatiblearray</code> )
       → <code class="returnvalue">integer</code>
</p>
<p>
        給定一個列出各桶之包含下界的陣列，回傳 <em class="parameter"><code>operand</code></em> 所落入之桶的編號。當輸入小於第一個下界時回傳 <code class="literal">0</code>。<em class="parameter"><code>operand</code></em> 與陣列元素可以是任何具有標準比較運算子的型別。<em class="parameter"><code>thresholds</code></em> 陣列<span class="emphasis"><em>必須依由小到大的順序排序</em></span>，否則會得到非預期的結果。
       </p>
<p>
<code class="literal">width_bucket(now(), array['yesterday', 'today', 'tomorrow']::timestamptz[])</code>
        → <code class="returnvalue">2</code>
</p></td></tr></tbody></table>

<br>

[表 9.6](functions-math.md#FUNCTIONS-MATH-RANDOM-TABLE) 列出了用於產生隨機數的函式。

<a id="FUNCTIONS-MATH-RANDOM-TABLE"></a>

**表 9.6. 隨機函式**

<table border="1" class="table" summary="Random Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.8.2.2.1.1.1.1"></a>
<code class="function">random</code> ( )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        回傳範圍在 0.0 &lt;= x &lt; 1.0 之間的隨機值
       </p>
<p>
<code class="literal">random()</code>
        → <code class="returnvalue">0.897124072839091</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.8.2.2.2.1.1.1"></a>
<code class="function">random</code> ( <em class="parameter"><code>min</code></em> <code class="type">integer</code>, <em class="parameter"><code>max</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<code class="function">random</code> ( <em class="parameter"><code>min</code></em> <code class="type">bigint</code>, <em class="parameter"><code>max</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p class="func_signature">
<code class="function">random</code> ( <em class="parameter"><code>min</code></em> <code class="type">numeric</code>, <em class="parameter"><code>max</code></em> <code class="type">numeric</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        回傳範圍在 <em class="parameter"><code>min</code></em> &lt;= x &lt;= <em class="parameter"><code>max</code></em> 之間的隨機值。對於 <code class="type">numeric</code> 型別，結果的小數位數會與 <em class="parameter"><code>min</code></em> 或 <em class="parameter"><code>max</code></em> 中小數位數較多者相同。
       </p>
<p>
<code class="literal">random(1, 10)</code>
        → <code class="returnvalue">7</code>
</p>
<p>
<code class="literal">random(-0.499, 0.499)</code>
        → <code class="returnvalue">0.347</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.8.2.2.3.1.1.1"></a>
<code class="function">random_normal</code> (
         [<span class="optional"> <em class="parameter"><code>mean</code></em> <code class="type">double precision</code>
         [<span class="optional">, <em class="parameter"><code>stddev</code></em> <code class="type">double precision</code> </span>]</span>] )
         → <code class="returnvalue">double precision</code>
</p>
<p>
        回傳依給定參數之常態分布的隨機值；<em class="parameter"><code>mean</code></em> 預設為 0.0，<em class="parameter"><code>stddev</code></em> 預設為 1.0
       </p>
<p>
<code class="literal">random_normal(0.0, 1.0)</code>
        → <code class="returnvalue">0.051285419</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.8.2.2.4.1.1.1"></a>
<code class="function">setseed</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        為後續的 <code class="literal">random()</code> 與 <code class="literal">random_normal()</code> 呼叫設定種子；引數必須介於 -1.0 與 1.0 之間（含）
       </p>
<p>
<code class="literal">setseed(0.12345)</code>
</p></td></tr></tbody></table>

<br>

[表 9.6](functions-math.md#FUNCTIONS-MATH-RANDOM-TABLE) 所列的 `random()` 與 `random_normal()` 函式，使用的是確定性的虛擬隨機數產生器。它的速度很快，但不適合用於密碼學應用；更安全的替代方案請參閱 [pgcrypto](../../appendixes/contrib/pgcrypto.md) 模組。如果呼叫了 `setseed()`，那麼只要以相同的引數再次執行 `setseed()`，就可以重現目前工作階段中後續呼叫這些函式所得到的結果序列。如果在同一個工作階段中事先沒有呼叫過 `setseed()`，第一次呼叫這些函式中的任何一個時，會從與平台相關的隨機位元來源取得種子。

[表 9.7](functions-math.md#FUNCTIONS-MATH-TRIG-TABLE) 列出了可用的三角函數。每個函式都有兩種變化形式，一種以弧度量測角度，另一種以度數量測角度。

<a id="FUNCTIONS-MATH-TRIG-TABLE"></a>

**表 9.7. 三角函數**

<table border="1" class="table" summary="Trigonometric Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.1.1.1.1"></a>
<code class="function">acos</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反餘弦，結果以弧度表示
       </p>
<p>
<code class="literal">acos(1)</code>
        → <code class="returnvalue">0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.2.1.1.1"></a>
<code class="function">acosd</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反餘弦，結果以度數表示
       </p>
<p>
<code class="literal">acosd(0.5)</code>
        → <code class="returnvalue">60</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.3.1.1.1"></a>
<code class="function">asin</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反正弦，結果以弧度表示
       </p>
<p>
<code class="literal">asin(1)</code>
        → <code class="returnvalue">1.5707963267948966</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.4.1.1.1"></a>
<code class="function">asind</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反正弦，結果以度數表示
       </p>
<p>
<code class="literal">asind(0.5)</code>
        → <code class="returnvalue">30</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.5.1.1.1"></a>
<code class="function">atan</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反正切，結果以弧度表示
       </p>
<p>
<code class="literal">atan(1)</code>
        → <code class="returnvalue">0.7853981633974483</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.6.1.1.1"></a>
<code class="function">atand</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反正切，結果以度數表示
       </p>
<p>
<code class="literal">atand(1)</code>
        → <code class="returnvalue">45</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.7.1.1.1"></a>
<code class="function">atan2</code> ( <em class="parameter"><code>y</code></em> <code class="type">double precision</code>,
        <em class="parameter"><code>x</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em> 的反正切，結果以弧度表示
       </p>
<p>
<code class="literal">atan2(1, 0)</code>
        → <code class="returnvalue">1.5707963267948966</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.8.1.1.1"></a>
<code class="function">atan2d</code> ( <em class="parameter"><code>y</code></em> <code class="type">double precision</code>,
        <em class="parameter"><code>x</code></em> <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em> 的反正切，結果以度數表示
       </p>
<p>
<code class="literal">atan2d(1, 0)</code>
        → <code class="returnvalue">90</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.9.1.1.1"></a>
<code class="function">cos</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        餘弦，引數以弧度表示
       </p>
<p>
<code class="literal">cos(0)</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.10.1.1.1"></a>
<code class="function">cosd</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        餘弦，引數以度數表示
       </p>
<p>
<code class="literal">cosd(60)</code>
        → <code class="returnvalue">0.5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.11.1.1.1"></a>
<code class="function">cot</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        餘切，引數以弧度表示
       </p>
<p>
<code class="literal">cot(0.5)</code>
        → <code class="returnvalue">1.830487721712452</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.12.1.1.1"></a>
<code class="function">cotd</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        餘切，引數以度數表示
       </p>
<p>
<code class="literal">cotd(45)</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.13.1.1.1"></a>
<code class="function">sin</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        正弦，引數以弧度表示
       </p>
<p>
<code class="literal">sin(1)</code>
        → <code class="returnvalue">0.8414709848078965</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.14.1.1.1"></a>
<code class="function">sind</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        正弦，引數以度數表示
       </p>
<p>
<code class="literal">sind(30)</code>
        → <code class="returnvalue">0.5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.15.1.1.1"></a>
<code class="function">tan</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        正切，引數以弧度表示
       </p>
<p>
<code class="literal">tan(1)</code>
        → <code class="returnvalue">1.5574077246549023</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.16.1.1.1"></a>
<code class="function">tand</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        正切，引數以度數表示
       </p>
<p>
<code class="literal">tand(45)</code>
        → <code class="returnvalue">1</code>
</p></td></tr></tbody></table>

<br>

### 注意

處理以度數量測之角度的另一種方式，是使用前面所列的單位轉換函式 `radians()` 與 `degrees()`。不過，建議使用以度數為基礎的三角函數，因為這樣可以避免在 `sind(30)` 這類特殊情況下的捨入誤差。

[表 9.8](functions-math.md#FUNCTIONS-MATH-HYP-TABLE) 列出了可用的雙曲函數。

<a id="FUNCTIONS-MATH-HYP-TABLE"></a>

**表 9.8. 雙曲函數**

<table border="1" class="table" summary="Hyperbolic Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.14.2.2.1.1.1.1"></a>
<code class="function">sinh</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        雙曲正弦
       </p>
<p>
<code class="literal">sinh(1)</code>
        → <code class="returnvalue">1.1752011936438014</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.14.2.2.2.1.1.1"></a>
<code class="function">cosh</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        雙曲餘弦
       </p>
<p>
<code class="literal">cosh(0)</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.14.2.2.3.1.1.1"></a>
<code class="function">tanh</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        雙曲正切
       </p>
<p>
<code class="literal">tanh(1)</code>
        → <code class="returnvalue">0.7615941559557649</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.14.2.2.4.1.1.1"></a>
<code class="function">asinh</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反雙曲正弦
       </p>
<p>
<code class="literal">asinh(1)</code>
        → <code class="returnvalue">0.881373587019543</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.14.2.2.5.1.1.1"></a>
<code class="function">acosh</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反雙曲餘弦
       </p>
<p>
<code class="literal">acosh(1)</code>
        → <code class="returnvalue">0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.14.2.2.6.1.1.1"></a>
<code class="function">atanh</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        反雙曲正切
       </p>
<p>
<code class="literal">atanh(0.5)</code>
        → <code class="returnvalue">0.5493061443340548</code>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-math.html)（原文版本：18.6；核對日期：2026-09-11）
