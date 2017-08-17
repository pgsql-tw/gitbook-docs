# 8.2. 貨幣型別[^1]

The`money`type stores a currency amount with a fixed fractional precision; see[Table 8.3](https://www.postgresql.org/docs/10/static/datatype-money.html#datatype-money-table). The fractional precision is determined by the database's[lc\_monetary](https://www.postgresql.org/docs/10/static/runtime-config-client.html#guc-lc-monetary)setting. The range shown in the table assumes there are two fractional digits. Input is accepted in a variety of formats, including integer and floating-point literals, as well as typical currency formatting, such as`'$1,000.00'`. Output is generally in the latter form but depends on the locale.

**Table 8.3. Monetary Types**

| Name | Storage Size | Description | Range |
| :--- | :--- | :--- | :--- |
| `money` | 8 bytes | currency amount | -92233720368547758.08 to +92233720368547758.07 |

  


Since the output of this data type is locale-sensitive, it might not work to load`money`data into a database that has a different setting of`lc_monetary`. To avoid problems, before restoring a dump into a new database make sure`lc_monetary`has the same or equivalent value as in the database that was dumped.

Values of the`numeric`,`int`, and`bigint`data types can be cast to`money`. Conversion from the`real`and`double precision`data types can be done by casting to`numeric`first, for example:

```
SELECT '12.34'::float8::numeric::money;

```

However, this is not recommended. Floating point numbers should not be used to handle money due to the potential for rounding errors.

A`money`value can be cast to`numeric`without loss of precision. Conversion to other types could potentially lose precision, and must also be done in two stages:

```
SELECT '52093.89'::money::numeric::float8;

```

When a`money`value is divided by another`money`value, the result is`double precision`\(i.e., a pure number, not money\); the currency units cancel each other out in the division.

---



[^1]: [PostgreSQL: Documentation: 10: 8.2. Monetary Types](https://www.postgresql.org/docs/10/static/datatype-money.html)

