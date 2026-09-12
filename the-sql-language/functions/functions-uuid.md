<a id="FUNCTIONS-UUID"></a>

## 9.14. UUID 函式 [#](#FUNCTIONS-UUID)

<a id="id-1.5.8.20.2"></a><a id="id-1.5.8.20.3"></a><a id="id-1.5.8.20.4"></a><a id="id-1.5.8.20.5"></a><a id="id-1.5.8.20.6"></a><a id="id-1.5.8.20.7"></a>

[表 9.45](functions-uuid.md#FUNC_UUID_GEN_TABLE) 列出了可用來產生 UUID 的 PostgreSQL 函式。

<a id="FUNC_UUID_GEN_TABLE"></a>

**表 9.45. UUID 產生函式**

<table border="1" class="table" summary="UUID Generation Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
        </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">gen_random_uuid</code> ( )
        → <code class="returnvalue">uuid</code>
</p>
<p class="func_signature">
<code class="function">uuidv4</code> ( )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        產生第 4 版（隨機）UUID
       </p>
<p>
<code class="literal">gen_random_uuid()</code>
        → <code class="returnvalue">5b30857f-0bfa-48b5-ac0b-5c64e28078d1</code>
</p>
<p>
<code class="literal">uuidv4()</code>
        → <code class="returnvalue">b42410ee-132f-42ee-9e4f-09a6485c95b8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuidv7</code>
        ( [<span class="optional"> <em class="parameter"><code>shift</code></em> <code class="type">interval</code> </span>] )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        產生第 7 版（依時間排序）UUID。時間戳記是使用毫秒精度的 UNIX 時間戳記 + 次毫秒時間戳記 + 隨機值計算而得。選用參數 <em class="parameter"><code>shift</code></em> 會將計算出的時間戳記位移給定的 <code class="type">interval</code>。不接受無限的 interval 值。位移後的時間戳記必須落在 UUID 第 7 版之 48 位元毫秒時間戳記欄位所支援的範圍內：從 1970-01-01 00:00:00 UTC 到大約西元 10889 年。如果得到的時間戳記超出這個範圍，就會引發錯誤。
       </p>
<p>
<code class="literal">uuidv7()</code>
        → <code class="returnvalue">019535d9-3df7-79fb-b466-fa907fa17f9e</code>
</p></td></tr></tbody></table>

<br>

### 注意

[uuid-ossp](../../appendixes/contrib/uuid-ossp.md) 模組提供了額外的函式，實作其他產生 UUID 的標準演算法。

[表 9.46](functions-uuid.md#FUNC_UUID_EXTRACT_TABLE) 列出了可用來從 UUID 擷取資訊的 PostgreSQL 函式。

<a id="FUNC_UUID_EXTRACT_TABLE"></a>

**表 9.46. UUID 擷取函式**

<table border="1" class="table" summary="UUID Extraction Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_extract_timestamp</code>
        ( <code class="type">uuid</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        從第 1 版或第 7 版的 UUID 中擷取 <code class="type">timestamp with time zone</code>。對於其他版本，這個函式會回傳 null。請注意，擷取出的時間戳記不一定與產生該 UUID 的時間完全相同；這取決於產生該 UUID 的實作。
       </p>
<p>
<code class="literal">uuid_extract_timestamp('019535d9-3df7-79fb-b466-​fa907fa17f9e'::uuid)</code>
         → <code class="returnvalue">2025-02-23 21:46:24.503-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_extract_version</code>
        ( <code class="type">uuid</code> )
        → <code class="returnvalue">smallint</code>
</p>
<p>
        從屬於 <a class="ulink" href="https://datatracker.ietf.org/doc/html/rfc9562" target="_top">RFC 9562</a> 所描述之變體的 UUID 中擷取版本。對於其他變體，這個函式會回傳 null。例如，對於由 <code class="function">gen_random_uuid()</code> 產生的 UUID，這個函式會回傳 4。
       </p>
<p>
<code class="literal">uuid_extract_version('41db1265-8bc1-4ab3-992f-​885799a4af1d'::uuid)</code>
        → <code class="returnvalue">4</code>
</p>
<p>
<code class="literal">uuid_extract_version('019535d9-3df7-79fb-b466-​fa907fa17f9e'::uuid)</code>
        → <code class="returnvalue">7</code>
</p></td></tr></tbody></table>

<br>

PostgreSQL 也為 UUID 提供了[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子。

關於 PostgreSQL 中 `uuid` 資料型別的細節，請參閱[第 8.12 節](../datatype/datatype-uuid.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-uuid.html)（原文版本：18.6；核對日期：2026-09-11）
