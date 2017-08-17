# 9.5. 位元字串函式及運算子[^1]

This section describes functions and operators for examining and manipulating values of type`bytea`.

SQLdefines some string functions that use key words, rather than commas, to separate arguments. Details are in[Table 9.11](https://www.postgresql.org/docs/10/static/functions-binarystring.html#functions-binarystring-sql).PostgreSQLalso provides versions of these functions that use the regular function invocation syntax \(see[Table 9.12](https://www.postgresql.org/docs/10/static/functions-binarystring.html#functions-binarystring-other)\).

### Note

The sample results shown on this page assume that the server parameter[`bytea_output`](https://www.postgresql.org/docs/10/static/runtime-config-client.html#guc-bytea-output)is set to`escape`\(the traditional PostgreSQL format\).

**Table 9.11. SQLBinary String Functions and Operators**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| _`string`_`||`_`string`_ | `bytea` | String concatenation | `E'\\\\Post'::bytea || E'\\047gres\\000'::bytea` | `\\Post'gres\000` |
| `octet_length(`_`string`_\) | `int` | Number of bytes in binary string | `octet_length(E'jo\\000se'::bytea)` | `5` |
| `overlay(`_`string`_placing_`string`_from`int`\[for`int`\]\) | `bytea` | Replace substring | `overlay(E'Th\\000omas'::bytea placing E'\\002\\003'::bytea from 2 for 3)` | `T\\002\\003mas` |
| `position(`_`substring`_in_`string`_\) | `int` | Location of specified substring | `position(E'\\000om'::bytea in E'Th\\000omas'::bytea)` | `3` |
| `substring(`_`string`_\[from`int`\] \[for`int`\]\) | `bytea` | Extract substring | `substring(E'Th\\000omas'::bytea from 2 for 3)` | `h\000o` |
| `trim([both]`_`bytes`_from_`string`_\) | `bytea` | Remove the longest string containing only bytes appearing in_`bytes`_from the start and end of_`string`_ | `trim(E'\\000\\001'::bytea from E'\\000Tom\\001'::bytea)` | `Tom` |

  


Additional binary string manipulation functions are available and are listed in[Table 9.12](https://www.postgresql.org/docs/10/static/functions-binarystring.html#functions-binarystring-other). Some of them are used internally to implement theSQL-standard string functions listed in[Table 9.11](https://www.postgresql.org/docs/10/static/functions-binarystring.html#functions-binarystring-sql).

**Table 9.12. Other Binary String Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `btrim(`_`string`_`bytea`,_`bytes`_`bytea`\) | `bytea` | Remove the longest string containing only bytes appearing in_`bytes`_from the start and end of_`string`_ | `btrim(E'\\000trim\\001'::bytea, E'\\000\\001'::bytea)` | `trim` |
| `decode(`_`string`_`text`,_`format`_`text`\) | `bytea` | Decode binary data from textual representation in_`string`_. Options for_`format`_are same as in`encode`. | `decode(E'123\\000456', 'escape')` | `123\000456` |
| `encode(`_`data`_`bytea`,_`format`_`text`\) | `text` | Encode binary data into a textual representation. Supported formats are:`base64`,`hex`,`escape`.`escape`converts zero bytes and high-bit-set bytes to octal sequences \(`\`_`nnn`_\) and doubles backslashes. | `encode(E'123\\000456'::bytea, 'escape')` | `123\000456` |
| `get_bit(`_`string`_,_`offset`_\) | `int` | Extract bit from string | `get_bit(E'Th\\000omas'::bytea, 45)` | `1` |
| `get_byte(`_`string`_,_`offset`_\) | `int` | Extract byte from string | `get_byte(E'Th\\000omas'::bytea, 4)` | `109` |
| `length(`_`string`_\) | `int` | Length of binary string | `length(E'jo\\000se'::bytea)` | `5` |
| `md5(`_`string`_\) | `text` | Calculates the MD5 hash of_`string`_, returning the result in hexadecimal | `md5(E'Th\\000omas'::bytea)` | `8ab2d3c9689aaf18 b4958c334c82d8b1` |
| `set_bit(`_`string`_,_`offset`_,_`newvalue`_\) | `bytea` | Set bit in string | `set_bit(E'Th\\000omas'::bytea, 45, 0)` | `Th\000omAs` |
| `set_byte(`_`string`_,_`offset`_,_`newvalue`_\) | `bytea` | Set byte in string | `set_byte(E'Th\\000omas'::bytea, 4, 64)` | `Th\000o@as` |

  


`get_byte`and`set_byte`number the first byte of a binary string as byte 0.`get_bit`and`set_bit`number bits from the right within each byte; for example bit 0 is the least significant bit of the first byte, and bit 15 is the most significant bit of the second byte.

See also the aggregate function`string_agg`in[Section 9.20](https://www.postgresql.org/docs/10/static/functions-aggregate.html)and the large object functions in[Section 34.4](https://www.postgresql.org/docs/10/static/lo-funcs.html).

---

  


[^1]:  [PostgreSQL: Documentation: 10: 9.5. Binary String Functions and Operators](https://www.postgresql.org/docs/10/static/functions-binarystring.html)

