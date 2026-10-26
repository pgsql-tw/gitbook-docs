<a id="SEG"></a>

## F.39. seg — 線段或浮點數區間的資料型別 [#](#seg) <a href="#seg" id="seg"></a>

[F.39.1. 設計理由](seg.md#SEG-RATIONALE)

[F.39.2. 語法](seg.md#SEG-SYNTAX)

[F.39.3. 精確度](seg.md#SEG-PRECISION)

[F.39.4. 用法](seg.md#SEG-USAGE)

[F.39.5. 注意事項](seg.md#SEG-NOTES)

[F.39.6. 致謝](seg.md#SEG-CREDITS)

<a id="id-1.11.7.49.2"></a>

此模組實作資料型別 `seg`，用來表示線段或浮點數區間。
`seg` 可以表示區間端點的不確定性，因此特別適合用來表示實驗室量測值。

此模組被視為「受信任」，也就是說，具有目前資料庫 `CREATE` 權限的非超級使用者也可以安裝它。

<a id="SEG-RATIONALE"></a>

### F.39.1. 設計理由 [#](#SEG-RATIONALE)

量測值的幾何性質通常比數值連續體中的一個點更複雜。量測值通常是該連續體中邊界有些模糊的一段。量測結果之所以呈現為區間，一方面是因為不確定性與隨機性，另一方面也因為被量測的值本身可能就是一個表示某種條件的區間，例如某種蛋白質維持穩定的溫度範圍。

單憑常識就可以看出，將這類資料儲存為區間，似乎比儲存為一對數字更方便。實際上，在大多數應用中這樣做甚至更有效率。

沿著常識再往下想，邊界的模糊性意味著使用傳統數值資料型別會造成某種程度的資訊流失。想想看：你的儀器讀數為
6.50，你將這個讀數輸入資料庫。取出時會得到什麼？請看：

```

test=> select 6.50 :: float8 as "pH";
 pH
---
6.5
(1 row)
```

在量測的世界裡，6.50 與 6.5 並不相同，兩者的差異有時可能至關重要。實驗者通常會記下（並發表）他們信任的位數。6.50
實際上是一個模糊區間，包含在另一個更大、更模糊的區間 6.5 之內，兩者的中心點（大概）是它們唯一的共同特徵。我們絕對不希望這樣不同的資料項目看起來一模一樣。

結論是什麼？若有一種特殊的資料型別，能以可任意變動的精確度記錄區間的邊界，會很方便。所謂可變動，是指每個資料元素各自記錄自己的精確度。

請看：

```

test=> select '6.25 .. 6.50'::seg as "pH";
          pH
------------
6.25 .. 6.50
(1 row)
```

<a id="SEG-SYNTAX"></a>

### F.39.2. 語法 [#](#SEG-SYNTAX)

區間的外部表示法由一個或兩個浮點數組成，兩數之間以範圍運算子（`..`
或 `...`）連接。另外，也可以指定為中心點加減一個偏差值。
也可以一併儲存選用的確定性指示符（`<`、
`>` 或 `~`）。
（不過，所有內建運算子都會忽略確定性指示符。）
[表 F.29](seg.md#SEG-REPR-TABLE) 概述允許的表示法；[表 F.30](seg.md#SEG-INPUT-EXAMPLES) 列出一些範例。

在[表 F.29](seg.md#SEG-REPR-TABLE) 中，*`x`*、*`y`* 與
*`delta`* 表示浮點數。*`x`* 與 *`y`* 前面可以加上確定性指示符，但
*`delta`* 不可以。

<a id="SEG-REPR-TABLE"></a>

**表 F.29. `seg` 外部表示法**

<table border="1" class="table" summary="seg 外部表示法"><colgroup><col/><col/></colgroup><tbody><tr><td><code class="literal"><em class="replaceable"><code>x</code></em></code></td><td>單一值（長度為零的區間）
      </td></tr><tr><td><code class="literal"><em class="replaceable"><code>x</code></em> .. <em class="replaceable"><code>y</code></em></code></td><td>從 <em class="replaceable"><code>x</code></em> 到 <em class="replaceable"><code>y</code></em> 的區間
</td></tr><tr><td><code class="literal"><em class="replaceable"><code>x</code></em> (+-) <em class="replaceable"><code>delta</code></em></code></td><td>從 <em class="replaceable"><code>x</code></em> - <em class="replaceable"><code>delta</code></em> 到
      <em class="replaceable"><code>x</code></em> + <em class="replaceable"><code>delta</code></em> 的區間
</td></tr><tr><td><code class="literal"><em class="replaceable"><code>x</code></em> ..</code></td><td>下界為 <em class="replaceable"><code>x</code></em> 的開放區間
</td></tr><tr><td><code class="literal">.. <em class="replaceable"><code>x</code></em></code></td><td>上界為 <em class="replaceable"><code>x</code></em> 的開放區間
</td></tr></tbody></table>

<br><a id="SEG-INPUT-EXAMPLES"></a>

**表 F.30. 有效的 `seg` 輸入範例**

<table border="1" class="table" summary="有效的 seg 輸入範例"><colgroup><col class="col1"/><col class="col2"/></colgroup><tbody><tr><td><code class="literal">5.0</code></td><td>
       建立長度為零的線段（也可以說是一個點）
      </td></tr><tr><td><code class="literal">~5.0</code></td><td>
       建立長度為零的線段，並在資料中記錄
       <code class="literal">~</code>。<code class="literal">~</code> 會被
       <code class="type">seg</code> 運算忽略，但會作為註記保留。
      </td></tr><tr><td><code class="literal">&lt;5.0</code></td><td>
       建立位於 5.0 的點。<code class="literal">&lt;</code> 會被忽略，但會作為註記保留。
      </td></tr><tr><td><code class="literal">&gt;5.0</code></td><td>
       建立位於 5.0 的點。<code class="literal">&gt;</code> 會被忽略，但會作為註記保留。
      </td></tr><tr><td><code class="literal">5(+-)0.3</code></td><td>
        建立區間 <code class="literal">4.7 .. 5.3</code>。
        請注意，<code class="literal">(+-)</code> 表示法不會被保留。
      </td></tr><tr><td><code class="literal">50 .. </code></td><td>所有大於或等於 50 的值</td></tr><tr><td><code class="literal">.. 0</code></td><td>所有小於或等於 0 的值</td></tr><tr><td><code class="literal">1.5e-2 .. 2E-2 </code></td><td>建立區間 <code class="literal">0.015 .. 0.02</code></td></tr><tr><td><code class="literal">1 ... 2</code></td><td>
       與 <code class="literal">1...2</code>、<code class="literal">1 .. 2</code>
       或 <code class="literal">1..2</code> 相同
       （範圍運算子前後的空白會被忽略）
      </td></tr></tbody></table>

<br>

由於 `...` 運算子在各種資料來源中廣泛使用，因此允許以它作為 `..` 運算子的另一種寫法。可惜的是，這會造成剖析上的歧義：無法確定
`0...23` 中的上界是指 `23` 還是 `0.23`。
解決方式是要求 `seg` 輸入中的所有數字，在小數點之前至少要有一位數字。

作為合理性檢查，`seg` 會拒絕下界大於上界的區間，例如 `5 .. 2`。

<a id="SEG-PRECISION"></a>

### F.39.3. 精確度 [#](#SEG-PRECISION)

`seg` 值在內部儲存為一對 32 位元浮點數。這表示有效位數超過 7 位的數字會被截斷。

有效位數在 7 位以下的數字會保留原本的精確度。也就是說，若你的查詢傳回 0.00，你可以確定結尾的零並不是格式化造成的假象：它們反映的是原始資料的精確度。前導零的個數不影響精確度：值 0.0067 被視為只有 2 位有效數字。

<a id="SEG-USAGE"></a>

### F.39.4. 用法 [#](#SEG-USAGE)

`seg` 模組包含一個用於
`seg` 值的 GiST 索引運算子類別。
該 GiST 運算子類別支援的運算子列於[表 F.31](seg.md#SEG-GIST-OPERATORS)。

<a id="SEG-GIST-OPERATORS"></a>

**表 F.31. Seg GiST 運算子**

<table border="1" class="table" summary="Seg GiST 運算子"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&lt;&lt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否完全位於第二個的左側？
        若 b &lt; c，則 [a, b] &lt;&lt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&gt;&gt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否完全位於第二個的右側？
        若 a &gt; d，則 [a, b] &gt;&gt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&amp;&lt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否沒有延伸到第二個的右側？
        若 b &lt;= d，則 [a, b] &amp;&lt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&amp;&gt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否沒有延伸到第二個的左側？
        若 a &gt;= c，則 [a, b] &amp;&gt; [c, d] 為真。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">=</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個 <code class="type">seg</code> 是否相等？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&amp;&amp;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個 <code class="type">seg</code> 是否重疊？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">@&gt;</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否包含第二個？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">seg</code> <code class="literal">&lt;@</code> <code class="type">seg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 <code class="type">seg</code> 是否包含於第二個？
       </p></td></tr></tbody></table>

<br>

除了上述運算子之外，[表 9.1](../../the-sql-language/functions/functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子也可用於型別
`seg`。這些運算子會先比較 (a) 與 (c)，若兩者相等，再比較 (b) 與 (d)。在大多數情況下，這會產生相當合理的排序，若你想對此型別使用
ORDER BY，這會很有用。

<a id="SEG-NOTES"></a>

### F.39.5. 注意事項 [#](#SEG-NOTES)

使用範例請參閱迴歸測試 `sql/seg.sql`。

將 `(+-)` 轉換為一般範圍的機制，在判定邊界的有效位數時並不完全準確。例如，若產生的區間包含 10 的乘冪，它會在下界多加一位數字：

```

postgres=> select '10(+-)1'::seg as seg;
      seg
---------
9.0 .. 11             -- should be: 9 .. 11
```

R-tree 索引的效能在很大程度上取決於輸入值最初的順序。依 `seg`
欄位對輸入資料表排序可能非常有幫助；範例請參閱指令稿 `sort-segments.pl`。

<a id="SEG-CREDITS"></a>

### F.39.6. 致謝 [#](#SEG-CREDITS)

原作者：Gene Selkov, Jr. `<selkovjr@mcs.anl.gov>`，
Argonne National Laboratory 數學與電腦科學部門（Mathematics and Computer Science Division）。

我首先要感謝 Joe Hellerstein 教授
（<https://dsf.berkeley.edu/jmh/>）闡明了 GiST 的精髓（<http://gist.cs.berkeley.edu/>）。我也感謝所有過去與現在的
Postgres 開發者，讓我能夠建立自己的世界，並在其中不受打擾地生活。此外，我要向 Argonne 實驗室與美國能源部致上謝意，感謝他們多年來對我資料庫研究的忠實支持。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/seg.html)（原文版本：18.6；核對日期：2026-10-22）
