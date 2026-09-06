<a id="id-1.9.3.18.1"></a>

## ALTER LARGE OBJECT

ALTER LARGE OBJECT — change the definition of a large object

## Synopsis

```

ALTER LARGE OBJECT large_object_oid OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

<a id="id-1.9.3.18.5"></a>

## Description

`ALTER LARGE OBJECT` changes the definition of a
large object.

You must own the large object to use `ALTER LARGE OBJECT`.
To alter the owner, you must also be able to `SET ROLE` to
the new owning role.
(However, a superuser can alter any large object anyway.)
Currently, the only functionality is to assign a new owner, so both
restrictions always apply.

<a id="id-1.9.3.18.6"></a>

## Parameters

*`large_object_oid`*
:   OID of the large object to be altered

*`new_owner`*
:   The new owner of the large object

<a id="id-1.9.3.18.7"></a>

## Compatibility

There is no `ALTER LARGE OBJECT` statement in the SQL
standard.

<a id="id-1.9.3.18.8"></a>

## See Also

[Chapter 33](../../client-interfaces/largeobjects/README.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alterlargeobject.html)（英文原文，待翻譯）
