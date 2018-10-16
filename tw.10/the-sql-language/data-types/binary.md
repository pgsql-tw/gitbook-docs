# 8.4. 位元組型別（bytea）

bytea 資料型別允許儲存位元組字串；詳見 [Table 8.6](binary.md#table-8-6-binary-data-types)。

#### **Table 8.6. Binary Data Types**

| Name | Storage Size | Description |
| :--- | :--- | :--- |
| `bytea` | 1 or 4 bytes 加上實際的位元組字串長度 | 可變長度二進位字串 |

位元組字串是位元組的序列。位元組字串以兩種方式與字串區分開來。首先，位元組字串特別允許儲存零值的位元組和其他「不可列印」位元組（通常是在 32 到 126 範圍之外的位元組）。字串不允許全為零位元組，並且還禁止資料庫選擇無效的字元集編碼序列。其次，對位元組字串的操作處理實際的位元組，而字串的處理取決於區域設定。簡而言之，位元組字串適合於儲存程式設計師認為是「raw bytes」的資料，而字串適合於儲存文字。

bytea 型別支援兩種輸入和輸出的外部格式：PostgreSQL 既有的「escape」格式和「十六進位」格式，輸入時始終接受這兩個。輸出格式取決於組態參數 [bytea\_output](../../server-administration/server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#bytea_output-enum)；預設值為十六進位。（注意，在 PostgreSQL 9.0 中引入了十六進位格式；早期版本和一些工具並無法解譯它。）

SQL 標準定義了一種不同的位元組字串型別，稱為 BLOB 或 BINARY LARGE OBJECT。輸入格式與 bytea 不同，但提供的函數和運算子大致相同。

## 8.4.1. `bytea` 十六進位格式

「十六進位」格式將二進位資料編碼為每個位元組為 2 個十六進位數字，儲存不反轉。整個字符串前面是序列 \x（以區別於轉譯格式）。在某些情況下，初始倒斜線可能需要透過加倍來進行轉譯，在相同的情況下，倒斜線必須以轉譯格式加倍；細節如下。十六進位數字可以是大寫或小寫，並且在數字組之間允許空格（但不在數字組內，也不在起始 \x 序列中）。十六進位格式與各種外部應用程序和協議相容，並且轉換速度往往比轉譯格式更快，因此偏好使用它。

例如：

```text
SELECT E'\\xDEADBEEF';
```

## 8.4.2. `bytea` 轉譯（escape）格式

「轉義」格式是 bytea 型別的傳統 PostgreSQL 格式。它採用將位元組字串表示為 ASCII 字元序列的方法，同時將那些不能表示為 ASCII 字元的位元組轉換為特殊的轉譯序列。如果從應用程序的角度來看，將位元組表示為字元是有意義的，那麼這種表示可以很方便。但實際上它通常會令人困惑，因為它模糊了位元組字串和字串之間的區別，而且所選擇的特定轉譯機制也有點笨拙。因此，對於大多數新的應用程序，應該避免使用此格式。

以轉譯格式輸入 bytea 值時，必須轉譯某些值的位元組，也同時可以轉譯所有位元組值。通常，要轉譯位元組，請將其轉換為三位數的八進位值，並在其前面加一個倒斜線（或兩個倒斜線，如果要使用轉譯字串語法將值寫為文字的話）。倒斜線本身（位元組 92）也可以用雙倒斜線表示。[Table 8.7](binary.md#table-8-7-bytea-literal-escaped-octets) 列出了必須轉譯的字元，並在適合的情況下提供了備用轉譯序列。

#### **Table 8.7. `bytea` Literal Escaped Octets**

| Decimal Octet Value | Description | Escaped Input Representation | Example | Output Representation |
| :--- | :--- | :--- | :--- | :--- |
| 0 | zero octet | `E'\\000'` | `SELECT E'\\000'::bytea;` | `\000` |
| 39 | single quote | `''''` or `E'\\047'` | `SELECT E'\''::bytea;` | `'` |
| 92 | backslash | `E'\\\\'` or `E'\\134'` | `SELECT E'\\\\'::bytea;` | `\\` |
| 0 to 31 and 127 to 255 | “non-printable” octets | `E'\\`_`xxx'`_ \(octal value\) | `SELECT E'\\001'::bytea;` | `\001` |

轉譯不可列印的位元組的要求因區域設定而異。在某些情況下，你可以放棄他們而不轉譯。請注意，即使看起來有時多於一個字符，[Table 8.7](binary.md#table-8-7-bytea-literal-escaped-octets) 中每個範例的結果也只有一個位元組。

如 Table 8.7 所示，需要多個倒斜線的原因是，作為字串文字編輯的輸入字串必須通過 PostgreSQL 伺服器中的兩個解析階段。每組的第一個倒斜線以字串文字解析器解釋為轉譯字元（假設使用了轉譯字串語法）並因此被消耗，留下該組的第二個倒斜線。（錢字號引用的字串可用於避免此轉譯程序。）然後，bytea 輸入函數將剩餘的倒斜線識別從三位數八進位值開始或轉譯另一個倒斜線。例如，在通過轉譯字串解析器後，作為 E'\ 001' 傳遞給伺服器的字串文字變為 \001。然後將 \001 發送到 bytea 輸入函數，在該函數中將其轉換為十進制值為 1 的單個位元組。請注意，單引號字元不受 bytea 特殊處理，因此它遵循字串文字的一般規則。（另詳見[第 4.1.2.1 節](../sql-syntax/lexical-structure.md#4-1-2-1-zi-chuan-chang)。）

bytea 位元組有時在輸出時被轉義。通常，每個「不可列印」的位元組都會轉換為等效的三位數八進位值，並以一個倒斜線開頭。大多數「可列印」位元組由它們在用戶端字元集中的標準來表示。十進位值為 92（倒斜線）的位元組在輸出中會加倍。詳情見 [Table 8.8](binary.md#table-8-8-bytea-output-escaped-octets)。

#### **Table 8.8. `bytea` Output Escaped Octets**

| Decimal Octet Value | Description | Escaped Output Representation | Example | Output Result |
| :--- | :--- | :--- | :--- | :--- |
| 92 | backslash | `\\` | `SELECT E'\\134'::bytea;` | `\\` |
| 0 to 31 and 127 to 255 | “non-printable” octets | `\`_`xxx`_ \(octal value\) | `SELECT E'\\001'::bytea;` | `\001` |
| 32 to 126 | “printable” octets | client character set representation | `SELECT E'\\176'::bytea;` | `~` |

根據您使用的 PostgreSQL 的前端，在轉譯和未轉譯 bytea 字串方面可能還有其他工作要做。例如，如果您的界面會自動轉譯這些，您可能還必須轉譯換行符號和回行首符號。

