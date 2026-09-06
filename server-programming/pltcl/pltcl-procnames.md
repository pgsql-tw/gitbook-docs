## 42.12. Tcl 程序名稱 [#](#PLTCL-PROCNAMES)

在 PostgreSQL 中，若函式位於不同的 schema，或引數數量或型別不同，就可以用相同函式名稱定義不同的函式。然而，Tcl 要求所有程序名稱都必須不同。PL/Tcl 的處理方式是將引數型別名稱納入內部 Tcl 程序名稱，並在必要時於名稱後附加函式的物件識別碼（OID），使其與同一 Tcl 直譯器中先前已載入的所有函式名稱有所區別。因此，名稱相同但引數型別不同的 PostgreSQL 函式，也會對應到不同的 Tcl 程序。PL/Tcl 程式設計者通常不必在意這點，但除錯時可能會看到這些名稱。

基於此原因及其他因素，PL/Tcl 函式不能直接呼叫另一個 PL/Tcl 函式（也就是在 Tcl 內呼叫）。若有此需求，必須使用 `spi_exec` 或相關命令，透過 SQL 呼叫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-procnames.html)（原文版本：18.6；核對日期：2026-09-07）
