## F.49. uuid-ossp — a UUID generator [#](#UUID-OSSP)

[F.49.1. `uuid-ossp` Functions](uuid-ossp.md#UUID-OSSP-FUNCTIONS-SECT)

[F.49.2. Building `uuid-ossp`](uuid-ossp.md#UUID-OSSP-BUILDING)

[F.49.3. Author](uuid-ossp.md#UUID-OSSP-AUTHOR)

<a id="id-1.11.7.59.2"></a>

The `uuid-ossp` module provides functions to generate universally
unique identifiers (UUIDs) using one of several standard algorithms. There
are also functions to produce certain special UUID constants.
This module is only necessary for special requirements beyond what is
available in core PostgreSQL. See [Section 9.14](../../the-sql-language/functions/functions-uuid.md) for built-in ways to generate UUIDs.

This module is considered “trusted”, that is, it can be
installed by non-superusers who have `CREATE` privilege
on the current database.

<a id="UUID-OSSP-FUNCTIONS-SECT"></a>

### F.49.1. `uuid-ossp` Functions [#](#UUID-OSSP-FUNCTIONS-SECT)

[Table F.35](uuid-ossp.md#UUID-OSSP-FUNCTIONS) shows the functions available to
generate UUIDs.
The relevant standards ITU-T Rec. X.667, ISO/IEC 9834-8:2005, and
[RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122)
specify four algorithms for generating UUIDs, identified by the
version numbers 1, 3, 4, and 5. (There is no version 2 algorithm.)
Each of these algorithms could be suitable for a different set of
applications.

<a id="UUID-OSSP-FUNCTIONS"></a>

**Table F.35. Functions for UUID Generation**

<table border="1" class="table" summary="Functions for UUID Generation"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.59.5.3.2.2.1.1.1.1"></a>
<code class="function">uuid_generate_v1</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Generates a version 1 UUID.  This involves the MAC
        address of the computer and a time stamp.  Note that UUIDs of this
        kind reveal the identity of the computer that created the identifier
        and the time at which it did so, which might make it unsuitable for
        certain security-sensitive applications.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.59.5.3.2.2.2.1.1.1"></a>
<code class="function">uuid_generate_v1mc</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Generates a version 1 UUID, but uses a random multicast
        MAC address instead of the real MAC address of the computer.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.59.5.3.2.2.3.1.1.1"></a>
<code class="function">uuid_generate_v3</code> ( <em class="parameter"><code>namespace</code></em> <code class="type">uuid</code>, <em class="parameter"><code>name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Generates a version 3 UUID in the given namespace using
        the specified input name.  The namespace should be one of the special
        constants produced by the <code class="function">uuid_ns_*()</code> functions
        shown in <a class="xref" href="uuid-ossp.md#UUID-OSSP-CONSTANTS">Table F.36</a>.  (It could be any UUID
        in theory.)  The name is an identifier in the selected namespace.
       </p>
<p>
        For example:

</p><pre class="programlisting">
SELECT uuid_generate_v3(uuid_ns_url(), 'http://www.postgresql.org');
</pre><p>

        The name parameter will be MD5-hashed, so the cleartext cannot be
        derived from the generated UUID.
        The generation of UUIDs by this method has no random or
        environment-dependent element and is therefore reproducible.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_generate_v4</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Generates a version 4 UUID, which is derived entirely
        from random numbers.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_generate_v5</code> ( <em class="parameter"><code>namespace</code></em> <code class="type">uuid</code>, <em class="parameter"><code>name</code></em> <code class="type">text</code> )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Generates a version 5 UUID, which works like a version 3
        UUID except that SHA-1 is used as a hashing method.  Version 5 should
        be preferred over version 3 because SHA-1 is thought to be more secure
        than MD5.
       </p></td></tr></tbody></table>

<br><a id="UUID-OSSP-CONSTANTS"></a>

**Table F.36. Functions Returning UUID Constants**

<table border="1" class="table" summary="Functions Returning UUID Constants"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_nil</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Returns a <span class="quote">“<span class="quote">nil</span>”</span> UUID constant, which does not occur as a
        real UUID.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_dns</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Returns a constant designating the DNS namespace for UUIDs.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_url</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Returns a constant designating the URL namespace for UUIDs.
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_oid</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Returns a constant designating the ISO object identifier (OID) namespace for
        UUIDs.  (This pertains to ASN.1 OIDs, which are unrelated to the OIDs
        used in <span class="productname">PostgreSQL</span>.)
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_ns_x500</code> ()
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Returns a constant designating the X.500 distinguished name (DN)
        namespace for UUIDs.
       </p></td></tr></tbody></table>

<br>

<a id="UUID-OSSP-BUILDING"></a>

### F.49.2. Building `uuid-ossp` [#](#UUID-OSSP-BUILDING)

Historically this module depended on the OSSP UUID library, which accounts
for the module's name. While the OSSP UUID library can still be found
at <http://www.ossp.org/pkg/lib/uuid/>, it is not well
maintained, and is becoming increasingly difficult to port to newer
platforms. `uuid-ossp` can now be built without the OSSP
library on some platforms. On FreeBSD and some other BSD-derived
platforms, suitable UUID creation functions are included in the
core `libc` library. On Linux, macOS, and some other
platforms, suitable functions are provided in the `libuuid`
library, which originally came from the `e2fsprogs` project
(though on modern Linux it is considered part
of `util-linux-ng`). When invoking `configure`,
specify `--with-uuid=bsd` to use the BSD functions,
or `--with-uuid=e2fs` to
use `e2fsprogs`' `libuuid`, or
`--with-uuid=ossp` to use the OSSP UUID library.
More than one of these libraries might be available on a particular
machine, so `configure` does not automatically choose one.

<a id="UUID-OSSP-AUTHOR"></a>

### F.49.3. Author [#](#UUID-OSSP-AUTHOR)

Peter Eisentraut `<peter_e@gmx.net>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/uuid-ossp.html)（英文原文，待翻譯）
