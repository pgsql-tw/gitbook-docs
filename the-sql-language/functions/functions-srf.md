<a id="FUNCTIONS-SRF"></a>

## 9.26. 集合回傳函式 [#](#FUNCTIONS-SRF)

<a id="id-1.5.8.32.2"></a>

本節說明可能回傳不只一筆資料列的函式。這類函式中使用最廣泛的是序列產生函式，詳見[表 9.69](functions-srf.md#FUNCTIONS-SRF-SERIES) 與[表 9.70](functions-srf.md#FUNCTIONS-SRF-SUBSCRIPTS)。其他更專門的集合回傳函式，則在本手冊的其他地方說明。關於組合多個集合回傳函式的方法，請參閱[第 7.2.1.4 節](../queries/queries-table-expressions.md#QUERIES-TABLEFUNCTIONS)。

<a id="FUNCTIONS-SRF-SERIES"></a>

**表 9.69. 序列產生函式**

<table border="1" class="table" summary="Series Generating Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.32.4.2.2.1.1.1.1"></a>
<code class="function">generate_series</code> ( <em class="parameter"><code>start</code></em> <code class="type">integer</code>, <em class="parameter"><code>stop</code></em> <code class="type">integer</code> [<span class="optional">, <em class="parameter"><code>step</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">setof integer</code>
</p>
<p class="func_signature">
<code class="function">generate_series</code> ( <em class="parameter"><code>start</code></em> <code class="type">bigint</code>, <em class="parameter"><code>stop</code></em> <code class="type">bigint</code> [<span class="optional">, <em class="parameter"><code>step</code></em> <code class="type">bigint</code> </span>] )
        → <code class="returnvalue">setof bigint</code>
</p>
<p class="func_signature">
<code class="function">generate_series</code> ( <em class="parameter"><code>start</code></em> <code class="type">numeric</code>, <em class="parameter"><code>stop</code></em> <code class="type">numeric</code> [<span class="optional">, <em class="parameter"><code>step</code></em> <code class="type">numeric</code> </span>] )
        → <code class="returnvalue">setof numeric</code>
</p>
<p>
        產生從 <em class="parameter"><code>start</code></em> 到 <em class="parameter"><code>stop</code></em>、步長為 <em class="parameter"><code>step</code></em> 的一系列值。<em class="parameter"><code>step</code></em> 預設為 1。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">generate_series</code> ( <em class="parameter"><code>start</code></em> <code class="type">timestamp</code>, <em class="parameter"><code>stop</code></em> <code class="type">timestamp</code>, <em class="parameter"><code>step</code></em> <code class="type">interval</code> )
        → <code class="returnvalue">setof timestamp</code>
</p>
<p class="func_signature">
<code class="function">generate_series</code> ( <em class="parameter"><code>start</code></em> <code class="type">timestamp with time zone</code>, <em class="parameter"><code>stop</code></em> <code class="type">timestamp with time zone</code>, <em class="parameter"><code>step</code></em> <code class="type">interval</code> [<span class="optional">, <em class="parameter"><code>timezone</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">setof timestamp with time zone</code>
</p>
<p>
        產生從 <em class="parameter"><code>start</code></em> 到 <em class="parameter"><code>stop</code></em>、步長為 <em class="parameter"><code>step</code></em> 的一系列值。在考量時區的形式中，一天中的時間與日光節約時間的調整，會依照 <em class="parameter"><code>timezone</code></em> 引數所指定的時區計算；如果省略該引數，則依照目前的 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-TIMEZONE">TimeZone</a> 設定計算。
       </p></td></tr></tbody></table>

<br>

當 *`step`* 為正數時，如果 *`start`* 大於 *`stop`*，就會回傳零筆資料列。反之，當 *`step`* 為負數時，如果 *`start`* 小於 *`stop`*，就會回傳零筆資料列。如果任何輸入為 `NULL`，也會回傳零筆資料列。*`step`* 為零是錯誤。以下是一些範例：

```

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

-- this example relies on the date-plus-integer operator:
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

-- this example assumes that TimeZone is set to UTC; note the DST transition:
SELECT * FROM generate_series('2001-10-22 00:00 -04:00'::timestamptz,
                              '2001-11-01 00:00 -05:00'::timestamptz,
                              '1 day'::interval, 'America/New_York');
    generate_series
------------------------
 2001-10-22 04:00:00+00
 2001-10-23 04:00:00+00
 2001-10-24 04:00:00+00
 2001-10-25 04:00:00+00
 2001-10-26 04:00:00+00
 2001-10-27 04:00:00+00
 2001-10-28 04:00:00+00
 2001-10-29 05:00:00+00
 2001-10-30 05:00:00+00
 2001-10-31 05:00:00+00
 2001-11-01 05:00:00+00
(11 rows)
```

<a id="FUNCTIONS-SRF-SUBSCRIPTS"></a>

**表 9.70. 下標產生函式**

<table border="1" class="table" summary="Subscript Generating Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.32.6.2.2.1.1.1.1"></a>
<code class="function">generate_subscripts</code> ( <em class="parameter"><code>array</code></em> <code class="type">anyarray</code>, <em class="parameter"><code>dim</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">setof integer</code>
</p>
<p>
        產生由給定陣列第 <em class="parameter"><code>dim</code></em> 維之有效下標所組成的序列。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">generate_subscripts</code> ( <em class="parameter"><code>array</code></em> <code class="type">anyarray</code>, <em class="parameter"><code>dim</code></em> <code class="type">integer</code>,  <em class="parameter"><code>reverse</code></em> <code class="type">boolean</code> )
        → <code class="returnvalue">setof integer</code>
</p>
<p>
        產生由給定陣列第 <em class="parameter"><code>dim</code></em> 維之有效下標所組成的序列。當 <em class="parameter"><code>reverse</code></em> 為 true 時，以相反的順序回傳該序列。
       </p></td></tr></tbody></table>

<br>

`generate_subscripts` 是一個方便的函式，會為給定陣列的指定維度產生有效下標的集合。對於沒有所要求維度的陣列，或是任何輸入為 `NULL` 時，會回傳零筆資料列。以下是一些範例：

```

-- basic usage:
SELECT generate_subscripts('{NULL,1,NULL,2}'::int[], 1) AS s;
 s
---
 1
 2
 3
 4
(4 rows)

-- presenting an array, the subscript and the subscripted
-- value requires a subquery:
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

-- unnest a 2D array:
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

<a id="id-1.5.8.32.8"></a>

當 `FROM` 子句中的函式後面加上 `WITH ORDINALITY` 時，函式的輸出欄位後面會附加一個 `bigint` 欄位，它從 1 開始，函式輸出的每一筆資料列遞增 1。這對於 `unnest()` 這類集合回傳函式最為有用。

```

-- set returning function WITH ORDINALITY:
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

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-srf.html)（原文版本：18.6；核對日期：2026-09-11）
