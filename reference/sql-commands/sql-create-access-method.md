<a id="id-1.9.3.56.1"></a>

## CREATE ACCESS METHOD

CREATE ACCESS METHOD — define a new access method

## Synopsis

```

CREATE ACCESS METHOD name
    TYPE access_method_type
    HANDLER handler_function
```

<a id="id-1.9.3.56.5"></a>

## Description

`CREATE ACCESS METHOD` creates a new access method.

The access method name must be unique within the database.

Only superusers can define new access methods.

<a id="id-1.9.3.56.6"></a>

## Parameters

*`name`*
:   The name of the access method to be created.

*`access_method_type`*
:   This clause specifies the type of access method to define.
    Only `TABLE` and `INDEX`
    are supported at present.

*`handler_function`*
:   *`handler_function`* is the
    name (possibly schema-qualified) of a previously registered function
    that represents the access method. The handler function must be
    declared to take a single argument of type `internal`,
    and its return type depends on the type of access method;
    for `TABLE` access methods, it must
    be `table_am_handler` and for `INDEX`
    access methods, it must be `index_am_handler`.
    The C-level API that the handler function must implement varies
    depending on the type of access method. The table access method API
    is described in [Chapter 62](../../internals/tableam/README.md) and the index access method
    API is described in [Chapter 63](../../internals/indexam/README.md).

<a id="id-1.9.3.56.7"></a>

## Examples

Create an index access method `heptree` with
handler function `heptree_handler`:

```

CREATE ACCESS METHOD heptree TYPE INDEX HANDLER heptree_handler;
```

<a id="id-1.9.3.56.8"></a>

## Compatibility

`CREATE ACCESS METHOD` is a
PostgreSQL extension.

<a id="id-1.9.3.56.9"></a>

## See Also

[DROP ACCESS METHOD](sql-drop-access-method.md), [CREATE OPERATOR CLASS](sql-createopclass.md), [CREATE OPERATOR FAMILY](sql-createopfamily.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-create-access-method.html)（英文原文，待翻譯）
