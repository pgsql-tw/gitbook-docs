<a id="DATATYPE-GEOMETRIC"></a>
## 8.8. 幾何型別 [#](#DATATYPE-GEOMETRIC)

[8.8.1. 點](datatype-geometric.md#DATATYPE-GEOMETRIC-POINTS)

[8.8.2. 直線](datatype-geometric.md#DATATYPE-LINE)

[8.8.3. 線段](datatype-geometric.md#DATATYPE-LSEG)

[8.8.4. 方框](datatype-geometric.md#DATATYPE-GEOMETRIC-BOXES)

[8.8.5. 路徑](datatype-geometric.md#DATATYPE-GEOMETRIC-PATHS)

[8.8.6. 多邊形](datatype-geometric.md#DATATYPE-POLYGON)

[8.8.7. 圓形](datatype-geometric.md#DATATYPE-CIRCLE)

幾何資料型別用來表示二維空間
物件。[表 8.20](datatype-geometric.md#DATATYPE-GEO-TABLE) 顯示了 PostgreSQL 中可用的幾何
型別。

<a id="DATATYPE-GEO-TABLE"></a>

**表 8.20. 幾何型別**

<table border="1" class="table" summary="Geometric Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>名稱</th><th>儲存大小</th><th>說明</th><th>表示法</th></tr></thead><tbody><tr><td><code class="type">point</code></td><td>16 位元組</td><td>平面上的點</td><td>(x,y)</td></tr><tr><td><code class="type">line</code></td><td>24 位元組</td><td>無限長直線</td><td>{A,B,C}</td></tr><tr><td><code class="type">lseg</code></td><td>32 位元組</td><td>有限長線段</td><td>[(x1,y1),(x2,y2)]</td></tr><tr><td><code class="type">box</code></td><td>32 位元組</td><td>矩形方框</td><td>(x1,y1),(x2,y2)</td></tr><tr><td><code class="type">path</code></td><td>16+16n 位元組</td><td>封閉路徑（類似多邊形）</td><td>((x1,y1),...)</td></tr><tr><td><code class="type">path</code></td><td>16+16n 位元組</td><td>開放路徑</td><td>[(x1,y1),...]</td></tr><tr><td><code class="type">polygon</code></td><td>40+16n 位元組</td><td>多邊形（類似封閉路徑）</td><td>((x1,y1),...)</td></tr><tr><td><code class="type">circle</code></td><td>24 位元組</td><td>圓形</td><td>&lt;(x,y),r&gt;（圓心與半徑）</td></tr></tbody></table>

<br>

在以上所有型別中，個別座標都是以
`double precision`（`float8`）數字儲存。

有一整套豐富的函式與運算子，可用來執行各種幾何
運算，例如縮放、平移、旋轉，以及判斷相交情形。詳情請見[9.11 節](../functions/functions-geometry.md)。

<a id="DATATYPE-GEOMETRIC-POINTS"></a>

### 8.8.1. 點 [#](#DATATYPE-GEOMETRIC-POINTS)

<a id="id-1.5.7.16.6.2"></a>

點是幾何型別最基本的二維建構單元。`point` 型別的值，可使用下列任一語法指定：

```

( x , y )
  x , y
```

其中 *`x`* 與 *`y`* 分別是以浮點數表示的
座標值。

點在輸出時採用第一種語法。

<a id="DATATYPE-LINE"></a>

### 8.8.2. 直線 [#](#DATATYPE-LINE)

<a id="id-1.5.7.16.7.2"></a>

直線是以線性方程式 *`A`*x + *`B`*y + *`C`* = 0
表示，其中 *`A`* 與 *`B`* 不能同時為零。`line`
型別的值，其輸入與輸出皆採用下列形式：

```

{ A, B, C }
```

或者，輸入時也可以使用下列任一形式：

```

[ ( x1 , y1 ) , ( x2 , y2 ) ]
( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

其中
`(x1,y1)`
與
`(x2,y2)`
是該直線上的兩個相異點。

<a id="DATATYPE-LSEG"></a>

### 8.8.3. 線段 [#](#DATATYPE-LSEG)

<a id="id-1.5.7.16.8.2"></a><a id="id-1.5.7.16.8.3"></a>

線段是以該線段兩端點的座標對來表示。`lseg` 型別的值，可使用下列任一
語法指定：

```

[ ( x1 , y1 ) , ( x2 , y2 ) ]
( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

其中
`(x1,y1)`
與
`(x2,y2)`
是該線段的端點。

線段在輸出時採用第一種語法。

<a id="DATATYPE-GEOMETRIC-BOXES"></a>

### 8.8.4. 方框 [#](#DATATYPE-GEOMETRIC-BOXES)

<a id="id-1.5.7.16.9.2"></a><a id="id-1.5.7.16.9.3"></a>

方框是以該方框兩個對角頂點的座標對來表示。
`box` 型別的值，可使用下列任一
語法指定：

```

( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

其中
`(x1,y1)`
與
`(x2,y2)`
是該方框任意一組對角頂點。

方框在輸出時採用第二種語法。

輸入時可提供任意一組對角頂點，但系統會視需要
重新排列這些值，依序儲存為
右上角與左下角。

<a id="DATATYPE-GEOMETRIC-PATHS"></a>

### 8.8.5. 路徑 [#](#DATATYPE-GEOMETRIC-PATHS)

<a id="id-1.5.7.16.10.2"></a>

路徑是以一連串相連的點來表示。路徑可以是
*開放的*，此時清單中第一個與最後一個點視為不相連；也可以是
*封閉的*，
此時第一個與最後一個點視為相連。

`path` 型別的值，可使用下列任一
語法指定：

```

[ ( x1 , y1 ) , ... , ( xn , yn ) ]
( ( x1 , y1 ) , ... , ( xn , yn ) )
  ( x1 , y1 ) , ... , ( xn , yn )
  ( x1 , y1   , ... ,   xn , yn )
    x1 , y1   , ... ,   xn , yn
```

其中這些點是構成該路徑之線段的端點。方括號（`[]`）表示
開放路徑，而括號（`()`）則表示
封閉路徑。當省略最外層的括號時，如
第三到第五種語法所示，則預設為封閉路徑。

路徑在輸出時，視情況採用第一種或第二種語法。

<a id="DATATYPE-POLYGON"></a>

### 8.8.6. 多邊形 [#](#DATATYPE-POLYGON)

<a id="id-1.5.7.16.11.2"></a>

多邊形是以一系列點（多邊形的頂點）來表示。多邊形與封閉路徑
非常相似；兩者本質上的語意差異在於，多邊形被視為包含其
內部的區域，而路徑則不是。

多邊形與路徑之間一項重要的實作差異在於，多邊形的儲存表示法
包含其最小外接方框。這可加快某些搜尋
運算的速度，不過在建構新的多邊形時，計算外接方框也會增加額外開銷。

`polygon` 型別的值，可使用下列任一
語法指定：

```

( ( x1 , y1 ) , ... , ( xn , yn ) )
  ( x1 , y1 ) , ... , ( xn , yn )
  ( x1 , y1   , ... ,   xn , yn )
    x1 , y1   , ... ,   xn , yn
```

其中這些點是構成該多邊形邊界之線段的端點。

多邊形在輸出時採用第一種語法。

<a id="DATATYPE-CIRCLE"></a>

### 8.8.7. 圓形 [#](#DATATYPE-CIRCLE)

<a id="id-1.5.7.16.12.2"></a>

圓形是以圓心與半徑來表示。
`circle` 型別的值，可使用下列任一
語法指定：

```

< ( x , y ) , r >
( ( x , y ) , r )
  ( x , y ) , r
    x , y   , r
```

其中
`(x,y)`
是圓心，*`r`* 則是該
圓形的半徑。

圓形在輸出時採用第一種語法。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-geometric.html)（原文版本：18.6；核對日期：2026-09-16）
