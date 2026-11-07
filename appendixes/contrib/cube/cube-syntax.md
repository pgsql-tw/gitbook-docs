# F.10.1. 語法

<a id="CUBE-SYNTAX"></a>

## F.10.1. 語法 [#](#cube-syntax) <a href="#cube-syntax" id="cube-syntax"></a>

[表 F.1](#cube-repr-table) 顯示 `cube` 型別有效的外部表示法。*`x`*、
*`y`* 等表示浮點數。

<a id="CUBE-REPR-TABLE"></a>

### 表 F.1. Cube 外部表示法 [#](#cube-repr-table) <a href="#cube-repr-table" id="cube-repr-table"></a>

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

[返回 F.10. cube — 多維 cube 資料型別](../cube.md#cube)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/cube.html)
