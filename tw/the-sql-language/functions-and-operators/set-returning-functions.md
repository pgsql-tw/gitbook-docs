# 9.24. 集合回傳函式

本節介紹可以回傳多個資料列的函數。此類中使用最廣泛的函數是序列生成函數，如 [Table 9.61](set-returning-functions.md#table-9-61-series-generating-functions)和 [Table 9.62](set-returning-functions.md#table-9-62-subscript-generating-functions) 所述。其他更專門的集合回傳函數在本手冊的其他地方介紹。有關組合多個集合回傳函數的方法，請參見[第 7.2.1.4 節](../queries/7.2.-zi-liao-biao-biao-shi-shi.md#7-2-1-the-from-clause)。

## **Table 9.61. Series Generating Functions**

| Function | Argument Type | Return Type | Description |
| :--- | :--- | :--- | :--- |
| `generate_series(`_`start`_, _`stop`_\) | `int`, `bigint` or `numeric` | `setof int`, `setof bigint`, or `setof numeric` \(same as argument type\) | 從 start 到 stop 產生成一系列的值，間隔為 1 |
| `generate_series(`_`start`_, _`stop`_, _`step`_\) | `int`, `bigint` or `numeric` | `setof int`, `setof bigint` or `setof numeric` \(same as argument type\) | 產生一系列的值，從 start 到 end，間隔為 step |
| `generate_series(`_`start`_, _`stop`_, _`step`_ `interval`\) | `timestamp` or `timestamp with time zone` | `setof timestamp` or `setof timestamp with time zone` \(same as argument type\) | 產生一系列的值，從 start 到 end，間隔為 step |

當 step 為正時，如果 start 大於 stop 則回傳零筆資料。相反地，當 step 為負時，如果 start 小於 stop 也回傳零筆資料。NULL 的輸入也回傳零筆資料。 step 為零是錯誤的。以下是一些範例：

```text
SELECT * FROM generate_series(2,4);
 generate_series
-----------------
               2
               3
               4
(3 rows)

SELECT * FROM generate_series(5,1,-2);
 generate_series
-----------------
               5
               3
               1
(3 rows)

SELECT * FROM generate_series(4,3);
 generate_series
-----------------
(0 rows)

SELECT generate_series(1.1, 4, 1.3);
 generate_series 
-----------------
             1.1
             2.4
             3.7
(3 rows)

-- this example relies on the date-plus-integer operator
SELECT current_date + s.a AS dates FROM generate_series(0,14,7) AS s(a);
   dates
------------
 2004-02-05
 2004-02-12
 2004-02-19
(3 rows)

SELECT * FROM generate_series('2008-03-01 00:00'::timestamp,
                              '2008-03-04 12:00', '10 hours');
   generate_series   
---------------------
 2008-03-01 00:00:00
 2008-03-01 10:00:00
 2008-03-01 20:00:00
 2008-03-02 06:00:00
 2008-03-02 16:00:00
 2008-03-03 02:00:00
 2008-03-03 12:00:00
 2008-03-03 22:00:00
 2008-03-04 08:00:00
(9 rows)
```

## **Table 9.62. Subscript Generating Functions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `generate_subscripts(`_`array anyarray`_, _`dim int`_\) | `setof int` | 產生成一個包含給定陣列索引的系列內容。 |
| `generate_subscripts(`_`array anyarray`_, _`dim int`_, _`reverse boolean`_\) | `setof int` | 產生一個包含給定陣列索引的序列內容。當 reverse 為 true 時，將以相反的順序回傳該序列。 |

generate\_subscripts 是一個很方便的函數，用於為給定陣列的指定維度產成一組有效的索引內容。對於沒有所請求維數的陣列或 NULL 陣列，回傳零筆資料（但是對於 NULL 陣列元素，回傳有效的索引）。以下是一些範例：

```text
-- basic usage
SELECT generate_subscripts('{NULL,1,NULL,2}'::int[], 1) AS s;
 s 
---
 1
 2
 3
 4
(4 rows)

-- presenting an array, the subscript and the subscripted
-- value requires a subquery
SELECT * FROM arrays;
         a          
--------------------
 {-1,-2}
 {100,200,300}
(2 rows)

SELECT a AS array, s AS subscript, a[s] AS value
FROM (SELECT generate_subscripts(a, 1) AS s, a FROM arrays) foo;
     array     | subscript | value
---------------+-----------+-------
 {-1,-2}       |         1 |    -1
 {-1,-2}       |         2 |    -2
 {100,200,300} |         1 |   100
 {100,200,300} |         2 |   200
 {100,200,300} |         3 |   300
(5 rows)

-- unnest a 2D array
CREATE OR REPLACE FUNCTION unnest2(anyarray)
RETURNS SETOF anyelement AS $$
select $1[i][j]
   from generate_subscripts($1,1) g1(i),
        generate_subscripts($1,2) g2(j);
$$ LANGUAGE sql IMMUTABLE;
CREATE FUNCTION
SELECT * FROM unnest2(ARRAY[[1,2],[3,4]]);
 unnest2 
---------
       1
       2
       3
       4
(4 rows)
```

當 FROM 子句中的函數加上 WITH ORDINALITY 時，一個 bigint 欄位將附加到輸出資料中，該欄位從 1 開始，並針對函數輸出的每一筆資料以 1 遞增。這對集合回傳函數中的 unnest\(\) 特別有用。

```text
-- set returning function WITH ORDINALITY
SELECT * FROM pg_ls_dir('.') WITH ORDINALITY AS t(ls,n);
       ls        | n
-----------------+----
 pg_serial       |  1
 pg_twophase     |  2
 postmaster.opts |  3
 pg_notify       |  4
 postgresql.conf |  5
 pg_tblspc       |  6
 logfile         |  7
 base            |  8
 postmaster.pid  |  9
 pg_ident.conf   | 10
 global          | 11
 pg_xact         | 12
 pg_snapshots    | 13
 pg_multixact    | 14
 PG_VERSION      | 15
 pg_wal          | 16
 pg_hba.conf     | 17
 pg_stat_tmp     | 18
 pg_subtrans     | 19
(19 rows)
```

