<a id="SQL-DROPUSERMAPPING"></a><a id="id-1.9.3.144.1"></a>

# DROP USER MAPPING

DROP USER MAPPING — remove a user mapping for a foreign server

## Synopsis

```

DROP USER MAPPING [ IF EXISTS ] FOR { user_name | USER | CURRENT_ROLE | CURRENT_USER | PUBLIC } SERVER server_name
```

<a id="id-1.9.3.144.5"></a>

## Description

`DROP USER MAPPING` removes an existing user mapping from foreign server.

The owner of a foreign server can drop user mappings for that server for any user. Also, a user can drop a user mapping for their own user name if `USAGE` privilege on the server has been granted to the user.

<a id="id-1.9.3.144.6"></a>

## Parameters

`IF EXISTS`

Do not throw an error if the user mapping does not exist. A notice is issued in this case.

<em class="replaceable"><code>user&#95;name</code></em>

User name of the mapping. `CURRENT_ROLE`, `CURRENT_USER`, and `USER` match the name of the current user. `PUBLIC` is used to match all present and future user names in the system.

<em class="replaceable"><code>server&#95;name</code></em>

Server name of the user mapping.

<a id="id-1.9.3.144.7"></a>

## Examples

Drop a user mapping `bob`, server `foo` if it exists:

```

DROP USER MAPPING IF EXISTS FOR bob SERVER foo;
```

<a id="id-1.9.3.144.8"></a>

## Compatibility

`DROP USER MAPPING` conforms to ISO/IEC 9075-9 (SQL/MED). The `IF EXISTS` clause is a PostgreSQL extension.

<a id="id-1.9.3.144.9"></a>

## See Also

[CREATE USER MAPPING](create-user-mapping.md), [ALTER USER MAPPING](alter-user-mapping.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-dropusermapping.html)（英文原文，待翻譯）
