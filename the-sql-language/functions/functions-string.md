<a id="FUNCTIONS-STRING"></a>

## 9.4. 字串函式與運算子 [#](#FUNCTIONS-STRING)

[9.4.1. `format`](functions-string.md#FUNCTIONS-STRING-FORMAT)

本節說明用於檢查與操作字串值的函式與運算子。在這裡，字串包括 `character`、`character varying` 與 `text` 型別的值。除非另有註明，這些函式與運算子都宣告為接受並回傳 `text` 型別。它們也可以同樣地接受 `character varying` 引數。`character` 型別的值在套用函式或運算子之前，會先被轉換為 `text`，因而會去除 `character` 值中所有的尾端空白。

SQL 定義了一些使用關鍵字而非逗號來分隔引數的字串函式。詳情請見[表 9.9](functions-string.md#FUNCTIONS-STRING-SQL)。PostgreSQL 也提供了這些函式使用一般函式呼叫語法的版本（請參閱[表 9.10](functions-string.md#FUNCTIONS-STRING-OTHER)）。

### 注意

只要至少有一個輸入是字串型別，字串串接運算子（`||`）就會接受非字串的輸入，如[表 9.9](functions-string.md#FUNCTIONS-STRING-SQL) 所示。在其他情況下，可以插入明確轉換為 `text` 的強制轉換，讓非字串輸入被接受。

<a id="FUNCTIONS-STRING-SQL"></a>

**表 9.9. SQL 字串函式與運算子**

<table border="1" class="table" summary="SQL String Functions and Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式／運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.1.1.1.1"></a>
<code class="type">text</code> <code class="literal">||</code> <code class="type">text</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        串接兩個字串。
       </p>
<p>
<code class="literal">'Post' || 'greSQL'</code>
        → <code class="returnvalue">PostgreSQL</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">||</code> <code class="type">anynonarray</code>
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="type">anynonarray</code> <code class="literal">||</code> <code class="type">text</code>
        → <code class="returnvalue">text</code>
</p>
<p>
        將非字串的輸入轉換為文字，然後串接兩個字串。（非字串的輸入不能是陣列型別，因為那會與陣列的 <code class="literal">||</code> 運算子產生歧義。如果你想串接陣列的文字表示，請明確地將它轉換為 <code class="type">text</code>。）
       </p>
<p>
<code class="literal">'Value: ' || 42</code>
        → <code class="returnvalue">Value: 42</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.3.1.1.1"></a>
<code class="function">btrim</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>
        [<span class="optional">, <em class="parameter"><code>characters</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將只由 <em class="parameter"><code>characters</code></em>（預設為空白）中的字元組成的最長字串，從 <em class="parameter"><code>string</code></em> 的開頭與結尾移除。
       </p>
<p>
<code class="literal">btrim('xyxtrimyyx', 'xyz')</code>
        → <code class="returnvalue">trim</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.4.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.10.5.2.2.4.1.1.2"></a>
<code class="type">text</code> <code class="literal">IS</code> [<span class="optional"><code class="literal">NOT</code></span>] [<span class="optional"><em class="parameter"><code>form</code></em></span>] <code class="literal">NORMALIZED</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢查字串是否為指定的 Unicode 正規化形式。選用的 <em class="parameter"><code>form</code></em> 關鍵字指定形式：<code class="literal">NFC</code>（預設值）、<code class="literal">NFD</code>、<code class="literal">NFKC</code> 或 <code class="literal">NFKD</code>。只有在伺服器編碼為 <code class="literal">UTF8</code> 時才能使用這個運算式。請注意，使用這個運算式檢查正規化，通常比對可能已經正規化的字串進行正規化更快。
       </p>
<p>
<code class="literal">U&amp;'\0061\0308bc' IS NFD NORMALIZED</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.5.1.1.1"></a>
<code class="function">bit_length</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳字串中的位元數（<code class="function">octet_length</code> 的 8 倍）。
       </p>
<p>
<code class="literal">bit_length('jose')</code>
        → <code class="returnvalue">32</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.6.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.10.5.2.2.6.1.1.2"></a>
<a class="indexterm" id="id-1.5.8.10.5.2.2.6.1.1.3"></a>
<code class="function">char_length</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.6.1.2.1"></a>
<code class="function">character_length</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳字串中的字元數。
       </p>
<p>
<code class="literal">char_length('josé')</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-LOWER"></a>
<code class="function">lower</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        依照資料庫語系的規則，將字串全部轉換為小寫。
       </p>
<p>
<code class="literal">lower('TOM')</code>
        → <code class="returnvalue">tom</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.8.1.1.1"></a>
<code class="function">lpad</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>length</code></em> <code class="type">integer</code>
        [<span class="optional">, <em class="parameter"><code>fill</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 延伸到長度 <em class="parameter"><code>length</code></em>，方法是在前面加上字元 <em class="parameter"><code>fill</code></em>（預設為空白）。如果 <em class="parameter"><code>string</code></em> 已經比 <em class="parameter"><code>length</code></em> 長，就會將它截斷（從右邊）。
       </p>
<p>
<code class="literal">lpad('hi', 5, 'xy')</code>
        → <code class="returnvalue">xyxhi</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.9.1.1.1"></a>
<code class="function">ltrim</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>
        [<span class="optional">, <em class="parameter"><code>characters</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將只由 <em class="parameter"><code>characters</code></em>（預設為空白）中的字元組成的最長字串，從 <em class="parameter"><code>string</code></em> 的開頭移除。
       </p>
<p>
<code class="literal">ltrim('zzzytest', 'xyz')</code>
        → <code class="returnvalue">test</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-NORMALIZE"></a>
<a class="indexterm" id="id-1.5.8.10.5.2.2.10.1.1.2"></a>
<code class="function">normalize</code> ( <code class="type">text</code>
        [<span class="optional">, <em class="parameter"><code>form</code></em> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將字串轉換為指定的 Unicode 正規化形式。選用的 <em class="parameter"><code>form</code></em> 關鍵字指定形式：<code class="literal">NFC</code>（預設值）、<code class="literal">NFD</code>、<code class="literal">NFKC</code> 或 <code class="literal">NFKD</code>。只有在伺服器編碼為 <code class="literal">UTF8</code> 時才能使用這個函式。
       </p>
<p>
<code class="literal">normalize(U&amp;'\0061\0308bc', NFC)</code>
        → <code class="returnvalue">U&amp;'\00E4bc'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.11.1.1.1"></a>
<code class="function">octet_length</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳字串中的位元組數。
       </p>
<p>
<code class="literal">octet_length('josé')</code> → <code class="returnvalue">5</code>（若伺服器編碼為 UTF8）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.12.1.1.1"></a>
<code class="function">octet_length</code> ( <code class="type">character</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳字串中的位元組數。由於這個版本的函式直接接受 <code class="type">character</code> 型別，它不會去除尾端空白。
       </p>
<p>
<code class="literal">octet_length('abc '::character(4))</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.13.1.1.1"></a>
<code class="function">overlay</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code> <code class="literal">PLACING</code> <em class="parameter"><code>newsubstring</code></em> <code class="type">text</code> <code class="literal">FROM</code> <em class="parameter"><code>start</code></em> <code class="type">integer</code> [<span class="optional"> <code class="literal">FOR</code> <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 中從第 <em class="parameter"><code>start</code></em> 個字元開始、延伸 <em class="parameter"><code>count</code></em> 個字元的子字串，替換為 <em class="parameter"><code>newsubstring</code></em>。如果省略 <em class="parameter"><code>count</code></em>，預設為 <em class="parameter"><code>newsubstring</code></em> 的長度。
       </p>
<p>
<code class="literal">overlay('Txxxxas' placing 'hom' from 2 for 4)</code>
        → <code class="returnvalue">Thomas</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.14.1.1.1"></a>
<code class="function">position</code> ( <em class="parameter"><code>substring</code></em> <code class="type">text</code> <code class="literal">IN</code> <em class="parameter"><code>string</code></em> <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳指定的 <em class="parameter"><code>substring</code></em> 在 <em class="parameter"><code>string</code></em> 中第一次出現的起始索引；如果不存在則回傳零。
       </p>
<p>
<code class="literal">position('om' in 'Thomas')</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.15.1.1.1"></a>
<code class="function">rpad</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>length</code></em> <code class="type">integer</code>
        [<span class="optional">, <em class="parameter"><code>fill</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 延伸到長度 <em class="parameter"><code>length</code></em>，方法是在後面加上字元 <em class="parameter"><code>fill</code></em>（預設為空白）。如果 <em class="parameter"><code>string</code></em> 已經比 <em class="parameter"><code>length</code></em> 長，就會將它截斷。
       </p>
<p>
<code class="literal">rpad('hi', 5, 'xy')</code>
        → <code class="returnvalue">hixyx</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.16.1.1.1"></a>
<code class="function">rtrim</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>characters</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        將只由 <em class="parameter"><code>characters</code></em>（預設為空白）中的字元組成的最長字串，從 <em class="parameter"><code>string</code></em> 的結尾移除。
       </p>
<p>
<code class="literal">rtrim('testxxzx', 'xyz')</code>
        → <code class="returnvalue">test</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.17.1.1.1"></a>
<code class="function">substring</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code> [<span class="optional"> <code class="literal">FROM</code> <em class="parameter"><code>start</code></em> <code class="type">integer</code> </span>] [<span class="optional"> <code class="literal">FOR</code> <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取 <em class="parameter"><code>string</code></em> 的子字串：如果有指定，就從第 <em class="parameter"><code>start</code></em> 個字元開始；如果有指定，就在 <em class="parameter"><code>count</code></em> 個字元之後停止。<em class="parameter"><code>start</code></em> 與 <em class="parameter"><code>count</code></em> 至少要提供其中一個。
       </p>
<p>
<code class="literal">substring('Thomas' from 2 for 3)</code>
        → <code class="returnvalue">hom</code>
</p>
<p>
<code class="literal">substring('Thomas' from 3)</code>
        → <code class="returnvalue">omas</code>
</p>
<p>
<code class="literal">substring('Thomas' for 2)</code>
        → <code class="returnvalue">Th</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">substring</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code> <code class="literal">FROM</code> <em class="parameter"><code>pattern</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取第一個符合 POSIX 正規表示式的子字串；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">substring('Thomas' from '...$')</code>
        → <code class="returnvalue">mas</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">substring</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code> <code class="literal">SIMILAR</code> <em class="parameter"><code>pattern</code></em> <code class="type">text</code> <code class="literal">ESCAPE</code> <em class="parameter"><code>escape</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">substring</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code> <code class="literal">FROM</code> <em class="parameter"><code>pattern</code></em> <code class="type">text</code> <code class="literal">FOR</code> <em class="parameter"><code>escape</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取第一個符合 <acronym class="acronym">SQL</acronym> 正規表示式的子字串；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-SIMILARTO-REGEXP">第 9.7.2 節</a>。第一種形式自 SQL:2003 起即已規定；第二種形式只存在於 SQL:1999，應視為已過時。
       </p>
<p>
<code class="literal">substring('Thomas' similar '%#"o_a#"_' escape '#')</code>
        → <code class="returnvalue">oma</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.20.1.1.1"></a>
<code class="function">trim</code> ( [<span class="optional"> <code class="literal">LEADING</code> | <code class="literal">TRAILING</code> | <code class="literal">BOTH</code> </span>]
        [<span class="optional"> <em class="parameter"><code>characters</code></em> <code class="type">text</code> </span>] <code class="literal">FROM</code>
<em class="parameter"><code>string</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將只由 <em class="parameter"><code>characters</code></em>（預設為空白）中的字元組成的最長字串，從開頭、結尾或兩端（預設為 <code class="literal">BOTH</code>）移除，處理的對象是 <em class="parameter"><code>string</code></em>。
       </p>
<p>
<code class="literal">trim(both 'xyz' from 'yxTomxx')</code>
        → <code class="returnvalue">Tom</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">trim</code> ( [<span class="optional"> <code class="literal">LEADING</code> | <code class="literal">TRAILING</code> | <code class="literal">BOTH</code> </span>] [<span class="optional"> <code class="literal">FROM</code> </span>]
        <em class="parameter"><code>string</code></em> <code class="type">text</code> [<span class="optional">,
        <em class="parameter"><code>characters</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        這是 <code class="function">trim()</code> 的非標準語法。
       </p>
<p>
<code class="literal">trim(both from 'yxTomxx', 'xyz')</code>
        → <code class="returnvalue">Tom</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.22.1.1.1"></a>
<code class="function">unicode_assigned</code> ( <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果字串中的所有字元都是已指派的 Unicode 碼位，就回傳 <code class="literal">true</code>；否則回傳 <code class="literal">false</code>。只有在伺服器編碼為 <code class="literal">UTF8</code> 時才能使用這個函式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.5.2.2.23.1.1.1"></a>
<code class="function">upper</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        依照資料庫語系的規則，將字串全部轉換為大寫。
       </p>
<p>
<code class="literal">upper('tom')</code>
        → <code class="returnvalue">TOM</code>
</p></td></tr></tbody></table>

<br>

另外還有其他字串操作函式與運算子可用，列於[表 9.10](functions-string.md#FUNCTIONS-STRING-OTHER)。（其中有些在內部用來實作[表 9.9](functions-string.md#FUNCTIONS-STRING-SQL) 所列的 SQL 標準字串函式。）此外還有模式比對運算子，說明於[第 9.7 節](functions-matching.md)；以及用於全文檢索的運算子，說明於[第 12 章](../textsearch/README.md)。

<a id="FUNCTIONS-STRING-OTHER"></a>

**表 9.10. 其他字串函式與運算子**

<table border="1" class="table" summary="Other String Functions and Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式／運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.1.1.1.1"></a>
<code class="type">text</code> <code class="literal">^@</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果第一個字串以第二個字串開頭，就回傳 true（等同於 <code class="function">starts_with()</code> 函式）。
       </p>
<p>
<code class="literal">'alphabet' ^@ 'alph'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.2.1.1.1"></a>
<code class="function">ascii</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳引數第一個字元的數值代碼。在 <acronym class="acronym">UTF8</acronym> 編碼中，回傳該字元的 Unicode 碼位。在其他多位元組編碼中，引數必須是 <acronym class="acronym">ASCII</acronym> 字元。
       </p>
<p>
<code class="literal">ascii('x')</code>
        → <code class="returnvalue">120</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.3.1.1.1"></a>
<code class="function">chr</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳具有指定代碼的字元。在 <acronym class="acronym">UTF8</acronym> 編碼中，引數被視為 Unicode 碼位。在其他多位元組編碼中，引數必須指定一個 <acronym class="acronym">ASCII</acronym> 字元。不允許使用 <code class="literal">chr(0)</code>，因為文字資料型別無法儲存該字元。
      </p>
<p>
<code class="literal">chr(65)</code>
        → <code class="returnvalue">A</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.4.1.1.1"></a>
<code class="function">concat</code> ( <em class="parameter"><code>val1</code></em> <code class="type">"any"</code>
         [<span class="optional">, <em class="parameter"><code>val2</code></em> <code class="type">"any"</code> [<span class="optional">, ...</span>] </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        串接所有引數的文字表示。NULL 引數會被忽略。
       </p>
<p>
<code class="literal">concat('abcde', 2, NULL, 22)</code>
        → <code class="returnvalue">abcde222</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.5.1.1.1"></a>
<code class="function">concat_ws</code> ( <em class="parameter"><code>sep</code></em> <code class="type">text</code>,
        <em class="parameter"><code>val1</code></em> <code class="type">"any"</code>
        [<span class="optional">, <em class="parameter"><code>val2</code></em> <code class="type">"any"</code> [<span class="optional">, ...</span>] </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        以分隔符號串接除了第一個引數之外的所有引數。第一個引數用作分隔字串，不應為 NULL。其他的 NULL 引數會被忽略。
       </p>
<p>
<code class="literal">concat_ws(',', 'abcde', 2, NULL, 22)</code>
        → <code class="returnvalue">abcde,2,22</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.6.1.1.1"></a>
<code class="function">format</code> ( <em class="parameter"><code>formatstr</code></em> <code class="type">text</code>
        [<span class="optional">, <em class="parameter"><code>formatarg</code></em> <code class="type">"any"</code> [<span class="optional">, ...</span>] </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
         依照格式字串格式化引數；請參閱<a class="xref" href="functions-string.md#FUNCTIONS-STRING-FORMAT">第 9.4.1 節</a>。這個函式類似於 C 函式 <code class="function">sprintf</code>。
       </p>
<p>
<code class="literal">format('Hello %s, %1$s', 'World')</code>
        → <code class="returnvalue">Hello World, World</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.7.1.1.1"></a>
<code class="function">initcap</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將每個單字的第一個字母轉換為大寫，其餘轉換為小寫。單字是由非英數字元分隔的英數字元序列。
       </p>
<p>
<code class="literal">initcap('hi THOMAS')</code>
        → <code class="returnvalue">Hi Thomas</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.8.1.1.1"></a>
<code class="function">casefold</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        依照定序對輸入字串進行大小寫摺疊（case folding）。大小寫摺疊類似於大小寫轉換，但大小寫摺疊的目的是便於進行不區分大小寫的字串比對，而大小寫轉換的目的則是轉換成特定的大小寫形式。只有在伺服器編碼為 <code class="literal">UTF8</code> 時才能使用這個函式。
       </p>
<p>
        一般而言，大小寫摺疊只是轉換成小寫，但視定序而定可能會有例外。例如，有些字元有兩種以上的小寫變體，或者會摺疊成大寫。
       </p>
<p>
        大小寫摺疊可能會改變字串的長度。例如，在 <code class="literal">PG_UNICODE_FAST</code> 定序中，<code class="literal">ß</code>（U+00DF）會摺疊成 <code class="literal">ss</code>。
       </p>
<p>
<code class="function">casefold</code> 可用於 Unicode 預設無大小寫比對（Default Caseless Matching）。它不一定會保留輸入字串的正規化形式（請參閱 <a class="xref" href="functions-string.md#FUNCTION-NORMALIZE">normalize</a>）。
       </p>
<p>
        <code class="literal">libc</code> 提供者不支援大小寫摺疊，因此 <code class="function">casefold</code> 與 <a class="xref" href="functions-string.md#FUNCTION-LOWER">lower</a> 相同。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.9.1.1.1"></a>
<code class="function">left</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳字串的前 <em class="parameter"><code>n</code></em> 個字元；當 <em class="parameter"><code>n</code></em> 為負數時，回傳除了最後 |<em class="parameter"><code>n</code></em>| 個字元之外的所有字元。
       </p>
<p>
<code class="literal">left('abcde', 2)</code>
        → <code class="returnvalue">ab</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.10.1.1.1"></a>
<code class="function">length</code> ( <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳字串中的字元數。
       </p>
<p>
<code class="literal">length('jose')</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.11.1.1.1"></a>
<code class="function">md5</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        計算引數的 MD5 <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">雜湊值</a>，結果以十六進位表示。
       </p>
<p>
<code class="literal">md5('abc')</code>
        → <code class="returnvalue">900150983cd24fb0​d6963f7d28e17f72</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.12.1.1.1"></a>
<code class="function">parse_ident</code> ( <em class="parameter"><code>qualified_identifier</code></em> <code class="type">text</code>
        [<span class="optional">, <em class="parameter"><code>strict_mode</code></em> <code class="type">boolean</code> <code class="literal">DEFAULT</code> <code class="literal">true</code> </span>] )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <em class="parameter"><code>qualified_identifier</code></em> 拆分成識別符號陣列，並移除個別識別符號的所有引號。預設情況下，最後一個識別符號之後的額外字元會被視為錯誤；但如果第二個參數為 <code class="literal">false</code>，這類額外字元就會被忽略。（這種行為對於剖析函式等物件的名稱很有用。）請注意，這個函式不會截斷過長的識別符號。如果你想要截斷，可以將結果轉換為 <code class="type">name[]</code>。
       </p>
<p>
<code class="literal">parse_ident('"SomeSchema".someTable')</code>
        → <code class="returnvalue">{SomeSchema,sometable}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.13.1.1.1"></a>
<code class="function">pg_client_encoding</code> ( )
        → <code class="returnvalue">name</code>
</p>
<p>
        回傳目前用戶端編碼的名稱。
       </p>
<p>
<code class="literal">pg_client_encoding()</code>
        → <code class="returnvalue">UTF8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.14.1.1.1"></a>
<code class="function">quote_ident</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳適當加上引號、可在 <acronym class="acronym">SQL</acronym> 陳述式字串中用作識別符號的給定字串。只有在必要時（也就是字串包含非識別符號字元，或會被大小寫摺疊時）才會加上引號。內嵌的引號會被正確地重複。另請參閱<a class="xref" href="../../server-programming/plpgsql/plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE">範例 41.1</a>。
       </p>
<p>
<code class="literal">quote_ident('Foo bar')</code>
        → <code class="returnvalue">"Foo bar"</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.15.1.1.1"></a>
<code class="function">quote_literal</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳適當加上引號、可在 <acronym class="acronym">SQL</acronym> 陳述式字串中用作字串字面值的給定字串。內嵌的單引號與反斜線會被正確地重複。請注意，<code class="function">quote_literal</code> 在輸入為 null 時會回傳 null；如果引數可能為 null，<code class="function">quote_nullable</code> 通常更合適。另請參閱<a class="xref" href="../../server-programming/plpgsql/plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE">範例 41.1</a>。
       </p>
<p>
<code class="literal">quote_literal(E'O\'Reilly')</code>
        → <code class="returnvalue">'O''Reilly'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">quote_literal</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將給定的值轉換為文字，然後將它加上引號作為字面值。內嵌的單引號與反斜線會被正確地重複。
       </p>
<p>
<code class="literal">quote_literal(42.5)</code>
        → <code class="returnvalue">'42.5'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.17.1.1.1"></a>
<code class="function">quote_nullable</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳適當加上引號、可在 <acronym class="acronym">SQL</acronym> 陳述式字串中用作字串字面值的給定字串；或者，如果引數為 null，則回傳 <code class="literal">NULL</code>。內嵌的單引號與反斜線會被正確地重複。另請參閱<a class="xref" href="../../server-programming/plpgsql/plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE">範例 41.1</a>。
       </p>
<p>
<code class="literal">quote_nullable(NULL)</code>
        → <code class="returnvalue">NULL</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">quote_nullable</code> ( <code class="type">anyelement</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將給定的值轉換為文字，然後將它加上引號作為字面值；或者，如果引數為 null，則回傳 <code class="literal">NULL</code>。內嵌的單引號與反斜線會被正確地重複。
       </p>
<p>
<code class="literal">quote_nullable(42.5)</code>
        → <code class="returnvalue">'42.5'</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.19.1.1.1"></a>
<code class="function">regexp_count</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>start</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] </span>] )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 在 <em class="parameter"><code>string</code></em> 中相符的次數；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_count('123456789012', '\d\d\d', 2)</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.20.1.1.1"></a>
<code class="function">regexp_instr</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>start</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>N</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>endoption</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>subexpr</code></em> <code class="type">integer</code> </span>] </span>] </span>] </span>] </span>] )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳在 <em class="parameter"><code>string</code></em> 中第 <em class="parameter"><code>N</code></em> 次與 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 相符之處的位置；如果沒有這樣的相符則回傳零；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_instr('ABCDEF', 'c(.)(..)', 1, 1, 0, 'i')</code>
        → <code class="returnvalue">3</code>
</p>
<p>
<code class="literal">regexp_instr('ABCDEF', 'c(.)(..)', 1, 1, 0, 'i', 2)</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.21.1.1.1"></a>
<code class="function">regexp_like</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢查 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 是否在 <em class="parameter"><code>string</code></em> 中有相符的項目；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_like('Hello World', 'world$', 'i')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.22.1.1.1"></a>
<code class="function">regexp_match</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        回傳 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 與 <em class="parameter"><code>string</code></em> 第一次相符之內的子字串；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_match('foobarbequebaz', '(bar)(beque)')</code>
        → <code class="returnvalue">{bar,beque}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.23.1.1.1"></a>
<code class="function">regexp_matches</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">setof text[]</code>
</p>
<p>
        回傳 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 與 <em class="parameter"><code>string</code></em> 第一次相符之內的子字串；如果使用了 <code class="literal">g</code> 旗標，則回傳所有這類相符之內的子字串；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_matches('foobarbequebaz', 'ba.', 'g')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 {bar}
 {baz}
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.24.1.1.1"></a>
<code class="function">regexp_replace</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code>, <em class="parameter"><code>replacement</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        替換與 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 第一次相符的子字串；如果使用了 <code class="literal">g</code> 旗標，則替換所有這類相符；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_replace('Thomas', '.[mN]a.', 'M')</code>
        → <code class="returnvalue">ThM</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">regexp_replace</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code>, <em class="parameter"><code>replacement</code></em> <code class="type">text</code>,
         <em class="parameter"><code>start</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>N</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        替換第 <em class="parameter"><code>N</code></em> 次與 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 相符的子字串；如果 <em class="parameter"><code>N</code></em> 為零，則替換所有這類相符；並從第 <em class="parameter"><code>start</code></em> 個字元開始搜尋 <em class="parameter"><code>string</code></em>。如果省略 <em class="parameter"><code>N</code></em>，預設為 1。請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_replace('Thomas', '.', 'X', 3, 2)</code>
        → <code class="returnvalue">ThoXas</code>
</p>
<p>
<code class="literal">regexp_replace(string=&gt;'hello world', pattern=&gt;'l', replacement=&gt;'XX', start=&gt;1, "N"=&gt;2)</code>
        → <code class="returnvalue">helXXo world</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.26.1.1.1"></a>
<code class="function">regexp_split_to_array</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        使用 POSIX 正規表示式作為分隔符號來拆分 <em class="parameter"><code>string</code></em>，產生一個結果陣列；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_split_to_array('hello world', '\s+')</code>
        → <code class="returnvalue">{hello,world}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.27.1.1.1"></a>
<code class="function">regexp_split_to_table</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        使用 POSIX 正規表示式作為分隔符號來拆分 <em class="parameter"><code>string</code></em>，產生一個結果集合；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_split_to_table('hello world', '\s+')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 hello
 world
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.28.1.1.1"></a>
<code class="function">regexp_substr</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>pattern</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>start</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>N</code></em> <code class="type">integer</code>
         [<span class="optional">, <em class="parameter"><code>flags</code></em> <code class="type">text</code>
         [<span class="optional">, <em class="parameter"><code>subexpr</code></em> <code class="type">integer</code> </span>] </span>] </span>] </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳 <em class="parameter"><code>string</code></em> 中第 <em class="parameter"><code>N</code></em> 個與 POSIX 正規表示式 <em class="parameter"><code>pattern</code></em> 相符的子字串；如果沒有這樣的相符，則回傳 <code class="literal">NULL</code>；請參閱<a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP">第 9.7.3 節</a>。
       </p>
<p>
<code class="literal">regexp_substr('ABCDEF', 'c(.)(..)', 1, 1, 'i')</code>
        → <code class="returnvalue">CDEF</code>
</p>
<p>
<code class="literal">regexp_substr('ABCDEF', 'c(.)(..)', 1, 1, 'i', 2)</code>
        → <code class="returnvalue">EF</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.29.1.1.1"></a>
<code class="function">repeat</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>number</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 重複指定的 <em class="parameter"><code>number</code></em> 次。
       </p>
<p>
<code class="literal">repeat('Pg', 4)</code>
        → <code class="returnvalue">PgPgPgPg</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.30.1.1.1"></a>
<code class="function">replace</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>from</code></em> <code class="type">text</code>,
        <em class="parameter"><code>to</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 中所有出現的子字串 <em class="parameter"><code>from</code></em> 替換為子字串 <em class="parameter"><code>to</code></em>。
       </p>
<p>
<code class="literal">replace('abcdefabcdef', 'cd', 'XX')</code>
        → <code class="returnvalue">abXXefabXXef</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.31.1.1.1"></a>
<code class="function">reverse</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        反轉字串中字元的順序。
       </p>
<p>
<code class="literal">reverse('abcde')</code>
        → <code class="returnvalue">edcba</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.32.1.1.1"></a>
<code class="function">right</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
         <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        回傳字串的最後 <em class="parameter"><code>n</code></em> 個字元；當 <em class="parameter"><code>n</code></em> 為負數時，回傳除了最前面 |<em class="parameter"><code>n</code></em>| 個字元之外的所有字元。
       </p>
<p>
<code class="literal">right('abcde', 2)</code>
        → <code class="returnvalue">de</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.33.1.1.1"></a>
<code class="function">split_part</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>delimiter</code></em> <code class="type">text</code>,
        <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 在 <em class="parameter"><code>delimiter</code></em> 出現的位置拆分，並回傳第 <em class="parameter"><code>n</code></em> 個欄位（從一開始計算）；當 <em class="parameter"><code>n</code></em> 為負數時，回傳倒數第 |<em class="parameter"><code>n</code></em>| 個欄位。
       </p>
<p>
<code class="literal">split_part('abc~@~def~@~ghi', '~@~', 2)</code>
        → <code class="returnvalue">def</code>
</p>
<p>
<code class="literal">split_part('abc,def,ghi,jkl', ',', -2)</code>
        → <code class="returnvalue">ghi</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.34.1.1.1"></a>
<code class="function">starts_with</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>prefix</code></em> <code class="type">text</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        如果 <em class="parameter"><code>string</code></em> 以 <em class="parameter"><code>prefix</code></em> 開頭，就回傳 true。
       </p>
<p>
<code class="literal">starts_with('alphabet', 'alph')</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-STRING-TO-ARRAY"></a>
<code class="function">string_to_array</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>delimiter</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>null_string</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">text[]</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 在 <em class="parameter"><code>delimiter</code></em> 出現的位置拆分，並將產生的欄位組成一個 <code class="type">text</code> 陣列。如果 <em class="parameter"><code>delimiter</code></em> 為 <code class="literal">NULL</code>，<em class="parameter"><code>string</code></em> 中的每個字元都會成為陣列中的一個獨立元素。如果 <em class="parameter"><code>delimiter</code></em> 是空字串，<em class="parameter"><code>string</code></em> 會被視為單一欄位。如果提供了 <em class="parameter"><code>null_string</code></em> 且其值不是 <code class="literal">NULL</code>，與該字串相符的欄位會被替換為 <code class="literal">NULL</code>。另請參閱 <a class="link" href="functions-array.md#FUNCTION-ARRAY-TO-STRING"><code class="function">array_to_string</code></a>。
       </p>
<p>
<code class="literal">string_to_array('xx~~yy~~zz', '~~', 'yy')</code>
        → <code class="returnvalue">{xx,NULL,zz}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.36.1.1.1"></a>
<code class="function">string_to_table</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>delimiter</code></em> <code class="type">text</code> [<span class="optional">, <em class="parameter"><code>null_string</code></em> <code class="type">text</code> </span>] )
        → <code class="returnvalue">setof text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 在 <em class="parameter"><code>delimiter</code></em> 出現的位置拆分，並將產生的欄位以一組 <code class="type">text</code> 資料列的形式回傳。如果 <em class="parameter"><code>delimiter</code></em> 為 <code class="literal">NULL</code>，<em class="parameter"><code>string</code></em> 中的每個字元都會成為結果中的一筆獨立資料列。如果 <em class="parameter"><code>delimiter</code></em> 是空字串，<em class="parameter"><code>string</code></em> 會被視為單一欄位。如果提供了 <em class="parameter"><code>null_string</code></em> 且其值不是 <code class="literal">NULL</code>，與該字串相符的欄位會被替換為 <code class="literal">NULL</code>。
       </p>
<p>
<code class="literal">string_to_table('xx~^~yy~^~zz', '~^~', 'yy')</code>
        → <code class="returnvalue"></code>
</p><pre class="programlisting">
 xx
 NULL
 zz
</pre><p>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.37.1.1.1"></a>
<code class="function">strpos</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>substring</code></em> <code class="type">text</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳指定的 <em class="parameter"><code>substring</code></em> 在 <em class="parameter"><code>string</code></em> 中第一次出現的起始索引；如果不存在則回傳零。（與 <code class="literal">position(<em class="parameter"><code>substring</code></em> in <em class="parameter"><code>string</code></em>)</code> 相同，但請注意引數順序相反。）
       </p>
<p>
<code class="literal">strpos('high', 'ig')</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.38.1.1.1"></a>
<code class="function">substr</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code> [<span class="optional">, <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">text</code>
</p>
<p>
        擷取 <em class="parameter"><code>string</code></em> 從第 <em class="parameter"><code>start</code></em> 個字元開始的子字串；如果有指定，則延伸 <em class="parameter"><code>count</code></em> 個字元。（與 <code class="literal">substring(<em class="parameter"><code>string</code></em> from <em class="parameter"><code>start</code></em> for <em class="parameter"><code>count</code></em>)</code> 相同。）
       </p>
<p>
<code class="literal">substr('alphabet', 3)</code>
        → <code class="returnvalue">phabet</code>
</p>
<p>
<code class="literal">substr('alphabet', 3, 2)</code>
        → <code class="returnvalue">ph</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.39.1.1.1"></a>
<code class="function">to_ascii</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">to_ascii</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>encoding</code></em> <code class="type">name</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">to_ascii</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>encoding</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 從另一種編碼轉換為 <acronym class="acronym">ASCII</acronym>，來源編碼可以用名稱或編號指定。如果省略 <em class="parameter"><code>encoding</code></em>，則假設為資料庫編碼（實務上這是唯一有用的情況）。轉換主要是去除重音符號。只支援從 <code class="literal">LATIN1</code>、<code class="literal">LATIN2</code>、<code class="literal">LATIN9</code> 與 <code class="literal">WIN1250</code> 編碼進行轉換。（另一個更有彈性的解決方案，請參閱 <a class="xref" href="../../appendixes/contrib/unaccent.md">unaccent</a> 模組。）
       </p>
<p>
<code class="literal">to_ascii('Karél')</code>
        → <code class="returnvalue">Karel</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.40.1.1.1"></a>
<code class="function">to_bin</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">to_bin</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將數字轉換為其等價的二補數二進位表示。
       </p>
<p>
<code class="literal">to_bin(2147483647)</code>
        → <code class="returnvalue">1111111111111111111111111111111</code>
</p>
<p>
<code class="literal">to_bin(-1234)</code>
        → <code class="returnvalue">11111111111111111111101100101110</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.41.1.1.1"></a>
<code class="function">to_hex</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">to_hex</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將數字轉換為其等價的二補數十六進位表示。
       </p>
<p>
<code class="literal">to_hex(2147483647)</code>
        → <code class="returnvalue">7fffffff</code>
</p>
<p>
<code class="literal">to_hex(-1234)</code>
        → <code class="returnvalue">fffffb2e</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.42.1.1.1"></a>
<code class="function">to_oct</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">text</code>
</p>
<p class="func_signature">
<code class="function">to_oct</code> ( <code class="type">bigint</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將數字轉換為其等價的二補數八進位表示。
       </p>
<p>
<code class="literal">to_oct(2147483647)</code>
        → <code class="returnvalue">17777777777</code>
</p>
<p>
<code class="literal">to_oct(-1234)</code>
        → <code class="returnvalue">37777775456</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.43.1.1.1"></a>
<code class="function">translate</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
        <em class="parameter"><code>from</code></em> <code class="type">text</code>,
        <em class="parameter"><code>to</code></em> <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <em class="parameter"><code>string</code></em> 中與 <em class="parameter"><code>from</code></em> 集合中某個字元相符的每個字元，替換為 <em class="parameter"><code>to</code></em> 集合中的對應字元。如果 <em class="parameter"><code>from</code></em> 比 <em class="parameter"><code>to</code></em> 長，<em class="parameter"><code>from</code></em> 中多出來的字元出現時會被刪除。
       </p>
<p>
<code class="literal">translate('12345', '143', 'ax')</code>
        → <code class="returnvalue">a2x5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.10.7.2.2.44.1.1.1"></a>
<code class="function">unistr</code> ( <code class="type">text</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        計算引數中跳脫的 Unicode 字元。Unicode 字元可以指定為 <code class="literal">\<em class="replaceable"><code>XXXX</code></em></code>（4 個十六進位數字）、<code class="literal">\+<em class="replaceable"><code>XXXXXX</code></em></code>（6 個十六進位數字）、<code class="literal">\u<em class="replaceable"><code>XXXX</code></em></code>（4 個十六進位數字）或 <code class="literal">\U<em class="replaceable"><code>XXXXXXXX</code></em></code>（8 個十六進位數字）。要指定反斜線，請寫兩個反斜線。所有其他字元都按字面解讀。
       </p>
<p>
        如果伺服器編碼不是 UTF-8，由這些跳脫序列之一所識別的 Unicode 碼位，會被轉換為實際的伺服器編碼；如果無法轉換，就會回報錯誤。
       </p>
<p>
        這個函式提供了一種（非標準的）替代方式，用來取代使用 Unicode 跳脫的字串常數（請參閱<a class="xref" href="../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-UESCAPE">第 4.1.2.3 節</a>）。
       </p>
<p>
<code class="literal">unistr('d\0061t\+000061')</code>
        → <code class="returnvalue">data</code>
</p>
<p>
<code class="literal">unistr('d\u0061t\U00000061')</code>
        → <code class="returnvalue">data</code>
</p></td></tr></tbody></table>

<br>

`concat`、`concat_ws` 與 `format` 函式是可變參數（variadic）函式，因此可以將要串接或格式化的值，以標有 `VARIADIC` 關鍵字的陣列形式傳入（請參閱[第 36.5.6 節](../../server-programming/extend/xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS)）。陣列的元素會被視為函式的個別一般引數。如果可變參數陣列引數為 NULL，`concat` 與 `concat_ws` 會回傳 NULL，但 `format` 會將 NULL 視為零個元素的陣列。

另請參閱[第 9.21 節](functions-aggregate.md)中的彙總函式 `string_agg`，以及[表 9.13](functions-binarystring.md#FUNCTIONS-BINARYSTRING-CONVERSIONS) 中用於在字串與 `bytea` 型別之間轉換的函式。

<a id="FUNCTIONS-STRING-FORMAT"></a>

### 9.4.1. `format` [#](#FUNCTIONS-STRING-FORMAT)

<a id="id-1.5.8.10.10.2"></a>

函式 `format` 會依照格式字串產生格式化的輸出，其風格類似於 C 函式 `sprintf`。

```

format(formatstr text [, formatarg "any" [, ...] ])
```

*`formatstr`* 是指定結果應如何格式化的格式字串。格式字串中的文字會直接複製到結果中，但使用*格式規範*（format specifier）的地方除外。格式規範在字串中扮演預留位置的角色，定義後續的函式引數應該如何格式化並插入結果中。每個 *`formatarg`* 引數都會依照其資料型別的一般輸出規則轉換為文字，然後依照格式規範進行格式化並插入結果字串中。

格式規範以 `%` 字元開頭，其形式為

```

%[position][flags][width]type
```

其中各組成欄位為：

*`position`*（選用）
:   形式為 `n$` 的字串，其中 *`n`* 是要印出之引數的索引。索引 1 表示 *`formatstr`* 之後的第一個引數。如果省略 *`position`*，預設會依序使用下一個引數。

*`flags`*（選用）
:   控制格式規範之輸出如何格式化的額外選項。目前唯一支援的旗標是減號（`-`），它會使格式規範的輸出靠左對齊。除非也指定了 *`width`* 欄位，否則它沒有任何作用。

*`width`*（選用）
:   指定用來顯示格式規範輸出的*最少*字元數。輸出會視需要在左側或右側（取決於 `-` 旗標）以空白填補，以填滿該寬度。寬度太小並不會截斷輸出，只會被忽略。寬度可以用下列任一方式指定：正整數；星號（`*`），表示使用下一個函式引數作為寬度；或形式為 `*n$` 的字串，表示使用第 *`n`* 個函式引數作為寬度。

    如果寬度來自函式引數，該引數會在用於格式規範之值的引數之前被取用。如果寬度引數為負數，結果會在長度為 `abs`(*`width`*) 的欄位內靠左對齊（就好像指定了 `-` 旗標一樣）。

*`type`*（必要）
:   用來產生格式規範輸出的格式轉換類型。支援下列類型：

    * `s` 將引數值格式化為簡單的字串。null 值會被視為空字串。
    * `I` 將引數值視為 SQL 識別符號，必要時會為它加上雙引號。值為 null 是錯誤（等同於 `quote_ident`）。
    * `L` 將引數值加上引號，作為 SQL 字面值。null 值會顯示為不加引號的字串 `NULL`（等同於 `quote_nullable`）。

除了上述的格式規範之外，也可以使用特殊序列 `%%` 來輸出字面的 `%` 字元。

以下是一些基本格式轉換的範例：

```

SELECT format('Hello %s', 'World');
Result: Hello World

SELECT format('Testing %s, %s, %s, %%', 'one', 'two', 'three');
Result: Testing one, two, three, %

SELECT format('INSERT INTO %I VALUES(%L)', 'Foo bar', E'O\'Reilly');
Result: INSERT INTO "Foo bar" VALUES('O''Reilly')

SELECT format('INSERT INTO %I VALUES(%L)', 'locations', 'C:\Program Files');
Result: INSERT INTO locations VALUES('C:\Program Files')
```

以下是使用 *`width`* 欄位與 `-` 旗標的範例：

```

SELECT format('|%10s|', 'foo');
Result: |       foo|

SELECT format('|%-10s|', 'foo');
Result: |foo       |

SELECT format('|%*s|', 10, 'foo');
Result: |       foo|

SELECT format('|%*s|', -10, 'foo');
Result: |foo       |

SELECT format('|%-*s|', 10, 'foo');
Result: |foo       |

SELECT format('|%-*s|', -10, 'foo');
Result: |foo       |
```

下面這些範例展示了 *`position`* 欄位的用法：

```

SELECT format('Testing %3$s, %2$s, %1$s', 'one', 'two', 'three');
Result: Testing three, two, one

SELECT format('|%*2$s|', 'foo', 10, 'bar');
Result: |       bar|

SELECT format('|%1$*2$s|', 'foo', 10, 'bar');
Result: |       foo|
```

與標準 C 函式 `sprintf` 不同，PostgreSQL 的 `format` 函式允許在同一個格式字串中混用有與沒有 *`position`* 欄位的格式規範。沒有 *`position`* 欄位的格式規範，一律會使用最後一個被取用之引數的下一個引數。此外，`format` 函式並不要求格式字串中用到所有的函式引數。例如：

```

SELECT format('Testing %3$s, %2$s, %s', 'one', 'two', 'three');
Result: Testing three, two, three
```

`%I` 與 `%L` 格式規範對於安全地建構動態 SQL 陳述式特別有用。請參閱[範例 41.1](../../server-programming/plpgsql/plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-string.html)（原文版本：18.6；核對日期：2026-09-11）
