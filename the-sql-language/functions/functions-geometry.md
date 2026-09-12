<a id="FUNCTIONS-GEOMETRY"></a>

## 9.11. 幾何函式與運算子 [#](#FUNCTIONS-GEOMETRY)

幾何型別 `point`、`box`、`lseg`、`line`、`path`、`polygon` 與 `circle`，擁有一大組原生支援的函式與運算子，列於[表 9.36](functions-geometry.md#FUNCTIONS-GEOMETRY-OP-TABLE)、[表 9.37](functions-geometry.md#FUNCTIONS-GEOMETRY-FUNC-TABLE) 與[表 9.38](functions-geometry.md#FUNCTIONS-GEOMETRY-CONV-TABLE)。

<a id="FUNCTIONS-GEOMETRY-OP-TABLE"></a>

**表 9.36. 幾何運算子**

<table border="1" class="table" summary="Geometric Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">+</code> <code class="type">point</code>
        → <code class="returnvalue"><em class="replaceable"><code>geometric_type</code></em></code>
</p>
<p>
        將第二個 <code class="type">point</code> 的座標加到第一個引數的每個點上，從而進行平移。適用於 <code class="type">point</code>、<code class="type">box</code>、<code class="type">path</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(1,1),(0,0)' + point '(2,0)'</code>
        → <code class="returnvalue">(3,1),(2,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">path</code> <code class="literal">+</code> <code class="type">path</code>
        → <code class="returnvalue">path</code>
</p>
<p>
        串接兩條開放路徑（如果任一條路徑是封閉的，則回傳 NULL）。
       </p>
<p>
<code class="literal">path '[(0,0),(1,1)]' + path '[(2,2),(3,3),(4,4)]'</code>
        → <code class="returnvalue">[(0,0),(1,1),(2,2),(3,3),(4,4)]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">-</code> <code class="type">point</code>
        → <code class="returnvalue"><em class="replaceable"><code>geometric_type</code></em></code>
</p>
<p>
        從第一個引數的每個點減去第二個 <code class="type">point</code> 的座標，從而進行平移。適用於 <code class="type">point</code>、<code class="type">box</code>、<code class="type">path</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(1,1),(0,0)' - point '(2,0)'</code>
        → <code class="returnvalue">(-1,1),(-2,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">*</code> <code class="type">point</code>
        → <code class="returnvalue"><em class="replaceable"><code>geometric_type</code></em></code>
</p>
<p>
        將第一個引數的每個點乘以第二個 <code class="type">point</code>（將點視為由實部與虛部表示的複數，並進行標準的複數乘法）。如果將第二個 <code class="type">point</code> 解讀為向量，這就等同於將物件的大小以及與原點的距離依向量的長度縮放，並繞原點以該向量與 <em class="replaceable"><code>x</code></em> 軸的夾角逆時針旋轉。適用於 <code class="type">point</code>、<code class="type">box</code>、<a class="footnote" href="#ftn.FUNCTIONS-GEOMETRY-ROTATION-FN"><sup class="footnote" id="FUNCTIONS-GEOMETRY-ROTATION-FN">[a]</sup></a><code class="type">path</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">path '((0,0),(1,0),(1,1))' * point '(3.0,0)'</code>
        → <code class="returnvalue">((0,0),(3,0),(3,3))</code>
</p>
<p>
<code class="literal">path '((0,0),(1,0),(1,1))' * point(cosd(45), sind(45))</code>
        → <code class="returnvalue">((0,0),​(0.7071067811865475,0.7071067811865475),​(0,1.414213562373095))</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">/</code> <code class="type">point</code>
        → <code class="returnvalue"><em class="replaceable"><code>geometric_type</code></em></code>
</p>
<p>
        將第一個引數的每個點除以第二個 <code class="type">point</code>（將點視為由實部與虛部表示的複數，並進行標準的複數除法）。如果將第二個 <code class="type">point</code> 解讀為向量，這就等同於將物件的大小以及與原點的距離依向量的長度縮小，並繞原點以該向量與 <em class="replaceable"><code>x</code></em> 軸的夾角順時針旋轉。適用於 <code class="type">point</code>、<code class="type">box</code>、<a class="footnoteref" href="functions-geometry.md#ftn.FUNCTIONS-GEOMETRY-ROTATION-FN"><sup class="footnoteref">[a]</sup></a> <code class="type">path</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">path '((0,0),(1,0),(1,1))' / point '(2.0,0)'</code>
        → <code class="returnvalue">((0,0),(0.5,0),(0.5,0.5))</code>
</p>
<p>
<code class="literal">path '((0,0),(1,0),(1,1))' / point(cosd(45), sind(45))</code>
        → <code class="returnvalue">((0,0),​(0.7071067811865476,-0.7071067811865476),​(1.4142135623730951,0))</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">@-@</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算總長度。適用於 <code class="type">lseg</code>、<code class="type">path</code>。
       </p>
<p>
<code class="literal">@-@ path '[(0,0),(1,0),(1,1)]'</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">@@</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">point</code>
</p>
<p>
        計算中心點。適用於 <code class="type">box</code>、<code class="type">lseg</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">@@ box '(2,2),(0,0)'</code>
        → <code class="returnvalue">(1,1)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">#</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳點的數量。適用於 <code class="type">path</code>、<code class="type">polygon</code>。
       </p>
<p>
<code class="literal"># path '((1,0),(0,1),(-1,0))'</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">#</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">point</code>
</p>
<p>
        計算交點；如果沒有交點則回傳 NULL。適用於 <code class="type">lseg</code>、<code class="type">line</code>。
       </p>
<p>
<code class="literal">lseg '[(0,0),(1,1)]' # lseg '[(1,0),(0,1)]'</code>
        → <code class="returnvalue">(0.5,0.5)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">box</code> <code class="literal">#</code> <code class="type">box</code>
        → <code class="returnvalue">box</code>
</p>
<p>
        計算兩個方框的交集；如果沒有交集則回傳 NULL。
       </p>
<p>
<code class="literal">box '(2,2),(-1,-1)' # box '(1,1),(-2,-2)'</code>
        → <code class="returnvalue">(1,1),(-1,-1)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">##</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">point</code>
</p>
<p>
        計算第二個物件上距離第一個物件最近的點。適用於下列型別組合：（<code class="type">point</code>、<code class="type">box</code>）、（<code class="type">point</code>、<code class="type">lseg</code>）、（<code class="type">point</code>、<code class="type">line</code>）、（<code class="type">lseg</code>、<code class="type">box</code>）、（<code class="type">lseg</code>、<code class="type">lseg</code>）、（<code class="type">line</code>、<code class="type">lseg</code>）。
       </p>
<p>
<code class="literal">point '(0,0)' ## lseg '[(2,0),(0,2)]'</code>
        → <code class="returnvalue">(1,1)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&lt;-&gt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算物件之間的距離。適用於全部七種幾何型別、<code class="type">point</code> 與另一種幾何型別的所有組合，以及下列其他型別組合：（<code class="type">box</code>、<code class="type">lseg</code>）、（<code class="type">lseg</code>、<code class="type">line</code>）、（<code class="type">polygon</code>、<code class="type">circle</code>）（以及交換後的情況）。
       </p>
<p>
<code class="literal">circle '&lt;(0,0),1&gt;' &lt;-&gt; circle '&lt;(5,0),1&gt;'</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">@&gt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否包含第二個物件？適用於下列型別組合：（<code class="literal">box</code>、<code class="literal">point</code>）、（<code class="literal">box</code>、<code class="literal">box</code>）、（<code class="literal">path</code>、<code class="literal">point</code>）、（<code class="literal">polygon</code>、<code class="literal">point</code>）、（<code class="literal">polygon</code>、<code class="literal">polygon</code>）、（<code class="literal">circle</code>、<code class="literal">point</code>）、（<code class="literal">circle</code>、<code class="literal">circle</code>）。
       </p>
<p>
<code class="literal">circle '&lt;(0,0),2&gt;' @&gt; point '(1,1)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&lt;@</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否被包含在第二個物件之內或之上？適用於下列型別組合：（<code class="literal">point</code>、<code class="literal">box</code>）、（<code class="literal">point</code>、<code class="literal">lseg</code>）、（<code class="literal">point</code>、<code class="literal">line</code>）、（<code class="literal">point</code>、<code class="literal">path</code>）、（<code class="literal">point</code>、<code class="literal">polygon</code>）、（<code class="literal">point</code>、<code class="literal">circle</code>）、（<code class="literal">box</code>、<code class="literal">box</code>）、（<code class="literal">lseg</code>、<code class="literal">box</code>）、（<code class="literal">lseg</code>、<code class="literal">line</code>）、（<code class="literal">polygon</code>、<code class="literal">polygon</code>）、（<code class="literal">circle</code>、<code class="literal">circle</code>）。
       </p>
<p>
<code class="literal">point '(1,1)' &lt;@ circle '&lt;(0,0),2&gt;'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&amp;&amp;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        這些物件是否重疊？（只要有一個共同點就為 true。）適用於 <code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(1,1),(0,0)' &amp;&amp; box '(2,2),(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&lt;&lt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否嚴格位於第二個物件的左邊？適用於 <code class="type">point</code>、<code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">circle '&lt;(0,0),1&gt;' &lt;&lt; circle '&lt;(5,0),1&gt;'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&gt;&gt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否嚴格位於第二個物件的右邊？適用於 <code class="type">point</code>、<code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">circle '&lt;(5,0),1&gt;' &gt;&gt; circle '&lt;(0,0),1&gt;'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&amp;&lt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否沒有延伸到第二個物件的右邊？適用於 <code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(1,1),(0,0)' &amp;&lt; box '(2,2),(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&amp;&gt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否沒有延伸到第二個物件的左邊？適用於 <code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(3,3),(0,0)' &amp;&gt; box '(2,2),(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&lt;&lt;|</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否嚴格位於第二個物件的下方？適用於 <code class="type">point</code>、<code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(3,3),(0,0)' &lt;&lt;| box '(5,5),(3,4)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">|&gt;&gt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否嚴格位於第二個物件的上方？適用於 <code class="type">point</code>、<code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(5,5),(3,4)' |&gt;&gt; box '(3,3),(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">&amp;&lt;|</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否沒有延伸到第二個物件的上方？適用於 <code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(1,1),(0,0)' &amp;&lt;| box '(2,2),(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">|&amp;&gt;</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否沒有延伸到第二個物件的下方？適用於 <code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">box '(3,3),(0,0)' |&amp;&gt; box '(2,2),(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">box</code> <code class="literal">&lt;^</code> <code class="type">box</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否位於第二個物件的下方（允許邊緣相接）？
       </p>
<p>
<code class="literal">box '((1,1),(0,0))' &lt;^ box '((2,2),(1,1))'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">box</code> <code class="literal">&gt;^</code> <code class="type">box</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        第一個物件是否位於第二個物件的上方（允許邊緣相接）？
       </p>
<p>
<code class="literal">box '((2,2),(1,1))' &gt;^ box '((1,1),(0,0))'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">?#</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        這些物件是否相交？適用於下列型別組合：（<code class="type">box</code>、<code class="type">box</code>）、（<code class="type">lseg</code>、<code class="type">box</code>）、（<code class="type">lseg</code>、<code class="type">lseg</code>）、（<code class="type">lseg</code>、<code class="type">line</code>）、（<code class="type">line</code>、<code class="type">box</code>）、（<code class="type">line</code>、<code class="type">line</code>）、（<code class="type">path</code>、<code class="type">path</code>）。
       </p>
<p>
<code class="literal">lseg '[(-1,0),(1,0)]' ?# box '(2,2),(-2,-2)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">?-</code> <code class="type">line</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="literal">?-</code> <code class="type">lseg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        直線是否水平？
       </p>
<p>
<code class="literal">?- lseg '[(-1,0),(1,0)]'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">point</code> <code class="literal">?-</code> <code class="type">point</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        這些點是否水平對齊（也就是具有相同的 y 座標）？
       </p>
<p>
<code class="literal">point '(1,0)' ?- point '(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">?|</code> <code class="type">line</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="literal">?|</code> <code class="type">lseg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        直線是否垂直？
       </p>
<p>
<code class="literal">?| lseg '[(-1,0),(1,0)]'</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">point</code> <code class="literal">?|</code> <code class="type">point</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        這些點是否垂直對齊（也就是具有相同的 x 座標）？
       </p>
<p>
<code class="literal">point '(0,1)' ?| point '(0,0)'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">line</code> <code class="literal">?-|</code> <code class="type">line</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lseg</code> <code class="literal">?-|</code> <code class="type">lseg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        直線是否互相垂直？
       </p>
<p>
<code class="literal">lseg '[(0,0),(0,1)]' ?-| lseg '[(0,0),(1,0)]'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">line</code> <code class="literal">?||</code> <code class="type">line</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lseg</code> <code class="literal">?||</code> <code class="type">lseg</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        直線是否互相平行？
       </p>
<p>
<code class="literal">lseg '[(-1,0),(1,0)]' ?|| lseg '[(-1,2),(1,2)]'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>geometric_type</code></em> <code class="literal">~=</code> <em class="replaceable"><code>geometric_type</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        這些物件是否相同？適用於 <code class="type">point</code>、<code class="type">box</code>、<code class="type">polygon</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">polygon '((0,0),(1,1))' ~= polygon '((1,1),(0,0))'</code>
        → <code class="returnvalue">t</code>
</p></td></tr></tbody><tbody class="footnotes"><tr><td colspan="1"><div class="footnote" id="ftn.FUNCTIONS-GEOMETRY-ROTATION-FN"><p><a class="para" href="#FUNCTIONS-GEOMETRY-ROTATION-FN"><sup class="para">[a] </sup></a>以這些運算子<span class="quote">“<span class="quote">旋轉</span>”</span>方框，只會移動它的角點：方框仍然被視為各邊與座標軸平行。因此，方框的大小不會像真正的旋轉那樣保持不變。</p></div></td></tr></tbody></table>

<br>

### 警示

請注意，「相同」運算子 `~=` 代表 `point`、`box`、`polygon` 與 `circle` 型別一般意義上的相等。有些幾何型別也有 `=` 運算子，但 `=` 只比較*面積*是否相等。其他的純量比較運算子（`<=` 等），在這些型別上可用時，同樣是比較面積。

### 注意

在 PostgreSQL 14 之前，點的嚴格位於下方／上方比較運算子 `point` `<<|` `point` 與 `point` `|>>` `point`，分別稱為 `<^` 與 `>^`。這些名稱仍然可用，但已不建議使用，最終將會被移除。

<a id="FUNCTIONS-GEOMETRY-FUNC-TABLE"></a>

**表 9.37. 幾何函式**

<table border="1" class="table" summary="Geometric Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.1.1.1.1"></a>
<code class="function">area</code> ( <em class="replaceable"><code>geometric_type</code></em> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算面積。適用於 <code class="type">box</code>、<code class="type">path</code>、<code class="type">circle</code>。<code class="type">path</code> 輸入必須是封閉的，否則會回傳 NULL。此外，如果 <code class="type">path</code> 自我相交，結果可能沒有意義。
       </p>
<p>
<code class="literal">area(box '(2,2),(0,0)')</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.2.1.1.1"></a>
<code class="function">center</code> ( <em class="replaceable"><code>geometric_type</code></em> )
        → <code class="returnvalue">point</code>
</p>
<p>
        計算中心點。適用於 <code class="type">box</code>、<code class="type">circle</code>。
       </p>
<p>
<code class="literal">center(box '(1,2),(0,0)')</code>
        → <code class="returnvalue">(0.5,1)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.3.1.1.1"></a>
<code class="function">diagonal</code> ( <code class="type">box</code> )
        → <code class="returnvalue">lseg</code>
</p>
<p>
        擷取方框的對角線作為線段（與 <code class="function">lseg(box)</code> 相同）。
       </p>
<p>
<code class="literal">diagonal(box '(1,2),(0,0)')</code>
        → <code class="returnvalue">[(1,2),(0,0)]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.4.1.1.1"></a>
<code class="function">diameter</code> ( <code class="type">circle</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算圓的直徑。
       </p>
<p>
<code class="literal">diameter(circle '&lt;(0,0),2&gt;')</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.5.1.1.1"></a>
<code class="function">height</code> ( <code class="type">box</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算方框的垂直大小。
       </p>
<p>
<code class="literal">height(box '(1,2),(0,0)')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.6.1.1.1"></a>
<code class="function">isclosed</code> ( <code class="type">path</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        路徑是否封閉？
       </p>
<p>
<code class="literal">isclosed(path '((0,0),(1,1),(2,0))')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.7.1.1.1"></a>
<code class="function">isopen</code> ( <code class="type">path</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        路徑是否開放？
       </p>
<p>
<code class="literal">isopen(path '[(0,0),(1,1),(2,0)]')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.8.1.1.1"></a>
<code class="function">length</code> ( <em class="replaceable"><code>geometric_type</code></em> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算總長度。適用於 <code class="type">lseg</code>、<code class="type">path</code>。
       </p>
<p>
<code class="literal">length(path '((-1,0),(1,0))')</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.9.1.1.1"></a>
<code class="function">npoints</code> ( <em class="replaceable"><code>geometric_type</code></em> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳點的數量。適用於 <code class="type">path</code>、<code class="type">polygon</code>。
       </p>
<p>
<code class="literal">npoints(path '[(0,0),(1,1),(2,0)]')</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.10.1.1.1"></a>
<code class="function">pclose</code> ( <code class="type">path</code> )
        → <code class="returnvalue">path</code>
</p>
<p>
        將路徑轉換為封閉形式。
       </p>
<p>
<code class="literal">pclose(path '[(0,0),(1,1),(2,0)]')</code>
        → <code class="returnvalue">((0,0),(1,1),(2,0))</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.11.1.1.1"></a>
<code class="function">popen</code> ( <code class="type">path</code> )
        → <code class="returnvalue">path</code>
</p>
<p>
        將路徑轉換為開放形式。
       </p>
<p>
<code class="literal">popen(path '((0,0),(1,1),(2,0))')</code>
        → <code class="returnvalue">[(0,0),(1,1),(2,0)]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.12.1.1.1"></a>
<code class="function">radius</code> ( <code class="type">circle</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算圓的半徑。
       </p>
<p>
<code class="literal">radius(circle '&lt;(0,0),2&gt;')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.13.1.1.1"></a>
<code class="function">slope</code> ( <code class="type">point</code>, <code class="type">point</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算通過兩點之直線的斜率。
       </p>
<p>
<code class="literal">slope(point '(0,0)', point '(2,1)')</code>
        → <code class="returnvalue">0.5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.6.2.2.14.1.1.1"></a>
<code class="function">width</code> ( <code class="type">box</code> )
        → <code class="returnvalue">double precision</code>
</p>
<p>
        計算方框的水平大小。
       </p>
<p>
<code class="literal">width(box '(1,2),(0,0)')</code>
        → <code class="returnvalue">1</code>
</p></td></tr></tbody></table>

<br><a id="FUNCTIONS-GEOMETRY-CONV-TABLE"></a>

**表 9.38. 幾何型別轉換函式**

<table border="1" class="table" summary="Geometric Type Conversion Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.1.1.1.1"></a>
<code class="function">box</code> ( <code class="type">circle</code> )
        → <code class="returnvalue">box</code>
</p>
<p>
        計算內接於圓的方框。
       </p>
<p>
<code class="literal">box(circle '&lt;(0,0),2&gt;')</code>
        → <code class="returnvalue">(1.414213562373095,1.414213562373095),​(-1.414213562373095,-1.414213562373095)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">box</code> ( <code class="type">point</code> )
        → <code class="returnvalue">box</code>
</p>
<p>
        將點轉換為空的方框。
       </p>
<p>
<code class="literal">box(point '(1,0)')</code>
        → <code class="returnvalue">(1,0),(1,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">box</code> ( <code class="type">point</code>, <code class="type">point</code> )
        → <code class="returnvalue">box</code>
</p>
<p>
        將任意兩個角點轉換為方框。
       </p>
<p>
<code class="literal">box(point '(0,1)', point '(1,0)')</code>
        → <code class="returnvalue">(1,1),(0,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">box</code> ( <code class="type">polygon</code> )
        → <code class="returnvalue">box</code>
</p>
<p>
        計算多邊形的外框。
       </p>
<p>
<code class="literal">box(polygon '((0,0),(1,1),(2,0))')</code>
        → <code class="returnvalue">(2,1),(0,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.5.1.1.1"></a>
<code class="function">bound_box</code> ( <code class="type">box</code>, <code class="type">box</code> )
        → <code class="returnvalue">box</code>
</p>
<p>
        計算兩個方框的外框。
       </p>
<p>
<code class="literal">bound_box(box '(1,1),(0,0)', box '(4,4),(3,3)')</code>
        → <code class="returnvalue">(4,4),(0,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.6.1.1.1"></a>
<code class="function">circle</code> ( <code class="type">box</code> )
        → <code class="returnvalue">circle</code>
</p>
<p>
        計算包圍方框的最小圓。
       </p>
<p>
<code class="literal">circle(box '(1,1),(0,0)')</code>
        → <code class="returnvalue">&lt;(0.5,0.5),0.7071067811865476&gt;</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">circle</code> ( <code class="type">point</code>, <code class="type">double precision</code> )
        → <code class="returnvalue">circle</code>
</p>
<p>
        從圓心與半徑建構圓。
       </p>
<p>
<code class="literal">circle(point '(0,0)', 2.0)</code>
        → <code class="returnvalue">&lt;(0,0),2&gt;</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">circle</code> ( <code class="type">polygon</code> )
        → <code class="returnvalue">circle</code>
</p>
<p>
        將多邊形轉換為圓。圓心是多邊形各點位置的平均值，半徑則是多邊形各點與該圓心之距離的平均值。
       </p>
<p>
<code class="literal">circle(polygon '((0,0),(1,3),(2,0))')</code>
        → <code class="returnvalue">&lt;(1,1),1.6094757082487299&gt;</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.9.1.1.1"></a>
<code class="function">line</code> ( <code class="type">point</code>, <code class="type">point</code> )
        → <code class="returnvalue">line</code>
</p>
<p>
        將兩點轉換為通過它們的直線。
       </p>
<p>
<code class="literal">line(point '(-1,0)', point '(1,0)')</code>
        → <code class="returnvalue">{0,-1,0}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.10.1.1.1"></a>
<code class="function">lseg</code> ( <code class="type">box</code> )
        → <code class="returnvalue">lseg</code>
</p>
<p>
        擷取方框的對角線作為線段。
       </p>
<p>
<code class="literal">lseg(box '(1,0),(-1,0)')</code>
        → <code class="returnvalue">[(1,0),(-1,0)]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">lseg</code> ( <code class="type">point</code>, <code class="type">point</code> )
        → <code class="returnvalue">lseg</code>
</p>
<p>
        從兩個端點建構線段。
       </p>
<p>
<code class="literal">lseg(point '(-1,0)', point '(1,0)')</code>
        → <code class="returnvalue">[(-1,0),(1,0)]</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.12.1.1.1"></a>
<code class="function">path</code> ( <code class="type">polygon</code> )
        → <code class="returnvalue">path</code>
</p>
<p>
        將多邊形轉換為具有相同點清單的封閉路徑。
       </p>
<p>
<code class="literal">path(polygon '((0,0),(1,1),(2,0))')</code>
        → <code class="returnvalue">((0,0),(1,1),(2,0))</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.13.1.1.1"></a>
<code class="function">point</code> ( <code class="type">double precision</code>, <code class="type">double precision</code> )
        → <code class="returnvalue">point</code>
</p>
<p>
        從座標建構點。
       </p>
<p>
<code class="literal">point(23.4, -44.5)</code>
        → <code class="returnvalue">(23.4,-44.5)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">point</code> ( <code class="type">box</code> )
        → <code class="returnvalue">point</code>
</p>
<p>
        計算方框的中心。
       </p>
<p>
<code class="literal">point(box '(1,0),(-1,0)')</code>
        → <code class="returnvalue">(0,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">point</code> ( <code class="type">circle</code> )
        → <code class="returnvalue">point</code>
</p>
<p>
        計算圓的中心。
       </p>
<p>
<code class="literal">point(circle '&lt;(0,0),2&gt;')</code>
        → <code class="returnvalue">(0,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">point</code> ( <code class="type">lseg</code> )
        → <code class="returnvalue">point</code>
</p>
<p>
        計算線段的中心。
       </p>
<p>
<code class="literal">point(lseg '[(-1,0),(1,0)]')</code>
        → <code class="returnvalue">(0,0)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">point</code> ( <code class="type">polygon</code> )
        → <code class="returnvalue">point</code>
</p>
<p>
        計算多邊形的中心（多邊形各點位置的平均值）。
       </p>
<p>
<code class="literal">point(polygon '((0,0),(1,1),(2,0))')</code>
        → <code class="returnvalue">(1,0.3333333333333333)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.17.7.2.2.18.1.1.1"></a>
<code class="function">polygon</code> ( <code class="type">box</code> )
        → <code class="returnvalue">polygon</code>
</p>
<p>
        將方框轉換為 4 點的多邊形。
       </p>
<p>
<code class="literal">polygon(box '(1,1),(0,0)')</code>
        → <code class="returnvalue">((0,0),(0,1),(1,1),(1,0))</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">polygon</code> ( <code class="type">circle</code> )
        → <code class="returnvalue">polygon</code>
</p>
<p>
        將圓轉換為 12 點的多邊形。
       </p>
<p>
<code class="literal">polygon(circle '&lt;(0,0),2&gt;')</code>
        → <code class="returnvalue">((-2,0),​(-1.7320508075688774,0.9999999999999999),​(-1.0000000000000002,1.7320508075688772),​(-1.2246063538223773e-16,2),​(0.9999999999999996,1.7320508075688774),​(1.732050807568877,1.0000000000000007),​(2,2.4492127076447545e-16),​(1.7320508075688776,-0.9999999999999994),​(1.0000000000000009,-1.7320508075688767),​(3.673819061467132e-16,-2),​(-0.9999999999999987,-1.732050807568878),​(-1.7320508075688767,-1.0000000000000009))</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">polygon</code> ( <code class="type">integer</code>, <code class="type">circle</code> )
        → <code class="returnvalue">polygon</code>
</p>
<p>
        將圓轉換為 <em class="replaceable"><code>n</code></em> 點的多邊形。
       </p>
<p>
<code class="literal">polygon(4, circle '&lt;(3,0),1&gt;')</code>
        → <code class="returnvalue">((2,0),​(3,1),​(4,1.2246063538223773e-16),​(3,-1))</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">polygon</code> ( <code class="type">path</code> )
        → <code class="returnvalue">polygon</code>
</p>
<p>
        將封閉路徑轉換為具有相同點清單的多邊形。
       </p>
<p>
<code class="literal">polygon(path '((0,0),(1,1),(2,0))')</code>
        → <code class="returnvalue">((0,0),(1,1),(2,0))</code>
</p></td></tr></tbody></table>

<br>

可以把 `point` 當作索引為 0 與 1 的陣列，來存取它的兩個組成數字。例如，如果 `t.p` 是一個 `point` 欄位，那麼 `SELECT p[0] FROM t` 會取得 X 座標，而 `UPDATE t SET p[1] = ...` 會改變 Y 座標。同樣地，`box` 或 `lseg` 型別的值也可以被視為由兩個 `point` 值組成的陣列。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-geometry.html)（原文版本：18.6；核對日期：2026-09-11）
