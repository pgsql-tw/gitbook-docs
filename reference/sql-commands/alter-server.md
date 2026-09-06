<a id="SQL-ALTERSERVER"></a><a id="id-1.9.3.31.1"></a>

# ALTER SERVER

ALTER SERVER — change the definition of a foreign server

## Synopsis

```

ALTER SERVER name [ VERSION 'new_version' ]
    [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] ) ]
ALTER SERVER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SERVER name RENAME TO new_name
```

<a id="id-1.9.3.31.5"></a>

## Description

`ALTER SERVER` changes the definition of a foreign server. The first form changes the server version string or the generic options of the server (at least one clause is required). The second form changes the owner of the server.

To alter the server you must be the owner of the server. Additionally to alter the owner, you must own the server and also be a direct or indirect member of the new owning role, and you must have `USAGE` privilege on the server's foreign-data wrapper. (Note that superusers satisfy all these criteria automatically.)

<a id="id-1.9.3.31.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of an existing server.

<em class="replaceable"><code>new&#95;version</code></em>

New server version.

<code class="literal">OPTIONS ( &#91; ADD | SET | DROP &#93; <em class="replaceable"><code>option</code></em> &#91;'<em class="replaceable"><code>value</code></em>'&#93; &#91;, ... &#93; )</code>

Change options for the server. `ADD`, `SET`, and `DROP` specify the action to be performed. `ADD` is assumed if no operation is explicitly specified. Option names must be unique; names and values are also validated using the server's foreign-data wrapper library.

<em class="replaceable"><code>new&#95;owner</code></em>

The user name of the new owner of the foreign server.

<em class="replaceable"><code>new&#95;name</code></em>

The new name for the foreign server.

<a id="id-1.9.3.31.7"></a>

## Examples

Alter server `foo`, add connection options:

```

ALTER SERVER foo OPTIONS (host 'foo', dbname 'foodb');
```

Alter server `foo`, change version, change `host` option:

```

ALTER SERVER foo VERSION '8.4' OPTIONS (SET host 'baz');
```

<a id="id-1.9.3.31.8"></a>

## Compatibility

`ALTER SERVER` conforms to ISO/IEC 9075-9 (SQL/MED). The `OWNER TO` and `RENAME` forms are PostgreSQL extensions.

<a id="id-1.9.3.31.9"></a>

## See Also

[CREATE SERVER](create-server.md), [DROP SERVER](drop-server.md)

---

原文：[PostgreSQL 15.19 Documentation](alter-server.md)（英文原文，待翻譯）
