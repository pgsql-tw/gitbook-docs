<a id="PLPERL-UNDER-THE-HOOD"></a>
## 43.8. PL/Perl 內部運作原理 [#](#PLPERL-UNDER-THE-HOOD)

[43.8.1. 組態設定](plperl-under-the-hood.md#PLPERL-CONFIG)

[43.8.2. 限制與缺少的功能](plperl-under-the-hood.md#PLPERL-MISSING)

<a id="PLPERL-CONFIG"></a>

### 43.8.1. 組態設定 [#](#PLPERL-CONFIG)

本節列出會影響 PL/Perl 的組態參數。

<a id="GUC-PLPERL-ON-INIT"></a>

`plperl.on_init`（`string`）<a id="id-1.8.10.16.2.3.1.1.3"></a> [#](#GUC-PLPERL-ON-INIT)
:   指定當 Perl 直譯器首次初始化時要執行的 Perl 程式碼，此時該直譯器尚未特化供 `plperl` 或
    `plperlu` 使用。
    執行此程式碼時，SPI 函式並不可用。
    若此程式碼執行失敗並發生錯誤，將會中止直譯器的初始化，並向外傳播至呼叫端查詢，導致目前的交易或子交易中止。

    Perl 程式碼僅限於單一字串。較長的程式碼可放入模組，再由 `on_init`
    字串載入。範例：

    ```

    plperl.on_init = 'require "plperlinit.pl"'
    plperl.on_init = 'use lib "/my/app"; use MyApp::PgInit;'
    ```

    無論是直接或間接由 `plperl.on_init` 載入的任何模組，都可供 `plperl`
    使用，這可能會造成安全風險。若要查看已載入哪些模組，可使用：

    ```

    DO 'elog(WARNING, join ", ", sort keys %INC)' LANGUAGE plperl;
    ```

    若 `plperl` 程式庫已包含在 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 中，初始化將會在 postmaster
    中進行，此時應特別考量此舉可能使 postmaster 不穩定的風險。使用此功能的主要理由，是由 `plperl.on_init`
    載入的 Perl 模組只需在 postmaster 啟動時載入一次，之後在各個資料庫工作階段中即可立即使用，無需再承擔載入的額外負擔。不過請留意，這項額外負擔的節省，僅適用於資料庫工作階段中第一個使用到的 Perl 直譯器——即 PL/PerlU，或是第一個呼叫 PL/Perl 函式的 SQL 角色所使用的 PL/Perl。在同一資料庫工作階段中，若建立了任何額外的 Perl 直譯器，都必須重新執行一次
    `plperl.on_init`。此外，在 Windows 上，預先載入完全無法帶來任何節省，因為 postmaster 程序中建立的 Perl 直譯器並不會傳遞給子程序。

    此參數只能在 `postgresql.conf` 檔案中或伺服器命令列上設定。
<a id="GUC-PLPERL-ON-PLPERL-INIT"></a>

`plperl.on_plperl_init`（`string`）<a id="id-1.8.10.16.2.3.2.1.3"></a> <br> `plperl.on_plperlu_init`（`string`）<a id="id-1.8.10.16.2.3.2.2.3"></a> [#](#GUC-PLPERL-ON-PLPERL-INIT)
:   這些參數分別指定當 Perl 直譯器特化為 `plperl` 或
    `plperlu` 時要執行的 Perl 程式碼。這會發生在資料庫工作階段中首次執行 PL/Perl 或
    PL/PerlU 函式時，或是因呼叫了另一種語言、或某個新的 SQL 角色呼叫了 PL/Perl 函式，而必須建立額外直譯器時。這會在
    `plperl.on_init` 完成的任何初始化之後執行。
    執行此程式碼時，SPI 函式並不可用。
    `plperl.on_plperl_init` 中的 Perl 程式碼是在直譯器「鎖定」之後執行，因此只能執行受信任的操作。

    若此程式碼執行失敗並發生錯誤，將會中止初始化，並向外傳播至呼叫端查詢，導致目前的交易或子交易中止。任何已在 Perl 中完成的動作都不會被復原；不過該直譯器將不會再被使用。若再次使用該語言，將會在一個全新的 Perl 直譯器中重新嘗試初始化。

    只有超級使用者可以變更這些設定。雖然這些設定可以在工作階段中變更，但這類變更並不會影響已經用來執行函式的 Perl 直譯器。
<a id="GUC-PLPERL-USE-STRICT"></a>

`plperl.use_strict`（`boolean`）<a id="id-1.8.10.16.2.3.3.1.3"></a> [#](#GUC-PLPERL-USE-STRICT)
:   設為 true 時，後續編譯的 PL/Perl 函式將會啟用 `strict` 編譯指示（pragma）。此參數不會影響目前工作階段中已經編譯完成的函式。

<a id="PLPERL-MISSING"></a>

### 43.8.2. 限制與缺少的功能 [#](#PLPERL-MISSING)

以下功能目前在 PL/Perl 中仍付之闕如，歡迎大家貢獻心力予以補上。

* PL/Perl 函式之間無法直接互相呼叫。
* SPI 尚未完全實作。
* 若您使用 `spi_exec_query` 擷取非常龐大的資料集，請留意這些資料將全部載入記憶體中。您可以改用先前示範過的
  `spi_query`／`spi_fetchrow` 來避免這個問題。

  傳回集合函式若透過 `return` 將大量資料列傳回 PostgreSQL，也會發生類似的問題。您同樣可以改用先前示範過的方式，為每一筆傳回的資料列改用
  `return_next`，藉此避免這個問題。
* 當工作階段正常結束（而非因致命錯誤而結束）時，任何已定義的
  `END` 區塊都會被執行。目前不會執行其他任何動作。具體來說，檔案控制代碼不會自動排清（flush），物件也不會自動銷毀。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-under-the-hood.html)（原文版本：18.6；核對日期：2026-09-22）
