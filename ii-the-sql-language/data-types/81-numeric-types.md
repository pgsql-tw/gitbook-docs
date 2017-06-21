# 8.1. 數字型別[^1]

Numeric types consist of two-, four-, and eight-byte integers, four- and eight-byte floating-point numbers, and selectable-precision decimals.[Table 8.2](https://www.postgresql.org/docs/10/static/datatype-numeric.html#datatype-numeric-table)lists the available types.

**Table 8.2. Numeric Types**

| Name | Storage Size | Description | Range |
| :--- | :--- | :--- | :--- |
| `smallint` | 2 bytes | small-range integer | -32768 to +32767 |
| `integer` | 4 bytes | typical choice for integer | -2147483648 to +2147483647 |
| `bigint` | 8 bytes | large-range integer | -9223372036854775808 to +9223372036854775807 |
| `decimal` | variable | user-specified precision, exact | up to 131072 digits before the decimal point; up to 16383 digits after the decimal point |
| `numeric` | variable | user-specified precision, exact | up to 131072 digits before the decimal point; up to 16383 digits after the decimal point |
| `real` | 4 bytes | variable-precision, inexact | 6 decimal digits precision |
| `double precision` | 8 bytes | variable-precision, inexact | 15 decimal digits precision |
| `smallserial` | 2 bytes | small autoincrementing integer | 1 to 32767 |
| `serial` | 4 bytes | autoincrementing integer | 1 to 2147483647 |
| `bigserial` | 8 bytes | large autoincrementing integer | 1 to 9223372036854775807 |

  


The syntax of constants for the numeric types is described in[Section 4.1.2](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-syntax-constants). The numeric types have a full set of corresponding arithmetic operators and functions. Refer to[Chapter 9](https://www.postgresql.org/docs/10/static/functions.html)for more information. The following sections describe the types in detail.

### 8.1.1. Integer Types













The types`smallint`,`integer`, and`bigint`store whole numbers, that is, numbers without fractional components, of various ranges. Attempts to store values outside of the allowed range will result in an error.

The type`integer`is the common choice, as it offers the best balance between range, storage size, and performance. The`smallint`type is generally only used if disk space is at a premium. The`bigint`type is designed to be used when the range of the`integer`type is insufficient.

SQLonly specifies the integer types`integer`\(or`int`\),`smallint`, and`bigint`. The type names`int2`,`int4`, and`int8`are extensions, which are also used by some otherSQLdatabase systems.

### 8.1.2. Arbitrary Precision Numbers







The type`numeric`can store numbers with a very large number of digits. It is especially recommended for storing monetary amounts and other quantities where exactness is required. Calculations with`numeric`values yield exact results where possible, e.g. addition, subtraction, multiplication. However, calculations on`numeric`values are very slow compared to the integer types, or to the floating-point types described in the next section.

We use the following terms below: The_scale_of a`numeric`is the count of decimal digits in the fractional part, to the right of the decimal point. The_precision_of a`numeric`is the total count of significant digits in the whole number, that is, the number of digits to both sides of the decimal point. So the number 23.5141 has a precision of 6 and a scale of 4. Integers can be considered to have a scale of zero.

Both the maximum precision and the maximum scale of a`numeric`column can be configured. To declare a column of type`numeric`use the syntax:

```
NUMERIC(
precision
, 
scale
)

```

The precision must be positive, the scale zero or positive. Alternatively:

```
NUMERIC(
precision
)

```

selects a scale of 0. Specifying:

```
NUMERIC

```

without any precision or scale creates a column in which numeric values of any precision and scale can be stored, up to the implementation limit on precision. A column of this kind will not coerce input values to any particular scale, whereas`numeric`columns with a declared scale will coerce input values to that scale. \(TheSQLstandard requires a default scale of 0, i.e., coercion to integer precision. We find this a bit useless. If you're concerned about portability, always specify the precision and scale explicitly.\)

### Note

The maximum allowed precision when explicitly specified in the type declaration is 1000;`NUMERIC`without a specified precision is subject to the limits described in[Table 8.2](https://www.postgresql.org/docs/10/static/datatype-numeric.html#datatype-numeric-table).

If the scale of a value to be stored is greater than the declared scale of the column, the system will round the value to the specified number of fractional digits. Then, if the number of digits to the left of the decimal point exceeds the declared precision minus the declared scale, an error is raised.

Numeric values are physically stored without any extra leading or trailing zeroes. Thus, the declared precision and scale of a column are maximums, not fixed allocations. \(In this sense the`numeric`type is more akin to`varchar(`_`n`_\)than to`char(`_`n`_\).\) The actual storage requirement is two bytes for each group of four decimal digits, plus three to eight bytes overhead.





In addition to ordinary numeric values, the`numeric`type allows the special value`NaN`, meaning“not-a-number”. Any operation on`NaN`yields another`NaN`. When writing this value as a constant in an SQL command, you must put quotes around it, for example`UPDATE table SET x = 'NaN'`. On input, the string`NaN`is recognized in a case-insensitive manner.

### Note

In most implementations of the“not-a-number”concept,`NaN`is not considered equal to any other numeric value \(including`NaN`\). In order to allow`numeric`values to be sorted and used in tree-based indexes,PostgreSQLtreats`NaN`values as equal, and greater than all non-`NaN`values.

The types`decimal`and`numeric`are equivalent. Both types are part of theSQLstandard.

When rounding values, the`numeric`type rounds ties away from zero, while \(on most machines\) the`real`and`double precision`types round ties to the nearest even number. For example:

```
SELECT x,
  round(x::numeric) AS num_round,
  round(x::double precision) AS dbl_round
FROM generate_series(-3.5, 3.5, 1) as x;
  x   | num_round | dbl_round
------+-----------+-----------
 -3.5 |        -4 |        -4
 -2.5 |        -3 |        -2
 -1.5 |        -2 |        -2
 -0.5 |        -1 |        -0
  0.5 |         1 |         0
  1.5 |         2 |         2
  2.5 |         3 |         2
  3.5 |         4 |         4
(8 rows)

```

### 8.1.3. Floating-Point Types











The data types`real`and`double precision`are inexact, variable-precision numeric types. In practice, these types are usually implementations ofIEEEStandard 754 for Binary Floating-Point Arithmetic \(single and double precision, respectively\), to the extent that the underlying processor, operating system, and compiler support it.

Inexact means that some values cannot be converted exactly to the internal format and are stored as approximations, so that storing and retrieving a value might show slight discrepancies. Managing these errors and how they propagate through calculations is the subject of an entire branch of mathematics and computer science and will not be discussed here, except for the following points:

* If you require exact storage and calculations \(such as for monetary amounts\), use the`numeric`type instead.

* If you want to do complicated calculations with these types for anything important, especially if you rely on certain behavior in boundary cases \(infinity, underflow\), you should evaluate the implementation carefully.

* Comparing two floating-point values for equality might not always work as expected.

On most platforms, the`real`type has a range of at least 1E-37 to 1E+37 with a precision of at least 6 decimal digits. The`double precision`type typically has a range of around 1E-307 to 1E+308 with a precision of at least 15 digits. Values that are too large or too small will cause an error. Rounding might take place if the precision of an input number is too high. Numbers too close to zero that are not representable as distinct from zero will cause an underflow error.

### Note

The[extra\_float\_digits](https://www.postgresql.org/docs/10/static/runtime-config-client.html#guc-extra-float-digits)setting controls the number of extra significant digits included when a floating point value is converted to text for output. With the default value of`0`, the output is the same on every platform supported by PostgreSQL. Increasing it will produce output that more accurately represents the stored value, but may be unportable.



In addition to ordinary numeric values, the floating-point types have several special values:

`Infinity`  
`-Infinity`  
`NaN`

These represent the IEEE 754 special values“infinity”,“negative infinity”, and“not-a-number”, respectively. \(On a machine whose floating-point arithmetic does not follow IEEE 754, these values will probably not work as expected.\) When writing these values as constants in an SQL command, you must put quotes around them, for example`UPDATE table SET x = '-Infinity'`. On input, these strings are recognized in a case-insensitive manner.

### Note

IEEE754 specifies that`NaN`should not compare equal to any other floating-point value \(including`NaN`\). In order to allow floating-point values to be sorted and used in tree-based indexes,PostgreSQLtreats`NaN`values as equal, and greater than all non-`NaN`values.

PostgreSQLalso supports the SQL-standard notations`float`and`float(`_`p`_\)for specifying inexact numeric types. Here,_`p`_specifies the minimum acceptable precision in_binary_digits.PostgreSQLaccepts`float(1)`to`float(24)`as selecting the`real`type, while`float(25)`to`float(53)`select`double precision`. Values of_`p`_outside the allowed range draw an error.`float`with no precision specified is taken to mean`double precision`.

### Note

The assumption that`real`and`double precision`have exactly 24 and 53 bits in the mantissa respectively is correct for IEEE-standard floating point implementations. On non-IEEE platforms it might be off a little, but for simplicity the same ranges of_`p`_are used on all platforms.

### 8.1.4. Serial Types

















The data types`smallserial`,`serial`and`bigserial`are not true types, but merely a notational convenience for creating unique identifier columns \(similar to the`AUTO_INCREMENT`property supported by some other databases\). In the current implementation, specifying:

```
CREATE TABLE 
tablename
 (
    
colname
 SERIAL
);

```

is equivalent to specifying:

```
CREATE SEQUENCE 
tablename
_
colname
_seq;
CREATE TABLE 
tablename
 (
    
colname
 integer NOT NULL DEFAULT nextval('
tablename
_
colname
_seq')
);
ALTER SEQUENCE 
tablename
_
colname
_seq OWNED BY 
tablename
.
colname
;

```

Thus, we have created an integer column and arranged for its default values to be assigned from a sequence generator. A`NOT NULL`constraint is applied to ensure that a null value cannot be inserted. \(In most cases you would also want to attach a`UNIQUE`or`PRIMARY KEY`constraint to prevent duplicate values from being inserted by accident, but this is not automatic.\) Lastly, the sequence is marked as“owned by”the column, so that it will be dropped if the column or table is dropped.

### Note

Because`smallserial`,`serial`and`bigserial`are implemented using sequences, there may be "holes" or gaps in the sequence of values which appears in the column, even if no rows are ever deleted. A value allocated from the sequence is still "used up" even if a row containing that value is never successfully inserted into the table column. This may happen, for example, if the inserting transaction rolls back. See`nextval()`in[Section 9.16](https://www.postgresql.org/docs/10/static/functions-sequence.html)for details.

To insert the next value of the sequence into the`serial`column, specify that the`serial`column should be assigned its default value. This can be done either by excluding the column from the list of columns in the`INSERT`statement, or through the use of the`DEFAULT`key word.

The type names`serial`and`serial4`are equivalent: both create`integer`columns. The type names`bigserial`and`serial8`work the same way, except that they create a`bigint`column.`bigserial`should be used if you anticipate the use of more than 231identifiers over the lifetime of the table. The type names`smallserial`and`serial2`also work the same way, except that they create a`smallint`column.

The sequence created for a`serial`column is automatically dropped when the owning column is dropped. You can drop the sequence without dropping the column, but this will force removal of the column default expression.

---



[^1]: [PostgreSQL: Documentation: 10: 8.1. Numeric Types](https://www.postgresql.org/docs/10/static/datatype-numeric.html)

