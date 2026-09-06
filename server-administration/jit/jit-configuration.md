## 30.3. 設定 [#](#JIT-CONFIGURATION)

設定變數 [jit](../runtime-config/runtime-config-query.md#GUC-JIT) 決定是否啟用 JIT 編譯。啟用後，設定變數 [jit_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-ABOVE-COST)、[jit_inline_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-INLINE-ABOVE-COST) 與 [jit_optimize_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-OPTIMIZE-ABOVE-COST)，會決定是否對查詢進行 JIT 編譯，以及投入多少編譯工作。

[jit_provider](../runtime-config/runtime-config-client.md#GUC-JIT-PROVIDER) 決定使用哪個 JIT 實作，通常不需要變更。請參閱[第 30.4.2 節](jit-extensibility.md#JIT-PLUGGABLE)。

另有一些供開發與除錯使用的設定參數，詳見[第 19.17 節](../runtime-config/runtime-config-developer.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/jit-configuration.html)（原文版本：18.6；核對日期：2026-09-07）
