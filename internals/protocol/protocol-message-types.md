<a id="PROTOCOL-MESSAGE-TYPES"></a>

## 54.6. 訊息資料型別 [#](#protocol-message-types) <a href="#protocol-message-types" id="protocol-message-types"></a>

本節說明訊息中使用的基本資料型別。

Int*`n`*(*`i`*)

以網路位元組順序（最高有效位元組在前）表示的 *`n`* 位元整數。若指定了 *`i`*，它就是將會出現的確切值，否則該值是可變的。例如 Int16、Int32(42)。

Int*`n`*[*`k`*]

由 *`k`* 個 *`n`* 位元整數組成的陣列，每個整數都以網路位元組順序表示。陣列長度 *`k`* 一律由訊息中較早的欄位決定。例如 Int16[M]。

String(*`s`*)

以 null 結尾的字串（C 風格字串）。字串沒有特定的長度限制。若指定了 *`s`*，它就是將會出現的確切值，否則該值是可變的。例如 String、String("user")。

### 注意

後端可傳回的字串長度*沒有預先定義的限制*。對前端而言，好的程式撰寫策略是使用可擴充的緩衝區，如此一來，任何能放進記憶體的內容都可以被接受。若這樣做不可行，請讀取完整的字串，並丟棄放不進固定大小緩衝區的尾端字元。

Byte*`n`*(*`c`*)

恰好 *`n`* 個位元組。若欄位寬度 *`n`* 不是常數，它一律可以從訊息中較早的欄位決定。若指定了 *`c`*，它就是確切的值。例如 Byte2、Byte1('\n')。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/protocol-message-types.html)（原文版本：18.6；核對日期：2026-10-12）
