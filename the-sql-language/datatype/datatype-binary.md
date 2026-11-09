<a id="DATATYPE-BINARY"></a>

## 8.4. 二進位資料型別 [#](#datatype-binary) <a href="#datatype-binary" id="datatype-binary"></a>

[8.4.1. `bytea` 十六進位格式](datatype-binary.md#datatype-binary-bytea-hex-format)

[8.4.2. `bytea` 跳脫格式](datatype-binary/datatype-binary-bytea-escape-format.md#datatype-binary-bytea-escape-format)

<a id="id-1.5.7.12.2"></a><a id="id-1.5.7.12.3"></a>

`bytea` 資料型別可以用來儲存二進位字串；請參閱[表 8.6](datatype-binary.md#datatype-binary-table)。

<a id="DATATYPE-BINARY-TABLE"></a>

### 表 8.6. 二進位資料型別 [#](#datatype-binary-table) <a href="#datatype-binary-table" id="datatype-binary-table"></a>

<table border="1" class="table" summary="二進位資料型別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>儲存空間大小</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">bytea</code></td><td>1 或 4 個位元組加上實際的二進位字串</td><td>可變長度的二進位字串</td></tr></tbody></table>

<br>

二進位字串是由一連串的位元組（octet，或稱 byte）所組成。二進位字串與字元字串有兩點不同。第一，二進位字串明確允許儲存值為零的位元組，以及其他「不可列印」的位元組（通常是十進位 32 到 126 範圍之外的位元組）。字元字串不允許零位元組，也不允許任何其他依資料庫所選用的字元集編碼而言屬於無效的位元組值與位元組值序列。第二，對二進位字串的操作處理的是實際的位元組，而字元字串的處理則取決於語系設定。簡而言之，二進位字串適合用來儲存程式設計者視為「原始位元組」的資料，而字元字串則適合用來儲存文字。

`bytea` 型別的輸入與輸出支援兩種格式：「十六進位」格式，以及 PostgreSQL 沿用已久的「跳脫」格式。這兩種格式在輸入時一律都會被接受。輸出格式則取決於組態參數 [bytea_output](../../server-administration/runtime-config/runtime-config-client.md#GUC-BYTEA-OUTPUT)，預設值是十六進位。（請注意，十六進位格式是在 PostgreSQL 9.0 引入的；較早的版本與某些工具並不認得它。）

SQL 標準定義了另一種不同的二進位字串型別，稱為 `BLOB` 或 `BINARY LARGE OBJECT`。其輸入格式與 `bytea` 不同，但所提供的函式與運算子則大致相同。

<a id="DATATYPE-BINARY-BYTEA-HEX-FORMAT"></a>

### 8.4.1. `bytea` 十六進位格式 [#](#datatype-binary-bytea-hex-format) <a href="#datatype-binary-bytea-hex-format" id="datatype-binary-bytea-hex-format"></a>

「十六進位」格式會把二進位資料編碼成每個位元組 2 個十六進位數字，高位的半位元組（nibble）在前。整個字串前面會加上 `\x` 序列（用來與跳脫格式區分）。在某些情況下，開頭的反斜線可能需要以重複兩次的方式來跳脫（請參閱[第 4.1.2.1 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)）。在輸入時，十六進位數字可以是大寫或小寫，而且數字對之間允許空白字元（但數字對內部以及開頭的 `\x` 序列中不允許）。十六進位格式與各式各樣的外部應用程式與通訊協定相容，而且轉換速度通常比跳脫格式快，因此建議優先使用。

範例：

```

SET bytea_output = 'hex';

SELECT '\xDEADBEEF'::bytea;
   bytea
------------
 \xdeadbeef
```

### 8.4.2. `bytea` 跳脫格式 [#](#datatype-binary-bytea-escape-format) <a href="#datatype-binary-bytea-escape-format" id="datatype-binary-bytea-escape-format"></a>

完整內容請見 [8.4.2. bytea 跳脫格式](datatype-binary/datatype-binary-bytea-escape-format.md#datatype-binary-bytea-escape-format)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-binary.html)（原文版本：18.6；核對日期：2026-09-13）
