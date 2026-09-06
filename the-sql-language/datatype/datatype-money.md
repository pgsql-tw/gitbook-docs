## 8.2. Monetary Types [#](#DATATYPE-MONEY)

The `money` type stores a currency amount with a fixed
fractional precision; see [Table 8.3](datatype-money.md#DATATYPE-MONEY-TABLE). The fractional precision is
determined by the database's [lc_monetary](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-MONETARY) setting.
The range shown in the table assumes there are two fractional digits.
Input is accepted in a variety of formats, including integer and
floating-point literals, as well as typical
currency formatting, such as `'$1,000.00'`.
Output is generally in the latter form but depends on the locale.

<a id="DATATYPE-MONEY-TABLE"></a>

**Table 8.3. Monetary Types**

<table border="1" class="table" summary="Monetary Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>Name</th><th>Storage Size</th><th>Description</th><th>Range</th></tr></thead><tbody><tr><td><code class="type">money</code></td><td>8 bytes</td><td>currency amount</td><td>-92233720368547758.08 to +92233720368547758.07</td></tr></tbody></table>

<br>

Since the output of this data type is locale-sensitive, it might not
work to load `money` data into a database that has a different
setting of `lc_monetary`. To avoid problems, before
restoring a dump into a new database make sure `lc_monetary` has
the same or equivalent value as in the database that was dumped.

Values of the `numeric`, `int`, and
`bigint` data types can be cast to `money`.
Conversion from the `real` and `double precision`
data types can be done by casting to `numeric` first, for
example:

```

SELECT '12.34'::float8::numeric::money;
```

However, this is not recommended. Floating point numbers should not be
used to handle money due to the potential for rounding errors.

A `money` value can be cast to `numeric` without
loss of precision. Conversion to other types could potentially lose
precision, and must also be done in two stages:

```

SELECT '52093.89'::money::numeric::float8;
```

Division of a `money` value by an integer value is performed
with truncation of the fractional part towards zero. To get a rounded
result, divide by a floating-point value, or cast the `money`
value to `numeric` before dividing and back to `money`
afterwards. (The latter is preferable to avoid risking precision loss.)
When a `money` value is divided by another `money`
value, the result is `double precision` (i.e., a pure number,
not money); the currency units cancel each other out in the division.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-money.html)（英文原文，待翻譯）
