## 65.5. BRIN Indexes [#](#BRIN)

[65.5.1. Introduction](brin.md#BRIN-INTRO)

[65.5.2. Built-in Operator Classes](brin.md#BRIN-BUILTIN-OPCLASSES)

[65.5.3. Extensibility](brin.md#BRIN-EXTENSIBILITY)

<a id="id-1.10.17.6.2"></a><a id="BRIN-INTRO"></a>

### 65.5.1. Introduction [#](#BRIN-INTRO)

BRIN stands for Block Range Index.
BRIN is designed for handling very large tables
in which certain columns have some natural correlation with their
physical location within the table.

BRIN works in terms of *block ranges*
(or “page ranges”).
A block range is a group of pages that are physically
adjacent in the table; for each block range, some summary info is stored
by the index.
For example, a table storing a store's sale orders might have
a date column on which each order was placed, and most of the time
the entries for earlier orders will appear earlier in the table as well;
a table storing a ZIP code column might have all codes for a city
grouped together naturally.

BRIN indexes can satisfy queries via regular bitmap
index scans, and will return all tuples in all pages within each range if
the summary info stored by the index is *consistent* with the
query conditions.
The query executor is in charge of rechecking these tuples and discarding
those that do not match the query conditions — in other words, these
indexes are lossy.
Because a BRIN index is very small, scanning the index
adds little overhead compared to a sequential scan, but may avoid scanning
large parts of the table that are known not to contain matching tuples.

The specific data that a BRIN index will store,
as well as the specific queries that the index will be able to satisfy,
depend on the operator class selected for each column of the index.
Data types having a linear sort order can have operator classes that
store the minimum and maximum value within each block range, for instance;
geometrical types might store the bounding box for all the objects
in the block range.

The size of the block range is determined at index creation time by
the `pages_per_range` storage parameter. The number of index
entries will be equal to the size of the relation in pages divided by
the selected value for `pages_per_range`. Therefore, the smaller
the number, the larger the index becomes (because of the need to
store more index entries), but at the same time the summary data stored can
be more precise and more data blocks can be skipped during an index scan.

<a id="BRIN-OPERATION"></a>

#### 65.5.1.1. Index Maintenance [#](#BRIN-OPERATION)

At the time of creation, all existing heap pages are scanned and a
summary index tuple is created for each range, including the
possibly-incomplete range at the end.
As new pages are filled with data, page ranges that are already
summarized will cause the summary information to be updated with data
from the new tuples.
When a new page is created that does not fall within the last
summarized range, the range that the new page belongs to
does not automatically acquire a summary tuple;
those tuples remain unsummarized until a summarization run is
invoked later, creating the initial summary for that range.

There are several ways to trigger the initial summarization of a page range.
If the table is vacuumed, either manually or by
[autovacuum](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM), all existing unsummarized
page ranges are summarized.
Also, if the index's
[autosummarize](../../reference/sql-commands/sql-createindex.md#INDEX-RELOPTION-AUTOSUMMARIZE) parameter is enabled,
which it isn't by default,
whenever autovacuum runs in that database, summarization will occur for all
unsummarized page ranges that have been filled,
regardless of whether the table itself is processed by autovacuum; see below.

Lastly, the following functions can be used (while these functions run,
[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) is temporarily changed to
`pg_catalog, pg_temp`):

<table border="0" class="simplelist" summary="Simple list"><tr><td>
<code class="function">brin_summarize_new_values(regclass)</code>
     which summarizes all unsummarized ranges;
    </td></tr><tr><td>
<code class="function">brin_summarize_range(regclass, bigint)</code>
     which summarizes only the range containing the given page,
     if it is unsummarized.
    </td></tr></table>

When autosummarization is enabled, a request is sent to
`autovacuum` to execute a targeted summarization
for a block range when an insertion is detected for the first item
of the first page of the next block range,
to be fulfilled the next time an autovacuum
worker finishes running in the
same database. If the request queue is full, the request is not recorded
and a message is sent to the server log:

```

LOG:  request for BRIN range summarization for index "brin_wi_idx" page 128 was not recorded
```

When this happens, the range will remain unsummarized until the next
regular vacuum run on the table, or one of the functions mentioned above
are invoked.

Conversely, a range can be de-summarized using the
`brin_desummarize_range(regclass, bigint)` function,
which is useful when the index tuple is no longer a very good
representation because the existing values have changed.
See [Section 9.28.8](../../the-sql-language/functions/functions-admin.md#FUNCTIONS-ADMIN-INDEX) for details.

<a id="BRIN-BUILTIN-OPCLASSES"></a>

### 65.5.2. Built-in Operator Classes [#](#BRIN-BUILTIN-OPCLASSES)

The core PostgreSQL distribution
includes the BRIN operator classes shown in
[Table 65.4](brin.md#BRIN-BUILTIN-OPCLASSES-TABLE).

The *minmax*
operator classes store the minimum and the maximum values appearing
in the indexed column within the range. The *inclusion*
operator classes store a value which includes the values in the indexed
column within the range. The *bloom* operator
classes build a Bloom filter for all values in the range. The
*minmax-multi* operator classes store multiple
minimum and maximum values, representing values appearing in the indexed
column within the range.

<a id="BRIN-BUILTIN-OPCLASSES-TABLE"></a>

**Table 65.4. Built-in BRIN Operator Classes**

<table border="1" class="table" summary="Built-in BRIN Operator Classes"><colgroup><col/><col/></colgroup><thead><tr><th>Name</th><th>Indexable Operators</th></tr></thead><tbody><tr><td rowspan="5" valign="middle"><code class="literal">bit_minmax_ops</code></td><td><code class="literal">= (bit,bit)</code></td></tr><tr><td><code class="literal">&lt; (bit,bit)</code></td></tr><tr><td><code class="literal">&gt; (bit,bit)</code></td></tr><tr><td><code class="literal">&lt;= (bit,bit)</code></td></tr><tr><td><code class="literal">&gt;= (bit,bit)</code></td></tr><tr><td rowspan="13" valign="middle"><code class="literal">box_inclusion_ops</code></td><td><code class="literal">@&gt; (box,point)</code></td></tr><tr><td><code class="literal">&lt;&lt; (box,box)</code></td></tr><tr><td><code class="literal">&amp;&lt; (box,box)</code></td></tr><tr><td><code class="literal">&amp;&gt; (box,box)</code></td></tr><tr><td><code class="literal">&gt;&gt; (box,box)</code></td></tr><tr><td><code class="literal">&lt;@ (box,box)</code></td></tr><tr><td><code class="literal">@&gt; (box,box)</code></td></tr><tr><td><code class="literal">~= (box,box)</code></td></tr><tr><td><code class="literal">&amp;&amp; (box,box)</code></td></tr><tr><td><code class="literal">&lt;&lt;| (box,box)</code></td></tr><tr><td><code class="literal">&amp;&lt;| (box,box)</code></td></tr><tr><td><code class="literal">|&amp;&gt; (box,box)</code></td></tr><tr><td><code class="literal">|&gt;&gt; (box,box)</code></td></tr><tr><td valign="middle"><code class="literal">bpchar_bloom_ops</code></td><td><code class="literal">= (character,character)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">bpchar_minmax_ops</code></td><td><code class="literal">= (character,character)</code></td></tr><tr><td><code class="literal">&lt; (character,character)</code></td></tr><tr><td><code class="literal">&lt;= (character,character)</code></td></tr><tr><td><code class="literal">&gt; (character,character)</code></td></tr><tr><td><code class="literal">&gt;= (character,character)</code></td></tr><tr><td valign="middle"><code class="literal">bytea_bloom_ops</code></td><td><code class="literal">= (bytea,bytea)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">bytea_minmax_ops</code></td><td><code class="literal">= (bytea,bytea)</code></td></tr><tr><td><code class="literal">&lt; (bytea,bytea)</code></td></tr><tr><td><code class="literal">&lt;= (bytea,bytea)</code></td></tr><tr><td><code class="literal">&gt; (bytea,bytea)</code></td></tr><tr><td><code class="literal">&gt;= (bytea,bytea)</code></td></tr><tr><td valign="middle"><code class="literal">char_bloom_ops</code></td><td><code class="literal">= ("char","char")</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">char_minmax_ops</code></td><td><code class="literal">= ("char","char")</code></td></tr><tr><td><code class="literal">&lt; ("char","char")</code></td></tr><tr><td><code class="literal">&lt;= ("char","char")</code></td></tr><tr><td><code class="literal">&gt; ("char","char")</code></td></tr><tr><td><code class="literal">&gt;= ("char","char")</code></td></tr><tr><td valign="middle"><code class="literal">date_bloom_ops</code></td><td><code class="literal">= (date,date)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">date_minmax_ops</code></td><td><code class="literal">= (date,date)</code></td></tr><tr><td><code class="literal">&lt; (date,date)</code></td></tr><tr><td><code class="literal">&lt;= (date,date)</code></td></tr><tr><td><code class="literal">&gt; (date,date)</code></td></tr><tr><td><code class="literal">&gt;= (date,date)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">date_minmax_multi_ops</code></td><td><code class="literal">= (date,date)</code></td></tr><tr><td><code class="literal">&lt; (date,date)</code></td></tr><tr><td><code class="literal">&lt;= (date,date)</code></td></tr><tr><td><code class="literal">&gt; (date,date)</code></td></tr><tr><td><code class="literal">&gt;= (date,date)</code></td></tr><tr><td valign="middle"><code class="literal">float4_bloom_ops</code></td><td><code class="literal">= (float4,float4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float4_minmax_ops</code></td><td><code class="literal">= (float4,float4)</code></td></tr><tr><td><code class="literal">&lt; (float4,float4)</code></td></tr><tr><td><code class="literal">&gt; (float4,float4)</code></td></tr><tr><td><code class="literal">&lt;= (float4,float4)</code></td></tr><tr><td><code class="literal">&gt;= (float4,float4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float4_minmax_multi_ops</code></td><td><code class="literal">= (float4,float4)</code></td></tr><tr><td><code class="literal">&lt; (float4,float4)</code></td></tr><tr><td><code class="literal">&gt; (float4,float4)</code></td></tr><tr><td><code class="literal">&lt;= (float4,float4)</code></td></tr><tr><td><code class="literal">&gt;= (float4,float4)</code></td></tr><tr><td valign="middle"><code class="literal">float8_bloom_ops</code></td><td><code class="literal">= (float8,float8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float8_minmax_ops</code></td><td><code class="literal">= (float8,float8)</code></td></tr><tr><td><code class="literal">&lt; (float8,float8)</code></td></tr><tr><td><code class="literal">&lt;= (float8,float8)</code></td></tr><tr><td><code class="literal">&gt; (float8,float8)</code></td></tr><tr><td><code class="literal">&gt;= (float8,float8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">float8_minmax_multi_ops</code></td><td><code class="literal">= (float8,float8)</code></td></tr><tr><td><code class="literal">&lt; (float8,float8)</code></td></tr><tr><td><code class="literal">&lt;= (float8,float8)</code></td></tr><tr><td><code class="literal">&gt; (float8,float8)</code></td></tr><tr><td><code class="literal">&gt;= (float8,float8)</code></td></tr><tr><td rowspan="6" valign="middle"><code class="literal">inet_inclusion_ops</code></td><td><code class="literal">&lt;&lt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;&gt;= (inet,inet)</code></td></tr><tr><td><code class="literal">= (inet,inet)</code></td></tr><tr><td><code class="literal">&amp;&amp; (inet,inet)</code></td></tr><tr><td valign="middle"><code class="literal">inet_bloom_ops</code></td><td><code class="literal">= (inet,inet)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">inet_minmax_ops</code></td><td><code class="literal">= (inet,inet)</code></td></tr><tr><td><code class="literal">&lt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;= (inet,inet)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">inet_minmax_multi_ops</code></td><td><code class="literal">= (inet,inet)</code></td></tr><tr><td><code class="literal">&lt; (inet,inet)</code></td></tr><tr><td><code class="literal">&lt;= (inet,inet)</code></td></tr><tr><td><code class="literal">&gt; (inet,inet)</code></td></tr><tr><td><code class="literal">&gt;= (inet,inet)</code></td></tr><tr><td valign="middle"><code class="literal">int2_bloom_ops</code></td><td><code class="literal">= (int2,int2)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int2_minmax_ops</code></td><td><code class="literal">= (int2,int2)</code></td></tr><tr><td><code class="literal">&lt; (int2,int2)</code></td></tr><tr><td><code class="literal">&gt; (int2,int2)</code></td></tr><tr><td><code class="literal">&lt;= (int2,int2)</code></td></tr><tr><td><code class="literal">&gt;= (int2,int2)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int2_minmax_multi_ops</code></td><td><code class="literal">= (int2,int2)</code></td></tr><tr><td><code class="literal">&lt; (int2,int2)</code></td></tr><tr><td><code class="literal">&gt; (int2,int2)</code></td></tr><tr><td><code class="literal">&lt;= (int2,int2)</code></td></tr><tr><td><code class="literal">&gt;= (int2,int2)</code></td></tr><tr><td valign="middle"><code class="literal">int4_bloom_ops</code></td><td><code class="literal">= (int4,int4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int4_minmax_ops</code></td><td><code class="literal">= (int4,int4)</code></td></tr><tr><td><code class="literal">&lt; (int4,int4)</code></td></tr><tr><td><code class="literal">&gt; (int4,int4)</code></td></tr><tr><td><code class="literal">&lt;= (int4,int4)</code></td></tr><tr><td><code class="literal">&gt;= (int4,int4)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int4_minmax_multi_ops</code></td><td><code class="literal">= (int4,int4)</code></td></tr><tr><td><code class="literal">&lt; (int4,int4)</code></td></tr><tr><td><code class="literal">&gt; (int4,int4)</code></td></tr><tr><td><code class="literal">&lt;= (int4,int4)</code></td></tr><tr><td><code class="literal">&gt;= (int4,int4)</code></td></tr><tr><td valign="middle"><code class="literal">int8_bloom_ops</code></td><td><code class="literal">= (bigint,bigint)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int8_minmax_ops</code></td><td><code class="literal">= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt;= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt;= (bigint,bigint)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">int8_minmax_multi_ops</code></td><td><code class="literal">= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt; (bigint,bigint)</code></td></tr><tr><td><code class="literal">&lt;= (bigint,bigint)</code></td></tr><tr><td><code class="literal">&gt;= (bigint,bigint)</code></td></tr><tr><td valign="middle"><code class="literal">interval_bloom_ops</code></td><td><code class="literal">= (interval,interval)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">interval_minmax_ops</code></td><td><code class="literal">= (interval,interval)</code></td></tr><tr><td><code class="literal">&lt; (interval,interval)</code></td></tr><tr><td><code class="literal">&lt;= (interval,interval)</code></td></tr><tr><td><code class="literal">&gt; (interval,interval)</code></td></tr><tr><td><code class="literal">&gt;= (interval,interval)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">interval_minmax_multi_ops</code></td><td><code class="literal">= (interval,interval)</code></td></tr><tr><td><code class="literal">&lt; (interval,interval)</code></td></tr><tr><td><code class="literal">&lt;= (interval,interval)</code></td></tr><tr><td><code class="literal">&gt; (interval,interval)</code></td></tr><tr><td><code class="literal">&gt;= (interval,interval)</code></td></tr><tr><td valign="middle"><code class="literal">macaddr_bloom_ops</code></td><td><code class="literal">= (macaddr,macaddr)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr_minmax_ops</code></td><td><code class="literal">= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr,macaddr)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr_minmax_multi_ops</code></td><td><code class="literal">= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt; (macaddr,macaddr)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr,macaddr)</code></td></tr><tr><td valign="middle"><code class="literal">macaddr8_bloom_ops</code></td><td><code class="literal">= (macaddr8,macaddr8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr8_minmax_ops</code></td><td><code class="literal">= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr8,macaddr8)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">macaddr8_minmax_multi_ops</code></td><td><code class="literal">= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&lt;= (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt; (macaddr8,macaddr8)</code></td></tr><tr><td><code class="literal">&gt;= (macaddr8,macaddr8)</code></td></tr><tr><td valign="middle"><code class="literal">name_bloom_ops</code></td><td><code class="literal">= (name,name)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">name_minmax_ops</code></td><td><code class="literal">= (name,name)</code></td></tr><tr><td><code class="literal">&lt; (name,name)</code></td></tr><tr><td><code class="literal">&lt;= (name,name)</code></td></tr><tr><td><code class="literal">&gt; (name,name)</code></td></tr><tr><td><code class="literal">&gt;= (name,name)</code></td></tr><tr><td valign="middle"><code class="literal">numeric_bloom_ops</code></td><td><code class="literal">= (numeric,numeric)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">numeric_minmax_ops</code></td><td><code class="literal">= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt;= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt;= (numeric,numeric)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">numeric_minmax_multi_ops</code></td><td><code class="literal">= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&lt;= (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt; (numeric,numeric)</code></td></tr><tr><td><code class="literal">&gt;= (numeric,numeric)</code></td></tr><tr><td valign="middle"><code class="literal">oid_bloom_ops</code></td><td><code class="literal">= (oid,oid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">oid_minmax_ops</code></td><td><code class="literal">= (oid,oid)</code></td></tr><tr><td><code class="literal">&lt; (oid,oid)</code></td></tr><tr><td><code class="literal">&gt; (oid,oid)</code></td></tr><tr><td><code class="literal">&lt;= (oid,oid)</code></td></tr><tr><td><code class="literal">&gt;= (oid,oid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">oid_minmax_multi_ops</code></td><td><code class="literal">= (oid,oid)</code></td></tr><tr><td><code class="literal">&lt; (oid,oid)</code></td></tr><tr><td><code class="literal">&gt; (oid,oid)</code></td></tr><tr><td><code class="literal">&lt;= (oid,oid)</code></td></tr><tr><td><code class="literal">&gt;= (oid,oid)</code></td></tr><tr><td valign="middle"><code class="literal">pg_lsn_bloom_ops</code></td><td><code class="literal">= (pg_lsn,pg_lsn)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">pg_lsn_minmax_ops</code></td><td><code class="literal">= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">pg_lsn_minmax_multi_ops</code></td><td><code class="literal">= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt; (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&lt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td><code class="literal">&gt;= (pg_lsn,pg_lsn)</code></td></tr><tr><td rowspan="14" valign="middle"><code class="literal">range_inclusion_ops</code></td><td><code class="literal">= (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;= (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&gt;= (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&amp; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange,anyelement)</code></td></tr><tr><td><code class="literal">@&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;@ (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&lt;&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&gt;&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&lt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">&amp;&gt; (anyrange,anyrange)</code></td></tr><tr><td><code class="literal">-|- (anyrange,anyrange)</code></td></tr><tr><td valign="middle"><code class="literal">text_bloom_ops</code></td><td><code class="literal">= (text,text)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">text_minmax_ops</code></td><td><code class="literal">= (text,text)</code></td></tr><tr><td><code class="literal">&lt; (text,text)</code></td></tr><tr><td><code class="literal">&lt;= (text,text)</code></td></tr><tr><td><code class="literal">&gt; (text,text)</code></td></tr><tr><td><code class="literal">&gt;= (text,text)</code></td></tr><tr><td valign="middle"><code class="literal">tid_bloom_ops</code></td><td><code class="literal">= (tid,tid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">tid_minmax_ops</code></td><td><code class="literal">= (tid,tid)</code></td></tr><tr><td><code class="literal">&lt; (tid,tid)</code></td></tr><tr><td><code class="literal">&gt; (tid,tid)</code></td></tr><tr><td><code class="literal">&lt;= (tid,tid)</code></td></tr><tr><td><code class="literal">&gt;= (tid,tid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">tid_minmax_multi_ops</code></td><td><code class="literal">= (tid,tid)</code></td></tr><tr><td><code class="literal">&lt; (tid,tid)</code></td></tr><tr><td><code class="literal">&gt; (tid,tid)</code></td></tr><tr><td><code class="literal">&lt;= (tid,tid)</code></td></tr><tr><td><code class="literal">&gt;= (tid,tid)</code></td></tr><tr><td valign="middle"><code class="literal">timestamp_bloom_ops</code></td><td><code class="literal">= (timestamp,timestamp)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamp_minmax_ops</code></td><td><code class="literal">= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt;= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt;= (timestamp,timestamp)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamp_minmax_multi_ops</code></td><td><code class="literal">= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&lt;= (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt; (timestamp,timestamp)</code></td></tr><tr><td><code class="literal">&gt;= (timestamp,timestamp)</code></td></tr><tr><td valign="middle"><code class="literal">timestamptz_bloom_ops</code></td><td><code class="literal">= (timestamptz,timestamptz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamptz_minmax_ops</code></td><td><code class="literal">= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt;= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt;= (timestamptz,timestamptz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timestamptz_minmax_multi_ops</code></td><td><code class="literal">= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&lt;= (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt; (timestamptz,timestamptz)</code></td></tr><tr><td><code class="literal">&gt;= (timestamptz,timestamptz)</code></td></tr><tr><td valign="middle"><code class="literal">time_bloom_ops</code></td><td><code class="literal">= (time,time)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">time_minmax_ops</code></td><td><code class="literal">= (time,time)</code></td></tr><tr><td><code class="literal">&lt; (time,time)</code></td></tr><tr><td><code class="literal">&lt;= (time,time)</code></td></tr><tr><td><code class="literal">&gt; (time,time)</code></td></tr><tr><td><code class="literal">&gt;= (time,time)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">time_minmax_multi_ops</code></td><td><code class="literal">= (time,time)</code></td></tr><tr><td><code class="literal">&lt; (time,time)</code></td></tr><tr><td><code class="literal">&lt;= (time,time)</code></td></tr><tr><td><code class="literal">&gt; (time,time)</code></td></tr><tr><td><code class="literal">&gt;= (time,time)</code></td></tr><tr><td valign="middle"><code class="literal">timetz_bloom_ops</code></td><td><code class="literal">= (timetz,timetz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timetz_minmax_ops</code></td><td><code class="literal">= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt;= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt;= (timetz,timetz)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">timetz_minmax_multi_ops</code></td><td><code class="literal">= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&lt;= (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt; (timetz,timetz)</code></td></tr><tr><td><code class="literal">&gt;= (timetz,timetz)</code></td></tr><tr><td valign="middle"><code class="literal">uuid_bloom_ops</code></td><td><code class="literal">= (uuid,uuid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">uuid_minmax_ops</code></td><td><code class="literal">= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt;= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt;= (uuid,uuid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">uuid_minmax_multi_ops</code></td><td><code class="literal">= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt; (uuid,uuid)</code></td></tr><tr><td><code class="literal">&lt;= (uuid,uuid)</code></td></tr><tr><td><code class="literal">&gt;= (uuid,uuid)</code></td></tr><tr><td rowspan="5" valign="middle"><code class="literal">varbit_minmax_ops</code></td><td><code class="literal">= (varbit,varbit)</code></td></tr><tr><td><code class="literal">&lt; (varbit,varbit)</code></td></tr><tr><td><code class="literal">&gt; (varbit,varbit)</code></td></tr><tr><td><code class="literal">&lt;= (varbit,varbit)</code></td></tr><tr><td><code class="literal">&gt;= (varbit,varbit)</code></td></tr></tbody></table>

<br><a id="BRIN-BUILTIN-OPCLASSES--PARAMETERS"></a>

#### 65.5.2.1. Operator Class Parameters [#](#BRIN-BUILTIN-OPCLASSES--PARAMETERS)

Some of the built-in operator classes allow specifying parameters affecting
behavior of the operator class. Each operator class has its own set of
allowed parameters. Only the `bloom` and `minmax-multi`
operator classes allow specifying parameters:

bloom operator classes accept these parameters:

`n_distinct_per_range`
:   Defines the estimated number of distinct non-null values in the block
    range, used by BRIN bloom indexes for sizing of the
    Bloom filter. It behaves similarly to `n_distinct` option
    for [ALTER TABLE](../../reference/sql-commands/sql-altertable.md). When set to a positive value,
    each block range is assumed to contain this number of distinct non-null
    values. When set to a negative value, which must be greater than or
    equal to -1, the number of distinct non-null values is assumed to grow linearly with
    the maximum possible number of tuples in the block range (about 290
    rows per block). The default value is `-0.1`, and
    the minimum number of distinct non-null values is `16`.

`false_positive_rate`
:   Defines the desired false positive rate used by BRIN
    bloom indexes for sizing of the Bloom filter. The values must be
    between 0.0001 and 0.25. The default value is 0.01, which is 1% false
    positive rate.

minmax-multi operator classes accept these parameters:

`values_per_range`
:   Defines the maximum number of values stored by BRIN
    minmax indexes to summarize a block range. Each value may represent
    either a point, or a boundary of an interval. Values must be between
    8 and 256, and the default value is 32.

<a id="BRIN-EXTENSIBILITY"></a>

### 65.5.3. Extensibility [#](#BRIN-EXTENSIBILITY)

The BRIN interface has a high level of abstraction,
requiring the access method implementer only to implement the semantics
of the data type being accessed. The BRIN layer
itself takes care of concurrency, logging and searching the index structure.

All it takes to get a BRIN access method working is to
implement a few user-defined methods, which define the behavior of
summary values stored in the index and the way they interact with
scan keys.
In short, BRIN combines
extensibility with generality, code reuse, and a clean interface.

There are four methods that an operator class for BRIN
must provide:

`BrinOpcInfo *opcInfo(Oid type_oid)`
:   Returns internal information about the indexed columns' summary data.
    The return value must point to a palloc'd `BrinOpcInfo`,
    which has this definition:

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

    `BrinOpcInfo`.`oi_opaque` can be used by the
    operator class routines to pass information between support functions
    during an index scan.

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey *keys, int nkeys)`
:   Returns whether all the ScanKey entries are consistent with the given
    indexed values for a range.
    The attribute number to use is passed as part of the scan key.
    Multiple scan keys for the same attribute may be passed at once; the
    number of entries is determined by the `nkeys` parameter.

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey key)`
:   Returns whether the ScanKey is consistent with the given indexed
    values for a range.
    The attribute number to use is passed as part of the scan key.
    This is an older backward-compatible variant of the consistent function.

`bool addValue(BrinDesc *bdesc, BrinValues *column, Datum newval, bool isnull)`
:   Given an index tuple and an indexed value, modifies the indicated
    attribute of the tuple so that it additionally represents the new value.
    If any modification was done to the tuple, `true` is
    returned.

`bool unionTuples(BrinDesc *bdesc, BrinValues *a, BrinValues *b)`
:   Consolidates two index tuples. Given two index tuples, modifies the
    indicated attribute of the first of them so that it represents both tuples.
    The second tuple is not modified.

An operator class for BRIN can optionally specify the
following method:

`void options(local_relopts *relopts)`
:   Defines a set of user-visible parameters that control operator class
    behavior.

    The `options` function is passed a pointer to a
    `local_relopts` struct, which needs to be
    filled with a set of operator class specific options. The options
    can be accessed from other support functions using the
    `PG_HAS_OPCLASS_OPTIONS()` and
    `PG_GET_OPCLASS_OPTIONS()` macros.

    Since both key extraction of indexed values and representation of the
    key in BRIN are flexible, they may depend on
    user-specified parameters.

The core distribution includes support for four types of operator classes:
minmax, minmax-multi, inclusion and bloom. Operator class definitions
using them are shipped for in-core data types as appropriate. Additional
operator classes can be defined by the user for other data types using
equivalent definitions, without having to write any source code;
appropriate catalog entries being declared is enough. Note that
assumptions about the semantics of operator strategies are embedded in the
support functions' source code.

Operator classes that implement completely different semantics are also
possible, provided implementations of the four main support functions
described above are written. Note that backwards compatibility across major
releases is not guaranteed: for example, additional support functions might
be required in later releases.

To write an operator class for a data type that implements a totally
ordered set, it is possible to use the minmax support functions
alongside the corresponding operators, as shown in
[Table 65.5](brin.md#BRIN-EXTENSIBILITY-MINMAX-TABLE).
All operator class members (functions and operators) are mandatory.

<a id="BRIN-EXTENSIBILITY-MINMAX-TABLE"></a>

**Table 65.5. Function and Support Numbers for Minmax Operator Classes**

<table border="1" class="table" summary="Function and Support Numbers for Minmax Operator Classes"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Operator class member</th><th>Object</th></tr></thead><tbody><tr><td>Support Function 1</td><td>internal function <code class="function">brin_minmax_opcinfo()</code></td></tr><tr><td>Support Function 2</td><td>internal function <code class="function">brin_minmax_add_value()</code></td></tr><tr><td>Support Function 3</td><td>internal function <code class="function">brin_minmax_consistent()</code></td></tr><tr><td>Support Function 4</td><td>internal function <code class="function">brin_minmax_union()</code></td></tr><tr><td>Operator Strategy 1</td><td>operator less-than</td></tr><tr><td>Operator Strategy 2</td><td>operator less-than-or-equal-to</td></tr><tr><td>Operator Strategy 3</td><td>operator equal-to</td></tr><tr><td>Operator Strategy 4</td><td>operator greater-than-or-equal-to</td></tr><tr><td>Operator Strategy 5</td><td>operator greater-than</td></tr></tbody></table>

<br>

To write an operator class for a complex data type which has values
included within another type, it's possible to use the inclusion support
functions alongside the corresponding operators, as shown
in [Table 65.6](brin.md#BRIN-EXTENSIBILITY-INCLUSION-TABLE). It requires
only a single additional function, which can be written in any language.
More functions can be defined for additional functionality. All operators
are optional. Some operators require other operators, as shown as
dependencies on the table.

<a id="BRIN-EXTENSIBILITY-INCLUSION-TABLE"></a>

**Table 65.6. Function and Support Numbers for Inclusion Operator Classes**

<table border="1" class="table" summary="Function and Support Numbers for Inclusion Operator Classes"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>Operator class member</th><th>Object</th><th>Dependency</th></tr></thead><tbody><tr><td>Support Function 1</td><td>internal function <code class="function">brin_inclusion_opcinfo()</code></td><td> </td></tr><tr><td>Support Function 2</td><td>internal function <code class="function">brin_inclusion_add_value()</code></td><td> </td></tr><tr><td>Support Function 3</td><td>internal function <code class="function">brin_inclusion_consistent()</code></td><td> </td></tr><tr><td>Support Function 4</td><td>internal function <code class="function">brin_inclusion_union()</code></td><td> </td></tr><tr><td>Support Function 11</td><td>function to merge two elements</td><td> </td></tr><tr><td>Support Function 12</td><td>optional function to check whether two elements are mergeable</td><td> </td></tr><tr><td>Support Function 13</td><td>optional function to check if an element is contained within another</td><td> </td></tr><tr><td>Support Function 14</td><td>optional function to check whether an element is empty</td><td> </td></tr><tr><td>Operator Strategy 1</td><td>operator left-of</td><td>Operator Strategy 4</td></tr><tr><td>Operator Strategy 2</td><td>operator does-not-extend-to-the-right-of</td><td>Operator Strategy 5</td></tr><tr><td>Operator Strategy 3</td><td>operator overlaps</td><td> </td></tr><tr><td>Operator Strategy 4</td><td>operator does-not-extend-to-the-left-of</td><td>Operator Strategy 1</td></tr><tr><td>Operator Strategy 5</td><td>operator right-of</td><td>Operator Strategy 2</td></tr><tr><td>Operator Strategy 6, 18</td><td>operator same-as-or-equal-to</td><td>Operator Strategy 7</td></tr><tr><td>Operator Strategy 7, 16, 24, 25</td><td>operator contains-or-equal-to</td><td> </td></tr><tr><td>Operator Strategy 8, 26, 27</td><td>operator is-contained-by-or-equal-to</td><td>Operator Strategy 3</td></tr><tr><td>Operator Strategy 9</td><td>operator does-not-extend-above</td><td>Operator Strategy 11</td></tr><tr><td>Operator Strategy 10</td><td>operator is-below</td><td>Operator Strategy 12</td></tr><tr><td>Operator Strategy 11</td><td>operator is-above</td><td>Operator Strategy 9</td></tr><tr><td>Operator Strategy 12</td><td>operator does-not-extend-below</td><td>Operator Strategy 10</td></tr><tr><td>Operator Strategy 20</td><td>operator less-than</td><td>Operator Strategy 5</td></tr><tr><td>Operator Strategy 21</td><td>operator less-than-or-equal-to</td><td>Operator Strategy 5</td></tr><tr><td>Operator Strategy 22</td><td>operator greater-than</td><td>Operator Strategy 1</td></tr><tr><td>Operator Strategy 23</td><td>operator greater-than-or-equal-to</td><td>Operator Strategy 1</td></tr></tbody></table>

<br>

Support function numbers 1 through 10 are reserved for the BRIN internal
functions, so the SQL level functions start with number 11. Support
function number 11 is the main function required to build the index.
It should accept two arguments with the same data type as the operator class,
and return the union of them. The inclusion operator class can store union
values with different data types if it is defined with the
`STORAGE` parameter. The return value of the union
function should match the `STORAGE` data type.

Support function numbers 12 and 14 are provided to support
irregularities of built-in data types. Function number 12
is used to support network addresses from different families which
are not mergeable. Function number 14 is used to support
empty ranges. Function number 13 is an optional but
recommended one, which allows the new value to be checked before
it is passed to the union function. As the BRIN framework can shortcut
some operations when the union is not changed, using this
function can improve index performance.

To write an operator class for a data type that implements only an equality
operator and supports hashing, it is possible to use the bloom support procedures
alongside the corresponding operators, as shown in
[Table 65.7](brin.md#BRIN-EXTENSIBILITY-BLOOM-TABLE).
All operator class members (procedures and operators) are mandatory.

<a id="BRIN-EXTENSIBILITY-BLOOM-TABLE"></a>

**Table 65.7. Procedure and Support Numbers for Bloom Operator Classes**

<table border="1" class="table" summary="Procedure and Support Numbers for Bloom Operator Classes"><colgroup><col/><col/></colgroup><thead><tr><th>Operator class member</th><th>Object</th></tr></thead><tbody><tr><td>Support Procedure 1</td><td>internal function <code class="function">brin_bloom_opcinfo()</code></td></tr><tr><td>Support Procedure 2</td><td>internal function <code class="function">brin_bloom_add_value()</code></td></tr><tr><td>Support Procedure 3</td><td>internal function <code class="function">brin_bloom_consistent()</code></td></tr><tr><td>Support Procedure 4</td><td>internal function <code class="function">brin_bloom_union()</code></td></tr><tr><td>Support Procedure 5</td><td>internal function <code class="function">brin_bloom_options()</code></td></tr><tr><td>Support Procedure 11</td><td>function to compute hash of an element</td></tr><tr><td>Operator Strategy 1</td><td>operator equal-to</td></tr></tbody></table>

<br>

Support procedure numbers 1-10 are reserved for the BRIN internal
functions, so the SQL level functions start with number 11. Support
function number 11 is the main function required to build the index.
It should accept one argument with the same data type as the operator class,
and return a hash of the value.

The minmax-multi operator class is also intended for data types implementing
a totally ordered set, and may be seen as a simple extension of the minmax
operator class. While minmax operator class summarizes values from each block
range into a single contiguous interval, minmax-multi allows summarization
into multiple smaller intervals to improve handling of outlier values.
It is possible to use the minmax-multi support procedures alongside the
corresponding operators, as shown in
[Table 65.8](brin.md#BRIN-EXTENSIBILITY-MINMAX-MULTI-TABLE).
All operator class members (procedures and operators) are mandatory.

<a id="BRIN-EXTENSIBILITY-MINMAX-MULTI-TABLE"></a>

**Table 65.8. Procedure and Support Numbers for minmax-multi Operator Classes**

<table border="1" class="table" summary="Procedure and Support Numbers for minmax-multi Operator Classes"><colgroup><col/><col/></colgroup><thead><tr><th>Operator class member</th><th>Object</th></tr></thead><tbody><tr><td>Support Procedure 1</td><td>internal function <code class="function">brin_minmax_multi_opcinfo()</code></td></tr><tr><td>Support Procedure 2</td><td>internal function <code class="function">brin_minmax_multi_add_value()</code></td></tr><tr><td>Support Procedure 3</td><td>internal function <code class="function">brin_minmax_multi_consistent()</code></td></tr><tr><td>Support Procedure 4</td><td>internal function <code class="function">brin_minmax_multi_union()</code></td></tr><tr><td>Support Procedure 5</td><td>internal function <code class="function">brin_minmax_multi_options()</code></td></tr><tr><td>Support Procedure 11</td><td>function to compute distance between two values (length of a range)</td></tr><tr><td>Operator Strategy 1</td><td>operator less-than</td></tr><tr><td>Operator Strategy 2</td><td>operator less-than-or-equal-to</td></tr><tr><td>Operator Strategy 3</td><td>operator equal-to</td></tr><tr><td>Operator Strategy 4</td><td>operator greater-than-or-equal-to</td></tr><tr><td>Operator Strategy 5</td><td>operator greater-than</td></tr></tbody></table>

<br>

Both minmax and inclusion operator classes support cross-data-type
operators, though with these the dependencies become more complicated.
The minmax operator class requires a full set of operators to be
defined with both arguments having the same data type. It allows
additional data types to be supported by defining extra sets
of operators. Inclusion operator class operator strategies are dependent
on another operator strategy as shown in
[Table 65.6](brin.md#BRIN-EXTENSIBILITY-INCLUSION-TABLE), or the same
operator strategy as themselves. They require the dependency
operator to be defined with the `STORAGE` data type as the
left-hand-side argument and the other supported data type to be the
right-hand-side argument of the supported operator. See
`float4_minmax_ops` as an example of minmax, and
`box_inclusion_ops` as an example of inclusion.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/brin.html)（英文原文，待翻譯）
