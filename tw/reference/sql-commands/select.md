---
description: 版本：11
---

# SELECT

SELECT, TABLE, WITH — 從資料表或檢視表中檢索資料列

## 語法

```text
[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    [ * | expression [ [ AS ] output_name ] [, ...] ]
    [ FROM from_item [, ...] ]
    [ WHERE condition ]
    [ GROUP BY grouping_element [, ...] ]
    [ HAVING condition ]
    [ WINDOW window_name AS ( window_definition ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
    [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } { ONLY | WITH TIES } ]
    [ FOR { UPDATE | NO KEY UPDATE | SHARE | KEY SHARE } [ OF table_name [, ...] ] [ NOWAIT | SKIP LOCKED ] [...] ]

where from_item can be one of:

    [ ONLY ] table_name [ * ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
                [ TABLESAMPLE sampling_method ( argument [, ...] ) [ REPEATABLE ( seed ) ] ]
    [ LATERAL ] ( select ) [ AS ] alias [ ( column_alias [, ...] ) ]
    with_query_name [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    [ LATERAL ] function_name ( [ argument [, ...] ] )
                [ WITH ORDINALITY ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    [ LATERAL ] function_name ( [ argument [, ...] ] ) [ AS ] alias ( column_definition [, ...] )
    [ LATERAL ] function_name ( [ argument [, ...] ] ) AS ( column_definition [, ...] )
    [ LATERAL ] ROWS FROM( function_name ( [ argument [, ...] ] ) [ AS ( column_definition [, ...] ) ] [, ...] )
                [ WITH ORDINALITY ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    from_item [ NATURAL ] join_type from_item [ ON join_condition | USING ( join_column [, ...] ) ]

and grouping_element can be one of:

    ( )
    expression
    ( expression [, ...] )
    ROLLUP ( { expression | ( expression [, ...] ) } [, ...] )
    CUBE ( { expression | ( expression [, ...] ) } [, ...] )
    GROUPING SETS ( grouping_element [, ...] )

and with_query is:

    with_query_name [ ( column_name [, ...] ) ] AS [ [ NOT ] MATERIALIZED ] ( select | values | insert | update | delete )

TABLE [ ONLY ] table_name [ * ]
```

## 說明

SELECT 從零個或多個資料表中檢索資料列。SELECT 的一般處理如下：

1. 計算 WITH 列表中的所有查詢語句。這有效地製作可以在 FROM 列表中引用的臨時資料表。在 FROM 中多次引用的 WITH 查詢僅會計算一次。（參閱下面的 [WITH 子句](select.md#with-clause)。）
2. FROM 列表中的所有元素都是計算出來的。（FROM 列表中的每個元素可以是一個真實或虛擬的資料表。）如果在 FROM 列表中指定了多個元素，它們將會交叉查詢在一起。 （參閱下面的 [FROM 語句](select.md#from-clause)。）
3. 如果指定了 WHERE 子句，則從會輸出中過濾掉所有不滿足條件的資料列。（參閱下面的 [WHERE 子句](select.md#where-clause)。）
4. 如果使用了 GROUP BY 子句，或者存在彙總函數的呼叫，則將輸出組合成與一個或多個相符合的資料列群組，合併計算彙總函數的結果。如果存在 HAVING 子句，則會刪除不滿足給定條件的群組。（參閱下面的 [GROUP BY 子句](select.md#group-by-clause)和 [HAVING 子句](select.md#having-clause)。）
5. 使用每個選定的資料列或資料列群組的 SELECT 輸出表示式計算實際輸出的資料列。 （參閱下面的 [SELECT List](select.md#select-list)。）
6. SELECT DISTINCT 從結果中刪除重複的資料列。SELECT DISTINCT ON 消除了在所有指定表示式上符合的資料列。SELECT ALL（預設值）將回傳所有的候選資料列，包括重複的資料列。 （參閱下面的 [DISTINCT 子句](select.md#distinct-clause)。）
7. 使用運算子 UNION、INTERSECT 和 EXCEPT，可以組合多個 SELECT 語句的輸出以形成單個結果集合。UNION 運算子回傳一個或兩個結果集合中的所有資料列。 INTERSECT 運算子回傳同時在兩個結果集合中的所有資料列。EXCEPT 運算子回傳第一個結果集合中但不在第二個結果集合中的資料列。在所有三種情況下，除非指定了 ALL，否則將刪除重複的資料列。可以添加 DISTINCT 以明確指定消除重複資料列。請注意，DISTINCT 是此處的預設行為，即使 ALL 是 SELECT 本身的預設行為。 （參閱下面的 [UNION 子句](select.md#union-clause)、[INTERSECT 子句](select.md#intersect-clause)和 [EXCEPT 子句](select.md#except-clause)。）
8. 如果使用了 ORDER BY 子句，則回傳的資料列按指定的順序排序。如果未使用 ORDER BY，則以系統最快産生的順序回傳資料列。（參閱下面的 [ORDER BY 子句](select.md#order-by-clause)。）
9. 如果使用了 LIMIT（或 FETCH FIRST）或 OFFSET 子句，則 SELECT 語句僅回傳結果資料列的子集。（參閱下面的 [LIMIT 子句](select.md#limit-clause)。）
10. 如果使用了 FOR UPDATE、FOR NO KEY UPDATE、FOR SHARE 或 FOR KEY SHARE，則 SELECT 語句將鎖定所選的資料列以防止同時更新。（參閱下面的 [Locking 子句](select.md#the-locking-clause)。）

您必須對 SELECT 指令中使用的每個欄位具有 SELECT 權限。FOR NO KEY UPDATE、FOR UPDATE、FOR SHARE 或 FOR KEY SHARE 的使用也需要 UPDATE 權限（對於如此選擇的每個資料表的至少一個欄位）。

## 子句

### `WITH` 子句

WITH 子句可以讓您指定一個或多個子查詢，這些子查詢可以在主查詢中以名稱引用。子查詢在主查詢的存續時間內有效地充當臨時資料表或檢視表。每個子查詢可以是 SELECT、TABLE、VALUES、INSERT、UPDATE 或 DELETE 語句。在 WITH 中使用資料變更語句（INSERT、UPDATE 或 DELETE）時，通常會包含 RETURNING 子句。它作為 RETURNING 的輸出，而不是語句修改的基礎資料表，它會構成主查詢所讀取的臨時資料表。 如果省略 RETURNING，則仍會執行該語句，但不會產生任何輸出，因此主查詢就不能將其作為資料表所引用。

必須為每個 WITH 查詢指定名稱（不用限定綱要）。選擇性地，可以指定欄位名稱列表；如果省略的話，則從子查詢中推斷欄位名稱。

如果指定了 RECURSIVE，也允許 SELECT 子查詢以名稱引用本身。這樣的子查詢必須具有這樣的形式

```text
non_recursive_term UNION [ ALL | DISTINCT ] recursive_term
```

遞迴自我引用必須出現在 UNION 的右側。每個查詢只允許一次遞迴自我引用。不支援遞迴式的資料變更語句，但您可以在資料變更語句中使用遞迴 SELECT 查詢的結果。相關範例，請參閱[第 7.8 節](../../the-sql-language/queries/with-queries.md)。

RECURSIVE 的另一個作用是不需要對 WITH 查詢進行排序：查詢可以引用列表後面的另一個查詢。（但是，未實作循環引用或相互遞迴。）如果沒有 RECURSIVE，WITH 查詢只能引用相鄰的 WITH，精確來說是 WITH 列表中較早的查詢。

WITH 查詢的一個關鍵屬性是，每次執行主查詢時，它們只會被運算一次，即使主查詢多次引用它們也是如此。特別的是，無論主查詢是讀取所有輸出還是任何輸出，都保證資料變更語句只會執行一次。

主查詢和 WITH 查詢都是（概念上）同時執行的。 這意味著除了透過讀取其 RETURNING 輸出之外，不能從查詢的其他部分看到 WITH 中的資料變更語句的執行結果。如果兩個此類資料變更語句嘗試修改同一筆資料，則無法預想其結果為何。

有關其他資訊，請參閱[第 7.8 節](../../the-sql-language/queries/with-queries.md)。

### `FROM` Clause

FROM子句為SELECT指定一個或多個來源資料表。如果指定了多個來源，則結果是所有來源的 Cartesian product（cross join）。但通常會加上過濾條件（透過 WHERE），將回傳的資料列限制在其中一小部分。

FROM 子句可以包含以下內容：

_`table_name`_

現有資料表或檢視表的名稱（可加上綱要名稱）。如果在資料表名稱之前指定了 ONLY，則僅掃描該資料表。如果未指定 ONLY，則掃描資料表及其所有繼承資料表（如果有的）。 （選擇性）可以在資料表名稱後指定 \* 以明確指示包含繼承資料表。

_`alias`_

提供 FROM 子句中的項目別名。別名用於簡潔或消除自我交叉查詢的模糊性（多次掃描同一個資料表）。提供別名時，它會完全隱藏資料表或函數的實際名稱；例如，給定 FROM foo AS f，SELECT 的其餘部分就必須將此項目稱為 f 而不是 foo。使用別名時，還可以編寫欄位別名列表以提供資料表的一個或多個欄位的替換名稱。

`TABLESAMPLE` _`sampling_method`_ \( _`argument`_ \[, ...\] \) \[ REPEATABLE \( _`seed`_ \) \]

table\_name 之後的 TABLESAMPLE 子句表示應使用指定的 sampling\_method 來檢索該資料表中的子集合。此抽樣將優先於任何其他過濾程序（如 WHERE 子句）。標準的 PostgreSQL 發行版包含兩種抽樣方法，BERNOULLI 和 SYSTEM，其他抽樣方法可以通過延伸功能安裝在資料庫中。

BERNOULLI 和 SYSTEM 抽樣方法都接受一個參數，該參數是要抽樣資料表的一部分，為 0 到 100 之間的百分比。此參數可以是任何實數表示式。（其他採樣方法可以接受更多或不同的參數。）這兩種方法都回傳一個隨機選擇的資料表樣本，該資料表將包含表行的大約指定的百分比。BERNOULLI 方法會掃描整個資料表，並以指定的機率獨立選擇或忽略各個資料列。SYSTEM 方法對具有指定機會被選中的每個磁碟區塊進行區塊級抽樣；回傳每個選定區塊中的所有資料列。當指定小的抽樣百分比時，SYSTEM 方法明顯快於 BERNOULLI 方法，但由於聚類效應，它可能回傳資料表中較不隨機的樣本。

選擇性的參數 REPEATABLE 子句指定用於在抽樣方法中産生隨機數的種子編號或表示式。種子值可以是任何非 null 浮點值。如果資料表沒有更新，則指定相同種子和參數值的兩個查詢將選擇資料表相同樣本。但是不同的種子值通常會產生不同的樣本。如果未設定 REPEATABLE，則由系統産生種子為每個查詢選擇新的隨機樣本。請注意，某些附加的抽樣方法不接受 REPEATABLE，每次使用時都會産生新的樣本。

_`select`_

sub-SELECT 可以出現在 FROM 子句中。就像在一般 SELECT 指令在執行時間時將其輸出建立為臨時資料表一樣。請注意，sub-SELECT 必須使用括號括起來，並且必須為它提供別名。這裡也可以使用 [VALUES](values.md) 指令。

_`with_query_name`_

透過使用其名稱來引用 WITH 查詢，就像查詢名稱是資料表名稱一樣。（事實上，為了主查詢的需要，WITH 查詢會隱藏任何同名的資料表。如果需要的話，也可以加上綱要限定的資料表名稱來引用同名的真實資料表。）別名可以使用，方式與資料表相同。

_`function_name`_

Function calls can appear in the `FROM` clause. \(This is especially useful for functions that return result sets, but any function can be used.\) This acts as though the function's output were created as a temporary table for the duration of this single `SELECT` command. If the function's result type is composite \(including the case of a function with multiple `OUT` parameters\), each attribute becomes a separate column in the implicit table.

When the optional `WITH ORDINALITY` clause is added to the function call, an additional column of type `bigint` will be appended to the function's result column\(s\). This column numbers the rows of the function's result set, starting from 1. By default, this column is named `ordinality`.

An alias can be provided in the same way as for a table. If an alias is written, a column alias list can also be written to provide substitute names for one or more attributes of the function's composite return type, including the ordinality column if present.

Multiple function calls can be combined into a single `FROM`-clause item by surrounding them with `ROWS FROM( ... )`. The output of such an item is the concatenation of the first row from each function, then the second row from each function, etc. If some of the functions produce fewer rows than others, null values are substituted for the missing data, so that the total number of rows returned is always the same as for the function that produced the most rows.

If the function has been defined as returning the `record` data type, then an alias or the key word `AS` must be present, followed by a column definition list in the form `(` _`column_name`_ _`data_type`_ \[, ... \]\). The column definition list must match the actual number and types of columns returned by the function.

When using the `ROWS FROM( ... )` syntax, if one of the functions requires a column definition list, it's preferred to put the column definition list after the function call inside `ROWS FROM( ... )`. A column definition list can be placed after the `ROWS FROM( ... )` construct only if there's just a single function and no `WITH ORDINALITY` clause.

To use `ORDINALITY` together with a column definition list, you must use the `ROWS FROM( ... )` syntax and put the column definition list inside `ROWS FROM( ... )`._`join_type`_

One of

* `[ INNER ] JOIN`
* `LEFT [ OUTER ] JOIN`
* `RIGHT [ OUTER ] JOIN`
* `FULL [ OUTER ] JOIN`
* `CROSS JOIN`

For the `INNER` and `OUTER` join types, a join condition must be specified, namely exactly one of `NATURAL`, `ON` _`join_condition`_, or `USING (`_`join_column`_ \[, ...\]\). See below for the meaning. For `CROSS JOIN`, none of these clauses can appear.

A `JOIN` clause combines two `FROM` items, which for convenience we will refer to as “tables”, though in reality they can be any type of `FROM` item. Use parentheses if necessary to determine the order of nesting. In the absence of parentheses, `JOIN`s nest left-to-right. In any case `JOIN` binds more tightly than the commas separating `FROM`-list items.

`CROSS JOIN` and `INNER JOIN` produce a simple Cartesian product, the same result as you get from listing the two tables at the top level of `FROM`, but restricted by the join condition \(if any\). `CROSS JOIN` is equivalent to `INNER JOIN ON (TRUE)`, that is, no rows are removed by qualification. These join types are just a notational convenience, since they do nothing you couldn't do with plain `FROM` and `WHERE`.

`LEFT OUTER JOIN` returns all rows in the qualified Cartesian product \(i.e., all combined rows that pass its join condition\), plus one copy of each row in the left-hand table for which there was no right-hand row that passed the join condition. This left-hand row is extended to the full width of the joined table by inserting null values for the right-hand columns. Note that only the `JOIN` clause's own condition is considered while deciding which rows have matches. Outer conditions are applied afterwards.

Conversely, `RIGHT OUTER JOIN` returns all the joined rows, plus one row for each unmatched right-hand row \(extended with nulls on the left\). This is just a notational convenience, since you could convert it to a `LEFT OUTER JOIN` by switching the left and right tables.

`FULL OUTER JOIN` returns all the joined rows, plus one row for each unmatched left-hand row \(extended with nulls on the right\), plus one row for each unmatched right-hand row \(extended with nulls on the left\).`ON` _`join_condition`_

_`join_condition`_ is an expression resulting in a value of type `boolean` \(similar to a `WHERE` clause\) that specifies which rows in a join are considered to match.`USING (` _`join_column`_ \[, ...\] \)

A clause of the form `USING ( a, b, ... )` is shorthand for `ON left_table.a = right_table.a AND left_table.b = right_table.b ...`. Also, `USING` implies that only one of each pair of equivalent columns will be included in the join output, not both.`NATURAL`

`NATURAL` is shorthand for a `USING` list that mentions all columns in the two tables that have matching names. If there are no common column names, `NATURAL` is equivalent to `ON TRUE`.`LATERAL`

The `LATERAL` key word can precede a sub-`SELECT` `FROM` item. This allows the sub-`SELECT` to refer to columns of `FROM` items that appear before it in the `FROM` list. \(Without `LATERAL`, each sub-`SELECT` is evaluated independently and so cannot cross-reference any other `FROM` item.\)

`LATERAL` can also precede a function-call `FROM` item, but in this case it is a noise word, because the function expression can refer to earlier `FROM` items in any case.

A `LATERAL` item can appear at top level in the `FROM` list, or within a `JOIN` tree. In the latter case it can also refer to any items that are on the left-hand side of a `JOIN` that it is on the right-hand side of.

When a `FROM` item contains `LATERAL` cross-references, evaluation proceeds as follows: for each row of the `FROM` item providing the cross-referenced column\(s\), or set of rows of multiple `FROM` items providing the columns, the `LATERAL` item is evaluated using that row or row set's values of the columns. The resulting row\(s\) are joined as usual with the rows they were computed from. This is repeated for each row or set of rows from the column source table\(s\).

The column source table\(s\) must be `INNER` or `LEFT` joined to the `LATERAL` item, else there would not be a well-defined set of rows from which to compute each set of rows for the `LATERAL` item. Thus, although a construct such as _`X`_ RIGHT JOIN LATERAL _`Y`_ is syntactically valid, it is not actually allowed for _`Y`_ to reference _`X`_.

#### `WHERE` Clause

The optional `WHERE` clause has the general form

```text
WHERE condition
```

where _`condition`_ is any expression that evaluates to a result of type `boolean`. Any row that does not satisfy this condition will be eliminated from the output. A row satisfies the condition if it returns true when the actual row values are substituted for any variable references.

#### `GROUP BY` Clause

The optional `GROUP BY` clause has the general form

```text
GROUP BY grouping_element [, ...]
```

`GROUP BY` will condense into a single row all selected rows that share the same values for the grouped expressions. An _`expression`_ used inside a _`grouping_element`_ can be an input column name, or the name or ordinal number of an output column \(`SELECT` list item\), or an arbitrary expression formed from input-column values. In case of ambiguity, a `GROUP BY` name will be interpreted as an input-column name rather than an output column name.

If any of `GROUPING SETS`, `ROLLUP` or `CUBE` are present as grouping elements, then the `GROUP BY` clause as a whole defines some number of independent _`grouping sets`_. The effect of this is equivalent to constructing a `UNION ALL` between subqueries with the individual grouping sets as their `GROUP BY` clauses. For further details on the handling of grouping sets see [Section 7.2.4](https://www.postgresql.org/docs/13/queries-table-expressions.html#QUERIES-GROUPING-SETS).

Aggregate functions, if any are used, are computed across all rows making up each group, producing a separate value for each group. \(If there are aggregate functions but no `GROUP BY` clause, the query is treated as having a single group comprising all the selected rows.\) The set of rows fed to each aggregate function can be further filtered by attaching a `FILTER` clause to the aggregate function call; see [Section 4.2.7](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-AGGREGATES) for more information. When a `FILTER` clause is present, only those rows matching it are included in the input to that aggregate function.

When `GROUP BY` is present, or any aggregate functions are present, it is not valid for the `SELECT` list expressions to refer to ungrouped columns except within aggregate functions or when the ungrouped column is functionally dependent on the grouped columns, since there would otherwise be more than one possible value to return for an ungrouped column. A functional dependency exists if the grouped columns \(or a subset thereof\) are the primary key of the table containing the ungrouped column.

Keep in mind that all aggregate functions are evaluated before evaluating any “scalar” expressions in the `HAVING` clause or `SELECT` list. This means that, for example, a `CASE` expression cannot be used to skip evaluation of an aggregate function; see [Section 4.2.14](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-EXPRESS-EVAL).

Currently, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` and `FOR KEY SHARE` cannot be specified with `GROUP BY`.

#### `HAVING` Clause

The optional `HAVING` clause has the general form

```text
HAVING condition
```

where _`condition`_ is the same as specified for the `WHERE` clause.

`HAVING` eliminates group rows that do not satisfy the condition. `HAVING` is different from `WHERE`: `WHERE` filters individual rows before the application of `GROUP BY`, while `HAVING` filters group rows created by `GROUP BY`. Each column referenced in _`condition`_ must unambiguously reference a grouping column, unless the reference appears within an aggregate function or the ungrouped column is functionally dependent on the grouping columns.

The presence of `HAVING` turns a query into a grouped query even if there is no `GROUP BY` clause. This is the same as what happens when the query contains aggregate functions but no `GROUP BY` clause. All the selected rows are considered to form a single group, and the `SELECT` list and `HAVING` clause can only reference table columns from within aggregate functions. Such a query will emit a single row if the `HAVING` condition is true, zero rows if it is not true.

Currently, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` and `FOR KEY SHARE` cannot be specified with `HAVING`.

#### `WINDOW` Clause

The optional `WINDOW` clause has the general form

```text
WINDOW window_name AS ( window_definition ) [, ...]
```

where _`window_name`_ is a name that can be referenced from `OVER` clauses or subsequent window definitions, and _`window_definition`_ is

```text
[ existing_window_name ]
[ PARTITION BY expression [, ...] ]
[ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ frame_clause ]
```

If an _`existing_window_name`_ is specified it must refer to an earlier entry in the `WINDOW` list; the new window copies its partitioning clause from that entry, as well as its ordering clause if any. In this case the new window cannot specify its own `PARTITION BY` clause, and it can specify `ORDER BY` only if the copied window does not have one. The new window always uses its own frame clause; the copied window must not specify a frame clause.

The elements of the `PARTITION BY` list are interpreted in much the same fashion as elements of a [`GROUP BY`](https://www.postgresql.org/docs/13/sql-select.html#SQL-GROUPBY) clause, except that they are always simple expressions and never the name or number of an output column. Another difference is that these expressions can contain aggregate function calls, which are not allowed in a regular `GROUP BY` clause. They are allowed here because windowing occurs after grouping and aggregation.

Similarly, the elements of the `ORDER BY` list are interpreted in much the same fashion as elements of a statement-level [`ORDER BY`](https://www.postgresql.org/docs/13/sql-select.html#SQL-ORDERBY) clause, except that the expressions are always taken as simple expressions and never the name or number of an output column.

The optional _`frame_clause`_ defines the _window frame_ for window functions that depend on the frame \(not all do\). The window frame is a set of related rows for each row of the query \(called the _current row_\). The _`frame_clause`_ can be one of

```text
{ RANGE | ROWS | GROUPS } frame_start [ frame_exclusion ]
{ RANGE | ROWS | GROUPS } BETWEEN frame_start AND frame_end [ frame_exclusion ]
```

where _`frame_start`_ and _`frame_end`_ can be one of

```text
UNBOUNDED PRECEDING
offset PRECEDING
CURRENT ROW
offset FOLLOWING
UNBOUNDED FOLLOWING
```

and _`frame_exclusion`_ can be one of

```text
EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```

If _`frame_end`_ is omitted it defaults to `CURRENT ROW`. Restrictions are that _`frame_start`_ cannot be `UNBOUNDED FOLLOWING`, _`frame_end`_ cannot be `UNBOUNDED PRECEDING`, and the _`frame_end`_ choice cannot appear earlier in the above list of _`frame_start`_ and _`frame_end`_ options than the _`frame_start`_ choice does — for example `RANGE BETWEEN CURRENT ROW AND` _`offset`_ PRECEDING is not allowed.

The default framing option is `RANGE UNBOUNDED PRECEDING`, which is the same as `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`; it sets the frame to be all rows from the partition start up through the current row's last _peer_ \(a row that the window's `ORDER BY` clause considers equivalent to the current row; all rows are peers if there is no `ORDER BY`\). In general, `UNBOUNDED PRECEDING` means that the frame starts with the first row of the partition, and similarly `UNBOUNDED FOLLOWING` means that the frame ends with the last row of the partition, regardless of `RANGE`, `ROWS` or `GROUPS` mode. In `ROWS` mode, `CURRENT ROW` means that the frame starts or ends with the current row; but in `RANGE` or `GROUPS` mode it means that the frame starts or ends with the current row's first or last peer in the `ORDER BY` ordering. The _`offset`_ `PRECEDING` and _`offset`_ `FOLLOWING` options vary in meaning depending on the frame mode. In `ROWS` mode, the _`offset`_ is an integer indicating that the frame starts or ends that many rows before or after the current row. In `GROUPS` mode, the _`offset`_ is an integer indicating that the frame starts or ends that many peer groups before or after the current row's peer group, where a _peer group_ is a group of rows that are equivalent according to the window's `ORDER BY` clause. In `RANGE` mode, use of an _`offset`_ option requires that there be exactly one `ORDER BY` column in the window definition. Then the frame contains those rows whose ordering column value is no more than _`offset`_ less than \(for `PRECEDING`\) or more than \(for `FOLLOWING`\) the current row's ordering column value. In these cases the data type of the _`offset`_ expression depends on the data type of the ordering column. For numeric ordering columns it is typically of the same type as the ordering column, but for datetime ordering columns it is an `interval`. In all these cases, the value of the _`offset`_ must be non-null and non-negative. Also, while the _`offset`_ does not have to be a simple constant, it cannot contain variables, aggregate functions, or window functions.

The _`frame_exclusion`_ option allows rows around the current row to be excluded from the frame, even if they would be included according to the frame start and frame end options. `EXCLUDE CURRENT ROW` excludes the current row from the frame. `EXCLUDE GROUP` excludes the current row and its ordering peers from the frame. `EXCLUDE TIES` excludes any peers of the current row from the frame, but not the current row itself. `EXCLUDE NO OTHERS` simply specifies explicitly the default behavior of not excluding the current row or its peers.

Beware that the `ROWS` mode can produce unpredictable results if the `ORDER BY` ordering does not order the rows uniquely. The `RANGE` and `GROUPS` modes are designed to ensure that rows that are peers in the `ORDER BY` ordering are treated alike: all rows of a given peer group will be in the frame or excluded from it.

The purpose of a `WINDOW` clause is to specify the behavior of _window functions_ appearing in the query's [`SELECT` list](https://www.postgresql.org/docs/13/sql-select.html#SQL-SELECT-LIST) or [`ORDER BY`](https://www.postgresql.org/docs/13/sql-select.html#SQL-ORDERBY) clause. These functions can reference the `WINDOW` clause entries by name in their `OVER` clauses. A `WINDOW` clause entry does not have to be referenced anywhere, however; if it is not used in the query it is simply ignored. It is possible to use window functions without any `WINDOW` clause at all, since a window function call can specify its window definition directly in its `OVER` clause. However, the `WINDOW` clause saves typing when the same window definition is needed for more than one window function.

Currently, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` and `FOR KEY SHARE` cannot be specified with `WINDOW`.

Window functions are described in detail in [Section 3.5](https://www.postgresql.org/docs/13/tutorial-window.html), [Section 4.2.8](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS), and [Section 7.2.5](https://www.postgresql.org/docs/13/queries-table-expressions.html#QUERIES-WINDOW).

#### `SELECT` List

The `SELECT` list \(between the key words `SELECT` and `FROM`\) specifies expressions that form the output rows of the `SELECT` statement. The expressions can \(and usually do\) refer to columns computed in the `FROM` clause.

Just as in a table, every output column of a `SELECT` has a name. In a simple `SELECT` this name is just used to label the column for display, but when the `SELECT` is a sub-query of a larger query, the name is seen by the larger query as the column name of the virtual table produced by the sub-query. To specify the name to use for an output column, write `AS` _`output_name`_ after the column's expression. \(You can omit `AS`, but only if the desired output name does not match any PostgreSQL keyword \(see [Appendix C](https://www.postgresql.org/docs/13/sql-keywords-appendix.html)\). For protection against possible future keyword additions, it is recommended that you always either write `AS` or double-quote the output name.\) If you do not specify a column name, a name is chosen automatically by PostgreSQL. If the column's expression is a simple column reference then the chosen name is the same as that column's name. In more complex cases a function or type name may be used, or the system may fall back on a generated name such as `?column?`.

An output column's name can be used to refer to the column's value in `ORDER BY` and `GROUP BY` clauses, but not in the `WHERE` or `HAVING` clauses; there you must write out the expression instead.

Instead of an expression, `*` can be written in the output list as a shorthand for all the columns of the selected rows. Also, you can write _`table_name`_.\* as a shorthand for the columns coming from just that table. In these cases it is not possible to specify new names with `AS`; the output column names will be the same as the table columns' names.

According to the SQL standard, the expressions in the output list should be computed before applying `DISTINCT`, `ORDER BY`, or `LIMIT`. This is obviously necessary when using `DISTINCT`, since otherwise it's not clear what values are being made distinct. However, in many cases it is convenient if output expressions are computed after `ORDER BY` and `LIMIT`; particularly if the output list contains any volatile or expensive functions. With that behavior, the order of function evaluations is more intuitive and there will not be evaluations corresponding to rows that never appear in the output. PostgreSQL will effectively evaluate output expressions after sorting and limiting, so long as those expressions are not referenced in `DISTINCT`, `ORDER BY` or `GROUP BY`. \(As a counterexample, `SELECT f(x) FROM tab ORDER BY 1` clearly must evaluate `f(x)` before sorting.\) Output expressions that contain set-returning functions are effectively evaluated after sorting and before limiting, so that `LIMIT` will act to cut off the output from a set-returning function.

#### Note

PostgreSQL versions before 9.6 did not provide any guarantees about the timing of evaluation of output expressions versus sorting and limiting; it depended on the form of the chosen query plan.

#### `DISTINCT` Clause

If `SELECT DISTINCT` is specified, all duplicate rows are removed from the result set \(one row is kept from each group of duplicates\). `SELECT ALL` specifies the opposite: all rows are kept; that is the default.

`SELECT DISTINCT ON (` _`expression`_ \[, ...\] \) keeps only the first row of each set of rows where the given expressions evaluate to equal. The `DISTINCT ON` expressions are interpreted using the same rules as for `ORDER BY` \(see above\). Note that the “first row” of each set is unpredictable unless `ORDER BY` is used to ensure that the desired row appears first. For example:

```text
SELECT DISTINCT ON (location) location, time, report
    FROM weather_reports
    ORDER BY location, time DESC;
```

retrieves the most recent weather report for each location. But if we had not used `ORDER BY` to force descending order of time values for each location, we'd have gotten a report from an unpredictable time for each location.

The `DISTINCT ON` expression\(s\) must match the leftmost `ORDER BY` expression\(s\). The `ORDER BY` clause will normally contain additional expression\(s\) that determine the desired precedence of rows within each `DISTINCT ON` group.

Currently, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` and `FOR KEY SHARE` cannot be specified with `DISTINCT`.

#### `UNION` Clause

The `UNION` clause has this general form:

```text
select_statement UNION [ ALL | DISTINCT ] select_statement
```

_`select_statement`_ is any `SELECT` statement without an `ORDER BY`, `LIMIT`, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE`, or `FOR KEY SHARE` clause. \(`ORDER BY` and `LIMIT` can be attached to a subexpression if it is enclosed in parentheses. Without parentheses, these clauses will be taken to apply to the result of the `UNION`, not to its right-hand input expression.\)

The `UNION` operator computes the set union of the rows returned by the involved `SELECT` statements. A row is in the set union of two result sets if it appears in at least one of the result sets. The two `SELECT` statements that represent the direct operands of the `UNION` must produce the same number of columns, and corresponding columns must be of compatible data types.

The result of `UNION` does not contain any duplicate rows unless the `ALL` option is specified. `ALL` prevents elimination of duplicates. \(Therefore, `UNION ALL` is usually significantly quicker than `UNION`; use `ALL` when you can.\) `DISTINCT` can be written to explicitly specify the default behavior of eliminating duplicate rows.

Multiple `UNION` operators in the same `SELECT` statement are evaluated left to right, unless otherwise indicated by parentheses.

Currently, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` and `FOR KEY SHARE` cannot be specified either for a `UNION` result or for any input of a `UNION`.

#### `INTERSECT` Clause

The `INTERSECT` clause has this general form:

```text
select_statement INTERSECT [ ALL | DISTINCT ] select_statement
```

_`select_statement`_ is any `SELECT` statement without an `ORDER BY`, `LIMIT`, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE`, or `FOR KEY SHARE` clause.

The `INTERSECT` operator computes the set intersection of the rows returned by the involved `SELECT` statements. A row is in the intersection of two result sets if it appears in both result sets.

The result of `INTERSECT` does not contain any duplicate rows unless the `ALL` option is specified. With `ALL`, a row that has _`m`_ duplicates in the left table and _`n`_ duplicates in the right table will appear min\(_`m`_,_`n`_\) times in the result set. `DISTINCT` can be written to explicitly specify the default behavior of eliminating duplicate rows.

Multiple `INTERSECT` operators in the same `SELECT` statement are evaluated left to right, unless parentheses dictate otherwise. `INTERSECT` binds more tightly than `UNION`. That is, `A UNION B INTERSECT C` will be read as `A UNION (B INTERSECT C)`.

Currently, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` and `FOR KEY SHARE` cannot be specified either for an `INTERSECT` result or for any input of an `INTERSECT`.

#### `EXCEPT` Clause

The `EXCEPT` clause has this general form:

```text
select_statement EXCEPT [ ALL | DISTINCT ] select_statement
```

_`select_statement`_ is any `SELECT` statement without an `ORDER BY`, `LIMIT`, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE`, or `FOR KEY SHARE` clause.

The `EXCEPT` operator computes the set of rows that are in the result of the left `SELECT` statement but not in the result of the right one.

The result of `EXCEPT` does not contain any duplicate rows unless the `ALL` option is specified. With `ALL`, a row that has _`m`_ duplicates in the left table and _`n`_ duplicates in the right table will appear max\(_`m`_-_`n`_,0\) times in the result set. `DISTINCT` can be written to explicitly specify the default behavior of eliminating duplicate rows.

Multiple `EXCEPT` operators in the same `SELECT` statement are evaluated left to right, unless parentheses dictate otherwise. `EXCEPT` binds at the same level as `UNION`.

Currently, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` and `FOR KEY SHARE` cannot be specified either for an `EXCEPT` result or for any input of an `EXCEPT`.

#### `ORDER BY` Clause

The optional `ORDER BY` clause has this general form:

```text
ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...]
```

The `ORDER BY` clause causes the result rows to be sorted according to the specified expression\(s\). If two rows are equal according to the leftmost expression, they are compared according to the next expression and so on. If they are equal according to all specified expressions, they are returned in an implementation-dependent order.

Each _`expression`_ can be the name or ordinal number of an output column \(`SELECT` list item\), or it can be an arbitrary expression formed from input-column values.

The ordinal number refers to the ordinal \(left-to-right\) position of the output column. This feature makes it possible to define an ordering on the basis of a column that does not have a unique name. This is never absolutely necessary because it is always possible to assign a name to an output column using the `AS` clause.

It is also possible to use arbitrary expressions in the `ORDER BY` clause, including columns that do not appear in the `SELECT` output list. Thus the following statement is valid:

```text
SELECT name FROM distributors ORDER BY code;
```

A limitation of this feature is that an `ORDER BY` clause applying to the result of a `UNION`, `INTERSECT`, or `EXCEPT` clause can only specify an output column name or number, not an expression.

If an `ORDER BY` expression is a simple name that matches both an output column name and an input column name, `ORDER BY` will interpret it as the output column name. This is the opposite of the choice that `GROUP BY` will make in the same situation. This inconsistency is made to be compatible with the SQL standard.

Optionally one can add the key word `ASC` \(ascending\) or `DESC` \(descending\) after any expression in the `ORDER BY` clause. If not specified, `ASC` is assumed by default. Alternatively, a specific ordering operator name can be specified in the `USING` clause. An ordering operator must be a less-than or greater-than member of some B-tree operator family. `ASC` is usually equivalent to `USING <` and `DESC` is usually equivalent to `USING >`. \(But the creator of a user-defined data type can define exactly what the default sort ordering is, and it might correspond to operators with other names.\)

If `NULLS LAST` is specified, null values sort after all non-null values; if `NULLS FIRST` is specified, null values sort before all non-null values. If neither is specified, the default behavior is `NULLS LAST` when `ASC` is specified or implied, and `NULLS FIRST` when `DESC` is specified \(thus, the default is to act as though nulls are larger than non-nulls\). When `USING` is specified, the default nulls ordering depends on whether the operator is a less-than or greater-than operator.

Note that ordering options apply only to the expression they follow; for example `ORDER BY x, y DESC` does not mean the same thing as `ORDER BY x DESC, y DESC`.

Character-string data is sorted according to the collation that applies to the column being sorted. That can be overridden at need by including a `COLLATE` clause in the _`expression`_, for example `ORDER BY mycolumn COLLATE "en_US"`. For more information see [Section 4.2.10](https://www.postgresql.org/docs/13/sql-expressions.html#SQL-SYNTAX-COLLATE-EXPRS) and [Section 23.2](https://www.postgresql.org/docs/13/collation.html).

#### `LIMIT` Clause

The `LIMIT` clause consists of two independent sub-clauses:

```text
LIMIT { count | ALL }
OFFSET start
```

The parameter _`count`_ specifies the maximum number of rows to return, while _`start`_ specifies the number of rows to skip before starting to return rows. When both are specified, _`start`_ rows are skipped before starting to count the _`count`_ rows to be returned.

If the _`count`_ expression evaluates to NULL, it is treated as `LIMIT ALL`, i.e., no limit. If _`start`_ evaluates to NULL, it is treated the same as `OFFSET 0`.

SQL:2008 introduced a different syntax to achieve the same result, which PostgreSQL also supports. It is:

```text
OFFSET start { ROW | ROWS }
FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } { ONLY | WITH TIES }
```

In this syntax, the _`start`_ or _`count`_ value is required by the standard to be a literal constant, a parameter, or a variable name; as a PostgreSQL extension, other expressions are allowed, but will generally need to be enclosed in parentheses to avoid ambiguity. If _`count`_ is omitted in a `FETCH` clause, it defaults to 1. The `WITH TIES` option is used to return any additional rows that tie for the last place in the result set according to the `ORDER BY` clause; `ORDER BY` is mandatory in this case. `ROW` and `ROWS` as well as `FIRST` and `NEXT` are noise words that don't influence the effects of these clauses. According to the standard, the `OFFSET` clause must come before the `FETCH` clause if both are present; but PostgreSQL is laxer and allows either order.

When using `LIMIT`, it is a good idea to use an `ORDER BY` clause that constrains the result rows into a unique order. Otherwise you will get an unpredictable subset of the query's rows — you might be asking for the tenth through twentieth rows, but tenth through twentieth in what ordering? You don't know what ordering unless you specify `ORDER BY`.

The query planner takes `LIMIT` into account when generating a query plan, so you are very likely to get different plans \(yielding different row orders\) depending on what you use for `LIMIT` and `OFFSET`. Thus, using different `LIMIT`/`OFFSET` values to select different subsets of a query result _will give inconsistent results_ unless you enforce a predictable result ordering with `ORDER BY`. This is not a bug; it is an inherent consequence of the fact that SQL does not promise to deliver the results of a query in any particular order unless `ORDER BY` is used to constrain the order.

It is even possible for repeated executions of the same `LIMIT` query to return different subsets of the rows of a table, if there is not an `ORDER BY` to enforce selection of a deterministic subset. Again, this is not a bug; determinism of the results is simply not guaranteed in such a case.

#### The Locking Clause

`FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE` and `FOR KEY SHARE` are _locking clauses_; they affect how `SELECT` locks rows as they are obtained from the table.

The locking clause has the general form

```text
FOR lock_strength [ OF table_name [, ...] ] [ NOWAIT | SKIP LOCKED ]
```

where _`lock_strength`_ can be one of

```text
UPDATE
NO KEY UPDATE
SHARE
KEY SHARE
```

For more information on each row-level lock mode, refer to [Section 13.3.2](https://www.postgresql.org/docs/13/explicit-locking.html#LOCKING-ROWS).

To prevent the operation from waiting for other transactions to commit, use either the `NOWAIT` or `SKIP LOCKED` option. With `NOWAIT`, the statement reports an error, rather than waiting, if a selected row cannot be locked immediately. With `SKIP LOCKED`, any selected rows that cannot be immediately locked are skipped. Skipping locked rows provides an inconsistent view of the data, so this is not suitable for general purpose work, but can be used to avoid lock contention with multiple consumers accessing a queue-like table. Note that `NOWAIT` and `SKIP LOCKED` apply only to the row-level lock\(s\) — the required `ROW SHARE` table-level lock is still taken in the ordinary way \(see [Chapter 13](https://www.postgresql.org/docs/13/mvcc.html)\). You can use [LOCK](https://www.postgresql.org/docs/13/sql-lock.html) with the `NOWAIT` option first, if you need to acquire the table-level lock without waiting.

If specific tables are named in a locking clause, then only rows coming from those tables are locked; any other tables used in the `SELECT` are simply read as usual. A locking clause without a table list affects all tables used in the statement. If a locking clause is applied to a view or sub-query, it affects all tables used in the view or sub-query. However, these clauses do not apply to `WITH` queries referenced by the primary query. If you want row locking to occur within a `WITH` query, specify a locking clause within the `WITH` query.

Multiple locking clauses can be written if it is necessary to specify different locking behavior for different tables. If the same table is mentioned \(or implicitly affected\) by more than one locking clause, then it is processed as if it was only specified by the strongest one. Similarly, a table is processed as `NOWAIT` if that is specified in any of the clauses affecting it. Otherwise, it is processed as `SKIP LOCKED` if that is specified in any of the clauses affecting it.

The locking clauses cannot be used in contexts where returned rows cannot be clearly identified with individual table rows; for example they cannot be used with aggregation.

When a locking clause appears at the top level of a `SELECT` query, the rows that are locked are exactly those that are returned by the query; in the case of a join query, the rows locked are those that contribute to returned join rows. In addition, rows that satisfied the query conditions as of the query snapshot will be locked, although they will not be returned if they were updated after the snapshot and no longer satisfy the query conditions. If a `LIMIT` is used, locking stops once enough rows have been returned to satisfy the limit \(but note that rows skipped over by `OFFSET` will get locked\). Similarly, if a locking clause is used in a cursor's query, only rows actually fetched or stepped past by the cursor will be locked.

When a locking clause appears in a sub-`SELECT`, the rows locked are those returned to the outer query by the sub-query. This might involve fewer rows than inspection of the sub-query alone would suggest, since conditions from the outer query might be used to optimize execution of the sub-query. For example,

```text
SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss WHERE col1 = 5;
```

will lock only rows having `col1 = 5`, even though that condition is not textually within the sub-query.

Previous releases failed to preserve a lock which is upgraded by a later savepoint. For example, this code:

```text
BEGIN;
SELECT * FROM mytable WHERE key = 1 FOR UPDATE;
SAVEPOINT s;
UPDATE mytable SET ... WHERE key = 1;
ROLLBACK TO s;
```

would fail to preserve the `FOR UPDATE` lock after the `ROLLBACK TO`. This has been fixed in release 9.3.

#### Caution

It is possible for a `SELECT` command running at the `READ COMMITTED` transaction isolation level and using `ORDER BY` and a locking clause to return rows out of order. This is because `ORDER BY` is applied first. The command sorts the result, but might then block trying to obtain a lock on one or more of the rows. Once the `SELECT` unblocks, some of the ordering column values might have been modified, leading to those rows appearing to be out of order \(though they are in order in terms of the original column values\). This can be worked around at need by placing the `FOR UPDATE/SHARE` clause in a sub-query, for example

```text
SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss ORDER BY column1;
```

Note that this will result in locking all rows of `mytable`, whereas `FOR UPDATE` at the top level would lock only the actually returned rows. This can make for a significant performance difference, particularly if the `ORDER BY` is combined with `LIMIT` or other restrictions. So this technique is recommended only if concurrent updates of the ordering columns are expected and a strictly sorted result is required.

At the `REPEATABLE READ` or `SERIALIZABLE` transaction isolation level this would cause a serialization failure \(with a `SQLSTATE` of `'40001'`\), so there is no possibility of receiving rows out of order under these isolation levels.

#### `TABLE` Command

The command

```text
TABLE name
```

is equivalent to

```text
SELECT * FROM name
```

It can be used as a top-level command or as a space-saving syntax variant in parts of complex queries. Only the `WITH`, `UNION`, `INTERSECT`, `EXCEPT`, `ORDER BY`, `LIMIT`, `OFFSET`, `FETCH` and `FOR` locking clauses can be used with `TABLE`; the `WHERE` clause and any form of aggregation cannot be used.

### Examples

To join the table `films` with the table `distributors`:

```text
SELECT f.title, f.did, d.name, f.date_prod, f.kind
    FROM distributors d, films f
    WHERE f.did = d.did

       title       | did |     name     | date_prod  |   kind
-------------------+-----+--------------+------------+----------
 The Third Man     | 101 | British Lion | 1949-12-23 | Drama
 The African Queen | 101 | British Lion | 1951-08-11 | Romantic
 ...
```

To sum the column `len` of all films and group the results by `kind`:

```text
SELECT kind, sum(len) AS total FROM films GROUP BY kind;

   kind   | total
----------+-------
 Action   | 07:34
 Comedy   | 02:58
 Drama    | 14:28
 Musical  | 06:42
 Romantic | 04:38
```

To sum the column `len` of all films, group the results by `kind` and show those group totals that are less than 5 hours:

```text
SELECT kind, sum(len) AS total
    FROM films
    GROUP BY kind
    HAVING sum(len) < interval '5 hours';

   kind   | total
----------+-------
 Comedy   | 02:58
 Romantic | 04:38
```

The following two examples are identical ways of sorting the individual results according to the contents of the second column \(`name`\):

```text
SELECT * FROM distributors ORDER BY name;
SELECT * FROM distributors ORDER BY 2;

 did |       name
-----+------------------
 109 | 20th Century Fox
 110 | Bavaria Atelier
 101 | British Lion
 107 | Columbia
 102 | Jean Luc Godard
 113 | Luso films
 104 | Mosfilm
 103 | Paramount
 106 | Toho
 105 | United Artists
 111 | Walt Disney
 112 | Warner Bros.
 108 | Westward
```

The next example shows how to obtain the union of the tables `distributors` and `actors`, restricting the results to those that begin with the letter W in each table. Only distinct rows are wanted, so the key word `ALL` is omitted.

```text
distributors:               actors:
 did |     name              id |     name
-----+--------------        ----+----------------
 108 | Westward               1 | Woody Allen
 111 | Walt Disney            2 | Warren Beatty
 112 | Warner Bros.           3 | Walter Matthau
 ...                         ...

SELECT distributors.name
    FROM distributors
    WHERE distributors.name LIKE 'W%'
UNION
SELECT actors.name
    FROM actors
    WHERE actors.name LIKE 'W%';

      name
----------------
 Walt Disney
 Walter Matthau
 Warner Bros.
 Warren Beatty
 Westward
 Woody Allen
```

This example shows how to use a function in the `FROM` clause, both with and without a column definition list:

```text
CREATE FUNCTION distributors(int) RETURNS SETOF distributors AS $$
    SELECT * FROM distributors WHERE did = $1;
$$ LANGUAGE SQL;

SELECT * FROM distributors(111);
 did |    name
-----+-------------
 111 | Walt Disney

CREATE FUNCTION distributors_2(int) RETURNS SETOF record AS $$
    SELECT * FROM distributors WHERE did = $1;
$$ LANGUAGE SQL;

SELECT * FROM distributors_2(111) AS (f1 int, f2 text);
 f1  |     f2
-----+-------------
 111 | Walt Disney
```

Here is an example of a function with an ordinality column added:

```text
SELECT * FROM unnest(ARRAY['a','b','c','d','e','f']) WITH ORDINALITY;
 unnest | ordinality
--------+----------
 a      |        1
 b      |        2
 c      |        3
 d      |        4
 e      |        5
 f      |        6
(6 rows)
```

This example shows how to use a simple `WITH` clause:

```text
WITH t AS (
    SELECT random() as x FROM generate_series(1, 3)
  )
SELECT * FROM t
UNION ALL
SELECT * FROM t

         x          
--------------------
  0.534150459803641
  0.520092216785997
 0.0735620250925422
  0.534150459803641
  0.520092216785997
 0.0735620250925422
```

Notice that the `WITH` query was evaluated only once, so that we got two sets of the same three random values.

This example uses `WITH RECURSIVE` to find all subordinates \(direct or indirect\) of the employee Mary, and their level of indirectness, from a table that shows only direct subordinates:

```text
WITH RECURSIVE employee_recursive(distance, employee_name, manager_name) AS (
    SELECT 1, employee_name, manager_name
    FROM employee
    WHERE manager_name = 'Mary'
  UNION ALL
    SELECT er.distance + 1, e.employee_name, e.manager_name
    FROM employee_recursive er, employee e
    WHERE er.employee_name = e.manager_name
  )
SELECT distance, employee_name FROM employee_recursive;
```

Notice the typical form of recursive queries: an initial condition, followed by `UNION`, followed by the recursive part of the query. Be sure that the recursive part of the query will eventually return no tuples, or else the query will loop indefinitely. \(See [Section 7.8](https://www.postgresql.org/docs/13/queries-with.html) for more examples.\)

This example uses `LATERAL` to apply a set-returning function `get_product_names()` for each row of the `manufacturers` table:

```text
SELECT m.name AS mname, pname
FROM manufacturers m, LATERAL get_product_names(m.id) pname;
```

Manufacturers not currently having any products would not appear in the result, since it is an inner join. If we wished to include the names of such manufacturers in the result, we could do:

```text
SELECT m.name AS mname, pname
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true;
```

### Compatibility

Of course, the `SELECT` statement is compatible with the SQL standard. But there are some extensions and some missing features.

#### Omitted `FROM` Clauses

PostgreSQL allows one to omit the `FROM` clause. It has a straightforward use to compute the results of simple expressions:

```text
SELECT 2+2;

 ?column?
----------
        4
```

Some other SQL databases cannot do this except by introducing a dummy one-row table from which to do the `SELECT`.

Note that if a `FROM` clause is not specified, the query cannot reference any database tables. For example, the following query is invalid:

```text
SELECT distributors.* WHERE distributors.name = 'Westward';
```

PostgreSQL releases prior to 8.1 would accept queries of this form, and add an implicit entry to the query's `FROM` clause for each table referenced by the query. This is no longer allowed.

#### Empty `SELECT` Lists

The list of output expressions after `SELECT` can be empty, producing a zero-column result table. This is not valid syntax according to the SQL standard. PostgreSQL allows it to be consistent with allowing zero-column tables. However, an empty list is not allowed when `DISTINCT` is used.

#### Omitting the `AS` Key Word

In the SQL standard, the optional key word `AS` can be omitted before an output column name whenever the new column name is a valid column name \(that is, not the same as any reserved keyword\). PostgreSQL is slightly more restrictive: `AS` is required if the new column name matches any keyword at all, reserved or not. Recommended practice is to use `AS` or double-quote output column names, to prevent any possible conflict against future keyword additions.

In `FROM` items, both the standard and PostgreSQL allow `AS` to be omitted before an alias that is an unreserved keyword. But this is impractical for output column names, because of syntactic ambiguities.

#### `ONLY` and Inheritance

The SQL standard requires parentheses around the table name when writing `ONLY`, for example `SELECT * FROM ONLY (tab1), ONLY (tab2) WHERE ...`. PostgreSQL considers these parentheses to be optional.

PostgreSQL allows a trailing `*` to be written to explicitly specify the non-`ONLY` behavior of including child tables. The standard does not allow this.

\(These points apply equally to all SQL commands supporting the `ONLY` option.\)

#### `TABLESAMPLE` Clause Restrictions

The `TABLESAMPLE` clause is currently accepted only on regular tables and materialized views. According to the SQL standard it should be possible to apply it to any `FROM` item.

#### Function Calls in `FROM`

PostgreSQL allows a function call to be written directly as a member of the `FROM` list. In the SQL standard it would be necessary to wrap such a function call in a sub-`SELECT`; that is, the syntax `FROM` _`func`_\(...\) _`alias`_ is approximately equivalent to `FROM LATERAL (SELECT` _`func`_\(...\)\) _`alias`_. Note that `LATERAL` is considered to be implicit; this is because the standard requires `LATERAL` semantics for an `UNNEST()` item in `FROM`. PostgreSQL treats `UNNEST()` the same as other set-returning functions.

#### Namespace Available to `GROUP BY` and `ORDER BY`

In the SQL-92 standard, an `ORDER BY` clause can only use output column names or numbers, while a `GROUP BY` clause can only use expressions based on input column names. PostgreSQL extends each of these clauses to allow the other choice as well \(but it uses the standard's interpretation if there is ambiguity\). PostgreSQL also allows both clauses to specify arbitrary expressions. Note that names appearing in an expression will always be taken as input-column names, not as output-column names.

SQL:1999 and later use a slightly different definition which is not entirely upward compatible with SQL-92. In most cases, however, PostgreSQL will interpret an `ORDER BY` or `GROUP BY` expression the same way SQL:1999 does.

#### Functional Dependencies

PostgreSQL recognizes functional dependency \(allowing columns to be omitted from `GROUP BY`\) only when a table's primary key is included in the `GROUP BY` list. The SQL standard specifies additional conditions that should be recognized.

#### `LIMIT` and `OFFSET`

The clauses `LIMIT` and `OFFSET` are PostgreSQL-specific syntax, also used by MySQL. The SQL:2008 standard has introduced the clauses `OFFSET ... FETCH {FIRST|NEXT} ...` for the same functionality, as shown above in [LIMIT Clause](https://www.postgresql.org/docs/13/sql-select.html#SQL-LIMIT). This syntax is also used by IBM DB2. \(Applications written for Oracle frequently use a workaround involving the automatically generated `rownum` column, which is not available in PostgreSQL, to implement the effects of these clauses.\)

#### `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE`, `FOR KEY SHARE`

Although `FOR UPDATE` appears in the SQL standard, the standard allows it only as an option of `DECLARE CURSOR`. PostgreSQL allows it in any `SELECT` query as well as in sub-`SELECT`s, but this is an extension. The `FOR NO KEY UPDATE`, `FOR SHARE` and `FOR KEY SHARE` variants, as well as the `NOWAIT` and `SKIP LOCKED` options, do not appear in the standard.

#### Data-Modifying Statements in `WITH`

PostgreSQL allows `INSERT`, `UPDATE`, and `DELETE` to be used as `WITH` queries. This is not found in the SQL standard.

#### Nonstandard Clauses

`DISTINCT ON ( ... )` is an extension of the SQL standard.

`ROWS FROM( ... )` is an extension of the SQL standard.

The `MATERIALIZED` and `NOT MATERIALIZED` options of `WITH` are extensions of the SQL standard.

