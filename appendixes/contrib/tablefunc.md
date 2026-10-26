<a id="TABLEFUNC"></a>

## F.43. tablefunc — 傳回資料表的函式（`crosstab` 等） [#](#tablefunc) <a href="#tablefunc" id="tablefunc"></a>

[F.43.1. 提供的函式](tablefunc.md#TABLEFUNC-FUNCTIONS-SECT)

[F.43.2. 作者](tablefunc.md#TABLEFUNC-AUTHOR)

<a id="id-1.11.7.53.2"></a>

`tablefunc` 模組包含各種傳回資料表（也就是多筆資料列）的函式。這些函式本身就很有用，也可以作為如何撰寫傳回多筆資料列之 C 函式的範例。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="TABLEFUNC-FUNCTIONS-SECT"></a>

### F.43.1. 提供的函式 [#](#TABLEFUNC-FUNCTIONS-SECT)

[表 F.33](tablefunc.md#TABLEFUNC-FUNCTIONS) 摘要列出 `tablefunc` 模組提供的函式。

<a id="TABLEFUNC-FUNCTIONS"></a>

**表 F.33. `tablefunc` 函式**

<table border="1" class="table" summary="tablefunc 函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">normal_rand</code> ( <em class="parameter"><code>numvals</code></em> <code class="type">integer</code>, <em class="parameter"><code>mean</code></em> <code class="type">float8</code>, <em class="parameter"><code>stddev</code></em> <code class="type">float8</code> )
        → <code class="returnvalue">setof float8</code>
</p>
<p>
        產生一組常態分布的隨機值。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">crosstab</code> ( <em class="parameter"><code>sql</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        產生包含資料列名稱以及 <em class="replaceable"><code>N</code></em> 個值欄位的<span class="quote">“<span class="quote">樞紐表</span>”</span>，其中 <em class="replaceable"><code>N</code></em> 由呼叫查詢中指定的資料列型別決定。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">crosstab<em class="replaceable"><code>N</code></em></code> ( <em class="parameter"><code>sql</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof table_crosstab_<em class="replaceable"><code>N</code></em></code>
</p>
<p>
        產生包含資料列名稱以及 <em class="replaceable"><code>N</code></em> 個值欄位的<span class="quote">“<span class="quote">樞紐表</span>”</span>。<code class="function">crosstab2</code>、<code class="function">crosstab3</code> 與 <code class="function">crosstab4</code> 已預先定義，但你可以依下文所述建立其他 <code class="function">crosstab<em class="replaceable"><code>N</code></em></code> 函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">crosstab</code> ( <em class="parameter"><code>source_sql</code></em> <code class="type">text</code>, <em class="parameter"><code>category_sql</code></em> <code class="type">text</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        產生<span class="quote">“<span class="quote">樞紐表</span>”</span>，其值欄位由第二個查詢指定。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">crosstab</code> ( <em class="parameter"><code>sql</code></em> <code class="type">text</code>, <em class="parameter"><code>N</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        <code class="function">crosstab(text)</code> 的過時版本。參數 <em class="parameter"><code>N</code></em> 現在會被忽略，因為值欄位的數量一律由呼叫查詢決定。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.53.5.3.2.2.6.1.1.1"></a>
<code class="function">connectby</code> ( <em class="parameter"><code>relname</code></em> <code class="type">text</code>, <em class="parameter"><code>keyid_fld</code></em> <code class="type">text</code>, <em class="parameter"><code>parent_keyid_fld</code></em> <code class="type">text</code>
        [<span class="optional">, <em class="parameter"><code>orderby_fld</code></em> <code class="type">text</code> </span>], <em class="parameter"><code>start_with</code></em> <code class="type">text</code>, <em class="parameter"><code>max_depth</code></em> <code class="type">integer</code>
        [<span class="optional">, <em class="parameter"><code>branch_delim</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">setof record</code>
</p>
<p>
        產生階層式樹狀結構的表示。
        </p></td></tr></tbody></table>

<br>

譯註：上表 crosstabN 一列的傳回型別寫作 setof table_crosstab_N，但 tablefunc 擴充功能實際定義的複合型別名稱是 tablefunc_crosstab_N（例如 crosstab2 傳回 setof tablefunc_crosstab_2），與 F.43.1.3 節的 CREATE TYPE 說明一致。

<a id="TABLEFUNC-FUNCTIONS-NORMAL-RAND"></a>

#### F.43.1.1. `normal_rand` [#](#TABLEFUNC-FUNCTIONS-NORMAL-RAND)

<a id="id-1.11.7.53.5.4.2"></a>

```

normal_rand(int numvals, float8 mean, float8 stddev) returns setof float8
```

`normal_rand` 會產生一組常態分布（高斯分布）的隨機值。

*`numvals`* 是函式要傳回的值的個數。*`mean`* 是值之常態分布的平均值，*`stddev`* 是值之常態分布的標準差。

例如，下列呼叫要求 1000 個平均值為 5、標準差為 3 的值：

```

test=# SELECT * FROM normal_rand(1000, 5, 3);
     normal_rand
----------------------
     1.56556322244898
     9.10040991424657
     5.36957140345079
   -0.369151492880995
    0.283600703686639
       .
       .
       .
     4.82992125404908
     9.71308014517282
     2.49639286969028
(1000 rows)
```

<a id="TABLEFUNC-FUNCTIONS-CROSSTAB-TEXT"></a>

#### F.43.1.2. `crosstab(text)` [#](#TABLEFUNC-FUNCTIONS-CROSSTAB-TEXT)

<a id="id-1.11.7.53.5.5.2"></a>

```

crosstab(text sql)
crosstab(text sql, int N)
```

`crosstab` 函式用於產生「樞紐」顯示，其中資料是橫向列出，而非縱向往下列出。例如，我們可能有如下的資料

```

row1    val11
row1    val12
row1    val13
...
row2    val21
row2    val22
row2    val23
...
```

而我們希望顯示成如下形式

```

row1    val11   val12   val13   ...
row2    val21   val22   val23   ...
...
```

`crosstab` 函式接受一個文字參數，該參數是一個 SQL 查詢，會產生以第一種方式排列的原始資料；函式則會產生以第二種方式排列的資料表。

*`sql`* 參數是產生來源資料集的 SQL 陳述式。此陳述式必須傳回一個 `row_name` 欄位、一個 `category` 欄位，以及一個 `value` 欄位。*`N`* 是過時的參數，若有提供會被忽略（以前它必須與輸出值欄位的數量相符，但現在該數量由呼叫查詢決定）。

例如，所提供的查詢可能產生類似下面的資料集：

```

 row_name    cat    value
----------+-------+-------
  row1      cat1    val1
  row1      cat2    val2
  row1      cat3    val3
  row1      cat4    val4
  row2      cat1    val5
  row2      cat2    val6
  row2      cat3    val7
  row2      cat4    val8
```

`crosstab` 函式宣告為傳回 `setof
record`，因此輸出欄位的實際名稱與型別必須在呼叫端 `SELECT` 陳述式的 `FROM` 子句中定義，例如：

```

SELECT * FROM crosstab('...') AS ct(row_name text, category_1 text, category_2 text);
```

此範例產生的資料集類似下面這樣：

```

           <== value  columns  ==>
 row_name   category_1   category_2
----------+------------+------------
  row1        val1         val2
  row2        val5         val6
```

`FROM` 子句必須將輸出定義為一個 `row_name` 欄位（資料型別與 SQL 查詢的第一個結果欄位相同），後接 N 個 `value` 欄位（資料型別皆與 SQL 查詢的第三個結果欄位相同）。你可以設定任意數量的輸出值欄位。輸出欄位的名稱由你決定。

`crosstab` 函式會為每一組具有相同 `row_name` 值的連續輸入資料列產生一筆輸出資料列。它會以這些資料列的 `value` 欄位，由左至右填入輸出的 `value` 欄位。若群組中的資料列少於輸出 `value` 欄位的數量，多出的輸出欄位會填入 null；若資料列較多，多出的輸入資料列會被略過。

實務上，SQL 查詢應該一律指定 `ORDER BY 1,2`，以確保輸入資料列的順序正確，也就是讓具有相同 `row_name` 的值集中在一起，並在該列中正確排序。請注意，`crosstab` 本身完全不理會查詢結果的第二個欄位；該欄位只是用來排序，以控制第三欄的值橫向出現的順序。

以下是完整的範例：

```

CREATE TABLE ct(id SERIAL, rowid TEXT, attribute TEXT, value TEXT);
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att1','val1');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att2','val2');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att3','val3');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att4','val4');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att1','val5');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att2','val6');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att3','val7');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att4','val8');

SELECT *
FROM crosstab(
  'select rowid, attribute, value
   from ct
   where attribute = ''att2'' or attribute = ''att3''
   order by 1,2')
AS ct(row_name text, category_1 text, category_2 text, category_3 text);

 row_name | category_1 | category_2 | category_3
----------+------------+------------+------------
 test1    | val2       | val3       |
 test2    | val6       | val7       |
(2 rows)
```

你可以設定一個自訂的 crosstab 函式，將所需的輸出資料列型別寫入其定義中，以免每次都必須寫出 `FROM` 子句來定義輸出欄位。下一節會說明這種做法。另一種可能的做法是將所需的 `FROM` 子句嵌入檢視表定義中。

### 注意

另請參閱 psql 中的 `\crosstabview` 命令，它提供類似 `crosstab()` 的功能。

<a id="TABLEFUNC-FUNCTIONS-CROSSTAB-N-TEXT"></a>

#### F.43.1.3. `crosstabN(text)` [#](#TABLEFUNC-FUNCTIONS-CROSSTAB-N-TEXT)

<a id="id-1.11.7.53.5.6.2"></a>

```

crosstabN(text sql)
```

`crosstabN` 函式是示範如何為通用 `crosstab` 函式設定自訂包裝函式的範例，讓你不必在呼叫端 `SELECT` 查詢中寫出欄位名稱與型別。`tablefunc` 模組包含 `crosstab2`、`crosstab3` 與 `crosstab4`，其輸出資料列型別定義如下

```

CREATE TYPE tablefunc_crosstab_N AS (
    row_name TEXT,
    category_1 TEXT,
    category_2 TEXT,
        .
        .
        .
    category_N TEXT
);
```

因此，當輸入查詢產生型別為 `text` 的 `row_name` 與 `value` 欄位，而你需要 2、3 或 4 個輸出值欄位時，就可以直接使用這些函式。在其他所有方面，它們的行為都與上文所述的通用 `crosstab` 函式完全相同。

例如，上一節所舉的範例也可以寫成

```

SELECT *
FROM crosstab3(
  'select rowid, attribute, value
   from ct
   where attribute = ''att2'' or attribute = ''att3''
   order by 1,2');
```

這些函式主要是為了示範而提供。你可以根據底層的 `crosstab()` 函式建立自己的傳回型別與函式。有兩種做法：

* 建立描述所需輸出欄位的複合型別，類似 `contrib/tablefunc/tablefunc--1.0.sql` 中的範例。接著定義一個唯一的函式名稱，接受一個 `text` 參數並傳回 `setof your_type_name`，但連結到同一個底層 `crosstab` C 函式。例如，若你的來源資料產生的資料列名稱為 `text`、值為 `float8`，而你需要 5 個值欄位：

  ```

  CREATE TYPE my_crosstab_float8_5_cols AS (
      my_row_name text,
      my_category_1 float8,
      my_category_2 float8,
      my_category_3 float8,
      my_category_4 float8,
      my_category_5 float8
  );

  CREATE OR REPLACE FUNCTION crosstab_float8_5_cols(text)
      RETURNS setof my_crosstab_float8_5_cols
      AS '$libdir/tablefunc','crosstab' LANGUAGE C STABLE STRICT;
  ```
* 使用 `OUT` 參數隱含地定義傳回型別。同一個範例也可以用這種方式完成：

  ```

  CREATE OR REPLACE FUNCTION crosstab_float8_5_cols(
      IN text,
      OUT my_row_name text,
      OUT my_category_1 float8,
      OUT my_category_2 float8,
      OUT my_category_3 float8,
      OUT my_category_4 float8,
      OUT my_category_5 float8)
    RETURNS setof record
    AS '$libdir/tablefunc','crosstab' LANGUAGE C STABLE STRICT;
  ```

<a id="TABLEFUNC-FUNCTIONS-CROSSTAB-TEXT-2"></a>

#### F.43.1.4. `crosstab(text, text)` [#](#TABLEFUNC-FUNCTIONS-CROSSTAB-TEXT-2)

<a id="id-1.11.7.53.5.7.2"></a>

```

crosstab(text source_sql, text category_sql)
```

單一參數形式的 `crosstab` 主要的限制在於，它會將群組中的所有值一視同仁，把每個值插入第一個可用的欄位。若你希望值欄位對應特定的資料類別，而某些群組可能沒有某些類別的資料，這種方式就不太適用。雙參數形式的 `crosstab` 透過提供與輸出欄位對應的明確類別清單來處理這種情況。

*`source_sql`* 是產生來源資料集的 SQL 陳述式。此陳述式必須傳回一個 `row_name` 欄位、一個 `category` 欄位，以及一個 `value` 欄位。它也可以有一個或多個「額外」欄位。`row_name` 欄位必須是第一個。`category` 與 `value` 欄位必須是最後兩個欄位，且依此順序排列。`row_name` 與 `category` 之間的任何欄位都會被視為「額外」欄位。具有相同 `row_name` 值的所有資料列，其「額外」欄位預期應該相同。

例如，*`source_sql`* 可能產生類似下面的資料集：

```

SELECT row_name, extra_col, cat, value FROM foo ORDER BY 1;

 row_name    extra_col   cat    value
----------+------------+-----+---------
  row1         extra1    cat1    val1
  row1         extra1    cat2    val2
  row1         extra1    cat4    val4
  row2         extra2    cat1    val5
  row2         extra2    cat2    val6
  row2         extra2    cat3    val7
  row2         extra2    cat4    val8
```

*`category_sql`* 是產生類別集合的 SQL 陳述式。此陳述式必須只傳回一個欄位。它必須產生至少一筆資料列，否則會產生錯誤。此外，它不得產生重複的值，否則會產生錯誤。*`category_sql`* 可能類似下面這樣：

```

SELECT DISTINCT cat FROM foo ORDER BY 1;
    cat
  -------
    cat1
    cat2
    cat3
    cat4
```

`crosstab` 函式宣告為傳回 `setof
record`，因此輸出欄位的實際名稱與型別必須在呼叫端 `SELECT` 陳述式的 `FROM` 子句中定義，例如：

```

SELECT * FROM crosstab('...', '...')
    AS ct(row_name text, extra text, cat1 text, cat2 text, cat3 text, cat4 text);
```

這會產生類似下面的結果：

```

                  <==  value  columns   ==>
row_name   extra   cat1   cat2   cat3   cat4
---------+-------+------+------+------+------
  row1     extra1  val1   val2          val4
  row2     extra2  val5   val6   val7   val8
```

`FROM` 子句必須定義正確數量、正確資料型別的輸出欄位。若 *`source_sql`* 查詢的結果有 *`N`* 個欄位，其中前 *`N`*-2 個必須與前 *`N`*-2 個輸出欄位相符。其餘的輸出欄位必須具有 *`source_sql`* 查詢結果最後一個欄位的型別，而且其數量必須恰好等於 *`category_sql`* 查詢結果的資料列數。

`crosstab` 函式會為每一組具有相同 `row_name` 值的連續輸入資料列產生一筆輸出資料列。輸出的 `row_name` 欄位以及任何「額外」欄位，都會從群組的第一筆資料列複製。輸出的 `value` 欄位會以 `category` 值相符之資料列的 `value` 欄位填入。若某筆資料列的 `category` 不符合 *`category_sql`* 查詢的任何輸出，其 `value` 會被忽略。若某個輸出欄位所對應的類別未出現在群組的任何輸入資料列中，該欄位會填入 null。

實務上，*`source_sql`* 查詢應該一律指定 `ORDER BY 1`，以確保具有相同 `row_name` 的值集中在一起。不過，群組內類別的順序並不重要。此外，務必確保 *`category_sql`* 查詢輸出的順序與指定的輸出欄位順序相符。

以下是兩個完整的範例：

```

create table sales(year int, month int, qty int);
insert into sales values(2007, 1, 1000);
insert into sales values(2007, 2, 1500);
insert into sales values(2007, 7, 500);
insert into sales values(2007, 11, 1500);
insert into sales values(2007, 12, 2000);
insert into sales values(2008, 1, 1000);

select * from crosstab(
  'select year, month, qty from sales order by 1',
  'select m from generate_series(1,12) m'
) as (
  year int,
  "Jan" int,
  "Feb" int,
  "Mar" int,
  "Apr" int,
  "May" int,
  "Jun" int,
  "Jul" int,
  "Aug" int,
  "Sep" int,
  "Oct" int,
  "Nov" int,
  "Dec" int
);
 year | Jan  | Feb  | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov  | Dec
------+------+------+-----+-----+-----+-----+-----+-----+-----+-----+------+------
 2007 | 1000 | 1500 |     |     |     |     | 500 |     |     |     | 1500 | 2000
 2008 | 1000 |      |     |     |     |     |     |     |     |     |      |
(2 rows)
```

```

CREATE TABLE cth(rowid text, rowdt timestamp, attribute text, val text);
INSERT INTO cth VALUES('test1','01 March 2003','temperature','42');
INSERT INTO cth VALUES('test1','01 March 2003','test_result','PASS');
INSERT INTO cth VALUES('test1','01 March 2003','volts','2.6987');
INSERT INTO cth VALUES('test2','02 March 2003','temperature','53');
INSERT INTO cth VALUES('test2','02 March 2003','test_result','FAIL');
INSERT INTO cth VALUES('test2','02 March 2003','test_startdate','01 March 2003');
INSERT INTO cth VALUES('test2','02 March 2003','volts','3.1234');

SELECT * FROM crosstab
(
  'SELECT rowid, rowdt, attribute, val FROM cth ORDER BY 1',
  'SELECT DISTINCT attribute FROM cth ORDER BY 1'
)
AS
(
       rowid text,
       rowdt timestamp,
       temperature int4,
       test_result text,
       test_startdate timestamp,
       volts float8
);
 rowid |          rowdt           | temperature | test_result |      test_startdate      | volts
-------+--------------------------+-------------+-------------+--------------------------+--------
 test1 | Sat Mar 01 00:00:00 2003 |          42 | PASS        |                          | 2.6987
 test2 | Sun Mar 02 00:00:00 2003 |          53 | FAIL        | Sat Mar 01 00:00:00 2003 | 3.1234
(2 rows)
```

你可以建立預先定義的函式，以免在每個查詢中都必須寫出結果欄位的名稱與型別。請參閱上一節的範例。這種形式的 `crosstab` 所使用的底層 C 函式名為 `crosstab_hash`。

<a id="TABLEFUNC-FUNCTIONS-CONNECTBY"></a>

#### F.43.1.5. `connectby` [#](#TABLEFUNC-FUNCTIONS-CONNECTBY)

<a id="id-1.11.7.53.5.8.2"></a>

```

connectby(text relname, text keyid_fld, text parent_keyid_fld
          [, text orderby_fld ], text start_with, int max_depth
          [, text branch_delim ])
```

`connectby` 函式會將儲存於資料表中的階層式資料顯示出來。該資料表必須有一個可唯一識別資料列的鍵欄位，以及一個參照各資料列之父資料列（若有的話）的父鍵欄位。`connectby` 可以顯示從任一資料列往下延伸的子樹。

[表 F.34](tablefunc.md#TABLEFUNC-CONNECTBY-PARAMETERS) 說明各參數。

<a id="TABLEFUNC-CONNECTBY-PARAMETERS"></a>

**表 F.34. `connectby` 參數**

<table border="1" class="table" summary="connectby 參數"><colgroup><col/><col/></colgroup><thead><tr><th>參數</th><th>說明</th></tr></thead><tbody><tr><td><em class="parameter"><code>relname</code></em></td><td>來源關聯的名稱</td></tr><tr><td><em class="parameter"><code>keyid_fld</code></em></td><td>鍵欄位的名稱</td></tr><tr><td><em class="parameter"><code>parent_keyid_fld</code></em></td><td>父鍵欄位的名稱</td></tr><tr><td><em class="parameter"><code>orderby_fld</code></em></td><td>用來排序同層節點的欄位名稱（選用）</td></tr><tr><td><em class="parameter"><code>start_with</code></em></td><td>作為起點之資料列的鍵值</td></tr><tr><td><em class="parameter"><code>max_depth</code></em></td><td>向下展開的最大深度；零表示不限深度</td></tr><tr><td><em class="parameter"><code>branch_delim</code></em></td><td>在分支輸出中用來分隔各鍵的字串（選用）</td></tr></tbody></table>

<br>

鍵欄位與父鍵欄位可以是任何資料型別，但兩者必須是相同的型別。請注意，無論鍵欄位的型別為何，*`start_with`* 值都必須以文字字串輸入。

`connectby` 函式宣告為傳回 `setof
record`，因此輸出欄位的實際名稱與型別必須在呼叫端 `SELECT` 陳述式的 `FROM` 子句中定義，例如：

```

SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'pos', 'row2', 0, '~')
    AS t(keyid text, parent_keyid text, level int, branch text, pos int);
```

前兩個輸出欄位用於目前資料列的鍵及其父資料列的鍵；它們必須與資料表鍵欄位的型別相符。第三個輸出欄位是在樹中的深度，型別必須是 `integer`。若有提供 *`branch_delim`* 參數，下一個輸出欄位是分支顯示，型別必須是 `text`。最後，若有提供 *`orderby_fld`* 參數，最後一個輸出欄位是序號，型別必須是 `integer`。

「branch」輸出欄位顯示到達目前資料列所經過的鍵路徑。各鍵之間以指定的 *`branch_delim`* 字串分隔。若不需要分支顯示，請同時省略 *`branch_delim`* 參數以及輸出欄位清單中的分支欄位。

若同一父節點下同層節點的順序很重要，請加入 *`orderby_fld`* 參數，指定用來排序同層節點的欄位。此欄位可以是任何可排序的資料型別。若且唯若有指定 *`orderby_fld`*，輸出欄位清單就必須包含最後一個整數序號欄位。

代表資料表與欄位名稱的參數會原樣複製到 `connectby` 內部產生的 SQL 查詢中。因此，若名稱包含大小寫混合或特殊字元，請加上雙引號。你也可能需要以綱要限定資料表名稱。

在大型資料表中，除非父鍵欄位上有索引，否則效能會很差。

重要的是，*`branch_delim`* 字串不可出現在任何鍵值中，否則 `connectby` 可能會誤報無限遞迴錯誤。請注意，若未提供 *`branch_delim`*，則會使用預設值 `~` 進行遞迴偵測。

以下是範例：

```

CREATE TABLE connectby_tree(keyid text, parent_keyid text, pos int);

INSERT INTO connectby_tree VALUES('row1',NULL, 0);
INSERT INTO connectby_tree VALUES('row2','row1', 0);
INSERT INTO connectby_tree VALUES('row3','row1', 0);
INSERT INTO connectby_tree VALUES('row4','row2', 1);
INSERT INTO connectby_tree VALUES('row5','row2', 0);
INSERT INTO connectby_tree VALUES('row6','row4', 0);
INSERT INTO connectby_tree VALUES('row7','row3', 0);
INSERT INTO connectby_tree VALUES('row8','row6', 0);
INSERT INTO connectby_tree VALUES('row9','row5', 0);

-- with branch, without orderby_fld (order of results is not guaranteed)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'row2', 0, '~')
 AS t(keyid text, parent_keyid text, level int, branch text);
 keyid | parent_keyid | level |       branch
-------+--------------+-------+---------------------
 row2  |              |     0 | row2
 row4  | row2         |     1 | row2~row4
 row6  | row4         |     2 | row2~row4~row6
 row8  | row6         |     3 | row2~row4~row6~row8
 row5  | row2         |     1 | row2~row5
 row9  | row5         |     2 | row2~row5~row9
(6 rows)

-- without branch, without orderby_fld (order of results is not guaranteed)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'row2', 0)
 AS t(keyid text, parent_keyid text, level int);
 keyid | parent_keyid | level
-------+--------------+-------
 row2  |              |     0
 row4  | row2         |     1
 row6  | row4         |     2
 row8  | row6         |     3
 row5  | row2         |     1
 row9  | row5         |     2
(6 rows)

-- with branch, with orderby_fld (notice that row5 comes before row4)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'pos', 'row2', 0, '~')
 AS t(keyid text, parent_keyid text, level int, branch text, pos int);
 keyid | parent_keyid | level |       branch        | pos
-------+--------------+-------+---------------------+-----
 row2  |              |     0 | row2                |   1
 row5  | row2         |     1 | row2~row5           |   2
 row9  | row5         |     2 | row2~row5~row9      |   3
 row4  | row2         |     1 | row2~row4           |   4
 row6  | row4         |     2 | row2~row4~row6      |   5
 row8  | row6         |     3 | row2~row4~row6~row8 |   6
(6 rows)

-- without branch, with orderby_fld (notice that row5 comes before row4)
SELECT * FROM connectby('connectby_tree', 'keyid', 'parent_keyid', 'pos', 'row2', 0)
 AS t(keyid text, parent_keyid text, level int, pos int);
 keyid | parent_keyid | level | pos
-------+--------------+-------+-----
 row2  |              |     0 |   1
 row5  | row2         |     1 |   2
 row9  | row5         |     2 |   3
 row4  | row2         |     1 |   4
 row6  | row4         |     2 |   5
 row8  | row6         |     3 |   6
(6 rows)
```

<a id="TABLEFUNC-AUTHOR"></a>

### F.43.2. 作者 [#](#TABLEFUNC-AUTHOR)

Joe Conway

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tablefunc.html)（原文版本：18.6；核對日期：2026-10-22）
