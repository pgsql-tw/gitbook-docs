<a id="FUNCTIONS-COMPARISON"></a>

## 9.2. 比較函式與運算子 [#](#FUNCTIONS-COMPARISON)

<a id="id-1.5.8.8.2"></a>

可用的是一般的比較運算子，如[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所示。

<a id="FUNCTIONS-COMPARISON-OP-TABLE"></a>

**表 9.1. 比較運算子**

<table border="1" class="table" summary="Comparison Operators"><colgroup><col/><col/></colgroup><thead><tr><th>運算子</th><th>說明</th></tr></thead><tbody><tr><td>
<em class="replaceable"><code>datatype</code></em> <code class="literal">&lt;</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</td><td>小於</td></tr><tr><td>
<em class="replaceable"><code>datatype</code></em> <code class="literal">&gt;</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</td><td>大於</td></tr><tr><td>
<em class="replaceable"><code>datatype</code></em> <code class="literal">&lt;=</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</td><td>小於或等於</td></tr><tr><td>
<em class="replaceable"><code>datatype</code></em> <code class="literal">&gt;=</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</td><td>大於或等於</td></tr><tr><td>
<em class="replaceable"><code>datatype</code></em> <code class="literal">=</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</td><td>等於</td></tr><tr><td>
<em class="replaceable"><code>datatype</code></em> <code class="literal">&lt;&gt;</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</td><td>不等於</td></tr><tr><td>
<em class="replaceable"><code>datatype</code></em> <code class="literal">!=</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</td><td>不等於</td></tr></tbody></table>

<br>

### 注意

`<>` 是「不等於」的標準 SQL 表示法。`!=` 是它的別名，在剖析的極早期階段就會被轉換為 `<>`。因此，無法實作行為不同的 `!=` 與 `<>` 運算子。

這些比較運算子適用於所有具有自然順序的內建資料型別，包括數值、字串與日期／時間型別。此外，只要陣列、複合型別與範圍的組成資料型別可以比較，它們也可以比較。

通常也可以比較相關資料型別的值；例如 `integer` `>` `bigint` 就可以運作。有些這類情況是直接由「跨型別」比較運算子實作的，但如果沒有這樣的運算子可用，剖析器會將較不通用的型別強制轉換為較通用的型別，然後套用後者的比較運算子。

如上所示，所有比較運算子都是回傳 `boolean` 型別值的二元運算子。因此，像 `1 < 2 < 3` 這樣的運算式是無效的（因為沒有將布林值與 `3` 比較的 `<` 運算子）。請使用下面所示的 `BETWEEN` 述詞來進行範圍測試。

此外還有一些比較述詞，如[表 9.2](functions-comparison.md#FUNCTIONS-COMPARISON-PRED-TABLE) 所示。它們的行為很像運算子，但具有 SQL 標準所規定的特殊語法。

<a id="FUNCTIONS-COMPARISON-PRED-TABLE"></a>

**表 9.2. 比較述詞**

<table border="1" class="table" summary="Comparison Predicates"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        述詞
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">BETWEEN</code> <em class="replaceable"><code>datatype</code></em> <code class="literal">AND</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        介於之間（包含範圍的端點）。
       </p>
<p>
<code class="literal">2 BETWEEN 1 AND 3</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">2 BETWEEN 3 AND 1</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">NOT BETWEEN</code> <em class="replaceable"><code>datatype</code></em> <code class="literal">AND</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        不介於之間（<code class="literal">BETWEEN</code> 的否定）。
       </p>
<p>
<code class="literal">2 NOT BETWEEN 1 AND 3</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">BETWEEN SYMMETRIC</code> <em class="replaceable"><code>datatype</code></em> <code class="literal">AND</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        將兩個端點值排序之後，判斷是否介於之間。
       </p>
<p>
<code class="literal">2 BETWEEN SYMMETRIC 3 AND 1</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">NOT BETWEEN SYMMETRIC</code> <em class="replaceable"><code>datatype</code></em> <code class="literal">AND</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        將兩個端點值排序之後，判斷是否不介於之間。
       </p>
<p>
<code class="literal">2 NOT BETWEEN SYMMETRIC 3 AND 1</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">IS DISTINCT FROM</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        不等於，將 null 視為可比較的值。
       </p>
<p>
<code class="literal">1 IS DISTINCT FROM NULL</code> → <code class="returnvalue">t</code>（而不是 <code class="literal">NULL</code>）
       </p>
<p>
<code class="literal">NULL IS DISTINCT FROM NULL</code> → <code class="returnvalue">f</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">IS NOT DISTINCT FROM</code> <em class="replaceable"><code>datatype</code></em>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        等於，將 null 視為可比較的值。
       </p>
<p>
<code class="literal">1 IS NOT DISTINCT FROM NULL</code> → <code class="returnvalue">f</code>（而不是 <code class="literal">NULL</code>）
       </p>
<p>
<code class="literal">NULL IS NOT DISTINCT FROM NULL</code> → <code class="returnvalue">t</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">IS NULL</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗值是否為 null。
       </p>
<p>
<code class="literal">1.5 IS NULL</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">IS NOT NULL</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗值是否不為 null。
       </p>
<p>
<code class="literal">'null' IS NOT NULL</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">ISNULL</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗值是否為 null（非標準語法）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<em class="replaceable"><code>datatype</code></em> <code class="literal">NOTNULL</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗值是否不為 null（非標準語法）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">boolean</code> <code class="literal">IS TRUE</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗布林運算式是否產生 true。
       </p>
<p>
<code class="literal">true IS TRUE</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">NULL::boolean IS TRUE</code> → <code class="returnvalue">f</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">boolean</code> <code class="literal">IS NOT TRUE</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗布林運算式是否產生 false 或未知。
       </p>
<p>
<code class="literal">true IS NOT TRUE</code>
        → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">NULL::boolean IS NOT TRUE</code> → <code class="returnvalue">t</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">boolean</code> <code class="literal">IS FALSE</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗布林運算式是否產生 false。
       </p>
<p>
<code class="literal">true IS FALSE</code>
        → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">NULL::boolean IS FALSE</code> → <code class="returnvalue">f</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">boolean</code> <code class="literal">IS NOT FALSE</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗布林運算式是否產生 true 或未知。
       </p>
<p>
<code class="literal">true IS NOT FALSE</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">NULL::boolean IS NOT FALSE</code> → <code class="returnvalue">t</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">boolean</code> <code class="literal">IS UNKNOWN</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗布林運算式是否產生未知。
       </p>
<p>
<code class="literal">true IS UNKNOWN</code>
        → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">NULL::boolean IS UNKNOWN</code> → <code class="returnvalue">t</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">boolean</code> <code class="literal">IS NOT UNKNOWN</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗布林運算式是否產生 true 或 false。
       </p>
<p>
<code class="literal">true IS NOT UNKNOWN</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">NULL::boolean IS NOT UNKNOWN</code> → <code class="returnvalue">f</code>（而不是 <code class="literal">NULL</code>）
       </p></td></tr></tbody></table>

<br>

<a id="id-1.5.8.8.11.1"></a>
<a id="id-1.5.8.8.11.2"></a>
`BETWEEN` 述詞可以簡化範圍測試：

```

a BETWEEN x AND y
```

等價於

```

a >= x AND a <= y
```

請注意，`BETWEEN` 將端點值視為包含在範圍內。`BETWEEN SYMMETRIC` 與 `BETWEEN` 類似，只是不要求 `AND` 左邊的引數小於或等於右邊的引數。如果不是這樣，這兩個引數會自動對調，因此一律隱含一個非空的範圍。

`BETWEEN` 的各種變化形式都是以一般的比較運算子實作的，因此適用於任何可以比較的資料型別。

### 注意

在 `BETWEEN` 語法中使用 `AND`，會與把 `AND` 用作邏輯運算子產生歧義。為了解決這個問題，`BETWEEN` 子句的第二個引數只允許使用有限的幾種運算式類型。如果你需要在 `BETWEEN` 中撰寫更複雜的子運算式，請在該子運算式外加上括號。

<a id="id-1.5.8.8.14.1"></a>
<a id="id-1.5.8.8.14.2"></a>
當任一輸入為 null 時，一般的比較運算子會產生 null（表示「未知」），而不是 true 或 false。例如，`7 = NULL` 會產生 null，`7 <> NULL` 也是如此。當這種行為不合適時，請使用 `IS [ NOT ] DISTINCT FROM` 述詞：

```

a IS DISTINCT FROM b
a IS NOT DISTINCT FROM b
```

對於非 null 的輸入，`IS DISTINCT FROM` 與 `<>` 運算子相同。不過，如果兩個輸入都是 null，它會回傳 false；如果只有一個輸入是 null，它會回傳 true。同樣地，對於非 null 的輸入，`IS NOT DISTINCT FROM` 與 `=` 完全相同，但當兩個輸入都是 null 時它會回傳 true，只有一個輸入是 null 時則回傳 false。因此，這些述詞實際上把 null 當作一般的資料值，而不是「未知」。

<a id="id-1.5.8.8.15.1"></a>
<a id="id-1.5.8.8.15.2"></a>
<a id="id-1.5.8.8.15.3"></a>
<a id="id-1.5.8.8.15.4"></a>
要檢查一個值是否為 null，請使用下列述詞：

```

expression IS NULL
expression IS NOT NULL
```

或是等價但非標準的述詞：

```

expression ISNULL
expression NOTNULL
```

<a id="id-1.5.8.8.15.7"></a>

*不要*寫成 `expression = NULL`，因為 `NULL` 並不「等於」`NULL`。（null 值代表未知的值，而我們無法得知兩個未知的值是否相等。）

### 提示

有些應用程式可能會預期，當 *`expression`* 的結果為 null 值時，`expression = NULL` 會回傳 true。強烈建議修改這些應用程式，使其符合 SQL 標準。不過，如果無法這麼做，可以使用 [transform_null_equals](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-TRANSFORM-NULL-EQUALS) 組態變數。如果啟用它，PostgreSQL 會將 `x = NULL` 子句轉換為 `x IS NULL`。

如果 *`expression`* 是資料列值，那麼當資料列運算式本身為 null，或該資料列的所有欄位都為 null 時，`IS NULL` 為 true；而當資料列運算式本身非 null，且該資料列的所有欄位都非 null 時，`IS NOT NULL` 為 true。由於這種行為，對於資料列值的運算式，`IS NULL` 與 `IS NOT NULL` 不一定總是回傳相反的結果；特別是，同時包含 null 與非 null 欄位的資料列值運算式，在兩項測試中都會回傳 false。例如：

```

SELECT ROW(1,2.5,'this is a test') = ROW(1, 3, 'not the same');

SELECT ROW(table.*) IS NULL FROM table;  -- detect all-null rows

SELECT ROW(table.*) IS NOT NULL FROM table;  -- detect all-non-null rows

SELECT NOT(ROW(table.*) IS NOT NULL) FROM TABLE; -- detect at least one null in rows
```

在某些情況下，寫成 *`row`* `IS DISTINCT FROM NULL` 或 *`row`* `IS NOT DISTINCT FROM NULL` 可能會比較好，它們只會檢查整個資料列值是否為 null，而不會對資料列的欄位進行任何額外的測試。

<a id="id-1.5.8.8.19.1"></a>
<a id="id-1.5.8.8.19.2"></a>
<a id="id-1.5.8.8.19.3"></a>
<a id="id-1.5.8.8.19.4"></a>
<a id="id-1.5.8.8.19.5"></a>
<a id="id-1.5.8.8.19.6"></a>
也可以使用下列述詞來檢驗布林值

```

boolean_expression IS TRUE
boolean_expression IS NOT TRUE
boolean_expression IS FALSE
boolean_expression IS NOT FALSE
boolean_expression IS UNKNOWN
boolean_expression IS NOT UNKNOWN
```

即使運算元為 null，這些述詞也一律會回傳 true 或 false，永遠不會回傳 null 值。null 輸入會被視為邏輯值「未知」。請注意，`IS UNKNOWN` 與 `IS NOT UNKNOWN` 實際上分別與 `IS NULL` 及 `IS NOT NULL` 相同，只是輸入運算式必須是布林型別。

另外還有一些與比較相關的函式，如[表 9.3](functions-comparison.md#FUNCTIONS-COMPARISON-FUNC-TABLE) 所示。

<a id="FUNCTIONS-COMPARISON-FUNC-TABLE"></a>

**表 9.3. 比較函式**

<table border="1" class="table" summary="Comparison Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.8.21.2.2.1.1.1.1"></a>
<code class="function">num_nonnulls</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳非 null 引數的數量。
       </p>
<p>
<code class="literal">num_nonnulls(1, NULL, 2)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.8.21.2.2.2.1.1.1"></a>
<code class="function">num_nulls</code> ( <code class="literal">VARIADIC</code> <code class="type">"any"</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳 null 引數的數量。
       </p>
<p>
<code class="literal">num_nulls(1, NULL, 2)</code>
        → <code class="returnvalue">1</code>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-comparison.html)（原文版本：18.6；核對日期：2026-09-11）
