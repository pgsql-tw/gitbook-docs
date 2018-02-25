# 19.15. 預先配置的參數[^1]

The following“parameters”are read-only, and are determined whenPostgreSQLis compiled or when it is installed. As such, they have been excluded from the sample`postgresql.conf`file. These options report various aspects ofPostgreSQLbehavior that might be of interest to certain applications, particularly administrative front-ends.

`block_size`

\(

`integer`

\)



Reports the size of a disk block. It is determined by the value of`BLCKSZ`when building the server. The default value is 8192 bytes. The meaning of some configuration variables \(such as[shared\_buffers](https://www.postgresql.org/docs/10/static/runtime-config-resource.html#GUC-SHARED-BUFFERS)\) is influenced by`block_size`. See[Section 19.4](https://www.postgresql.org/docs/10/static/runtime-config-resource.html)for information.

`data_checksums`

\(

`boolean`

\)



Reports whether data checksums are enabled for this cluster. See[data checksums](https://www.postgresql.org/docs/10/static/app-initdb.html#APP-INITDB-DATA-CHECKSUMS)for more information.

`debug_assertions`

\(

`boolean`

\)



Reports whetherPostgreSQLhas been built with assertions enabled. That is the case if the macro`USE_ASSERT_CHECKING`is defined whenPostgreSQLis built \(accomplished e.g. by the`configure`option`--enable-cassert`\). By defaultPostgreSQLis built without assertions.

`integer_datetimes`

\(

`boolean`

\)



Reports whetherPostgreSQLwas built with support for 64-bit-integer dates and times. As ofPostgreSQL10, this is always`on`.

`lc_collate`

\(

`string`

\)



Reports the locale in which sorting of textual data is done. See[Section 23.1](https://www.postgresql.org/docs/10/static/locale.html)for more information. This value is determined when a database is created.

`lc_ctype`

\(

`string`

\)



Reports the locale that determines character classifications. See[Section 23.1](https://www.postgresql.org/docs/10/static/locale.html)for more information. This value is determined when a database is created. Ordinarily this will be the same as`lc_collate`, but for special applications it might be set differently.

`max_function_args`

\(

`integer`

\)



Reports the maximum number of function arguments. It is determined by the value of`FUNC_MAX_ARGS`when building the server. The default value is 100 arguments.

`max_identifier_length`

\(

`integer`

\)



Reports the maximum identifier length. It is determined as one less than the value of`NAMEDATALEN`when building the server. The default value of`NAMEDATALEN`is 64; therefore the default`max_identifier_length`is 63 bytes, which can be less than 63 characters when using multibyte encodings.

`max_index_keys`

\(

`integer`

\)



Reports the maximum number of index keys. It is determined by the value of`INDEX_MAX_KEYS`when building the server. The default value is 32 keys.

`segment_size`

\(

`integer`

\)



Reports the number of blocks \(pages\) that can be stored within a file segment. It is determined by the value of`RELSEG_SIZE`when building the server. The maximum size of a segment file in bytes is equal to`segment_size`multiplied by`block_size`; by default this is 1GB.

`server_encoding`

\(

`string`

\)





Reports the database encoding \(character set\). It is determined when the database is created. Ordinarily, clients need only be concerned with the value of[client\_encoding](https://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-CLIENT-ENCODING).

`server_version`

\(

`string`

\)



Reports the version number of the server. It is determined by the value of`PG_VERSION`when building the server.

`server_version_num`

\(

`integer`

\)



Reports the version number of the server as an integer. It is determined by the value of`PG_VERSION_NUM`when building the server.

`wal_block_size`

\(

`integer`

\)



Reports the size of a WAL disk block. It is determined by the value of`XLOG_BLCKSZ`when building the server. The default value is 8192 bytes.

`wal_segment_size`

\(

`integer`

\)



Reports the number of blocks \(pages\) in a WAL segment file. The total size of a WAL segment file in bytes is equal to`wal_segment_size`multiplied by`wal_block_size`; by default this is 16MB. See[Section 30.4](https://www.postgresql.org/docs/10/static/wal-configuration.html)for more information.

---



[^1]:  [PostgreSQL: Documentation: 10: 19.15. Preset Options](https://www.postgresql.org/docs/10/static/runtime-config-preset.html)

