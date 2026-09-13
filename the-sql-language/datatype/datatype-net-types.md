<a id="DATATYPE-NET-TYPES"></a>

## 8.9. 網路位址型別 [#](#DATATYPE-NET-TYPES)

[8.9.1. `inet`](datatype-net-types.md#DATATYPE-INET)

[8.9.2. `cidr`](datatype-net-types.md#DATATYPE-CIDR)

[8.9.3. `inet` 與 `cidr` 的比較](datatype-net-types.md#DATATYPE-INET-VS-CIDR)

[8.9.4. `macaddr`](datatype-net-types.md#DATATYPE-MACADDR)

[8.9.5. `macaddr8`](datatype-net-types.md#DATATYPE-MACADDR8)

<a id="id-1.5.7.17.2"></a>

PostgreSQL 提供了用來儲存 IPv4、IPv6 與 MAC 位址的資料型別，如[表 8.21](datatype-net-types.md#DATATYPE-NET-TYPES-TABLE) 所示。儲存網路位址時，使用這些型別會比使用單純的文字型別更好，因為這些型別提供了輸入的錯誤檢查，以及專門的運算子與函式（請參閱[第 9.12 節](../functions/functions-net.md)）。

<a id="DATATYPE-NET-TYPES-TABLE"></a>

**表 8.21. 網路位址型別**

<table border="1" class="table" summary="網路位址型別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>儲存空間大小</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">cidr</code></td><td>7 或 19 個位元組</td><td>IPv4 與 IPv6 網路</td></tr><tr><td><code class="type">inet</code></td><td>7 或 19 個位元組</td><td>IPv4 與 IPv6 主機與網路</td></tr><tr><td><code class="type">macaddr</code></td><td>6 個位元組</td><td>MAC 位址</td></tr><tr><td><code class="type">macaddr8</code></td><td>8 個位元組</td><td>MAC 位址（EUI-64 格式）</td></tr></tbody></table>

<br>

在對 `inet` 或 `cidr` 資料型別排序時，IPv4 位址一律會排在 IPv6 位址之前，包括那些被封裝或對映到 IPv6 位址的 IPv4 位址，例如 ::10.2.3.4 或 ::ffff:10.4.3.2。

<a id="DATATYPE-INET"></a>

### 8.9.1. `inet` [#](#DATATYPE-INET)

<a id="id-1.5.7.17.6.2"></a>

`inet` 型別在同一個欄位中存放一個 IPv4 或 IPv6 主機位址，以及選擇性的子網路資訊。子網路是以該主機位址中屬於網路位址的位元數（即「網路遮罩」）來表示。如果網路遮罩是 32 而位址是 IPv4，那麼這個值並不表示一個子網路，而只表示單一主機。在 IPv6 中，位址長度是 128 位元，所以 128 位元就指定了一個唯一的主機位址。請注意，如果你只想接受網路，應該使用 `cidr` 型別而不是 `inet`。

這個型別的輸入格式是 *`address/y`*，其中 *`address`* 是 IPv4 或 IPv6 位址，而 *`y`* 則是網路遮罩的位元數。如果省略 *`/y`* 的部分，網路遮罩會被視為 IPv4 的 32 或 IPv6 的 128，因此該值就只代表單一主機。顯示時，如果網路遮罩所指定的是單一主機，*`/y`* 的部分會被省略。

<a id="DATATYPE-CIDR"></a>

### 8.9.2. `cidr` [#](#DATATYPE-CIDR)

<a id="id-1.5.7.17.7.2"></a>

`cidr` 型別存放的是 IPv4 或 IPv6 的網路指定。其輸入與輸出格式遵循無類別網際網域路由（Classless Internet Domain Routing）的慣例。指定網路的格式是 *`address/y`*，其中 *`address`* 是該網路中以 IPv4 或 IPv6 位址表示的最小位址，而 *`y`* 則是網路遮罩的位元數。如果省略 *`y`*，它會依據較舊的分類式網路編號系統的假設來計算，但至少會大到足以涵蓋輸入中所寫出的所有位元組。如果所指定的網路位址在指定的網路遮罩右側還有位元被設定，就會發生錯誤。

[表 8.22](datatype-net-types.md#DATATYPE-NET-CIDR-TABLE) 列出一些範例。

<a id="DATATYPE-NET-CIDR-TABLE"></a>

**表 8.22. `cidr` 型別的輸入範例**

<table border="1" class="table" summary="cidr 型別的輸入範例"><colgroup><col/><col/><col/></colgroup><thead><tr><th><code class="type">cidr</code> 輸入</th><th><code class="type">cidr</code> 輸出</th><th><code class="literal"><code class="function">abbrev(<code class="type">cidr</code>)</code></code></th></tr></thead><tbody><tr><td>192.168.100.128/25</td><td>192.168.100.128/25</td><td>192.168.100.128/25</td></tr><tr><td>192.168/24</td><td>192.168.0.0/24</td><td>192.168.0/24</td></tr><tr><td>192.168/25</td><td>192.168.0.0/25</td><td>192.168.0.0/25</td></tr><tr><td>192.168.1</td><td>192.168.1.0/24</td><td>192.168.1/24</td></tr><tr><td>192.168</td><td>192.168.0.0/24</td><td>192.168.0/24</td></tr><tr><td>128.1</td><td>128.1.0.0/16</td><td>128.1/16</td></tr><tr><td>128</td><td>128.0.0.0/16</td><td>128.0/16</td></tr><tr><td>128.1.2</td><td>128.1.2.0/24</td><td>128.1.2/24</td></tr><tr><td>10.1.2</td><td>10.1.2.0/24</td><td>10.1.2/24</td></tr><tr><td>10.1</td><td>10.1.0.0/16</td><td>10.1/16</td></tr><tr><td>10</td><td>10.0.0.0/8</td><td>10/8</td></tr><tr><td>10.1.2.3/32</td><td>10.1.2.3/32</td><td>10.1.2.3/32</td></tr><tr><td>2001:4f8:3:ba::/64</td><td>2001:4f8:3:ba::/64</td><td>2001:4f8:3:ba/64</td></tr><tr><td>2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128</td><td>2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128</td><td>2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128</td></tr><tr><td>::ffff:1.2.3.0/120</td><td>::ffff:1.2.3.0/120</td><td>::ffff:1.2.3/120</td></tr><tr><td>::ffff:1.2.3.0/128</td><td>::ffff:1.2.3.0/128</td><td>::ffff:1.2.3.0/128</td></tr></tbody></table>

<br>

<a id="DATATYPE-INET-VS-CIDR"></a>

### 8.9.3. `inet` 與 `cidr` 的比較 [#](#DATATYPE-INET-VS-CIDR)

`inet` 與 `cidr` 這兩種資料型別最主要的差別在於：`inet` 接受在網路遮罩右側含有非零位元的值，而 `cidr` 則不接受。例如 `192.168.0.1/24` 對 `inet` 而言是有效的，但對 `cidr` 而言則否。

### 提示

如果你不喜歡 `inet` 或 `cidr` 值的輸出格式，可以試試 `host`、`text` 與 `abbrev` 這幾個函式。

<a id="DATATYPE-MACADDR"></a>

### 8.9.4. `macaddr` [#](#DATATYPE-MACADDR)

<a id="id-1.5.7.17.9.2"></a><a id="id-1.5.7.17.9.3"></a>

`macaddr` 型別儲存 MAC 位址，這種位址最為人所知的例子就是乙太網路卡的硬體位址（不過 MAC 位址也用於其他用途）。輸入時可接受以下格式：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">'08:00:2b:01:02:03'</code></td></tr><tr><td><code class="literal">'08-00-2b-01-02-03'</code></td></tr><tr><td><code class="literal">'08002b:010203'</code></td></tr><tr><td><code class="literal">'08002b-010203'</code></td></tr><tr><td><code class="literal">'0800.2b01.0203'</code></td></tr><tr><td><code class="literal">'0800-2b01-0203'</code></td></tr><tr><td><code class="literal">'08002b010203'</code></td></tr></table>

這些範例指定的都是同一個位址。數字 `a` 到 `f` 大小寫皆可接受。輸出一律採用所示格式中的第一種。

IEEE Standard 802-2001 把所示的第二種格式（使用連字號）規定為 MAC 位址的標準格式，並規定第一種格式（使用冒號）用於位元反轉、MSB 在前的表示法，因此 08-00-2b-01-02-03 = 10:00:D4:80:40:C0。這個慣例如今普遍不被採用，而且只與過時的網路通訊協定（例如 Token Ring）有關。PostgreSQL 並未提供任何位元反轉的機制；所有可接受的格式都採用標準的 LSB 順序。

其餘五種輸入格式並不屬於任何標準。

<a id="DATATYPE-MACADDR8"></a>

### 8.9.5. `macaddr8` [#](#DATATYPE-MACADDR8)

<a id="id-1.5.7.17.10.2"></a><a id="id-1.5.7.17.10.3"></a>

`macaddr8` 型別以 EUI-64 格式儲存 MAC 位址，這種位址最為人所知的例子就是乙太網路卡的硬體位址（不過 MAC 位址也用於其他用途）。這個型別可以接受 6 個位元組與 8 個位元組長度的 MAC 位址，並以 8 個位元組的長度格式儲存它們。以 6 個位元組格式給定的 MAC 位址會以 8 個位元組的長度格式儲存，其中第 4 與第 5 個位元組分別設為 FF 與 FE。請注意，IPv6 使用的是經過修改的 EUI-64 格式，在由 EUI-48 轉換之後第 7 個位元應該設為 1。系統提供了 `macaddr8_set7bit` 函式來進行這項變更。一般而言，只要輸入是由成對的十六進位數字（以位元組為界）所組成，並可選擇性地一致以 `':'`、`'-'` 或 `'.'` 其中之一分隔，都可以被接受。十六進位數字的個數必須是 16（8 個位元組）或 12（6 個位元組）。開頭與結尾的空白字元會被忽略。以下是可接受的輸入格式範例：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">'08:00:2b:01:02:03:04:05'</code></td></tr><tr><td><code class="literal">'08-00-2b-01-02-03-04-05'</code></td></tr><tr><td><code class="literal">'08002b:0102030405'</code></td></tr><tr><td><code class="literal">'08002b-0102030405'</code></td></tr><tr><td><code class="literal">'0800.2b01.0203.0405'</code></td></tr><tr><td><code class="literal">'0800-2b01-0203-0405'</code></td></tr><tr><td><code class="literal">'08002b01:02030405'</code></td></tr><tr><td><code class="literal">'08002b0102030405'</code></td></tr></table>

這些範例指定的都是同一個位址。數字 `a` 到 `f` 大小寫皆可接受。輸出一律採用所示格式中的第一種。

上面所示的最後六種輸入格式並不屬於任何標準。

若要把傳統的 48 位元 EUI-48 格式 MAC 位址轉換成經過修改的 EUI-64 格式，以便作為 IPv6 位址的主機部分，請依下列方式使用 `macaddr8_set7bit`：

```

SELECT macaddr8_set7bit('08:00:2b:01:02:03');

    macaddr8_set7bit
-------------------------
 0a:00:2b:ff:fe:01:02:03
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-net-types.html)（原文版本：18.6；核對日期：2026-09-13）
