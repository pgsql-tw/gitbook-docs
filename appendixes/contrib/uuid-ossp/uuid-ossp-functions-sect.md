# F.49.1. uuid-ossp 函式

<a id="UUID-OSSP-FUNCTIONS-SECT"></a>

## F.49.1. `uuid-ossp` 函式 [#](#uuid-ossp-functions-sect) <a href="#uuid-ossp-functions-sect" id="uuid-ossp-functions-sect"></a>

[表 F.35](#uuid-ossp-functions) 列出可用於產生 UUID 的函式。相關標準 ITU-T Rec. X.667、ISO/IEC 9834-8:2005 與 [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122) 規定了四種產生 UUID 的演算法，分別以版本號碼 1、3、4、5 識別。（沒有第 2 版演算法。）這些演算法各自可能適用於不同類型的應用程式。

<a id="UUID-OSSP-FUNCTIONS"></a>

### 表 F.35. 產生 UUID 的函式 [#](#uuid-ossp-functions) <a href="#uuid-ossp-functions" id="uuid-ossp-functions"></a>

<table border="1" class="table" summary="產生 UUID 的函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.59.5.3.2.2.1.1.1.1"></a>
<code class="function">uuid_generate_v1</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        產生第 1 版 UUID。這會用到電腦的 MAC 位址與時間戳記。請注意，這類 UUID 會透露建立該識別碼的電腦身分以及建立的時間，因此可能不適合某些對安全性敏感的應用程式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.59.5.3.2.2.2.1.1.1"></a>
<code class="function">uuid_generate_v1mc</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        產生第 1 版 UUID，但使用隨機的多播 MAC 位址，而非電腦的實際 MAC 位址。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.59.5.3.2.2.3.1.1.1"></a>
<code class="function">uuid_generate_v3</code> ( <em class="parameter"><code>namespace</code></em> <code class="type">uuid</code>, <em class="parameter"><code>name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        使用指定的輸入名稱，在給定的命名空間中產生第 3 版 UUID。命名空間應該是由 <code class="function">uuid_ns_*()</code> 函式（列於<a class="xref" href="#uuid-ossp-constants">表 F.36</a>）所產生的特殊常數之一。（理論上它可以是任何 UUID。）名稱是所選命名空間中的識別碼。
       </p>
<p>
        例如：
</p><pre class="programlisting">
SELECT uuid_generate_v3(uuid_ns_url(), 'http://www.postgresql.org');
</pre><p>
        名稱參數會經過 MD5 雜湊，因此無法從產生的 UUID 推導出明文。以此方法產生 UUID 不含任何隨機或與環境相關的成分，因此是可重現的。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_generate_v4</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        產生第 4 版 UUID，它完全由隨機數衍生而來。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_generate_v5</code> ( <em class="parameter"><code>namespace</code></em> <code class="type">uuid</code>, <em class="parameter"><code>name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        產生第 5 版 UUID，其運作方式與第 3 版 UUID 相同，只是改用 SHA-1 作為雜湊方法。應該優先使用第 5 版而非第 3 版，因為一般認為 SHA-1 比 MD5 更安全。
       </p></td></tr></tbody></table>

<br><a id="UUID-OSSP-CONSTANTS"></a>

### 表 F.36. 傳回 UUID 常數的函式 [#](#uuid-ossp-constants) <a href="#uuid-ossp-constants" id="uuid-ossp-constants"></a>

<table border="1" class="table" summary="傳回 UUID 常數的函式"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_nil</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        傳回 <span class="quote">“<span class="quote">nil</span>”</span> UUID 常數，它不會作為真正的 UUID 出現。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_dns</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        傳回表示 UUID 之 DNS 命名空間的常數。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_url</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        傳回表示 UUID 之 URL 命名空間的常數。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_oid</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        傳回表示 UUID 之 ISO 物件識別碼（OID）命名空間的常數。（這指的是 ASN.1 OID，與 <span class="productname">PostgreSQL</span> 中使用的 OID 無關。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_x500</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        傳回表示 UUID 之 X.500 辨別名稱（DN）命名空間的常數。
       </p></td></tr></tbody></table>

<br>

[返回 F.49. uuid-ossp — UUID 產生器](../uuid-ossp.md#uuid-ossp)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/uuid-ossp.html)（原文版本：18.6；核對日期：2026-10-22）
