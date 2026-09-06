## 47.7. 邏輯解碼輸出寫入器 [#](#LOGICALDECODING-WRITER)

可為邏輯解碼新增更多輸出方法。詳細資訊請參閱 `src/backend/replication/logical/logicalfuncs.c`。基本上需要提供三個函式：一個讀取 WAL、一個準備寫入輸出，另一個則寫入輸出（請參閱[第 47.6.5 節](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-writer.html)（原文版本：18.6；核對日期：2026-09-06）
