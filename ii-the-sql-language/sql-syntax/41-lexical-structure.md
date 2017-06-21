# 4.1. 語法結構[^1]

SQL input consists of a sequence of_commands_. A command is composed of a sequence of_tokens_, terminated by a semicolon \(“;”\). The end of the input stream also terminates a command. Which tokens are valid depends on the syntax of the particular command.

A token can be a_key word_, an_identifier_, a_quoted identifier_, a_literal_\(or constant\), or a special character symbol. Tokens are normally separated by whitespace \(space, tab, newline\), but need not be if there is no ambiguity \(which is generally only the case if a special character is adjacent to some other token type\).

For example, the following is \(syntactically\) valid SQL input:

```
SELECT * FROM MY_TABLE;
UPDATE MY_TABLE SET A = 5;
INSERT INTO MY_TABLE VALUES (3, 'hi there');

```

This is a sequence of three commands, one per line \(although this is not required; more than one command can be on a line, and commands can usefully be split across lines\).

Additionally,_comments_can occur in SQL input. They are not tokens, they are effectively equivalent to whitespace.

The SQL syntax is not very consistent regarding what tokens identify commands and which are operands or parameters. The first few tokens are generally the command name, so in the above example we would usually speak of a“SELECT”, an“UPDATE”, and an“INSERT”command. But for instance the`UPDATE`command always requires a`SET`token to appear in a certain position, and this particular variation of`INSERT`also requires a`VALUES`in order to be complete. The precise syntax rules for each command are described in[Part VI](https://www.postgresql.org/docs/10/static/reference.html).

### 4.1.1. Identifiers and Key Words







Tokens such as`SELECT`,`UPDATE`, or`VALUES`in the example above are examples of_key words_, that is, words that have a fixed meaning in the SQL language. The tokens`MY_TABLE`and`A`are examples of_identifiers_. They identify names of tables, columns, or other database objects, depending on the command they are used in. Therefore they are sometimes simply called“names”. Key words and identifiers have the same lexical structure, meaning that one cannot know whether a token is an identifier or a key word without knowing the language. A complete list of key words can be found in[Appendix C](https://www.postgresql.org/docs/10/static/sql-keywords-appendix.html).

SQL identifiers and key words must begin with a letter \(`a`-`z`, but also letters with diacritical marks and non-Latin letters\) or an underscore \(`_`\). Subsequent characters in an identifier or key word can be letters, underscores, digits \(`0`-`9`\), or dollar signs \(`$`\). Note that dollar signs are not allowed in identifiers according to the letter of the SQL standard, so their use might render applications less portable. The SQL standard will not define a key word that contains digits or starts or ends with an underscore, so identifiers of this form are safe against possible conflict with future extensions of the standard.

The system uses no more than`NAMEDATALEN`-1 bytes of an identifier; longer names can be written in commands, but they will be truncated. By default,`NAMEDATALEN`is 64 so the maximum identifier length is 63 bytes. If this limit is problematic, it can be raised by changing the`NAMEDATALEN`constant in`src/include/pg_config_manual.h`.

Key words and unquoted identifiers are case insensitive. Therefore:

```
UPDATE MY_TABLE SET A = 5;

```

can equivalently be written as:

```
uPDaTE my_TabLE SeT a = 5;

```

A convention often used is to write key words in upper case and names in lower case, e.g.:

```
UPDATE my_table SET a = 5;

```

There is a second kind of identifier: the_delimited identifier_or_quoted identifier_. It is formed by enclosing an arbitrary sequence of characters in double-quotes \(`"`\). A delimited identifier is always an identifier, never a key word. So`"select"`could be used to refer to a column or table named“select”, whereas an unquoted`select`would be taken as a key word and would therefore provoke a parse error when used where a table or column name is expected. The example can be written with quoted identifiers like this:

```
UPDATE "my_table" SET "a" = 5;

```

Quoted identifiers can contain any character, except the character with code zero. \(To include a double quote, write two double quotes.\) This allows constructing table or column names that would otherwise not be possible, such as ones containing spaces or ampersands. The length limitation still applies.



A variant of quoted identifiers allows including escaped Unicode characters identified by their code points. This variant starts with`U&`\(upper or lower case U followed by ampersand\) immediately before the opening double quote, without any spaces in between, for example`U&"foo"`. \(Note that this creates an ambiguity with the operator`&`. Use spaces around the operator to avoid this problem.\) Inside the quotes, Unicode characters can be specified in escaped form by writing a backslash followed by the four-digit hexadecimal code point number or alternatively a backslash followed by a plus sign followed by a six-digit hexadecimal code point number. For example, the identifier`"data"`could be written as

```
U
&
"d\0061t\+000061"

```

The following less trivial example writes the Russian word“slon”\(elephant\) in Cyrillic letters:

```
U
&
"\0441\043B\043E\043D"

```

If a different escape character than backslash is desired, it can be specified using the`UESCAPE`clause after the string, for example:

```
U
&
"d!0061t!+000061" UESCAPE '!'

```

The escape character can be any single character other than a hexadecimal digit, the plus sign, a single quote, a double quote, or a whitespace character. Note that the escape character is written in single quotes, not double quotes.

To include the escape character in the identifier literally, write it twice.

The Unicode escape syntax works only when the server encoding is`UTF8`. When other server encodings are used, only code points in the ASCII range \(up to`\007F`\) can be specified. Both the 4-digit and the 6-digit form can be used to specify UTF-16 surrogate pairs to compose characters with code points larger than U+FFFF, although the availability of the 6-digit form technically makes this unnecessary. \(Surrogate pairs are not stored directly, but combined into a single code point that is then encoded in UTF-8.\)

Quoting an identifier also makes it case-sensitive, whereas unquoted names are always folded to lower case. For example, the identifiers`FOO`,`foo`, and`"foo"`are considered the same byPostgreSQL, but`"Foo"`and`"FOO"`are different from these three and each other. \(The folding of unquoted names to lower case inPostgreSQLis incompatible with the SQL standard, which says that unquoted names should be folded to upper case. Thus,`foo`should be equivalent to`"FOO"`not`"foo"`according to the standard. If you want to write portable applications you are advised to always quote a particular name or never quote it.\)

### 4.1.2. Constants



There are three kinds of_implicitly-typed constants_inPostgreSQL: strings, bit strings, and numbers. Constants can also be specified with explicit types, which can enable more accurate representation and more efficient handling by the system. These alternatives are discussed in the following subsections.

#### 4.1.2.1. String Constants



A string constant in SQL is an arbitrary sequence of characters bounded by single quotes \(`'`\), for example`'This is a string'`. To include a single-quote character within a string constant, write two adjacent single quotes, e.g.,`'Dianne''s horse'`. Note that this is_not_the same as a double-quote character \(`"`\).

Two string constants that are only separated by whitespace_with at least one newline_are concatenated and effectively treated as if the string had been written as one constant. For example:

```
SELECT 'foo'
'bar';

```

is equivalent to:

```
SELECT 'foobar';

```

but:

```
SELECT 'foo'      'bar';

```

is not valid syntax. \(This slightly bizarre behavior is specified bySQL;PostgreSQLis following the standard.\)

#### 4.1.2.2. String Constants with C-style Escapes





PostgreSQLalso accepts“escape”string constants, which are an extension to the SQL standard. An escape string constant is specified by writing the letter`E`\(upper or lower case\) just before the opening single quote, e.g.,`E'foo'`. \(When continuing an escape string constant across lines, write`E`only before the first opening quote.\) Within an escape string, a backslash character \(`\`\) begins a C-like_backslash escape_sequence, in which the combination of backslash and following character\(s\) represent a special byte value, as shown in[Table 4.1](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-backslash-table).

**Table 4.1. Backslash Escape Sequences**

| Backslash Escape Sequence | Interpretation |
| :--- | :--- |
| `\b` | backspace |
| `\f` | form feed |
| `\n` | newline |
| `\r` | carriage return |
| `\t` | tab |
| `\`_`o`_,`\`_`oo`_,`\`_`ooo`_\(_`o`_= 0 - 7\) | octal byte value |
| `\x`_`h`_,`\x`_`hh`_\(_`h`_= 0 - 9, A - F\) | hexadecimal byte value |
| `\u`_`xxxx`_,`\U`_`xxxxxxxx`_\(_`x`_= 0 - 9, A - F\) | 16 or 32-bit hexadecimal Unicode character value |

  


Any other character following a backslash is taken literally. Thus, to include a backslash character, write two backslashes \(`\\`\). Also, a single quote can be included in an escape string by writing`\'`, in addition to the normal way of`''`.

It is your responsibility that the byte sequences you create, especially when using the octal or hexadecimal escapes, compose valid characters in the server character set encoding. When the server encoding is UTF-8, then the Unicode escapes or the alternative Unicode escape syntax, explained in[Section 4.1.2.3](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-syntax-strings-uescape), should be used instead. \(The alternative would be doing the UTF-8 encoding by hand and writing out the bytes, which would be very cumbersome.\)

The Unicode escape syntax works fully only when the server encoding is`UTF8`. When other server encodings are used, only code points in the ASCII range \(up to`\u007F`\) can be specified. Both the 4-digit and the 8-digit form can be used to specify UTF-16 surrogate pairs to compose characters with code points larger than U+FFFF, although the availability of the 8-digit form technically makes this unnecessary. \(When surrogate pairs are used when the server encoding is`UTF8`, they are first combined into a single code point that is then encoded in UTF-8.\)

### Caution

If the configuration parameter[standard\_conforming\_strings](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#guc-standard-conforming-strings)is`off`, thenPostgreSQLrecognizes backslash escapes in both regular and escape string constants. However, as ofPostgreSQL9.1, the default is`on`, meaning that backslash escapes are recognized only in escape string constants. This behavior is more standards-compliant, but might break applications which rely on the historical behavior, where backslash escapes were always recognized. As a workaround, you can set this parameter to`off`, but it is better to migrate away from using backslash escapes. If you need to use a backslash escape to represent a special character, write the string constant with an`E`.

In addition to`standard_conforming_strings`, the configuration parameters[escape\_string\_warning](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#guc-escape-string-warning)and[backslash\_quote](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#guc-backslash-quote)govern treatment of backslashes in string constants.

The character with the code zero cannot be in a string constant.

#### 4.1.2.3. String Constants with Unicode Escapes



PostgreSQLalso supports another type of escape syntax for strings that allows specifying arbitrary Unicode characters by code point. A Unicode escape string constant starts with`U&`\(upper or lower case letter U followed by ampersand\) immediately before the opening quote, without any spaces in between, for example`U&'foo'`. \(Note that this creates an ambiguity with the operator`&`. Use spaces around the operator to avoid this problem.\) Inside the quotes, Unicode characters can be specified in escaped form by writing a backslash followed by the four-digit hexadecimal code point number or alternatively a backslash followed by a plus sign followed by a six-digit hexadecimal code point number. For example, the string`'data'`could be written as

```
U
&
'd\0061t\+000061'

```

The following less trivial example writes the Russian word“slon”\(elephant\) in Cyrillic letters:

```
U
&
'\0441\043B\043E\043D'

```

If a different escape character than backslash is desired, it can be specified using the`UESCAPE`clause after the string, for example:

```
U
&
'd!0061t!+000061' UESCAPE '!'

```

The escape character can be any single character other than a hexadecimal digit, the plus sign, a single quote, a double quote, or a whitespace character.

The Unicode escape syntax works only when the server encoding is`UTF8`. When other server encodings are used, only code points in the ASCII range \(up to`\007F`\) can be specified. Both the 4-digit and the 6-digit form can be used to specify UTF-16 surrogate pairs to compose characters with code points larger than U+FFFF, although the availability of the 6-digit form technically makes this unnecessary. \(When surrogate pairs are used when the server encoding is`UTF8`, they are first combined into a single code point that is then encoded in UTF-8.\)

Also, the Unicode escape syntax for string constants only works when the configuration parameter[standard\_conforming\_strings](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#guc-standard-conforming-strings)is turned on. This is because otherwise this syntax could confuse clients that parse the SQL statements to the point that it could lead to SQL injections and similar security issues. If the parameter is set to off, this syntax will be rejected with an error message.

To include the escape character in the string literally, write it twice.

#### 4.1.2.4. Dollar-quoted String Constants



While the standard syntax for specifying string constants is usually convenient, it can be difficult to understand when the desired string contains many single quotes or backslashes, since each of those must be doubled. To allow more readable queries in such situations,PostgreSQLprovides another way, called“dollar quoting”, to write string constants. A dollar-quoted string constant consists of a dollar sign \(`$`\), an optional“tag”of zero or more characters, another dollar sign, an arbitrary sequence of characters that makes up the string content, a dollar sign, the same tag that began this dollar quote, and a dollar sign. For example, here are two different ways to specify the string“Dianne's horse”using dollar quoting:

```
$$Dianne's horse$$
$SomeTag$Dianne's horse$SomeTag$

```

Notice that inside the dollar-quoted string, single quotes can be used without needing to be escaped. Indeed, no characters inside a dollar-quoted string are ever escaped: the string content is always written literally. Backslashes are not special, and neither are dollar signs, unless they are part of a sequence matching the opening tag.

It is possible to nest dollar-quoted string constants by choosing different tags at each nesting level. This is most commonly used in writing function definitions. For example:

```
$function$
BEGIN
    RETURN ($1 ~ $q$[\t\r\n\v\\]$q$);
END;
$function$

```

Here, the sequence`$q$[\t\r\n\v\\]$q$`represents a dollar-quoted literal string`[\t\r\n\v\\]`, which will be recognized when the function body is executed byPostgreSQL. But since the sequence does not match the outer dollar quoting delimiter`$function$`, it is just some more characters within the constant so far as the outer string is concerned.

The tag, if any, of a dollar-quoted string follows the same rules as an unquoted identifier, except that it cannot contain a dollar sign. Tags are case sensitive, so`$tag$String content$tag$`is correct, but`$TAG$String content$tag$`is not.

A dollar-quoted string that follows a keyword or identifier must be separated from it by whitespace; otherwise the dollar quoting delimiter would be taken as part of the preceding identifier.

Dollar quoting is not part of the SQL standard, but it is often a more convenient way to write complicated string literals than the standard-compliant single quote syntax. It is particularly useful when representing string constants inside other constants, as is often needed in procedural function definitions. With single-quote syntax, each backslash in the above example would have to be written as four backslashes, which would be reduced to two backslashes in parsing the original string constant, and then to one when the inner string constant is re-parsed during function execution.

#### 4.1.2.5. Bit-string Constants



Bit-string constants look like regular string constants with a`B`\(upper or lower case\) immediately before the opening quote \(no intervening whitespace\), e.g.,`B'1001'`. The only characters allowed within bit-string constants are`0`and`1`.

Alternatively, bit-string constants can be specified in hexadecimal notation, using a leading`X`\(upper or lower case\), e.g.,`X'1FF'`. This notation is equivalent to a bit-string constant with four binary digits for each hexadecimal digit.

Both forms of bit-string constant can be continued across lines in the same way as regular string constants. Dollar quoting cannot be used in a bit-string constant.

#### 4.1.2.6. Numeric Constants



Numeric constants are accepted in these general forms:

```
digits
digits
.[
digits
][
e[
+-
]
digits
]
[
digits
].
digits
[
e[
+-
]
digits
]

digits
e[
+-
]
digits
```

where_`digits`_is one or more decimal digits \(0 through 9\). At least one digit must be before or after the decimal point, if one is used. At least one digit must follow the exponent marker \(`e`\), if one is present. There cannot be any spaces or other characters embedded in the constant. Note that any leading plus or minus sign is not actually considered part of the constant; it is an operator applied to the constant.

These are some examples of valid numeric constants:

42  
3.5  
4.  
.001  
5e2  
1.925e-3

A numeric constant that contains neither a decimal point nor an exponent is initially presumed to be type`integer`if its value fits in type`integer`\(32 bits\); otherwise it is presumed to be type`bigint`if its value fits in type`bigint`\(64 bits\); otherwise it is taken to be type`numeric`. Constants that contain decimal points and/or exponents are always initially presumed to be type`numeric`.

The initially assigned data type of a numeric constant is just a starting point for the type resolution algorithms. In most cases the constant will be automatically coerced to the most appropriate type depending on context. When necessary, you can force a numeric value to be interpreted as a specific data type by casting it.For example, you can force a numeric value to be treated as type`real`\(`float4`\) by writing:

```
REAL '1.23'  -- string style
1.23::REAL   -- PostgreSQL (historical) style

```

These are actually just special cases of the general casting notations discussed next.

#### 4.1.2.7. Constants of Other Types



A constant of an_arbitrary_type can be entered using any one of the following notations:

```
type
 '
string
'
'
string
'::
type

CAST ( '
string
' AS 
type
 )

```

The string constant's text is passed to the input conversion routine for the type called_`type`_. The result is a constant of the indicated type. The explicit type cast can be omitted if there is no ambiguity as to the type the constant must be \(for example, when it is assigned directly to a table column\), in which case it is automatically coerced.

The string constant can be written using either regular SQL notation or dollar-quoting.

It is also possible to specify a type coercion using a function-like syntax:

```
typename
 ( '
string
' )

```

but not all type names can be used in this way; see[Section 4.2.9](https://www.postgresql.org/docs/10/static/sql-expressions.html#sql-syntax-type-casts)for details.

The`::`,`CAST()`, and function-call syntaxes can also be used to specify run-time type conversions of arbitrary expressions, as discussed in[Section 4.2.9](https://www.postgresql.org/docs/10/static/sql-expressions.html#sql-syntax-type-casts). To avoid syntactic ambiguity, the_`type`_'_`string`_'syntax can only be used to specify the type of a simple literal constant. Another restriction on the_`type`_'_`string`_'syntax is that it does not work for array types; use`::`or`CAST()`to specify the type of an array constant.

The`CAST()`syntax conforms to SQL. The_`type`_'_`string`_'syntax is a generalization of the standard: SQL specifies this syntax only for a few data types, butPostgreSQLallows it for all types. The syntax with`::`is historicalPostgreSQLusage, as is the function-call syntax.

### 4.1.3. Operators



An operator name is a sequence of up to`NAMEDATALEN`-1 \(63 by default\) characters from the following list:

+ - \* / &lt;&gt; = ~ ! @ \# % ^ & \| \` ?

There are a few restrictions on operator names, however:

* `--`and`/*`cannot appear anywhere in an operator name, since they will be taken as the start of a comment.

* A multiple-character operator name cannot end in`+`or`-`, unless the name also contains at least one of these characters:

  ~ ! @ \# % ^ & \| \` ?

  For example,`@-`is an allowed operator name, but`*-`is not. This restriction allowsPostgreSQLto parse SQL-compliant queries without requiring spaces between tokens.

When working with non-SQL-standard operator names, you will usually need to separate adjacent operators with spaces to avoid ambiguity. For example, if you have defined a left unary operator named`@`, you cannot write`X*@Y`; you must write`X* @Y`to ensure thatPostgreSQLreads it as two operator names not one.

### 4.1.4. Special Characters

Some characters that are not alphanumeric have a special meaning that is different from being an operator. Details on the usage can be found at the location where the respective syntax element is described. This section only exists to advise the existence and summarize the purposes of these characters.

* A dollar sign \(`$`\) followed by digits is used to represent a positional parameter in the body of a function definition or a prepared statement. In other contexts the dollar sign can be part of an identifier or a dollar-quoted string constant.

* Parentheses \(`()`\) have their usual meaning to group expressions and enforce precedence. In some cases parentheses are required as part of the fixed syntax of a particular SQL command.

* Brackets \(`[]`\) are used to select the elements of an array. See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html)for more information on arrays.

* Commas \(`,`\) are used in some syntactical constructs to separate the elements of a list.

* The semicolon \(`;`\) terminates an SQL command. It cannot appear anywhere within a command, except within a string constant or quoted identifier.

* The colon \(`:`\) is used to select“slices”from arrays. \(See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html).\) In certain SQL dialects \(such as Embedded SQL\), the colon is used to prefix variable names.

* The asterisk \(`*`\) is used in some contexts to denote all the fields of a table row or composite value. It also has a special meaning when used as the argument of an aggregate function, namely that the aggregate does not require any explicit parameter.

* The period \(`.`\) is used in numeric constants, and to separate schema, table, and column names.

### 4.1.5. Comments



A comment is a sequence of characters beginning with double dashes and extending to the end of the line, e.g.:

```
-- This is a standard SQL comment

```

Alternatively, C-style block comments can be used:

```
/* multiline comment
 * with nesting: /* nested block comment */
 */

```

where the comment begins with`/*`and extends to the matching occurrence of`*/`. These block comments nest, as specified in the SQL standard but unlike C, so that one can comment out larger blocks of code that might contain existing block comments.

A comment is removed from the input stream before further syntax analysis and is effectively replaced by whitespace.

### 4.1.6. Operator Precedence



[Table 4.2](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-precedence-table)shows the precedence and associativity of the operators inPostgreSQL. Most operators have the same precedence and are left-associative. The precedence and associativity of the operators is hard-wired into the parser.

You will sometimes need to add parentheses when using combinations of binary and unary operators. For instance:

```
SELECT 5 ! - 6;

```

will be parsed as:

```
SELECT 5 ! (- 6);

```

because the parser has no idea — until it is too late — that`!`is defined as a postfix operator, not an infix one. To get the desired behavior in this case, you must write:

```
SELECT (5 !) - 6;

```

This is the price one pays for extensibility.

**Table 4.2. Operator Precedence \(highest to lowest\)**

| Operator/Element | Associativity | Description |
| :--- | :--- | :--- |
| `.` | left | table/column name separator |
| `::` | left | PostgreSQL-style typecast |
| `[]` | left | array element selection |
| `+-` | right | unary plus, unary minus |
| `^` | left | exponentiation |
| `*/%` | left | multiplication, division, modulo |
| `+-` | left | addition, subtraction |
| \(any other operator\) | left | all other native and user-defined operators |
| `BETWEENINLIKEILIKESIMILAR` |  | range containment, set membership, string matching |
| `<>=<=>=<>` |  | comparison operators |
| `ISISNULLNOTNULL` |  | `IS TRUE`,`IS FALSE`,`IS NULL`,`IS DISTINCT FROM`, etc |
| `NOT` | right | logical negation |
| `AND` | left | logical conjunction |
| `OR` | left | logical disjunction |

  


Note that the operator precedence rules also apply to user-defined operators that have the same names as the built-in operators mentioned above. For example, if you define a“+”operator for some custom data type it will have the same precedence as the built-in“+”operator, no matter what yours does.

When a schema-qualified operator name is used in the`OPERATOR`syntax, as for example in:

```
SELECT 3 OPERATOR(pg_catalog.+) 4;

```

the`OPERATOR`construct is taken to have the default precedence shown in[Table 4.2](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-precedence-table)for“any other operator”. This is true no matter which specific operator appears inside`OPERATOR()`.

### Note

PostgreSQLversions before 9.5 used slightly different operator precedence rules. In particular,`<=>=`and`<>`used to be treated as generic operators;`IS`tests used to have higher priority; and`NOT BETWEEN`and related constructs acted inconsistently, being taken in some cases as having the precedence of`NOT`rather than`BETWEEN`. These rules were changed for better compliance with the SQL standard and to reduce confusion from inconsistent treatment of logically equivalent constructs. In most cases, these changes will result in no behavioral change, or perhaps in“no such operator”failures which can be resolved by adding parentheses. However there are corner cases in which a query might change behavior without any parsing error being reported. If you are concerned about whether these changes have silently broken something, you can test your application with the configuration parameter[operator\_precedence\_warning](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#guc-operator-precedence-warning)turned on to see if any warnings are logged.

---

  


[^1]: [PostgreSQL: Documentation: 10: 4.1. Lexical Structure](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html)

