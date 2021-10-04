# F.44. uuid-ossp

uuid-ossp 模組提供了使用幾種標準演算法來產生 Universally Unique IDentifiers \(UUIDs\) 的功能。還有一些函數可以產生某些特殊的 UUID 常數。此模組僅在 PostgreSQL 中特殊需求時才需要。有關產生 UUID 的內建函數，請參閱[第 9.14 節](../../the-sql-language/functions-and-operators/uuid-functions.md)。

該模組被認為是「可信任的」，也就是說，它可以由對目前資料庫具有 CREATE 權限的非超級使用者安裝。

## F.44.1. `uuid-ossp` Functions

[Table F.32](uuid-ossp.md#table-f-32-functions-for-uuid-generation) 列出了可用於產生 UUID 的函數。相關標準為 ITU-T Rec. X.667、ISO/IEC 9834-8:2005 和 RFC 4122 所指定的四種用於產生 UUID 的演算法，由標示為版本號 1、3、4 和 5 。（沒有版本 2 。）這些演算法可能適用於不同的應用情境。

#### **Table F.32. Functions for UUID Generation**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_generate_v1</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x7248;&#x672C; 1 UUID&#x3002; &#x9019;&#x6D89;&#x53CA;&#x4E3B;&#x6A5F;&#x7684;
          MAC &#x4F4D;&#x5740;&#x548C;&#x6642;&#x9593;&#x6233;&#x8A18;&#x3002;&#x8ACB;&#x6CE8;&#x610F;&#xFF0C;&#x6B64;&#x985E;
          UUID &#x6703;&#x986F;&#x793A;&#x5EFA;&#x7ACB;&#x8B58;&#x5225;&#x7B26;&#x7684;&#x4E3B;&#x6A5F;&#x8EAB;&#x4EFD;&#x53CA;&#x5176;&#x5EFA;&#x7ACB;&#x6642;&#x9593;&#xFF0C;&#x9019;&#x53EF;&#x80FD;&#x4F7F;&#x5176;&#x4E0D;&#x9069;&#x7528;&#x65BC;&#x67D0;&#x4E9B;&#x5C0D;&#x5B89;&#x5168;&#x654F;&#x611F;&#x7684;&#x61C9;&#x7528;&#x60C5;&#x5883;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_generate_v1mc</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x7522;&#x751F;&#x7248;&#x672C; 1 UUID&#xFF0C;&#x4F46;&#x4F7F;&#x7528;&#x96A8;&#x6A5F;&#x7684;
          multicast MAC &#x4F4D;&#x5740;&#x800C;&#x4E0D;&#x662F;&#x4E3B;&#x6A5F;&#x7684;&#x771F;&#x5BE6;
          MAC &#x4F4D;&#x5740;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_generate_v3</code> ( <em><code>namespace</code></em>  <code>uuid</code>, <em><code>name</code></em>  <code>text</code> )
          &#x2192; <code>uuid</code>
        </p>
        <p>&#x4F7F;&#x7528;&#x6307;&#x5B9A;&#x7684;&#x8F38;&#x5165;&#x540D;&#x7A31;&#x5728;&#x7D66;&#x4E88;&#x7684;&#x547D;&#x540D;&#x7A7A;&#x9593;
          namespace &#x4E2D;&#x7522;&#x751F;&#x6210;&#x7248;&#x672C; 3 &#x7684; UUID&#x3002;&#x547D;&#x540D;&#x7A7A;&#x9593;&#x61C9;&#x8A72;&#x662F;
          <a
          href="uuid-ossp.md#table-f-33-functions-returning-uuid-constants">Table F.33</a>&#x4E2D;&#x5217;&#x51FA;&#x7684;&#x7684; uuid<em>ns</em>*()
            &#x51FD;&#x6578;&#x7522;&#x751F;&#x7684;&#x7279;&#x6B8A;&#x5E38;&#x6578;&#x4E4B;&#x4E00;&#x3002;&#xFF08;&#x7406;&#x8AD6;&#x4E0A;&#x53EF;&#x4EE5;&#x662F;&#x4EFB;&#x4F55;&#x7684;
            UUID&#x3002;&#xFF09;&#x540D;&#x7A31;&#x662F;&#x6240;&#x9078;&#x547D;&#x540D;&#x7A7A;&#x9593;&#x4E2D;&#x7684;&#x8B58;&#x5225;&#x5B57;&#x3002;</p>
        <p>&#x4F8B;&#x5982;&#xFF1A;
          <br />SELECT uuid_generate_v3(uuid_ns_url(), &apos;<a href="http://www.postgresql.org">http://www.postgresql.org</a>&apos;);</p>
        <p>&#x53C3;&#x6578; name &#x5C07;&#x70BA; MD5 &#x96DC;&#x6E4A;&#x503C;&#xFF0C;&#x56E0;&#x6B64;&#x7121;&#x6CD5;&#x5F9E;&#x7522;&#x751F;&#x7684;
          UUID &#x53CD;&#x63A8;&#x539F;&#x4F86;&#x7684;&#x5167;&#x5BB9;&#x3002;&#x900F;&#x904E;&#x9019;&#x7A2E;&#x65B9;&#x6CD5;&#x7522;&#x751F;&#x7684;
          UUID &#x4E26;&#x6C92;&#x6709;&#x96A8;&#x6A5F;&#x6216;&#x8207;&#x74B0;&#x5883;&#x76F8;&#x95DC;&#x7684;&#x5143;&#x7D20;&#xFF0C;&#x56E0;&#x6B64;&#x662F;&#x53EF;&#x91CD;&#x73FE;&#x7684;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_generate_v4</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x7522;&#x751F;&#x7248;&#x672C; 4 UUID&#xFF0C;&#x5B83;&#x5B8C;&#x5168;&#x4F86;&#x81EA;&#x4E82;&#x6578;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_generate_v5</code> ( <em><code>namespace</code></em>  <code>uuid</code>, <em><code>name</code></em>  <code>text</code> )
          &#x2192; <code>uuid</code>
        </p>
        <p>&#x7522;&#x751F;&#x7248;&#x672C; 5 &#x7684; UUID&#xFF0C;&#x6B64;&#x7248;&#x672C;&#x8207;&#x7248;&#x672C;
          3 UUID &#x985E;&#x4F3C;&#xFF0C;&#x4E0D;&#x540C;&#x4E4B;&#x8655;&#x5728;&#x65BC;&#x4EE5;
          SHA-1 &#x4F5C;&#x70BA;&#x96DC;&#x6E4A;&#x6F14;&#x7B97;&#x6CD5;&#x3002;&#x7248;&#x672C;
          5 &#x61C9;&#x8A72;&#x6BD4;&#x7248;&#x672C; 3 &#x66F4;&#x597D;&#xFF0C;&#x56E0;&#x70BA;
          SHA-1 &#x88AB;&#x8A8D;&#x70BA;&#x6BD4; MD5 &#x66F4;&#x52A0;&#x5B89;&#x5168;&#x3002;</p>
      </td>
    </tr>
  </tbody>
</table>

#### **Table F.33. Functions Returning UUID Constants**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Function</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_nil</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x56DE;&#x50B3;&#x4E00;&#x500B;&#x300C;nil&#x300D;UUID &#x5E38;&#x6578;&#xFF0C;&#x5B83;&#x4E0D;&#x6703;&#x7522;&#x751F;&#x70BA;&#x771F;&#x6B63;&#x7684;
          UUID&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_dns</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x56DE;&#x50B3;&#x4E00;&#x500B;&#x5E38;&#x6578;&#xFF0C;&#x70BA; UUID
          &#x6307;&#x5B9A;&#x70BA; DNS &#x7684;&#x547D;&#x540D;&#x7A7A;&#x9593;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_url</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x56DE;&#x50B3;&#x4E00;&#x500B;&#x5E38;&#x6578;&#xFF0C;&#x6307;&#x5B9A;
          UUID &#x70BA; URL &#x7684;&#x547D;&#x540D;&#x7A7A;&#x9593;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_oid</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x56DE;&#x50B3;&#x4E00;&#x500B;&#x5E38;&#x6578;&#xFF0C;&#x70BA; UUID
          &#x6307;&#x5B9A; ISO &#x7269;&#x4EF6;&#x8B58;&#x5225;&#x7B26;&#x865F; (OID)
          &#x7684;&#x547D;&#x540D;&#x7A7A;&#x9593;&#x3002; &#xFF08;&#x9019;&#x8207;
          ASN.1 OID &#x76F8;&#x95DC;&#xFF0C;&#x5B83;&#x8207; PostgreSQL &#x4E2D;&#x4F7F;&#x7528;&#x7684;
          OID &#x7121;&#x95DC;&#x3002;&#xFF09;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_x500</code> () &#x2192; <code>uuid</code>
        </p>
        <p>&#x56DE;&#x50B3;&#x6307;&#x5B9A; UUID &#x70BA; X.500 &#x5C08;&#x6709;&#x540D;&#x7A31;
          (DN) &#x547D;&#x540D;&#x7A7A;&#x9593;&#x7684;&#x5E38;&#x6578;&#x3002;</p>
      </td>
    </tr>
  </tbody>
</table>

## F.44.2. Building `uuid-ossp`

從歷史上看，這個模組相依於 OSSP UUID 函式庫，它也是模組名稱的由來。雖然 OSSP UUID 庫仍然可以在 [http://www.ossp.org/pkg/lib/uuid/](http://www.ossp.org/pkg/lib/uuid/) 找到，但它沒有得到很好的維護，並且越來越難以移植到更新的平台。uuid-ossp 現在可以在某些平台上在沒有 OSSP 函式庫的情況下編譯。在 FreeBSD、NetBSD 和其他一些 BSD 衍生平台上，核心 libc 函式庫中包含合適的 UUID 建立函數。在 Linux、macOS 和其他一些平台上，libuuid 函式庫中提供了合適的函數，該函式庫最初來自 e2fsprogs 專案（儘管在近代 Linux 上它被認為是 util-linux-ng 的一部分）。呼叫 configure 時，指定 --with-uuid=bsd 使用 BSD 函數，或 --with-uuid=e2fs 使用 e2fsprogs 的 libuuid，或 --with-uuid=ossp 使用 OSSP UUID 函式庫。在某些主機上可能有多種函式庫可用，因此 configure 並不會自動選擇。

## F.44.3. Author

Peter Eisentraut `<`[`peter_e@gmx.net`](mailto:peter_e@gmx.net)`>`

