<a id="DATATYPE-BINARY"></a>

## 8.4. 二進位資料型別 [#](#DATATYPE-BINARY)

[8.4.1. `bytea` 十六進位格式](datatype-binary.md#DATATYPE-BINARY-BYTEA-HEX-FORMAT)

[8.4.2. `bytea` 跳脫格式](datatype-binary.md#DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT)

<a id="id-1.5.7.12.2"></a><a id="id-1.5.7.12.3"></a>

`bytea` 資料型別可以用來儲存二進位字串；請參閱[表 8.6](datatype-binary.md#DATATYPE-BINARY-TABLE)。

<a id="DATATYPE-BINARY-TABLE"></a>

**表 8.6. 二進位資料型別**

<table border="1" class="table" summary="二進位資料型別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>名稱</th><th>儲存空間大小</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">bytea</code></td><td>1 或 4 個位元組加上實際的二進位字串</td><td>可變長度的二進位字串</td></tr></tbody></table>

<br>

二進位字串是由一連串的位元組（octet，或稱 byte）所組成。二進位字串與字元字串有兩點不同。第一，二進位字串明確允許儲存值為零的位元組，以及其他「不可列印」的位元組（通常是十進位 32 到 126 範圍之外的位元組）。字元字串不允許零位元組，也不允許任何其他依資料庫所選用的字元集編碼而言屬於無效的位元組值與位元組值序列。第二，對二進位字串的操作處理的是實際的位元組，而字元字串的處理則取決於語系設定。簡而言之，二進位字串適合用來儲存程式設計者視為「原始位元組」的資料，而字元字串則適合用來儲存文字。

`bytea` 型別的輸入與輸出支援兩種格式：「十六進位」格式，以及 PostgreSQL 沿用已久的「跳脫」格式。這兩種格式在輸入時一律都會被接受。輸出格式則取決於組態參數 [bytea_output](../../server-administration/runtime-config/runtime-config-client.md#GUC-BYTEA-OUTPUT)，預設值是十六進位。（請注意，十六進位格式是在 PostgreSQL 9.0 引入的；較早的版本與某些工具並不認得它。）

SQL 標準定義了另一種不同的二進位字串型別，稱為 `BLOB` 或 `BINARY LARGE OBJECT`。其輸入格式與 `bytea` 不同，但所提供的函式與運算子則大致相同。

<a id="DATATYPE-BINARY-BYTEA-HEX-FORMAT"></a>

### 8.4.1. `bytea` 十六進位格式 [#](#DATATYPE-BINARY-BYTEA-HEX-FORMAT)

「十六進位」格式會把二進位資料編碼成每個位元組 2 個十六進位數字，高位的半位元組（nibble）在前。整個字串前面會加上 `\x` 序列（用來與跳脫格式區分）。在某些情況下，開頭的反斜線可能需要以重複兩次的方式來跳脫（請參閱[第 4.1.2.1 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)）。在輸入時，十六進位數字可以是大寫或小寫，而且數字對之間允許空白字元（但數字對內部以及開頭的 `\x` 序列中不允許）。十六進位格式與各式各樣的外部應用程式與通訊協定相容，而且轉換速度通常比跳脫格式快，因此建議優先使用。

範例：

```

SET bytea_output = 'hex';

SELECT '\xDEADBEEF'::bytea;
   bytea
------------
 \xdeadbeef
```

<a id="DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT"></a>

### 8.4.2. `bytea` 跳脫格式 [#](#DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT)

「跳脫」格式是 PostgreSQL 對 `bytea` 型別的傳統格式。它採取的做法是把二進位字串表示成一連串的 ASCII 字元，同時把那些無法以 ASCII 字元表示的位元組轉換成特殊的跳脫序列。如果從應用程式的角度來看，把位元組表示成字元是合理的，那麼這種表示法可能會很方便。但實務上它通常令人困惑，因為它模糊了二進位字串與字元字串之間的區別，而且所選用的那套跳脫機制也有些笨拙。因此，大多數新的應用程式大概都應該避免使用這種格式。

以跳脫格式輸入 `bytea` 值時，某些值的位元組*必須*跳脫，而所有位元組值都*可以*跳脫。一般而言，要跳脫一個位元組，就把它轉換成三位數的八進位值，並在前面加上一個反斜線。反斜線本身（十進位位元組值 92）也可以改用兩個反斜線來表示。[表 8.7](datatype-binary.md#DATATYPE-BINARY-SQLESC) 列出必須跳脫的字元，並在適用時給出可替代的跳脫序列。

<a id="DATATYPE-BINARY-SQLESC"></a>

**表 8.7. `bytea` 常數中的跳脫位元組**

<table border="1" class="table" summary="bytea 常數中的跳脫位元組"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/></colgroup><thead><tr><th>十進位位元組值</th><th>說明</th><th>跳脫後的輸入表示法</th><th>範例</th><th>十六進位表示法</th></tr></thead><tbody><tr><td>0</td><td>零位元組</td><td><code class="literal">'\000'</code></td><td><code class="literal">'\000'::bytea</code></td><td><code class="literal">\x00</code></td></tr><tr><td>39</td><td>單引號</td><td><code class="literal">''''</code> 或 <code class="literal">'\047'</code></td><td><code class="literal">''''::bytea</code></td><td><code class="literal">\x27</code></td></tr><tr><td>92</td><td>反斜線</td><td><code class="literal">'\\'</code> 或 <code class="literal">'\134'</code></td><td><code class="literal">'\\'::bytea</code></td><td><code class="literal">\x5c</code></td></tr><tr><td>0 到 31 以及 127 到 255</td><td><span class="quote">「<span class="quote">不可列印</span>」</span>的位元組</td><td><code class="literal">'\<em class="replaceable"><code>xxx'</code></em></code>（八進位值）</td><td><code class="literal">'\001'::bytea</code></td><td><code class="literal">\x01</code></td></tr></tbody></table>

<br>

*不可列印*位元組是否必須跳脫，會因語系設定而異。在某些情況下，你可以不跳脫它們也沒問題。

如同[表 8.7](datatype-binary.md#DATATYPE-BINARY-SQLESC) 所示，單引號必須重複兩次的原因在於：這對 SQL 指令中的任何字串常數都成立。一般性的字串常數剖析器會消耗掉最外層的單引號，並把每一對單引號縮減成一個資料字元。`bytea` 輸入函式所看到的就只是一個單引號，而它會把那個單引號當成一般的資料字元。不過，`bytea` 輸入函式會把反斜線視為特殊字元，而[表 8.7](datatype-binary.md#DATATYPE-BINARY-SQLESC) 中所示的其他行為都是由該函式所實作的。

在某些情況下，反斜線必須比上面所示的再多重複一次，因為一般性的字串常數剖析器也會把每一對反斜線縮減成一個資料字元；請參閱[第 4.1.2.1 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)。

`Bytea` 的位元組預設會以 `hex` 格式輸出。如果你把 [bytea_output](../../server-administration/runtime-config/runtime-config-client.md#GUC-BYTEA-OUTPUT) 改成 `escape`，「不可列印」的位元組會被轉換成等價的三位數八進位值，並在前面加上一個反斜線。大多數「可列印」的位元組則會以它們在用戶端字元集中的標準表示法輸出，例如：

```

SET bytea_output = 'escape';

SELECT 'abc \153\154\155 \052\251\124'::bytea;
     bytea
----------------
 abc klm *\251T
```

十進位值為 92 的位元組（反斜線）在輸出時會重複兩次。細節請參閱[表 8.8](datatype-binary.md#DATATYPE-BINARY-RESESC)。

<a id="DATATYPE-BINARY-RESESC"></a>

**表 8.8. `bytea` 輸出的跳脫位元組**

<table border="1" class="table" summary="bytea 輸出的跳脫位元組"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/></colgroup><thead><tr><th>十進位位元組值</th><th>說明</th><th>跳脫後的輸出表示法</th><th>範例</th><th>輸出結果</th></tr></thead><tbody><tr><td>92</td><td>反斜線</td><td><code class="literal">\\</code></td><td><code class="literal">'\134'::bytea</code></td><td><code class="literal">\\</code></td></tr><tr><td>0 到 31 以及 127 到 255</td><td><span class="quote">「<span class="quote">不可列印</span>」</span>的位元組</td><td><code class="literal">\<em class="replaceable"><code>xxx</code></em></code>（八進位值）</td><td><code class="literal">'\001'::bytea</code></td><td><code class="literal">\001</code></td></tr><tr><td>32 至 126</td><td><span class="quote">「<span class="quote">可列印</span>」</span>的位元組</td><td>用戶端字元集的表示法</td><td><code class="literal">'\176'::bytea</code></td><td><code class="literal">~</code></td></tr></tbody></table>

<br>

視你所使用的 PostgreSQL 前端而定，在跳脫與還原 `bytea` 字串方面你可能還得多做一些工作。例如，如果你的介面會自動轉換換行字元與歸位字元，你可能也必須把它們跳脫。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-binary.html)（原文版本：18.6；核對日期：2026-09-13）
