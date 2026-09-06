<a id="ECPG-ORACLE-COMPAT"></a>

# 36.16. Oracle Compatibility Mode

`ecpg` can be run in a so-called <em class="firstterm">Oracle compatibility mode</em>. If this mode is active, it tries to behave as if it were Oracle Pro&#42;C.

Specifically, this mode changes `ecpg` in three ways:

* Pad character arrays receiving character string types with trailing spaces to the specified length
* Zero byte terminate these character arrays, and set the indicator variable if truncation occurs
* Set the null indicator to `-1` when character arrays receive empty character string types

---

原文：[PostgreSQL 15.19 Documentation](ecpg-oracle-compat.md)（英文原文，待翻譯）
