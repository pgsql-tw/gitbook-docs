## 30.3. Configuration [#](#JIT-CONFIGURATION)

The configuration variable
[jit](../runtime-config/runtime-config-query.md#GUC-JIT) determines whether JIT
compilation is enabled or disabled.
If it is enabled, the configuration variables
[jit_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-ABOVE-COST), [jit_inline_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-INLINE-ABOVE-COST), and [jit_optimize_above_cost](../runtime-config/runtime-config-query.md#GUC-JIT-OPTIMIZE-ABOVE-COST) determine
whether JIT compilation is performed for a query,
and how much effort is spent doing so.

[jit_provider](../runtime-config/runtime-config-client.md#GUC-JIT-PROVIDER) determines which JIT
implementation is used. It is rarely required to be changed. See [Section 30.4.2](jit-extensibility.md#JIT-PLUGGABLE).

For development and debugging purposes a few additional configuration
parameters exist, as described in
[Section 19.17](../runtime-config/runtime-config-developer.md).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/jit-configuration.html)（英文原文，待翻譯）
