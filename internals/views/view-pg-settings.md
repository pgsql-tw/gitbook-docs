<a id="VIEW-PG-SETTINGS"></a>

## 53.25. `pg_settings` [#](#VIEW-PG-SETTINGS)

<a id="id-1.10.5.29.2"></a>

檢視表 `pg_settings` 可用來存取伺服器的執行期參數。它本質上是 [`SHOW`](../../reference/sql-commands/sql-show.md) 與 [`SET`](../../reference/sql-commands/sql-set.md) 命令的另一種介面。它也可用來存取每個參數無法直接從 [`SHOW`](../../reference/sql-commands/sql-show.md) 取得的一些資訊，例如最小值與最大值。

<a id="id-1.10.5.29.4"></a>

**表 53.25. `pg_settings` 欄位**

<table border="1" class="table" summary="表 53.25. pg_settings 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       執行期設定參數名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">setting</code> <code class="type">text</code>
</p>
<p>
       參數的目前值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">unit</code> <code class="type">text</code>
</p>
<p>
       參數的隱含單位
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">category</code> <code class="type">text</code>
</p>
<p>
       參數的邏輯分組
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">short_desc</code> <code class="type">text</code>
</p>
<p>
       參數的簡短說明
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">extra_desc</code> <code class="type">text</code>
</p>
<p>
       參數的額外、更詳細的說明
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">context</code> <code class="type">text</code>
</p>
<p>
       設定此參數值所需的情境（請參閱下文）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">vartype</code> <code class="type">text</code>
</p>
<p>
       參數類型（<code class="literal">bool</code>、<code class="literal">enum</code>、<code class="literal">integer</code>、<code class="literal">real</code> 或 <code class="literal">string</code>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">source</code> <code class="type">text</code>
</p>
<p>
       目前參數值的來源
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">min_val</code> <code class="type">text</code>
</p>
<p>
       參數允許的最小值（非數值的值則為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">max_val</code> <code class="type">text</code>
</p>
<p>
       參數允許的最大值（非數值的值則為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">enumvals</code> <code class="type">text[]</code>
</p>
<p>
       列舉（enum）參數允許的值（非列舉的值則為 null）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">boot_val</code> <code class="type">text</code>
</p>
<p>
       若參數未以其他方式設定，伺服器啟動時所採用的參數值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reset_val</code> <code class="type">text</code>
</p>
<p>
       在目前工作階段中，<a class="link" href="../../reference/sql-commands/sql-reset.md"><code class="command">RESET</code></a> 會將參數重設成的值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sourcefile</code> <code class="type">text</code>
</p>
<p>
       設定目前值的設定檔（若值是從設定檔以外的來源設定，或檢視者既不是超級使用者，也不具有 <code class="literal">pg_read_all_settings</code> 的權限，則為 null）；在設定檔中使用 <code class="literal">include</code> 指令時很有用
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">sourceline</code> <code class="type">int4</code>
</p>
<p>
       目前值在設定檔中被設定的行號（若值是從設定檔以外的來源設定，或檢視者既不是超級使用者，也不具有 <code class="literal">pg_read_all_settings</code> 的權限，則為 null）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pending_restart</code> <code class="type">bool</code>
</p>
<p>
若該值已在設定檔中變更但需要重新啟動，則為 <code class="literal">true</code>；否則為 <code class="literal">false</code>。
      </p></td></tr></tbody></table>

<br>

`context` 有數種可能的值。依變更設定的難度由高到低排列如下：

`internal`
:   這些設定無法直接變更；它們反映的是內部決定的值。其中有些可能可以透過以不同的組態選項重新建置伺服器，或變更提供給 initdb 的選項來調整。

`postmaster`
:   這些設定只能在伺服器啟動時套用，因此任何變更都需要重新啟動伺服器。這些設定的值通常儲存在 `postgresql.conf` 檔案中，或在啟動伺服器時於命令列傳入。當然，任何較低 `context` 類型的設定也都可以在伺服器啟動時設定。

`sighup`
:   這些設定可以在 `postgresql.conf` 中變更，而不需要重新啟動伺服器。對 postmaster 發送 SIGHUP 訊號，使其重新讀取 `postgresql.conf` 並套用變更。postmaster 也會將 SIGHUP 訊號轉送給它的子程序，讓它們全都取得新的值。

`superuser-backend`
:   這些設定可以在 `postgresql.conf` 中變更，而不需要重新啟動伺服器。它們也可以在連線請求封包中針對特定工作階段設定（例如透過 libpq 的 `PGOPTIONS` 環境變數），但前提是連線的使用者是超級使用者，或已被授予適當的 `SET` 權限。不過，這些設定在工作階段啟動之後，就不會再於該工作階段中改變。若你在 `postgresql.conf` 中變更它們，請對 postmaster 發送 SIGHUP 訊號，使其重新讀取 `postgresql.conf`。新的值只會影響之後啟動的工作階段。

`backend`
:   這些設定可以在 `postgresql.conf` 中變更，而不需要重新啟動伺服器。它們也可以在連線請求封包中針對特定工作階段設定（例如透過 libpq 的 `PGOPTIONS` 環境變數）；任何使用者都可以為自己的工作階段進行這種變更。不過，這些設定在工作階段啟動之後，就不會再於該工作階段中改變。若你在 `postgresql.conf` 中變更它們，請對 postmaster 發送 SIGHUP 訊號，使其重新讀取 `postgresql.conf`。新的值只會影響之後啟動的工作階段。

`superuser`
:   這些設定可以從 `postgresql.conf` 設定，或在工作階段中透過 `SET` 命令設定；但只有超級使用者以及具有適當 `SET` 權限的使用者，才能透過 `SET` 變更它們。只有在尚未以 `SET` 建立工作階段區域值的情況下，`postgresql.conf` 中的變更才會影響既有的工作階段。

`user`
:   這些設定可以從 `postgresql.conf` 設定，或在工作階段中透過 `SET` 命令設定。任何使用者都可以變更自己的工作階段區域值。只有在尚未以 `SET` 建立工作階段區域值的情況下，`postgresql.conf` 中的變更才會影響既有的工作階段。

關於變更這些參數之各種方式的更多資訊，請參閱[第 19.1 節](../../server-administration/runtime-config/config-setting.md)。

此檢視表無法進行插入或刪除，但可以更新。對 `pg_settings` 的某個資料列套用 `UPDATE`，等同於對該名稱的參數執行 `SET` 命令。此變更只會影響目前工作階段所使用的值。若 `UPDATE` 是在之後被中止的交易中發出，則當該交易回復時，`UPDATE` 命令的效果就會消失。一旦外圍的交易提交，其效果將持續到工作階段結束，除非被另一個 `UPDATE` 或 `SET` 覆寫。

此檢視表不會顯示[自訂選項](../../server-administration/runtime-config/runtime-config-custom.md)，除非定義這些選項的擴充模組已被執行該查詢的後端程序載入（例如透過在 [shared_preload_libraries](../../server-administration/runtime-config/runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) 中列出、呼叫該擴充模組中的 C 函式，或使用 [`LOAD`](../../reference/sql-commands/sql-load.md) 命令）。例如，由於[封存模組](../../server-programming/archive-modules/README.md)通常只由封存程序（archiver）載入，而非由一般工作階段載入，因此除非採取特殊措施將它們載入執行該查詢的後端程序，否則此檢視表不會顯示這類模組所定義的任何自訂選項。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-settings.html)（原文版本：18.6；核對日期：2026-10-09）
