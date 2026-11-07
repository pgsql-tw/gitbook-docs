# F.10.3. 用法

<a id="CUBE-USAGE"></a>

## F.10.3. 用法 [#](#cube-usage) <a href="#cube-usage" id="cube-usage"></a>

[表 F.2](#cube-operators-table) 顯示為 `cube` 型別提供的專用運算子。

<a id="CUBE-OPERATORS-TABLE"></a>

### 表 F.2. Cube 運算子 [#](#cube-operators-table) <a href="#cube-operators-table" id="cube-operators-table"></a>

<table border="1" class="table" summary="Cube 運算子"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">&amp;&amp;</code> <code class="type">cube</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        兩個 cube 是否重疊？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">@&gt;</code> <code class="type">cube</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 cube 是否包含第二個？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">&lt;@</code> <code class="type">cube</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個 cube 是否包含於第二個？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">-&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">float8</code>
</p>
<p>
        擷取 cube 的第 <em class="parameter"><code>n</code></em> 個座標
        （從 1 開始計數）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">~&gt;</code> <code class="type">integer</code>
        → <code class="returnvalue">float8</code>
</p>
<p>
        擷取 cube 的第 <em class="parameter"><code>n</code></em> 個座標，
        計數方式如下：<em class="parameter"><code>n</code></em> = 2
        * <em class="parameter"><code>k</code></em> - 1 表示第 <em class="parameter"><code>k</code></em> 維的
        下界，<em class="parameter"><code>n</code></em> = 2 * <em class="parameter"><code>k</code></em>
        表示第 <em class="parameter"><code>k</code></em> 維的上界。負的
        <em class="parameter"><code>n</code></em> 表示相應正座標的反值。此運算子設計用於支援 KNN-GiST。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">&lt;-&gt;</code> <code class="type">cube</code>
        → <code class="returnvalue">float8</code>
</p>
<p>
        計算兩個 cube 之間的歐幾里得距離。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">&lt;#&gt;</code> <code class="type">cube</code>
        → <code class="returnvalue">float8</code>
</p>
<p>
        計算兩個 cube 之間的計程車（L-1 度量）距離。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">cube</code> <code class="literal">&lt;=&gt;</code> <code class="type">cube</code>
        → <code class="returnvalue">float8</code>
</p>
<p>
        計算兩個 cube 之間的 Chebyshev（L-inf 度量）距離。
       </p></td></tr></tbody></table>

<br>

除了上述運算子外，`cube` 型別也可使用[表 9.1](../../../the-sql-language/functions/functions-comparison.md#functions-comparison-table)
所示的一般比較運算子。這些運算子會先比較第一個座標，若相等再比較第二個
座標，依此類推。它們主要用於支援 `cube` 的 B-tree 索引運算子類別；例如，
你想要在 `cube` 欄位上建立 UNIQUE 限制條件時可能有用。除此之外，此排序沒有
太多實務用途。

`cube` 模組也為 `cube` 值提供 GiST 索引運算子類別。`cube` GiST 索引可用於
在 `WHERE` 子句中，以 `=`、`&&`、`@>` 和 `<@` 運算子搜尋值。

此外，`cube` GiST 索引可在 `ORDER BY` 子句中使用度量運算子 `<->`、`<#>`
和 `<=>` 尋找最近鄰。例如，可用下列方式有效找出三維點 (0.5, 0.5, 0.5)
的最近鄰：

```

SELECT c FROM test ORDER BY c <-> cube(array[0.5,0.5,0.5]) LIMIT 1;
```

`~>` 運算子也能以此方式，依選定座標排序並有效擷取前幾個值。例如，若要
依第一個座標（左下角）遞增順序取得前幾個 cube，可使用下列查詢：

```

SELECT c FROM test ORDER BY c ~> 1 LIMIT 5;
```

若要依右上角的第一個座標遞減順序取得二維 cube：

```

SELECT c FROM test ORDER BY c ~> 3 DESC LIMIT 5;
```

[表 F.3](#cube-functions-table) 顯示可用函式。

<a id="CUBE-FUNCTIONS-TABLE"></a>

### 表 F.3. Cube 函式 [#](#cube-functions-table) <a href="#cube-functions-table" id="cube-functions-table"></a>

<table border="1" class="table" summary="Cube 函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube</code> ( <code class="type">float8</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        建立兩個座標相同的一維 cube。
       </p>
<p>
<code class="literal">cube(1)</code>
        → <code class="returnvalue">(1)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube</code> ( <code class="type">float8</code>, <code class="type">float8</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        建立一維 cube。
       </p>
<p>
<code class="literal">cube(1, 2)</code>
        → <code class="returnvalue">(1),(2)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube</code> ( <code class="type">float8[]</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        使用陣列定義的座標建立體積為零的 cube。
       </p>
<p>
<code class="literal">cube(ARRAY[1,2,3])</code>
        → <code class="returnvalue">(1, 2, 3)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube</code> ( <code class="type">float8[]</code>, <code class="type">float8[]</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        以兩個陣列所定義的右上與左下座標建立 cube；兩個陣列的長度必須相同。
       </p>
<p>
<code class="literal">cube(ARRAY[1,2], ARRAY[3,4])</code>
        → <code class="returnvalue">(1, 2),(3, 4)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube</code> ( <code class="type">cube</code>, <code class="type">float8</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        對既有 cube 加入一個維度以建立新 cube，新增座標的兩個端點值相同。這可用於
        依計算所得的值逐步建立 cube。
       </p>
<p>
<code class="literal">cube('(1,2),(3,4)'::cube, 5)</code>
        → <code class="returnvalue">(1, 2, 5),(3, 4, 5)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube</code> ( <code class="type">cube</code>, <code class="type">float8</code>, <code class="type">float8</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        對既有 cube 加入一個維度以建立新 cube。這可用於依計算所得的值逐步建立 cube。
       </p>
<p>
<code class="literal">cube('(1,2),(3,4)'::cube, 5, 6)</code>
        → <code class="returnvalue">(1, 2, 5),(3, 4, 6)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_dim</code> ( <code class="type">cube</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回 cube 的維度數。
       </p>
<p>
<code class="literal">cube_dim('(1,2),(3,4)')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_ll_coord</code> ( <code class="type">cube</code>, <code class="type">integer</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        傳回 cube 左下角的第 <em class="parameter"><code>n</code></em> 個座標值。
       </p>
<p>
<code class="literal">cube_ll_coord('(1,2),(3,4)', 2)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_ur_coord</code> ( <code class="type">cube</code>, <code class="type">integer</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        傳回 cube 右上角的第 <em class="parameter"><code>n</code></em> 個座標值。
       </p>
<p>
<code class="literal">cube_ur_coord('(1,2),(3,4)', 2)</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_is_point</code> ( <code class="type">cube</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        若 cube 是點（亦即定義它的兩個角點相同）則傳回 true。
       </p>
<p>
<code class="literal">cube_is_point(cube(1,1))</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_distance</code> ( <code class="type">cube</code>, <code class="type">cube</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        傳回兩個 cube 之間的距離。若兩個 cube 都是點，這就是一般距離函式。
       </p>
<p>
<code class="literal">cube_distance('(1,2)', '(3,4)')</code>
        → <code class="returnvalue">2.8284271247461903</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_subset</code> ( <code class="type">cube</code>, <code class="type">integer[]</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        使用陣列中的維度索引清單，從既有 cube 建立新 cube。可用於擷取單一維度的
        端點、移除維度，或依需要重新排序維度。
       </p>
<p>
<code class="literal">cube_subset(cube('(1,3,5),(6,7,8)'), ARRAY[2])</code>
        → <code class="returnvalue">(3),(7)</code>
</p>
<p>
<code class="literal">cube_subset(cube('(1,3,5),(6,7,8)'), ARRAY[3,2,1,1])</code>
        → <code class="returnvalue">(5, 3, 1, 1),(8, 7, 6, 6)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_union</code> ( <code class="type">cube</code>, <code class="type">cube</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        產生兩個 cube 的聯集。
       </p>
<p>
<code class="literal">cube_union('(1,2)', '(3,4)')</code>
        → <code class="returnvalue">(1, 2),(3, 4)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_inter</code> ( <code class="type">cube</code>, <code class="type">cube</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        產生兩個 cube 的交集。
       </p>
<p>
<code class="literal">cube_inter('(1,2)', '(3,4)')</code>
        → <code class="returnvalue">(3, 4),(1, 2)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">cube_enlarge</code> ( <em class="parameter"><code>c</code></em> <code class="type">cube</code>, <em class="parameter"><code>r</code></em> <code class="type">double</code>, <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        在至少 <em class="parameter"><code>n</code></em> 個維度中，以指定半徑
        <em class="parameter"><code>r</code></em> 增加 cube 的大小。半徑為負時則縮小 cube。
        所有已定義維度都會依半徑 <em class="parameter"><code>r</code></em> 變更：左下座標減去
        <em class="parameter"><code>r</code></em>，右上座標加上 <em class="parameter"><code>r</code></em>。
        若左下座標增大至超過對應的右上座標（此情況僅會在 <em class="parameter"><code>r</code></em> &lt; 0 時發生），
        兩個座標都設為其平均值。若 <em class="parameter"><code>n</code></em> 大於已定義維度數，且正在
        擴大 cube（<em class="parameter"><code>r</code></em> &gt; 0），則會新增維度使總數成為
        <em class="parameter"><code>n</code></em>；額外座標的初始值為 0。此函式可用於建立點周圍的
        邊界方框，以搜尋鄰近點。
       </p>
<p>
<code class="literal">cube_enlarge('(1,2),(3,4)', 0.5, 3)</code>
        → <code class="returnvalue">(0.5, 1.5, -0.5),(3.5, 4.5, 0.5)</code>
</p></td></tr></tbody></table>

<br>

[返回 F.10. cube — 多維 cube 資料型別](../cube.md#cube)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/cube.html)
