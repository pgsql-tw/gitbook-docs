<a id="BRIN"></a>

## 65.5. BRIN 索引 [#](#brin) <a href="#brin" id="brin"></a>

[65.5.1. 簡介](brin.md#BRIN-INTRO)

[65.5.2. 內建運算子類別](brin.md#BRIN-BUILTIN-OPCLASSES)

[65.5.3. 擴充性](brin.md#BRIN-EXTENSIBILITY)

<a id="id-1.10.17.6.2"></a>
<a id="BRIN-INTRO"></a>

### 65.5.1. 簡介 [#](#BRIN-INTRO)

BRIN 是 Block Range Index（區塊範圍索引）的縮寫。BRIN 的設計目的是處理非常大的資料表，其中某些欄位與其在資料表中的實體位置具有某種自然的相關性。

BRIN 以*區塊範圍*（或稱「頁面範圍」）為單位運作。區塊範圍是資料表中實體上相鄰的一組頁面；索引會為每個區塊範圍儲存一些摘要資訊。舉例來說，儲存商店銷售訂單的資料表可能有一個記錄每筆訂單下單日期的日期欄位，而且大多數情況下，較早訂單的項目在資料表中也會出現在較前面的位置；儲存郵遞區號欄位的資料表，則可能自然地將同一城市的所有郵遞區號歸在一起。

BRIN 索引可以透過一般的點陣圖索引掃描來滿足查詢；若索引所儲存的摘要資訊與查詢條件*一致*，就會傳回每個範圍內所有頁面中的所有 tuple。查詢執行器負責重新檢查這些 tuple，並捨棄不符合查詢條件的 tuple——換句話說，這些索引是有損的（lossy）。由於 BRIN 索引非常小，與循序掃描相比，掃描索引只會增加很少的額外負擔，但可能可以避免掃描資料表中已知不含符合條件之 tuple 的大部分區域。

BRIN 索引實際儲存哪些資料，以及索引能夠滿足哪些查詢，取決於為索引的每個欄位所選用的運算子類別。例如，具有線性排序順序的資料型別，可以有儲存每個區塊範圍內最小值與最大值的運算子類別；幾何型別則可能儲存區塊範圍內所有物件的外接矩形（bounding box）。

區塊範圍的大小在建立索引時由 `pages_per_range` 儲存參數決定。索引項目的數量會等於以頁面計的關聯大小除以為 `pages_per_range` 選定的值。因此，這個數字越小，索引就越大（因為需要儲存更多索引項目），但同時所儲存的摘要資料也可以更精確，而且在索引掃描期間可以跳過更多資料區塊。

<a id="BRIN-OPERATION"></a>

#### 65.5.1.1. 索引維護 [#](#BRIN-OPERATION)

建立索引時，會掃描所有現有的堆積頁面，並為每個範圍建立一個摘要索引 tuple，包括結尾處可能不完整的範圍。當新頁面填入資料時，已摘要的頁面範圍會使摘要資訊以新 tuple 的資料更新。當建立的新頁面不在最後一個已摘要的範圍內時，該新頁面所屬的範圍不會自動取得摘要 tuple；這些 tuple 會維持未摘要的狀態，直到之後執行摘要作業，為該範圍建立初始摘要為止。

有幾種方式可以觸發頁面範圍的初始摘要。如果資料表被執行 vacuum，無論是手動執行或由 [autovacuum](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM) 執行，所有現有的未摘要頁面範圍都會被摘要。此外，如果啟用了索引的 [autosummarize](../../reference/sql-commands/sql-createindex.md#INDEX-RELOPTION-AUTOSUMMARIZE) 參數（預設並未啟用），則每當 autovacuum 在該資料庫中執行時，所有已填滿的未摘要頁面範圍都會進行摘要，無論資料表本身是否被 autovacuum 處理；請參閱下文。

最後，也可以使用下列函式（這些函式執行期間，[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 會暫時變更為 `pg_catalog, pg_temp`）：

<table border="0" class="simplelist" summary="簡單清單"><tr><td>
<code class="function">brin_summarize_new_values(regclass)</code>
     摘要所有未摘要的範圍；
    </td></tr><tr><td>
<code class="function">brin_summarize_range(regclass, bigint)</code>
     僅摘要包含指定頁面的範圍（若該範圍尚未摘要）。
    </td></tr></table>

啟用自動摘要時，當偵測到有資料插入下一個區塊範圍第一個頁面的第一個項目時，會向 `autovacuum` 送出一個請求，要求對該區塊範圍執行定向摘要，這個請求會在下一次 autovacuum 工作程序於同一資料庫中執行完畢時完成。如果請求佇列已滿，該請求不會被記錄，並且會向伺服器日誌送出一則訊息：

```

LOG:  request for BRIN range summarization for index "brin_wi_idx" page 128 was not recorded
```

發生這種情況時，該範圍會維持未摘要的狀態，直到下一次對該資料表執行一般的 vacuum，或呼叫上述函式之一為止。

反過來說，可以使用 `brin_desummarize_range(regclass, bigint)` 函式取消某個範圍的摘要；當現有的值已經改變，使得索引 tuple 不再能很好地代表它們時，這個函式就很有用。詳細資訊請參閱[第 9.28.8 節](../../the-sql-language/functions/functions-admin.md#functions-admin-index)。

<a id="BRIN-BUILTIN-OPCLASSES"></a>

### 65.5.2. 內建運算子類別 [#](#BRIN-BUILTIN-OPCLASSES)

PostgreSQL 核心發行版本包含[表 65.4](brin.md#BRIN-BUILTIN-OPCLASSES-TABLE) 所列的 BRIN 運算子類別。

*minmax* 運算子類別儲存範圍內被索引欄位中出現的最小值與最大值。*inclusion* 運算子類別儲存一個值，該值涵蓋範圍內被索引欄位中的各個值。*bloom* 運算子類別為範圍內的所有值建立 Bloom 過濾器（Bloom filter）。*minmax-multi* 運算子類別儲存多個最小值與最大值，用以代表範圍內被索引欄位中出現的值。

<a id="BRIN-BUILTIN-OPCLASSES-TABLE"></a>

**表 65.4. 內建 BRIN 運算子類別**

<table border="1" class="table" summary="內建 BRIN 運算子類別"><colgroup><col/><col/></colgroup><thead><tr><th>名稱</th><th>可索引運算子</th></tr></thead><tbody><tr><td rowspan="5" valign="middle"><code class="literal">bit_minmax_ops</code></td><td><code class="literal">= (bit,bit)</code></td></tr><tr><td><code class="literal">&lt; (bit,bit)</code></td></tr><tr><td><code class="literal">&gt; (bit,bit)</code></td></tr><tr><td><code class="literal">&lt;= (bit,bit)</code></td></tr><tr><td><code class="literal">&gt;= (bit,bit)</code></td></tr><tr><td rowspan="13" valign="middle"><code class="literal">box_inclusion_ops</code></td><td><code class="literal">@&gt; (box,point)</code></td></tr><tr><td><code class="literal">&lt;&lt; (box,box)</code></td></tr><tr><td><code class="literal">&amp;&lt; (box,box)</code></td></tr><tr><td><code class="literal">&amp;&gt; (box,box)</code></td></tr><tr><td><code class="literal">&gt;&gt; (box,box)</code></td></tr><tr><td><code class="literal">&lt;@ (box,box)</code></td></tr><tr><td><code class="literal">@&gt; (box,box)</code></td></tr><tr><td><code class="literal">~= (box,box)</code></td></tr><tr><td><code class="literal">&amp;&amp; (box,box)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (box,box)</code></td></tr><tr><td><code class="literal">&amp;&lt;| (box,box)</code></td></tr><tr><td><code class="literal">|&amp;&gt; (box,box)</code></td></tr><tr><td><code class="literal">|&gt;&gt; (box,box)</code></td></tr><tr><td valign="middle"><code class="literal">bpchar_bloom_ops</code></td><td><code class="literal">= (character,character)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">bpchar_minmax_ops</code></td><td><code class="literal">= (character,character)</code></td></tr><tr><td><code class="literal">&lt; (character,character)</code></td></tr><tr><td><code class="literal">&lt;= (character,character)</code></td></tr><tr><td><code class="literal">&gt; (character,character)</code></td></tr><tr><td><code class="literal">&gt;= (character,character)</code></td></tr><tr><td valign="middle"><code class="literal">bytea_bloom_ops</code></td><td><code class="literal">= (bytea,bytea)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">bytea_minmax_ops</code></td><td><code class="literal">= (bytea,bytea)</code></td></tr><tr><td><code class="literal">&lt; (bytea,bytea)</code></td></tr><tr><td><code class="literal">&lt;= (bytea,bytea)</code></td></tr><tr><td><code class="literal">&gt; (bytea,bytea)</code></td></tr><tr><td><code class="literal">&gt;= (bytea,bytea)</code></td></tr><tr><td valign="middle"><code class="literal">char_bloom_ops</code></td><td><code class="literal">= ("char","char")</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">char_minmax_ops</code></td><td><code class="literal">= ("char","char")</code></td></tr><tr><td><code class="literal">&lt; ("char","char")</code></td></tr><tr><td><code class="literal">&lt;= ("char","char")</code></td></tr><tr><td><code class="literal">&gt; ("char","char")</code></td></tr><tr><td><code class="literal">&gt;= ("char","char")</code></td></tr><tr><td valign="middle"><code class="literal">date_bloom_ops</code></td><td><code class="literal">= (date,date)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">date_minmax_ops</code></td><td><code class="literal">= (date,date)</code></td></tr><tr><td><code class="literal">&lt; (date,date)</code></td></tr><tr><td><code class="literal">&lt;= (date,date)</code></td></tr><tr><td><code class="literal">&gt; (date,date)</code></td></tr><tr><td><code class="literal">&gt;= (date,date)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">date_minmax_multi_ops</code></td><td><code class="literal">= (date,date)</code></td></tr><tr><td><code class="literal">&lt; (date,date)</code></td></tr><tr><td><code class="literal">&lt;= (date,date)</code></td></tr><tr><td><code class="literal">&gt; (date,date)</code></td></tr><tr><td><code class="literal">&gt;= (date,date)</code></td></tr><tr><td valign="middle"><code class="literal">float4_bloom_ops</code></td><td><code class="literal">= (float4,float4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float4_minmax_ops</code></td><td><code class="literal">= (float4,float4)</code></td></tr><tr><td><code class="literal">&lt; (float4,float4)</code></td></tr><tr><td><code class="literal">&gt; (float4,float4)</code></td></tr><tr><td><code class="literal">&lt;= (float4,float4)</code></td></tr><tr><td><code class="literal">&gt;= (float4,float4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float4_minmax_multi_ops</code></td><td><code class="literal">= (float4,float4)</code></td></tr><tr><td><code class="literal">&lt; (float4,float4)</code></td></tr><tr><td><code class="literal">&gt; (float4,float4)</code></td></tr><tr><td><code class="literal">&lt;= (float4,float4)</code></td></tr><tr><td><code class="literal">&gt;= (float4,float4)</code></td></tr><tr><td valign="middle"><code class="literal">float8_bloom_ops</code></td><td><code class="literal">= (float8,float8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float8_minmax_ops</code></td><td><code class="literal">= (float8,float8)</code></td></tr><tr><td><code class="literal">&lt; (float8,float8)</code></td></tr><tr><td><code class="literal">&lt;= (float8,float8)</code></td></tr><tr><td><code class="literal">&gt; (float8,float8)</code></td></tr><tr><td><code class="literal">&gt;= (float8,float8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float8_minmax_multi_ops</code></td><td><code class="literal">= (float8,float8)</code></td></tr><tr><td><code class="literal">&lt; (float8,float8)</code></td></tr><tr><td><code class="literal">&lt;= (float8,float8)</code></td></tr><tr><td><code class="literal">&gt; (float8,float8)</code></td></tr><tr><td><code class="literal">&gt;= (float8,float8)</code></td></tr><tr><td rowspan="6" valign="middle"><code class="literal">inet_inclusion_ops</code></td><td><code class="literal">&lt;&lt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;&gt;= (inet,inet)</code></td></tr><tr><td><code class="literal">= (inet,inet)</code></td></tr><tr><td><code class="literal">&amp;&amp; (inet,inet)</code></td></tr><tr><td valign="middle"><code class="literal">inet_bloom_ops</code></td><td><code class="literal">= (inet,inet)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">inet_minmax_ops</code></td><td><code class="literal">= (inet,inet)</code></td></tr><tr><td><code class="literal">&lt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;= (inet,inet)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">inet_minmax_multi_ops</code></td><td><code class="literal">= (inet,inet)</code></td></tr><tr><td><code class="literal">&lt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;= (inet,inet)</code></td></tr><tr><td valign="middle"><code class="literal">int2_bloom_ops</code></td><td><code class="literal">= (int2,int2)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int2_minmax_ops</code></td><td><code class="literal">= (int2,int2)</code></td></tr><tr><td><code class="literal">&lt; (int2,int2)</code></td></tr><tr><td><code class="literal">&gt; (int2,int2)</code></td></tr><tr><td><code class="literal">&lt;= (int2,int2)</code></td></tr><tr><td><code class="literal">&gt;= (int2,int2)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int2_minmax_multi_ops</code></td><td><code class="literal">= (int2,int2)</code></td></tr><tr><td><code class="literal">&lt; (int2,int2)</code></td></tr><tr><td><code class="literal">&gt; (int2,int2)</code></td></tr><tr><td><code class="literal">&lt;= (int2,int2)</code></td></tr><tr><td><code class="literal">&gt;= (int2,int2)</code></td></tr><tr><td valign="middle"><code class="literal">int4_bloom_ops</code></td><td><code class="literal">= (int4,int4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int4_minmax_ops</code></td><td><code class="literal">= (int4,int4)</code></td></tr><tr><td><code class="literal">&lt; (int4,int4)</code></td></tr><tr><td><code class="literal">&gt; (int4,int4)</code></td></tr><tr><td><code class="literal">&lt;= (int4,int4)</code></td></tr><tr><td><code class="literal">&gt;= (int4,int4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int4_minmax_multi_ops</code></td><td><code class="literal">= (int4,int4)</code></td></tr><tr><td><code class="literal">&lt; (int4,int4)</code></td></tr><tr><td><code class="literal">&gt; (int4,int4)</code></td></tr><tr><td><code class="literal">&lt;= (int4,int4)</code></td></tr><tr><td><code class="literal">&gt;= (int4,int4)</code></td></tr><tr><td valign="middle"><code class="literal">int8_bloom_ops</code></td><td><code class="literal">= (bigint,bigint)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int8_minmax_ops</code></td><td><code class="literal">= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt;= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt;= (bigint,bigint)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int8_minmax_multi_ops</code></td><td><code class="literal">= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt;= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt;= (bigint,bigint)</code></td></tr><tr><td valign="middle"><code class="literal">interval_bloom_ops</code></td><td><code class="literal">= (interval,interval)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">interval_minmax_ops</code></td><td><code class="literal">= (interval,interval)</code></td></tr><tr><td><code class="literal">&lt; (interval,interval)</code></td></tr><tr><td><code class="literal">&lt;= (interval,interval)</code></td></tr><tr><td><code class="literal">&gt; (interval,interval)</code></td></tr><tr><td><code class="literal">&gt;= (interval,interval)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">interval_minmax_multi_ops</code></td><td><code class="literal">= (interval,interval)</code></td></tr><tr><td><code class="literal">&lt; (interval,interval)</code></td></tr><tr><td><code class="literal">&lt;= (interval,interval)</code></td></tr><tr><td><code class="literal">&gt; (interval,interval)</code></td></tr><tr><td><code class="literal">&gt;= (interval,interval)</code></td></tr><tr><td valign="middle"><code class="literal">macaddr_bloom_ops</code></td><td><code class="literal">= (macaddr,macaddr)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr_minmax_ops</code></td><td><code class="literal">= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr,macaddr)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr_minmax_multi_ops</code></td><td><code class="literal">= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr,macaddr)</code></td></tr><tr><td valign="middle"><code class="literal">macaddr8_bloom_ops</code></td><td><code class="literal">= (macaddr8,macaddr8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr8_minmax_ops</code></td><td><code class="literal">= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr8,macaddr8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr8_minmax_multi_ops</code></td><td><code class="literal">= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr8,macaddr8)</code></td></tr><tr><td valign="middle"><code class="literal">name_bloom_ops</code></td><td><code class="literal">= (name,name)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">name_minmax_ops</code></td><td><code class="literal">= (name,name)</code></td></tr><tr><td><code class="literal">&lt; (name,name)</code></td></tr><tr><td><code class="literal">&lt;= (name,name)</code></td></tr><tr><td><code class="literal">&gt; (name,name)</code></td></tr><tr><td><code class="literal">&gt;= (name,name)</code></td></tr><tr><td valign="middle"><code class="literal">numeric_bloom_ops</code></td><td><code class="literal">= (numeric,numeric)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">numeric_minmax_ops</code></td><td><code class="literal">= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt;= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt;= (numeric,numeric)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">numeric_minmax_multi_ops</code></td><td><code class="literal">= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt;= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt;= (numeric,numeric)</code></td></tr><tr><td valign="middle"><code class="literal">oid_bloom_ops</code></td><td><code class="literal">= (oid,oid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">oid_minmax_ops</code></td><td><code class="literal">= (oid,oid)</code></td></tr><tr><td><code class="literal">&lt; (oid,oid)</code></td></tr><tr><td><code class="literal">&gt; (oid,oid)</code></td></tr><tr><td><code class="literal">&lt;= (oid,oid)</code></td></tr><tr><td><code class="literal">&gt;= (oid,oid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">oid_minmax_multi_ops</code></td><td><code class="literal">= (oid,oid)</code></td></tr><tr><td><code class="literal">&lt; (oid,oid)</code></td></tr><tr><td><code class="literal">&gt; (oid,oid)</code></td></tr><tr><td><code class="literal">&lt;= (oid,oid)</code></td></tr><tr><td><code class="literal">&gt;= (oid,oid)</code></td></tr><tr><td valign="middle"><code class="literal">pg_lsn_bloom_ops</code></td><td><code class="literal">= (pg_lsn,pg_lsn)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">pg_lsn_minmax_ops</code></td><td><code class="literal">= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">pg_lsn_minmax_multi_ops</code></td><td><code class="literal">= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td rowspan="14" valign="middle"><code class="literal">range_inclusion_ops</code></td><td><code class="literal">= (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;= (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&gt;= (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&amp; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange,anyelement)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;@ (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&gt;&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">-|- (anyrange,anyrange)</code></td></tr><tr><td valign="middle"><code class="literal">text_bloom_ops</code></td><td><code class="literal">= (text,text)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">text_minmax_ops</code></td><td><code class="literal">= (text,text)</code></td></tr><tr><td><code class="literal">&lt; (text,text)</code></td></tr><tr><td><code class="literal">&lt;= (text,text)</code></td></tr><tr><td><code class="literal">&gt; (text,text)</code></td></tr><tr><td><code class="literal">&gt;= (text,text)</code></td></tr><tr><td valign="middle"><code class="literal">tid_bloom_ops</code></td><td><code class="literal">= (tid,tid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">tid_minmax_ops</code></td><td><code class="literal">= (tid,tid)</code></td></tr><tr><td><code class="literal">&lt; (tid,tid)</code></td></tr><tr><td><code class="literal">&gt; (tid,tid)</code></td></tr><tr><td><code class="literal">&lt;= (tid,tid)</code></td></tr><tr><td><code class="literal">&gt;= (tid,tid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">tid_minmax_multi_ops</code></td><td><code class="literal">= (tid,tid)</code></td></tr><tr><td><code class="literal">&lt; (tid,tid)</code></td></tr><tr><td><code class="literal">&gt; (tid,tid)</code></td></tr><tr><td><code class="literal">&lt;= (tid,tid)</code></td></tr><tr><td><code class="literal">&gt;= (tid,tid)</code></td></tr><tr><td valign="middle"><code class="literal">timestamp_bloom_ops</code></td><td><code class="literal">= (timestamp,timestamp)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamp_minmax_ops</code></td><td><code class="literal">= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt;= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt;= (timestamp,timestamp)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamp_minmax_multi_ops</code></td><td><code class="literal">= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt;= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt;= (timestamp,timestamp)</code></td></tr><tr><td valign="middle"><code class="literal">timestamptz_bloom_ops</code></td><td><code class="literal">= (timestamptz,timestamptz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamptz_minmax_ops</code></td><td><code class="literal">= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt;= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt;= (timestamptz,timestamptz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamptz_minmax_multi_ops</code></td><td><code class="literal">= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt;= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt;= (timestamptz,timestamptz)</code></td></tr><tr><td valign="middle"><code class="literal">time_bloom_ops</code></td><td><code class="literal">= (time,time)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">time_minmax_ops</code></td><td><code class="literal">= (time,time)</code></td></tr><tr><td><code class="literal">&lt; (time,time)</code></td></tr><tr><td><code class="literal">&lt;= (time,time)</code></td></tr><tr><td><code class="literal">&gt; (time,time)</code></td></tr><tr><td><code class="literal">&gt;= (time,time)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">time_minmax_multi_ops</code></td><td><code class="literal">= (time,time)</code></td></tr><tr><td><code class="literal">&lt; (time,time)</code></td></tr><tr><td><code class="literal">&lt;= (time,time)</code></td></tr><tr><td><code class="literal">&gt; (time,time)</code></td></tr><tr><td><code class="literal">&gt;= (time,time)</code></td></tr><tr><td valign="middle"><code class="literal">timetz_bloom_ops</code></td><td><code class="literal">= (timetz,timetz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timetz_minmax_ops</code></td><td><code class="literal">= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt;= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt;= (timetz,timetz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timetz_minmax_multi_ops</code></td><td><code class="literal">= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt;= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt;= (timetz,timetz)</code></td></tr><tr><td valign="middle"><code class="literal">uuid_bloom_ops</code></td><td><code class="literal">= (uuid,uuid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">uuid_minmax_ops</code></td><td><code class="literal">= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt;= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt;= (uuid,uuid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">uuid_minmax_multi_ops</code></td><td><code class="literal">= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt;= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt;= (uuid,uuid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">varbit_minmax_ops</code></td><td><code class="literal">= (varbit,varbit)</code></td></tr><tr><td><code class="literal">&lt; (varbit,varbit)</code></td></tr><tr><td><code class="literal">&gt; (varbit,varbit)</code></td></tr><tr><td><code class="literal">&lt;= (varbit,varbit)</code></td></tr><tr><td><code class="literal">&gt;= (varbit,varbit)</code></td></tr></tbody></table>

<br>

<a id="BRIN-BUILTIN-OPCLASSES--PARAMETERS"></a>

#### 65.5.2.1. 運算子類別參數 [#](#BRIN-BUILTIN-OPCLASSES--PARAMETERS)

部分內建運算子類別允許指定會影響該運算子類別行為的參數。每個運算子類別都有自己的一組可用參數。只有 `bloom` 與 `minmax-multi` 運算子類別允許指定參數：

bloom 運算子類別接受下列參數：

`n_distinct_per_range`

定義區塊範圍中相異非 null 值的估計數量，BRIN bloom 索引用它來決定 Bloom 過濾器的大小。它的行為類似 [ALTER TABLE](../../reference/sql-commands/sql-altertable.md) 的 `n_distinct` 選項。設為正值時，假設每個區塊範圍包含此數量的相異非 null 值。設為負值時（必須大於或等於 -1），假設相異非 null 值的數量會隨區塊範圍中可能的最大 tuple 數量線性成長（每個區塊約 290 個資料列）。預設值為 `-0.1`，相異非 null 值的最小數量為 `16`。

`false_positive_rate`

定義 BRIN bloom 索引決定 Bloom 過濾器大小時所使用的期望偽陽性率。值必須介於 0.0001 與 0.25 之間。預設值為 0.01，即 1% 的偽陽性率。

minmax-multi 運算子類別接受下列參數：

`values_per_range`

定義 BRIN minmax 索引為了摘要一個區塊範圍所儲存的值的最大數量。每個值可能代表一個點，或一個區間的邊界。值必須介於 8 與 256 之間，預設值為 32。

<a id="BRIN-EXTENSIBILITY"></a>

### 65.5.3. 擴充性 [#](#BRIN-EXTENSIBILITY)

BRIN 介面具有高度的抽象性，只要求存取方法的實作者實作所存取資料型別的語意。BRIN 層本身會負責並行處理、日誌記錄以及索引結構的搜尋。

要讓 BRIN 存取方法運作，只需要實作幾個使用者定義的方法，這些方法定義了索引中所儲存之摘要值的行為，以及它們與掃描鍵互動的方式。簡而言之，BRIN 結合了擴充性與通用性、程式碼重用，以及簡潔的介面。

BRIN 的運算子類別必須提供四個方法：

`BrinOpcInfo *opcInfo(Oid type_oid)`

傳回被索引欄位之摘要資料的內部資訊。傳回值必須指向一個以 palloc 配置的 `BrinOpcInfo`，其定義如下：

```

    typedef struct BrinOpcInfo
    {
        /* Number of columns stored in an index column of this opclass */
        uint16      oi_nstored;

        /* Opaque pointer for the opclass' private use */
        void       *oi_opaque;

        /* Type cache entries of the stored columns */
        TypeCacheEntry *oi_typcache[FLEXIBLE_ARRAY_MEMBER];
    } BrinOpcInfo;
```

`BrinOpcInfo`.`oi_opaque` 可供運算子類別的常式在索引掃描期間於支援函式之間傳遞資訊。

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey *keys, int nkeys)`

傳回所有 ScanKey 項目是否都與某個範圍的給定索引值一致。要使用的屬性編號會作為掃描鍵的一部分傳入。同一屬性的多個掃描鍵可以一次傳入；項目數量由 `nkeys` 參數決定。

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey key)`

傳回 ScanKey 是否與某個範圍的給定索引值一致。要使用的屬性編號會作為掃描鍵的一部分傳入。這是 consistent 函式較舊、具向後相容性的變體。

`bool addValue(BrinDesc *bdesc, BrinValues *column, Datum newval, bool isnull)`

給定一個索引 tuple 與一個被索引的值，修改該 tuple 的指定屬性，使其額外代表這個新值。如果對該 tuple 做了任何修改，則傳回 `true`。

`bool unionTuples(BrinDesc *bdesc, BrinValues *a, BrinValues *b)`

合併兩個索引 tuple。給定兩個索引 tuple，修改其中第一個 tuple 的指定屬性，使其同時代表這兩個 tuple。第二個 tuple 不會被修改。

BRIN 的運算子類別可以選擇性地指定下列方法：

`void options(local_relopts *relopts)`

定義一組使用者可見的參數，用以控制運算子類別的行為。

`options` 函式會收到一個指向 `local_relopts` 結構的指標，該結構需要填入一組運算子類別專屬的選項。其他支援函式可以使用 `PG_HAS_OPCLASS_OPTIONS()` 與 `PG_GET_OPCLASS_OPTIONS()` 巨集存取這些選項。

由於被索引值的鍵擷取方式，以及鍵在 BRIN 中的表示方式都具有彈性，它們可能取決於使用者指定的參數。

核心發行版本支援四種運算子類別：minmax、minmax-multi、inclusion 與 bloom。使用它們的運算子類別定義會視情況隨附於核心內建的資料型別。使用者可以用等效的定義，為其他資料型別定義額外的運算子類別，而不必撰寫任何原始碼；只要宣告適當的系統目錄項目即可。請注意，關於運算子策略語意的假設已內嵌在支援函式的原始碼中。

也可以有實作完全不同語意的運算子類別，前提是撰寫了上述四個主要支援函式的實作。請注意，不保證跨主要版本的向後相容性：例如，之後的版本可能會需要額外的支援函式。

要為實作全序集合的資料型別撰寫運算子類別，可以搭配相應的運算子使用 minmax 支援函式，如[表 65.5](brin.md#BRIN-EXTENSIBILITY-MINMAX-TABLE) 所示。所有運算子類別成員（函式與運算子）都是必要的。

<a id="BRIN-EXTENSIBILITY-MINMAX-TABLE"></a>

**表 65.5. minmax 運算子類別的函式與支援編號**

<table border="1" class="table" summary="minmax 運算子類別的函式與支援編號"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th></tr></thead><tbody><tr><td>支援函式 1</td><td>內部函式 <code class="function">brin_minmax_opcinfo()</code></td></tr><tr><td>支援函式 2</td><td>內部函式 <code class="function">brin_minmax_add_value()</code></td></tr><tr><td>支援函式 3</td><td>內部函式 <code class="function">brin_minmax_consistent()</code></td></tr><tr><td>支援函式 4</td><td>內部函式 <code class="function">brin_minmax_union()</code></td></tr><tr><td>運算子策略 1</td><td>「小於」運算子</td></tr><tr><td>運算子策略 2</td><td>「小於或等於」運算子</td></tr><tr><td>運算子策略 3</td><td>「等於」運算子</td></tr><tr><td>運算子策略 4</td><td>「大於或等於」運算子</td></tr><tr><td>運算子策略 5</td><td>「大於」運算子</td></tr></tbody></table>

<br>

若要為某種複雜資料型別撰寫運算子類別，且該型別的值包含在另一種型別之中，可以搭配相應的運算子使用 inclusion 支援函式，如[表 65.6](brin.md#BRIN-EXTENSIBILITY-INCLUSION-TABLE) 所示。它只需要一個額外的函式，而該函式可以用任何語言撰寫。可以定義更多函式來提供額外的功能。所有運算子都是選擇性的。某些運算子需要其他運算子，如表中的相依關係所示。

<a id="BRIN-EXTENSIBILITY-INCLUSION-TABLE"></a>

**表 65.6. inclusion 運算子類別的函式與支援編號**

<table border="1" class="table" summary="inclusion 運算子類別的函式與支援編號"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th><th>相依於</th></tr></thead><tbody><tr><td>支援函式 1</td><td>內部函式 <code class="function">brin_inclusion_opcinfo()</code></td><td> </td></tr><tr><td>支援函式 2</td><td>內部函式 <code class="function">brin_inclusion_add_value()</code></td><td> </td></tr><tr><td>支援函式 3</td><td>內部函式 <code class="function">brin_inclusion_consistent()</code></td><td> </td></tr><tr><td>支援函式 4</td><td>內部函式 <code class="function">brin_inclusion_union()</code></td><td> </td></tr><tr><td>支援函式 11</td><td>合併兩個元素的函式</td><td> </td></tr><tr><td>支援函式 12</td><td>檢查兩個元素是否可合併的選擇性函式</td><td> </td></tr><tr><td>支援函式 13</td><td>檢查某元素是否包含於另一元素之中的選擇性函式</td><td> </td></tr><tr><td>支援函式 14</td><td>檢查元素是否為空的選擇性函式</td><td> </td></tr><tr><td>運算子策略 1</td><td>「位於左側」運算子</td><td>運算子策略 4</td></tr><tr><td>運算子策略 2</td><td>「不延伸至右側」運算子</td><td>運算子策略 5</td></tr><tr><td>運算子策略 3</td><td>「重疊」運算子</td><td> </td></tr><tr><td>運算子策略 4</td><td>「不延伸至左側」運算子</td><td>運算子策略 1</td></tr><tr><td>運算子策略 5</td><td>「位於右側」運算子</td><td>運算子策略 2</td></tr><tr><td>運算子策略 6, 18</td><td>「相同或等於」運算子</td><td>運算子策略 7</td></tr><tr><td>運算子策略 7, 16, 24, 25</td><td>「包含或等於」運算子</td><td> </td></tr><tr><td>運算子策略 8, 26, 27</td><td>「被包含或等於」運算子</td><td>運算子策略 3</td></tr><tr><td>運算子策略 9</td><td>「不延伸至上方」運算子</td><td>運算子策略 11</td></tr><tr><td>運算子策略 10</td><td>「位於下方」運算子</td><td>運算子策略 12</td></tr><tr><td>運算子策略 11</td><td>「位於上方」運算子</td><td>運算子策略 9</td></tr><tr><td>運算子策略 12</td><td>「不延伸至下方」運算子</td><td>運算子策略 10</td></tr><tr><td>運算子策略 20</td><td>「小於」運算子</td><td>運算子策略 5</td></tr><tr><td>運算子策略 21</td><td>「小於或等於」運算子</td><td>運算子策略 5</td></tr><tr><td>運算子策略 22</td><td>「大於」運算子</td><td>運算子策略 1</td></tr><tr><td>運算子策略 23</td><td>「大於或等於」運算子</td><td>運算子策略 1</td></tr></tbody></table>

<br>

支援函式編號 1 到 10 保留給 BRIN 內部函式使用，因此 SQL 層級的函式從編號 11 開始。支援函式編號 11 是建立索引所需的主要函式。它應該接受兩個資料型別與運算子類別相同的引數，並傳回兩者的聯集。如果 inclusion 運算子類別是以 `STORAGE` 參數定義的，它可以儲存不同資料型別的聯集值。聯集函式的傳回值應該與 `STORAGE` 資料型別相符。

支援函式編號 12 與 14 用於支援內建資料型別的不規則之處。函式編號 12 用於支援來自不同位址家族、無法合併的網路位址。函式編號 14 用於支援空範圍。函式編號 13 是選擇性但建議提供的函式，它允許在新值傳給聯集函式之前先加以檢查。由於 BRIN 框架在聯集沒有改變時可以略過某些操作，使用此函式可以提升索引效能。

要為只實作等於運算子並支援雜湊的資料型別撰寫運算子類別，可以搭配相應的運算子使用 bloom 支援程序，如[表 65.7](brin.md#BRIN-EXTENSIBILITY-BLOOM-TABLE) 所示。所有運算子類別成員（程序與運算子）都是必要的。

<a id="BRIN-EXTENSIBILITY-BLOOM-TABLE"></a>

**表 65.7. bloom 運算子類別的程序與支援編號**

<table border="1" class="table" summary="bloom 運算子類別的程序與支援編號"><colgroup><col/><col/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th></tr></thead><tbody><tr><td>支援程序 1</td><td>內部函式 <code class="function">brin_bloom_opcinfo()</code></td></tr><tr><td>支援程序 2</td><td>內部函式 <code class="function">brin_bloom_add_value()</code></td></tr><tr><td>支援程序 3</td><td>內部函式 <code class="function">brin_bloom_consistent()</code></td></tr><tr><td>支援程序 4</td><td>內部函式 <code class="function">brin_bloom_union()</code></td></tr><tr><td>支援程序 5</td><td>內部函式 <code class="function">brin_bloom_options()</code></td></tr><tr><td>支援程序 11</td><td>計算元素雜湊值的函式</td></tr><tr><td>運算子策略 1</td><td>「等於」運算子</td></tr></tbody></table>

<br>

支援程序編號 1-10 保留給 BRIN 內部函式使用，因此 SQL 層級的函式從編號 11 開始。支援函式編號 11 是建立索引所需的主要函式。它應該接受一個資料型別與運算子類別相同的引數，並傳回該值的雜湊。

minmax-multi 運算子類別同樣適用於實作全序集合的資料型別，可以視為 minmax 運算子類別的簡單延伸。minmax 運算子類別會將每個區塊範圍的值摘要成單一連續區間，而 minmax-multi 則允許摘要成多個較小的區間，以改善對離群值的處理。可以搭配相應的運算子使用 minmax-multi 支援程序，如[表 65.8](brin.md#BRIN-EXTENSIBILITY-MINMAX-MULTI-TABLE) 所示。所有運算子類別成員（程序與運算子）都是必要的。

<a id="BRIN-EXTENSIBILITY-MINMAX-MULTI-TABLE"></a>

**表 65.8. minmax-multi 運算子類別的程序與支援編號**

<table border="1" class="table" summary="minmax-multi 運算子類別的程序與支援編號"><colgroup><col/><col/></colgroup><thead><tr><th>運算子類別成員</th><th>物件</th></tr></thead><tbody><tr><td>支援程序 1</td><td>內部函式 <code class="function">brin_minmax_multi_opcinfo()</code></td></tr><tr><td>支援程序 2</td><td>內部函式 <code class="function">brin_minmax_multi_add_value()</code></td></tr><tr><td>支援程序 3</td><td>內部函式 <code class="function">brin_minmax_multi_consistent()</code></td></tr><tr><td>支援程序 4</td><td>內部函式 <code class="function">brin_minmax_multi_union()</code></td></tr><tr><td>支援程序 5</td><td>內部函式 <code class="function">brin_minmax_multi_options()</code></td></tr><tr><td>支援程序 11</td><td>計算兩個值之間距離（範圍長度）的函式</td></tr><tr><td>運算子策略 1</td><td>「小於」運算子</td></tr><tr><td>運算子策略 2</td><td>「小於或等於」運算子</td></tr><tr><td>運算子策略 3</td><td>「等於」運算子</td></tr><tr><td>運算子策略 4</td><td>「大於或等於」運算子</td></tr><tr><td>運算子策略 5</td><td>「大於」運算子</td></tr></tbody></table>

<br>

minmax 與 inclusion 運算子類別都支援跨資料型別的運算子，不過如此一來相依關係會變得更複雜。minmax 運算子類別要求定義一整組兩個引數資料型別相同的運算子。它允許藉由定義額外幾組運算子來支援其他資料型別。inclusion 運算子類別的運算子策略相依於另一個運算子策略（如[表 65.6](brin.md#BRIN-EXTENSIBILITY-INCLUSION-TABLE) 所示），或相依於與自身相同的運算子策略。它們要求相依的運算子以 `STORAGE` 資料型別作為左側引數，並以另一個受支援的資料型別作為受支援運算子的右側引數。minmax 的範例請參閱 `float4_minmax_ops`，inclusion 的範例請參閱 `box_inclusion_ops`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/brin.html)（原文版本：18.6；核對日期：2026-10-12）
