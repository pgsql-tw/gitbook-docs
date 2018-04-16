# 9.16. 序列函式

This section describes functions for operating on_sequence objects_, also called sequence generators or just sequences. Sequence objects are special single-row tables created with[CREATE SEQUENCE](https://www.postgresql.org/docs/10/static/sql-createsequence.html). Sequence objects are commonly used to generate unique identifiers for rows of a table. The sequence functions, listed in[Table 9.47](https://www.postgresql.org/docs/10/static/functions-sequence.html#functions-sequence-table), provide simple, multiuser-safe methods for obtaining successive sequence values from sequence objects.

**Table 9.47. Sequence Functions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `currval(regclass`\) | `bigint` | Return value most recently obtained with`nextval`for specified sequence |
| `lastval()` | `bigint` | Return value most recently obtained with`nextval`for any sequence |
| `nextval(regclass`\) | `bigint` | Advance sequence and return new value |
| `setval(regclass`,`bigint`\) | `bigint` | Set sequence's current value |
| `setval(regclass`,`bigint`,`boolean`\) | `bigint` | Set sequence's current value and`is_called`flag |

The sequence to be operated on by a sequence function is specified by a`regclass`argument, which is simply the OID of the sequence in the`pg_class`system catalog. You do not have to look up the OID by hand, however, since the`regclass`data type's input converter will do the work for you. Just write the sequence name enclosed in single quotes so that it looks like a literal constant. For compatibility with the handling of ordinarySQLnames, the string will be converted to lower case unless it contains double quotes around the sequence name. Thus:

```text
nextval('foo')      
operates on sequence 
foo

nextval('FOO')      
operates on sequence 
foo

nextval('"Foo"')    
operates on sequence 
Foo
```

The sequence name can be schema-qualified if necessary:

```text
nextval('myschema.foo')     
operates on 
myschema.foo

nextval('"myschema".foo')   
same as above

nextval('foo')              
searches search path for 
foo
```

See[Section 8.18](https://www.postgresql.org/docs/10/static/datatype-oid.html)for more information about`regclass`.

## Note

BeforePostgreSQL8.1, the arguments of the sequence functions were of type`text`, not`regclass`, and the above-described conversion from a text string to an OID value would happen at run time during each call. For backward compatibility, this facility still exists, but internally it is now handled as an implicit coercion from`text`to`regclass`before the function is invoked.

When you write the argument of a sequence function as an unadorned literal string, it becomes a constant of type`regclass`. Since this is really just an OID, it will track the originally identified sequence despite later renaming, schema reassignment, etc. This“early binding”behavior is usually desirable for sequence references in column defaults and views. But sometimes you might want“late binding”where the sequence reference is resolved at run time. To get late-binding behavior, force the constant to be stored as a`text`constant instead of`regclass`:

```text
nextval('foo'::text)      
foo
 is looked up at runtime
```

Note that late binding was the only behavior supported inPostgreSQLreleases before 8.1, so you might need to do this to preserve the semantics of old applications.

Of course, the argument of a sequence function can be an expression as well as a constant. If it is a text expression then the implicit coercion will result in a run-time lookup.

The available sequence functions are:

`nextval`

Advance the sequence object to its next value and return that value. This is done atomically: even if multiple sessions execute`nextval`concurrently, each will safely receive a distinct sequence value.

If a sequence object has been created with default parameters, successive`nextval`calls will return successive values beginning with 1. Other behaviors can be obtained by using special parameters in the[CREATE SEQUENCE](https://www.postgresql.org/docs/10/static/sql-createsequence.html)command; see its command reference page for more information.

## Important

To avoid blocking concurrent transactions that obtain numbers from the same sequence, a`nextval`operation is never rolled back; that is, once a value has been fetched it is considered used and will not be returned again. This is true even if the surrounding transaction later aborts, or if the calling query ends up not using the value. For example an`INSERT`with an`ON CONFLICT`clause will compute the to-be-inserted tuple, including doing any required`nextval`calls, before detecting any conflict that would cause it to follow the`ON CONFLICT`rule instead. Such cases will leave unused“holes”in the sequence of assigned values. Thus,PostgreSQLsequence objects_cannot be used to obtain“gapless”sequences_.

This function requires`USAGE`or`UPDATE`privilege on the sequence.

`currval`

Return the value most recently obtained by`nextval`for this sequence in the current session. \(An error is reported if`nextval`has never been called for this sequence in this session.\) Because this is returning a session-local value, it gives a predictable answer whether or not other sessions have executed`nextval`since the current session did.

This function requires`USAGE`or`SELECT`privilege on the sequence.

`lastval`

Return the value most recently returned by`nextval`in the current session. This function is identical to`currval`, except that instead of taking the sequence name as an argument it refers to whichever sequence`nextval`was most recently applied to in the current session. It is an error to call`lastval`if`nextval`has not yet been called in the current session.

This function requires`USAGE`or`SELECT`privilege on the last used sequence.

`setval`

Reset the sequence object's counter value. The two-parameter form sets the sequence's`last_value`field to the specified value and sets its`is_called`field to`true`, meaning that the next`nextval`will advance the sequence before returning a value. The value reported by`currval`is also set to the specified value. In the three-parameter form,`is_called`can be set to either`true`or`false`.`true`has the same effect as the two-parameter form. If it is set to`false`, the next`nextval`will return exactly the specified value, and sequence advancement commences with the following`nextval`. Furthermore, the value reported by`currval`is not changed in this case. For example,

```text
SELECT setval('foo', 42);           
Next 
nextval
 will return 43

SELECT setval('foo', 42, true);     
Same as above

SELECT setval('foo', 42, false);    
Next 
nextval
 will return 42
```

The result returned by`setval`is just the value of its second argument.

## Important

Because sequences are non-transactional, changes made by`setval`are not undone if the transaction rolls back.

This function requires`UPDATE`privilege on the sequence.

