# 4.1.2. 常數

<a id="SQL-SYNTAX-CONSTANTS"></a>

## 4.1.2. 常數 [#](#sql-syntax-constants) <a href="#sql-syntax-constants" id="sql-syntax-constants"></a>

<a id="id-1.5.3.5.9.2"></a>

PostgreSQL 中有三種*隱含型別的常數*（implicitly-typed constant）：字串、位元字串與數字。常數也可以指定明確的型別，這能讓系統更精確地表示並更有效率地處理它們。以下各小節會討論這些做法。

<a id="SQL-SYNTAX-STRINGS"></a>

### 4.1.2.1. 字串常數 [#](#sql-syntax-strings) <a href="#sql-syntax-strings" id="sql-syntax-strings"></a>

<a id="id-1.5.3.5.9.4.2"></a>

<a id="id-1.5.3.5.9.4.3.1"></a>
SQL 中的字串常數是以單引號（`'`）括住的任意字元序列，例如 `'This is a string'`。要在字串常數中包含單引號字元，請寫兩個相鄰的單引號，例如 `'Dianne''s horse'`。請注意，這與雙引號字元（`"`）*並不*相同。

兩個字串常數之間如果只以*至少包含一個換行*的空白字元分隔，就會被串接起來，實際上等同於將字串寫成一個常數。例如：

```

SELECT 'foo'
'bar';
```

等同於：

```

SELECT 'foobar';
```

但是：

```

SELECT 'foo'      'bar';
```

則不是有效的語法。（這種有點奇怪的行為是 SQL 所規定的；PostgreSQL 遵循標準。）

<a id="SQL-SYNTAX-STRINGS-ESCAPE"></a>

### 4.1.2.2. 使用 C 語言風格跳脫的字串常數 [#](#sql-syntax-strings-escape) <a href="#sql-syntax-strings-escape" id="sql-syntax-strings-escape"></a>

<a id="id-1.5.3.5.9.5.2"></a><a id="id-1.5.3.5.9.5.3"></a>

PostgreSQL 也接受「跳脫」字串常數，這是 SQL 標準的延伸。跳脫字串常數的寫法，是在開頭的單引號之前加上字母 `E`（大寫或小寫），例如 `E'foo'`。（將跳脫字串常數延續到多行時，只要在第一個開頭引號之前寫 `E`。）在跳脫字串中，反斜線字元（`\`）會開始一個類似 C 語言的*反斜線跳脫*（backslash escape）序列，其中反斜線與後續字元的組合代表一個特殊的位元組值，如[表 4.1](#sql-backslash-table) 所示。

<a id="SQL-BACKSLASH-TABLE"></a>

### 表 4.1. 反斜線跳脫序列 [#](#sql-backslash-table) <a href="#sql-backslash-table" id="sql-backslash-table"></a>

<table border="1" class="table" summary="Backslash Escape Sequences"><colgroup><col/><col/></colgroup><thead><tr><th>反斜線跳脫序列</th><th>解讀</th></tr></thead><tbody><tr><td><code class="literal">\b</code></td><td>退格（backspace）</td></tr><tr><td><code class="literal">\f</code></td><td>換頁（form feed）</td></tr><tr><td><code class="literal">\n</code></td><td>換行（newline）</td></tr><tr><td><code class="literal">\r</code></td><td>歸位（carriage return）</td></tr><tr><td><code class="literal">\t</code></td><td>定位字元（tab）</td></tr><tr><td>
<code class="literal">\<em class="replaceable"><code>o</code></em></code>,
         <code class="literal">\<em class="replaceable"><code>oo</code></em></code>,
         <code class="literal">\<em class="replaceable"><code>ooo</code></em></code>
         (<em class="replaceable"><code>o</code></em> = 0–7)
        </td><td>八進位位元組值</td></tr><tr><td>
<code class="literal">\x<em class="replaceable"><code>h</code></em></code>,
         <code class="literal">\x<em class="replaceable"><code>hh</code></em></code>
         (<em class="replaceable"><code>h</code></em> = 0–9, A–F)
        </td><td>十六進位位元組值</td></tr><tr><td>
<code class="literal">\u<em class="replaceable"><code>xxxx</code></em></code>,
         <code class="literal">\U<em class="replaceable"><code>xxxxxxxx</code></em></code>
         (<em class="replaceable"><code>x</code></em> = 0–9, A–F)
        </td><td>16 或 32 位元的十六進位 Unicode 字元值</td></tr></tbody></table>

<br>

反斜線後面接的任何其他字元都會按字面處理。因此，要包含反斜線字元，請寫兩個反斜線（`\\`）。此外，除了一般的 `''` 寫法之外，也可以在跳脫字串中寫 `\'` 來包含單引號。

你有責任確保自己建立的位元組序列（特別是使用八進位或十六進位跳脫時）在伺服器的字元集編碼中組成有效的字元。一個實用的替代做法是使用 Unicode 跳脫或另一種 Unicode 跳脫語法（說明見[第 4.1.2.3 節](#sql-syntax-strings-uescape)）；這樣伺服器就會檢查字元轉換是否可行。

### 警示

如果設定參數 [standard_conforming_strings](../../../server-administration/runtime-config/runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS) 為 `off`，PostgreSQL 會在一般字串常數與跳脫字串常數中都辨識反斜線跳脫。不過從 PostgreSQL 9.1 起，預設值是 `on`，表示只有在跳脫字串常數中才會辨識反斜線跳脫。這種行為比較符合標準，但可能會破壞依賴歷史行為（總是辨識反斜線跳脫）的應用程式。作為權宜之計，你可以將這個參數設為 `off`，但最好還是逐步改掉使用反斜線跳脫的做法。如果你需要使用反斜線跳脫來表示特殊字元，請在字串常數前加上 `E`。

除了 `standard_conforming_strings` 之外，設定參數 [escape_string_warning](../../../server-administration/runtime-config/runtime-config-compatible.md#GUC-ESCAPE-STRING-WARNING) 與 [backslash_quote](../../../server-administration/runtime-config/runtime-config-compatible.md#GUC-BACKSLASH-QUOTE) 也會影響字串常數中反斜線的處理方式。

字串常數中不能包含代碼為零的字元。

<a id="SQL-SYNTAX-STRINGS-UESCAPE"></a>

### 4.1.2.3. 使用 Unicode 跳脫的字串常數 [#](#sql-syntax-strings-uescape) <a href="#sql-syntax-strings-uescape" id="sql-syntax-strings-uescape"></a>

<a id="id-1.5.3.5.9.6.2"></a>

PostgreSQL 也支援另一種字串跳脫語法，可以依碼位指定任意 Unicode 字元。Unicode 跳脫字串常數以 `U&`（大寫或小寫的字母 U 後面接著 & 符號）開頭，緊接在開頭的引號之前，中間不能有任何空格，例如 `U&'foo'`。（請注意，這會與運算子 `&` 產生歧義。在運算子前後加上空格即可避免這個問題。）在引號內，可以用跳脫形式指定 Unicode 字元：寫一個反斜線後接四位數的十六進位碼位數字，或寫一個反斜線後接加號，再接六位數的十六進位碼位數字。例如，字串 `'data'` 可以寫成

```

U&'d\0061t\+000061'
```

下面這個比較不簡單的範例，以西里爾字母寫出俄文單字「slon」（大象）：

```

U&'\0441\043B\043E\043D'
```

如果想使用反斜線以外的跳脫字元，可以在字串之後使用 `UESCAPE`<a id="id-1.5.3.5.9.6.4.2"></a> 子句指定，例如：

```

U&'d!0061t!+000061' UESCAPE '!'
```

跳脫字元可以是十六進位數字、加號、單引號、雙引號或空白字元以外的任何單一字元。

要在字串中按字面包含跳脫字元，請將它寫兩次。

四位數或六位數的跳脫形式都可以用來指定 UTF-16 代理對，以組成碼位大於 U+FFFF 的字元，不過既然有六位數的形式，技術上就不需要這麼做。（代理對不會直接儲存，而是會合併為單一碼位。）

如果伺服器編碼不是 UTF-8，這些跳脫序列所識別的 Unicode 碼位會轉換為實際的伺服器編碼；如果無法轉換，就會回報錯誤。

此外，字串常數的 Unicode 跳脫語法只有在設定參數 [standard_conforming_strings](../../../server-administration/runtime-config/runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS) 開啟時才有作用。這是因為否則這種語法可能會混淆剖析 SQL 陳述式的用戶端，進而可能導致 SQL 注入（SQL injection）等類似的安全問題。如果這個參數設為 off，這種語法會被拒絕並產生錯誤訊息。

<a id="SQL-SYNTAX-DOLLAR-QUOTING"></a>

### 4.1.2.4. 錢號引用的字串常數 [#](#sql-syntax-dollar-quoting) <a href="#sql-syntax-dollar-quoting" id="sql-syntax-dollar-quoting"></a>

<a id="id-1.5.3.5.9.7.2"></a>

雖然指定字串常數的標準語法通常很方便，但當想要的字串包含許多單引號時，就可能變得難以閱讀，因為每個單引號都必須重複寫兩次。為了在這類情況下讓查詢更容易閱讀，PostgreSQL 提供了另一種撰寫字串常數的方式，稱為「錢號引用」（dollar quoting）。錢號引用的字串常數依序由下列部分組成：一個錢號（`$`）、一個由零或多個字元組成的選用「標籤」、另一個錢號、構成字串內容的任意字元序列、一個錢號、與開頭相同的標籤，以及一個錢號。例如，以下是用錢號引用指定字串「Dianne's horse」的兩種不同寫法：

```

$$Dianne's horse$$
$SomeTag$Dianne's horse$SomeTag$
```

請注意，在錢號引用的字串中，單引號不需要跳脫就可以使用。事實上，錢號引用字串中的任何字元都不會被跳脫：字串內容永遠是按字面撰寫的。反斜線不具特殊意義，錢號也一樣，除非它是與開頭標籤相符之序列的一部分。

在每一層巢狀結構選用不同的標籤，就可以將錢號引用的字串常數巢狀使用。這最常用在撰寫函式定義時。例如：

```

$function$
BEGIN
    RETURN ($1 ~ $q$[\t\r\n\v\\]$q$);
END;
$function$
```

在這裡，序列 `$q$[\t\r\n\v\\]$q$` 代表錢號引用的字面字串 `[\t\r\n\v\\]`，它會在 PostgreSQL 執行函式主體時被辨識出來。但由於該序列與外層的錢號引用分隔符號 `$function$` 不相符，對外層字串而言，它只不過是常數中的其他字元而已。

錢號引用字串的標籤（如果有的話）遵循與未加引號識別字相同的規則，只是不能包含錢號。標籤會區分大小寫，因此 `$tag$String content$tag$` 是正確的，但 `$TAG$String content$tag$` 則不是。

緊接在關鍵字或識別字之後的錢號引用字串，必須以空白字元與之分隔；否則錢號引用的分隔符號會被當作前面識別字的一部分。

錢號引用不是 SQL 標準的一部分，但它通常是比符合標準的單引號語法更方便撰寫複雜字串字面值的方式。在其他常數中表示字串常數時特別有用，這在程序式函式定義中經常需要。如果使用單引號語法，上例中的每個反斜線都必須寫成四個反斜線；在剖析原本的字串常數時會簡化為兩個，接著在函式執行期間重新剖析內層字串常數時，再簡化為一個。

<a id="SQL-SYNTAX-BIT-STRINGS"></a>

### 4.1.2.5. 位元字串常數 [#](#sql-syntax-bit-strings) <a href="#sql-syntax-bit-strings" id="sql-syntax-bit-strings"></a>

<a id="id-1.5.3.5.9.8.2"></a>

位元字串常數看起來就像一般的字串常數，只是在開頭引號之前緊接著一個 `B`（大寫或小寫，中間沒有空白），例如 `B'1001'`。位元字串常數中唯一允許的字元是 `0` 與 `1`。

另外，位元字串常數也可以用十六進位表示法指定，以 `X`（大寫或小寫）開頭，例如 `X'1FF'`。這種表示法等同於每個十六進位數字對應四個二進位數字的位元字串常數。

這兩種形式的位元字串常數，都可以用與一般字串常數相同的方式延續到多行。位元字串常數中不能使用錢號引用。

<a id="SQL-SYNTAX-CONSTANTS-NUMERIC"></a>

### 4.1.2.6. 數值常數 [#](#sql-syntax-constants-numeric) <a href="#sql-syntax-constants-numeric" id="sql-syntax-constants-numeric"></a>

<a id="id-1.5.3.5.9.9.2"></a>

數值常數可以採用下列一般形式：

```

digits
digits.[digits][e[+-]digits]
[digits].digits[e[+-]digits]
digitse[+-]digits
```

其中 *`digits`* 是一個或多個十進位數字（0 到 9）。如果使用小數點，小數點之前或之後至少必須有一個數字。如果有指數標記（`e`），其後至少必須有一個數字。常數中不能嵌入任何空格或其他字元，但可以使用底線來做視覺上的分組，說明如下。請注意，任何前置的正號或負號實際上都不被視為常數的一部分；它是套用在常數上的運算子。

以下是一些有效數值常數的範例：

<br>
42<br>
3.5<br>
4.<br>
.001<br>
5e2<br>
1.925e-3<br>

此外，也接受下列形式的非十進位整數常數：

```

0xhexdigits
0ooctdigits
0bbindigits
```

其中 *`hexdigits`* 是一個或多個十六進位數字（0-9、A-F），*`octdigits`* 是一個或多個八進位數字（0-7），而 *`bindigits`* 是一個或多個二進位數字（0 或 1）。十六進位數字與進位前綴可以是大寫或小寫。請注意，只有整數可以使用非十進位的形式，帶有小數部分的數字則不行。

以下是一些有效非十進位整數常數的範例：

<br>
0b100101<br>
0B10011001<br>
0o273<br>
0O755<br>
0x42f<br>
0XFFFF<br>

為了視覺上的分組，可以在數字之間插入底線。底線對常數的值沒有任何其他影響。例如：

<br>
1_500_000_000<br>
0b10001000_00000000<br>
0o_1_755<br>
0xFFFF_FFFF<br>
1.618_034<br>

數值常數或數字群組的開頭或結尾（也就是緊接在小數點或指數標記之前或之後）不允許出現底線，也不允許連續出現多個底線。

<a id="id-1.5.3.5.9.9.8.1"></a>
<a id="id-1.5.3.5.9.9.8.2"></a>
<a id="id-1.5.3.5.9.9.8.3"></a>
不包含小數點也不包含指數的數值常數，如果其值能放入 `integer` 型別（32 位元），一開始會被假定為 `integer` 型別；否則，如果其值能放入 `bigint` 型別（64 位元），就會被假定為 `bigint` 型別；否則會被視為 `numeric` 型別。包含小數點或指數的常數，一開始一律被假定為 `numeric` 型別。

數值常數最初被指派的資料型別，只是型別解析演算法的起點。在大多數情況下，常數會依情境自動轉換為最適當的型別。必要時，你可以透過型別轉換，強制將數值解讀為特定的資料型別。<a id="id-1.5.3.5.9.9.9.1"></a>例如，你可以這樣寫，強制將數值當作 `real`（`float4`）型別處理：

```

REAL '1.23'  -- string style
1.23::REAL   -- PostgreSQL (historical) style
```

這些其實只是接下來要討論的一般型別轉換表示法的特例。

<a id="SQL-SYNTAX-CONSTANTS-GENERIC"></a>

### 4.1.2.7. 其他型別的常數 [#](#sql-syntax-constants-generic) <a href="#sql-syntax-constants-generic" id="sql-syntax-constants-generic"></a>

<a id="id-1.5.3.5.9.10.2"></a>

*任意*型別的常數都可以使用下列任一種表示法輸入：

```

type 'string'
'string'::type
CAST ( 'string' AS type )
```

字串常數的文字會傳給名為 *`type`* 之型別的輸入轉換程序。結果是所指定型別的常數。如果常數必須是什麼型別沒有歧義（例如，直接指派給資料表欄位時），就可以省略明確的型別轉換，此時常數會自動轉換。

字串常數可以使用一般的 SQL 表示法或錢號引用來撰寫。

也可以使用類似函式的語法來指定型別轉換：

```

typename ( 'string' )
```

但並不是所有型別名稱都能以這種方式使用；詳情請參閱[第 4.2.9 節](../sql-expressions.md#sql-syntax-type-casts)。

`::`、`CAST()` 與函式呼叫語法，也可以用來指定任意運算式在執行期間的型別轉換，如[第 4.2.9 節](../sql-expressions.md#sql-syntax-type-casts)所述。為了避免語法上的歧義，`type 'string'` 語法只能用來指定簡單字面常數的型別。`type 'string'` 語法的另一個限制是它不適用於陣列型別；請使用 `::` 或 `CAST()` 來指定陣列常數的型別。

`CAST()` 語法符合 SQL 標準。`type 'string'` 語法則是標準的一般化：SQL 只為少數幾種資料型別規定了這種語法，但 PostgreSQL 允許所有型別使用。使用 `::` 的語法是 PostgreSQL 的歷史用法，函式呼叫語法也是。

[返回 4.1. 詞彙結構](../sql-syntax-lexical.md#sql-syntax-lexical)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-syntax-lexical.html)（原文版本：18.6；核對日期：2026-09-11）
