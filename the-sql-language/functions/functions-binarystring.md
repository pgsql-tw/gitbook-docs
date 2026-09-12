<a id="FUNCTIONS-BINARYSTRING"></a>

## 9.5. 二進位字串函式與運算子 [#](#FUNCTIONS-BINARYSTRING)

<a id="id-1.5.8.11.2"></a>

本節說明用於檢查與操作二進位字串（也就是 `bytea` 型別的值）的函式與運算子。其中許多函式在用途與語法上，都等同於前一節所說明的文字字串函式。

SQL 定義了一些使用關鍵字而非逗號來分隔引數的字串函式。詳情請見[表 9.11](functions-binarystring.md#FUNCTIONS-BINARYSTRING-SQL)。PostgreSQL 也提供了這些函式使用一般函式呼叫語法的版本（請參閱[表 9.12](functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER)）。

<a id="FUNCTIONS-BINARYSTRING-SQL"></a>

**表 9.11. SQL 二進位字串函式與運算子**

<table border="1" class="table" summary="SQL Binary String Functions and Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式／運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.1.1.1.1"></a>
<code class="type">bytea</code> <code class="literal">||</code> <code class="type">bytea</code>
        → <code class="returnvalue">bytea</code>
</p>
<p>
        串接兩個二進位字串。
       </p>
<p>
<code class="literal">'\x123456'::bytea || '\x789a00bcde'::bytea</code>
        → <code class="returnvalue">\x123456789a00bcde</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.2.1.1.1"></a>
<code class="function">bit_length</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳二進位字串中的位元數（<code class="function">octet_length</code> 的 8 倍）。
       </p>
<p>
<code class="literal">bit_length('\x123456'::bytea)</code>
        → <code class="returnvalue">24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.3.1.1.1"></a>
<code class="function">btrim</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
        <em class="parameter"><code>bytesremoved</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        將只由 <em class="parameter"><code>bytesremoved</code></em> 中出現之位元組組成的最長字串，從 <em class="parameter"><code>bytes</code></em> 的開頭與結尾移除。
       </p>
<p>
<code class="literal">btrim('\x1234567890'::bytea, '\x9012'::bytea)</code>
        → <code class="returnvalue">\x345678</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.4.1.1.1"></a>
<code class="function">ltrim</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
         <em class="parameter"><code>bytesremoved</code></em> <code class="type">bytea</code> )
         → <code class="returnvalue">bytea</code>
</p>
<p>
         將只由 <em class="parameter"><code>bytesremoved</code></em> 中出現之位元組組成的最長字串，從 <em class="parameter"><code>bytes</code></em> 的開頭移除。
        </p>
<p>
<code class="literal">ltrim('\x1234567890'::bytea, '\x9012'::bytea)</code>
         → <code class="returnvalue">\x34567890</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.5.1.1.1"></a>
<code class="function">octet_length</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳二進位字串中的位元組數。
       </p>
<p>
<code class="literal">octet_length('\x123456'::bytea)</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.6.1.1.1"></a>
<code class="function">overlay</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code> <code class="literal">PLACING</code> <em class="parameter"><code>newsubstring</code></em> <code class="type">bytea</code> <code class="literal">FROM</code> <em class="parameter"><code>start</code></em> <code class="type">integer</code> [<span class="optional"> <code class="literal">FOR</code> <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        將 <em class="parameter"><code>bytes</code></em> 中從第 <em class="parameter"><code>start</code></em> 個位元組開始、延伸 <em class="parameter"><code>count</code></em> 個位元組的子字串，替換為 <em class="parameter"><code>newsubstring</code></em>。如果省略 <em class="parameter"><code>count</code></em>，預設為 <em class="parameter"><code>newsubstring</code></em> 的長度。
       </p>
<p>
<code class="literal">overlay('\x1234567890'::bytea placing '\002\003'::bytea from 2 for 3)</code>
        → <code class="returnvalue">\x12020390</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.7.1.1.1"></a>
<code class="function">position</code> ( <em class="parameter"><code>substring</code></em> <code class="type">bytea</code> <code class="literal">IN</code> <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳指定的 <em class="parameter"><code>substring</code></em> 在 <em class="parameter"><code>bytes</code></em> 中第一次出現的起始索引；如果不存在則回傳零。
       </p>
<p>
<code class="literal">position('\x5678'::bytea in '\x1234567890'::bytea)</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.8.1.1.1"></a>
<code class="function">rtrim</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
         <em class="parameter"><code>bytesremoved</code></em> <code class="type">bytea</code> )
         → <code class="returnvalue">bytea</code>
</p>
<p>
         將只由 <em class="parameter"><code>bytesremoved</code></em> 中出現之位元組組成的最長字串，從 <em class="parameter"><code>bytes</code></em> 的結尾移除。
        </p>
<p>
<code class="literal">rtrim('\x1234567890'::bytea, '\x9012'::bytea)</code>
         → <code class="returnvalue">\x12345678</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.9.1.1.1"></a>
<code class="function">substring</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code> [<span class="optional"> <code class="literal">FROM</code> <em class="parameter"><code>start</code></em> <code class="type">integer</code> </span>] [<span class="optional"> <code class="literal">FOR</code> <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        擷取 <em class="parameter"><code>bytes</code></em> 的子字串：如果有指定，就從第 <em class="parameter"><code>start</code></em> 個位元組開始；如果有指定，就在 <em class="parameter"><code>count</code></em> 個位元組之後停止。<em class="parameter"><code>start</code></em> 與 <em class="parameter"><code>count</code></em> 至少要提供其中一個。
       </p>
<p>
<code class="literal">substring('\x1234567890'::bytea from 3 for 2)</code>
        → <code class="returnvalue">\x5678</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.5.2.2.10.1.1.1"></a>
<code class="function">trim</code> ( [<span class="optional"> <code class="literal">LEADING</code> | <code class="literal">TRAILING</code> | <code class="literal">BOTH</code> </span>]
        <em class="parameter"><code>bytesremoved</code></em> <code class="type">bytea</code> <code class="literal">FROM</code>
<em class="parameter"><code>bytes</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        將只由 <em class="parameter"><code>bytesremoved</code></em> 中出現之位元組組成的最長字串，從開頭、結尾或兩端（預設為 <code class="literal">BOTH</code>）移除，處理的對象是 <em class="parameter"><code>bytes</code></em>。
       </p>
<p>
<code class="literal">trim('\x9012'::bytea from '\x1234567890'::bytea)</code>
        → <code class="returnvalue">\x345678</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">trim</code> ( [<span class="optional"> <code class="literal">LEADING</code> | <code class="literal">TRAILING</code> | <code class="literal">BOTH</code> </span>] [<span class="optional"> <code class="literal">FROM</code> </span>]
        <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
        <em class="parameter"><code>bytesremoved</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        這是 <code class="function">trim()</code> 的非標準語法。
       </p>
<p>
<code class="literal">trim(both from '\x1234567890'::bytea, '\x9012'::bytea)</code>
        → <code class="returnvalue">\x345678</code>
</p></td></tr></tbody></table>

<br>

另外還有其他二進位字串操作函式可用，列於[表 9.12](functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER)。其中有些在內部用來實作[表 9.11](functions-binarystring.md#FUNCTIONS-BINARYSTRING-SQL) 所列的 SQL 標準字串函式。

<a id="FUNCTIONS-BINARYSTRING-OTHER"></a>

**表 9.12. 其他二進位字串函式**

<table border="1" class="table" summary="Other Binary String Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.1.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.11.7.2.2.1.1.1.2"></a>
<code class="function">bit_count</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳二進位字串中被設定的位元數（也稱為 <span class="quote">“<span class="quote">popcount</span>”</span>）。
       </p>
<p>
<code class="literal">bit_count('\x1234567890'::bytea)</code>
        → <code class="returnvalue">15</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.2.1.1.1"></a>
<code class="function">crc32</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算二進位字串的 CRC-32 值。
       </p>
<p>
<code class="literal">crc32('abc'::bytea)</code>
        → <code class="returnvalue">891568578</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.3.1.1.1"></a>
<code class="function">crc32c</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算二進位字串的 CRC-32C 值。
       </p>
<p>
<code class="literal">crc32c('abc'::bytea)</code>
        → <code class="returnvalue">910901175</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.4.1.1.1"></a>
<code class="function">get_bit</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
        <em class="parameter"><code>n</code></em> <code class="type">bigint</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        從二進位字串中擷取<a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">第 n 個</a>位元。
       </p>
<p>
<code class="literal">get_bit('\x1234567890'::bytea, 30)</code>
        → <code class="returnvalue">1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.5.1.1.1"></a>
<code class="function">get_byte</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
        <em class="parameter"><code>n</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        從二進位字串中擷取<a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">第 n 個</a>位元組。
       </p>
<p>
<code class="literal">get_byte('\x1234567890'::bytea, 4)</code>
        → <code class="returnvalue">144</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.6.1.1.1"></a>
<a class="indexterm" id="id-1.5.8.11.7.2.2.6.1.1.2"></a>
<a class="indexterm" id="id-1.5.8.11.7.2.2.6.1.1.3"></a>
<code class="function">length</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳二進位字串中的位元組數。
       </p>
<p>
<code class="literal">length('\x1234567890'::bytea)</code>
        → <code class="returnvalue">5</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">length</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
        <em class="parameter"><code>encoding</code></em> <code class="type">name</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        假設二進位字串是以給定 <em class="parameter"><code>encoding</code></em> 編碼的文字，回傳其中的字元數。
       </p>
<p>
<code class="literal">length('jose'::bytea, 'UTF8')</code>
        → <code class="returnvalue">4</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.8.1.1.1"></a>
<code class="function">md5</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        計算二進位字串的 MD5 <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">雜湊值</a>，結果以十六進位表示。
       </p>
<p>
<code class="literal">md5('Th\000omas'::bytea)</code>
        → <code class="returnvalue">8ab2d3c9689aaf18​b4958c334c82d8b1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.9.1.1.1"></a>
<code class="function">reverse</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        反轉二進位字串中位元組的順序。
       </p>
<p>
<code class="literal">reverse('\xabcd'::bytea)</code>
        → <code class="returnvalue">\xcdab</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.10.1.1.1"></a>
<code class="function">set_bit</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
        <em class="parameter"><code>n</code></em> <code class="type">bigint</code>,
        <em class="parameter"><code>newvalue</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        將二進位字串中的<a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">第 n 個</a>位元設為 <em class="parameter"><code>newvalue</code></em>。
       </p>
<p>
<code class="literal">set_bit('\x1234567890'::bytea, 30, 0)</code>
        → <code class="returnvalue">\x1234563890</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.11.1.1.1"></a>
<code class="function">set_byte</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
        <em class="parameter"><code>n</code></em> <code class="type">integer</code>,
        <em class="parameter"><code>newvalue</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        將二進位字串中的<a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">第 n 個</a>位元組設為 <em class="parameter"><code>newvalue</code></em>。
       </p>
<p>
<code class="literal">set_byte('\x1234567890'::bytea, 4, 64)</code>
        → <code class="returnvalue">\x1234567840</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.12.1.1.1"></a>
<code class="function">sha224</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        計算二進位字串的 SHA-224 <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">雜湊值</a>。
       </p>
<p>
<code class="literal">sha224('abc'::bytea)</code>
        → <code class="returnvalue">\x23097d223405d8228642a477bda2​55b32aadbce4bda0b3f7e36c9da7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.13.1.1.1"></a>
<code class="function">sha256</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        計算二進位字串的 SHA-256 <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">雜湊值</a>。
       </p>
<p>
<code class="literal">sha256('abc'::bytea)</code>
        → <code class="returnvalue">\xba7816bf8f01cfea414140de5dae2223​b00361a396177a9cb410ff61f20015ad</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.14.1.1.1"></a>
<code class="function">sha384</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        計算二進位字串的 SHA-384 <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">雜湊值</a>。
       </p>
<p>
<code class="literal">sha384('abc'::bytea)</code>
        → <code class="returnvalue">\xcb00753f45a35e8bb5a03d699ac65007​272c32ab0eded1631a8b605a43ff5bed​8086072ba1e7cc2358baeca134c825a7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.15.1.1.1"></a>
<code class="function">sha512</code> ( <code class="type">bytea</code> )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        計算二進位字串的 SHA-512 <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">雜湊值</a>。
       </p>
<p>
<code class="literal">sha512('abc'::bytea)</code>
        → <code class="returnvalue">\xddaf35a193617abacc417349ae204131​12e6fa4e89a97ea20a9eeee64b55d39a​2192992a274fc1a836ba3c23a3feebbd​454d4423643ce80e2a9ac94fa54ca49f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.7.2.2.16.1.1.1"></a>
<code class="function">substr</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code> [<span class="optional">, <em class="parameter"><code>count</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        擷取 <em class="parameter"><code>bytes</code></em> 從第 <em class="parameter"><code>start</code></em> 個位元組開始的子字串；如果有指定，則延伸 <em class="parameter"><code>count</code></em> 個位元組。（與 <code class="literal">substring(<em class="parameter"><code>bytes</code></em> from <em class="parameter"><code>start</code></em> for <em class="parameter"><code>count</code></em>)</code> 相同。）
       </p>
<p>
<code class="literal">substr('\x1234567890'::bytea, 3, 2)</code>
        → <code class="returnvalue">\x5678</code>
</p></td></tr></tbody></table>

<br><a id="FUNCTIONS-ZEROBASED-NOTE"></a>

函式 `get_byte` 與 `set_byte` 將二進位字串的第一個位元組編號為第 0 個位元組。函式 `get_bit` 與 `set_bit` 在每個位元組內從右邊開始為位元編號；例如，第 0 個位元是第一個位元組的最低有效位元，而第 15 個位元是第二個位元組的最高有效位元。

<a id="FUNCTIONS-HASH-NOTE"></a>

基於歷史原因，函式 `md5` 回傳的是以十六進位編碼的 `text` 型別值，而 SHA-2 函式回傳的則是 `bytea` 型別。請使用函式 [`encode`](functions-binarystring.md#FUNCTION-ENCODE) 與 [`decode`](functions-binarystring.md#FUNCTION-DECODE) 在兩者之間轉換。例如，寫成 `encode(sha256('abc'), 'hex')` 可以得到十六進位編碼的文字表示，寫成 `decode(md5('abc'), 'hex')` 則可以得到 `bytea` 值。

<a id="id-1.5.8.11.10.1"></a>
<a id="id-1.5.8.11.10.2"></a>
用於在不同字元集（編碼）之間轉換字串，以及以文字形式表示任意二進位資料的函式，列於[表 9.13](functions-binarystring.md#FUNCTIONS-BINARYSTRING-CONVERSIONS)。對於這些函式，`text` 型別的引數或結果是以資料庫的預設編碼表示，而 `bytea` 型別的引數或結果則是以另一個引數所指定的編碼表示。

<a id="FUNCTIONS-BINARYSTRING-CONVERSIONS"></a>

**表 9.13. 文字／二進位字串轉換函式**

<table border="1" class="table" summary="Text/Binary String Conversion Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
       函式
      </p>
<p>
       說明
      </p>
<p>
       範例
      </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.11.2.2.1.1.1.1"></a>
<code class="function">convert</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
       <em class="parameter"><code>src_encoding</code></em> <code class="type">name</code>,
       <em class="parameter"><code>dest_encoding</code></em> <code class="type">name</code> )
       → <code class="returnvalue">bytea</code>
</p>
<p>
       將代表以 <em class="parameter"><code>src_encoding</code></em> 編碼之文字的二進位字串，轉換為以 <em class="parameter"><code>dest_encoding</code></em> 編碼的二進位字串（可用的轉換請參閱<a class="xref" href="../../server-administration/charset/multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED">第 23.3.4 節</a>）。
      </p>
<p>
<code class="literal">convert('text_in_utf8', 'UTF8', 'LATIN1')</code>
       → <code class="returnvalue">\x746578745f696e5f75746638</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.11.2.2.2.1.1.1"></a>
<code class="function">convert_from</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
       <em class="parameter"><code>src_encoding</code></em> <code class="type">name</code> )
       → <code class="returnvalue">text</code>
</p>
<p>
       將代表以 <em class="parameter"><code>src_encoding</code></em> 編碼之文字的二進位字串，轉換為資料庫編碼的 <code class="type">text</code>（可用的轉換請參閱<a class="xref" href="../../server-administration/charset/multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED">第 23.3.4 節</a>）。
      </p>
<p>
<code class="literal">convert_from('text_in_utf8', 'UTF8')</code>
       → <code class="returnvalue">text_in_utf8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.11.11.2.2.3.1.1.1"></a>
<code class="function">convert_to</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
       <em class="parameter"><code>dest_encoding</code></em> <code class="type">name</code> )
       → <code class="returnvalue">bytea</code>
</p>
<p>
       將 <code class="type">text</code> 字串（資料庫編碼）轉換為以 <em class="parameter"><code>dest_encoding</code></em> 編碼的二進位字串（可用的轉換請參閱<a class="xref" href="../../server-administration/charset/multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED">第 23.3.4 節</a>）。
      </p>
<p>
<code class="literal">convert_to('some_text', 'UTF8')</code>
       → <code class="returnvalue">\x736f6d655f74657874</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-ENCODE"></a>
<code class="function">encode</code> ( <em class="parameter"><code>bytes</code></em> <code class="type">bytea</code>,
       <em class="parameter"><code>format</code></em> <code class="type">text</code> )
       → <code class="returnvalue">text</code>
</p>
<p>
       將二進位資料編碼為文字表示；支援的 <em class="parameter"><code>format</code></em> 值為：<a class="link" href="functions-binarystring.md#ENCODE-FORMAT-BASE64"><code class="literal">base64</code></a>、<a class="link" href="functions-binarystring.md#ENCODE-FORMAT-ESCAPE"><code class="literal">escape</code></a>、<a class="link" href="functions-binarystring.md#ENCODE-FORMAT-HEX"><code class="literal">hex</code></a>。
      </p>
<p>
<code class="literal">encode('123\000\001', 'base64')</code>
       → <code class="returnvalue">MTIzAAE=</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="FUNCTION-DECODE"></a>
<code class="function">decode</code> ( <em class="parameter"><code>string</code></em> <code class="type">text</code>,
       <em class="parameter"><code>format</code></em> <code class="type">text</code> )
       → <code class="returnvalue">bytea</code>
</p>
<p>
       從文字表示解碼二進位資料；支援的 <em class="parameter"><code>format</code></em> 值與 <code class="function">encode</code> 相同。
      </p>
<p>
<code class="literal">decode('MTIzAAE=', 'base64')</code>
       → <code class="returnvalue">\x3132330001</code>
</p></td></tr></tbody></table>

<br>

`encode` 與 `decode` 函式支援下列文字格式：

<a id="ENCODE-FORMAT-BASE64"></a>

base64 <a id="id-1.5.8.11.12.3.1.1.1"></a> [#](#ENCODE-FORMAT-BASE64)
:   `base64` 格式即 [RFC 2045 第 6.8 節](https://datatracker.ietf.org/doc/html/rfc2045#section-6.8)所定義的格式。依照該 RFC，編碼後的行會在 76 個字元處斷行。不過，行尾只使用換行字元，而不是 MIME 的 CRLF 行尾標記。`decode` 函式會忽略歸位字元、換行字元、空白與 tab 字元。除此之外，當提供給 `decode` 的 base64 資料無效時——包括尾端填補不正確的情況——就會引發錯誤。
<a id="ENCODE-FORMAT-ESCAPE"></a>

escape <a id="id-1.5.8.11.12.3.2.1.1"></a> [#](#ENCODE-FORMAT-ESCAPE)
:   `escape` 格式會將零位元組以及最高位元已設定的位元組轉換為八進位跳脫序列（`\`*`nnn`*），並將反斜線重複。其他的位元組值則按字面表示。如果反斜線後面接的既不是第二個反斜線，也不是三個八進位數字，`decode` 函式就會引發錯誤；其他的位元組值則原樣接受。
<a id="ENCODE-FORMAT-HEX"></a>

hex <a id="id-1.5.8.11.12.3.3.1.1"></a> [#](#ENCODE-FORMAT-HEX)
:   `hex` 格式將每 4 個位元的資料表示為一個十六進位數字（`0` 到 `f`），並先寫出每個位元組的高位數字。`encode` 函式會以小寫輸出 `a`-`f` 的十六進位數字。由於最小的資料單位是 8 個位元，`encode` 回傳的字元數一定是偶數。`decode` 函式接受大寫或小寫的 `a`-`f` 字元。當提供給 `decode` 的十六進位資料無效時——包括提供了奇數個字元的情況——就會引發錯誤。

此外，整數值可以與 `bytea` 型別互相轉換。將整數轉換為 `bytea` 會產生 2、4 或 8 個位元組，取決於整數型別的寬度。結果是該整數的二補數表示，最高有效位元組在前。一些範例：

```

1234::smallint::bytea          \x04d2
cast(1234 as bytea)            \x000004d2
cast(-1234 as bytea)           \xfffffb2e
'\x8000'::bytea::smallint      -32768
'\x8000'::bytea::integer       32768
```

如果 `bytea` 的長度超過整數型別的寬度，將 `bytea` 轉換為整數就會引發錯誤。

另請參閱[第 9.21 節](functions-aggregate.md)中的彙總函式 `string_agg`，以及[第 33.4 節](../../client-interfaces/largeobjects/lo-funcs.md)中的大型物件函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-binarystring.html)（原文版本：18.6；核對日期：2026-09-11）
