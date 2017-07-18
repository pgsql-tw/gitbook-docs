# 4.2. 參數表示式[^1]

參數表示式用在許多不同的方面，像是 SELECT 指令中的回傳列表；在 INSERT 或 UPDATE 指令中指定欄位的新值；又或是在一些命令中，指出搜尋的條件等。參數表示式的結果，有時候會被稱作 scalar，以有別於表格表示式（就是一個表格）的結果。參數表示式也可以稱作 scalar expressions（賦值表示式），甚或簡化為 expressions （表示式）。表示式的語法容許其值為各種運算的單一結果，如數學、邏輯、集合、或其他運算。

參數表示式可以是下列的其中一種形態：

* 常數或文字內容
* 欄位的引用
* 函數參數的引用，在函數裡或預備指令（prepared statement）中
* 子參數表示式
* 欄位選擇表示式
* 運算子宣告
* 函數呼叫
* 彙總表示式
* 窗函數呼叫
* 型別轉換
* 校對轉換（collation expression）
* 賦值子查詢（scalar subquery）
* 陣列建構式
* 列建構式
* 其他被括號括住的參數表示式（用於群組子表示式和強制調整運算優先權）

除了這個列表之外，還有一些建構式也會應用到表示式，但並沒有特別定義語法規則。一般來說，他們會包含函數或運算子的操作，在[第 9 章](/ii-the-sql-language/functions-and-operators.md)中會有適當的說明。其中有一個例子便是 IS NULL 字句。

我們已經在 [4.1.2 節](/ii-the-sql-language/sql-syntax/41-lexical-structure.md)中討論過常數了，所以接下來就從常數以下的項目繼續說明。

### 4.2.1. 欄位引用

要引要一個欄位的話，請使用下列的形式：

```
correlation.columnname
```

「correlation」（所屬名稱）是其所屬表格的名稱（也可能需要包含結構名），或是表格的別名（在 FROM 子句中所定義的）。所屬名稱和分隔用的句點是可以省略的，如果欄位名稱在目前查詢中的所有表格中是唯一的話。（[參閱第 7 章](/ii-the-sql-language/queries.md)）

### 4.2.2. 函數參數引用

函數參數的引用，用來指定一個不在該 SQL 指令中的值。參數是使用在 SQL 函數定義或預備查詢之中。有一些用戶端函式庫也支援將資料數值與 SQL 指令分離，在這種情境下，參數就會用來指向外部的資料數值。參數引用的形式如下：

```
$number
```

舉個例子，有一個函數 dept 的宣告如下：

```
CREATE FUNCTION dept(text) RETURNS dept
    AS $$ SELECT * FROM dept WHERE name = $1 $$
    LANGUAGE SQL;
```

這裡的 $1 指的是函數被呼叫時的第 1 個輸入參數：

### 4.2.3. 子參數表示式（Subscripts）

如果表示式要產生陣列的結果的話，指定陣列中某個元素，請使用：

```
expression[subscript]
```

或是要取得陣列中多個相隣的元素，請使用：

```
expression[lower_subscript:upper_subscript]
```

每一個「subscript」本身都是一個表示式，必須要產生一個整數值。

一般來說，陣列表示式必須被括號起來，但如果該表示式只是一個欄位或參數的引用的話，那麼括號可以省略。然後，多個子參數表示式可以連在一起使用，當你需要陣列表達多維度的概念時。舉例如下：

```
mytable.arraycolumn[4]
mytable.two_d_column[17][34]
$1[10:42]
(arrayfunction(a,b))[42]
```

在最後一個例子中，括號是必須的。關於陣列，在 [8.15 節](/ii-the-sql-language/data-types/815-arrays.md)有更多說明。

### 4.2.4. Field Selection

If an expression yields a value of a composite type \(row type\), then a specific field of the row can be extracted by writing

```
expression
.
fieldname
```

In general the row\_`expression`\_must be parenthesized, but the parentheses can be omitted when the expression to be selected from is just a table reference or positional parameter. For example:

```
mytable.mycolumn
$1.somecolumn
(rowfunction(a,b)).col3
```

\(Thus, a qualified column reference is actually just a special case of the field selection syntax.\) An important special case is extracting a field from a table column that is of a composite type:

```
(compositecol).somefield
(mytable.compositecol).somefield
```

The parentheses are required here to show that`compositecol`is a column name not a table name, or that`mytable`is a table name not a schema name in the second case.

You can ask for all fields of a composite value by writing`.*`:

```
(compositecol).*
```

This notation behaves differently depending on context; see[Section 8.16.5](https://www.postgresql.org/docs/10/static/rowtypes.html#rowtypes-usage)for details.

### 4.2.5. Operator Invocations

There are three possible syntaxes for an operator invocation:

| `expressionoperatorexpression`\(binary infix operator\) |
| :--- |
| `operatorexpression`\(unary prefix operator\) |
| `expressionoperator`\(unary postfix operator\) |

where the\_`operator`\_token follows the syntax rules of[Section 4.1.3](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-syntax-operators), or is one of the key words`AND`,`OR`, and`NOT`, or is a qualified operator name in the form:

```
OPERATOR(
schema
.
operatorname
)
```

Which particular operators exist and whether they are unary or binary depends on what operators have been defined by the system or the user.[Chapter 9](https://www.postgresql.org/docs/10/static/functions.html)describes the built-in operators.

### 4.2.6. Function Calls

The syntax for a function call is the name of a function \(possibly qualified with a schema name\), followed by its argument list enclosed in parentheses:

```
function_name
 ([
expression
 [
, 
expression
 ... 
]
] )
```

For example, the following computes the square root of 2:

```
sqrt(2)
```

The list of built-in functions is in[Chapter 9](https://www.postgresql.org/docs/10/static/functions.html). Other functions can be added by the user.

The arguments can optionally have names attached. See[Section 4.3](https://www.postgresql.org/docs/10/static/sql-syntax-calling-funcs.html)for details.

### Note

A function that takes a single argument of composite type can optionally be called using field-selection syntax, and conversely field selection can be written in functional style. That is, the notations`col(table)`and`table.col`are interchangeable. This behavior is not SQL-standard but is provided inPostgreSQLbecause it allows use of functions to emulate“computed fields”. For more information see[Section 8.16.5](https://www.postgresql.org/docs/10/static/rowtypes.html#rowtypes-usage).

### 4.2.7. Aggregate Expressions

An\_aggregate expression\_represents the application of an aggregate function across the rows selected by a query. An aggregate function reduces multiple inputs to a single output value, such as the sum or average of the inputs. The syntax of an aggregate expression is one of the following:

```
aggregate_name
 (
expression
 [ , ... ] [ 
order_by_clause
 ] ) [ FILTER ( WHERE 
filter_clause
 ) ]

aggregate_name
 (ALL 
expression
 [ , ... ] [ 
order_by_clause
 ] ) [ FILTER ( WHERE 
filter_clause
 ) ]

aggregate_name
 (DISTINCT 
expression
 [ , ... ] [ 
order_by_clause
 ] ) [ FILTER ( WHERE 
filter_clause
 ) ]

aggregate_name
 ( * ) [ FILTER ( WHERE 
filter_clause
 ) ]

aggregate_name
 ( [ 
expression
 [ , ... ] ] ) WITHIN GROUP ( 
order_by_clause
 ) [ FILTER ( WHERE 
filter_clause
 ) ]
```

where`aggregate_name`_\_is a previously defined aggregate \(possibly qualified with a schema name\) and_`expression`_is any value expression that does not itself contain an aggregate expression or a window function call. The optional_`order_by_clause`_and_`filter_clause`\_are described below.

The first form of aggregate expression invokes the aggregate once for each input row. The second form is the same as the first, since`ALL`is the default. The third form invokes the aggregate once for each distinct value of the expression \(or distinct set of values, for multiple expressions\) found in the input rows. The fourth form invokes the aggregate once for each input row; since no particular input value is specified, it is generally only useful for the`count(*)`aggregate function. The last form is used with\_ordered-set\_aggregate functions, which are described below.

Most aggregate functions ignore null inputs, so that rows in which one or more of the expression\(s\) yield null are discarded. This can be assumed to be true, unless otherwise specified, for all built-in aggregates.

For example,`count(*)`yields the total number of input rows;`count(f1)`yields the number of input rows in which`f1`is non-null, since`count`ignores nulls; and`count(distinct f1)`yields the number of distinct non-null values of`f1`.

Ordinarily, the input rows are fed to the aggregate function in an unspecified order. In many cases this does not matter; for example,`min`produces the same result no matter what order it receives the inputs in. However, some aggregate functions \(such as`array_agg`and`string_agg`\) produce results that depend on the ordering of the input rows. When using such an aggregate, the optional`order_by_clause`_\_can be used to specify the desired ordering. The_`order_by_clause`\_has the same syntax as for a query-level`ORDER BY`clause, as described in[Section 7.5](https://www.postgresql.org/docs/10/static/queries-order.html), except that its expressions are always just expressions and cannot be output-column names or numbers. For example:

```
SELECT array_agg(a ORDER BY b DESC) FROM table;
```

When dealing with multiple-argument aggregate functions, note that the`ORDER BY`clause goes after all the aggregate arguments. For example, write this:

```
SELECT string_agg(a, ',' ORDER BY a) FROM table;
```

not this:

```
SELECT string_agg(a ORDER BY a, ',') FROM table;  -- incorrect
```

The latter is syntactically valid, but it represents a call of a single-argument aggregate function with two`ORDER BY`keys \(the second one being rather useless since it's a constant\).

If`DISTINCT`is specified in addition to an`order_by_clause`, then all the`ORDER BY`expressions must match regular arguments of the aggregate; that is, you cannot sort on an expression that is not included in the`DISTINCT`list.

### Note

The ability to specify both`DISTINCT`and`ORDER BY`in an aggregate function is aPostgreSQLextension.

Placing`ORDER BY`within the aggregate's regular argument list, as described so far, is used when ordering the input rows for general-purpose and statistical aggregates, for which ordering is optional. There is a subclass of aggregate functions called_ordered-set aggregates\_for which an_`order_by_clause`_is\_required_, usually because the aggregate's computation is only sensible in terms of a specific ordering of its input rows. Typical examples of ordered-set aggregates include rank and percentile calculations. For an ordered-set aggregate, the`order_by_clause`_\_is written inside_`WITHIN GROUP (...)`_, as shown in the final syntax alternative above. The expressions in the_`order_by_clause`_are evaluated once per input row just like regular aggregate arguments, sorted as per the_`order_by_clause`_'s requirements, and fed to the aggregate function as input arguments. \(This is unlike the case for a non-_`WITHIN GROUPorder_by_clause`_, which is not treated as argument\(s\) to the aggregate function.\) The argument expressions preceding_`WITHIN GROUP`_, if any, are called\_direct arguments\_to distinguish them from the\_aggregated arguments\_listed in the_`order_by_clause`\_. Unlike regular aggregate arguments, direct arguments are evaluated only once per aggregate call, not once per input row. This means that they can contain variables only if those variables are grouped by`GROUP BY`; this restriction is the same as if the direct arguments were not inside an aggregate expression at all. Direct arguments are typically used for things like percentile fractions, which only make sense as a single value per aggregation calculation. The direct argument list can be empty; in this case, write just`()`not`(*)`. \(PostgreSQLwill actually accept either spelling, but only the first way conforms to the SQL standard.\)

An example of an ordered-set aggregate call is:

```
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY income) FROM households;
 percentile_cont
-----------------
           50489
```

which obtains the 50th percentile, or median, value of the`income`column from table`households`. Here,`0.5`is a direct argument; it would make no sense for the percentile fraction to be a value varying across rows.

If`FILTER`is specified, then only the input rows for which the\_`filter_clause`\_evaluates to true are fed to the aggregate function; other rows are discarded. For example:

```
SELECT
    count(*) AS unfiltered,
    count(*) FILTER (WHERE i 
<
 5) AS filtered
FROM generate_series(1,10) AS s(i);
 unfiltered | filtered
------------+----------
         10 |        4
(1 row)
```

The predefined aggregate functions are described in[Section 9.20](https://www.postgresql.org/docs/10/static/functions-aggregate.html). Other aggregate functions can be added by the user.

An aggregate expression can only appear in the result list or`HAVING`clause of a`SELECT`command. It is forbidden in other clauses, such as`WHERE`, because those clauses are logically evaluated before the results of aggregates are formed.

When an aggregate expression appears in a subquery \(see[Section 4.2.11](https://www.postgresql.org/docs/10/static/sql-expressions.html#sql-syntax-scalar-subqueries)and[Section 9.22](https://www.postgresql.org/docs/10/static/functions-subquery.html)\), the aggregate is normally evaluated over the rows of the subquery. But an exception occurs if the aggregate's arguments \(and\_`filter_clause`\_if any\) contain only outer-level variables: the aggregate then belongs to the nearest such outer level, and is evaluated over the rows of that query. The aggregate expression as a whole is then an outer reference for the subquery it appears in, and acts as a constant over any one evaluation of that subquery. The restriction about appearing only in the result list or`HAVING`clause applies with respect to the query level that the aggregate belongs to.

### 4.2.8. Window Function Calls

A\_window function call\_represents the application of an aggregate-like function over some portion of the rows selected by a query. Unlike non-window aggregate calls, this is not tied to grouping of the selected rows into a single output row — each row remains separate in the query output. However the window function has access to all the rows that would be part of the current row's group according to the grouping specification \(`PARTITION BY`list\) of the window function call. The syntax of a window function call is one of the following:

```
function_name
 ([
expression
 [
, 
expression
 ... 
]
]) [ FILTER ( WHERE 
filter_clause
 ) ] OVER 
window_name
function_name
 ([
expression
 [
, 
expression
 ... 
]
]) [ FILTER ( WHERE 
filter_clause
 ) ] OVER ( 
window_definition
 )

function_name
 ( * ) [ FILTER ( WHERE 
filter_clause
 ) ] OVER 
window_name
function_name
 ( * ) [ FILTER ( WHERE 
filter_clause
 ) ] OVER ( 
window_definition
 )
```

where\_`window_definition`\_has the syntax

```
[ 
existing_window_name
 ]
[ PARTITION BY 
expression
 [, ...] ]
[ ORDER BY 
expression
 [ ASC | DESC | USING 
operator
 ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ 
frame_clause
 ]
```

and the optional\_`frame_clause`\_can be one of

```
{ RANGE | ROWS } 
frame_start

{ RANGE | ROWS } BETWEEN 
frame_start
 AND 
frame_end
```

where`frame_start`_\_and_`frame_end`\_can be one of

```
UNBOUNDED PRECEDING

value
 PRECEDING
CURRENT ROW

value
 FOLLOWING
UNBOUNDED FOLLOWING
```

Here,\_`expression`\_represents any value expression that does not itself contain window function calls.

`window_name`_\_is a reference to a named window specification defined in the query's_`WINDOW`_clause. Alternatively, a full_`window_definition`\_can be given within parentheses, using the same syntax as for defining a named window in the`WINDOW`clause; see the[SELECT](https://www.postgresql.org/docs/10/static/sql-select.html)reference page for details. It's worth pointing out that`OVER wname`is not exactly equivalent to`OVER (wname ...)`; the latter implies copying and modifying the window definition, and will be rejected if the referenced window specification includes a frame clause.

The`PARTITION BY`clause groups the rows of the query into_partitions_, which are processed separately by the window function.`PARTITION BY`works similarly to a query-level`GROUP BY`clause, except that its expressions are always just expressions and cannot be output-column names or numbers. Without`PARTITION BY`, all rows produced by the query are treated as a single partition. The`ORDER BY`clause determines the order in which the rows of a partition are processed by the window function. It works similarly to a query-level`ORDER BY`clause, but likewise cannot use output-column names or numbers. Without`ORDER BY`, rows are processed in an unspecified order.

The`frame_clause`_\_specifies the set of rows constituting the\_window frame_, which is a subset of the current partition, for those window functions that act on the frame instead of the whole partition. The frame can be specified in either`RANGE`or`ROWS`mode; in either case, it runs from the`frame_start`_\_to the_`frame_end`_. If_`frame_end`\_is omitted, it defaults to`CURRENT ROW`.

A`frame_start`_\_of_`UNBOUNDED PRECEDING`_means that the frame starts with the first row of the partition, and similarly a_`frame_end`\_of`UNBOUNDED FOLLOWING`means that the frame ends with the last row of the partition.

In`RANGE`mode, a`frame_start`_\_of_`CURRENT ROW`_means the frame starts with the current row's first\_peer\_row \(a row that_`ORDER BY`_considers equivalent to the current row\), while a_`frame_end`\_of`CURRENT ROW`means the frame ends with the last equivalent`ORDER BY`peer. In`ROWS`mode,`CURRENT ROW`simply means the current row.

The`valuePRECEDING`and`valueFOLLOWING`cases are currently only allowed in`ROWS`mode. They indicate that the frame starts or ends the specified number of rows before or after the current row.\_`value`\_must be an integer expression not containing any variables, aggregate functions, or window functions. The value must not be null or negative; but it can be zero, which just selects the current row.

The default framing option is`RANGE UNBOUNDED PRECEDING`, which is the same as`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. With`ORDER BY`, this sets the frame to be all rows from the partition start up through the current row's last`ORDER BY`peer. Without`ORDER BY`, all rows of the partition are included in the window frame, since all rows become peers of the current row.

Restrictions are that`frame_start`_\_cannot be_`UNBOUNDED FOLLOWING`_,_`frame_end`_cannot be_`UNBOUNDED PRECEDING`_, and the_`frame_end`_choice cannot appear earlier in the above list than the_`frame_start`_choice — for example_`RANGE BETWEEN CURRENT ROW ANDvalue`\_PRECEDINGis not allowed.

If`FILTER`is specified, then only the input rows for which the\_`filter_clause`\_evaluates to true are fed to the window function; other rows are discarded. Only window functions that are aggregates accept a`FILTER`clause.

The built-in window functions are described in[Table 9.57](https://www.postgresql.org/docs/10/static/functions-window.html#functions-window-table). Other window functions can be added by the user. Also, any built-in or user-defined general-purpose or statistical aggregate can be used as a window function. \(Ordered-set and hypothetical-set aggregates cannot presently be used as window functions.\)

The syntaxes using`*`are used for calling parameter-less aggregate functions as window functions, for example`count(*) OVER (PARTITION BY x ORDER BY y)`. The asterisk \(`*`\) is customarily not used for window-specific functions. Window-specific functions do not allow`DISTINCT`or`ORDER BY`to be used within the function argument list.

Window function calls are permitted only in the`SELECT`list and the`ORDER BY`clause of the query.

More information about window functions can be found in[Section 3.5](https://www.postgresql.org/docs/10/static/tutorial-window.html),[Section 9.21](https://www.postgresql.org/docs/10/static/functions-window.html), and[Section 7.2.5](https://www.postgresql.org/docs/10/static/queries-table-expressions.html#queries-window).

### 4.2.9. Type Casts

A type cast specifies a conversion from one data type to another.PostgreSQLaccepts two equivalent syntaxes for type casts:

```
CAST ( 
expression
 AS 
type
 )

expression
::
type
```

The`CAST`syntax conforms to SQL; the syntax with`::`is historicalPostgreSQLusage.

When a cast is applied to a value expression of a known type, it represents a run-time type conversion. The cast will succeed only if a suitable type conversion operation has been defined. Notice that this is subtly different from the use of casts with constants, as shown in[Section 4.1.2.7](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-syntax-constants-generic). A cast applied to an unadorned string literal represents the initial assignment of a type to a literal constant value, and so it will succeed for any type \(if the contents of the string literal are acceptable input syntax for the data type\).

An explicit type cast can usually be omitted if there is no ambiguity as to the type that a value expression must produce \(for example, when it is assigned to a table column\); the system will automatically apply a type cast in such cases. However, automatic casting is only done for casts that are marked“OK to apply implicitly”in the system catalogs. Other casts must be invoked with explicit casting syntax. This restriction is intended to prevent surprising conversions from being applied silently.

It is also possible to specify a type cast using a function-like syntax:

```
typename
 ( 
expression
 )
```

However, this only works for types whose names are also valid as function names. For example,`double precision`cannot be used this way, but the equivalent`float8`can. Also, the names`interval`,`time`, and`timestamp`can only be used in this fashion if they are double-quoted, because of syntactic conflicts. Therefore, the use of the function-like cast syntax leads to inconsistencies and should probably be avoided.

### Note

The function-like syntax is in fact just a function call. When one of the two standard cast syntaxes is used to do a run-time conversion, it will internally invoke a registered function to perform the conversion. By convention, these conversion functions have the same name as their output type, and thus the“function-like syntax”is nothing more than a direct invocation of the underlying conversion function. Obviously, this is not something that a portable application should rely on. For further details see[CREATE CAST](https://www.postgresql.org/docs/10/static/sql-createcast.html).

### 4.2.10. Collation Expressions

The`COLLATE`clause overrides the collation of an expression. It is appended to the expression it applies to:

```
expr
 COLLATE 
collation
```

where\_`collation`\_is a possibly schema-qualified identifier. The`COLLATE`clause binds tighter than operators; parentheses can be used when necessary.

If no collation is explicitly specified, the database system either derives a collation from the columns involved in the expression, or it defaults to the default collation of the database if no column is involved in the expression.

The two common uses of the`COLLATE`clause are overriding the sort order in an`ORDER BY`clause, for example:

```
SELECT a, b, c FROM tbl WHERE ... ORDER BY a COLLATE "C";
```

and overriding the collation of a function or operator call that has locale-sensitive results, for example:

```
SELECT * FROM tbl WHERE a 
>
 'foo' COLLATE "C";
```

Note that in the latter case the`COLLATE`clause is attached to an input argument of the operator we wish to affect. It doesn't matter which argument of the operator or function call the`COLLATE`clause is attached to, because the collation that is applied by the operator or function is derived by considering all arguments, and an explicit`COLLATE`clause will override the collations of all other arguments. \(Attaching non-matching`COLLATE`clauses to more than one argument, however, is an error. For more details see[Section 23.2](https://www.postgresql.org/docs/10/static/collation.html).\) Thus, this gives the same result as the previous example:

```
SELECT * FROM tbl WHERE a COLLATE "C" 
>
 'foo';
```

But this is an error:

```
SELECT * FROM tbl WHERE (a 
>
 'foo') COLLATE "C";
```

because it attempts to apply a collation to the result of the`>`operator, which is of the non-collatable data type`boolean`.

### 4.2.11. Scalar Subqueries

A scalar subquery is an ordinary`SELECT`query in parentheses that returns exactly one row with one column. \(See[Chapter 7](https://www.postgresql.org/docs/10/static/queries.html)for information about writing queries.\) The`SELECT`query is executed and the single returned value is used in the surrounding value expression. It is an error to use a query that returns more than one row or more than one column as a scalar subquery. \(But if, during a particular execution, the subquery returns no rows, there is no error; the scalar result is taken to be null.\) The subquery can refer to variables from the surrounding query, which will act as constants during any one evaluation of the subquery. See also[Section 9.22](https://www.postgresql.org/docs/10/static/functions-subquery.html)for other expressions involving subqueries.

For example, the following finds the largest city population in each state:

```
SELECT name, (SELECT max(pop) FROM cities WHERE cities.state = states.name)
    FROM states;
```

### 4.2.12. Array Constructors

An array constructor is an expression that builds an array value using values for its member elements. A simple array constructor consists of the key word`ARRAY`, a left square bracket`[`, a list of expressions \(separated by commas\) for the array element values, and finally a right square bracket`]`. For example:

```
SELECT ARRAY[1,2,3+4];
  array
---------
 {1,2,7}
(1 row)
```

By default, the array element type is the common type of the member expressions, determined using the same rules as for`UNION`or`CASE`constructs \(see[Section 10.5](https://www.postgresql.org/docs/10/static/typeconv-union-case.html)\). You can override this by explicitly casting the array constructor to the desired type, for example:

```
SELECT ARRAY[1,2,22.7]::integer[];
  array
----------
 {1,2,23}
(1 row)
```

This has the same effect as casting each expression to the array element type individually. For more on casting, see[Section 4.2.9](https://www.postgresql.org/docs/10/static/sql-expressions.html#sql-syntax-type-casts).

Multidimensional array values can be built by nesting array constructors. In the inner constructors, the key word`ARRAY`can be omitted. For example, these produce the same result:

```
SELECT ARRAY[ARRAY[1,2], ARRAY[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)

SELECT ARRAY[[1,2],[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)
```

Since multidimensional arrays must be rectangular, inner constructors at the same level must produce sub-arrays of identical dimensions. Any cast applied to the outer`ARRAY`constructor propagates automatically to all the inner constructors.

Multidimensional array constructor elements can be anything yielding an array of the proper kind, not only a sub-`ARRAY`construct. For example:

```
CREATE TABLE arr(f1 int[], f2 int[]);

INSERT INTO arr VALUES (ARRAY[[1,2],[3,4]], ARRAY[[5,6],[7,8]]);

SELECT ARRAY[f1, f2, '{{9,10},{11,12}}'::int[]] FROM arr;
                     array
------------------------------------------------
 {{{1,2},{3,4}},{{5,6},{7,8}},{{9,10},{11,12}}}
(1 row)
```

You can construct an empty array, but since it's impossible to have an array with no type, you must explicitly cast your empty array to the desired type. For example:

```
SELECT ARRAY[]::integer[];
 array
-------
 {}
(1 row)
```

It is also possible to construct an array from the results of a subquery. In this form, the array constructor is written with the key word`ARRAY`followed by a parenthesized \(not bracketed\) subquery. For example:

```
SELECT ARRAY(SELECT oid FROM pg_proc WHERE proname LIKE 'bytea%');
                                 array
-----------------------------------------------------------------------
 {2011,1954,1948,1952,1951,1244,1950,2005,1949,1953,2006,31,2412,2413}
(1 row)

SELECT ARRAY(SELECT ARRAY[i, i*2] FROM generate_series(1,5) AS a(i));
              array
----------------------------------
 {{1,2},{2,4},{3,6},{4,8},{5,10}}
(1 row)
```

The subquery must return a single column. If the subquery's output column is of a non-array type, the resulting one-dimensional array will have an element for each row in the subquery result, with an element type matching that of the subquery's output column. If the subquery's output column is of an array type, the result will be an array of the same type but one higher dimension; in this case all the subquery rows must yield arrays of identical dimensionality, else the result would not be rectangular.

The subscripts of an array value built with`ARRAY`always begin with one. For more information about arrays, see[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html).

### 4.2.13. Row Constructors

A row constructor is an expression that builds a row value \(also called a composite value\) using values for its member fields. A row constructor consists of the key word`ROW`, a left parenthesis, zero or more expressions \(separated by commas\) for the row field values, and finally a right parenthesis. For example:

```
SELECT ROW(1,2.5,'this is a test');
```

The key word`ROW`is optional when there is more than one expression in the list.

A row constructor can include the syntax`rowvalue.*`, which will be expanded to a list of the elements of the row value, just as occurs when the`.*`syntax is used at the top level of a`SELECT`list \(see[Section 8.16.5](https://www.postgresql.org/docs/10/static/rowtypes.html#rowtypes-usage)\). For example, if table`t`has columns`f1`and`f2`, these are the same:

```
SELECT ROW(t.*, 42) FROM t;
SELECT ROW(t.f1, t.f2, 42) FROM t;
```

### Note

BeforePostgreSQL8.2, the`.*`syntax was not expanded in row constructors, so that writing`ROW(t.*, 42)`created a two-field row whose first field was another row value. The new behavior is usually more useful. If you need the old behavior of nested row values, write the inner row value without`.*`, for instance`ROW(t, 42)`.

By default, the value created by a`ROW`expression is of an anonymous record type. If necessary, it can be cast to a named composite type — either the row type of a table, or a composite type created with`CREATE TYPE AS`. An explicit cast might be needed to avoid ambiguity. For example:

```
CREATE TABLE mytable(f1 int, f2 float, f3 text);

CREATE FUNCTION getf1(mytable) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- No cast needed since only one getf1() exists
SELECT getf1(ROW(1,2.5,'this is a test'));
 getf1
-------
     1
(1 row)

CREATE TYPE myrowtype AS (f1 int, f2 text, f3 numeric);

CREATE FUNCTION getf1(myrowtype) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- Now we need a cast to indicate which function to call:
SELECT getf1(ROW(1,2.5,'this is a test'));
ERROR:  function getf1(record) is not unique

SELECT getf1(ROW(1,2.5,'this is a test')::mytable);
 getf1
-------
     1
(1 row)

SELECT getf1(CAST(ROW(11,'this is a test',2.5) AS myrowtype));
 getf1
-------
    11
(1 row)
```

Row constructors can be used to build composite values to be stored in a composite-type table column, or to be passed to a function that accepts a composite parameter. Also, it is possible to compare two row values or test a row with`IS NULL`or`IS NOT NULL`, for example:

```
SELECT ROW(1,2.5,'this is a test') = ROW(1, 3, 'not the same');

SELECT ROW(table.*) IS NULL FROM table;  -- detect all-null rows
```

For more detail see[Section 9.23](https://www.postgresql.org/docs/10/static/functions-comparisons.html). Row constructors can also be used in connection with subqueries, as discussed in[Section 9.22](https://www.postgresql.org/docs/10/static/functions-subquery.html).

### 4.2.14. Expression Evaluation Rules

The order of evaluation of subexpressions is not defined. In particular, the inputs of an operator or function are not necessarily evaluated left-to-right or in any other fixed order.

Furthermore, if the result of an expression can be determined by evaluating only some parts of it, then other subexpressions might not be evaluated at all. For instance, if one wrote:

```
SELECT true OR somefunc();
```

then`somefunc()`would \(probably\) not be called at all. The same would be the case if one wrote:

```
SELECT somefunc() OR true;
```

Note that this is not the same as the left-to-right“short-circuiting”of Boolean operators that is found in some programming languages.

As a consequence, it is unwise to use functions with side effects as part of complex expressions. It is particularly dangerous to rely on side effects or evaluation order in`WHERE`and`HAVING`clauses, since those clauses are extensively reprocessed as part of developing an execution plan. Boolean expressions \(`AND`/`OR`/`NOT`combinations\) in those clauses can be reorganized in any manner allowed by the laws of Boolean algebra.

When it is essential to force evaluation order, a`CASE`construct \(see[Section 9.17](https://www.postgresql.org/docs/10/static/functions-conditional.html)\) can be used. For example, this is an untrustworthy way of trying to avoid division by zero in a`WHERE`clause:

```
SELECT ... WHERE x 
>
 0 AND y/x 
>
 1.5;
```

But this is safe:

```
SELECT ... WHERE CASE WHEN x 
>
 0 THEN y/x 
>
 1.5 ELSE false END;
```

A`CASE`construct used in this fashion will defeat optimization attempts, so it should only be done when necessary. \(In this particular example, it would be better to sidestep the problem by writing`y > 1.5*x`instead.\)

`CASE`is not a cure-all for such issues, however. One limitation of the technique illustrated above is that it does not prevent early evaluation of constant subexpressions. As described in[Section 37.6](https://www.postgresql.org/docs/10/static/xfunc-volatility.html), functions and operators marked`IMMUTABLE`can be evaluated when the query is planned rather than when it is executed. Thus for example

```
SELECT CASE WHEN x 
>
 0 THEN x ELSE 1/0 END FROM tab;
```

is likely to result in a division-by-zero failure due to the planner trying to simplify the constant subexpression, even if every row in the table has`x > 0`so that the`ELSE`arm would never be entered at run time.

While that particular example might seem silly, related cases that don't obviously involve constants can occur in queries executed within functions, since the values of function arguments and local variables can be inserted into queries as constants for planning purposes. WithinPL/pgSQLfunctions, for example, using an`IF`-`THEN`-`ELSE`statement to protect a risky computation is much safer than just nesting it in a`CASE`expression.

Another limitation of the same kind is that a`CASE`cannot prevent evaluation of an aggregate expression contained within it, because aggregate expressions are computed before other expressions in a`SELECT`list or`HAVING`clause are considered. For example, the following query can cause a division-by-zero error despite seemingly having protected against it:

```
SELECT CASE WHEN min(employees) 
>
 0
            THEN avg(expenses / employees)
       END
    FROM departments;
```

The`min()`and`avg()`aggregates are computed concurrently over all the input rows, so if any row has`employees`equal to zero, the division-by-zero error will occur before there is any opportunity to test the result of`min()`. Instead, use a`WHERE`or`FILTER`clause to prevent problematic input rows from reaching an aggregate function in the first place.

---

[^1]: [PostgreSQL: Documentation: 10: 4.2. Value Expressions](https://www.postgresql.org/docs/10/static/sql-expressions.html)

