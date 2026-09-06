<a id="SQL-CREATETSTEMPLATE"></a><a id="id-1.9.3.91.1"></a>

# CREATE TEXT SEARCH TEMPLATE

CREATE TEXT SEARCH TEMPLATE — define a new text search template

## Synopsis

```

CREATE TEXT SEARCH TEMPLATE name (
    [ INIT = init_function , ]
    LEXIZE = lexize_function
)
```

<a id="id-1.9.3.91.5"></a>

## Description

`CREATE TEXT SEARCH TEMPLATE` creates a new text search template. Text search templates define the functions that implement text search dictionaries. A template is not useful by itself, but must be instantiated as a dictionary to be used. The dictionary typically specifies parameters to be given to the template functions.

If a schema name is given then the text search template is created in the specified schema. Otherwise it is created in the current schema.

You must be a superuser to use `CREATE TEXT SEARCH TEMPLATE`. This restriction is made because an erroneous text search template definition could confuse or even crash the server. The reason for separating templates from dictionaries is that a template encapsulates the “unsafe” aspects of defining a dictionary. The parameters that can be set when defining a dictionary are safe for unprivileged users to set, and so creating a dictionary need not be a privileged operation.

Refer to [Chapter 12](../../the-sql-language/12.-quan-wen-jian-suo/README.md) for further information.

<a id="id-1.9.3.91.6"></a>

## Parameters

<em class="replaceable"><code>name</code></em>

The name of the text search template to be created. The name can be schema-qualified.

<em class="replaceable"><code>init&#95;function</code></em>

The name of the init function for the template.

<em class="replaceable"><code>lexize&#95;function</code></em>

The name of the lexize function for the template.

The function names can be schema-qualified if necessary. Argument types are not given, since the argument list for each type of function is predetermined. The lexize function is required, but the init function is optional.

The arguments can appear in any order, not only the one shown above.

<a id="id-1.9.3.91.7"></a>

## Compatibility

There is no `CREATE TEXT SEARCH TEMPLATE` statement in the SQL standard.

<a id="id-1.9.3.91.8"></a>

## See Also

[ALTER TEXT SEARCH TEMPLATE](alter-text-search-template.md), [DROP TEXT SEARCH TEMPLATE](drop-text-search-template.md)

---

原文：[PostgreSQL 15.19 Documentation](create-text-search-template.md)（英文原文，待翻譯）
