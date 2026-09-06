<a id="SQL-ALTERFOREIGNDATAWRAPPER"></a><a id="id-1.9.3.12.1"></a>

# ALTER FOREIGN DATA WRAPPER

ALTER FOREIGN DATA WRAPPER — change the definition of a foreign-data wrapper

## Synopsis

```

ALTER FOREIGN DATA WRAPPER name
    [ HANDLER handler_function | NO HANDLER ]
    [ VALIDATOR validator_function | NO VALIDATOR ]
    [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ]) ]
ALTER FOREIGN DATA WRAPPER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER FOREIGN DATA WRAPPER name RENAME TO new_name
```

<a id="id-1.9.3.12.5"></a>

## Description

`ALTER FOREIGN DATA WRAPPER` changes the definition of a foreign-data wrapper. The first form of the command changes the support functions or the generic options of the foreign-data wrapper (at least one clause is required). The second form changes the owner of the foreign-data wrapper.

Only superusers can alter foreign-data wrappers. Additionally, only superusers can own foreign-data wrappers.

<a id="id-1.9.3.12.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of an existing foreign-data wrapper.

<code class="literal">HANDLER <em class="replaceable"><code>handler&#95;function</code></em></code>

Specifies a new handler function for the foreign-data wrapper.

`NO HANDLER`

This is used to specify that the foreign-data wrapper should no longer have a handler function.

Note that foreign tables that use a foreign-data wrapper with no handler cannot be accessed.

<code class="literal">VALIDATOR <em class="replaceable"><code>validator&#95;function</code></em></code>

Specifies a new validator function for the foreign-data wrapper.

Note that it is possible that pre-existing options of the foreign-data wrapper, or of dependent servers, user mappings, or foreign tables, are invalid according to the new validator. PostgreSQL does not check for this. It is up to the user to make sure that these options are correct before using the modified foreign-data wrapper. However, any options specified in this `ALTER FOREIGN DATA WRAPPER` command will be checked using the new validator.

`NO VALIDATOR`

This is used to specify that the foreign-data wrapper should no longer have a validator function.

<code class="literal">OPTIONS ( &#91; ADD | SET | DROP &#93; <em class="replaceable"><code>option</code></em> &#91;'<em class="replaceable"><code>value</code></em>'&#93; &#91;, ... &#93; )</code>

Change options for the foreign-data wrapper. `ADD`, `SET`, and `DROP` specify the action to be performed. `ADD` is assumed if no operation is explicitly specified. Option names must be unique; names and values are also validated using the foreign data wrapper's validator function, if any.

<em class="replaceable"><code>new&#95;owner</code></em>

The user name of the new owner of the foreign-data wrapper.

<em class="replaceable"><code>new&#95;name</code></em>

The new name for the foreign-data wrapper.

<a id="id-1.9.3.12.7"></a>

## Examples

Change a foreign-data wrapper `dbi`, add option `foo`, drop `bar`:

```

ALTER FOREIGN DATA WRAPPER dbi OPTIONS (ADD foo '1', DROP bar);
```

Change the foreign-data wrapper `dbi` validator to `bob.myvalidator`:

```

ALTER FOREIGN DATA WRAPPER dbi VALIDATOR bob.myvalidator;
```

<a id="id-1.9.3.12.8"></a>

## Compatibility

`ALTER FOREIGN DATA WRAPPER` conforms to ISO/IEC 9075-9 (SQL/MED), except that the `HANDLER`, `VALIDATOR`, `OWNER TO`, and `RENAME` clauses are extensions.

<a id="id-1.9.3.12.9"></a>

## See Also

[CREATE FOREIGN DATA WRAPPER](create-foreign-data-wrapper.md), [DROP FOREIGN DATA WRAPPER](drop-foreign-data-wrapper.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/sql-alterforeigndatawrapper.html)（英文原文，待翻譯）
