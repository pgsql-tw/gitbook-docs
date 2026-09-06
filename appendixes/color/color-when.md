## N.1. When Color is Used [#](#COLOR-WHEN)

To use colorized output, set the environment variable
`PG_COLOR`<a id="id-1.11.15.4.2.2"></a>
as follows:

1. If the value is `always`, then color is used.
2. If the value is `auto` and the standard error stream
   is associated with a terminal device, then color is used.
3. Otherwise, color is not used.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/color-when.html)（英文原文，待翻譯）
