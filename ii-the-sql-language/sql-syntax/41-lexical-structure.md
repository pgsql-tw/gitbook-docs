# 4.1. 語法結構[^1]

SQL 語法包含一連串的命令，命令是由一系列的指示記號所組合而成，以分號結尾。最後如果是串流輸入，也會結束一個命令。指示的合法性是由特別的命令語法所定義的。

指示記號可能是關鍵字、識別項、引號識別項、文字、或一個特別的字元符號。指示一般來說是以空白分隔（空白符號、定位符號、換行符號），但如果不會混淆的話，也不一定需要。（一般只出現在特殊字元用來調整了其他指示的型別）

舉個例子，下面就是一個合法（符合語法）的 SQL 輸入：

```
SELECT * FROM MY_TABLE;
UPDATE MY_TABLE SET A = 5;
INSERT INTO MY_TABLE VALUES (3, 'hi there');
```

這個序列包含了 3 個命令，每行一個（然而這不是一定的，同一行可以超過一個命令，而一個命令也可以分解為多行使用）。

順帶一提的是，註解也是 SQL 輸入的一部份，但不屬於任何指示記號，他們等同於空白字元。

SQL 語法並不是很嚴格要求什麼樣的指示記號來識別命令，或是哪些是運算子或參數。通常最前面的指示記號是命令的名稱，以上面的例子來說，我們通常會說是一個「SELECT」、一個「UPDATE」、以及一個「INSERT」命令。但對於 UPDATE 命令而言，有一個 SET 指示記號出現在某個地方是必要的；同樣地，INSERT 也需要有 VALUES 來搭配。精確的語法規則都在[第 6 部份](/vi-reference.md)中的章節進行說明。

### 4.1.1. 識別項（Identifier）和關鍵字 （Keyword）

在上面的例子中的 SELECT、UPDATE、或是 VALUES，都是屬於關鍵字的範圍。所謂關鍵字，意即在 SQL 語言中，其具有固定的意義。像指示記號 MY\_TABLE 則是屬於識別項。它識別表格的名稱，欄位名稱，或是其他的資料庫物件，端看命令如何看待該識別項。然而，有時候它們會被簡稱為「名稱」。關鍵字和識別項的文法結構是相同的，意即不看整個命令的話，是無法辨別到底是識別項還是關鍵字的。完整的關鍵字列表，收錄在附件 C 當中。

SQL 識別項與關鍵字必須以英文字母開頭（a - z，也可以是附加符號和非拉丁字母，中文沒問題）或是底線（\_）。剩餘的字元可以是字母、底線、數字（0 - 9）、或錢字號（$）。注意錢字號，在標準 SQL 語法中是不允許使用的，所以可能會降低一些應用程式的可攜性。標準 SQL 也沒有定義包含數字或是以底線起迄的關鍵字，所以識別項這樣的形式定義是安全的，不會和標準未來的修訂相衝突。

資料庫系統不能使用長度超過 NAMEDATALEN -1 的識別項；太長的名稱仍然可以在命令中被輸入，但會被截斷。預設上，NAMEDATALEN 的設定是 64，所以最長的識別項名稱長度是 63 位元組。如果這個限制會造成困擾的話，你也可以調整 NAMEDATALEN 的編譯值，它的設定在 src/include/pg\_config\_manual.h 檔案中。

關鍵字和無引號識別項都是不分大小寫的，所以：

```
UPDATE MY_TABLE SET A = 5;
```

等同於：

```
uPDaTE my_TabLE SeT a = 5;
```

有一種寫法很常使用，就是把關鍵字用大寫表示，而識別項名稱使用小寫，例如：

```
UPDATE my_table SET a = 5;
```

第二種要介紹的識別項是，受限制的識別項，或是引號識別項。它的形式就是以雙引號括住的任何字串。受限制的識別項，就一定是識別項，不會是關鍵字。所以，「"select"」就會被識別為名稱為「select」的表格或欄位，而無引號的 select 就會被視為是關鍵字，也可能會產生解譯錯誤，如果剛好用在可能是表格或欄位名稱的位置上的話。使用引號識別項的例子如下：

```
UPDATE "my_table" SET "a" = 5;
```

引號識別項可以包含任何字元，除了字元碼為 0 的字元以外。（要包含雙引號字元的話，請使用連續兩個雙引號。）這可以用來建立原來不能使用的表格或欄位名稱，甚至是包含空白或＂&＂。但長度的限制仍然要遵守。

還有一種變形的引號識別項，允許包含跳脫的形式來表現萬國碼（unicode）。這種變形會以「U&」開頭（U大小寫皆可）緊接在前面的雙引號的前面，不能有任何空白在它們之間，例如：U&"foo"。（注意，這可能會和運算子的 & 產生混淆，但可以在運算子的 & 前後都加上空白來避免這個問題。）在雙引號內，萬國碼字元以跳脫的形式表現，也就是以倒斜線再接 4 位數的 16 進位碼，或倒斜線接一個加號再串一組 6 位數的 16 進位碼。例如，識別項 "data" 可以寫成這樣：

```
U&"d\0061t\+000061"
```

下面是稍微不簡明的例子是，俄文的＂slon＂（大象），以希伯萊文字母表現：

```
U&"\0441\043B\043E\043D"
```

如果希望以不同的跳脫字元來代替倒斜線的話，那麼可以雙引號結束後使用 UESCAPE 子句來指定，舉例來說：

```
U&"d!0061t!+000061" UESCAPE '!'
```

跳脫字元可以是任何的單一字元，除了 16 進位數字的字元、單引號、雙引號、或空白以外。注意指定的跳脫字元是以單引號括住，而不是雙引號。

內容要使用到跳脫字元的話，就重覆輸入 2 次。

萬國碼的跳脫語法，只能使用 UTF8 的編碼。如果有用到其他的編碼的話，只有在 ASCII 範圍（最大為 \007F）可以使用。4 位數及 6 位數的形式，可以組合配對用來指定 UTF-16 中，大於 U+FFFF 的字元，雖然 6 位數的形式單獨就可以解決這個問題（組合配對並不會直接被儲存起來，他們會被編碼成 UTF-8 再儲存。）

把識別項用引號括起來也可以用來保持它的大小寫狀態，沒有括起來的話，都會被轉成小寫字母。舉例來說，對 PostgreSQL 而言，FOO、foo、"foo"，三者都是一樣的，但 "Foo" 和 "FOO" 就彼此及前面三者都視為不同。（在 PostgreSQL 中，把未引號括起的名稱轉成小寫，並不是 SQL 的標準。SQL 標準反而是都轉成大寫。所以在 SQL 標準中，foo 應該是等同於 "FOO" 而不同於 "foo"。如果你要增加語法的可攜性的話，建議最好都使用引號括起特別的名稱，或者都不要使用引號。）

### 4.1.2. 常數

PostgreSQL 中有三種隱含型別的常數：字串、位元字串、和數值。常數也可以強制型別，有助於更精確的表達，也可以讓系統處理更有效率。接下來就開始進行相關的說明。

#### 4.1.2.1. 字串常數

在 SQL 中，所謂的字串常數，指的是用單引號括住的任意字元串列，例如：'This is a string'。如果在字串常數內需要有單引號的話就使用連續兩個單引號，例如：'Dianne''s horse'。注意這不是雙引號，是兩個單引號。

兩個字串常數如果只用空白及至少一個換行符號所分隔的話，那個它們會被連在一起，和寫成一個字串是一樣的。舉例來說：

```
SELECT 'foo'
'bar';
```

等同於：

```
SELECT 'foobar';
```

但如果是這樣：

```
SELECT 'foo'      'bar';
```

語法上就不正確了。（這是來自於 SQL 奇怪的常規，PostgreSQL 單純只是遵循。）

#### 4.1.2.2. C 語言樣式的跳脫字串常數

PostgreSQL 也支援跳脫字串常數，這些是 SQL 標準的延伸。跳脫字串常數使用的是字母 E （大小寫皆可），緊接著單引號所組成，例如：E'foo'。（如果字串有超過一行的話，也只要在第一個單引號前有 E 就可以了。）在跳脫字串當中，使用倒斜線開頭，就可以使用 C 語言式的倒斜線跳脫字串，通常是一個倒斜線再接一個字元，對應到一個特殊位元組的值，如 Table 4.1 所示。

**Table 4.1. 倒斜線跳腳字串（Backslash Escape Sequence）**

| **倒斜線跳腳字串** | 字元意義 |
| :--- | :--- |
| `\b` | backspace（倒退） |
| `\f` | form feed（換頁） |
| `\n` | newline（換行） |
| `\r` | carriage return（回到行首） |
| `\t` | tab（定位符號） |
| `\o`,`\oo`,`\ooo`\(`o`= 0 - 7\) | octal byte value（8 進位值） |
| `\xh`,`\xhh`\(`h`= 0 - 9, A - F\) | hexadecimal byte value（16 進位值） |
| `\uxxxx`,`\Uxxxxxxxx`\(`x`= 0 - 9, A - F\) | 16 or 32-bit hexadecimal Unicode character value（16 位元或 32 位元的 16 進位萬國碼字元值） |

任何其他接在倒斜線後面的字元都僅以原樣呈現。而如果要包含一個倒斜線的話，就使用連續兩個倒斜線輸入。同樣地，要包含一個單引號的話，可以使用跳脫字串 \' 輸入，也可以用一般連續兩個單引號的方式輸入。

你需要確保你所使用的 8 進位或 16 進位創建的位元組序列，都是屬於資料庫中合法的字元集。當資料庫編輯是 UTF-8 時，就應該使用萬國碼跳脫寫法，或其他萬國碼的輸入方式，如前 4.1.2.3 中所述。（所謂其他的方式可能是自行組合每一個位元組，但這樣會是相當麻煩的事。）

萬國碼跳脫語法只有在 UTF8 的編碼下才完整支援。當有其他的字元編碼被使用時，就只能使用 ASCII 的範圍（最大值為 \u007F）中的值。4 位數及 6 位數的型式可以用來配對指定 UTF-16 超過 U+FFFF 的字元，即使 6 位數的型式就足以解決這個問題。（當使用配對語法，且字元編碼為 UTF8 時，他們會先被合併成單一字元，然後再編碼成 UTF-8。）

### 注意

如果設定檔參數 standard\_conforming\_string 設定為 off，PostgreSQL 不論在一般字串還是跳脫字串常數，都會把倒斜線識別為跳脫符號。然而，在 PostgreSQL 9.1 之前，這個參數的預設值為 on，表示只在跳脫字串常數裡，才把倒斜線視為跳脫符號。這樣的模式是更與標準相容的，但可能會破壞默認舊有設定的應用程式，也就是總是把倒斜線視為跳脫符號。在這樣的背景之下，你可以把這個參數設為 off，但更好的是，修改程式不再使用倒斜線跳脫符號。如果你需要使用倒斜線跳脫符號來表示一個特殊字元，請使用 E 開頭的字串常數。

有關 standard\_conforming\_string，順帶一提的是，還有 escape\_string\_warning 和 backslash\_quote 兩個參數，也提供調整倒斜線在字串常數中的使用。

字元代碼 0 的字元不能使用在字串常數當中。

#### 4.1.2.3. String Constants with Unicode Escapes

PostgreSQL 也支援其他跳脫字串的語法，可以用來直接輸入任意的萬國碼字元。萬國碼跳脫字串常數是以 U& （U& 或 u& 皆可）開頭，然後緊接著單引號括住的字串，記得中間不能有任何空白，例如：U&'foo'。（注意這可能會混淆到 & 的使用，最好在其他使用 & 作為運算子的指令中，在 & 前後 加上空白字元，以避免這個問題。）在括住的內容裡，萬國碼字元可以使用跳脫字元來指定，也就是使用倒斜線再接一組 4 位數的 16 進位值，或者以倒斜線加上加號再接一組 6 位數的 16 進位值。舉個例子，字串 'data' 也可以寫成：

```
U&'d\0061t\+000061'
```

下面是稍微不簡明的例子是，俄文的＂slon＂（大象），以希伯萊文字母表現：

```
U&'\0441\043B\043E\043D'
```

如果希望以不同的跳脫字元來代替倒斜線的話，那麼可以雙引號結束後使用 UESCAPE 子句來指定，舉例來說：

```
U&'d!0061t!+000061' UESCAPE '!'
```

跳脫字元可以是任何的單一字元，除了 16 進位數字的字元、單引號、雙引號、或空白以外。

萬國碼跳脫語法只有在 UTF8 的編碼下才完整支援。當有其他的字元編碼被使用時，就只能使用 ASCII 的範圍（最大值為 \u007F）中的值。4 位數及 6 位數的型式可以用來配對指定 UTF-16 超過 U+FFFF 的字元，即使 6 位數的型式就足以解決這個問題。（當使用配對語法，且字元編碼為 UTF8 時，他們會先被合併成單一字元，然後再編碼成 UTF-8。）

然而，萬國碼的跳脫字串語法，只有在參數 standard\_conforming\_strings 設定為 on 時有效。這是因為這個語法可能會造成 SQL 指令在編譯時的困擾，造成 SQL 隱碼攻擊（SQL injection） 或其他安全性的問題。如果這個參數設定為 off，那麼這個語法就會被禁止，並且產生錯誤訊息。

內容要使用到跳脫字元的話，就重覆輸入 2 次。

#### 4.1.2.4. 錢字引號字串常數

標準的語法用於字串常數的設定很方便的，但如果字串裡有很多單引號或倒斜線，可讀性就很低了，因為它們都必須再連續多一個符號輸入。像這樣的例子，要改善可讀性的話，PostgreSQL 提供了另一個方式，稱作「錢字引號」（dollar quoting），來描述字串常數。錢字引號字串常數包含一個錢字號（$），可省略或多個字元所組成的「標籤」，另一個錢字號，組成字川的任何序列文字，再一個錢字號，與起始的錢字引號同樣的標籤，再一個錢字號。舉例來說，這裡有兩個不同使用錢字引號的方式，但都是「Dianne's horse」

```
$$Dianne's horse$$
$SomeTag$Dianne's horse$SomeTag$
```

注意在錢字引號字串中，單引號的使用就不需要跳脫處理了。實際上，在錢字引號字串中，沒有字元需要跳脫處理：字串內容就原樣輸出。倒斜錢並不特別，就算是錢字號也是，除非它們是引號標籤配對的一部份。

巢狀錢字字串常數是可以的，只要在不同層選擇不同的標籤就好。最常見的用途就是撰寫函數定義。舉例如下：

```
$function$
BEGIN
    RETURN ($1 ~ $q$[\t\r\n\v\\]$q$);
END;
$function$
```

這裡，「$q$\[\t\r\n\v\\]$q$」以錢字引號字串輸出就是「\[\t\r\n\v\\]」，作為 PostgreSQL 的函數內容。但這個字串並不會和外層的 $function$ 配對。對外層的字串而言，它只是被包裏的一部份字元而已。

以錢字符作為標籤（如果有的話）的引號字串和無引號的識別項，遵循相同的規則，除了它無法包含錢字符號以外。標籤是區分大小寫的，所以 $tag$String content$tag$ 是正確的，而 $TAG$String content$tag$ 是不合法的。

錢字引號字串緊接著關鍵字或識別項的話，就必須以空白分隔；否則錢字號的終止符可能會被當作前面識別項的一部份。

錢字引號並不是標準 SQL 的用法，但當撰寫一些複雜字串的時候，會比標準語法更為便利。當字串常數內嵌於另一個常數時，也是很好用的情境，像自訂函數時就時常用到。使用單引號的語法時，前面例子中的每一個倒斜線，需要使用 4 個倒斜線才能表示（原來字串常數時需要雙倒斜線，然後在執行階段時也需要雙倒斜線，一共就是 4 倍）。

#### 4.1.2.5. 位元字串常數（Bit-string Constants）

位元字串常數看起來就像是一般的字串常數，只是將 B（大小寫皆可）放在引號的前面（不能有空白），例如：B'1001'。而在位元字串當中，只能有 0 或 1 的存在。

另一方面，位元字串常數也可以表示一個 16 進位的值，使用的先導字為 X（大小寫皆可），例如：X'1FF'。這個撰寫方式與使用前段方式，以 4 位數 2 進位表示每一個 16 進位位數，是相同的結果。

這兩種位元字串常數的表達方式，都可以在字串中換行，如同一般的字串常數。錢字引號表示方式不能使用在位元字串常數上。

#### 4.1.2.6. Numeric Constants

Numeric constants are accepted in these general forms:

```
digits
digits
.[
digits
][
e[
+-
]
digits
]
[
digits
].
digits
[
e[
+-
]
digits
]

digits
e[
+-
]
digits
```

where\_`digits`\_is one or more decimal digits \(0 through 9\). At least one digit must be before or after the decimal point, if one is used. At least one digit must follow the exponent marker \(`e`\), if one is present. There cannot be any spaces or other characters embedded in the constant. Note that any leading plus or minus sign is not actually considered part of the constant; it is an operator applied to the constant.

These are some examples of valid numeric constants:

42  
3.5  
4.  
.001  
5e2  
1.925e-3

A numeric constant that contains neither a decimal point nor an exponent is initially presumed to be type`integer`if its value fits in type`integer`\(32 bits\); otherwise it is presumed to be type`bigint`if its value fits in type`bigint`\(64 bits\); otherwise it is taken to be type`numeric`. Constants that contain decimal points and/or exponents are always initially presumed to be type`numeric`.

The initially assigned data type of a numeric constant is just a starting point for the type resolution algorithms. In most cases the constant will be automatically coerced to the most appropriate type depending on context. When necessary, you can force a numeric value to be interpreted as a specific data type by casting it.For example, you can force a numeric value to be treated as type`real`\(`float4`\) by writing:

```
REAL '1.23'  -- string style
1.23::REAL   -- PostgreSQL (historical) style
```

These are actually just special cases of the general casting notations discussed next.

#### 4.1.2.7. Constants of Other Types

A constant of an\_arbitrary\_type can be entered using any one of the following notations:

```
type
 '
string
'
'
string
'::
type

CAST ( '
string
' AS 
type
 )
```

The string constant's text is passed to the input conversion routine for the type called`type`. The result is a constant of the indicated type. The explicit type cast can be omitted if there is no ambiguity as to the type the constant must be \(for example, when it is assigned directly to a table column\), in which case it is automatically coerced.

The string constant can be written using either regular SQL notation or dollar-quoting.

It is also possible to specify a type coercion using a function-like syntax:

```
typename
 ( '
string
' )
```

but not all type names can be used in this way; see[Section 4.2.9](https://www.postgresql.org/docs/10/static/sql-expressions.html#sql-syntax-type-casts)for details.

The`::`,`CAST()`, and function-call syntaxes can also be used to specify run-time type conversions of arbitrary expressions, as discussed in[Section 4.2.9](https://www.postgresql.org/docs/10/static/sql-expressions.html#sql-syntax-type-casts). To avoid syntactic ambiguity, the`type`'`string`'syntax can only be used to specify the type of a simple literal constant. Another restriction on the`type`'`string`'syntax is that it does not work for array types; use`::`or`CAST()`to specify the type of an array constant.

The`CAST()`syntax conforms to SQL. The`type`'`string`'syntax is a generalization of the standard: SQL specifies this syntax only for a few data types, butPostgreSQLallows it for all types. The syntax with`::`is historicalPostgreSQLusage, as is the function-call syntax.

### 4.1.3. Operators

An operator name is a sequence of up to`NAMEDATALEN`-1 \(63 by default\) characters from the following list:

* * \* / &lt;&gt; = ~ ! @ \# % ^ & \| \` ?

There are a few restrictions on operator names, however:

* `--`and`/*`cannot appear anywhere in an operator name, since they will be taken as the start of a comment.

* A multiple-character operator name cannot end in`+`or`-`, unless the name also contains at least one of these characters:

  ~ ! @ \# % ^ & \| \` ?

  For example,`@-`is an allowed operator name, but`*-`is not. This restriction allowsPostgreSQLto parse SQL-compliant queries without requiring spaces between tokens.

When working with non-SQL-standard operator names, you will usually need to separate adjacent operators with spaces to avoid ambiguity. For example, if you have defined a left unary operator named`@`, you cannot write`X*@Y`; you must write`X* @Y`to ensure thatPostgreSQLreads it as two operator names not one.

### 4.1.4. Special Characters

Some characters that are not alphanumeric have a special meaning that is different from being an operator. Details on the usage can be found at the location where the respective syntax element is described. This section only exists to advise the existence and summarize the purposes of these characters.

* A dollar sign \(`$`\) followed by digits is used to represent a positional parameter in the body of a function definition or a prepared statement. In other contexts the dollar sign can be part of an identifier or a dollar-quoted string constant.

* Parentheses \(`()`\) have their usual meaning to group expressions and enforce precedence. In some cases parentheses are required as part of the fixed syntax of a particular SQL command.

* Brackets \(`[]`\) are used to select the elements of an array. See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html)for more information on arrays.

* Commas \(`,`\) are used in some syntactical constructs to separate the elements of a list.

* The semicolon \(`;`\) terminates an SQL command. It cannot appear anywhere within a command, except within a string constant or quoted identifier.

* The colon \(`:`\) is used to select“slices”from arrays. \(See[Section 8.15](https://www.postgresql.org/docs/10/static/arrays.html).\) In certain SQL dialects \(such as Embedded SQL\), the colon is used to prefix variable names.

* The asterisk \(`*`\) is used in some contexts to denote all the fields of a table row or composite value. It also has a special meaning when used as the argument of an aggregate function, namely that the aggregate does not require any explicit parameter.

* The period \(`.`\) is used in numeric constants, and to separate schema, table, and column names.

### 4.1.5. Comments

A comment is a sequence of characters beginning with double dashes and extending to the end of the line, e.g.:

```
-- This is a standard SQL comment
```

Alternatively, C-style block comments can be used:

```
/* multiline comment
 * with nesting: /* nested block comment */
 */
```

where the comment begins with`/*`and extends to the matching occurrence of`*/`. These block comments nest, as specified in the SQL standard but unlike C, so that one can comment out larger blocks of code that might contain existing block comments.

A comment is removed from the input stream before further syntax analysis and is effectively replaced by whitespace.

### 4.1.6. Operator Precedence

[Table 4.2](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-precedence-table)shows the precedence and associativity of the operators inPostgreSQL. Most operators have the same precedence and are left-associative. The precedence and associativity of the operators is hard-wired into the parser.

You will sometimes need to add parentheses when using combinations of binary and unary operators. For instance:

```
SELECT 5 ! - 6;
```

will be parsed as:

```
SELECT 5 ! (- 6);
```

because the parser has no idea — until it is too late — that`!`is defined as a postfix operator, not an infix one. To get the desired behavior in this case, you must write:

```
SELECT (5 !) - 6;
```

This is the price one pays for extensibility.

**Table 4.2. Operator Precedence \(highest to lowest\)**

| Operator/Element | Associativity | Description |
| :--- | :--- | :--- |
| `.` | left | table/column name separator |
| `::` | left | PostgreSQL-style typecast |
| `[]` | left | array element selection |
| `+-` | right | unary plus, unary minus |
| `^` | left | exponentiation |
| `*/%` | left | multiplication, division, modulo |
| `+-` | left | addition, subtraction |
| \(any other operator\) | left | all other native and user-defined operators |
| `BETWEENINLIKEILIKESIMILAR` |  | range containment, set membership, string matching |
| `<>=<=>=<>` |  | comparison operators |
| `ISISNULLNOTNULL` |  | `IS TRUE`,`IS FALSE`,`IS NULL`,`IS DISTINCT FROM`, etc |
| `NOT` | right | logical negation |
| `AND` | left | logical conjunction |
| `OR` | left | logical disjunction |

Note that the operator precedence rules also apply to user-defined operators that have the same names as the built-in operators mentioned above. For example, if you define a“+”operator for some custom data type it will have the same precedence as the built-in“+”operator, no matter what yours does.

When a schema-qualified operator name is used in the`OPERATOR`syntax, as for example in:

```
SELECT 3 OPERATOR(pg_catalog.+) 4;
```

the`OPERATOR`construct is taken to have the default precedence shown in[Table 4.2](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html#sql-precedence-table)for“any other operator”. This is true no matter which specific operator appears inside`OPERATOR()`.

### Note

PostgreSQLversions before 9.5 used slightly different operator precedence rules. In particular,`<=>=`and`<>`used to be treated as generic operators;`IS`tests used to have higher priority; and`NOT BETWEEN`and related constructs acted inconsistently, being taken in some cases as having the precedence of`NOT`rather than`BETWEEN`. These rules were changed for better compliance with the SQL standard and to reduce confusion from inconsistent treatment of logically equivalent constructs. In most cases, these changes will result in no behavioral change, or perhaps in“no such operator”failures which can be resolved by adding parentheses. However there are corner cases in which a query might change behavior without any parsing error being reported. If you are concerned about whether these changes have silently broken something, you can test your application with the configuration parameter[operator\_precedence\_warning](https://www.postgresql.org/docs/10/static/runtime-config-compatible.html#guc-operator-precedence-warning)turned on to see if any warnings are logged.

---

[^1]: [PostgreSQL: Documentation: 10: 4.1. Lexical Structure](https://www.postgresql.org/docs/10/static/sql-syntax-lexical.html)

