# CREATE ACCESS METHOD

CREATE ACCESS METHOD — define a new access method

### Synopsis

```text
CREATE ACCESS METHOD name
    TYPE access_method_type
    HANDLER handler_function
```

### Description

`CREATE ACCESS METHOD` creates a new access method.

The access method name must be unique within the database.

Only superusers can define new access methods.

### Parameters

_`name`_

The name of the access method to be created.

_`access_method_type`_

This clause specifies the type of access method to define. Only `TABLE` and `INDEX` are supported at present.

_`handler_function`_

_`handler_function`_ is the name \(possibly schema-qualified\) of a previously registered function that represents the access method. The handler function must be declared to take a single argument of type `internal`, and its return type depends on the type of access method; for `TABLE` access methods, it must be `table_am_handler` and for `INDEX` access methods, it must be `index_am_handler`. The C-level API that the handler function must implement varies depending on the type of access method. The table access method API is described in [Chapter 60](https://www.postgresql.org/docs/13/tableam.html) and the index access method API is described in [Chapter 61](https://www.postgresql.org/docs/13/indexam.html).

### Examples

Create an index access method `heptree` with handler function `heptree_handler`:

```text
CREATE ACCESS METHOD heptree TYPE INDEX HANDLER heptree_handler;
```

### Compatibility

`CREATE ACCESS METHOD` is a PostgreSQL extension.

### See Also

[DROP ACCESS METHOD](https://www.postgresql.org/docs/13/sql-drop-access-method.html), [CREATE OPERATOR CLASS](https://www.postgresql.org/docs/13/sql-createopclass.html), [CREATE OPERATOR FAMILY](https://www.postgresql.org/docs/13/sql-createopfamily.html)

