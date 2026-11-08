# 9.27.9. 已提交交易資訊函式

<a id="FUNCTIONS-INFO-COMMIT-TIMESTAMP"></a>

## 9.27.9. 已提交交易資訊函式 [#](#functions-info-commit-timestamp) <a href="#functions-info-commit-timestamp" id="functions-info-commit-timestamp"></a>

[表 9.87](#functions-commit-timestamp) 所列的函式提供過去的交易是在何時提交的資訊。只有在啟用了 [track_commit_timestamp](../../../server-administration/runtime-config/runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) 組態選項時，它們才會提供有用的資料，而且只適用於啟用該選項之後才提交的交易。提交時間戳記資訊會在 vacuum 期間例行性地移除。

<a id="FUNCTIONS-COMMIT-TIMESTAMP"></a>

### 表 9.87. 已提交交易資訊函式 [#](#functions-commit-timestamp) <a href="#functions-commit-timestamp" id="functions-commit-timestamp"></a>

<table border="1" class="table" summary="Committed Transaction Information Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.1.1.1.1"></a>
<code class="function">pg_xact_commit_timestamp</code> ( <code class="type">xid</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        回傳交易的提交時間戳記。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.2.1.1.1"></a>
<code class="function">pg_xact_commit_timestamp_origin</code> ( <code class="type">xid</code> )
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>timestamp</code></em> <code class="type">timestamp with time zone</code>,
         <em class="parameter"><code>roident</code></em> <code class="type">oid</code>)
       </p>
<p>
         回傳交易的提交時間戳記與複寫來源（replication origin）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.33.11.3.2.2.3.1.1.1"></a>
<code class="function">pg_last_committed_xact</code> ()
        → <code class="returnvalue">record</code>
        ( <em class="parameter"><code>xid</code></em> <code class="type">xid</code>,
        <em class="parameter"><code>timestamp</code></em> <code class="type">timestamp with time zone</code>,
        <em class="parameter"><code>roident</code></em> <code class="type">oid</code> )
       </p>
<p>
        回傳最近一個已提交交易的交易 ID、提交時間戳記與複寫來源。
       </p></td></tr></tbody></table>

<br>

[返回 9.27. 系統資訊函式與運算子](../functions-info.md#functions-info)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-info.html)（原文版本：18.6；核對日期：2026-09-11）
