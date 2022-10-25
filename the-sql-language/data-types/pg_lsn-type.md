# 8.20. pg\_lsn 型別

pg\_lsn 資料型別用於儲存 LSN（日誌序列編號）資料，該資料是指向 WAL 中某個位置的指標。此型別用於表示 XLogRecPtr，並且是 PostgreSQL 的內部系統型別。

Internally, an LSN is a 64-bit integer, representing a byte position in the write-ahead log stream. It is printed as two hexadecimal numbers of up to 8 digits each, separated by a slash; for example, `16/B374D848`. The `pg_lsn` type supports the standard comparison operators, like `=` and `>`. Two LSNs can be subtracted using the `-` operator; the result is the number of bytes separating those write-ahead log locations.
