## 33.4. Server-Side Functions [#](#LO-FUNCS)

Server-side functions tailored for manipulating large objects from SQL are
listed in [Table 33.1](lo-funcs.md#LO-FUNCS-TABLE).

<a id="LO-FUNCS-TABLE"></a>

**Table 33.1. SQL-Oriented Large Object Functions**

<table border="1" class="table" summary="SQL-Oriented Large Object Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        Function
       </p>
<p>
        Description
       </p>
<p>
        Example(s)
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.7.4.9.3.2.2.1.1.1.1"></a>
<code class="function">lo_from_bytea</code> ( <em class="parameter"><code>loid</code></em> <code class="type">oid</code>, <em class="parameter"><code>data</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">oid</code>
</p>
<p>
        Creates a large object and stores <em class="parameter"><code>data</code></em> in it.
        If <em class="parameter"><code>loid</code></em> is zero then the system will choose a
        free OID, otherwise that OID is used (with an error if some large
        object already has that OID).  On success, the large object's OID is
        returned.
       </p>
<p>
<code class="literal">lo_from_bytea(0, '\xffffff00')</code>
        → <code class="returnvalue">24528</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.7.4.9.3.2.2.2.1.1.1"></a>
<code class="function">lo_put</code> ( <em class="parameter"><code>loid</code></em> <code class="type">oid</code>, <em class="parameter"><code>offset</code></em> <code class="type">bigint</code>, <em class="parameter"><code>data</code></em> <code class="type">bytea</code> )
        → <code class="returnvalue">void</code>
</p>
<p>
        Writes <em class="parameter"><code>data</code></em> starting at the given offset within
        the large object; the large object is enlarged if necessary.
       </p>
<p>
<code class="literal">lo_put(24528, 1, '\xaa')</code>
        → <code class="returnvalue"></code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.7.4.9.3.2.2.3.1.1.1"></a>
<code class="function">lo_get</code> ( <em class="parameter"><code>loid</code></em> <code class="type">oid</code> [<span class="optional">, <em class="parameter"><code>offset</code></em> <code class="type">bigint</code>, <em class="parameter"><code>length</code></em> <code class="type">integer</code> </span>] )
        → <code class="returnvalue">bytea</code>
</p>
<p>
        Extracts the large object's contents, or a substring thereof.
       </p>
<p>
<code class="literal">lo_get(24528, 0, 3)</code>
        → <code class="returnvalue">\xffaaff</code>
</p></td></tr></tbody></table>

<br>

There are additional server-side functions corresponding to each of the
client-side functions described earlier; indeed, for the most part the
client-side functions are simply interfaces to the equivalent server-side
functions. The ones just as convenient to call via SQL commands are
`lo_creat`<a id="id-1.7.4.9.4.2"></a>,
`lo_create`,
`lo_unlink`<a id="id-1.7.4.9.4.5"></a>,
`lo_import`<a id="id-1.7.4.9.4.7"></a>, and
`lo_export`<a id="id-1.7.4.9.4.9"></a>.
Here are examples of their use:

```

CREATE TABLE image (
    name            text,
    raster          oid
);

SELECT lo_creat(-1);       -- returns OID of new, empty large object

SELECT lo_create(43213);   -- attempts to create large object with OID 43213

SELECT lo_unlink(173454);  -- deletes large object with OID 173454

INSERT INTO image (name, raster)
    VALUES ('beautiful image', lo_import('/etc/motd'));

INSERT INTO image (name, raster)  -- same as above, but specify OID to use
    VALUES ('beautiful image', lo_import('/etc/motd', 68583));

SELECT lo_export(image.raster, '/tmp/motd') FROM image
    WHERE name = 'beautiful image';
```

The server-side `lo_import` and
`lo_export` functions behave considerably differently
from their client-side analogs. These two functions read and write files
in the server's file system, using the permissions of the database's
owning user. Therefore, by default their use is restricted to superusers.
In contrast, the client-side import and export functions read and write
files in the client's file system, using the permissions of the client
program. The client-side functions do not require any database
privileges, except the privilege to read or write the large object in
question.

### Caution

It is possible to [GRANT](../../reference/sql-commands/sql-grant.md) use of the
server-side `lo_import`
and `lo_export` functions to non-superusers, but
careful consideration of the security implications is required. A
malicious user of such privileges could easily parlay them into becoming
superuser (for example by rewriting server configuration files), or could
attack the rest of the server's file system without bothering to obtain
database superuser privileges as such. *Access to roles having
such privilege must therefore be guarded just as carefully as access to
superuser roles.* Nonetheless, if use of
server-side `lo_import`
or `lo_export` is needed for some routine task, it's
safer to use a role with such privileges than one with full superuser
privileges, as that helps to reduce the risk of damage from accidental
errors.

The functionality of `lo_read` and
`lo_write` is also available via server-side calls,
but the names of the server-side functions differ from the client side
interfaces in that they do not contain underscores. You must call
these functions as `loread` and `lowrite`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/lo-funcs.html)（英文原文，待翻譯）
