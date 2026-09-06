## 47.7. Logical Decoding Output Writers [#](#LOGICALDECODING-WRITER)

It is possible to add more output methods for logical decoding.
For details, see
`src/backend/replication/logical/logicalfuncs.c`.
Essentially, three functions need to be provided: one to read WAL, one to
prepare writing output, and one to write the output
(see [Section 47.6.5](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-writer.html)（英文原文，待翻譯）
