## 9.3. Mathematical Functions and Operators [#](#FUNCTIONS-MATH)

Mathematical operators are provided for many
PostgreSQL types. For types without
standard mathematical conventions
(e.g., date/time types) we
describe the actual behavior in subsequent sections.

[Table 9.4](functions-math.md#FUNCTIONS-MATH-OP-TABLE) shows the mathematical
operators that are available for the standard numeric types.
Unless otherwise noted, operators shown as
accepting *`numeric_type`* are available for all
the types `smallint`, `integer`,
`bigint`, `numeric`, `real`,
and `double precision`.
Operators shown as accepting *`integral_type`*
are available for the types `smallint`, `integer`,
and `bigint`.
Except where noted, each form of an operator returns the same data type
as its argument(s). Calls involving multiple argument data types, such
as `integer` `+` `numeric`,
are resolved by using the type appearing later in these lists.

<a id="FUNCTIONS-MATH-OP-TABLE"></a>

**Table 9.4. Mathematical Operators**

<table border="1" class="table" summary="Mathematical Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">+</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Addition
       </p>
<p>
<code class="literal">2 + 3</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">+</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Unary plus (no operation)
       </p>
<p>
<code class="literal">+ 3.5</code>
        → <code class="returnvalue">3.5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">-</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Subtraction
       </p>
<p>
<code class="literal">2 - 3</code>
        → <code class="returnvalue">-1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">-</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Negation
       </p>
<p>
<code class="literal">- (-4)</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">*</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Multiplication
       </p>
<p>
<code class="literal">2 * 3</code>
        → <code class="returnvalue">6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>numeric_type</code></em> <code class="literal">/</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Division (for integral types, division truncates the result towards
        zero)
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
        Modulo (remainder); available for <code class="type">smallint</code>,
        <code class="type">integer</code>, <code class="type">bigint</code>, and <code class="type">numeric</code>
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
        Exponentiation
       </p>
<p>
<code class="literal">2 ^ 3</code>
        → <code class="returnvalue">8</code>
</p>
<p>
        Unlike typical mathematical practice, multiple uses of
        <code class="literal">^</code> will associate left to right by default:
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
        Square root
       </p>
<p>
<code class="literal">|/ 25.0</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">||/</code> <code class="type">double precision</code>
        → <code class="returnvalue">double precision</code>
</p>
<p>
        Cube root
       </p>
<p>
<code class="literal">||/ 64.0</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">@</code> <em class="replaceable"><code>numeric_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Absolute value
       </p>
<p>
<code class="literal">@ -5.0</code>
        → <code class="returnvalue">5.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">&amp;</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        Bitwise AND
       </p>
<p>
<code class="literal">91 &amp; 15</code>
        → <code class="returnvalue">11</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">|</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        Bitwise OR
       </p>
<p>
<code class="literal">32 | 3</code>
        → <code class="returnvalue">35</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">#</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        Bitwise exclusive OR
       </p>
<p>
<code class="literal">17 # 5</code>
        → <code class="returnvalue">20</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">~</code> <em class="replaceable"><code>integral_type</code></em>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        Bitwise NOT
       </p>
<p>
<code class="literal">~1</code>
        → <code class="returnvalue">-2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">&lt;&lt;</code> <code class="type">integer</code>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        Bitwise shift left
       </p>
<p>
<code class="literal">1 &lt;&lt; 4</code>
        → <code class="returnvalue">16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>integral_type</code></em> <code class="literal">&gt;&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue"><em class="replaceable"><code>integral_type</code></em></code>
</p>
<p>
        Bitwise shift right
       </p>
<p>
<code class="literal">8 &gt;&gt; 2</code>
        → <code class="returnvalue">2</code>
</p></td></tr></tbody></table>

<br>

[Table 9.5](functions-math.md#FUNCTIONS-MATH-FUNC-TABLE) shows the available
mathematical functions.
Many of these functions are provided in multiple forms with different
argument types.
Except where noted, any given form of a function returns the same
data type as its argument(s); cross-type cases are resolved in the
same way as explained above for operators.
The functions working with `double precision` data are mostly
implemented on top of the host system's C library; accuracy and behavior in
boundary cases can therefore vary depending on the host system.

<a id="FUNCTIONS-MATH-FUNC-TABLE"></a>

**Table 9.5. Mathematical Functions**

<table border="1" class="table" summary="Mathematical Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.6.2.2.1.1.1.1"></a>
<code class="function">abs</code> ( <em class="replaceable"><code>numeric_type</code></em> )
        → <code class="returnvalue"><em class="replaceable"><code>numeric_type</code></em></code>
</p>
<p>
        Absolute value
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
        Cube root
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
        Nearest integer greater than or equal to argument
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
        Nearest integer greater than or equal to argument (same
        as <code class="function">ceil</code>)
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
        Converts radians to degrees
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
        Integer quotient of <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em>
        (truncates towards zero)
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
        Error function
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
        Complementary error function (<code class="literal">1 - erf(x)</code>, without
        loss of precision for large inputs)
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
        Exponential (<code class="literal">e</code> raised to the given power)
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
        Factorial
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
        Nearest integer less than or equal to argument
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
        Gamma function
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
        Greatest common divisor (the largest positive number that divides both
        inputs with no remainder); returns <code class="literal">0</code> if both inputs
        are zero; available for <code class="type">integer</code>, <code class="type">bigint</code>,
        and <code class="type">numeric</code>
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
        Least common multiple (the smallest strictly positive number that is
        an integral multiple of both inputs); returns <code class="literal">0</code> if
        either input is zero; available for <code class="type">integer</code>,
        <code class="type">bigint</code>, and <code class="type">numeric</code>
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
        Natural logarithm of the absolute value of the gamma function
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
        Natural logarithm
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
        Base 10 logarithm
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
        Base 10 logarithm (same as <code class="function">log</code>)
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
        Logarithm of <em class="parameter"><code>x</code></em> to base <em class="parameter"><code>b</code></em>
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
        Minimum scale (number of fractional decimal digits) needed
        to represent the supplied value precisely
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
        Remainder of <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em>;
        available for <code class="type">smallint</code>, <code class="type">integer</code>,
        <code class="type">bigint</code>, and <code class="type">numeric</code>
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
        Approximate value of <span class="symbol_font">π</span>
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
<em class="parameter"><code>a</code></em> raised to the power of <em class="parameter"><code>b</code></em>
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
        Converts degrees to radians
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
        Rounds to nearest integer.  For <code class="type">numeric</code>, ties are
        broken by rounding away from zero.  For <code class="type">double precision</code>,
        the tie-breaking behavior is platform dependent, but
        <span class="quote">“<span class="quote">round to nearest even</span>”</span> is the most common rule.
       </p>
<p>
<code class="literal">round(42.4)</code>
        → <code class="returnvalue">42</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">round</code> ( <em class="parameter"><code>v</code></em> <code class="type">numeric</code>, <em class="parameter"><code>s</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">numeric</code>
</p>
<p>
        Rounds <em class="parameter"><code>v</code></em> to <em class="parameter"><code>s</code></em> decimal
        places.  Ties are broken by rounding away from zero.
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
        Scale of the argument (the number of decimal digits in the fractional part)
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
        Sign of the argument (-1, 0, or +1)
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
        Square root
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
        Reduces the value's scale (number of fractional decimal digits) by
        removing trailing zeroes
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
        Truncates to integer (towards zero)
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
        Truncates <em class="parameter"><code>v</code></em> to <em class="parameter"><code>s</code></em>
        decimal places
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
        Returns the number of the bucket in
        which <em class="parameter"><code>operand</code></em> falls in a histogram
        having <em class="parameter"><code>count</code></em> equal-width buckets spanning the
        range <em class="parameter"><code>low</code></em> to <em class="parameter"><code>high</code></em>.
        The buckets have inclusive lower bounds and exclusive upper bounds.
        Returns <code class="literal">0</code> for an input less
        than <em class="parameter"><code>low</code></em>,
        or <code class="literal"><em class="parameter"><code>count</code></em>+1</code> for an input
        greater than or equal to <em class="parameter"><code>high</code></em>.
        If <em class="parameter"><code>low</code></em> &gt; <em class="parameter"><code>high</code></em>,
        the behavior is mirror-reversed, with bucket <code class="literal">1</code>
        now being the one just below <em class="parameter"><code>low</code></em>, and the
        inclusive bounds now being on the upper side.
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
        Returns the number of the bucket in
        which <em class="parameter"><code>operand</code></em> falls given an array listing the
        inclusive lower bounds of the buckets.
        Returns <code class="literal">0</code> for an input less than the first lower
        bound.  <em class="parameter"><code>operand</code></em> and the array elements can be
        of any type having standard comparison operators.
        The <em class="parameter"><code>thresholds</code></em> array <span class="emphasis"><em>must be
        sorted</em></span>, smallest first, or unexpected results will be
        obtained.
       </p>
<p>
<code class="literal">width_bucket(now(), array['yesterday', 'today', 'tomorrow']::timestamptz[])</code>
        → <code class="returnvalue">2</code>
</p></td></tr></tbody></table>

<br>

[Table 9.6](functions-math.md#FUNCTIONS-MATH-RANDOM-TABLE) shows functions for
generating random numbers.

<a id="FUNCTIONS-MATH-RANDOM-TABLE"></a>

**Table 9.6. Random Functions**

<table border="1" class="table" summary="Random Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.8.2.2.1.1.1.1"></a>
<code class="function">random</code> ( )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        Returns a random value in the range 0.0 &lt;= x &lt; 1.0
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
        Returns a random value in the range
        <em class="parameter"><code>min</code></em> &lt;= x &lt;= <em class="parameter"><code>max</code></em>.
        For type <code class="type">numeric</code>, the result will have the same number of
        fractional decimal digits as <em class="parameter"><code>min</code></em> or
        <em class="parameter"><code>max</code></em>, whichever has more.
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
        Returns a random value from the normal distribution with the given
        parameters; <em class="parameter"><code>mean</code></em> defaults to 0.0
        and <em class="parameter"><code>stddev</code></em> defaults to 1.0
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
        Sets the seed for subsequent <code class="literal">random()</code> and
        <code class="literal">random_normal()</code> calls;
        argument must be between -1.0 and 1.0, inclusive
       </p>
<p>
<code class="literal">setseed(0.12345)</code>
</p></td></tr></tbody></table>

<br>

The `random()` and `random_normal()`
functions listed in [Table 9.6](functions-math.md#FUNCTIONS-MATH-RANDOM-TABLE) use a
deterministic pseudo-random number generator.
It is fast but not suitable for cryptographic
applications; see the [pgcrypto](../../appendixes/contrib/pgcrypto.md) module for a more
secure alternative.
If `setseed()` is called, the series of results of
subsequent calls to these functions in the current session
can be repeated by re-issuing `setseed()` with the same
argument.
Without any prior `setseed()` call in the same
session, the first call to any of these functions obtains a seed
from a platform-dependent source of random bits.

[Table 9.7](functions-math.md#FUNCTIONS-MATH-TRIG-TABLE) shows the
available trigonometric functions. Each of these functions comes in
two variants, one that measures angles in radians and one that
measures angles in degrees.

<a id="FUNCTIONS-MATH-TRIG-TABLE"></a>

**Table 9.7. Trigonometric Functions**

<table border="1" class="table" summary="Trigonometric Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.11.2.2.1.1.1.1"></a>
<code class="function">acos</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        Inverse cosine, result in radians
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
        Inverse cosine, result in degrees
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
        Inverse sine, result in radians
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
        Inverse sine, result in degrees
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
        Inverse tangent, result in radians
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
        Inverse tangent, result in degrees
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
        Inverse tangent of
        <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em>,
        result in radians
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
        Inverse tangent of
        <em class="parameter"><code>y</code></em>/<em class="parameter"><code>x</code></em>,
        result in degrees
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
        Cosine, argument in radians
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
        Cosine, argument in degrees
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
        Cotangent, argument in radians
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
        Cotangent, argument in degrees
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
        Sine, argument in radians
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
        Sine, argument in degrees
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
        Tangent, argument in radians
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
        Tangent, argument in degrees
       </p>
<p>
<code class="literal">tand(45)</code>
        → <code class="returnvalue">1</code>
</p></td></tr></tbody></table>

<br>

### Note

Another way to work with angles measured in degrees is to use the unit
transformation functions `radians()`
and `degrees()` shown earlier.
However, using the degree-based trigonometric functions is preferred,
as that way avoids round-off error for special cases such
as `sind(30)`.

[Table 9.8](functions-math.md#FUNCTIONS-MATH-HYP-TABLE) shows the
available hyperbolic functions.

<a id="FUNCTIONS-MATH-HYP-TABLE"></a>

**Table 9.8. Hyperbolic Functions**

<table border="1" class="table" summary="Hyperbolic Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.9.14.2.2.1.1.1.1"></a>
<code class="function">sinh</code> ( <code class="type">double precision</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        Hyperbolic sine
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
        Hyperbolic cosine
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
        Hyperbolic tangent
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
        Inverse hyperbolic sine
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
        Inverse hyperbolic cosine
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
        Inverse hyperbolic tangent
       </p>
<p>
<code class="literal">atanh(0.5)</code>
        → <code class="returnvalue">0.5493061443340548</code>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-math.html)（英文原文，待翻譯）
