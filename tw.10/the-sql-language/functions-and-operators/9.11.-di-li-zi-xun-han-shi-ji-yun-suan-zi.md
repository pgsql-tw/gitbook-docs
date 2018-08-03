# 9.11. 地理資訊函式及運算子

The geometric types`point`,`box`,`lseg`,`line`,`path`,`polygon`, and`circle`have a large set of native support functions and operators, shown in[Table 9.33](https://www.postgresql.org/docs/10/static/functions-geometry.html#functions-geometry-op-table),[Table 9.34](https://www.postgresql.org/docs/10/static/functions-geometry.html#functions-geometry-func-table), and[Table 9.35](https://www.postgresql.org/docs/10/static/functions-geometry.html#functions-geometry-conv-table).

## Caution

Note that the“same as”operator,`~=`, represents the usual notion of equality for the`point`,`box`,`polygon`, and`circle`types. Some of these types also have an`=`operator, but`=`compares for equal\_areas\_only. The other scalar comparison operators \(`<=`and so on\) likewise compare areas for these types.

**Table 9.33. Geometric Operators**

| Operator | Description | Example |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `+` | Translation | `box '((0,0),(1,1))' + point '(2.0,0)'` |  |  |  |  |
| `-` | Translation | `box '((0,0),(1,1))' - point '(2.0,0)'` |  |  |  |  |
| `*` | Scaling/rotation | `box '((0,0),(1,1))' * point '(2.0,0)'` |  |  |  |  |
| `/` | Scaling/rotation | `box '((0,0),(2,2))' / point '(2.0,0)'` |  |  |  |  |
| `#` | Point or box of intersection | `box '((1,-1),(-1,1))' # box '((1,1),(-2,-2))'` |  |  |  |  |
| `#` | Number of points in path or polygon | `# path '((1,0),(0,1),(-1,0))'` |  |  |  |  |
| `@-@` | Length or circumference | `@-@ path '((0,0),(1,0))'` |  |  |  |  |
| `@@` | Center | `@@ circle '((0,0),10)'` |  |  |  |  |
| `##` | Closest point to first operand on second operand | `point '(0,0)' ## lseg '((2,0),(0,2))'` |  |  |  |  |
| `<->` | Distance between | `circle '((0,0),1)' <-> circle '((5,0),1)'` |  |  |  |  |
| `&&` | Overlaps? \(One point in common makes this true.\) | `box '((0,0),(1,1))' && box '((0,0),(2,2))'` |  |  |  |  |
| `<<` | Is strictly left of? | `circle '((0,0),1)' << circle '((5,0),1)'` |  |  |  |  |
| `>>` | Is strictly right of? | `circle '((5,0),1)' >> circle '((0,0),1)'` |  |  |  |  |
| `&<` | Does not extend to the right of? | `box '((0,0),(1,1))' &< box '((0,0),(2,2))'` |  |  |  |  |
| `&>` | Does not extend to the left of? | `box '((0,0),(3,3))' &> box '((0,0),(2,2))'` |  |  |  |  |
| \`&lt;&lt; | \` | Is strictly below? | \`box '\(\(0,0\),\(3,3\)\)' &lt;&lt; | box '\(\(3,4\),\(5,5\)\)'\` |  |  |
| \` | &gt;&gt;\` | Is strictly above? | \`box '\(\(3,4\),\(5,5\)\)' | &gt;&gt; box '\(\(0,0\),\(3,3\)\)'\` |  |  |
| \`&&lt; | \` | Does not extend above? | \`box '\(\(0,0\),\(1,1\)\)' &&lt; | box '\(\(0,0\),\(2,2\)\)'\` |  |  |
| \` | &&gt;\` | Does not extend below? | \`box '\(\(0,0\),\(3,3\)\)' | &&gt; box '\(\(0,0\),\(2,2\)\)'\` |  |  |
| `<^` | Is below \(allows touching\)? | `circle '((0,0),1)' <^ circle '((0,5),1)'` |  |  |  |  |
| `>^` | Is above \(allows touching\)? | `circle '((0,5),1)' >^ circle '((0,0),1)'` |  |  |  |  |
| `?#` | Intersects? | `lseg '((-1,0),(1,0))' ?# box '((-2,-2),(2,2))'` |  |  |  |  |
| `?-` | Is horizontal? | `?- lseg '((-1,0),(1,0))'` |  |  |  |  |
| `?-` | Are horizontally aligned? | `point '(1,0)' ?- point '(0,0)'` |  |  |  |  |
| \`? | \` | Is vertical? | \`? | lseg '\(\(-1,0\),\(1,0\)\)'\` |  |  |
| \`? | \` | Are vertically aligned? | \`point '\(0,1\)' ? | point '\(0,0\)'\` |  |  |
| \`?- | \` | Is perpendicular? | \`lseg '\(\(0,0\),\(0,1\)\)' ?- | lseg '\(\(0,0\),\(1,0\)\)'\` |  |  |
| \`? |  | \` | Are parallel? | \`lseg '\(\(-1,0\),\(1,0\)\)' ? |  | lseg '\(\(-1,2\),\(1,2\)\)'\` |
| `@>` | Contains? | `circle '((0,0),2)' @> point '(1,1)'` |  |  |  |  |
| `<@` | Contained in or on? | `point '(1,1)' <@ circle '((0,0),2)'` |  |  |  |  |
| `~=` | Same as? | `polygon '((0,0),(1,1))' ~= polygon '((1,1),(0,0))'` |  |  |  |  |

## Note

BeforePostgreSQL8.2, the containment operators`@>`and`<@`were respectively called`~`and`@`. These names are still available, but are deprecated and will eventually be removed.

**Table 9.34. Geometric Functions**

| Function | Return Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `area(object`\) | `double precision` | area | `area(box '((0,0),(1,1))')` |
| `center(object`\) | `point` | center | `center(box '((0,0),(1,2))')` |
| `diameter(circle`\) | `double precision` | diameter of circle | `diameter(circle '((0,0),2.0)')` |
| `height(box`\) | `double precision` | vertical size of box | `height(box '((0,0),(1,1))')` |
| `isclosed(path`\) | `boolean` | a closed path? | `isclosed(path '((0,0),(1,1),(2,0))')` |
| `isopen(path`\) | `boolean` | an open path? | `isopen(path '[(0,0),(1,1),(2,0)]')` |
| `length(object`\) | `double precision` | length | `length(path '((-1,0),(1,0))')` |
| `npoints(path`\) | `int` | number of points | `npoints(path '[(0,0),(1,1),(2,0)]')` |
| `npoints(polygon`\) | `int` | number of points | `npoints(polygon '((1,1),(0,0))')` |
| `pclose(path`\) | `path` | convert path to closed | `pclose(path '[(0,0),(1,1),(2,0)]')` |
| `popen(path`\) | `path` | convert path to open | `popen(path '((0,0),(1,1),(2,0))')` |
| `radius(circle`\) | `double precision` | radius of circle | `radius(circle '((0,0),2.0)')` |
| `width(box`\) | `double precision` | horizontal size of box | `width(box '((0,0),(1,1))')` |

**Table 9.35. Geometric Type Conversion Functions**

| Function | Return Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `box(circle`\) | `box` | circle to box | `box(circle '((0,0),2.0)')` |
| `box(point`\) | `box` | point to empty box | `box(point '(0,0)')` |
| `box(point`,`point`\) | `box` | points to box | `box(point '(0,0)', point '(1,1)')` |
| `box(polygon`\) | `box` | polygon to box | `box(polygon '((0,0),(1,1),(2,0))')` |
| `bound_box(box`,`box`\) | `box` | boxes to bounding box | `bound_box(box '((0,0),(1,1))', box '((3,3),(4,4))')` |
| `circle(box`\) | `circle` | box to circle | `circle(box '((0,0),(1,1))')` |
| `circle(point`,`double precision`\) | `circle` | center and radius to circle | `circle(point '(0,0)', 2.0)` |
| `circle(polygon`\) | `circle` | polygon to circle | `circle(polygon '((0,0),(1,1),(2,0))')` |
| `line(point`,`point`\) | `line` | points to line | `line(point '(-1,0)', point '(1,0)')` |
| `lseg(box`\) | `lseg` | box diagonal to line segment | `lseg(box '((-1,0),(1,0))')` |
| `lseg(point`,`point`\) | `lseg` | points to line segment | `lseg(point '(-1,0)', point '(1,0)')` |
| `path(polygon`\) | `path` | polygon to path | `path(polygon '((0,0),(1,1),(2,0))')` |
| `point`\(`double precision`,`double precision`\) | `point` | construct point | `point(23.4, -44.5)` |
| `point(box`\) | `point` | center of box | `point(box '((-1,0),(1,0))')` |
| `point(circle`\) | `point` | center of circle | `point(circle '((0,0),2.0)')` |
| `point(lseg`\) | `point` | center of line segment | `point(lseg '((-1,0),(1,0))')` |
| `point(polygon`\) | `point` | center of polygon | `point(polygon '((0,0),(1,1),(2,0))')` |
| `polygon(box`\) | `polygon` | box to 4-point polygon | `polygon(box '((0,0),(1,1))')` |
| `polygon(circle`\) | `polygon` | circle to 12-point polygon | `polygon(circle '((0,0),2.0)')` |
| `polygon(npts`,`circle`\) | `polygon` | circle to`npts`-point polygon | `polygon(12, circle '((0,0),2.0)')` |
| `polygon(path`\) | `polygon` | path to polygon | `polygon(path '((0,0),(1,1),(2,0))')` |

It is possible to access the two component numbers of a`point`as though the point were an array with indexes 0 and 1. For example, if`t.p`is a`point`column then`SELECT p[0] FROM t`retrieves the X coordinate and`UPDATE t SET p[1] = ...`changes the Y coordinate. In the same way, a value of type`box`or`lseg`can be treated as an array of two`point`values.

The`area`function works for the types`box`,`circle`, and`path`. The`area`function only works on the`path`data type if the points in the`path`are non-intersecting. For example, the`path'((0,0),(0,1),(2,1),(2,2),(1,2),(1,0),(0,0))'::PATH`will not work; however, the following visually identical`path'((0,0),(0,1),(1,1),(1,2),(2,2),(2,1),(1,1),(1,0),(0,0))'::PATH`will work. If the concept of an intersecting versus non-intersecting`path`is confusing, draw both of the above`path`s side by side on a piece of graph paper.

