# 9.5. 位元字串函式及運算子

This section describes functions and operators for examining and manipulating values of type `bytea`.

SQL defines some string functions that use key words, rather than commas, to separate arguments. Details are in [Table 9.12](https://www.postgresql.org/docs/12/functions-binarystring.html#FUNCTIONS-BINARYSTRING-SQL). PostgreSQL also provides versions of these functions that use the regular function invocation syntax \(see [Table 9.13](https://www.postgresql.org/docs/12/functions-binarystring.html#FUNCTIONS-BINARYSTRING-OTHER)\).

#### Note

The sample results shown on this page assume that the server parameter [`bytea_output`](https://www.postgresql.org/docs/12/runtime-config-client.html#GUC-BYTEA-OUTPUT) is set to `escape` \(the traditional PostgreSQL format\).

#### **Table 9.12. SQL Binary String Functions and Operators**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| _`string`_ `||` _`string`_ | `bytea` | String concatenation | `'\\Post'::bytea || '\047gres\000'::bytea` | `\\Post'gres\000` |
| `octet_length(`_`string`_\) | `int` | Number of bytes in binary string | `octet_length('jo\000se'::bytea)` | `5` |
| `overlay(`_`string`_ placing _`string`_ from `int` \[for `int`\]\) | `bytea` | Replace substring | `overlay('Th\000omas'::bytea placing '\002\003'::bytea from 2 for 3)` | `T\\002\\003mas` |
| `position(`_`substring`_ in _`string`_\) | `int` | Location of specified substring | `position('\000om'::bytea in 'Th\000omas'::bytea)` | `3` |
| `substring(`_`string`_ \[from `int`\] \[for `int`\]\) | `bytea` | Extract substring | `substring('Th\000omas'::bytea from 2 for 3)` | `h\000o` |
| `trim([both]` _`bytes`_ from _`string`_\) | `bytea` | Remove the longest string containing only bytes appearing in _`bytes`_ from the start and end of _`string`_ | `trim('\000\001'::bytea from '\000Tom\001'::bytea)` | `Tom` |

Additional binary string manipulation functions are available and are listed in [Table 9.13](https://www.postgresql.org/docs/12/functions-binarystring.html#FUNCTIONS-BINARYSTRING-OTHER). Some of them are used internally to implement the SQL-standard string functions listed in [Table 9.12](https://www.postgresql.org/docs/12/functions-binarystring.html#FUNCTIONS-BINARYSTRING-SQL).

#### **Table 9.13. Other Binary String Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `btrim(`_`string`_ `bytea`, _`bytes`_ `bytea`\) | `bytea` | Remove the longest string containing only bytes appearing in _`bytes`_ from the start and end of _`string`_ | `btrim('\000trim\001'::bytea, '\000\001'::bytea)` | `trim` |
| `decode(`_`string`_ `text`, _`format`_ `text`\) | `bytea` | Decode binary data from textual representation in _`string`_. Options for _`format`_ are same as in `encode`. | `decode('123\000456', 'escape')` | `123\000456` |
| `encode(`_`data`_ `bytea`, _`format`_ `text`\) | `text` | Encode binary data into a textual representation. Supported formats are: `base64`, `hex`, `escape`. `escape` converts zero bytes and high-bit-set bytes to octal sequences \(`\`_`nnn`_\) and doubles backslashes. | `encode('123\000456'::bytea, 'escape')` | `123\000456` |
| `get_bit(`_`string`_, _`offset`_\) | `int` | Extract bit from string | `get_bit('Th\000omas'::bytea, 45)` | `1` |
| `get_byte(`_`string`_, _`offset`_\) | `int` | Extract byte from string | `get_byte('Th\000omas'::bytea, 4)` | `109` |
| `length(`_`string`_\) | `int` | Length of binary string | `length('jo\000se'::bytea)` | `5` |
| `md5(`_`string`_\) | `text` | Calculates the MD5 hash of _`string`_, returning the result in hexadecimal | `md5('Th\000omas'::bytea)` | `8ab2d3c9689aaf18​b4958c334c82d8b1` |
| `set_bit(`_`string`_, _`offset`_, _`newvalue`_\) | `bytea` | Set bit in string | `set_bit('Th\000omas'::bytea, 45, 0)` | `Th\000omAs` |
| `set_byte(`_`string`_, _`offset`_, _`newvalue`_\) | `bytea` | Set byte in string | `set_byte('Th\000omas'::bytea, 4, 64)` | `Th\000o@as` |
| `sha224(bytea`\) | `bytea` | SHA-224 hash | `sha224('abc')` | `\x23097d223405d8228642a477bda2​55b32aadbce4bda0b3f7e36c9da7` |
| `sha256(bytea`\) | `bytea` | SHA-256 hash | `sha256('abc')` | `\xba7816bf8f01cfea414140de5dae2223​b00361a396177a9cb410ff61f20015ad` |
| `sha384(bytea`\) | `bytea` | SHA-384 hash | `sha384('abc')` | `\xcb00753f45a35e8bb5a03d699ac65007​272c32ab0eded1631a8b605a43ff5bed​8086072ba1e7cc2358baeca134c825a7` |
| `sha512(bytea`\) | `bytea` | SHA-512 hash | `sha512('abc')` | `\xddaf35a193617abacc417349ae204131​12e6fa4e89a97ea20a9eeee64b55d39a​2192992a274fc1a836ba3c23a3feebbd​454d4423643ce80e2a9ac94fa54ca49f` |

`get_byte` and `set_byte` number the first byte of a binary string as byte 0. `get_bit` and `set_bit` number bits from the right within each byte; for example bit 0 is the least significant bit of the first byte, and bit 15 is the most significant bit of the second byte.

Note that for historic reasons, the function `md5` returns a hex-encoded value of type `text` whereas the SHA-2 functions return type `bytea`. Use the functions `encode` and `decode` to convert between the two, for example `encode(sha256('abc'), 'hex')` to get a hex-encoded text representation.

See also the aggregate function `string_agg` in [Section 9.20](https://www.postgresql.org/docs/12/functions-aggregate.html) and the large object functions in [Section 34.4](https://www.postgresql.org/docs/12/lo-funcs.html).

