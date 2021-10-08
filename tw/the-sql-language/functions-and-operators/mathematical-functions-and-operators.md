# 9.3. 數學函式及運算子

本節提供了 PostgreSQL 的數學運算方式。對於沒有標準數學約定的型別（例如，日期/時間型別），我們將在後續部分中介紹具體的行為。

[Table 9.4](mathematical-functions-and-operators.md#table-9-4-mathematical-operators) 列出了可用的數學運算子。

## **Table 9.4. Mathematical Operators**

| Operator | Description | Example | Result |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `+` | addition | `2 + 3` | `5` |  |  |  |  |
| `-` | subtraction | `2 - 3` | `-1` |  |  |  |  |
| `*` | multiplication | `2 * 3` | `6` |  |  |  |  |
| `/` | division \(integer division truncates the result\) | `4 / 2` | `2` |  |  |  |  |
| `%` | modulo \(remainder\) | `5 % 4` | `1` |  |  |  |  |
| `^` | exponentiation \(associates left to right\) | `2.0 ^ 3.0` | `8` |  |  |  |  |
| \` | /\` | square root | \` | / 25.0\` | `5` |  |  |
| \` |  | /\` | cube root | \` |  | / 27.0\` | `3` |
| `!` | factorial | `5 !` | `120` |  |  |  |  |
| `!!` | factorial \(prefix operator\) | `!! 5` | `120` |  |  |  |  |
| `@` | absolute value | `@ -5.0` | `5` |  |  |  |  |
| `&` | bitwise AND | `91 & 15` | `11` |  |  |  |  |
| \` | \` | bitwise OR | \`32 | 3\` | `35` |  |  |
| `#` | bitwise XOR | `17 # 5` | `20` |  |  |  |  |
| `~` | bitwise NOT | `~1` | `-2` |  |  |  |  |
| `<<` | bitwise shift left | `1 << 4` | `16` |  |  |  |  |
| `>>` | bitwise shift right | `8 >> 2` | `2` |  |  |  |  |

位元運算子僅適用於整數資料型別，也可用於位元字串型別的位元和位元變化，如 [Table 9.14](bit-string-functions-and-operators.md#table-9-14-bit-string-operators) 所示。

[Table 9.5](mathematical-functions-and-operators.md#table-9-5-mathematical-functions) 列出了可用的數學函數。在該表中，dp 表示雙精確度。這些函數中的許多函數都提供了多種形式，且具有不同的參數型別。除非另有說明，否則函數的任何形式都將回傳與其參數相同的資料型別。使用雙精確度資料的功能主要以主機系統的 C 函式庫實作； 因此，邊界情況下的準確性和行為可能會因主機系統而有所差異。

## **Table 9.5. Mathematical Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `abs(`_`x`_\) | \(same as input\) | absolute value | `abs(-17.4)` | `17.4` |
| `cbrt(dp`\) | `dp` | cube root | `cbrt(27.0)` | `3` |
| `ceil(dp` or `numeric`\) | \(same as input\) | nearest integer greater than or equal to argument | `ceil(-42.8)` | `-42` |
| `ceiling(dp` or `numeric`\) | \(same as input\) | nearest integer greater than or equal to argument \(same as `ceil`\) | `ceiling(-95.3)` | `-95` |
| `degrees(dp`\) | `dp` | radians to degrees | `degrees(0.5)` | `28.6478897565412` |
| `div(`_`y`_ `numeric`, _`x`_ `numeric`\) | `numeric` | integer quotient of _`y`_/_`x`_ | `div(9,4)` | `2` |
| `exp(dp` or `numeric`\) | \(same as input\) | exponential | `exp(1.0)` | `2.71828182845905` |
| `floor(dp` or `numeric`\) | \(same as input\) | nearest integer less than or equal to argument | `floor(-42.8)` | `-43` |
| `ln(dp` or `numeric`\) | \(same as input\) | natural logarithm | `ln(2.0)` | `0.693147180559945` |
| `log(dp` or `numeric`\) | \(same as input\) | base 10 logarithm | `log(100.0)` | `2` |
| `log10(dp` or `numeric`\) | \(same as input\) | base 10 logarithm | `log10(100.0)` | `2` |
| `log(`_`b`_ `numeric`, _`x`_ `numeric`\) | `numeric` | logarithm to base _`b`_ | `log(2.0, 64.0)` | `6.0000000000` |
| `mod(`_`y`_, _`x`_\) | \(same as argument types\) | remainder of _`y`_/_`x`_ | `mod(9,4)` | `1` |
| `pi()` | `dp` | “π” constant | `pi()` | `3.14159265358979` |
| `power(`_`a`_ `dp`, _`b`_ `dp`\) | `dp` | _`a`_ raised to the power of _`b`_ | `power(9.0, 3.0)` | `729` |
| `power(`_`a`_ `numeric`, _`b`_ `numeric`\) | `numeric` | _`a`_ raised to the power of _`b`_ | `power(9.0, 3.0)` | `729` |
| `radians(dp`\) | `dp` | degrees to radians | `radians(45.0)` | `0.785398163397448` |
| `round(dp` or `numeric`\) | \(same as input\) | round to nearest integer | `round(42.4)` | `42` |
| `round(`_`v`_ `numeric`, _`s`_ `int`\) | `numeric` | round to _`s`_ decimal places | `round(42.4382, 2)` | `42.44` |
| `scale(numeric`\) | `integer` | scale of the argument \(the number of decimal digits in the fractional part\) | `scale(8.41)` | `2` |
| `sign(dp` or `numeric`\) | \(same as input\) | sign of the argument \(-1, 0, +1\) | `sign(-8.4)` | `-1` |
| `sqrt(dp` or `numeric`\) | \(same as input\) | square root | `sqrt(2.0)` | `1.4142135623731` |
| `trunc(dp` or `numeric`\) | \(same as input\) | truncate toward zero | `trunc(42.8)` | `42` |
| `trunc(`_`v`_ `numeric`, _`s`_ `int`\) | `numeric` | truncate to _`s`_ decimal places | `trunc(42.4382, 2)` | `42.43` |
| `width_bucket(`_`operand`_ `dp`, _`b1`_ `dp`, _`b2`_ `dp`, _`count`_ `int`\) | `int` | return the bucket number to which _`operand`_ would be assigned in a histogram having _`count`_ equal-width buckets spanning the range _`b1`_ to _`b2`_; returns `0` or _`count`_+1 for an input outside the range | `width_bucket(5.35, 0.024, 10.06, 5)` | `3` |
| `width_bucket(`_`operand`_ `numeric`, _`b1`_ `numeric`, _`b2`_ `numeric`, _`count`_ `int`\) | `int` | return the bucket number to which _`operand`_ would be assigned in a histogram having _`count`_ equal-width buckets spanning the range _`b1`_ to _`b2`_; returns `0` or _`count`_+1 for an input outside the range | `width_bucket(5.35, 0.024, 10.06, 5)` | `3` |
| `width_bucket(`_`operand`_ `anyelement`, _`thresholds`_ `anyarray`\) | `int` | return the bucket number to which _`operand`_ would be assigned given an array listing the lower bounds of the buckets; returns `0` for an input less than the first lower bound; the _`thresholds`_ array _must be sorted_, smallest first, or unexpected results will be obtained | `width_bucket(now(), array['yesterday', 'today', 'tomorrow']::timestamptz[])` | `2` |

[Table 9.6](https://www.postgresql.org/docs/12/functions-math.html#FUNCTIONS-MATH-RANDOM-TABLE) shows functions for generating random numbers.

## **Table 9.6. Random Functions**

| Function | Return Type | Description |
| :--- | :--- | :--- |
| `random()` | `dp` | random value in the range 0.0 &lt;= x &lt; 1.0 |
| `setseed(dp`\) | `void` | set seed for subsequent `random()` calls \(value between -1.0 and 1.0, inclusive\) |

The `random()` function uses a simple linear congruential algorithm. It is fast but not suitable for cryptographic applications; see the [pgcrypto](https://www.postgresql.org/docs/12/pgcrypto.html) module for a more secure alternative. If `setseed()` is called, the results of subsequent `random()` calls in the current session are repeatable by re-issuing `setseed()` with the same argument.

[Table 9.7](https://www.postgresql.org/docs/12/functions-math.html#FUNCTIONS-MATH-TRIG-TABLE) shows the available trigonometric functions. All these functions take arguments and return values of type `double precision`. Each of the trigonometric functions comes in two variants, one that measures angles in radians and one that measures angles in degrees.

## **Table 9.7. Trigonometric Functions**

| Function \(radians\) | Function \(degrees\) | Description |
| :--- | :--- | :--- |
| `acos(`_`x`_\) | `acosd(`_`x`_\) | inverse cosine |
| `asin(`_`x`_\) | `asind(`_`x`_\) | inverse sine |
| `atan(`_`x`_\) | `atand(`_`x`_\) | inverse tangent |
| `atan2(`_`y`_, _`x`_\) | `atan2d(`_`y`_, _`x`_\) | inverse tangent of _`y`_/_`x`_ |
| `cos(`_`x`_\) | `cosd(`_`x`_\) | cosine |
| `cot(`_`x`_\) | `cotd(`_`x`_\) | cotangent |
| `sin(`_`x`_\) | `sind(`_`x`_\) | sine |
| `tan(`_`x`_\) | `tand(`_`x`_\) | tangent |

## Note

Another way to work with angles measured in degrees is to use the unit transformation functions `radians()` and `degrees()` shown earlier. However, using the degree-based trigonometric functions is preferred, as that way avoids round-off error for special cases such as `sind(30)`.

[Table 9.8](https://www.postgresql.org/docs/12/functions-math.html#FUNCTIONS-MATH-HYP-TABLE) shows the available hyperbolic functions. All these functions take arguments and return values of type `double precision`.

## **Table 9.8. Hyperbolic Functions**

| Function | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `sinh(`_`x`_\) | hyperbolic sine | `sinh(0)` | `0` |
| `cosh(`_`x`_\) | hyperbolic cosine | `cosh(0)` | `1` |
| `tanh(`_`x`_\) | hyperbolic tangent | `tanh(0)` | `0` |
| `asinh(`_`x`_\) | inverse hyperbolic sine | `asinh(0)` | `0` |
| `acosh(`_`x`_\) | inverse hyperbolic cosine | `acosh(1)` | `0` |
| `atanh(`_`x`_\) | inverse hyperbolic tangent | `atanh(0)` | `0` |

