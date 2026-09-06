## 34.16. Oracle Compatibility Mode [#](#ECPG-ORACLE-COMPAT)

`ecpg` can be run in a so-called *Oracle
compatibility mode*. If this mode is active, it tries to
behave as if it were Oracle Pro\*C.

Specifically, this mode changes `ecpg` in three ways:

* Pad character arrays receiving character string types with
  trailing spaces to the specified length
* Zero byte terminate these character arrays, and set the indicator
  variable if truncation occurs
* Set the null indicator to `-1` when character
  arrays receive empty character string types

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-oracle-compat.html)（英文原文，待翻譯）
