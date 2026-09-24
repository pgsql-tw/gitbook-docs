<a id="RUNTIME-CONFIG-SHORT"></a>

## 19.18. 簡短選項 [#](#RUNTIME-CONFIG-SHORT)

為方便起見，部分參數也提供單一字母的命令列選項開關，
詳情請參閱[表 19.5](runtime-config-short.md#RUNTIME-CONFIG-SHORT-TABLE)。其中有些選項是基於歷史因素而存在，其以單一字母選項的形式出現，
並不代表認可大量使用該選項。

<a id="RUNTIME-CONFIG-SHORT-TABLE"></a>

**表 19.5. 簡短選項對照表**

<table border="1" class="table" summary="Short Option Key"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>簡短選項</th><th>等效設定</th></tr></thead><tbody><tr><td><code class="option">-B <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">shared_buffers = <em class="replaceable"><code>x</code></em></code></td></tr><tr><td><code class="option">-d <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">log_min_messages = DEBUG<em class="replaceable"><code>x</code></em></code></td></tr><tr><td><code class="option">-e</code></td><td><code class="literal">datestyle = euro</code></td></tr><tr><td>
<code class="option">-fb</code>, <code class="option">-fh</code>, <code class="option">-fi</code>,
          <code class="option">-fm</code>, <code class="option">-fn</code>, <code class="option">-fo</code>,
          <code class="option">-fs</code>, <code class="option">-ft</code>
</td><td>
<code class="literal">enable_bitmapscan = off</code>,
          <code class="literal">enable_hashjoin = off</code>,
          <code class="literal">enable_indexscan = off</code>,
          <code class="literal">enable_mergejoin = off</code>,
          <code class="literal">enable_nestloop = off</code>,
          <code class="literal">enable_indexonlyscan = off</code>,
          <code class="literal">enable_seqscan = off</code>,
          <code class="literal">enable_tidscan = off</code>
</td></tr><tr><td><code class="option">-F</code></td><td><code class="literal">fsync = off</code></td></tr><tr><td><code class="option">-h <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">listen_addresses = <em class="replaceable"><code>x</code></em></code></td></tr><tr><td><code class="option">-i</code></td><td><code class="literal">listen_addresses = '*'</code></td></tr><tr><td><code class="option">-k <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">unix_socket_directories = <em class="replaceable"><code>x</code></em></code></td></tr><tr><td><code class="option">-l</code></td><td><code class="literal">ssl = on</code></td></tr><tr><td><code class="option">-N <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">max_connections = <em class="replaceable"><code>x</code></em></code></td></tr><tr><td><code class="option">-O</code></td><td><code class="literal">allow_system_table_mods = on</code></td></tr><tr><td><code class="option">-p <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">port = <em class="replaceable"><code>x</code></em></code></td></tr><tr><td><code class="option">-P</code></td><td><code class="literal">ignore_system_indexes = on</code></td></tr><tr><td><code class="option">-s</code></td><td><code class="literal">log_statement_stats = on</code></td></tr><tr><td><code class="option">-S <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">work_mem = <em class="replaceable"><code>x</code></em></code></td></tr><tr><td><code class="option">-tpa</code>, <code class="option">-tpl</code>, <code class="option">-te</code></td><td><code class="literal">log_parser_stats = on</code>,
        <code class="literal">log_planner_stats = on</code>,
        <code class="literal">log_executor_stats = on</code></td></tr><tr><td><code class="option">-W <em class="replaceable"><code>x</code></em></code></td><td><code class="literal">post_auth_delay = <em class="replaceable"><code>x</code></em></code></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-short.html)（原文版本：18.6；核對日期：2026-09-24）
