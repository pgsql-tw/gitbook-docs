# 9.6. 二元字串函式及運算子

This section describes functions and operators for examining and manipulating bit strings, that is values of the types `bit` and `bit varying`. Aside from the usual comparison operators, the operators shown in [Table 9.14](https://www.postgresql.org/docs/12/functions-bitstring.html#FUNCTIONS-BIT-STRING-OP-TABLE) can be used. Bit string operands of `&`, `|`, and `#` must be of equal length. When bit shifting, the original length of the string is preserved, as shown in the examples.

## **Table 9.14. Bit String Operators**

| Operator | Description | Example | Result |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| \` |  | \` | concatenation | \`B'10001' |  | B'011'\` | `10001011` |
| `&` | bitwise AND | `B'10001' & B'01101'` | `00001` |  |  |  |  |
| \` | \` | bitwise OR | \`B'10001' | B'01101'\` | `11101` |  |  |
| `#` | bitwise XOR | `B'10001' # B'01101'` | `11100` |  |  |  |  |
| `~` | bitwise NOT | `~ B'10001'` | `01110` |  |  |  |  |
| `<<` | bitwise shift left | `B'10001' << 3` | `01000` |  |  |  |  |
| `>>` | bitwise shift right | `B'10001' >> 2` | `00100` |  |  |  |  |

The following SQL-standard functions work on bit strings as well as character strings: `length`, `bit_length`, `octet_length`, `position`, `substring`, `overlay`.

The following functions work on bit strings as well as binary strings: `get_bit`, `set_bit`. When working with a bit string, these functions number the first \(leftmost\) bit of the string as bit 0.

In addition, it is possible to cast integral values to and from type `bit`. Some examples:

```text
44::bit(10)                    0000101100
44::bit(3)                     100
cast(-44 as bit(12))           111111010100
'1110'::bit(4)::integer        14
```

Note that casting to just “bit” means casting to `bit(1)`, and so will deliver only the least significant bit of the integer.

## Note

Casting an integer to `bit(n)` copies the rightmost `n` bits. Casting an integer to a bit string width wider than the integer itself will sign-extend on the left.

