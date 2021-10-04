# 51.85. pg\_settings

檢視表 pg\_settings 提供對伺服器的執行時參數的存取。它本質上是 [SHOW](../../reference/sql-commands/show.md) 和 [SET ](../../reference/sql-commands/set.md)指令的替代介面。它也提供 SHOW 無法直接獲得的一些資訊存取，例如最小值和最大值。

####  **Table 51.86. `pg_settings` Columns**

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Column Type</p>
        <p>Description</p>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><code>name</code>  <code>text</code>
        </p>
        <p>&#x57F7;&#x884C;&#x968E;&#x6BB5;&#x7684;&#x7D44;&#x614B;&#x53C3;&#x6578;&#x540D;&#x7A31;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>setting</code>  <code>text</code>
        </p>
        <p>&#x53C3;&#x6578;&#x7684;&#x73FE;&#x503C;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>unit</code>  <code>text</code>
        </p>
        <p>&#x53C3;&#x6578;&#x96B1;&#x542B;&#x7684;&#x55AE;&#x4F4D;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>category</code>  <code>text</code>
        </p>
        <p>&#x53C3;&#x6578;&#x7684;&#x908F;&#x8F2F;&#x5206;&#x985E;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>short_desc</code>  <code>text</code>
        </p>
        <p>&#x53C3;&#x6578;&#x7684;&#x7C21;&#x8981;&#x8AAA;&#x660E;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>extra_desc</code>  <code>text</code>
        </p>
        <p>&#x66F4;&#x9032;&#x4E00;&#x6B65;&#x7684;&#x8A73;&#x7D30;&#x53C3;&#x6578;&#x8AAA;&#x660E;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>context</code>  <code>text</code>
        </p>
        <p>&#x7D44;&#x614B;&#x53C3;&#x6578;&#x503C;&#x7684;&#x5FC5;&#x8981;&#x5167;&#x5BB9;&#xFF08;&#x8A73;&#x898B;&#x4E0B;&#x6587;&#xFF09;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>vartype</code>  <code>text</code>
        </p>
        <p>&#x53C3;&#x6578;&#x578B;&#x5225;&#xFF08;bool&#x3001;enum&#x3001;integer&#x3001;real
          &#x6216; string&#xFF09;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>source</code>  <code>text</code>
        </p>
        <p>&#x76EE;&#x524D;&#x53C3;&#x6578;&#x503C;&#x7684;&#x4F86;&#x6E90;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>min_val</code>  <code>text</code>
        </p>
        <p>&#x53C3;&#x6578;&#x7684;&#x6700;&#x5C0F;&#x5141;&#x8A31;&#x503C;&#xFF08;&#x975E;&#x6578;&#x5B57;&#x578B;&#x5225;&#x70BA;
          null&#xFF09;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>max_val</code>  <code>text</code>
        </p>
        <p>&#x53C3;&#x6578;&#x7684;&#x6700;&#x5927;&#x5141;&#x8A31;&#x503C;&#xFF08;&#x975E;&#x6578;&#x5B57;&#x578B;&#x5225;&#x70BA;
          null&#xFF09;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>enumvals</code>  <code>text[]</code>
        </p>
        <p>&#x5217;&#x8209;&#x53C3;&#x6578;&#x7684;&#x5141;&#x8A31;&#x503C;&#xFF08;&#x975E;&#x5217;&#x8209;&#x578B;&#x5225;&#x70BA;
          null&#xFF09;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>boot_val</code>  <code>text</code>
        </p>
        <p>&#x5982;&#x679C;&#x672A;&#x53E6;&#x884C;&#x8A2D;&#x5B9A;&#x53C3;&#x6578;&#xFF0C;&#x5247;&#x5728;&#x4F3A;&#x670D;&#x5668;&#x555F;&#x52D5;&#x6642;&#x9810;&#x5148;&#x7D66;&#x4E88;&#x53C3;&#x6578;&#x503C;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>reset_val</code>  <code>text</code>
        </p>
        <p>RESET &#x5C07;&#x53C3;&#x6578;&#x91CD;&#x7F6E;&#x70BA;&#x76EE;&#x524D;&#x9023;&#x7DDA;&#x4E2D;&#x7684;&#x503C;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sourcefile</code>  <code>text</code>
        </p>
        <p>&#x7D44;&#x614B;&#x6A94;&#x6848;&#x76EE;&#x524D;&#x8A2D;&#x5B9A;&#x70BA;&#x4F55;&#xFF08;&#x5C0D;&#x65BC;&#x5F9E;&#x7D44;&#x614B;&#x6A94;&#x6848;&#x4EE5;&#x5916;&#x4F86;&#x6E90;&#x8A2D;&#x5B9A;&#x7684;&#x503C;&#xFF0C;&#x6216;&#x8005;&#x7531;&#x975E;&#x8D85;&#x7D1A;&#x4F7F;&#x7528;&#x8005;&#x4E5F;&#x4E0D;&#x662F;
          pg_read_all_settings &#x7684;&#x6210;&#x54E1;&#x6240;&#x7D66;&#x4E88;&#xFF0C;&#x70BA;null&#xFF09;&#xFF1B;&#x5728;&#x7D44;&#x614B;&#x6A94;&#x6848;&#x4E2D;&#x4F7F;&#x7528;
          include &#x6307;&#x4EE4;&#x6642;&#x6703;&#x5F88;&#x6709;&#x5E6B;&#x52A9;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>sourceline</code>  <code>int4</code>
        </p>
        <p>&#x7D44;&#x614B;&#x6A94;&#x6848;&#x4E2D;&#x76EE;&#x524D;&#x8A2D;&#x5B9A;&#x6240;&#x5728;&#x7684;&#x884C;&#x865F;&#xFF08;&#x5C0D;&#x65BC;&#x5F9E;&#x7D44;&#x614B;&#x6A94;&#x6848;&#x4EE5;&#x5916;&#x4F86;&#x6E90;&#x6240;&#x8A2D;&#x5B9A;&#x7684;&#x503C;&#xFF0C;&#x6216;&#x8005;&#x7531;&#x975E;&#x8D85;&#x7D1A;&#x4F7F;&#x7528;&#x8005;&#xFF0C;&#x4E5F;&#x4E0D;&#x662F;
          pg_read_all_settings &#x6210;&#x54E1;&#x6240;&#x7D66;&#x4E88;&#x7684;&#x503C;&#xFF0C;&#x5247;&#x70BA;
          null&#xFF09;&#x3002;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><code>pending_restart</code>  <code>bool</code>
        </p>
        <p>&#x5982;&#x679C;&#x7D44;&#x614B;&#x6A94;&#x6848;&#x4E2D;&#x7684;&#x503C;&#x5DF2;&#x66F4;&#x6539;&#x4F46;&#x9700;&#x8981;&#x91CD;&#x65B0;&#x555F;&#x52D5;&#xFF0C;&#x5247;&#x70BA;
          true&#xFF1B;&#x5426;&#x5247;&#x70BA; false&#x3002;</p>
      </td>
    </tr>
  </tbody>
</table>

設定內容有幾種可能的值，是為了降低變更組態的複雜度，它們是：

`internal`

這些設定無法直接更改；它們反映了內部所決定的值，其中一些可以透過使用不同的組態選項重建伺服器，或透過更改提供給 initdb 的選項來調整。

`postmaster`

這些設定只能在伺服器啟動時套用，因此任何變更都需要重新啟動伺服器。這些設定的值通常儲存在 postgresql.conf 檔案中，或在啟動伺服器時在命令列中給予。當然，也可以在伺服器啟動時設定任何層級較低的設定。

`sighup`

可以在 postgresql.conf 中對這些設定進行變更，而毌須重新啟動伺服器。只要向 postmaster 發送一個 SIGHUP 信號，使其重新讀取 postgresql.conf 並套用變更。postmaster 還會將 SIGHUP 信號轉發給其子程序，以便它們都獲取新值。

`superuser-backend`

可以在 postgresql.conf 中對這些設定進行變更，且毌須重新啟動伺服器。它們也可以在連線要求的封包中設定為特別連線（例如，透過 libpq 的 PGOPTIONS 環境變數），但前提是連線使用者是超級使用者。但是，這些設定在啟動後的連線中永遠不會變更。如果你在 postgresql.conf 中更改它們，請向 postmaster 發送一個 SIGHUP 信號，使其重新讀取 postgresql.conf。新值只會影響隨後啟動的連線。

`backend`

可以在 postgresql.conf 中對這些設定進行變更，而毌須重新啟動伺服器。它們也可以在連線請求封包中設定為特別連線（例如，透過 libpq 的 PGOPTIONS 環境變數）；任何使用者都可以為他們的連線進行這樣的變更。但是，這些設定在啟動後的連線中永遠無法變更。如果你在 postgresql.conf 中更改它們，請向 postmaster 發送一個 SIGHUP 信號，使其重新讀取 postgresql.conf。新值只會影響隨後啟動的連線。

`superuser`

這些設定可以從 postgresql.conf 設定，也可以透過 SET 指令在連線中設定；但只有超級使用者可以透過 SET 來更改。僅當沒有使用 SET 建立連線專用的值時，postgresql.conf 中的變更才會影響現有連線。

`user`

這些設定可以從 postgresql.conf 設定，也可以透過 SET 指令在連線中設定。允許任何使用者變更其連線中所使用的值。僅當未使用 SET 未建立連線專用值時，postgresql.conf 中的變更才會影響現有連線。

有關變更這些參數的各種方法和更多資訊，請參閱[第 19.1 節](../../server-administration/server-configuration/setting-parameters.md)。

pg\_settings 檢視表無法INSERT 或 DELETE，但可以 UPDATE。套用於一行 pg\_settings 的 UPDATE 相當於對該參數執行 [SET](../../reference/sql-commands/set.md) 指令。此變更僅影響目前連線所使用的值。如果在稍後中止的交易事務中發出 UPDATE，則在回溯事務時 UPDATE 指令的效果會消失。一旦提交了相關的事務，則效果將持續到連線結束，除非被另一個 UPDATE 或 SET 覆蓋。

