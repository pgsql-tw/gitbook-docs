<a id="ECPG-PGTYPES-CONSTANTS"></a>

## 34.6.8. pgtypeslib 的特殊常數 [#](#ecpg-pgtypes-constants) <a href="#ecpg-pgtypes-constants" id="ecpg-pgtypes-constants"></a>

<a id="PGTYPESINVALIDTIMESTAMP"></a>

### `PGTYPESInvalidTimestamp` [#](#pgtypesinvalidtimestamp) <a href="#pgtypesinvalidtimestamp" id="pgtypesinvalidtimestamp"></a>

代表無效時間戳記的 timestamp 型別值。`PGTYPEStimestamp_from_asc` 函式發生剖析錯誤時會傳回此值。
    請注意，由於 `timestamp` 資料型別的內部表示方式，`PGTYPESInvalidTimestamp` 同時也是一個有效的 timestamp。它被設為 `1899-12-31 23:59:59`。為了偵測錯誤，請確保你的應用程式在每次呼叫 `PGTYPEStimestamp_from_asc` 之後，不只檢查 `PGTYPESInvalidTimestamp`，也檢查 `errno != 0`。

[返回 34.6. pgtypes 函式庫](ecpg-pgtypes.md#ecpg-pgtypes)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-pgtypes.html)（原文版本：18.6；核對日期：2026-10-18）
