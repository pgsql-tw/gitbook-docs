# 9.18. 陣列函式及運算子[^1]

[Table 9.48](https://www.postgresql.org/docs/10/static/functions-array.html#array-operators-table)shows the operators available for array types.

**Table 9.48. Array Operators**

Array comparisons compare the array contents element-by-element, using the default B-tree comparison function for the element data type. In multidimensional arrays the elements are visited in row-major order \(last subscript varies most rapidly\). If the contents of two arrays are equal but the dimensionality is different, the first difference in the dimensionality information determines the sort order. \(This is a change from versions ofPostgreSQLprior to 8.2: older versions would claim that two arrays with the same contents were equal, even if the number of dimensions or subscript ranges were different.\)

See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html)for more details about array operator behavior. See[Section 11.2](https://www.postgresql.org/docs/10/static/indexes-types.html)for more details about which operators support indexed operations.

[Table 9.49](https://www.postgresql.org/docs/10/static/functions-array.html#array-functions-table)shows the functions available for use with array types. See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html)for more information and examples of the use of these functions.

**Table 9.49. Array Functions**

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

