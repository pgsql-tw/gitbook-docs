# 9.18. 陣列函式及運算子[^1]

[Table 9.48](https://www.postgresql.org/docs/10/static/functions-array.html#array-operators-table)shows the operators available for array types.

**Table 9.48. Array Operators**

| Operator | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `=` | equal | `ARRAY[1.1,2.1,3.1]::int[] = ARRAY[1,2,3]` | `t` |
| `<>` | not equal | `ARRAY[1,2,3] <> ARRAY[1,2,4]` | `t` |
| `<` | less than | `ARRAY[1,2,3] < ARRAY[1,2,4]` | `t` |
| `>` | greater than | `ARRAY[1,4,3] > ARRAY[1,2,4]` | `t` |
| `<=` | less than or equal | `ARRAY[1,2,3] <= ARRAY[1,2,3]` | `t` |
| `>=` | greater than or equal | `ARRAY[1,4,3] >= ARRAY[1,4,3]` | `t` |
| `@>` | contains | `ARRAY[1,4,3] @> ARRAY[3,1]` | `t` |
| `<@` | is contained by | `ARRAY[2,7] <@ ARRAY[1,7,4,2,6]` | `t` |
| `&&` | overlap \(have elements in common\) | `ARRAY[1,4,3] && ARRAY[2,1]` | `t` |
| `||` | array-to-array concatenation | `ARRAY[1,2,3] || ARRAY[4,5,6]` | `{1,2,3,4,5,6}` |
| `||` | array-to-array concatenation | `ARRAY[1,2,3] || ARRAY[[4,5,6],[7,8,9]]` | `{ {1,2,3},{4,5,6},{7,8,9} }` |
| `||` | element-to-array concatenation | `3 || ARRAY[4,5,6]` | `{3,4,5,6}` |
| `||` | array-to-element concatenation | `ARRAY[4,5,6] || 7` | `{4,5,6,7}` |

Array comparisons compare the array contents element-by-element, using the default B-tree comparison function for the element data type. In multidimensional arrays the elements are visited in row-major order \(last subscript varies most rapidly\). If the contents of two arrays are equal but the dimensionality is different, the first difference in the dimensionality information determines the sort order. \(This is a change from versions ofPostgreSQLprior to 8.2: older versions would claim that two arrays with the same contents were equal, even if the number of dimensions or subscript ranges were different.\)

See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html)for more details about array operator behavior. See[Section 11.2](https://www.postgresql.org/docs/10/static/indexes-types.html)for more details about which operators support indexed operations.

[Table 9.49](https://www.postgresql.org/docs/10/static/functions-array.html#array-functions-table)shows the functions available for use with array types. See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html)for more information and examples of the use of these functions.

**Table 9.49. Array Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `array_append`\(`anyarray`,`anyelement`\) | `anyarray` | append an element to the end of an array | `array_append(ARRAY[1,2], 3)` | `{1,2,3}` |
| `array_cat`\(`anyarray`,`anyarray`\) | `anyarray` | concatenate two arrays | `array_cat(ARRAY[1,2,3], ARRAY[4,5])` | `{1,2,3,4,5}` |
| `array_ndims`\(`anyarray`\) | `int` | returns the number of dimensions of the array | `array_ndims(ARRAY[[1,2,3], [4,5,6]])` | `2` |
| `array_dims`\(`anyarray`\) | `text` | returns a text representation of array's dimensions | `array_dims(ARRAY[[1,2,3], [4,5,6]])` | `[1:2][1:3]` |
| `array_fill`\(`anyelement`,`int[]`, \[,`int[]`\]\) | `anyarray` | returns an array initialized with supplied value and dimensions, optionally with lower bounds other than 1 | `array_fill(7, ARRAY[3], ARRAY[2])` | `[2:4]={7,7,7}` |
| `array_length`\(`anyarray`,`int`\) | `int` | returns the length of the requested array dimension | `array_length(array[1,2,3], 1)` | `3` |
| `array_lower`\(`anyarray`,`int`\) | `int` | returns lower bound of the requested array dimension | `array_lower('[0:2]={1,2,3}'::int[], 1)` | `0` |
| `array_position`\(`anyarray`,`anyelement`\[,`int`\]\) | `int` | returns the subscript of the first occurrence of the second argument in the array, starting at the element indicated by the third argument or at the first element \(array must be one-dimensional\) | `array_position(ARRAY['sun','mon','tue','wed','thu','fri','sat'], 'mon')` | `2` |
| `array_positions`\(`anyarray`,`anyelement`\) | `int[]` | returns an array of subscripts of all occurrences of the second argument in the array given as first argument \(array must be one-dimensional\) | `array_positions(ARRAY['A','A','B','A'], 'A')` | `{1,2,4}` |
| `array_prepend`\(`anyelement`,`anyarray`\) | `anyarray` | append an element to the beginning of an array | `array_prepend(1, ARRAY[2,3])` | `{1,2,3}` |
| `array_remove`\(`anyarray`,`anyelement`\) | `anyarray` | remove all elements equal to the given value from the array \(array must be one-dimensional\) | `array_remove(ARRAY[1,2,3,2], 2)` | `{1,3}` |
| `array_replace`\(`anyarray`,`anyelement`,`anyelement`\) | `anyarray` | replace each array element equal to the given value with a new value | `array_replace(ARRAY[1,2,5,4], 5, 3)` | `{1,2,3,4}` |
| `array_to_string`\(`anyarray`,`text`\[,`text`\]\) | `text` | concatenates array elements using supplied delimiter and optional null string | `array_to_string(ARRAY[1, 2, 3, NULL, 5], ',', '*')` | `1,2,3,*,5` |
| `array_upper`\(`anyarray`,`int`\) | `int` | returns upper bound of the requested array dimension | `array_upper(ARRAY[1,8,3,7], 1)` | `4` |
| `cardinality`\(`anyarray`\) | `int` | returns the total number of elements in the array, or 0 if the array is empty | `cardinality(ARRAY[[1,2],[3,4]])` | `4` |
| `string_to_array`\(`text`,`text`\[,`text`\]\) | `text[]` | splits string into array elements using supplied delimiter and optional null string | `string_to_array('xx~^~yy~^~zz', '~^~', 'yy')` | `{xx,NULL,zz}` |
| `unnest`\(`anyarray`\) | `setof anyelement` | expand an array to a set of rows | `unnest(ARRAY[1,2])` | 12\(2 rows\) |
| `unnest`\(`anyarray`,`anyarray`\[, ...\]\) | `setof anyelement, anyelement [, ...]` | expand multiple arrays \(possibly of different types\) to a set of rows. This is only allowed in the FROM clause; see[Section 7.2.1.4](https://www.postgresql.org/docs/10/static/queries-table-expressions.html#queries-tablefunctions) | `unnest(ARRAY[1,2],ARRAY['foo','bar','baz'])` | 1    foo2    barNULL baz\(3 rows\) |

In`array_position`and`array_positions`, each array element is compared to the searched value using`IS NOT DISTINCT FROM`semantics.

In`array_position`,`NULL`is returned if the value is not found.

In`array_positions`,`NULL`is returned only if the array is`NULL`; if the value is not found in the array, an empty array is returned instead.

In`string_to_array`, if the delimiter parameter is NULL, each character in the input string will become a separate element in the resulting array. If the delimiter is an empty string, then the entire input string is returned as a one-element array. Otherwise the input string is split at each occurrence of the delimiter string.

In`string_to_array`, if the null-string parameter is omitted or NULL, none of the substrings of the input will be replaced by NULL. In`array_to_string`, if the null-string parameter is omitted or NULL, any null elements in the array are simply skipped and not represented in the output string.

### Note

There are two differences in the behavior of`string_to_array`from pre-9.1 versions ofPostgreSQL. First, it will return an empty \(zero-element\) array rather than NULL when the input string is of zero length. Second, if the delimiter string is NULL, the function splits the input into individual characters, rather than returning NULL as before.

See also[Section 9.20](https://www.postgresql.org/docs/10/static/functions-aggregate.html)about the aggregate function`array_agg`for use with arrays.

---

[^1]:  [PostgreSQL: Documentation: 10: 9.18. Array Functions and Operators](https://www.postgresql.org/docs/10/static/functions-array.html)

