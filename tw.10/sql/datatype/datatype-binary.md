# 8.4. 位元組型別

The `bytea` data type allows storage of binary strings; see [Table 8.6](https://www.postgresql.org/docs/10/static/datatype-binary.html#DATATYPE-BINARY-TABLE).

**Table 8.6. Binary Data Types**

| Name | Storage Size | Description |
| --- | --- |
| `bytea` | 1 or 4 bytes plus the actual binary string | variable-length binary string |

A binary string is a sequence of octets \(or bytes\). Binary strings are distinguished from character strings in two ways. First, binary strings specifically allow storing octets of value zero and other “non-printable” octets \(usually, octets outside the range 32 to 126\). Character strings disallow zero octets, and also disallow any other octet values and sequences of octet values that are invalid according to the database's selected character set encoding. Second, operations on binary strings process the actual bytes, whereas the processing of character strings depends on locale settings. In short, binary strings are appropriate for storing data that the programmer thinks of as “raw bytes”, whereas character strings are appropriate for storing text.

The `bytea` type supports two external formats for input and output: PostgreSQL's historical “escape” format, and “hex” format. Both of these are always accepted on input. The output format depends on the configuration parameter [bytea\_output](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-BYTEA-OUTPUT); the default is hex. \(Note that the hex format was introduced in PostgreSQL 9.0; earlier versions and some tools don't understand it.\)

The SQL standard defines a different binary string type, called `BLOB` or `BINARY LARGE OBJECT`. The input format is different from `bytea`, but the provided functions and operators are mostly the same.

#### 8.4.1. `bytea` Hex Format

The “hex” format encodes binary data as 2 hexadecimal digits per byte, most significant nibble first. The entire string is preceded by the sequence `\x` \(to distinguish it from the escape format\). In some contexts, the initial backslash may need to be escaped by doubling it, in the same cases in which backslashes have to be doubled in escape format; details appear below. The hexadecimal digits can be either upper or lower case, and whitespace is permitted between digit pairs \(but not within a digit pair nor in the starting `\x` sequence\). The hex format is compatible with a wide range of external applications and protocols, and it tends to be faster to convert than the escape format, so its use is preferred.

Example:

```text
SELECT E'\\xDEADBEEF';
```

#### 8.4.2. `bytea` Escape Format

The “escape” format is the traditional PostgreSQL format for the `bytea` type. It takes the approach of representing a binary string as a sequence of ASCII characters, while converting those bytes that cannot be represented as an ASCII character into special escape sequences. If, from the point of view of the application, representing bytes as characters makes sense, then this representation can be convenient. But in practice it is usually confusing because it fuzzes up the distinction between binary strings and character strings, and also the particular escape mechanism that was chosen is somewhat unwieldy. So this format should probably be avoided for most new applications.

When entering `bytea` values in escape format, octets of certain values _must_ be escaped, while all octet values _can_ be escaped. In general, to escape an octet, convert it into its three-digit octal value and precede it by a backslash \(or two backslashes, if writing the value as a literal using escape string syntax\). Backslash itself \(octet value 92\) can alternatively be represented by double backslashes. [Table 8.7](https://www.postgresql.org/docs/10/static/datatype-binary.html#DATATYPE-BINARY-SQLESC) shows the characters that must be escaped, and gives the alternative escape sequences where applicable.

**Table 8.7. `bytea` Literal Escaped Octets**

| Decimal Octet Value | Description | Escaped Input Representation | Example | Output Representation |
| --- | --- | --- | --- | --- |
| 0 | zero octet | `E'\\000'` | `SELECT E'\\000'::bytea;` | `\000` |
| 39 | single quote | `''''` or `E'\\047'` | `SELECT E'\''::bytea;` | `'` |
| 92 | backslash | `E'\\\\'` or `E'\\134'` | `SELECT E'\\\\'::bytea;` | `\\` |
| 0 to 31 and 127 to 255 | “non-printable” octets | `E'\\`_`xxx'`_ \(octal value\) | `SELECT E'\\001'::bytea;` | `\001` |

The requirement to escape _non-printable_ octets varies depending on locale settings. In some instances you can get away with leaving them unescaped. Note that the result in each of the examples in [Table 8.7](https://www.postgresql.org/docs/10/static/datatype-binary.html#DATATYPE-BINARY-SQLESC) was exactly one octet in length, even though the output representation is sometimes more than one character.

The reason multiple backslashes are required, as shown in [Table 8.7](https://www.postgresql.org/docs/10/static/datatype-binary.html#DATATYPE-BINARY-SQLESC), is that an input string written as a string literal must pass through two parse phases in the PostgreSQL server. The first backslash of each pair is interpreted as an escape character by the string-literal parser \(assuming escape string syntax is used\) and is therefore consumed, leaving the second backslash of the pair. \(Dollar-quoted strings can be used to avoid this level of escaping.\) The remaining backslash is then recognized by the `bytea` input function as starting either a three digit octal value or escaping another backslash. For example, a string literal passed to the server as `E'\\001'` becomes `\001` after passing through the escape string parser. The `\001` is then sent to the `bytea` input function, where it is converted to a single octet with a decimal value of 1. Note that the single-quote character is not treated specially by `bytea`, so it follows the normal rules for string literals. \(See also [Section 4.1.2.1](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#SQL-SYNTAX-STRINGS).\)

`Bytea` octets are sometimes escaped when output. In general, each “non-printable” octet is converted into its equivalent three-digit octal value and preceded by one backslash. Most “printable” octets are represented by their standard representation in the client character set. The octet with decimal value 92 \(backslash\) is doubled in the output. Details are in [Table 8.8](https://www.postgresql.org/docs/10/static/datatype-binary.html#DATATYPE-BINARY-RESESC).

**Table 8.8. `bytea` Output Escaped Octets**

| Decimal Octet Value | Description | Escaped Output Representation | Example | Output Result |
| --- | --- | --- | --- |
| 92 | backslash | `\\` | `SELECT E'\\134'::bytea;` | `\\` |
| 0 to 31 and 127 to 255 | “non-printable” octets | `\`_`xxx`_ \(octal value\) | `SELECT E'\\001'::bytea;` | `\001` |
| 32 to 126 | “printable” octets | client character set representation | `SELECT E'\\176'::bytea;` | `~` |

Depending on the front end to PostgreSQL you use, you might have additional work to do in terms of escaping and unescaping `bytea` strings. For example, you might also have to escape line feeds and carriage returns if your interface automatically translates these.

