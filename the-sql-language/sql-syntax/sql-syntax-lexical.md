<a id="SQL-SYNTAX-LEXICAL"></a>

## 4.1. 詞彙結構 [#](#sql-syntax-lexical) <a href="#sql-syntax-lexical" id="sql-syntax-lexical"></a>

[4.1.1. 識別字與關鍵字](sql-syntax-lexical.md#sql-syntax-identifiers)

[4.1.2. 常數](sql-syntax-lexical/sql-syntax-constants.md#sql-syntax-constants)

[4.1.3. 運算子](sql-syntax-lexical.md#sql-syntax-operators)

[4.1.4. 特殊字元](sql-syntax-lexical.md#sql-syntax-special-chars)

[4.1.5. 註解](sql-syntax-lexical.md#sql-syntax-comments)

[4.1.6. 運算子優先順序](sql-syntax-lexical/sql-precedence.md#sql-precedence)

<a id="id-1.5.3.5.2"></a>

SQL 輸入由一連串的*指令*（command）組成。一個指令由一連串的*語彙單元*（token）組成，並以分號（「;」）結束。輸入串流的結尾也會結束一個指令。哪些語彙單元是有效的，取決於特定指令的語法。

語彙單元可以是*關鍵字*（key word）、*識別字*（identifier）、*加引號的識別字*（quoted identifier）、*字面值*（literal，或稱常數），或是特殊字元符號。語彙單元通常以空白字元（空格、定位字元、換行）分隔，但如果不會產生歧義，也可以不分隔（一般只有在特殊字元緊鄰其他類型的語彙單元時才會如此）。

例如，下列是（語法上）有效的 SQL 輸入：

```

SELECT * FROM MY_TABLE;
UPDATE MY_TABLE SET A = 5;
INSERT INTO MY_TABLE VALUES (3, 'hi there');
```

這是由三個指令組成的序列，每行一個指令（雖然這並非必要；一行可以有多個指令，而且把指令拆成多行也很實用）。

此外，SQL 輸入中也可以出現*註解*（comment）。註解不是語彙單元，實際上等同於空白字元。

SQL 語法在哪些語彙單元用來識別指令、哪些是運算元或參數這方面並不太一致。前幾個語彙單元一般是指令名稱，所以在上面的範例中，我們通常會說這是一個「SELECT」、一個「UPDATE」與一個「INSERT」指令。但舉例來說，`UPDATE` 指令總是要求在某個特定位置出現 `SET` 語彙單元，而這種形式的 `INSERT` 也需要 `VALUES` 才算完整。每個指令精確的語法規則，請參閱[第六部分](../../reference/README.md)。

<a id="SQL-SYNTAX-IDENTIFIERS"></a>

### 4.1.1. 識別字與關鍵字 [#](#sql-syntax-identifiers) <a href="#sql-syntax-identifiers" id="sql-syntax-identifiers"></a>

<a id="id-1.5.3.5.8.2"></a><a id="id-1.5.3.5.8.3"></a><a id="id-1.5.3.5.8.4"></a>

上面範例中的 `SELECT`、`UPDATE` 或 `VALUES` 這類語彙單元就是*關鍵字*的例子，也就是在 SQL 語言中具有固定意義的單字。語彙單元 `MY_TABLE` 與 `A` 則是*識別字*的例子。依所在的指令而定，它們用來識別資料表、欄位或其他資料庫物件的名稱。因此它們有時也被簡單地稱為「名稱」。關鍵字與識別字具有相同的詞彙結構，這表示如果不懂這個語言，就無法知道某個語彙單元究竟是識別字還是關鍵字。完整的關鍵字清單請參閱[附錄 C](../../appendixes/sql-keywords-appendix/README.md)。

SQL 識別字與關鍵字必須以字母（`a`-`z`，也包括帶有變音符號的字母與非拉丁字母）或底線（`_`）開頭。識別字或關鍵字中後續的字元可以是字母、底線、數字（`0`-`9`）或錢號（`$`）。請注意，依照 SQL 標準的字面規定，識別字中不允許出現錢號，因此使用錢號可能會降低應用程式的可攜性。SQL 標準不會定義包含數字、或以底線開頭或結尾的關鍵字，因此這種形式的識別字不會與標準未來的延伸發生衝突。

<a id="id-1.5.3.5.8.7.1"></a>
系統最多只使用識別字的 `NAMEDATALEN`-1 個位元組；指令中可以寫更長的名稱，但會被截斷。預設情況下，`NAMEDATALEN` 是 64，因此識別字的最大長度是 63 個位元組。如果這個限制造成問題，可以修改 `src/include/pg_config_manual.h` 中的 `NAMEDATALEN` 常數來提高它。

<a id="id-1.5.3.5.8.8.1"></a>
關鍵字與未加引號的識別字不區分大小寫。因此：

```

UPDATE MY_TABLE SET A = 5;
```

也可以等價地寫成：

```

uPDaTE my_TabLE SeT a = 5;
```

一種常用的慣例是將關鍵字寫成大寫，名稱寫成小寫，例如：

```

UPDATE my_table SET a = 5;
```

<a id="id-1.5.3.5.8.9.1"></a>
還有第二種識別字：*界定識別字*（delimited identifier）或*加引號的識別字*（quoted identifier）。它是以雙引號（`"`）括住任意字元序列而形成的。界定識別字永遠是識別字，絕不會是關鍵字。因此，`"select"` 可以用來參照名為「select」的欄位或資料表；而未加引號的 `select` 則會被當成關鍵字，因此在需要資料表或欄位名稱的地方使用時，會引發剖析錯誤。上面的範例可以用加引號的識別字寫成這樣：

```

UPDATE "my_table" SET "a" = 5;
```

加引號的識別字可以包含任何字元，只有代碼為零的字元除外。（要包含雙引號，請寫兩個雙引號。）這讓你可以建立原本不可能使用的資料表或欄位名稱，例如包含空格或 & 符號的名稱。長度限制仍然適用。

將識別字加上引號也會讓它區分大小寫，而未加引號的名稱則一律會轉為小寫。例如，PostgreSQL 會將識別字 `FOO`、`foo` 與 `"foo"` 視為相同，但 `"Foo"` 與 `"FOO"` 則與這三者不同，彼此之間也不同。（PostgreSQL 將未加引號的名稱轉為小寫的做法與 SQL 標準不相容；SQL 標準規定未加引號的名稱應該轉為大寫。因此，依照標準，`foo` 應該等同於 `"FOO"`，而不是 `"foo"`。如果你想撰寫可攜的應用程式，建議對某個特定名稱要嘛一律加上引號，要嘛一律不加。）

<a id="id-1.5.3.5.8.12"></a>

加引號識別字的一種變形，允許包含以碼位（code point）識別的跳脫 Unicode 字元。這種變形以 `U&`（大寫或小寫的 U 後面接著 & 符號）開頭，緊接在開頭的雙引號之前，中間不能有任何空格，例如 `U&"foo"`。（請注意，這會與運算子 `&` 產生歧義。在運算子前後加上空格即可避免這個問題。）在引號內，可以用跳脫形式指定 Unicode 字元：寫一個反斜線後接四位數的十六進位碼位數字，或寫一個反斜線後接加號，再接六位數的十六進位碼位數字。例如，識別字 `"data"` 可以寫成

```

U&"d\0061t\+000061"
```

下面這個比較不簡單的範例，以西里爾字母寫出俄文單字「slon」（大象）：

```

U&"\0441\043B\043E\043D"
```

如果想使用反斜線以外的跳脫字元，可以在字串之後使用 `UESCAPE`<a id="id-1.5.3.5.8.14.2"></a> 子句指定，例如：

```

U&"d!0061t!+000061" UESCAPE '!'
```

跳脫字元可以是十六進位數字、加號、單引號、雙引號或空白字元以外的任何單一字元。請注意，`UESCAPE` 之後的跳脫字元是以單引號括住，而不是雙引號。

要在識別字中按字面包含跳脫字元，請將它寫兩次。

四位數或六位數的跳脫形式都可以用來指定 UTF-16 代理對（surrogate pair），以組成碼位大於 U+FFFF 的字元，不過既然有六位數的形式，技術上就不需要這麼做。（代理對不會直接儲存，而是會合併為單一碼位。）

如果伺服器編碼不是 UTF-8，這些跳脫序列所識別的 Unicode 碼位會轉換為實際的伺服器編碼；如果無法轉換，就會回報錯誤。

### 4.1.2. 常數 [#](#sql-syntax-constants) <a href="#sql-syntax-constants" id="sql-syntax-constants"></a>

完整內容請見 [4.1.2. 常數](sql-syntax-lexical/sql-syntax-constants.md#sql-syntax-constants)。

<a id="SQL-SYNTAX-OPERATORS"></a>

### 4.1.3. 運算子 [#](#sql-syntax-operators) <a href="#sql-syntax-operators" id="sql-syntax-operators"></a>

<a id="id-1.5.3.5.10.2"></a>

運算子名稱是由最多 `NAMEDATALEN`-1（預設為 63）個字元組成的序列，這些字元取自下列清單：

<br>
+ - \* / < > = ~ ! @ # % ^ & | ` ?<br>

不過，運算子名稱有一些限制：

* `--` 與 `/*` 不能出現在運算子名稱中的任何位置，因為它們會被當作註解的開頭。
* 多字元的運算子名稱不能以 `+` 或 `-` 結尾，除非該名稱同時也包含下列至少一個字元：

  <br>
  ~ ! @ # % ^ & | ` ?<br>

  例如，`@-` 是允許的運算子名稱，但 `*-` 則不是。這項限制讓 PostgreSQL 能夠剖析符合 SQL 標準的查詢，而不需要在語彙單元之間加上空格。

使用非 SQL 標準的運算子名稱時，通常需要以空格分隔相鄰的運算子，以避免歧義。例如，如果你定義了一個名為 `@` 的前置運算子，就不能寫 `X*@Y`；你必須寫 `X* @Y`，以確保 PostgreSQL 將它讀成兩個運算子名稱，而不是一個。

<a id="SQL-SYNTAX-SPECIAL-CHARS"></a>

### 4.1.4. 特殊字元 [#](#sql-syntax-special-chars) <a href="#sql-syntax-special-chars" id="sql-syntax-special-chars"></a>

有些非英數字元具有特殊意義，與作為運算子的意義不同。用法的細節可以在說明各個語法元素的地方找到。本節只是用來提醒這些字元的存在，並概述它們的用途。

* 錢號（`$`）後面接著數字，用來在函式定義主體或預備陳述式中表示位置參數。在其他情境中，錢號可以是識別字或錢號引用字串常數的一部分。
* 圓括號（`()`）具有一般的意義，用來將運算式分組並強制優先順序。在某些情況下，圓括號是特定 SQL 指令固定語法的一部分，是必要的。
* 方括號（`[]`）用來選取陣列的元素。關於陣列的更多資訊，請參閱[第 8.15 節](../datatype/arrays.md)。
* 逗號（`,`）在某些語法結構中用來分隔清單中的元素。
* 分號（`;`）用來結束一個 SQL 指令。除了在字串常數或加引號的識別字中之外，它不能出現在指令中的任何位置。
* 冒號（`:`）用來從陣列中選取「切片」（slice）。（請參閱[第 8.15 節](../datatype/arrays.md)。）在某些 SQL 方言中（例如 Embedded SQL），冒號用來作為變數名稱的前綴。
* 星號（`*`）在某些情境中用來表示資料表資料列或複合值的所有欄位。當它作為彙總函式的參數時也具有特殊意義，也就是表示該彙總函式不需要任何明確的參數。
* 句點（`.`）用在數值常數中，也用來分隔 schema、資料表與欄位名稱。

<a id="SQL-SYNTAX-COMMENTS"></a>

### 4.1.5. 註解 [#](#sql-syntax-comments) <a href="#sql-syntax-comments" id="sql-syntax-comments"></a>

<a id="id-1.5.3.5.12.2"></a>

註解是以兩個連字號開頭、一直延伸到行尾的字元序列，例如：

```

-- This is a standard SQL comment
```

另外，也可以使用 C 語言風格的區塊註解：

```

/* multiline comment
 * with nesting: /* nested block comment */
 */
```

其中註解以 `/*` 開頭，一直延伸到相對應的 `*/`。這些區塊註解可以巢狀使用，這是 SQL 標準的規定，但與 C 語言不同；因此可以將可能已經包含區塊註解的大段程式碼整個註解掉。

註解會在進一步的語法分析之前從輸入串流中移除，實際上會被空白字元取代。

### 4.1.6. 運算子優先順序 [#](#sql-precedence) <a href="#sql-precedence" id="sql-precedence"></a>

完整內容請見 [4.1.6. 運算子優先順序](sql-syntax-lexical/sql-precedence.md#sql-precedence)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-syntax-lexical.html)（原文版本：18.6；核對日期：2026-09-11）
