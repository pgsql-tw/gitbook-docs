# 48.7. Logical Decoding Output Writers

&#x20;It is possible to add more output methods for logical decoding. For details, see `src/backend/replication/logical/logicalfuncs.c`. Essentially, three functions need to be provided: one to read WAL, one to prepare writing output, and one to write the output (see [Section 48.6.5](https://www.postgresql.org/docs/13/logicaldecoding-output-plugin.html#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)).
