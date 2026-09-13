<a id="PLTCL-OVERVIEW"></a>

## 42.1. 概觀 [#](#PLTCL-OVERVIEW)

PL/Tcl 提供了函式撰寫者在 C 語言中所能擁有的大部分能力，只有少數限制，並且額外加上 Tcl 所提供的強大字串處理函式庫。

其中一個很有說服力的*好*限制是：所有東西都在 Tcl 直譯器的安全情境中執行。除了 safe Tcl 有限的指令集之外，只有少數幾個指令可以用來透過 SPI 存取資料庫，以及透過 `elog()` 發出訊息。PL/Tcl 沒有提供任何方式去存取資料庫伺服器的內部，也無法像 C 函式那樣，以 PostgreSQL 伺服器程序的權限取得作業系統層級的存取能力。因此，可以信任沒有特權的資料庫使用者使用這個語言；它並不會賦予他們無限的權限。

另一個值得注意的實作限制是：Tcl 函式不能用來為新的資料型別建立輸入／輸出函式。

有時候我們會希望撰寫不受 safe Tcl 限制的 Tcl 函式。例如，可能會想要一個能寄送電子郵件的 Tcl 函式。為了處理這類情況，PL/Tcl 有一個稱為 `PL/TclU`（代表不受信任的 Tcl）的變體。這個語言完全相同，只是改用完整的 Tcl 直譯器。*如果要使用 PL/TclU，它必須被安裝成不受信任的程序語言*，如此才只有資料庫超級使用者能夠用它建立函式。PL/TclU 函式的撰寫者必須注意，該函式不能被用來做出任何不樂見的事情，因為它能做到的事情，等同於以資料庫管理者身分登入的使用者所能做的一切。

如果在安裝程序的組態設定階段指定了 Tcl 支援，PL/Tcl 與 PL/TclU 呼叫處理常式的共享物件程式碼會自動建置並安裝到 PostgreSQL 的函式庫目錄中。若要在特定資料庫中安裝 PL/Tcl 及／或 PL/TclU，請使用 `CREATE EXTENSION` 指令，例如 `CREATE EXTENSION pltcl` 或 `CREATE EXTENSION pltclu`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pltcl-overview.html)（原文版本：18.6；核對日期：2026-09-13）
