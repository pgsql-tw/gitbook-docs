## 第 30 章 即時編譯（JIT）

**目錄**

- [30.1. 什麼是 JIT 編譯？](jit-reason.md)
  - [30.1.1. JIT 加速的操作](jit-reason.md#jit-accelerated-operations)

  - [30.1.2. 內嵌](jit-reason.md#jit-inlining)

  - [30.1.3. 最佳化](jit-reason.md#jit-optimization)

- [30.2. 何時使用 JIT？](jit-decision.md)

- [30.3. 設定](jit-configuration.md)

- [30.4. 擴充能力](jit-extensibility.md)
  - [30.4.1. 擴充套件的內嵌支援](jit-extensibility.md#jit-extensibility-bitcode)

  - [30.4.2. 可插拔的 JIT 提供者](jit-extensibility.md#jit-pluggable)

<a id="id-1.6.17.2"></a><a id="id-1.6.17.3"></a>

本章說明什麼是即時編譯，以及如何在 PostgreSQL 中設定它。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/jit.html)（原文版本：18.6；核對日期：2026-09-07）
