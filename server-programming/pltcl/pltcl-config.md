<a id="PLTCL-CONFIG"></a>

## 42.11. PL/Tcl 組態設定 [#](#PLTCL-CONFIG)

本節列出會影響 PL/Tcl 的組態參數。

<a id="GUC-PLTCL-START-PROC"></a>

`pltcl.start_proc` (`string`) <a id="id-1.8.9.15.3.1.1.3"></a> [#](#GUC-PLTCL-START-PROC)
:   這個參數若被設為非空字串，會指定一個不帶參數的 PL/Tcl 函式名稱（可以加上綱要限定），每當為 PL/Tcl 建立新的 Tcl 直譯器時就會執行該函式。這樣的函式可以執行每個工作階段的初始化工作，例如載入額外的 Tcl 程式碼。當 PL/Tcl 函式在某個資料庫工作階段中第一次被執行時，或是因為 PL/Tcl 函式被新的 SQL 角色呼叫而必須建立額外的直譯器時，就會建立新的 Tcl 直譯器。

    被參照的函式必須以 `pltcl` 語言撰寫，而且不能被標記為 `SECURITY DEFINER`。（這些限制確保它會在它應該初始化的那個直譯器中執行。）目前的使用者也必須擁有呼叫它的權限。

    如果該函式以錯誤失敗，它會中止那個造成新直譯器被建立的函式呼叫，並向外傳播到呼叫端的查詢，造成目前的交易或子交易被中止。在 Tcl 中已經做過的動作不會被還原；不過，那個直譯器不會再被使用。如果該語言再次被使用，初始化會在一個全新的 Tcl 直譯器中再試一次。

    只有超級使用者可以變更這項設定。雖然這項設定可以在工作階段中變更，但這類變更不會影響已經建立好的 Tcl 直譯器。
<a id="GUC-PLTCLU-START-PROC"></a>

`pltclu.start_proc` (`string`) <a id="id-1.8.9.15.3.2.1.3"></a> [#](#GUC-PLTCLU-START-PROC)
:   這個參數與 `pltcl.start_proc` 完全相同，只是它適用於 PL/TclU。被參照的函式必須以 `pltclu` 語言撰寫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-config.html)（原文版本：18.6；核對日期：2026-09-13）
