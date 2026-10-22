<a id="UUID-OSSP"></a>

## F.49. uuid-ossp — UUID 產生器 [#](#UUID-OSSP)

[F.49.1. `uuid-ossp` 函式](uuid-ossp.md#UUID-OSSP-FUNCTIONS-SECT)

[F.49.2. 建置 `uuid-ossp`](uuid-ossp.md#UUID-OSSP-BUILDING)

[F.49.3. 作者](uuid-ossp.md#UUID-OSSP-AUTHOR)

<a id="id-1.11.7.59.2"></a>

`uuid-ossp` 模組提供多個函式，可使用數種標準演算法之一產生通用唯一識別碼（UUID）。此外也有函式可產生某些特殊的 UUID 常數。只有在需求超出 PostgreSQL 核心所提供的功能時，才需要此模組。產生 UUID 的內建方式請參閱[第 9.14 節](../../the-sql-language/functions/functions-uuid.md)。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="UUID-OSSP-FUNCTIONS-SECT"></a>

### F.49.1. `uuid-ossp` 函式 [#](#UUID-OSSP-FUNCTIONS-SECT)

[表 F.35](uuid-ossp.md#UUID-OSSP-FUNCTIONS) 列出可用於產生 UUID 的函式。相關標準 ITU-T Rec. X.667、ISO/IEC 9834-8:2005 與 [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122) 規定了四種產生 UUID 的演算法，分別以版本號碼 1、3、4、5 識別。（沒有第 2 版演算法。）這些演算法各自可能適用於不同類型的應用程式。

<a id="UUID-OSSP-FUNCTIONS"></a>

**表 F.35. 產生 UUID 的函式**

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
        使用指定的輸入名稱，在給定的命名空間中產生第 3 版 UUID。命名空間應該是由 <code class="function">uuid_ns_*()</code> 函式（列於<a class="xref" href="uuid-ossp.md#UUID-OSSP-CONSTANTS">表 F.36</a>）所產生的特殊常數之一。（理論上它可以是任何 UUID。）名稱是所選命名空間中的識別碼。
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

**表 F.36. 傳回 UUID 常數的函式**

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

<a id="UUID-OSSP-BUILDING"></a>

### F.49.2. 建置 `uuid-ossp` [#](#UUID-OSSP-BUILDING)

過去此模組依賴 OSSP UUID 函式庫，這也是此模組名稱的由來。雖然 OSSP UUID 函式庫仍可在 <http://www.ossp.org/pkg/lib/uuid/> 找到，但它的維護狀況不佳，而且越來越難以移植到較新的平台。現在 `uuid-ossp` 在某些平台上可以不依賴 OSSP 函式庫建置。在 FreeBSD 與其他一些 BSD 衍生平台上，核心的 `libc` 函式庫已包含合適的 UUID 建立函式。在 Linux、macOS 與其他一些平台上，合適的函式由 `libuuid` 函式庫提供，該函式庫最初來自 `e2fsprogs` 專案（不過在現代的 Linux 上，它被視為 `util-linux-ng` 的一部分）。呼叫 `configure` 時，指定 `--with-uuid=bsd` 以使用 BSD 函式，或指定 `--with-uuid=e2fs` 以使用 `e2fsprogs` 的 `libuuid`，或指定 `--with-uuid=ossp` 以使用 OSSP UUID 函式庫。一部特定機器上可能有超過一個這類函式庫可用，因此 `configure` 不會自動選擇其中一個。

<a id="UUID-OSSP-AUTHOR"></a>

### F.49.3. 作者 [#](#UUID-OSSP-AUTHOR)

Peter Eisentraut `<peter_e@gmx.net>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/uuid-ossp.html)（原文版本：18.6；核對日期：2026-10-22）
