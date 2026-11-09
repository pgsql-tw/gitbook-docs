# 8.9.2. cidr

<a id="DATATYPE-CIDR"></a>

## 8.9.2. `cidr` [#](#datatype-cidr) <a href="#datatype-cidr" id="datatype-cidr"></a>

<a id="id-1.5.7.17.7.2"></a>

`cidr` 型別存放的是 IPv4 或 IPv6 的網路指定。其輸入與輸出格式遵循無類別網際網域路由（Classless Internet Domain Routing）的慣例。指定網路的格式是 *`address/y`*，其中 *`address`* 是該網路中以 IPv4 或 IPv6 位址表示的最小位址，而 *`y`* 則是網路遮罩的位元數。如果省略 *`y`*，它會依據較舊的分類式網路編號系統的假設來計算，但至少會大到足以涵蓋輸入中所寫出的所有位元組。如果所指定的網路位址在指定的網路遮罩右側還有位元被設定，就會發生錯誤。

[表 8.22](#datatype-net-cidr-table) 列出一些範例。

<a id="DATATYPE-NET-CIDR-TABLE"></a>

### 表 8.22. `cidr` 型別的輸入範例 [#](#datatype-net-cidr-table) <a href="#datatype-net-cidr-table" id="datatype-net-cidr-table"></a>

<table border="1" class="table" summary="cidr 型別的輸入範例"><colgroup><col/><col/><col/></colgroup><thead><tr><th><code class="type">cidr</code> 輸入</th><th><code class="type">cidr</code> 輸出</th><th><code class="literal"><code class="function">abbrev(<code class="type">cidr</code>)</code></code></th></tr></thead><tbody><tr><td>192.168.100.128/25</td><td>192.168.100.128/25</td><td>192.168.100.128/25</td></tr><tr><td>192.168/24</td><td>192.168.0.0/24</td><td>192.168.0/24</td></tr><tr><td>192.168/25</td><td>192.168.0.0/25</td><td>192.168.0.0/25</td></tr><tr><td>192.168.1</td><td>192.168.1.0/24</td><td>192.168.1/24</td></tr><tr><td>192.168</td><td>192.168.0.0/24</td><td>192.168.0/24</td></tr><tr><td>128.1</td><td>128.1.0.0/16</td><td>128.1/16</td></tr><tr><td>128</td><td>128.0.0.0/16</td><td>128.0/16</td></tr><tr><td>128.1.2</td><td>128.1.2.0/24</td><td>128.1.2/24</td></tr><tr><td>10.1.2</td><td>10.1.2.0/24</td><td>10.1.2/24</td></tr><tr><td>10.1</td><td>10.1.0.0/16</td><td>10.1/16</td></tr><tr><td>10</td><td>10.0.0.0/8</td><td>10/8</td></tr><tr><td>10.1.2.3/32</td><td>10.1.2.3/32</td><td>10.1.2.3/32</td></tr><tr><td>2001:4f8:3:ba::/64</td><td>2001:4f8:3:ba::/64</td><td>2001:4f8:3:ba/64</td></tr><tr><td>2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128</td><td>2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128</td><td>2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128</td></tr><tr><td>::ffff:1.2.3.0/120</td><td>::ffff:1.2.3.0/120</td><td>::ffff:1.2.3/120</td></tr><tr><td>::ffff:1.2.3.0/128</td><td>::ffff:1.2.3.0/128</td><td>::ffff:1.2.3.0/128</td></tr></tbody></table>

<br>

[返回 8.9. 網路位址型別](../datatype-net-types.md#datatype-net-types)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-net-types.html)（原文版本：18.6；核對日期：2026-09-13）
