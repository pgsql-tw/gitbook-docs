## 第 37 章 觸發器

**目錄**

[37.1. 觸發器行為概述](trigger-definition.md)

[37.2. 資料變更的可見性](trigger-datachanges.md)

[37.3. 以 C 撰寫觸發器函式](trigger-interface.md)

[37.4. 完整的觸發器範例](trigger-example.md)

<a id="id-1.8.4.2"></a>

本章提供撰寫觸發器函式的一般資訊。觸發器函式可用多數可用的程序語言撰寫，包括 PL/pgSQL（[第 41 章](../plpgsql/README.md)）、PL/Tcl（[第 42 章](../pltcl/README.md)）、PL/Perl（[第 43 章](../plperl/README.md)）及 PL/Python（[第 44 章](../plpython/README.md)）。讀完本章後，應參閱所選程序語言的章節，瞭解用該語言撰寫觸發器的特定細節。

也可以使用 C 撰寫觸發器函式，不過多數人覺得使用程序語言比較容易。目前無法使用一般 SQL 函式語言撰寫觸發器函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/triggers.html)（原文版本：18.6；核對日期：2026-09-07）
