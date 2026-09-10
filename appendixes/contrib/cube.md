## F.10. cube — 多維 cube 資料型別 [#](#CUBE)

[F.10.1. 語法](cube.md#CUBE-SYNTAX)

[F.10.2. 精確度](cube.md#CUBE-PRECISION)

[F.10.3. 用法](cube.md#CUBE-USAGE)

[F.10.4. 預設值](cube.md#CUBE-DEFAULTS)

[F.10.5. 注意事項](cube.md#CUBE-NOTES)

[F.10.6. 致謝](cube.md#CUBE-CREDITS)

<a id="id-1.11.7.20.2"></a>

此模組實作 `cube` 資料型別，用來表示多維 cube。

此模組視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非 superuser 也可
安裝它。

<a id="CUBE-SYNTAX"></a>

### F.10.1. 語法 [#](#CUBE-SYNTAX)

[表 F.1](cube.md#CUBE-REPR-TABLE) 顯示 `cube` 型別有效的外部表示法。*`x`*、
*`y`* 等表示浮點數。

<a id="CUBE-REPR-TABLE"></a>

**表 F.1. Cube 外部表示法**

<table border="1" class="table" summary="Cube 外部表示法"><colgroup><col/><col/></colgroup><thead><tr><th>外部語法</th><th>意義</th></tr></thead><tbody><tr><td><code class="literal"><em class="replaceable"><code>x</code></em></code></td><td>一維點
       （或長度為零的一維區間）
      </td></tr><tr><td><code class="literal">(<em class="replaceable"><code>x</code></em>)</code></td><td>同上</td></tr><tr><td><code class="literal"><em class="replaceable"><code>x1</code></em>,<em class="replaceable"><code>x2</code></em>,...,<em class="replaceable"><code>xn</code></em></code></td><td>n 維空間中的點，在內部表示為
      體積為零的 cube
      </td></tr><tr><td><code class="literal">(<em class="replaceable"><code>x1</code></em>,<em class="replaceable"><code>x2</code></em>,...,<em class="replaceable"><code>xn</code></em>)</code></td><td>同上</td></tr><tr><td><code class="literal">(<em class="replaceable"><code>x</code></em>),(<em class="replaceable"><code>y</code></em>)</code></td><td>從 <em class="replaceable"><code>x</code></em> 開始到 <em class="replaceable"><code>y</code></em> 結束的一維區間，或反向亦可；
       順序不重要
      </td></tr><tr><td><code class="literal">[(<em class="replaceable"><code>x</code></em>),(<em class="replaceable"><code>y</code></em>)]</code></td><td>同上</td></tr><tr><td><code class="literal">(<em class="replaceable"><code>x1</code></em>,...,<em class="replaceable"><code>xn</code></em>),(<em class="replaceable"><code>y1</code></em>,...,<em class="replaceable"><code>yn</code></em>)</code></td><td>由一對對角表示的 n 維 cube
      </td></tr><tr><td><code class="literal">[(<em class="replaceable"><code>x1</code></em>,...,<em class="replaceable"><code>xn</code></em>),(<em class="replaceable"><code>y1</code></em>,...,<em class="replaceable"><code>yn</code></em>)]</code></td><td>同上</td></tr></tbody></table>

<br>

輸入 cube 對角的順序不重要。`cube` 函式會在需要時自動交換值，以建立統一的
「左下 — 右上」內部表示法。角點重合時，`cube` 僅儲存一個角點及「is point」
旗標，避免浪費空間。

輸入時會忽略空白，因此 `[(x),(y)]` 與 `[ ( x ), ( y ) ]` 相同。

<a id="CUBE-PRECISION"></a>

### F.10.2. 精確度 [#](#CUBE-PRECISION)

值在內部以 64 位元浮點數儲存。因此，具有超過約 16 位有效數字的數值會被截斷。

<a id="CUBE-USAGE"></a>

### F.10.3. 用法 [#](#CUBE-USAGE)

[表 F.2](cube.md#CUBE-OPERATORS-TABLE) 顯示為 `cube` 型別提供的專用運算子。

<a id="CUBE-OPERATORS-TABLE"></a>

**表 F.2. Cube 運算子**

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

除了上述運算子外，`cube` 型別也可使用[表 9.1](../../the-sql-language/functions/functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE)
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

[表 F.3](cube.md#CUBE-FUNCTIONS-TABLE) 顯示可用函式。

<a id="CUBE-FUNCTIONS-TABLE"></a>

**表 F.3. Cube 函式**

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

<a id="CUBE-DEFAULTS"></a>

### F.10.4. 預設值 [#](#CUBE-DEFAULTS)

下列聯集：

```

select cube_union('(0,5,2),(2,3,1)', '0');
cube_union
-------------------
(0, 0, 0),(2, 5, 2)
(1 row)
```

符合直覺；下列交集也同樣如此：

```

select cube_inter('(0,-1),(1,1)', '(-2),(2)');
cube_inter
-------------
(0, 0),(1, 0)
(1 row)
```

對於維度不同的 cube 執行所有二元運算時，會將維度較低者視為笛卡兒投影，
亦即字串表示法中省略的座標位置為零。以上範例等同於：

```

cube_union('(0,5,2),(2,3,1)','(0,0,0),(0,0,0)');
cube_inter('(0,-1),(1,1)','(-2,0),(2,0)');
```

下列包含述詞使用點的語法，而第二個引數實際上在內部表示為方框。此語法使得
無須為 (box, point) 述詞另行定義點型別與函式。

```

select cube_contains('(0,0),(1,1)', '0.5,0.5');
cube_contains
--------------
t
(1 row)
```

<a id="CUBE-NOTES"></a>

### F.10.5. 注意事項 [#](#CUBE-NOTES)

用法範例請參閱回歸測試 `sql/cube.sql`。

為了降低不慎破壞的可能性，cube 的維度數上限為 100。若需要更大的上限，可在
`cubedata.h` 設定。

<a id="CUBE-CREDITS"></a>

### F.10.6. 致謝 [#](#CUBE-CREDITS)

原作者：Gene Selkov, Jr. `<selkovjr@mcs.anl.gov>`，Argonne National Laboratory
數學與電腦科學部門。

我主要感謝 Joe Hellerstein 教授（<https://dsf.berkeley.edu/jmh/>）闡明 GiST
（<http://gist.cs.berkeley.edu/>）的要旨，以及其前學生 Andy Dong 為 Illustra
撰寫的範例。我也感謝所有現任及過去的 Postgres 開發者，讓我得以創造並安居
於自己的世界。並感謝 Argonne Lab 與 U.S. Department of Energy 多年來對我
資料庫研究的持續支持。

Bruno Wolff III `<bruno@wolff.to>` 在 2002 年 8／9 月對此套件進行小幅更新，
包括將精確度從單精度改為雙精度，並新增一些函式。

Joshua Reich `<josh@root.net>` 在 2006 年 7 月進行額外更新，包括
`cube(float8[], float8[])`，以及清理程式碼以改用 V1 呼叫協定，而非已棄用的
V0 協定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/cube.html)
