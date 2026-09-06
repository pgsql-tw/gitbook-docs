# 8.9. 網路位址型別

PostgreSQL 提供了用於儲存 IPv4、IPv6 和 MAC 位址的資料型別，如 [Table 8.21](network-address-types.md#table-8.21.-network-address-types) 所示。可以的話，最好使用這些型別而不是文字型別來儲存網路位址，因為這些型別提供了輸入錯誤檢查以及專用的操作子和函數（請參閱[第 9.12 節](../functions-and-operators/network-address-functions-and-operators.md)）。

#### **Table 8.21. Network Address Types**

| Name       | Storage Size  | Description                      |
| ---------- | ------------- | -------------------------------- |
| `cidr`     | 7 or 19 bytes | IPv4 and IPv6 networks           |
| `inet`     | 7 or 19 bytes | IPv4 and IPv6 hosts and networks |
| `macaddr`  | 6 bytes       | MAC addresses                    |
| `macaddr8` | 8 bytes       | MAC addresses (EUI-64 format)    |

對 inet 或 cidr 資料型別進行排序時，IPv4 位址將會排在 IPv6 位址之前，包括封裝或對應到 IPv6 位址的 IPv4 位址，例如 ::10.2.3.4 或 ::ffff:10.4.3.2。

## 8.9.1. `inet`&#x20;

inet 型別包含 IPv4 或 IPv6 網路位址及其可選的子網，它們都包含在一個欄位中。子網路由網路位址（「網路遮罩」）中的網路位址位元數表示。如果網路遮罩為 32 位元且位址為 IPv4，則該值不表示子網，而僅表示單一網路位址。在 IPv6 中，位址長度為 128 位，因此 128 位元指定唯一的主機位址。請注意，如果您只想表現網路，而不是位址，則應使用 cidr 型別而不是 inet 型別。

此型別的輸入格式為 address/y，其中 address 是 IPv4 或 IPv6 位址，y 是網路遮罩的位元數。如果省略 /y 部分，則網路遮罩在 IPv4 中視為 32 位元，在 IPv6 中視為 128 位元，因此該值僅表示單一位址。如果網路遮罩指定單一主機，顯示時會隱藏 /y 部分。

## 8.9.2. `cidr`&#x20;

cidr 型別包含 IPv4 或 IPv6 網路規範。輸入和輸出格式遵循 Classless Internet Domain Routing 約定。指定網路的格式為 address/y，其中 address 是網路的最低的位址，以 IPv4 或 IPv6 位址表示，y 是網路遮罩的位元數。如果省略 y，則使用舊有類別網路系統的假設來計算，但它至少要足夠大，以包含輸入中所有的位元組。指定網路位址時，如果其位元設定在指定網路遮罩的右側，則會導致錯誤。

[Table 8.22](network-address-types.md#table-8.22.-cidr-type-input-examples) 列出了一些範例。

#### **Table 8.22. `cidr` Type Input Examples**

| `cidr` Input                          | `cidr` Output                         | `abbrev(cidr)`                        |
| ------------------------------------- | ------------------------------------- | ------------------------------------- |
| 192.168.100.128/25                    | 192.168.100.128/25                    | 192.168.100.128/25                    |
| 192.168/24                            | 192.168.0.0/24                        | 192.168.0/24                          |
| 192.168/25                            | 192.168.0.0/25                        | 192.168.0.0/25                        |
| 192.168.1                             | 192.168.1.0/24                        | 192.168.1/24                          |
| 192.168                               | 192.168.0.0/24                        | 192.168.0/24                          |
| 128.1                                 | 128.1.0.0/16                          | 128.1/16                              |
| 128                                   | 128.0.0.0/16                          | 128.0/16                              |
| 128.1.2                               | 128.1.2.0/24                          | 128.1.2/24                            |
| 10.1.2                                | 10.1.2.0/24                           | 10.1.2/24                             |
| 10.1                                  | 10.1.0.0/16                           | 10.1/16                               |
| 10                                    | 10.0.0.0/8                            | 10/8                                  |
| 10.1.2.3/32                           | 10.1.2.3/32                           | 10.1.2.3/32                           |
| 2001:4f8:3:ba::/64                    | 2001:4f8:3:ba::/64                    | 2001:4f8:3:ba/64                      |
| 2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128 | 2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128 | 2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128 |
| ::ffff:1.2.3.0/120                    | ::ffff:1.2.3.0/120                    | ::ffff:1.2.3/120                      |
| ::ffff:1.2.3.0/128                    | ::ffff:1.2.3.0/128                    | ::ffff:1.2.3.0/128                    |

## 8.9.3. `inet` vs. `cidr`&#x20;

inet 和 cidr 資料型別的本質差異在於，inet 接受網路遮罩右側非零的值，而 cidr 則不接受。例如，192.168.0.1/24 對 inet 有效，但對 cidr 無效。

{% hint style="info" %}
如果您不喜歡 inet 或 cidr 值的標準輸出格式，請嘗試使用函數 host、text 和 abbrev。
{% endhint %}

## 8.9.4. `macaddr`&#x20;

The `macaddr` type stores MAC addresses, known for example from Ethernet card hardware addresses (although MAC addresses are used for other purposes as well). Input is accepted in the following formats:

| `'08:00:2b:01:02:03'` |
| --------------------- |
| `'08-00-2b-01-02-03'` |
| `'08002b:010203'`     |
| `'08002b-010203'`     |
| `'0800.2b01.0203'`    |
| `'0800-2b01-0203'`    |
| `'08002b010203'`      |

These examples all specify the same address. Upper and lower case is accepted for the digits `a` through `f`. Output is always in the first of the forms shown.

IEEE Standard 802-2001 specifies the second form shown (with hyphens) as the canonical form for MAC addresses, and specifies the first form (with colons) as used with bit-reversed, MSB-first notation, so that 08-00-2b-01-02-03 = 10:00:D4:80:40:C0. This convention is widely ignored nowadays, and it is relevant only for obsolete network protocols (such as Token Ring). PostgreSQL makes no provisions for bit reversal; all accepted formats use the canonical LSB order.

The remaining five input formats are not part of any standard.

## 8.9.5. `macaddr8`&#x20;

The `macaddr8` type stores MAC addresses in EUI-64 format, known for example from Ethernet card hardware addresses (although MAC addresses are used for other purposes as well). This type can accept both 6 and 8 byte length MAC addresses and stores them in 8 byte length format. MAC addresses given in 6 byte format will be stored in 8 byte length format with the 4th and 5th bytes set to FF and FE, respectively. Note that IPv6 uses a modified EUI-64 format where the 7th bit should be set to one after the conversion from EUI-48. The function `macaddr8_set7bit` is provided to make this change. Generally speaking, any input which is comprised of pairs of hex digits (on byte boundaries), optionally separated consistently by one of `':'`, `'-'` or `'.'`, is accepted. The number of hex digits must be either 16 (8 bytes) or 12 (6 bytes). Leading and trailing whitespace is ignored. The following are examples of input formats that are accepted:

| `'08:00:2b:01:02:03:04:05'` |
| --------------------------- |
| `'08-00-2b-01-02-03-04-05'` |
| `'08002b:0102030405'`       |
| `'08002b-0102030405'`       |
| `'0800.2b01.0203.0405'`     |
| `'0800-2b01-0203-0405'`     |
| `'08002b01:02030405'`       |
| `'08002b0102030405'`        |

These examples all specify the same address. Upper and lower case is accepted for the digits `a` through `f`. Output is always in the first of the forms shown.

The last six input formats shown above are not part of any standard.

To convert a traditional 48 bit MAC address in EUI-48 format to modified EUI-64 format to be included as the host portion of an IPv6 address, use `macaddr8_set7bit` as shown:

```
SELECT macaddr8_set7bit('08:00:2b:01:02:03');

    macaddr8_set7bit
-------------------------
 0a:00:2b:ff:fe:01:02:03
(1 row)

```

<br>
