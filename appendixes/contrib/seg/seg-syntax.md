# F.39.2. 語法

<a id="SEG-SYNTAX"></a>

## F.39.2. 語法 [#](#seg-syntax) <a href="#seg-syntax" id="seg-syntax"></a>

區間的外部表示法由一個或兩個浮點數組成，兩數之間以範圍運算子（`..`
或 `...`）連接。另外，也可以指定為中心點加減一個偏差值。
也可以一併儲存選用的確定性指示符（`<`、
`>` 或 `~`）。
（不過，所有內建運算子都會忽略確定性指示符。）
[表 F.29](#seg-repr-table) 概述允許的表示法；[表 F.30](#seg-input-examples) 列出一些範例。

在[表 F.29](#seg-repr-table) 中，*`x`*、*`y`* 與
*`delta`* 表示浮點數。*`x`* 與 *`y`* 前面可以加上確定性指示符，但
*`delta`* 不可以。

<a id="SEG-REPR-TABLE"></a>

### 表 F.29. `seg` 外部表示法 [#](#seg-repr-table) <a href="#seg-repr-table" id="seg-repr-table"></a>

<table border="1" class="table" summary="seg 外部表示法"><colgroup><col/><col/></colgroup><tbody><tr><td><code class="literal"><em class="replaceable"><code>x</code></em></code></td><td>單一值（長度為零的區間）
      </td></tr><tr><td><code class="literal"><em class="replaceable"><code>x</code></em> .. <em class="replaceable"><code>y</code></em></code></td><td>從 <em class="replaceable"><code>x</code></em> 到 <em class="replaceable"><code>y</code></em> 的區間
</td></tr><tr><td><code class="literal"><em class="replaceable"><code>x</code></em> (+-) <em class="replaceable"><code>delta</code></em></code></td><td>從 <em class="replaceable"><code>x</code></em> - <em class="replaceable"><code>delta</code></em> 到
      <em class="replaceable"><code>x</code></em> + <em class="replaceable"><code>delta</code></em> 的區間
</td></tr><tr><td><code class="literal"><em class="replaceable"><code>x</code></em> ..</code></td><td>下界為 <em class="replaceable"><code>x</code></em> 的開放區間
</td></tr><tr><td><code class="literal">.. <em class="replaceable"><code>x</code></em></code></td><td>上界為 <em class="replaceable"><code>x</code></em> 的開放區間
</td></tr></tbody></table>

<br><a id="SEG-INPUT-EXAMPLES"></a>

### 表 F.30. 有效的 `seg` 輸入範例 [#](#seg-input-examples) <a href="#seg-input-examples" id="seg-input-examples"></a>

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

[返回 F.39. seg — 線段或浮點數區間的資料型別](../seg.md#seg)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/seg.html)（原文版本：18.6；核對日期：2026-10-22）
