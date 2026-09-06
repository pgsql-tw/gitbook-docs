## 44.3. Sharing Data [#](#PLPYTHON-SHARING)

The global dictionary `SD` is available to store
private data between repeated calls to the same function.
The global dictionary `GD` is public data,
that is available to all Python functions within a session; use with
care.<a id="id-1.8.11.11.2.3"></a>

Each function gets its own execution environment in the
Python interpreter, so that global data and function arguments from
`myfunc` are not available to
`myfunc2`. The exception is the data in the
`GD` dictionary, as mentioned above.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-sharing.html)（英文原文，待翻譯）
