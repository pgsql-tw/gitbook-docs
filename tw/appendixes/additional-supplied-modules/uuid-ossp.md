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
        <p>Generates a version 3 UUID in the given namespace using the specified
          input name. The namespace should be one of the special constants produced
          by the <code>uuid_ns_*()</code> functions shown in <a href="https://www.postgresql.org/docs/13/uuid-ossp.html#UUID-OSSP-CONSTANTS">Table F.33</a>.
          (It could be any UUID in theory.) The name is an identifier in the selected
          namespace.</p>
        <p>For example:</p>
        <p>The name parameter will be MD5-hashed, so the cleartext cannot be derived
          from the generated UUID. The generation of UUIDs by this method has no
          random or environment-dependent element and is therefore reproducible.</p>
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
        <p>Generates a version 5 UUID, which works like a version 3 UUID except that
          SHA-1 is used as a hashing method. Version 5 should be preferred over version
          3 because SHA-1 is thought to be more secure than MD5.</p>
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

