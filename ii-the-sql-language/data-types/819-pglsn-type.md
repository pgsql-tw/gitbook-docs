# 8.19. pg\_lsn型別[^1]

The`pg_lsn`data type can be used to store LSN \(Log Sequence Number\) data which is a pointer to a location in the WAL. This type is a representation of`XLogRecPtr`and an internal system type ofPostgreSQL.

Internally, an LSN is a 64-bit integer, representing a byte position in the write-ahead log stream. It is printed as two hexadecimal numbers of up to 8 digits each, separated by a slash; for example,`16/B374D848`. The`pg_lsn`type supports the standard comparison operators, like`=`and`>`. Two LSNs can be subtracted using the`-`operator; the result is the number of bytes separating those write-ahead log locations.

---



[^1]:  [PostgreSQL: Documentation: 10: 8.19. pg\_lsn Type](https://www.postgresql.org/docs/10/static/datatype-pg-lsn.html)

