# F.44. uuid-ossp

The `uuid-ossp` module provides functions to generate universally unique identifiers \(UUIDs\) using one of several standard algorithms. There are also functions to produce certain special UUID constants. This module is only necessary for special requirements beyond what is available in core PostgreSQL. See [Section 9.14](https://www.postgresql.org/docs/13/functions-uuid.html) for built-in ways to generate UUIDs.

This module is considered “trusted”, that is, it can be installed by non-superusers who have `CREATE` privilege on the current database.

## F.44.1. `uuid-ossp` Functions

[Table F.32](https://www.postgresql.org/docs/13/uuid-ossp.html#UUID-OSSP-FUNCTIONS) shows the functions available to generate UUIDs. The relevant standards ITU-T Rec. X.667, ISO/IEC 9834-8:2005, and RFC 4122 specify four algorithms for generating UUIDs, identified by the version numbers 1, 3, 4, and 5. \(There is no version 2 algorithm.\) Each of these algorithms could be suitable for a different set of applications.

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
        <p>Generates a version 1 UUID. This involves the MAC address of the computer
          and a time stamp. Note that UUIDs of this kind reveal the identity of the
          computer that created the identifier and the time at which it did so, which
          might make it unsuitable for certain security-sensitive applications.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_generate_v1mc</code> () &#x2192; <code>uuid</code>
        </p>
        <p>Generates a version 1 UUID, but uses a random multicast MAC address instead
          of the real MAC address of the computer.</p>
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
        <p>&#x4F8B;&#x5982;&#xFF1A;</p>
        <p>&#x53C3;&#x6578; name &#x5C07;&#x70BA; MD5 &#x96DC;&#x6E4A;&#x503C;&#xFF0C;&#x56E0;&#x6B64;&#x7121;&#x6CD5;&#x5F9E;&#x7522;&#x751F;&#x7684;
          UUID &#x53CD;&#x63A8;&#x539F;&#x4F86;&#x7684;&#x5167;&#x5BB9;&#x3002;&#x900F;&#x904E;&#x9019;&#x7A2E;&#x65B9;&#x6CD5;&#x7522;&#x751F;&#x7684;
          UUID &#x4E26;&#x6C92;&#x6709;&#x96A8;&#x6A5F;&#x6216;&#x8207;&#x74B0;&#x5883;&#x76F8;&#x95DC;&#x7684;&#x5143;&#x7D20;&#xFF0C;&#x56E0;&#x6B64;&#x662F;&#x53EF;&#x91CD;&#x73FE;&#x7684;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_generate_v4</code> () &#x2192; <code>uuid</code>
        </p>
        <p>Generates a version 4 UUID, which is derived entirely from random numbers.</p>
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

## **Table F.33. Functions Returning UUID Constants**

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
        <p>Returns a &#x201C;nil&#x201D; UUID constant, which does not occur as a
          real UUID.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_dns</code> () &#x2192; <code>uuid</code>
        </p>
        <p>Returns a constant designating the DNS namespace for UUIDs.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_url</code> () &#x2192; <code>uuid</code>
        </p>
        <p>Returns a constant designating the URL namespace for UUIDs.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_oid</code> () &#x2192; <code>uuid</code>
        </p>
        <p>Returns a constant designating the ISO object identifier (OID) namespace
          for UUIDs. (This pertains to ASN.1 OIDs, which are unrelated to the OIDs
          used in PostgreSQL.)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>uuid_ns_x500</code> () &#x2192; <code>uuid</code>
        </p>
        <p>Returns a constant designating the X.500 distinguished name (DN) namespace
          for UUIDs.</p>
      </td>
    </tr>
  </tbody>
</table>

## F.44.2. Building `uuid-ossp`

Historically this module depended on the OSSP UUID library, which accounts for the module's name. While the OSSP UUID library can still be found at [http://www.ossp.org/pkg/lib/uuid/](http://www.ossp.org/pkg/lib/uuid/), it is not well maintained, and is becoming increasingly difficult to port to newer platforms. `uuid-ossp` can now be built without the OSSP library on some platforms. On FreeBSD, NetBSD, and some other BSD-derived platforms, suitable UUID creation functions are included in the core `libc` library. On Linux, macOS, and some other platforms, suitable functions are provided in the `libuuid` library, which originally came from the `e2fsprogs` project \(though on modern Linux it is considered part of `util-linux-ng`\). When invoking `configure`, specify `--with-uuid=bsd` to use the BSD functions, or `--with-uuid=e2fs` to use `e2fsprogs`' `libuuid`, or `--with-uuid=ossp` to use the OSSP UUID library. More than one of these libraries might be available on a particular machine, so `configure` does not automatically choose one.

## F.44.3. Author

Peter Eisentraut `<`[`peter_e@gmx.net`](mailto:peter_e@gmx.net)`>`

