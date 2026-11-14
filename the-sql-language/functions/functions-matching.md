<a id="FUNCTIONS-MATCHING"></a>

## 9.7. 模式比對 [#](#functions-matching) <a href="#functions-matching" id="functions-matching"></a>

[9.7.1. `LIKE`](functions-matching.md#functions-like)

[9.7.2. `SIMILAR TO` 正規表示式](functions-matching.md#functions-similarto-regexp)

[9.7.3. POSIX 正規表示式](functions-matching/functions-posix-regexp.md#functions-posix-regexp)

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

### 9.7.1. `LIKE` [#](#functions-like) <a href="#functions-like" id="functions-like"></a>

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

如果你關閉了 [standard_conforming_strings](../../server-administration/runtime-config/runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS)，你在字面字串常數中寫的所有反斜線都需要重複寫兩次。詳情請參閱[第 4.1.2.1 節](../sql-syntax/sql-syntax-lexical/sql-syntax-constants.md#sql-syntax-strings)。

也可以寫成 `ESCAPE ''` 來不選擇任何跳脫字元。這實際上會停用跳脫機制，使得無法關閉模式中底線與百分比符號的特殊意義。

根據 SQL 標準，省略 `ESCAPE` 表示沒有跳脫字元（而不是預設為反斜線），而且不允許長度為零的 `ESCAPE` 值。因此，PostgreSQL 在這方面的行為略微不符合標準。

可以使用關鍵字 `ILIKE` 取代 `LIKE`，依照目前作用中的語系進行不區分大小寫的比對。（但這不支援非決定性定序。）這不在 SQL 標準中，而是 PostgreSQL 的延伸功能。

運算子 `~~` 等同於 `LIKE`，而 `~~*` 對應於 `ILIKE`。另外還有 `!~~` 與 `!~~*` 運算子，分別代表 `NOT LIKE` 與 `NOT ILIKE`。這些運算子都是 PostgreSQL 特有的。你可能會在 `EXPLAIN` 輸出及類似的地方看到這些運算子名稱，因為剖析器實際上會將 `LIKE` 等轉譯為這些運算子。

在 PostgreSQL 語法中，`LIKE`、`ILIKE`、`NOT LIKE` 與 `NOT ILIKE` 這些片語一般被視為運算子；例如，它們可以用在 *`expression`* *`operator`* ANY (*`subquery`*) 建構中，不過其中不能包含 `ESCAPE` 子句。在某些少見的情況下，可能需要改用底層的運算子名稱。

另請參閱「開頭為」（starts-with）運算子 `^@` 及對應的 `starts_with()` 函式，在只需要比對字串開頭的情況下，它們很有用。

<a id="FUNCTIONS-SIMILARTO-REGEXP"></a>

### 9.7.2. `SIMILAR TO` 正規表示式 [#](#functions-similarto-regexp) <a href="#functions-similarto-regexp" id="functions-similarto-regexp"></a>

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

另一項非標準的延伸是：在跳脫字元後面接一個字母或數字，就可以使用為 POSIX 正規表示式定義的跳脫序列；請參閱下方的[表 9.20](functions-matching/functions-posix-regexp.md#posix-character-entry-escapes-table)、[表 9.21](functions-matching/functions-posix-regexp.md#posix-class-shorthand-escapes-table) 與[表 9.22](functions-matching/functions-posix-regexp.md#posix-constraint-escapes-table)。

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

### 9.7.3. POSIX 正規表示式 [#](#functions-posix-regexp) <a href="#functions-posix-regexp" id="functions-posix-regexp"></a>

完整內容請見 [9.7.3. POSIX 正規表示式](functions-matching/functions-posix-regexp.md#functions-posix-regexp)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-matching.html)（原文版本：18.6；核對日期：2026-09-11）
