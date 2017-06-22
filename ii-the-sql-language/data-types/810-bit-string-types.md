# 8.10. 位元字串型別[^1]

Bit strings are strings of 1's and 0's. They can be used to store or visualize bit masks. There are two SQL bit types:bit\(n\)andbit varying\(n\), wherenis a positive integer.

bittype data must match the lengthnexactly; it is an error to attempt to store shorter or longer bit strings.bit varyingdata is of variable length up to the maximum lengthn; longer strings will be rejected. Writingbitwithout a length is equivalent tobit\(1\), whilebit varyingwithout a length specification means unlimited length.

> **Note:**If one explicitly casts a bit-string value tobit\(n\), it will be truncated or zero-padded on the right to be exactlynbits, without raising an error. Similarly, if one explicitly casts a bit-string value tobit varying\(n\), it will be truncated on the right if it is more thannbits.

Refer to[Section 4.1.2.5](https://www.postgresql.org/docs/current/static/sql-syntax-lexical.html#SQL-SYNTAX-BIT-STRINGS)for information about the syntax of bit string constants. Bit-logical operators and string manipulation functions are available; see[Section 9.6](https://www.postgresql.org/docs/current/static/functions-bitstring.html).



Example 8-3. Using the Bit String Types

```
CREATE TABLE test (a BIT(3), b BIT VARYING(5));
INSERT INTO test VALUES (B'101', B'00');
INSERT INTO test VALUES (B'10', B'101');

ERROR:  bit string length 2 does not match type bit(3)

INSERT INTO test VALUES (B'10'::bit(3), B'101');
SELECT * FROM test;

  a  |  b
-----+-----
 101 | 00
 100 | 101
```

A bit string value requires 1 byte for each group of 8 bits, plus 5 or 8 bytes overhead depending on the length of the string \(but long values may be compressed or moved out-of-line, as explained in[Section 8.3](https://www.postgresql.org/docs/current/static/datatype-character.html)for character strings\).

---



[^1]: [PostgreSQL: Documentation: 9.6: Bit String Types](https://www.postgresql.org/docs/current/static/datatype-bit.html)

