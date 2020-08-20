# 9.12. 網路位址函式及運算子

[Table 9.36](https://www.postgresql.org/docs/10/static/functions-net.html#cidr-inet-operators-table)shows the operators available for the`cidr`and`inet`types. The operators`<<`,`<<=`,`>>`,`>>=`, and`&&`test for subnet inclusion. They consider only the network parts of the two addresses \(ignoring any host part\) and determine whether one network is identical to or a subnet of the other.

**Table 9.36.** `cidr`**and**`inet`**Operators**

| Operator | Description | Example |  |  |
| :--- | :--- | :--- | :--- | :--- |
| `<` | is less than | `inet '192.168.1.5' < inet '192.168.1.6'` |  |  |
| `<=` | is less than or equal | `inet '192.168.1.5' <= inet '192.168.1.5'` |  |  |
| `=` | equals | `inet '192.168.1.5' = inet '192.168.1.5'` |  |  |
| `>=` | is greater or equal | `inet '192.168.1.5' >= inet '192.168.1.5'` |  |  |
| `>` | is greater than | `inet '192.168.1.5' > inet '192.168.1.4'` |  |  |
| `<>` | is not equal | `inet '192.168.1.5' <> inet '192.168.1.4'` |  |  |
| `<<` | is contained by | `inet '192.168.1.5' << inet '192.168.1/24'` |  |  |
| `<<=` | is contained by or equals | `inet '192.168.1/24' <<= inet '192.168.1/24'` |  |  |
| `>>` | contains | `inet '192.168.1/24' >> inet '192.168.1.5'` |  |  |
| `>>=` | contains or equals | `inet '192.168.1/24' >>= inet '192.168.1/24'` |  |  |
| `&&` | contains or is contained by | `inet '192.168.1/24' && inet '192.168.1.80/28'` |  |  |
| `~` | bitwise NOT | `~ inet '192.168.1.6'` |  |  |
| `&` | bitwise AND | `inet '192.168.1.6' & inet '0.0.0.255'` |  |  |
| \` | \` | bitwise OR | \`inet '192.168.1.6' | inet '0.0.0.255'\` |
| `+` | addition | `inet '192.168.1.6' + 25` |  |  |
| `-` | subtraction | `inet '192.168.1.43' - 36` |  |  |
| `-` | subtraction | `inet '192.168.1.43' - inet '192.168.1.19'` |  |  |

[Table 9.37](https://www.postgresql.org/docs/10/static/functions-net.html#cidr-inet-functions-table)shows the functions available for use with the`cidr`and`inet`types. The`abbrev`,`host`, and`text`functions are primarily intended to offer alternative display formats.

**Table 9.37.** `cidr`**and**`inet`**Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `abbrev(inet`\) | `text` | abbreviated display format as text | `abbrev(inet '10.1.0.0/16')` | `10.1.0.0/16` |
| `abbrev(cidr`\) | `text` | abbreviated display format as text | `abbrev(cidr '10.1.0.0/16')` | `10.1/16` |
| `broadcast(inet`\) | `inet` | broadcast address for network | `broadcast('192.168.1.5/24')` | `192.168.1.255/24` |
| `family(inet`\) | `int` | extract family of address;`4`for IPv4,`6`for IPv6 | `family('::1')` | `6` |
| `host(inet`\) | `text` | extract IP address as text | `host('192.168.1.5/24')` | `192.168.1.5` |
| `hostmask(inet`\) | `inet` | construct host mask for network | `hostmask('192.168.23.20/30')` | `0.0.0.3` |
| `masklen(inet`\) | `int` | extract netmask length | `masklen('192.168.1.5/24')` | `24` |
| `netmask(inet`\) | `inet` | construct netmask for network | `netmask('192.168.1.5/24')` | `255.255.255.0` |
| `network(inet`\) | `cidr` | extract network part of address | `network('192.168.1.5/24')` | `192.168.1.0/24` |
| `set_masklen(inet`,`int`\) | `inet` | set netmask length for`inet`value | `set_masklen('192.168.1.5/24', 16)` | `192.168.1.5/16` |
| `set_masklen(cidr`,`int`\) | `cidr` | set netmask length for`cidr`value | `set_masklen('192.168.1.0/24'::cidr, 16)` | `192.168.0.0/16` |
| `text(inet`\) | `text` | extract IP address and netmask length as text | `text(inet '192.168.1.5')` | `192.168.1.5/32` |
| `inet_same_family(inet`,`inet`\) | `boolean` | are the addresses from the same family? | `inet_same_family('192.168.1.5/24', '::1')` | `false` |
| `inet_merge(inet`,`inet`\) | `cidr` | the smallest network which includes both of the given networks | `inet_merge('192.168.1.5/24', '192.168.2.5/24')` | `192.168.0.0/22` |

Any`cidr`value can be cast to`inet`implicitly or explicitly; therefore, the functions shown above as operating on`inet`also work on`cidr`values. \(Where there are separate functions for`inet`and`cidr`, it is because the behavior should be different for the two cases.\) Also, it is permitted to cast an`inet`value to`cidr`. When this is done, any bits to the right of the netmask are silently zeroed to create a valid`cidr`value. In addition, you can cast a text value to`inet`or`cidr`using normal casting syntax: for example,`inet(expression`\)or`colname`::cidr.

[Table 9.38](https://www.postgresql.org/docs/10/static/functions-net.html#macaddr-functions-table)shows the functions available for use with the`macaddr`type. The function`trunc(macaddr`\)returns a MAC address with the last 3 bytes set to zero. This can be used to associate the remaining prefix with a manufacturer.

**Table 9.38.** `macaddr`**Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `trunc(macaddr`\) | `macaddr` | set last 3 bytes to zero | `trunc(macaddr '12:34:56:78:90:ab')` | `12:34:56:00:00:00` |

The`macaddr`type also supports the standard relational operators \(`>`,`<=`, etc.\) for lexicographical ordering, and the bitwise arithmetic operators \(`~`,`&`and`|`\) for NOT, AND and OR.

[Table 9.39](https://www.postgresql.org/docs/10/static/functions-net.html#macaddr8-functions-table)shows the functions available for use with the`macaddr8`type. The function`trunc(macaddr8`\)returns a MAC address with the last 5 bytes set to zero. This can be used to associate the remaining prefix with a manufacturer.

**Table 9.39.** `macaddr8`**Functions**

| Function | Return Type | Description | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `trunc(macaddr8`\) | `macaddr8` | set last 5 bytes to zero | `trunc(macaddr8 '12:34:56:78:90:ab:cd:ef')` | `12:34:56:00:00:00:00:00` |
| `macaddr8_set7bit(macaddr8`\) | `macaddr8` | set 7th bit to one, also known as modified EUI-64, for inclusion in an IPv6 address | `macaddr8_set7bit(macaddr8 '00:34:56:ab:cd:ef')` | `02:34:56:ff:fe:ab:cd:ef` |

The`macaddr8`type also supports the standard relational operators \(`>`,`<=`, etc.\) for ordering, and the bitwise arithmetic operators \(`~`,`&`and`|`\) for NOT, AND and OR.

