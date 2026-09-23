## 第 47 章 邏輯解碼

**目錄**

[47.1. 邏輯解碼範例](logicaldecoding-example.md)

[47.2. 邏輯解碼的概念](logicaldecoding-explanation.md)
:   [47.2.1. 邏輯解碼](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-LOG-DEC)

    [47.2.2. 複寫插槽](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS)

    [47.2.3. 複寫插槽同步](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)

    [47.2.4. 輸出外掛程式](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)

    [47.2.5. 匯出的快照](logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

[47.3. 串流複寫協定介面](logicaldecoding-walsender.md)

[47.4. 邏輯解碼 SQL 介面](logicaldecoding-sql.md)

[47.5. 與邏輯解碼相關的系統目錄](logicaldecoding-catalogs.md)

[47.6. 邏輯解碼輸出外掛程式](logicaldecoding-output-plugin.md)
:   [47.6.1. 初始化函式](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-INIT)

    [47.6.2. 功能](logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES)

    [47.6.3. 輸出模式](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-MODE)

    [47.6.4. 輸出外掛程式回呼函式](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS)

    [47.6.5. 用於產生輸出的函式](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)

[47.7. 邏輯解碼輸出寫入器](logicaldecoding-writer.md)

[47.8. 邏輯解碼的同步複寫支援](logicaldecoding-synchronous.md)
:   [47.8.1. 概觀](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)

    [47.8.2. 注意事項](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

[47.9. 邏輯解碼的大型交易串流](logicaldecoding-streaming.md)

[47.10. 邏輯解碼的兩階段提交支援](logicaldecoding-two-phase-commits.md)

<a id="id-1.8.14.2"></a>

PostgreSQL 提供了一套基礎架構，可以把透過 SQL 所做的修改，以串流方式傳送給外部消費端。這項功能可用於各種用途，包括複寫解決方案與稽核。

變更會在由邏輯複寫插槽識別的串流中送出。

這些變更以何種格式串流傳送，是由所使用的輸出外掛程式決定的。PostgreSQL 發行版中提供了一個範例外掛程式。也可以在不修改任何核心程式碼的情況下，撰寫額外的外掛程式，以擴充可用的格式選項。每個輸出外掛程式，都能存取由 `INSERT` 所產生的每一筆新資料列，以及由 `UPDATE` 所建立的新版本資料列。至於 `UPDATE` 與 `DELETE` 的舊版本資料列是否可用，則取決於所設定的複本識別（見 [`REPLICA IDENTITY`](../../reference/sql-commands/sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)）。

變更可以透過串流複寫協定來消費（見[第 54.4 節](../../internals/protocol/protocol-replication.md)與[第 47.3 節](logicaldecoding-walsender.md)），也可以透過呼叫 SQL 函式來消費（見[第 47.4 節](logicaldecoding-sql.md)）。你也可以在不修改核心程式碼的情況下，撰寫額外的方法來消費複寫插槽的輸出（見[第 47.7 節](logicaldecoding-writer.md)）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding.html)（原文版本：18.6；核對日期：2026-09-22）
