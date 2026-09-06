## 9.12. Network Address Functions and Operators [#](#FUNCTIONS-NET)

The IP network address types, `cidr` and `inet`,
support the usual comparison operators shown in
[Table 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE)
as well as the specialized operators and functions shown in
[Table 9.39](functions-net.md#CIDR-INET-OPERATORS-TABLE) and
[Table 9.40](functions-net.md#CIDR-INET-FUNCTIONS-TABLE).

Any `cidr` value can be cast to `inet` implicitly;
therefore, the operators and functions shown below as operating on
`inet` also work on `cidr` values. (Where there are
separate functions for `inet` and `cidr`, it is
because the behavior should be different for the two cases.)
Also, it is permitted to cast an `inet` value
to `cidr`. When this is done, any bits to the right of the
netmask are silently zeroed to create a valid `cidr` value.

<a id="CIDR-INET-OPERATORS-TABLE"></a>

**Table 9.39. IP Address Operators**

<table border="1" class="table" summary="IP Address Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Operator
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&lt;&lt;</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is subnet strictly contained by subnet?
        This operator, and the next four, test for subnet inclusion.  They
        consider only the network parts of the two addresses (ignoring any
        bits to the right of the netmasks) and determine whether one network
        is identical to or a subnet of the other.
       </p>
<p>
<code class="literal">inet '192.168.1.5' &lt;&lt; inet '192.168.1/24'</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">inet '192.168.0.5' &lt;&lt; inet '192.168.1/24'</code>
        → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">inet '192.168.1/24' &lt;&lt; inet '192.168.1/24'</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&lt;&lt;=</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Is subnet contained by or equal to subnet?
       </p>
<p>
<code class="literal">inet '192.168.1/24' &lt;&lt;= inet '192.168.1/24'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&gt;&gt;</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does subnet strictly contain subnet?
       </p>
<p>
<code class="literal">inet '192.168.1/24' &gt;&gt; inet '192.168.1.5'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&gt;&gt;=</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does subnet contain or equal subnet?
       </p>
<p>
<code class="literal">inet '192.168.1/24' &gt;&gt;= inet '192.168.1/24'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&amp;&amp;</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Does either subnet contain or equal the other?
       </p>
<p>
<code class="literal">inet '192.168.1/24' &amp;&amp; inet '192.168.1.80/28'</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">inet '192.168.1/24' &amp;&amp; inet '192.168.2.0/28'</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">~</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        Computes bitwise NOT.
       </p>
<p>
<code class="literal">~ inet '192.168.1.6'</code>
        → <code class="returnvalue">63.87.254.249</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&amp;</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        Computes bitwise AND.
       </p>
<p>
<code class="literal">inet '192.168.1.6' &amp; inet '0.0.0.255'</code>
        → <code class="returnvalue">0.0.0.6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">|</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        Computes bitwise OR.
       </p>
<p>
<code class="literal">inet '192.168.1.6' | inet '0.0.0.255'</code>
        → <code class="returnvalue">192.168.1.255</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">+</code> <code class="type">bigint</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        Adds an offset to an address.
       </p>
<p>
<code class="literal">inet '192.168.1.6' + 25</code>
        → <code class="returnvalue">192.168.1.31</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bigint</code> <code class="literal">+</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        Adds an offset to an address.
       </p>
<p>
<code class="literal">200 + inet '::ffff:fff0:1'</code>
        → <code class="returnvalue">::ffff:255.240.0.201</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">-</code> <code class="type">bigint</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        Subtracts an offset from an address.
       </p>
<p>
<code class="literal">inet '192.168.1.43' - 36</code>
        → <code class="returnvalue">192.168.1.7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">-</code> <code class="type">inet</code>
        → <code class="returnvalue">bigint</code>
</p>
<p>
        Computes the difference of two addresses.
       </p>
<p>
<code class="literal">inet '192.168.1.43' - inet '192.168.1.19'</code>
        → <code class="returnvalue">24</code>
</p>
<p>
<code class="literal">inet '::1' - inet '::ffff:1'</code>
        → <code class="returnvalue">-4294901760</code>
</p></td></tr></tbody></table>

<br><a id="CIDR-INET-FUNCTIONS-TABLE"></a>

**Table 9.40. IP Address Functions**

<table border="1" class="table" summary="IP Address Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.1.1.1.1"></a>
<code class="function">abbrev</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Creates an abbreviated display format as text.
        (The result is the same as the <code class="type">inet</code> output function
        produces; it is <span class="quote">“<span class="quote">abbreviated</span>”</span> only in comparison to the
        result of an explicit cast to <code class="type">text</code>, which for historical
        reasons will never suppress the netmask part.)
       </p>
<p>
<code class="literal">abbrev(inet '10.1.0.0/32')</code>
        → <code class="returnvalue">10.1.0.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">abbrev</code> ( <code class="type">cidr</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Creates an abbreviated display format as text.
        (The abbreviation consists of dropping all-zero octets to the right
        of the netmask; more examples are in
        <a class="xref" href="../datatype/datatype-net-types.md#DATATYPE-NET-CIDR-TABLE">Table 8.22</a>.)
       </p>
<p>
<code class="literal">abbrev(cidr '10.1.0.0/16')</code>
        → <code class="returnvalue">10.1/16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.3.1.1.1"></a>
<code class="function">broadcast</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        Computes the broadcast address for the address's network.
       </p>
<p>
<code class="literal">broadcast(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">192.168.1.255/24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.4.1.1.1"></a>
<code class="function">family</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the address's family: <code class="literal">4</code> for IPv4,
        <code class="literal">6</code> for IPv6.
       </p>
<p>
<code class="literal">family(inet '::1')</code>
        → <code class="returnvalue">6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.5.1.1.1"></a>
<code class="function">host</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the IP address as text, ignoring the netmask.
       </p>
<p>
<code class="literal">host(inet '192.168.1.0/24')</code>
        → <code class="returnvalue">192.168.1.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.6.1.1.1"></a>
<code class="function">hostmask</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        Computes the host mask for the address's network.
       </p>
<p>
<code class="literal">hostmask(inet '192.168.23.20/30')</code>
        → <code class="returnvalue">0.0.0.3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.7.1.1.1"></a>
<code class="function">inet_merge</code> ( <code class="type">inet</code>, <code class="type">inet</code> )
        → <code class="returnvalue">cidr</code>
</p>
<p>
        Computes the smallest network that includes both of the given networks.
       </p>
<p>
<code class="literal">inet_merge(inet '192.168.1.5/24', inet '192.168.2.5/24')</code>
        → <code class="returnvalue">192.168.0.0/22</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.8.1.1.1"></a>
<code class="function">inet_same_family</code> ( <code class="type">inet</code>, <code class="type">inet</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        Tests whether the addresses belong to the same IP family.
       </p>
<p>
<code class="literal">inet_same_family(inet '192.168.1.5/24', inet '::1')</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.9.1.1.1"></a>
<code class="function">masklen</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        Returns the netmask length in bits.
       </p>
<p>
<code class="literal">masklen(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.10.1.1.1"></a>
<code class="function">netmask</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        Computes the network mask for the address's network.
       </p>
<p>
<code class="literal">netmask(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">255.255.255.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.11.1.1.1"></a>
<code class="function">network</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">cidr</code>
</p>
<p>
        Returns the network part of the address, zeroing out
        whatever is to the right of the netmask.
        (This is equivalent to casting the value to <code class="type">cidr</code>.)
       </p>
<p>
<code class="literal">network(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">192.168.1.0/24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.12.1.1.1"></a>
<code class="function">set_masklen</code> ( <code class="type">inet</code>, <code class="type">integer</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        Sets the netmask length for an <code class="type">inet</code> value.
        The address part does not change.
       </p>
<p>
<code class="literal">set_masklen(inet '192.168.1.5/24', 16)</code>
        → <code class="returnvalue">192.168.1.5/16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">set_masklen</code> ( <code class="type">cidr</code>, <code class="type">integer</code> )
        → <code class="returnvalue">cidr</code>
</p>
<p>
        Sets the netmask length for a <code class="type">cidr</code> value.
        Address bits to the right of the new netmask are set to zero.
       </p>
<p>
<code class="literal">set_masklen(cidr '192.168.1.0/24', 16)</code>
        → <code class="returnvalue">192.168.0.0/16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.14.1.1.1"></a>
<code class="function">text</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        Returns the unabbreviated IP address and netmask length as text.
        (This has the same result as an explicit cast to <code class="type">text</code>.)
       </p>
<p>
<code class="literal">text(inet '192.168.1.5')</code>
        → <code class="returnvalue">192.168.1.5/32</code>
</p></td></tr></tbody></table>

<br>

### Tip

The `abbrev`, `host`,
and `text` functions are primarily intended to offer
alternative display formats for IP addresses.

The MAC address types, `macaddr` and `macaddr8`,
support the usual comparison operators shown in
[Table 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE)
as well as the specialized functions shown in
[Table 9.41](functions-net.md#MACADDR-FUNCTIONS-TABLE).
In addition, they support the bitwise logical operators
`~`, `&` and `|`
(NOT, AND and OR), just as shown above for IP addresses.

<a id="MACADDR-FUNCTIONS-TABLE"></a>

**Table 9.41. MAC Address Functions**

<table border="1" class="table" summary="MAC Address Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.8.2.2.1.1.1.1"></a>
<code class="function">trunc</code> ( <code class="type">macaddr</code> )
        → <code class="returnvalue">macaddr</code>
</p>
<p>
        Sets the last 3 bytes of the address to zero.  The remaining prefix
        can be associated with a particular manufacturer (using data not
        included in <span class="productname">PostgreSQL</span>).
       </p>
<p>
<code class="literal">trunc(macaddr '12:34:56:78:90:ab')</code>
        → <code class="returnvalue">12:34:56:00:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">trunc</code> ( <code class="type">macaddr8</code> )
        → <code class="returnvalue">macaddr8</code>
</p>
<p>
        Sets the last 5 bytes of the address to zero.  The remaining prefix
        can be associated with a particular manufacturer (using data not
        included in <span class="productname">PostgreSQL</span>).
       </p>
<p>
<code class="literal">trunc(macaddr8 '12:34:56:78:90:ab:cd:ef')</code>
        → <code class="returnvalue">12:34:56:00:00:00:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.8.2.2.3.1.1.1"></a>
<code class="function">macaddr8_set7bit</code> ( <code class="type">macaddr8</code> )
        → <code class="returnvalue">macaddr8</code>
</p>
<p>
        Sets the 7th bit of the address to one, creating what is known as
        modified EUI-64, for inclusion in an IPv6 address.
       </p>
<p>
<code class="literal">macaddr8_set7bit(macaddr8 '00:34:56:ab:cd:ef')</code>
        → <code class="returnvalue">02:34:56:ff:fe:ab:cd:ef</code>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-net.html)（英文原文，待翻譯）
