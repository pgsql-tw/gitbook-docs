# 36.7. character\_sets

The view `character_sets` identifies the character sets available in the current database. Since PostgreSQL does not support multiple character sets within one database, this view only shows one, which is the database encoding.

Take note of how the following terms are used in the SQL standard:character repertoire

An abstract collection of characters, for example `UNICODE`, `UCS`, or `LATIN1`. Not exposed as an SQL object, but visible in this view.character encoding form

An encoding of some character repertoire. Most older character repertoires only use one encoding form, and so there are no separate names for them (e.g., `LATIN1` is an encoding form applicable to the `LATIN1` repertoire). But for example Unicode has the encoding forms `UTF8`, `UTF16`, etc. (not all supported by PostgreSQL). Encoding forms are not exposed as an SQL object, but are visible in this view.character set

A named SQL object that identifies a character repertoire, a character encoding, and a default collation. A predefined character set would typically have the same name as an encoding form, but users could define other names. For example, the character set `UTF8` would typically identify the character repertoire `UCS`, encoding form `UTF8`, and some default collation.

You can think of an “encoding” in PostgreSQL either as a character set or a character encoding form. They will have the same name, and there can only be one in one database.

#### **Table 36.5. `character_sets` Columns**

| <p>Column Type</p><p>Description</p>                                                                                                                                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><code>character_set_catalog</code> <code>sql_identifier</code></p><p>Character sets are currently not implemented as schema objects, so this column is null.</p>                                                                                                                                                                                                   |
| <p><code>character_set_schema</code> <code>sql_identifier</code></p><p>Character sets are currently not implemented as schema objects, so this column is null.</p>                                                                                                                                                                                                    |
| <p><code>character_set_name</code> <code>sql_identifier</code></p><p>Name of the character set, currently implemented as showing the name of the database encoding</p>                                                                                                                                                                                                |
| <p><code>character_repertoire</code> <code>sql_identifier</code></p><p>Character repertoire, showing <code>UCS</code> if the encoding is <code>UTF8</code>, else just the encoding name</p>                                                                                                                                                                           |
| <p><code>form_of_use</code> <code>sql_identifier</code></p><p>Character encoding form, same as the database encoding</p>                                                                                                                                                                                                                                              |
| <p><code>default_collate_catalog</code> <code>sql_identifier</code></p><p>Name of the database containing the default collation (always the current database, if any collation is identified)</p>                                                                                                                                                                     |
| <p><code>default_collate_schema</code> <code>sql_identifier</code></p><p>Name of the schema containing the default collation</p>                                                                                                                                                                                                                                      |
| <p><code>default_collate_name</code> <code>sql_identifier</code></p><p>Name of the default collation. The default collation is identified as the collation that matches the <code>COLLATE</code> and <code>CTYPE</code> settings of the current database. If there is no such collation, then this column and the associated schema and catalog columns are null.</p> |
