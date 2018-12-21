# ALTER LANGUAGE

ALTER LANGUAGE — change the definition of a procedural language

### Synopsis

```text
ALTER [ PROCEDURAL ] LANGUAGE name RENAME TO new_name
ALTER [ PROCEDURAL ] LANGUAGE name OWNER TO { new_owner | CURRENT_USER | SESSION_USER }
```

### Description

`ALTER LANGUAGE` changes the definition of a procedural language. The only functionality is to rename the language or assign a new owner. You must be superuser or owner of the language to use `ALTER LANGUAGE`.

### Parameters

_`name`_

Name of a language

_`new_name`_

The new name of the language

_`new_owner`_

The new owner of the language

### Compatibility

There is no `ALTER LANGUAGE` statement in the SQL standard.

### See Also

[CREATE LANGUAGE](create-language.md), [DROP LANGUAGE](drop-language.md)  


