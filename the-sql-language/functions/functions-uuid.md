## 9.14. UUID Functions [#](#FUNCTIONS-UUID)

<a id="id-1.5.8.20.2"></a><a id="id-1.5.8.20.3"></a><a id="id-1.5.8.20.4"></a><a id="id-1.5.8.20.5"></a><a id="id-1.5.8.20.6"></a><a id="id-1.5.8.20.7"></a>

[Table 9.45](functions-uuid.md#FUNC_UUID_GEN_TABLE) shows the PostgreSQL
functions that can be used to generate UUIDs.

<a id="FUNC_UUID_GEN_TABLE"></a>

**Table 9.45. UUID Generation Functions**

<table border="1" class="table" summary="UUID Generation Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
        </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">gen_random_uuid</code> ( )
        → <code class="returnvalue">uuid</code>
</p>
<p class="func_signature">
<code class="function">uuidv4</code> ( )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Generates a version 4 (random) UUID
       </p>
<p>
<code class="literal">gen_random_uuid()</code>
        → <code class="returnvalue">5b30857f-0bfa-48b5-ac0b-5c64e28078d1</code>
</p>
<p>
<code class="literal">uuidv4()</code>
        → <code class="returnvalue">b42410ee-132f-42ee-9e4f-09a6485c95b8</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuidv7</code>
        ( [<span class="optional"> <em class="parameter"><code>shift</code></em> <code class="type">interval</code> </span>] )
        → <code class="returnvalue">uuid</code>
</p>
<p>
        Generates a version 7 (time-ordered) UUID. The timestamp is
        computed using UNIX timestamp with millisecond precision +
        sub-millisecond timestamp + random. The optional
        parameter <em class="parameter"><code>shift</code></em> will shift the computed
        timestamp by the given <code class="type">interval</code>.
        Infinite interval values are not accepted.
        The shifted timestamp must fall within the range supported by
        UUID version 7's 48-bit millisecond timestamp field: from
        1970-01-01 00:00:00 UTC to approximately year 10889.
        An error is raised if the resulting timestamp is outside this
        range.
       </p>
<p>
<code class="literal">uuidv7()</code>
        → <code class="returnvalue">019535d9-3df7-79fb-b466-fa907fa17f9e</code>
</p></td></tr></tbody></table>

<br>

### Note

The [uuid-ossp](../../appendixes/contrib/uuid-ossp.md) module provides additional functions that
implement other standard algorithms for generating UUIDs.

[Table 9.46](functions-uuid.md#FUNC_UUID_EXTRACT_TABLE) shows the PostgreSQL
functions that can be used to extract information from UUIDs.

<a id="FUNC_UUID_EXTRACT_TABLE"></a>

**Table 9.46. UUID Extraction Functions**

<table border="1" class="table" summary="UUID Extraction Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_extract_timestamp</code>
        ( <code class="type">uuid</code> )
        → <code class="returnvalue">timestamp with time zone</code>
</p>
<p>
        Extracts a <code class="type">timestamp with time zone</code> from a UUID of
        version 1 or 7.  For other versions, this function returns null.
        Note that the extracted timestamp is not necessarily exactly equal
        to the time the UUID was generated; this depends on the
        implementation that generated the UUID.
       </p>
<p>
<code class="literal">uuid_extract_timestamp('019535d9-3df7-79fb-b466-​fa907fa17f9e'::uuid)</code>
         → <code class="returnvalue">2025-02-23 21:46:24.503-05</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">uuid_extract_version</code>
        ( <code class="type">uuid</code> )
        → <code class="returnvalue">smallint</code>
</p>
<p>
        Extracts the version from a UUID of one of the variants described by
        <a class="ulink" href="https://datatracker.ietf.org/doc/html/rfc9562" target="_top">RFC
        9562</a>.  For other variants, this function returns null.
        For example, for a UUID generated
        by <code class="function">gen_random_uuid()</code>, this function will
        return 4.
       </p>
<p>
<code class="literal">uuid_extract_version('41db1265-8bc1-4ab3-992f-​885799a4af1d'::uuid)</code>
        → <code class="returnvalue">4</code>
</p>
<p>
<code class="literal">uuid_extract_version('019535d9-3df7-79fb-b466-​fa907fa17f9e'::uuid)</code>
        → <code class="returnvalue">7</code>
</p></td></tr></tbody></table>

<br>

PostgreSQL also provides the usual comparison
operators shown in [Table 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) for
UUIDs.

See [Section 8.12](../datatype/datatype-uuid.md) for details on the data type
`uuid` in PostgreSQL.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-uuid.html)（英文原文，待翻譯）
