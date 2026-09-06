# 8. 資料型別

PostgreSQL 內建一套豐富的資料型別供用戶使用。使用者也可以使用 [CREATE TYPE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/create-type.md) 指令讓 PostgreSQL 增加新的資料型別。

Table 8.1 列出所有內建的通用資料型別。大多數列在「Aliases」中的替代名稱是由於在 PostgreSQL 內部使用的歷史因素。此外，還有一些內部使用或不建議使用的資料型別，但這裡並沒有列出。

**Table 8.1. Data Types**

| Name                                       | Aliases               | Description                                        |
| ------------------------------------------ | --------------------- | -------------------------------------------------- |
| `bigint`                                   | `int8`                | signed eight-byte integer                          |
| `bigserial`                                | `serial8`             | autoincrementing eight-byte integer                |
| `bit [ (n`) ]                              |                       | fixed-length bit string                            |
| `bit varying [ (n`) ]                      | `varbit`              | variable-length bit string                         |
| `boolean`                                  | `bool`                | logical Boolean (true/false)                       |
| `box`                                      |                       | rectangular box on a plane                         |
| `bytea`                                    |                       | binary data (“byte array”)                         |
| `character [ (n`) ]                        | `char [ (n`) ]        | fixed-length character string                      |
| `character varying [ (n`) ]                | `varchar [ (n`) ]     | variable-length character string                   |
| `cidr`                                     |                       | IPv4 or IPv6 network address                       |
| `circle`                                   |                       | circle on a plane                                  |
| `date`                                     |                       | calendar date (year, month, day)                   |
| `double precision`                         | `float8`              | double precision floating-point number (8 bytes)   |
| `inet`                                     |                       | IPv4 or IPv6 host address                          |
| `integer`                                  | `int`,`int4`          | signed four-byte integer                           |
| `interval [fields`] \[ (`p`) ]             |                       | time span                                          |
| `json`                                     |                       | textual JSON data                                  |
| `jsonb`                                    |                       | binary JSON data, decomposed                       |
| `line`                                     |                       | infinite line on a plane                           |
| `lseg`                                     |                       | line segment on a plane                            |
| `macaddr`                                  |                       | MAC (Media Access Control) address                 |
| `macaddr8`                                 |                       | MAC (Media Access Control) address (EUI-64 format) |
| `money`                                    |                       | currency amount                                    |
| `numeric [ (p`,`s`) ]                      | `decimal [ (p`,`s`) ] | exact numeric of selectable precision              |
| `path`                                     |                       | geometric path on a plane                          |
| `pg_lsn`                                   |                       | PostgreSQLLog Sequence Number                      |
| `point`                                    |                       | geometric point on a plane                         |
| `polygon`                                  |                       | closed geometric path on a plane                   |
| `real`                                     | `float4`              | single precision floating-point number (4 bytes)   |
| `smallint`                                 | `int2`                | signed two-byte integer                            |
| `smallserial`                              | `serial2`             | autoincrementing two-byte integer                  |
| `serial`                                   | `serial4`             | autoincrementing four-byte integer                 |
| `text`                                     |                       | variable-length character string                   |
| `time [ (p`) ] \[ without time zone ]      |                       | time of day (no time zone)                         |
| `time [ (p`) ] with time zone              | `timetz`              | time of day, including time zone                   |
| `timestamp [ (p`) ] \[ without time zone ] |                       | date and time (no time zone)                       |
| `timestamp [ (p`) ] with time zone         | `timestamptz`         | date and time, including time zone                 |
| `tsquery`                                  |                       | text search query                                  |
| `tsvector`                                 |                       | text search document                               |
| `txid_snapshot`                            |                       | user-level transaction ID snapshot                 |
| `uuid`                                     |                       | universally unique identifier                      |
| `xml`                                      |                       | XML data                                           |

## 相容性

以下資料型別（或其拼寫方式）是由 SQL 指定的：`bigint`,`bit`,`bit varying`,`boolean`,`char`,`character varying`,`character`,`varchar`,`date`,`double precision`,`integer`,`interval`,`numeric`,`decimal`,`real`,`smallint`,`time`(with or without time zone),`timestamp`(with or without time zone),`xml`.

每種資料型別都具有其明確的輸入和輸出功能外部表示法。許多內建的資料型別都有明顯的外部格式。但是，有幾種資料型別是 PostgreSQL 獨有的，比如幾何路徑，或者有幾種可能的格式，像是日期和時間型別。某些輸入和輸出功能是不可逆的，意即，與原始輸入相比，輸出功能的結果可能會失去一些精確度。
