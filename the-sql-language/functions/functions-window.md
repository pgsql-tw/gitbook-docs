<a id="FUNCTIONS-WINDOW"></a>

## 9.22. Window 函式 [#](#FUNCTIONS-WINDOW)

<a id="id-1.5.8.28.2"></a>

*Window 函式*（window function）提供了對與目前查詢資料列相關的資料列集合進行計算的能力。關於這項功能的介紹，請參閱[第 3.5 節](../../tutorial/tutorial-advanced/tutorial-window.md)；語法細節則請參閱[第 4.2.8 節](../sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)。

內建的 window 函式列於[表 9.67](functions-window.md#FUNCTIONS-WINDOW-TABLE)。請注意，這些函式*必須*使用 window 函式語法呼叫，也就是必須有 `OVER` 子句。

除了這些函式之外，任何內建或使用者定義的一般彙總函式（也就是非有序集合或假設集合彙總函式）都可以用作 window 函式；內建彙總函式的清單請參閱[第 9.21 節](functions-aggregate.md)。只有當呼叫後面接著 `OVER` 子句時，彙總函式才會作為 window 函式運作；否則它們會作為一般的彙總函式運作，並為整個集合回傳單一資料列。

<a id="FUNCTIONS-WINDOW-TABLE"></a>

**表 9.67. 通用 Window 函式**

<table border="1" class="table" summary="General-Purpose Window Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.1.1.1.1"></a>
<code class="function">row_number</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳目前資料列在其分割區中的編號，從 1 開始計算。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.2.1.1.1"></a>
<code class="function">rank</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳目前資料列的排名，有間隙；也就是其同儕群組中第一筆資料列的 <code class="function">row_number</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.3.1.1.1"></a>
<code class="function">dense_rank</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳目前資料列的排名，沒有間隙；這個函式實際上是在計算同儕群組的數量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.4.1.1.1"></a>
<code class="function">percent_rank</code> ()
        → <code class="returnvalue">double precision</code>
</p>
<p>
        回傳目前資料列的相對排名，也就是 (<code class="function">rank</code> - 1) / (分割區資料列總數 - 1)。因此其值的範圍是 0 到 1（含）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.5.1.1.1"></a>
<code class="function">cume_dist</code> ()
        → <code class="returnvalue">double precision</code>
</p>
<p>
        回傳累積分布，也就是（排在目前資料列之前或與之同儕的分割區資料列數）/（分割區資料列總數）。因此其值的範圍是 1/<em class="parameter"><code>N</code></em> 到 1。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.6.1.1.1"></a>
<code class="function">ntile</code> ( <em class="parameter"><code>num_buckets</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳從 1 到引數值的整數，盡可能平均地劃分分割區。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.7.1.1.1"></a>
<code class="function">lag</code> ( <em class="parameter"><code>value</code></em> <code class="type">anycompatible</code>
          [<span class="optional">, <em class="parameter"><code>offset</code></em> <code class="type">integer</code>
          [<span class="optional">, <em class="parameter"><code>default</code></em> <code class="type">anycompatible</code> </span>]</span>] )
        → <code class="returnvalue">anycompatible</code>
</p>
<p>
        回傳 <em class="parameter"><code>value</code></em> 在分割區中位於目前資料列之前第 <em class="parameter"><code>offset</code></em> 筆之資料列上的評估結果；如果沒有這樣的資料列，則改為回傳 <em class="parameter"><code>default</code></em>（其型別必須與 <em class="parameter"><code>value</code></em> 相容）。<em class="parameter"><code>offset</code></em> 與 <em class="parameter"><code>default</code></em> 都是相對於目前資料列評估的。如果省略，<em class="parameter"><code>offset</code></em> 預設為 1，<em class="parameter"><code>default</code></em> 預設為 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.8.1.1.1"></a>
<code class="function">lead</code> ( <em class="parameter"><code>value</code></em> <code class="type">anycompatible</code>
          [<span class="optional">, <em class="parameter"><code>offset</code></em> <code class="type">integer</code>
          [<span class="optional">, <em class="parameter"><code>default</code></em> <code class="type">anycompatible</code> </span>]</span>] )
        → <code class="returnvalue">anycompatible</code>
</p>
<p>
        回傳 <em class="parameter"><code>value</code></em> 在分割區中位於目前資料列之後第 <em class="parameter"><code>offset</code></em> 筆之資料列上的評估結果；如果沒有這樣的資料列，則改為回傳 <em class="parameter"><code>default</code></em>（其型別必須與 <em class="parameter"><code>value</code></em> 相容）。<em class="parameter"><code>offset</code></em> 與 <em class="parameter"><code>default</code></em> 都是相對於目前資料列評估的。如果省略，<em class="parameter"><code>offset</code></em> 預設為 1，<em class="parameter"><code>default</code></em> 預設為 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.9.1.1.1"></a>
<code class="function">first_value</code> ( <em class="parameter"><code>value</code></em> <code class="type">anyelement</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        回傳在視窗框架第一筆資料列上評估 <em class="parameter"><code>value</code></em> 的結果。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.10.1.1.1"></a>
<code class="function">last_value</code> ( <em class="parameter"><code>value</code></em> <code class="type">anyelement</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        回傳在視窗框架最後一筆資料列上評估 <em class="parameter"><code>value</code></em> 的結果。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.28.6.2.2.11.1.1.1"></a>
<code class="function">nth_value</code> ( <em class="parameter"><code>value</code></em> <code class="type">anyelement</code>, <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">anyelement</code>
</p>
<p>
        回傳 <em class="parameter"><code>value</code></em> 在視窗框架第 <em class="parameter"><code>n</code></em> 筆資料列（從 1 開始計算）上的評估結果；如果沒有這樣的資料列，則回傳 <code class="literal">NULL</code>。
       </p></td></tr></tbody></table>

<br>

[表 9.67](functions-window.md#FUNCTIONS-WINDOW-TABLE) 所列的所有函式，都取決於相關聯之 window 定義中 `ORDER BY` 子句所指定的排序順序。只考慮 `ORDER BY` 欄位時彼此沒有區別的資料列，稱為*同儕*（peer）。四個排名函式（包括 `cume_dist`）的定義，使它們對同一個同儕群組中的所有資料列都給出相同的答案。

請注意，`first_value`、`last_value` 與 `nth_value` 只考慮「視窗框架」（window frame）內的資料列，而預設的視窗框架包含從分割區開頭到目前資料列之最後一個同儕為止的資料列。這很可能讓 `last_value`（有時也包括 `nth_value`）給出沒有幫助的結果。你可以在 `OVER` 子句中加上合適的框架規格（`RANGE`、`ROWS` 或 `GROUPS`）來重新定義框架。關於框架規格的更多資訊，請參閱[第 4.2.8 節](../sql-syntax/sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)。

當彙總函式用作 window 函式時，它會彙總目前資料列之視窗框架內的資料列。搭配 `ORDER BY` 與預設視窗框架定義使用的彙總函式，會產生「累計總和」類型的行為，而這不一定是你想要的。要對整個分割區進行彙總，請省略 `ORDER BY`，或使用 `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`。使用其他框架規格可以得到其他效果。

### 注意

SQL 標準為 `lead`、`lag`、`first_value`、`last_value` 與 `nth_value` 定義了 `RESPECT NULLS` 或 `IGNORE NULLS` 選項。PostgreSQL 並未實作這個選項：其行為一律與標準的預設值相同，也就是 `RESPECT NULLS`。同樣地，標準中 `nth_value` 的 `FROM FIRST` 或 `FROM LAST` 選項也沒有實作：只支援預設的 `FROM FIRST` 行為。（你可以藉由反轉 `ORDER BY` 的排序來得到 `FROM LAST` 的結果。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-window.html)（原文版本：18.6；核對日期：2026-09-11）
