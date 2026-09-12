<a id="FUNCTIONS-MATCHING"></a>

## 9.7. 模式比對 [#](#FUNCTIONS-MATCHING)

[9.7.1. `LIKE`](functions-matching.md#FUNCTIONS-LIKE)

[9.7.2. `SIMILAR TO` 正規表示式](functions-matching.md#FUNCTIONS-SIMILARTO-REGEXP)

[9.7.3. POSIX 正規表示式](functions-matching.md#FUNCTIONS-POSIX-REGEXP)

<a id="id-1.5.8.13.2"></a>

PostgreSQL 提供了三種不同的模式比對方式：傳統的 SQL `LIKE` 運算子、較新的 `SIMILAR TO` 運算子（於 SQL:1999 加入），以及 POSIX 風格的正規表示式。除了基本的「這個字串是否符合這個模式？」運算子之外，也有函式可用來擷取或替換符合的子字串，以及在符合的位置分割字串。

### 提示

如果你的模式比對需求超出這些範圍，可以考慮以 Perl 或 Tcl 撰寫使用者自訂函式。

### 警示

雖然大多數正規表示式搜尋都能非常快速地執行，但也可能刻意構造出需要任意長時間與任意大量記憶體才能處理的正規表示式。對於接受來自不友善來源的正規表示式搜尋模式，務必謹慎。如果非這麼做不可，建議設定陳述句逾時（statement timeout）。

使用 `SIMILAR TO` 模式的搜尋也有相同的安全風險，因為 `SIMILAR TO` 提供了許多與 POSIX 風格正規表示式相同的功能。

`LIKE` 搜尋比其他兩種選擇簡單得多，因此在模式來源可能不友善時使用較為安全。

`SIMILAR TO` 與 POSIX 風格的正規表示式不支援非決定性定序（nondeterministic collation）。如有需要，請改用 `LIKE`，或對運算式套用不同的定序來避開這項限制。

<a id="FUNCTIONS-LIKE"></a>

### 9.7.1. `LIKE` [#](#FUNCTIONS-LIKE)

<a id="id-1.5.8.13.7.2"></a>

```

string LIKE pattern [ESCAPE escape-character]
string NOT LIKE pattern [ESCAPE escape-character]
```

如果 *`string`* 符合所提供的 *`pattern`*，`LIKE` 運算式就會回傳 true。（如同預期，如果 `LIKE` 回傳 true，`NOT LIKE` 運算式就會回傳 false，反之亦然。等效的運算式為 `NOT (string LIKE pattern)`。）

如果 *`pattern`* 不包含百分比符號或底線，那麼該模式就只代表字串本身；在這種情況下，`LIKE` 的作用就如同等號運算子。*`pattern`* 中的底線（`_`）代表（符合）任何單一字元；百分比符號（`%`）則符合零個或多個字元的任意序列。

一些範例：

```

'abc' LIKE 'abc'    true
'abc' LIKE 'a%'     true
'abc' LIKE '_b_'    true
'abc' LIKE 'c'      false
```

`LIKE` 模式比對支援非決定性定序（請參閱[第 23.2.2.4 節](../../server-administration/charset/collation.md#COLLATION-NONDETERMINISTIC)），例如不區分大小寫的定序，或是會忽略標點符號之類的定序。因此，使用不區分大小寫的定序時，可以得到：

```

'AbC' LIKE 'abc' COLLATE case_insensitive    true
'AbC' LIKE 'a%' COLLATE case_insensitive     true
```

若使用會忽略某些字元的定序，或者一般而言會將不同長度的字串視為相等的定序，語意可能會變得稍微複雜一些。請看以下範例：

```

'.foo.' LIKE 'foo' COLLATE ign_punct    true
'.foo.' LIKE 'f_o' COLLATE ign_punct    true
'.foo.' LIKE '_oo' COLLATE ign_punct    false
```

比對的運作方式是：模式會被切分為萬用字元與非萬用字元字串的序列（萬用字元為 `_` 與 `%`）。例如，模式 `f_o` 會被切分為 `f, _, o`，模式 `_oo` 會被切分為 `_, oo`。如果輸入字串能以某種方式切分，使得萬用字元分別符合一個字元或任意數量的字元，而非萬用字元的部分在適用的定序下相等，那麼輸入字串就符合該模式。因此，舉例來說，`'.foo.' LIKE 'f_o' COLLATE ign_punct` 為 true，因為可以將 `.foo.` 切分為 `.f, o, o.`，然後 `'.f' = 'f' COLLATE ign_punct`、`'o'` 符合萬用字元 `_`，且 `'o.' = 'o' COLLATE ign_punct`。但 `'.foo.' LIKE '_oo' COLLATE ign_punct` 為 false，因為 `.foo.` 無法以「第一個字元為任意字元，而字串其餘部分與 `oo` 比較相等」的方式切分。（請注意，單一字元萬用字元總是恰好符合一個字元，與定序無關。因此在這個範例中，`_` 會符合 `.`，但接下來輸入字串的其餘部分就無法符合模式的其餘部分。）

`LIKE` 模式比對總是涵蓋整個字串。因此，如果希望比對字串內任何位置的序列，模式就必須以百分比符號開頭並以百分比符號結尾。

若要比對字面上的底線或百分比符號，而不比對其他字元，*`pattern`* 中對應的字元前面必須加上跳脫字元。預設的跳脫字元是反斜線，但可以使用 `ESCAPE` 子句選擇其他字元。若要比對跳脫字元本身，請寫兩個跳脫字元。

### 注意

如果你關閉了 [standard_conforming_strings](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS)，你在字面字串常數中寫的所有反斜線都需要重複寫兩次。詳情請參閱[第 4.1.2.1 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)。

也可以寫成 `ESCAPE ''` 來不選擇任何跳脫字元。這實際上會停用跳脫機制，使得無法關閉模式中底線與百分比符號的特殊意義。

根據 SQL 標準，省略 `ESCAPE` 表示沒有跳脫字元（而不是預設為反斜線），而且不允許長度為零的 `ESCAPE` 值。因此，PostgreSQL 在這方面的行為略微不符合標準。

可以使用關鍵字 `ILIKE` 取代 `LIKE`，依照目前作用中的語系進行不區分大小寫的比對。（但這不支援非決定性定序。）這不在 SQL 標準中，而是 PostgreSQL 的延伸功能。

運算子 `~~` 等同於 `LIKE`，而 `~~*` 對應於 `ILIKE`。另外還有 `!~~` 與 `!~~*` 運算子，分別代表 `NOT LIKE` 與 `NOT ILIKE`。這些運算子都是 PostgreSQL 特有的。你可能會在 `EXPLAIN` 輸出及類似的地方看到這些運算子名稱，因為剖析器實際上會將 `LIKE` 等轉譯為這些運算子。

在 PostgreSQL 語法中，`LIKE`、`ILIKE`、`NOT LIKE` 與 `NOT ILIKE` 這些片語一般被視為運算子；例如，它們可以用在 *`expression`* *`operator`* ANY (*`subquery`*) 建構中，不過其中不能包含 `ESCAPE` 子句。在某些少見的情況下，可能需要改用底層的運算子名稱。

另請參閱「開頭為」（starts-with）運算子 `^@` 及對應的 `starts_with()` 函式，在只需要比對字串開頭的情況下，它們很有用。

<a id="FUNCTIONS-SIMILARTO-REGEXP"></a>

### 9.7.2. `SIMILAR TO` 正規表示式 [#](#FUNCTIONS-SIMILARTO-REGEXP)

<a id="id-1.5.8.13.8.2"></a><a id="id-1.5.8.13.8.3"></a><a id="id-1.5.8.13.8.4"></a>

```

string SIMILAR TO pattern [ESCAPE escape-character]
string NOT SIMILAR TO pattern [ESCAPE escape-character]
```

`SIMILAR TO` 運算子會依據其模式是否符合給定的字串，回傳 true 或 false。它與 `LIKE` 類似，差別在於它使用 SQL 標準對正規表示式的定義來解讀模式。SQL 正規表示式是 `LIKE` 表示法與一般（POSIX）正規表示式表示法之間一種奇特的混合體。

與 `LIKE` 相同，`SIMILAR TO` 運算子只有在其模式符合整個字串時才會成功；這與一般正規表示式的行為不同，後者的模式可以符合字串的任何部分。同樣與 `LIKE` 一樣，`SIMILAR TO` 使用 `_` 與 `%` 作為萬用字元，分別代表任何單一字元與任何字串（它們相當於 POSIX 正規表示式中的 `.` 與 `.*`）。

除了這些借自 `LIKE` 的功能之外，`SIMILAR TO` 還支援以下借自 POSIX 正規表示式的模式比對元字元：

* `|` 表示擇一（兩個選項中的任一個）。
* `*` 表示前一個項目重複零次或多次。
* `+` 表示前一個項目重複一次或多次。
* `?` 表示前一個項目重複零次或一次。
* `{`*`m`*`}` 表示前一個項目恰好重複 *`m`* 次。
* `{`*`m`*`,}` 表示前一個項目重複 *`m`* 次或更多次。
* `{`*`m`*`,`*`n`*`}` 表示前一個項目重複至少 *`m`* 次且不超過 *`n`* 次。
* 括號 `()` 可用來將多個項目組合成單一的邏輯項目。
* 方括號運算式 `[...]` 指定一個字元類別，就如同在 POSIX 正規表示式中一樣。

請注意，句點（`.`）對 `SIMILAR TO` 而言不是元字元。

與 `LIKE` 一樣，反斜線會停用這些元字元的特殊意義。可以使用 `ESCAPE` 指定不同的跳脫字元，或者寫成 `ESCAPE ''` 來停用跳脫功能。

根據 SQL 標準，省略 `ESCAPE` 表示沒有跳脫字元（而不是預設為反斜線），而且不允許長度為零的 `ESCAPE` 值。因此，PostgreSQL 在這方面的行為略微不符合標準。

另一項非標準的延伸是：在跳脫字元後面接一個字母或數字，就可以使用為 POSIX 正規表示式定義的跳脫序列；請參閱下方的[表 9.20](functions-matching.md#POSIX-CHARACTER-ENTRY-ESCAPES-TABLE)、[表 9.21](functions-matching.md#POSIX-CLASS-SHORTHAND-ESCAPES-TABLE) 與[表 9.22](functions-matching.md#POSIX-CONSTRAINT-ESCAPES-TABLE)。

一些範例：

```

'abc' SIMILAR TO 'abc'          true
'abc' SIMILAR TO 'a'            false
'abc' SIMILAR TO '%(b|d)%'      true
'abc' SIMILAR TO '(b|c)%'       false
'-abc-' SIMILAR TO '%\mabc\M%'  true
'xabcy' SIMILAR TO '%\mabc\M%'  false
```

具有三個參數的 `substring` 函式，可擷取符合 SQL 正規表示式模式的子字串。這個函式可以依照標準 SQL 語法撰寫：

```

substring(string similar pattern escape escape-character)
```

或是使用現已過時的 SQL:1999 語法：

```

substring(string from pattern for escape-character)
```

或是寫成一般的三引數函式：

```

substring(string, pattern, escape-character)
```

與 `SIMILAR TO` 一樣，指定的模式必須符合整個資料字串，否則函式就會失敗並回傳 NULL。為了指出模式中哪個部分所符合的資料子字串是我們感興趣的，模式中應該包含兩個「跳脫字元後接雙引號（`"`）」的組合。比對成功時，會回傳符合這兩個分隔符號之間模式部分的文字。

這種「跳脫字元加雙引號」的分隔符號，實際上會將 `substring` 的模式分成三個獨立的正規表示式；例如，三個區段中任何一個區段裡的直線符號（`|`）只會影響該區段。此外，當資料字串的哪一部分符合哪個模式有歧義時，第一個與第三個正規表示式會被定義為符合最少量的文字，而不是最多量的文字。（以 POSIX 的說法，第一個與第三個正規表示式被強制為非貪婪的。）

作為 SQL 標準的延伸，PostgreSQL 允許只有一個「跳脫字元加雙引號」分隔符號，此時第三個正規表示式會被視為空的；或是完全沒有分隔符號，此時第一個與第三個正規表示式都會被視為空的。

一些範例，以 `#"` 界定回傳字串：

```

substring('foobar' similar '%#"o_b#"%' escape '#')   oob
substring('foobar' similar '#"o_b#"%' escape '#')    NULL
```

<a id="FUNCTIONS-POSIX-REGEXP"></a>

### 9.7.3. POSIX 正規表示式 [#](#FUNCTIONS-POSIX-REGEXP)

<a id="id-1.5.8.13.9.2"></a><a id="id-1.5.8.13.9.3"></a><a id="id-1.5.8.13.9.4"></a><a id="id-1.5.8.13.9.5"></a><a id="id-1.5.8.13.9.6"></a><a id="id-1.5.8.13.9.7"></a><a id="id-1.5.8.13.9.8"></a><a id="id-1.5.8.13.9.9"></a><a id="id-1.5.8.13.9.10"></a><a id="id-1.5.8.13.9.11"></a><a id="id-1.5.8.13.9.12"></a>

[表 9.16](functions-matching.md#FUNCTIONS-POSIX-TABLE) 列出了使用 POSIX 正規表示式進行模式比對時可用的運算子。

<a id="FUNCTIONS-POSIX-TABLE"></a>

**表 9.16. 正規表示式比對運算子**

<table border="1" class="table" summary="Regular Expression Match Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">~</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        字串符合正規表示式，區分大小寫
       </p>
<p>
<code class="literal">'thomas' ~ 't.*ma'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">~*</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        字串符合正規表示式，不區分大小寫
       </p>
<p>
<code class="literal">'thomas' ~* 'T.*ma'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">!~</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        字串不符合正規表示式，區分大小寫
       </p>
<p>
<code class="literal">'thomas' !~ 't.*max'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">text</code> <code class="literal">!~*</code> <code class="type">text</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        字串不符合正規表示式，不區分大小寫
       </p>
<p>
<code class="literal">'thomas' !~* 'T.*ma'</code>
        → <code class="returnvalue">f</code>
</p></td></tr></tbody></table>

<br>

POSIX 正規表示式提供了比 `LIKE` 與 `SIMILAR TO` 運算子更強大的模式比對方法。許多 Unix 工具，例如 `egrep`、`sed` 或 `awk`，都使用與這裡所述類似的模式比對語言。

正規表示式是一個字元序列，它是一組字串（一個*正規集合*（regular set））的簡略定義。如果一個字串是某個正規表示式所描述之正規集合的成員，就稱該字串符合這個正規表示式。與 `LIKE` 一樣，除非模式字元是正規表示式語言中的特殊字元，否則模式字元會與字串字元完全相符——但正規表示式使用的特殊字元與 `LIKE` 不同。與 `LIKE` 模式不同的是，正規表示式可以符合字串內的任何位置，除非該正規表示式明確地錨定在字串的開頭或結尾。

一些範例：

```

'abcd' ~ 'bc'     true
'abcd' ~ 'a.c'    true — dot matches any character
'abcd' ~ 'a.*d'   true — * repeats the preceding pattern item
'abcd' ~ '(b|x)'  true — | means OR, parentheses group
'abcd' ~ '^a'     true — ^ anchors to start of string
'abcd' ~ '^(b|c)' false — would match except for anchoring
```

POSIX 模式語言會在下方更詳細地說明。

具有兩個參數的 `substring` 函式，`substring(string from pattern)`，可擷取符合 POSIX 正規表示式模式的子字串。如果沒有符合，它會回傳 NULL；否則回傳文字中第一個符合模式的部分。但如果模式包含任何括號，則會回傳符合第一個括號子運算式（左括號最先出現的那一個）的文字部分。如果你想在運算式中使用括號而又不觸發這項例外，可以在整個運算式外面加上括號。如果你需要在要擷取的子運算式之前的模式中使用括號，請參閱下方所述的非擷取括號。

一些範例：

```

substring('foobar' from 'o.b')     oob
substring('foobar' from 'o(.)b')   o
```

`regexp_count` 函式會計算 POSIX 正規表示式模式在字串中符合的位置數量。其語法為 `regexp_count`(*`string`*, *`pattern`* [, *`start`* [, *`flags`* ]])。*`pattern`* 會在 *`string`* 中搜尋，通常從字串的開頭開始，但如果提供了 *`start`* 參數，就從該字元索引開始。*`flags`* 參數是一個選用的文字字串，包含零個或多個會改變函式行為的單字母旗標。例如，在 *`flags`* 中包含 `i` 表示進行不區分大小寫的比對。支援的旗標說明於[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)。

一些範例：

```

regexp_count('ABCABCAXYaxy', 'A.')          3
regexp_count('ABCABCAXYaxy', 'A.', 1, 'i')  4
```

`regexp_instr` 函式會回傳 POSIX 正規表示式模式在字串中第 *`N`* 次符合的開始或結束位置；如果沒有這樣的符合則回傳零。其語法為 `regexp_instr`(*`string`*, *`pattern`* [, *`start`* [, *`N`* [, *`endoption`* [, *`flags`* [, *`subexpr`* ]]]]])。*`pattern`* 會在 *`string`* 中搜尋，通常從字串的開頭開始，但如果提供了 *`start`* 參數，就從該字元索引開始。如果指定了 *`N`*，就會找出模式的第 *`N`* 次符合，否則找出第一次符合。如果省略 *`endoption`* 參數或將其指定為零，函式會回傳符合部分第一個字元的位置。否則，*`endoption`* 必須為一，函式會回傳符合部分之後那個字元的位置。*`flags`* 參數是一個選用的文字字串，包含零個或多個會改變函式行為的單字母旗標。支援的旗標說明於[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)。對於包含括號子運算式的模式，*`subexpr`* 是一個整數，指出感興趣的是哪一個子運算式：結果會指出符合該子運算式之子字串的位置。子運算式依其左括號出現的順序編號。當 *`subexpr`* 省略或為零時，結果會指出整個符合部分的位置，不論是否有括號子運算式。

一些範例：

```

regexp_instr('number of your street, town zip, FR', '[^,]+', 1, 2)
                                   23
regexp_instr(string=>'ABCDEFGHI', pattern=>'(c..)(...)', start=>1, "N"=>1, endoption=>0, flags=>'i', subexpr=>2)
                                   6
```

`regexp_like` 函式會檢查字串中是否出現 POSIX 正規表示式模式的符合，回傳布林值 true 或 false。其語法為 `regexp_like`(*`string`*, *`pattern`* [, *`flags`* ])。*`flags`* 參數是一個選用的文字字串，包含零個或多個會改變函式行為的單字母旗標。支援的旗標說明於[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)。如果沒有指定旗標，這個函式的結果與 `~` 運算子相同。如果只指定了 `i` 旗標，其結果與 `~*` 運算子相同。

一些範例：

```

regexp_like('Hello World', 'world')       false
regexp_like('Hello World', 'world', 'i')  true
```

`regexp_match` 函式會回傳一個文字陣列，內容為 POSIX 正規表示式模式在字串中第一次符合時所符合的子字串。其語法為 `regexp_match`(*`string`*, *`pattern`* [, *`flags`* ])。如果沒有符合，結果為 `NULL`。如果找到符合，且 *`pattern`* 不含括號子運算式，則結果為單一元素的文字陣列，包含符合整個模式的子字串。如果找到符合，且 *`pattern`* 包含括號子運算式，則結果為一個文字陣列，其第 *`n`* 個元素是符合 *`pattern`* 第 *`n`* 個括號子運算式的子字串（不計入「非擷取」括號；詳情請見下文）。*`flags`* 參數是一個選用的文字字串，包含零個或多個會改變函式行為的單字母旗標。支援的旗標說明於[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)。

一些範例：

```

SELECT regexp_match('foobarbequebaz', 'bar.*que');
 regexp_match
--------------
 {barbeque}
(1 row)

SELECT regexp_match('foobarbequebaz', '(bar)(beque)');
 regexp_match
--------------
 {bar,beque}
(1 row)
```

### 提示

在常見的情況下，如果你只想要整個符合的子字串，或在沒有符合時得到 `NULL`，最好的做法是使用 `regexp_substr()`。不過，`regexp_substr()` 只存在於 PostgreSQL 15 版及以後的版本。在較舊的版本中，可以擷取 `regexp_match()` 結果的第一個元素，例如：

```

SELECT (regexp_match('foobarbequebaz', 'bar.*que'))[1];
 regexp_match
--------------
 barbeque
(1 row)
```

`regexp_matches` 函式會回傳一組文字陣列，內容為 POSIX 正規表示式模式在字串中各次符合時所符合的子字串。其語法與 `regexp_match` 相同。如果沒有符合，這個函式不會回傳任何資料列；如果有符合且未指定 `g` 旗標，回傳一列；如果有 *`N`* 次符合且指定了 `g` 旗標，則回傳 *`N`* 列。每一個回傳的資料列都是一個文字陣列，包含整個符合的子字串，或是符合 *`pattern`* 中括號子運算式的各個子字串，就如同上面對 `regexp_match` 的說明。`regexp_matches` 接受[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE) 中所列的所有旗標，另外還有 `g` 旗標，指示它回傳所有的符合，而不只是第一個。

一些範例：

```

SELECT regexp_matches('foo', 'not there');
 regexp_matches
----------------
(0 rows)

SELECT regexp_matches('foobarbequebazilbarfbonk', '(b[^b]+)(b[^b]+)', 'g');
 regexp_matches
----------------
 {bar,beque}
 {bazil,barf}
(2 rows)
```

### 提示

在大多數情況下，`regexp_matches()` 應該搭配 `g` 旗標使用，因為如果你只想要第一個符合，使用 `regexp_match()` 會更簡單也更有效率。不過，`regexp_match()` 只存在於 PostgreSQL 10 版及以後的版本。在較舊的版本中，一個常見的技巧是將 `regexp_matches()` 呼叫放在子查詢（sub-select）中，例如：

```

SELECT col1, (SELECT regexp_matches(col2, '(bar)(beque)')) FROM tab;
```

如果有符合，這會產生一個文字陣列；如果沒有則產生 `NULL`，與 `regexp_match()` 的做法相同。如果沒有使用子查詢，對於沒有符合的資料表資料列，這個查詢將完全不會產生任何輸出，而這通常不是我們想要的行為。

`regexp_replace` 函式可將符合 POSIX 正規表示式模式的子字串替換為新的文字。其語法為 `regexp_replace`(*`string`*, *`pattern`*, *`replacement`* [, *`flags`* ]) 或 `regexp_replace`(*`string`*, *`pattern`*, *`replacement`*, *`start`* [, *`N`* [, *`flags`* ]])。如果 *`pattern`* 沒有任何符合，來源 *`string`* 會原封不動地回傳。如果有符合，回傳的 *`string`* 中符合的子字串會被 *`replacement`* 字串取代。*`replacement`* 字串可以包含 `\`*`n`*（其中 *`n`* 為 1 到 9），表示應插入符合模式中第 *`n`* 個括號子運算式的來源子字串；也可以包含 `\&`，表示應插入符合整個模式的子字串。如果你需要在替換文字中放入字面上的反斜線，請寫成 `\\`。*`pattern`* 會在 *`string`* 中搜尋，通常從字串的開頭開始，但如果提供了 *`start`* 參數，就從該字元索引開始。預設情況下，只會替換模式的第一個符合。如果指定了 *`N`* 且大於零，就會替換模式的第 *`N`* 個符合。如果指定了 `g` 旗標，或指定了 *`N`* 且為零，則位於 *`start`* 位置或其後的所有符合都會被替換。（指定 *`N`* 時，會忽略 `g` 旗標。）*`flags`* 參數是一個選用的文字字串，包含零個或多個會改變函式行為的單字母旗標。支援的旗標（但不包括 `g`）說明於[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)。

一些範例：

```

regexp_replace('foobarbaz', 'b..', 'X')
                                   fooXbaz
regexp_replace('foobarbaz', 'b..', 'X', 'g')
                                   fooXX
regexp_replace('foobarbaz', 'b(..)', 'X\1Y', 'g')
                                   fooXarYXazY
regexp_replace('A PostgreSQL function', 'a|e|i|o|u', 'X', 1, 0, 'i')
                                   X PXstgrXSQL fXnctXXn
regexp_replace(string=>'A PostgreSQL function', pattern=>'a|e|i|o|u', replacement=>'X', start=>1, "N"=>3, flags=>'i')
                                   A PostgrXSQL function
```

`regexp_split_to_table` 函式會以 POSIX 正規表示式模式作為分隔符號來分割字串。其語法為 `regexp_split_to_table`(*`string`*, *`pattern`* [, *`flags`* ])。如果 *`pattern`* 沒有任何符合，函式會回傳 *`string`*。如果至少有一個符合，對於每個符合，它會回傳從上一個符合的結尾（或字串的開頭）到該符合開頭之間的文字。當沒有更多符合時，它會回傳從最後一個符合的結尾到字串結尾的文字。*`flags`* 參數是一個選用的文字字串，包含零個或多個會改變函式行為的單字母旗標。`regexp_split_to_table` 支援[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE) 中所述的旗標。

`regexp_split_to_array` 函式的行為與 `regexp_split_to_table` 相同，差別在於 `regexp_split_to_array` 會以 `text` 陣列的形式回傳結果。其語法為 `regexp_split_to_array`(*`string`*, *`pattern`* [, *`flags`* ])。參數與 `regexp_split_to_table` 相同。

一些範例：

```

SELECT foo FROM regexp_split_to_table('the quick brown fox jumps over the lazy dog', '\s+') AS foo;
  foo
-------
 the
 quick
 brown
 fox
 jumps
 over
 the
 lazy
 dog
(9 rows)

SELECT regexp_split_to_array('the quick brown fox jumps over the lazy dog', '\s+');
              regexp_split_to_array
-----------------------------------------------
 {the,quick,brown,fox,jumps,over,the,lazy,dog}
(1 row)

SELECT foo FROM regexp_split_to_table('the quick brown fox', '\s*') AS foo;
 foo
-----
 t
 h
 e
 q
 u
 i
 c
 k
 b
 r
 o
 w
 n
 f
 o
 x
(16 rows)
```

如最後一個範例所示，regexp 分割函式會忽略出現在字串開頭或結尾、或緊接在前一個符合之後的零長度符合。這與其他 regexp 函式所實作的 regexp 比對嚴格定義相反，但在實務上通常是最方便的行為。其他軟體系統（例如 Perl）也使用類似的定義。

`regexp_substr` 函式會回傳符合 POSIX 正規表示式模式的子字串；如果沒有符合，則回傳 `NULL`。其語法為 `regexp_substr`(*`string`*, *`pattern`* [, *`start`* [, *`N`* [, *`flags`* [, *`subexpr`* ]]]])。*`pattern`* 會在 *`string`* 中搜尋，通常從字串的開頭開始，但如果提供了 *`start`* 參數，就從該字元索引開始。如果指定了 *`N`*，就回傳模式的第 *`N`* 個符合，否則回傳第一個符合。*`flags`* 參數是一個選用的文字字串，包含零個或多個會改變函式行為的單字母旗標。支援的旗標說明於[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)。對於包含括號子運算式的模式，*`subexpr`* 是一個整數，指出感興趣的是哪一個子運算式：結果為符合該子運算式的子字串。子運算式依其左括號出現的順序編號。當 *`subexpr`* 省略或為零時，結果為整個符合部分，不論是否有括號子運算式。

一些範例：

```

regexp_substr('number of your street, town zip, FR', '[^,]+', 1, 2)
                                    town zip
regexp_substr('ABCDEFGHI', '(c..)(...)', 1, 1, 'i', 2)
                                   FGH
```

<a id="POSIX-SYNTAX-DETAILS"></a>

#### 9.7.3.1. 正規表示式細節 [#](#POSIX-SYNTAX-DETAILS)

PostgreSQL 的正規表示式是使用 Henry Spencer 撰寫的軟體套件實作的。下面對正規表示式的說明，有很大一部分是逐字取自他的使用手冊。

POSIX 1003.2 所定義的正規表示式（RE）有兩種形式：*延伸* RE，即 ERE（大致相當於 `egrep` 所用的），以及*基本* RE，即 BRE（大致相當於 `ed` 所用的）。PostgreSQL 支援這兩種形式，並且還實作了一些不在 POSIX 標準中、但因為在 Perl 與 Tcl 等程式語言中可用而被廣泛使用的延伸功能。使用這些非 POSIX 延伸功能的 RE，在本文件中稱為*進階* RE，即 ARE。ARE 幾乎是 ERE 的完整超集合，但 BRE 則有若干表示法上的不相容之處（而且功能也受限許多）。我們首先說明 ARE 與 ERE 形式，並註明只適用於 ARE 的功能，然後再說明 BRE 有何不同。

### 注意

PostgreSQL 一開始總是假定正規表示式遵循 ARE 規則。不過，可以如[第 9.7.3.4 節](functions-matching.md#POSIX-METASYNTAX)所述，在 RE 模式前面加上*嵌入選項*，以選擇較受限的 ERE 或 BRE 規則。這對於需要與完全遵循 POSIX 1003.2 規則的應用程式相容時很有用。

正規表示式定義為一個或多個以 `|` 分隔的*分支*。凡是符合其中任一分支的內容，都符合該正規表示式。

分支是零個或多個*帶量詞的原子*或*限制*串接而成。它符合的是：第一個的符合，接著第二個的符合，依此類推；空分支符合空字串。

帶量詞的原子是一個*原子*，後面可能接著單一個*量詞*。沒有量詞時，它符合該原子的一次符合。有量詞時，它可以符合該原子的若干次符合。*原子*可以是[表 9.17](functions-matching.md#POSIX-ATOMS-TABLE) 所列的任何一種可能。可用的量詞及其意義列於[表 9.18](functions-matching.md#POSIX-QUANTIFIERS-TABLE)。

*限制*符合一個空字串，但只有在符合特定條件時才會符合。限制可以用在任何可以使用原子的地方，只是後面不能接量詞。簡單的限制列於[表 9.19](functions-matching.md#POSIX-CONSTRAINTS-TABLE)；稍後還會說明更多的限制。

<a id="POSIX-ATOMS-TABLE"></a>

**表 9.17. 正規表示式原子**

<table border="1" class="table" summary="Regular Expression Atoms"><colgroup><col/><col/></colgroup><thead><tr><th>原子</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">(</code><em class="replaceable"><code>re</code></em><code class="literal">)</code> </td><td> （其中 <em class="replaceable"><code>re</code></em> 是任何正規表示式）符合 <em class="replaceable"><code>re</code></em> 的一次符合，並記錄該符合以供可能的回報 </td></tr><tr><td> <code class="literal">(?:</code><em class="replaceable"><code>re</code></em><code class="literal">)</code> </td><td> 同上，但不記錄該符合以供回報（一組<span class="quote">「<span class="quote">非擷取</span>」</span>括號）（僅限 ARE） </td></tr><tr><td> <code class="literal">.</code> </td><td> 符合任何單一字元 </td></tr><tr><td> <code class="literal">[</code><em class="replaceable"><code>chars</code></em><code class="literal">]</code> </td><td> <em class="firstterm">方括號運算式</em>，符合 <em class="replaceable"><code>chars</code></em> 中的任何一個（詳情請參閱<a class="xref" href="functions-matching.md#POSIX-BRACKET-EXPRESSIONS">第 9.7.3.2 節</a>） </td></tr><tr><td> <code class="literal">\</code><em class="replaceable"><code>k</code></em> </td><td> （其中 <em class="replaceable"><code>k</code></em> 是非英數字元）將該字元視為一般字元來比對，例如 <code class="literal">\\</code> 符合一個反斜線字元 </td></tr><tr><td> <code class="literal">\</code><em class="replaceable"><code>c</code></em> </td><td> 其中 <em class="replaceable"><code>c</code></em> 是英數字元（後面可能接著其他字元），這是一個<em class="firstterm">跳脫</em>，請參閱<a class="xref" href="functions-matching.md#POSIX-ESCAPE-SEQUENCES">第 9.7.3.3 節</a>（僅限 ARE；在 ERE 與 BRE 中，這會符合 <em class="replaceable"><code>c</code></em>） </td></tr><tr><td> <code class="literal">{</code> </td><td> 後面接著數字以外的字元時，符合左大括號字元 <code class="literal">{</code>；後面接著數字時，它是<em class="replaceable"><code>bound</code></em>（界限）的開頭（請參閱下文） </td></tr><tr><td> <em class="replaceable"><code>x</code></em> </td><td> 其中 <em class="replaceable"><code>x</code></em> 是沒有其他意義的單一字元，符合該字元 </td></tr></tbody></table>

<br>

RE 不能以反斜線（`\`）結尾。

### 注意

如果你關閉了 [standard_conforming_strings](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS)，你在字面字串常數中寫的所有反斜線都需要重複寫兩次。詳情請參閱[第 4.1.2.1 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)。

<a id="POSIX-QUANTIFIERS-TABLE"></a>

**表 9.18. 正規表示式量詞**

<table border="1" class="table" summary="Regular Expression Quantifiers"><colgroup><col/><col/></colgroup><thead><tr><th>量詞</th><th>比對</th></tr></thead><tbody><tr><td> <code class="literal">*</code> </td><td> 原子的 0 次或多次符合所構成的序列 </td></tr><tr><td> <code class="literal">+</code> </td><td> 原子的 1 次或多次符合所構成的序列 </td></tr><tr><td> <code class="literal">?</code> </td><td> 原子的 0 次或 1 次符合所構成的序列 </td></tr><tr><td> <code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">}</code> </td><td> 原子恰好 <em class="replaceable"><code>m</code></em> 次符合所構成的序列 </td></tr><tr><td> <code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">,}</code> </td><td> 原子的 <em class="replaceable"><code>m</code></em> 次或更多次符合所構成的序列 </td></tr><tr><td>
<code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">,</code><em class="replaceable"><code>n</code></em><code class="literal">}</code> </td><td> 原子的 <em class="replaceable"><code>m</code></em> 次到 <em class="replaceable"><code>n</code></em> 次（含）符合所構成的序列；<em class="replaceable"><code>m</code></em> 不能超過 <em class="replaceable"><code>n</code></em> </td></tr><tr><td> <code class="literal">*?</code> </td><td> <code class="literal">*</code> 的非貪婪版本 </td></tr><tr><td> <code class="literal">+?</code> </td><td> <code class="literal">+</code> 的非貪婪版本 </td></tr><tr><td> <code class="literal">??</code> </td><td> <code class="literal">?</code> 的非貪婪版本 </td></tr><tr><td> <code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">}?</code> </td><td> <code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">}</code> 的非貪婪版本 </td></tr><tr><td> <code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">,}?</code> </td><td> <code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">,}</code> 的非貪婪版本 </td></tr><tr><td>
<code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">,</code><em class="replaceable"><code>n</code></em><code class="literal">}?</code> </td><td> <code class="literal">{</code><em class="replaceable"><code>m</code></em><code class="literal">,</code><em class="replaceable"><code>n</code></em><code class="literal">}</code> 的非貪婪版本 </td></tr></tbody></table>

<br>

使用 `{`*`...`*`}` 的形式稱為*界限*（bound）。界限中的數字 *`m`* 與 *`n`* 是無號十進位整數，允許的值為 0 到 255（含）。

*非貪婪*量詞（僅適用於 ARE）與其對應的一般（*貪婪*）量詞符合相同的可能性，但偏好最少而非最多的符合次數。詳情請參閱[第 9.7.3.5 節](functions-matching.md#POSIX-MATCHING-RULES)。

### 注意

量詞不能緊接在另一個量詞之後，例如 `**` 是無效的。量詞不能作為運算式或子運算式的開頭，也不能接在 `^` 或 `|` 之後。

<a id="POSIX-CONSTRAINTS-TABLE"></a>

**表 9.19. 正規表示式限制**

<table border="1" class="table" summary="Regular Expression Constraints"><colgroup><col/><col/></colgroup><thead><tr><th>限制</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">^</code> </td><td> 在字串的開頭處符合 </td></tr><tr><td> <code class="literal">$</code> </td><td> 在字串的結尾處符合 </td></tr><tr><td> <code class="literal">(?=</code><em class="replaceable"><code>re</code></em><code class="literal">)</code> </td><td> <em class="firstterm">正向前瞻</em>會在任何有符合 <em class="replaceable"><code>re</code></em> 之子字串開始的位置符合（僅限 ARE） </td></tr><tr><td> <code class="literal">(?!</code><em class="replaceable"><code>re</code></em><code class="literal">)</code> </td><td> <em class="firstterm">負向前瞻</em>會在任何沒有符合 <em class="replaceable"><code>re</code></em> 之子字串開始的位置符合（僅限 ARE） </td></tr><tr><td> <code class="literal">(?&lt;=</code><em class="replaceable"><code>re</code></em><code class="literal">)</code> </td><td> <em class="firstterm">正向後顧</em>會在任何有符合 <em class="replaceable"><code>re</code></em> 之子字串結束的位置符合（僅限 ARE） </td></tr><tr><td> <code class="literal">(?&lt;!</code><em class="replaceable"><code>re</code></em><code class="literal">)</code> </td><td> <em class="firstterm">負向後顧</em>會在任何沒有符合 <em class="replaceable"><code>re</code></em> 之子字串結束的位置符合（僅限 ARE） </td></tr></tbody></table>

<br>

前瞻（lookahead）與後顧（lookbehind）限制不能包含*反向參照*（請參閱[第 9.7.3.3 節](functions-matching.md#POSIX-ESCAPE-SEQUENCES)），而且其中所有的括號都被視為非擷取的。

<a id="POSIX-BRACKET-EXPRESSIONS"></a>

#### 9.7.3.2. 方括號運算式 [#](#POSIX-BRACKET-EXPRESSIONS)

*方括號運算式*是以 `[]` 括起來的字元清單。它通常符合清單中的任何單一字元（但請參閱下文）。如果清單以 `^` 開頭，則它符合清單其餘部分以外的任何單一字元（*不*在清單中的字元）。如果清單中的兩個字元以 `-` 分隔，這是定序順序中介於這兩個字元之間（含）完整字元範圍的簡寫，例如在 ASCII 中，`[0-9]` 符合任何十進位數字。兩個範圍共用同一個端點是不合法的，例如 `a-c-e`。範圍與定序順序高度相關，因此可攜式的程式應避免依賴它們。

若要在清單中包含字面上的 `]`，請將它放在第一個字元（如果有使用 `^`，則放在它之後）。若要包含字面上的 `-`，請將它放在第一個或最後一個字元，或作為範圍的第二個端點。若要以字面上的 `-` 作為範圍的第一個端點，請用 `[.` 與 `.]` 將它括起來，使它成為一個定序元素（請參閱下文）。除了這些字元、一些使用 `[` 的組合（請參閱接下來的段落）以及跳脫（僅限 ARE）之外，所有其他特殊字元在方括號運算式中都會失去其特殊意義。特別是，依照 ERE 或 BRE 規則時，`\` 不是特殊字元，但在 ARE 中它是特殊字元（作為跳脫的開頭）。

在方括號運算式中，以 `[.` 與 `.]` 括起來的定序元素（一個字元、一個在定序時如同單一字元的多字元序列，或是上述兩者的定序順序名稱）代表該定序元素的字元序列。該序列會被視為方括號運算式清單中的單一元素。這使得包含多字元定序元素的方括號運算式可以符合多於一個字元，例如，如果定序順序中包含 `ch` 定序元素，那麼 RE `[[.ch.]]*c` 會符合 `chchcc` 的前五個字元。

### 注意

PostgreSQL 目前不支援多字元定序元素。此處的資訊描述的是未來可能的行為。

在方括號運算式中，以 `[=` 與 `=]` 括起來的定序元素是一個*等價類別*，代表與該定序元素等價的所有定序元素（包括它自己）的字元序列。（如果沒有其他等價的定序元素，其處理方式就如同外圍的分隔符號是 `[.` 與 `.]`。）例如，如果 `o` 與 `^` 是同一個等價類別的成員，那麼 `[[=o=]]`、`[[=^=]]` 與 `[o^]` 都是同義的。等價類別不能作為範圍的端點。

在方括號運算式中，以 `[:` 與 `:]` 括起來的字元類別名稱，代表屬於該類別之所有字元的清單。字元類別不能作為範圍的端點。POSIX 標準定義了以下字元類別名稱：`alnum`（字母與數字）、`alpha`（字母）、`blank`（空格與定位字元）、`cntrl`（控制字元）、`digit`（數字）、`graph`（空格以外的可列印字元）、`lower`（小寫字母）、`print`（包括空格在內的可列印字元）、`punct`（標點符號）、`space`（任何空白字元）、`upper`（大寫字母），以及 `xdigit`（十六進位數字）。對於 7 位元 ASCII 字元集中的字元，這些標準字元類別的行為在各平台之間大致一致。某個非 ASCII 字元是否被視為屬於這些類別之一，取決於正規表示式函式或運算子所使用的*定序*（請參閱[第 23.2 節](../../server-administration/charset/collation.md)），預設則取決於資料庫的 `LC_CTYPE` 語系設定（請參閱[第 23.1 節](../../server-administration/charset/locale.md)）。即使在名稱相似的語系中，非 ASCII 字元的分類也可能因平台而異。（但 `C` 語系從不認為任何非 ASCII 字元屬於這些類別中的任何一個。）除了這些標準字元類別之外，PostgreSQL 還定義了 `word` 字元類別，它等同於 `alnum` 再加上底線（`_`）字元；以及 `ascii` 字元類別，它恰好包含 7 位元 ASCII 字元集。

方括號運算式有兩種特殊情況：方括號運算式 `[[:<:]]` 與 `[[:>:]]` 是限制，分別符合單字開頭與結尾處的空字串。單字定義為一個單字字元序列，其前後都不是單字字元。單字字元是屬於 `word` 字元類別的任何字元，也就是任何字母、數字或底線。這是一項延伸功能，與 POSIX 1003.2 相容但未由其規定，在打算移植到其他系統的軟體中應謹慎使用。通常較建議使用下面所述的限制跳脫；它們並沒有更符合標準，但比較容易輸入。

<a id="POSIX-ESCAPE-SEQUENCES"></a>

#### 9.7.3.3. 正規表示式跳脫 [#](#POSIX-ESCAPE-SEQUENCES)

*跳脫*是以 `\` 開頭、後接一個英數字元的特殊序列。跳脫有幾種類型：字元輸入、類別簡寫、限制跳脫與反向參照。在 ARE 中，`\` 後接英數字元但不構成有效跳脫的情況是不合法的。在 ERE 中沒有跳脫：在方括號運算式之外，`\` 後接英數字元僅代表該字元本身（作為一般字元）；而在方括號運算式之內，`\` 是一般字元。（後者是 ERE 與 ARE 之間唯一真正的不相容之處。）

*字元輸入跳脫*的存在，是為了讓在 RE 中指定不可列印字元及其他不便輸入的字元更加容易。它們列於[表 9.20](functions-matching.md#POSIX-CHARACTER-ENTRY-ESCAPES-TABLE)。

*類別簡寫跳脫*為某些常用的字元類別提供簡寫。它們列於[表 9.21](functions-matching.md#POSIX-CLASS-SHORTHAND-ESCAPES-TABLE)。

*限制跳脫*是一種以跳脫形式撰寫的限制，在符合特定條件時符合空字串。它們列於[表 9.22](functions-matching.md#POSIX-CONSTRAINT-ESCAPES-TABLE)。

*反向參照*（`\`*`n`*）符合的是由數字 *`n`* 指定的前面某個括號子運算式所符合的相同字串（請參閱[表 9.23](functions-matching.md#POSIX-CONSTRAINT-BACKREF-TABLE)）。例如，`([bc])\1` 符合 `bb` 或 `cc`，但不符合 `bc` 或 `cb`。在 RE 中，子運算式必須完全位於反向參照之前。子運算式依其左括號出現的順序編號。非擷取括號不會定義子運算式。反向參照只考慮被參照之子運算式所符合的字串字元，而不考慮其中包含的任何限制。例如，`(^\d)\1` 會符合 `22`。

<a id="POSIX-CHARACTER-ENTRY-ESCAPES-TABLE"></a>

**表 9.20. 正規表示式字元輸入跳脫**

<table border="1" class="table" summary="Regular Expression Character-Entry Escapes"><colgroup><col/><col/></colgroup><thead><tr><th>跳脫</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">\a</code> </td><td> 警示（鈴聲）字元，同 C 語言 </td></tr><tr><td> <code class="literal">\b</code> </td><td> 倒退鍵（backspace），同 C 語言 </td></tr><tr><td> <code class="literal">\B</code> </td><td> 反斜線（<code class="literal">\</code>）的同義詞，有助於減少重複寫反斜線的需要 </td></tr><tr><td> <code class="literal">\c</code><em class="replaceable"><code>X</code></em> </td><td> （其中 <em class="replaceable"><code>X</code></em> 是任何字元）低位 5 個位元與 <em class="replaceable"><code>X</code></em> 相同、其餘位元全為零的字元 </td></tr><tr><td> <code class="literal">\e</code> </td><td> 定序順序名稱為 <code class="literal">ESC</code> 的字元，若沒有，則為八進位值 <code class="literal">033</code> 的字元 </td></tr><tr><td> <code class="literal">\f</code> </td><td> 換頁（form feed），同 C 語言 </td></tr><tr><td> <code class="literal">\n</code> </td><td> 換行（newline），同 C 語言 </td></tr><tr><td> <code class="literal">\r</code> </td><td> 歸位（carriage return），同 C 語言 </td></tr><tr><td> <code class="literal">\t</code> </td><td> 水平定位（horizontal tab），同 C 語言 </td></tr><tr><td> <code class="literal">\u</code><em class="replaceable"><code>wxyz</code></em> </td><td> （其中 <em class="replaceable"><code>wxyz</code></em> 恰好是四個十六進位數字）十六進位值為 <code class="literal">0x</code><em class="replaceable"><code>wxyz</code></em> 的字元
</td></tr><tr><td> <code class="literal">\U</code><em class="replaceable"><code>stuvwxyz</code></em> </td><td> （其中 <em class="replaceable"><code>stuvwxyz</code></em> 恰好是八個十六進位數字）十六進位值為 <code class="literal">0x</code><em class="replaceable"><code>stuvwxyz</code></em> 的字元
</td></tr><tr><td> <code class="literal">\v</code> </td><td> 垂直定位（vertical tab），同 C 語言 </td></tr><tr><td> <code class="literal">\x</code><em class="replaceable"><code>hhh</code></em> </td><td> （其中 <em class="replaceable"><code>hhh</code></em> 是任意長度的十六進位數字序列）十六進位值為 <code class="literal">0x</code><em class="replaceable"><code>hhh</code></em> 的字元（無論使用多少個十六進位數字，都是單一字元）
       </td></tr><tr><td> <code class="literal">\0</code> </td><td> 值為 <code class="literal">0</code> 的字元（空位元組）</td></tr><tr><td> <code class="literal">\</code><em class="replaceable"><code>xy</code></em> </td><td> （其中 <em class="replaceable"><code>xy</code></em> 恰好是兩個八進位數字，且不是<em class="firstterm">反向參照</em>）八進位值為 <code class="literal">0</code><em class="replaceable"><code>xy</code></em> 的字元 </td></tr><tr><td> <code class="literal">\</code><em class="replaceable"><code>xyz</code></em> </td><td> （其中 <em class="replaceable"><code>xyz</code></em> 恰好是三個八進位數字，且不是<em class="firstterm">反向參照</em>）八進位值為 <code class="literal">0</code><em class="replaceable"><code>xyz</code></em> 的字元 </td></tr></tbody></table>

<br>

十六進位數字為 `0`-`9`、`a`-`f` 與 `A`-`F`。八進位數字為 `0`-`7`。

指定 ASCII 範圍（0–127）以外之值的數值字元輸入跳脫，其意義取決於資料庫編碼。當編碼為 UTF-8 時，跳脫值等同於 Unicode 碼位，例如 `\u1234` 表示字元 `U+1234`。對於其他多位元組編碼，字元輸入跳脫通常只是指定該字元各位元組值的串接。如果跳脫值不對應到資料庫編碼中的任何合法字元，並不會引發錯誤，但它永遠不會符合任何資料。

字元輸入跳脫總是被視為一般字元。例如，`\135` 在 ASCII 中是 `]`，但 `\135` 不會結束方括號運算式。

<a id="POSIX-CLASS-SHORTHAND-ESCAPES-TABLE"></a>

**表 9.21. 正規表示式類別簡寫跳脫**

<table border="1" class="table" summary="Regular Expression Class-Shorthand Escapes"><colgroup><col/><col/></colgroup><thead><tr><th>跳脫</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">\d</code> </td><td> 符合任何數字，如同 <code class="literal">[[:digit:]]</code> </td></tr><tr><td> <code class="literal">\s</code> </td><td> 符合任何空白字元，如同 <code class="literal">[[:space:]]</code> </td></tr><tr><td> <code class="literal">\w</code> </td><td> 符合任何單字字元，如同 <code class="literal">[[:word:]]</code> </td></tr><tr><td> <code class="literal">\D</code> </td><td> 符合任何非數字字元，如同 <code class="literal">[^[:digit:]]</code> </td></tr><tr><td> <code class="literal">\S</code> </td><td> 符合任何非空白字元，如同 <code class="literal">[^[:space:]]</code> </td></tr><tr><td> <code class="literal">\W</code> </td><td> 符合任何非單字字元，如同 <code class="literal">[^[:word:]]</code> </td></tr></tbody></table>

<br>

類別簡寫跳脫在方括號運算式中也能運作，儘管上面所示的定義在該情境下在語法上並不完全有效。例如，`[a-c\d]` 等同於 `[a-c[:digit:]]`。

<a id="POSIX-CONSTRAINT-ESCAPES-TABLE"></a>

**表 9.22. 正規表示式限制跳脫**

<table border="1" class="table" summary="Regular Expression Constraint Escapes"><colgroup><col/><col/></colgroup><thead><tr><th>跳脫</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">\A</code> </td><td> 只在字串的開頭處符合（與 <code class="literal">^</code> 有何不同，請參閱<a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES">第 9.7.3.5 節</a>） </td></tr><tr><td> <code class="literal">\m</code> </td><td> 只在單字的開頭處符合 </td></tr><tr><td> <code class="literal">\M</code> </td><td> 只在單字的結尾處符合 </td></tr><tr><td> <code class="literal">\y</code> </td><td> 只在單字的開頭或結尾處符合 </td></tr><tr><td> <code class="literal">\Y</code> </td><td> 只在不是單字開頭或結尾的位置符合 </td></tr><tr><td> <code class="literal">\Z</code> </td><td> 只在字串的結尾處符合（與 <code class="literal">$</code> 有何不同，請參閱<a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES">第 9.7.3.5 節</a>） </td></tr></tbody></table>

<br>

單字的定義與上面 `[[:<:]]` 及 `[[:>:]]` 的規格中相同。在方括號運算式中使用限制跳脫是不合法的。

<a id="POSIX-CONSTRAINT-BACKREF-TABLE"></a>

**表 9.23. 正規表示式反向參照**

<table border="1" class="table" summary="Regular Expression Back References"><colgroup><col/><col/></colgroup><thead><tr><th>跳脫</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">\</code><em class="replaceable"><code>m</code></em> </td><td> （其中 <em class="replaceable"><code>m</code></em> 是非零數字）對第 <em class="replaceable"><code>m</code></em> 個子運算式的反向參照 </td></tr><tr><td> <code class="literal">\</code><em class="replaceable"><code>mnn</code></em> </td><td> （其中 <em class="replaceable"><code>m</code></em> 是非零數字，<em class="replaceable"><code>nn</code></em> 是更多的數字，且十進位值 <em class="replaceable"><code>mnn</code></em> 不大於到目前為止出現過的右擷取括號數量）對第 <em class="replaceable"><code>mnn</code></em> 個子運算式的反向參照 </td></tr></tbody></table>

<br>

### 注意

八進位字元輸入跳脫與反向參照之間存在固有的歧義，如上文所暗示，這個歧義以下列經驗法則解決。開頭的零總是表示八進位跳脫。單一個非零數字、且後面沒有接其他數字時，總是被視為反向參照。不以零開頭的多位數序列，如果出現在適當的子運算式之後（亦即該數字在反向參照的合法範圍內），就被視為反向參照，否則被視為八進位。

<a id="POSIX-METASYNTAX"></a>

#### 9.7.3.4. 正規表示式後設語法 [#](#POSIX-METASYNTAX)

除了上面所述的主要語法之外，還有一些特殊形式與其他雜項語法功能可用。

RE 可以用兩種特殊的*指引*（director）前綴之一開頭。如果 RE 以 `***:` 開頭，RE 的其餘部分會被視為 ARE。（這在 PostgreSQL 中通常沒有作用，因為 RE 本來就被假定為 ARE；但如果 regex 函式的 *`flags`* 參數指定了 ERE 或 BRE 模式，它就會有作用。）如果 RE 以 `***=` 開頭，RE 的其餘部分會被視為字面字串，其中所有字元都被視為一般字元。

ARE 可以用*嵌入選項*開頭：序列 `(?`*`xyz`*`)`（其中 *`xyz`* 是一個或多個字母字元）指定影響 RE 其餘部分的選項。這些選項會覆寫任何先前決定的選項——特別是，它們可以覆寫 regex 運算子所隱含的大小寫區分行為，或 regex 函式的 *`flags`* 參數。可用的選項字母列於[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)。請注意，regex 函式的 *`flags`* 參數也使用這些相同的選項字母。

<a id="POSIX-EMBEDDED-OPTIONS-TABLE"></a>

**表 9.24. ARE 嵌入選項字母**

<table border="1" class="table" summary="ARE Embedded-Option Letters"><colgroup><col/><col/></colgroup><thead><tr><th>選項</th><th>說明</th></tr></thead><tbody><tr><td> <code class="literal">b</code> </td><td> RE 的其餘部分是 BRE </td></tr><tr><td> <code class="literal">c</code> </td><td> 區分大小寫的比對（覆寫運算子類型） </td></tr><tr><td> <code class="literal">e</code> </td><td> RE 的其餘部分是 ERE </td></tr><tr><td> <code class="literal">i</code> </td><td> 不區分大小寫的比對（請參閱<a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES">第 9.7.3.5 節</a>）（覆寫運算子類型） </td></tr><tr><td> <code class="literal">m</code> </td><td> <code class="literal">n</code> 的歷史同義詞 </td></tr><tr><td> <code class="literal">n</code> </td><td> 換行敏感比對（請參閱<a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES">第 9.7.3.5 節</a>） </td></tr><tr><td> <code class="literal">p</code> </td><td> 部分換行敏感比對（請參閱<a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES">第 9.7.3.5 節</a>） </td></tr><tr><td> <code class="literal">q</code> </td><td> RE 的其餘部分是字面（<span class="quote">「<span class="quote">引用</span>」</span>）字串，全部都是一般字元 </td></tr><tr><td> <code class="literal">s</code> </td><td> 非換行敏感比對（預設） </td></tr><tr><td> <code class="literal">t</code> </td><td> 緊湊語法（預設；請參閱下文） </td></tr><tr><td> <code class="literal">w</code> </td><td> 反向部分換行敏感（<span class="quote">「<span class="quote">怪異</span>」</span>）比對（請參閱<a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES">第 9.7.3.5 節</a>） </td></tr><tr><td> <code class="literal">x</code> </td><td> 擴充語法（請參閱下文） </td></tr></tbody></table>

<br>

嵌入選項會在結束該序列的 `)` 處生效。它們只能出現在 ARE 的開頭（如果有 `***:` 指引，則在其之後）。

除了一般的（*緊湊*）RE 語法（其中所有字元都有意義）之外，還有一種*擴充*語法，可藉由指定嵌入的 `x` 選項來使用。在擴充語法中，RE 中的空白字元會被忽略，`#` 與其後的換行字元（或 RE 結尾）之間的所有字元也會被忽略。這允許為複雜的 RE 分段並加上註解。這項基本規則有三個例外：

* 前面有 `\` 的空白字元或 `#` 會被保留
* 方括號運算式中的空白或 `#` 會被保留
* 空白與註解不能出現在多字元符號之中，例如 `(?:`

就此而言，空白字元是指空格、定位字元、換行字元，以及任何屬於 *`space`* 字元類別的字元。

最後，在 ARE 中、方括號運算式之外，序列 `(?#`*`ttt`*`)`（其中 *`ttt`* 是任何不包含 `)` 的文字）是註解，會被完全忽略。同樣地，這不允許出現在多字元符號（例如 `(?:`）的字元之間。這類註解與其說是實用的功能，不如說是歷史遺留產物，已不建議使用；請改用擴充語法。

如果開頭的 `***=` 指引已指定將使用者的輸入視為字面字串而非 RE，那麼這些後設語法延伸功能*全都*無法使用。

<a id="POSIX-MATCHING-RULES"></a>

#### 9.7.3.5. 正規表示式比對規則 [#](#POSIX-MATCHING-RULES)

如果一個 RE 可以符合給定字串中多於一個的子字串，RE 會符合字串中最早開始的那一個。如果 RE 可以符合從該位置開始的多於一個子字串，則會取最長可能的符合或最短可能的符合，取決於該 RE 是*貪婪*還是*非貪婪*的。

一個 RE 是否為貪婪，由下列規則決定：

* 大多數原子以及所有限制都沒有貪婪屬性（因為它們本來就無法符合可變長度的文字）。
* 在 RE 外面加上括號不會改變其貪婪性。
* 帶有固定重複次數量詞（`{`*`m`*`}` 或 `{`*`m`*`}?`）的帶量詞原子，其貪婪性（可能是沒有）與原子本身相同。
* 帶有其他一般量詞（包括 *`m`* 等於 *`n`* 的 `{`*`m`*`,`*`n`*`}`）的帶量詞原子是貪婪的（偏好最長的符合）。
* 帶有非貪婪量詞（包括 *`m`* 等於 *`n`* 的 `{`*`m`*`,`*`n`*`}?`）的帶量詞原子是非貪婪的（偏好最短的符合）。
* 分支——也就是沒有頂層 `|` 運算子的 RE——其貪婪性與其中第一個具有貪婪屬性的帶量詞原子相同。
* 由兩個或多個以 `|` 運算子連接的分支所組成的 RE，總是貪婪的。

上述規則不僅將貪婪屬性與個別的帶量詞原子相關聯，也與包含帶量詞原子的分支及整個 RE 相關聯。這表示比對進行的方式是：分支或整個 RE *作為一個整體*，符合最長或最短的可能子字串。一旦決定了整個符合的長度，其中符合任何特定子運算式的部分，便依據該子運算式的貪婪屬性來決定，而在 RE 中較早開始的子運算式優先於較晚開始的子運算式。

以下範例說明這代表的意義：

```

SELECT SUBSTRING('XY1234Z', 'Y*([0-9]{1,3})');
Result: 123
SELECT SUBSTRING('XY1234Z', 'Y*?([0-9]{1,3})');
Result: 1
```

在第一個例子中，RE 整體是貪婪的，因為 `Y*` 是貪婪的。它可以從 `Y` 開始符合，並符合從該處開始的最長可能字串，也就是 `Y123`。輸出是其中括號內的部分，也就是 `123`。在第二個例子中，RE 整體是非貪婪的，因為 `Y*?` 是非貪婪的。它可以從 `Y` 開始符合，並符合從該處開始的最短可能字串，也就是 `Y1`。子運算式 `[0-9]{1,3}` 是貪婪的，但它無法改變關於整體符合長度的決定；因此它被迫只符合 `1`。

簡而言之，當一個 RE 同時包含貪婪與非貪婪的子運算式時，總符合長度會依據指派給整個 RE 的屬性，盡可能地長或盡可能地短。指派給子運算式的屬性，只會影響它們彼此之間可以「吃掉」該符合的多少部分。

量詞 `{1,1}` 與 `{1,1}?` 可以分別用來強制子運算式或整個 RE 為貪婪或非貪婪。當你需要整個 RE 具有與從其元素推導出來的不同的貪婪屬性時，這就很有用。舉例來說，假設我們試著將一個包含一些數字的字串，分成數字以及數字前後的部分。我們可能會這樣嘗試：

```

SELECT regexp_match('abc01234xyz', '(.*)(\d+)(.*)');
Result: {abc0123,4,xyz}
```

這樣行不通：第一個 `.*` 是貪婪的，所以它會盡可能地「吃掉」，讓 `\d+` 只能在最後可能的位置——也就是最後一個數字——進行比對。我們可能會試著將它改為非貪婪來修正：

```

SELECT regexp_match('abc01234xyz', '(.*?)(\d+)(.*)');
Result: {abc,0,""}
```

這樣也行不通，因為現在 RE 整體是非貪婪的，所以它會盡早結束整體的符合。我們可以強制讓 RE 整體為貪婪，來得到我們想要的結果：

```

SELECT regexp_match('abc01234xyz', '(?:(.*?)(\d+)(.*)){1,1}');
Result: {abc,01234,xyz}
```

將 RE 的整體貪婪性與其組成部分的貪婪性分開控制，在處理可變長度的模式時提供了極大的彈性。

在判斷何者是較長或較短的符合時，符合長度是以字元而非定序元素來計算的。空字串被認為比完全沒有符合還要長。例如：`bb*` 符合 `abbbc` 中間的三個字元；`(week|wee)(night|knights)` 符合 `weeknights` 的全部十個字元；當 `(.*).*` 與 `abc` 比對時，括號子運算式符合全部三個字元；而當 `(a*)*` 與 `bc` 比對時，整個 RE 與括號子運算式都符合空字串。

如果指定了不區分大小寫的比對，其效果就如同字母表中所有大小寫的區別都消失了一樣。當一個具有多種大小寫形式的字母，以一般字元的身分出現在方括號運算式之外時，它實際上會被轉換為包含兩種大小寫的方括號運算式，例如 `x` 會變成 `[xX]`。當它出現在方括號運算式之內時，它所有對應的大小寫形式都會被加入該方括號運算式，例如 `[x]` 會變成 `[xX]`，而 `[^x]` 會變成 `[^xX]`。

如果指定了換行敏感比對，`.` 以及使用 `^` 的方括號運算式將永遠不會符合換行字元（因此除非 RE 明確包含換行字元，否則符合不會跨越多行）；而 `^` 與 `$` 除了分別在字串開頭與結尾處符合之外，也會分別符合換行字元之後與之前的空字串。但 ARE 跳脫 `\A` 與 `\Z` 仍然*只*符合字串的開頭或結尾。此外，無論是否處於這個模式，字元類別簡寫 `\D` 與 `\W` 都會符合換行字元。（在 PostgreSQL 14 之前，處於換行敏感模式時它們不會符合換行字元。若要得到舊的行為，請寫成 `[^[:digit:]]` 或 `[^[:word:]]`。）

如果指定了部分換行敏感比對，它會如同換行敏感比對一樣影響 `.` 與方括號運算式，但不影響 `^` 與 `$`。

如果指定了反向部分換行敏感比對，它會如同換行敏感比對一樣影響 `^` 與 `$`，但不影響 `.` 與方括號運算式。這並不是很有用，但為了對稱性而提供。

<a id="POSIX-LIMITS-COMPATIBILITY"></a>

#### 9.7.3.6. 限制與相容性 [#](#POSIX-LIMITS-COMPATIBILITY)

在這個實作中，RE 的長度沒有特別的限制。不過，希望具有高度可攜性的程式不應使用超過 256 位元組的 RE，因為符合 POSIX 的實作可能會拒絕接受這樣的 RE。

ARE 唯一真正與 POSIX ERE 不相容的功能，是 `\` 在方括號運算式中不會失去其特殊意義。所有其他 ARE 功能所使用的語法，在 POSIX ERE 中都是不合法的，或具有未定義或未指明的效果；指引的 `***` 語法同樣也不在 BRE 與 ERE 的 POSIX 語法範圍內。

許多 ARE 延伸功能是借自 Perl，但其中有些已經過修改以使其更加整齊，而且有少數 Perl 延伸功能並不存在。值得注意的不相容之處包括：`\b`、`\B`、對結尾換行字元沒有特殊處理、將取補集的方括號運算式加入受換行敏感比對影響的項目、前瞻／後顧限制中對括號與反向參照的限制，以及最長／最短符合（而非最先符合）的比對語意。

<a id="POSIX-BASIC-REGEXES"></a>

#### 9.7.3.7. 基本正規表示式 [#](#POSIX-BASIC-REGEXES)

BRE 與 ERE 在幾個方面有所不同。在 BRE 中，`|`、`+` 與 `?` 是一般字元，而且沒有與其功能等效的替代寫法。界限的分隔符號是 `\{` 與 `\}`，而 `{` 與 `}` 本身是一般字元。巢狀子運算式的括號是 `\(` 與 `\)`，而 `(` 與 `)` 本身是一般字元。`^` 是一般字元，除非它位於 RE 的開頭或括號子運算式的開頭；`$` 是一般字元，除非它位於 RE 的結尾或括號子運算式的結尾；而如果 `*` 出現在 RE 的開頭或括號子運算式的開頭（在可能存在的開頭 `^` 之後），它就是一般字元。最後，BRE 可以使用單一位數的反向參照，而 `\<` 與 `\>` 分別是 `[[:<:]]` 與 `[[:>:]]` 的同義詞；BRE 中沒有其他可用的跳脫。

<a id="POSIX-VS-XQUERY"></a>

#### 9.7.3.8. 與 SQL 標準及 XQuery 的差異 [#](#POSIX-VS-XQUERY)

<a id="id-1.5.8.13.9.48.2"></a><a id="id-1.5.8.13.9.48.3"></a><a id="id-1.5.8.13.9.48.4"></a><a id="id-1.5.8.13.9.48.5"></a><a id="id-1.5.8.13.9.48.6"></a><a id="id-1.5.8.13.9.48.7"></a>

自 SQL:2008 起，SQL 標準納入了依照 XQuery 正規表示式標準進行模式比對的正規表示式運算子與函式：

* `LIKE_REGEX`
* `OCCURRENCES_REGEX`
* `POSITION_REGEX`
* `SUBSTRING_REGEX`
* `TRANSLATE_REGEX`

PostgreSQL 目前並未實作這些運算子與函式。在每種情況下，你都可以如[表 9.25](functions-matching.md#FUNCTIONS-REGEXP-SQL-TABLE) 所示，取得大致等效的功能。（此表中省略了兩邊的各種選用子句。）

<a id="FUNCTIONS-REGEXP-SQL-TABLE"></a>

**表 9.25. 正規表示式函式對照**

<table border="1" class="table" summary="Regular Expression Functions Equivalencies"><colgroup><col/><col/></colgroup><thead><tr><th>SQL 標準</th><th><span class="productname">PostgreSQL</span></th></tr></thead><tbody><tr><td><code class="literal"><em class="replaceable"><code>string</code></em> LIKE_REGEX <em class="replaceable"><code>pattern</code></em></code></td><td><code class="literal">regexp_like(<em class="replaceable"><code>string</code></em>, <em class="replaceable"><code>pattern</code></em>)</code> or <code class="literal"><em class="replaceable"><code>string</code></em> ~ <em class="replaceable"><code>pattern</code></em></code></td></tr><tr><td><code class="literal">OCCURRENCES_REGEX(<em class="replaceable"><code>pattern</code></em> IN <em class="replaceable"><code>string</code></em>)</code></td><td><code class="literal">regexp_count(<em class="replaceable"><code>string</code></em>, <em class="replaceable"><code>pattern</code></em>)</code></td></tr><tr><td><code class="literal">POSITION_REGEX(<em class="replaceable"><code>pattern</code></em> IN <em class="replaceable"><code>string</code></em>)</code></td><td><code class="literal">regexp_instr(<em class="replaceable"><code>string</code></em>, <em class="replaceable"><code>pattern</code></em>)</code></td></tr><tr><td><code class="literal">SUBSTRING_REGEX(<em class="replaceable"><code>pattern</code></em> IN <em class="replaceable"><code>string</code></em>)</code></td><td><code class="literal">regexp_substr(<em class="replaceable"><code>string</code></em>, <em class="replaceable"><code>pattern</code></em>)</code></td></tr><tr><td><code class="literal">TRANSLATE_REGEX(<em class="replaceable"><code>pattern</code></em> IN <em class="replaceable"><code>string</code></em> WITH <em class="replaceable"><code>replacement</code></em>)</code></td><td><code class="literal">regexp_replace(<em class="replaceable"><code>string</code></em>, <em class="replaceable"><code>pattern</code></em>, <em class="replaceable"><code>replacement</code></em>)</code></td></tr></tbody></table>

<br>

與 PostgreSQL 所提供的正規表示式函式類似的函式，在許多其他 SQL 實作中也有提供，而 SQL 標準的函式則沒有那麼廣泛地被實作。正規表示式語法的一些細節，在各個實作中很可能會有所不同。

SQL 標準的運算子與函式使用 XQuery 正規表示式，它與上面所述的 ARE 語法相當接近。現有以 POSIX 為基礎的正規表示式功能與 XQuery 正規表示式之間值得注意的差異包括：

* 不支援 XQuery 的字元類別減法。這項功能的一個例子，是使用下列寫法只比對英文子音：`[a-z-[aeiou]]`。
* 不支援 XQuery 的字元類別簡寫 `\c`、`\C`、`\i` 與 `\I`。
* 不支援使用 `\p{UnicodeProperty}` 或其反向形式 `\P{UnicodeProperty}` 的 XQuery 字元類別元素。
* POSIX 會依據目前通行的語系（你可以在運算子或函式上附加 `COLLATE` 子句來控制）來解讀字元類別，例如 `\w`（請參閱[表 9.21](functions-matching.md#POSIX-CLASS-SHORTHAND-ESCAPES-TABLE)）。XQuery 則是參照 Unicode 字元屬性來規定這些類別，因此只有在使用遵循 Unicode 規則的語系時，才能得到等效的行為。
* SQL 標準（而非 XQuery 本身）試圖顧及比 POSIX 更多種類的「換行」。上面所述的換行敏感比對選項只將 ASCII NL（`\n`）視為換行，但 SQL 會要求我們將 CR（`\r`）、CRLF（`\r\n`）（Windows 風格的換行）以及一些 Unicode 特有的字元，例如 LINE SEPARATOR（U+2028），也都視為換行。值得注意的是，依照 SQL，`.` 與 `\s` 應該將 `\r\n` 計為一個字元而不是兩個。
* 在[表 9.20](functions-matching.md#POSIX-CHARACTER-ENTRY-ESCAPES-TABLE) 所述的字元輸入跳脫中，XQuery 只支援 `\n`、`\r` 與 `\t`。
* XQuery 不支援在方括號運算式中用於字元類別的 `[:name:]` 語法。
* XQuery 沒有前瞻或後顧限制，也沒有[表 9.22](functions-matching.md#POSIX-CONSTRAINT-ESCAPES-TABLE) 所述的任何限制跳脫。
* [第 9.7.3.4 節](functions-matching.md#POSIX-METASYNTAX)所述的後設語法形式在 XQuery 中並不存在。
* XQuery 所定義的正規表示式旗標字母，與 POSIX 的選項字母（[表 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE)）相關但不相同。雖然 `i` 與 `q` 選項的行為相同，其他選項則不然：

  * XQuery 的 `s`（允許點號符合換行字元）與 `m`（允許 `^` 與 `$` 在換行處符合）旗標，提供了與 POSIX 的 `n`、`p` 與 `w` 旗標相同的行為，但它們與 POSIX 的 `s` 及 `m` 旗標的行為*並不*相符。特別要注意的是，點號符合換行字元在 POSIX 中是預設行為，但在 XQuery 中則不是。
  * XQuery 的 `x`（忽略模式中的空白）旗標與 POSIX 的擴充模式旗標明顯不同。POSIX 的 `x` 旗標也允許 `#` 在模式中開始一段註解，而且 POSIX 不會忽略反斜線之後的空白字元。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-matching.html)（原文版本：18.6；核對日期：2026-09-11）
