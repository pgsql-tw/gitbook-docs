## 8.8. Geometric Types [#](#DATATYPE-GEOMETRIC)

[8.8.1. Points](datatype-geometric.md#DATATYPE-GEOMETRIC-POINTS)

[8.8.2. Lines](datatype-geometric.md#DATATYPE-LINE)

[8.8.3. Line Segments](datatype-geometric.md#DATATYPE-LSEG)

[8.8.4. Boxes](datatype-geometric.md#DATATYPE-GEOMETRIC-BOXES)

[8.8.5. Paths](datatype-geometric.md#DATATYPE-GEOMETRIC-PATHS)

[8.8.6. Polygons](datatype-geometric.md#DATATYPE-POLYGON)

[8.8.7. Circles](datatype-geometric.md#DATATYPE-CIRCLE)

Geometric data types represent two-dimensional spatial
objects. [Table 8.20](datatype-geometric.md#DATATYPE-GEO-TABLE) shows the geometric
types available in PostgreSQL.

<a id="DATATYPE-GEO-TABLE"></a>

**Table 8.20. Geometric Types**

<table border="1" class="table" summary="Geometric Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>Name</th><th>Storage Size</th><th>Description</th><th>Representation</th></tr></thead><tbody><tr><td><code class="type">point</code></td><td>16 bytes</td><td>Point on a plane</td><td>(x,y)</td></tr><tr><td><code class="type">line</code></td><td>24 bytes</td><td>Infinite line</td><td>{A,B,C}</td></tr><tr><td><code class="type">lseg</code></td><td>32 bytes</td><td>Finite line segment</td><td>[(x1,y1),(x2,y2)]</td></tr><tr><td><code class="type">box</code></td><td>32 bytes</td><td>Rectangular box</td><td>(x1,y1),(x2,y2)</td></tr><tr><td><code class="type">path</code></td><td>16+16n bytes</td><td>Closed path (similar to polygon)</td><td>((x1,y1),...)</td></tr><tr><td><code class="type">path</code></td><td>16+16n bytes</td><td>Open path</td><td>[(x1,y1),...]</td></tr><tr><td><code class="type">polygon</code></td><td>40+16n bytes</td><td>Polygon (similar to closed path)</td><td>((x1,y1),...)</td></tr><tr><td><code class="type">circle</code></td><td>24 bytes</td><td>Circle</td><td>&lt;(x,y),r&gt; (center point and radius)</td></tr></tbody></table>

<br>

In all these types, the individual coordinates are stored as
`double precision` (`float8`) numbers.

A rich set of functions and operators is available to perform various geometric
operations such as scaling, translation, rotation, and determining
intersections. They are explained in [Section 9.11](../functions/functions-geometry.md).

<a id="DATATYPE-GEOMETRIC-POINTS"></a>

### 8.8.1. Points [#](#DATATYPE-GEOMETRIC-POINTS)

<a id="id-1.5.7.16.6.2"></a>

Points are the fundamental two-dimensional building block for geometric
types. Values of type `point` are specified using either of
the following syntaxes:

```

( x , y )
  x , y
```

where *`x`* and *`y`* are the respective
coordinates, as floating-point numbers.

Points are output using the first syntax.

<a id="DATATYPE-LINE"></a>

### 8.8.2. Lines [#](#DATATYPE-LINE)

<a id="id-1.5.7.16.7.2"></a>

Lines are represented by the linear
equation *`A`*x + *`B`*y + *`C`* = 0,
where *`A`* and *`B`* are not both zero. Values
of type `line` are input and output in the following form:

```

{ A, B, C }
```

Alternatively, any of the following forms can be used for input:

```

[ ( x1 , y1 ) , ( x2 , y2 ) ]
( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

where
`(x1,y1)`
and
`(x2,y2)`
are two different points on the line.

<a id="DATATYPE-LSEG"></a>

### 8.8.3. Line Segments [#](#DATATYPE-LSEG)

<a id="id-1.5.7.16.8.2"></a><a id="id-1.5.7.16.8.3"></a>

Line segments are represented by pairs of points that are the endpoints
of the segment. Values of type `lseg` are specified using any
of the following syntaxes:

```

[ ( x1 , y1 ) , ( x2 , y2 ) ]
( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

where
`(x1,y1)`
and
`(x2,y2)`
are the end points of the line segment.

Line segments are output using the first syntax.

<a id="DATATYPE-GEOMETRIC-BOXES"></a>

### 8.8.4. Boxes [#](#DATATYPE-GEOMETRIC-BOXES)

<a id="id-1.5.7.16.9.2"></a><a id="id-1.5.7.16.9.3"></a>

Boxes are represented by pairs of points that are opposite
corners of the box.
Values of type `box` are specified using any of the following
syntaxes:

```

( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

where
`(x1,y1)`
and
`(x2,y2)`
are any two opposite corners of the box.

Boxes are output using the second syntax.

Any two opposite corners can be supplied on input, but the values
will be reordered as needed to store the
upper right and lower left corners, in that order.

<a id="DATATYPE-GEOMETRIC-PATHS"></a>

### 8.8.5. Paths [#](#DATATYPE-GEOMETRIC-PATHS)

<a id="id-1.5.7.16.10.2"></a>

Paths are represented by lists of connected points. Paths can be
*open*, where
the first and last points in the list are considered not connected, or
*closed*,
where the first and last points are considered connected.

Values of type `path` are specified using any of the following
syntaxes:

```

[ ( x1 , y1 ) , ... , ( xn , yn ) ]
( ( x1 , y1 ) , ... , ( xn , yn ) )
  ( x1 , y1 ) , ... , ( xn , yn )
  ( x1 , y1   , ... ,   xn , yn )
    x1 , y1   , ... ,   xn , yn
```

where the points are the end points of the line segments
comprising the path. Square brackets (`[]`) indicate
an open path, while parentheses (`()`) indicate a
closed path. When the outermost parentheses are omitted, as
in the third through fifth syntaxes, a closed path is assumed.

Paths are output using the first or second syntax, as appropriate.

<a id="DATATYPE-POLYGON"></a>

### 8.8.6. Polygons [#](#DATATYPE-POLYGON)

<a id="id-1.5.7.16.11.2"></a>

Polygons are represented by lists of points (the vertices of the
polygon). Polygons are very similar to closed paths; the essential
semantic difference is that a polygon is considered to include the
area within it, while a path is not.

An important implementation difference between polygons and
paths is that the stored representation of a polygon includes its
smallest bounding box. This speeds up certain search operations,
although computing the bounding box adds overhead while constructing
new polygons.

Values of type `polygon` are specified using any of the
following syntaxes:

```

( ( x1 , y1 ) , ... , ( xn , yn ) )
  ( x1 , y1 ) , ... , ( xn , yn )
  ( x1 , y1   , ... ,   xn , yn )
    x1 , y1   , ... ,   xn , yn
```

where the points are the end points of the line segments
comprising the boundary of the polygon.

Polygons are output using the first syntax.

<a id="DATATYPE-CIRCLE"></a>

### 8.8.7. Circles [#](#DATATYPE-CIRCLE)

<a id="id-1.5.7.16.12.2"></a>

Circles are represented by a center point and radius.
Values of type `circle` are specified using any of the
following syntaxes:

```

< ( x , y ) , r >
( ( x , y ) , r )
  ( x , y ) , r
    x , y   , r
```

where
`(x,y)`
is the center point and *`r`* is the radius of the
circle.

Circles are output using the first syntax.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-geometric.html)（英文原文，待翻譯）
