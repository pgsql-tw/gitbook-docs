<a id="ERROR-STYLE-GUIDE"></a>

## 55.3. 錯誤訊息風格指南 [#](#error-style-guide) <a href="#error-style-guide" id="error-style-guide"></a>

提供這份風格指南，是希望 PostgreSQL 所產生的所有訊息都能維持一致、對使用者友善的風格。

<a id="ERROR-STYLE-GUIDE-WHAT-GOES-WHERE"></a>

### 什麼內容放在哪裡 [#](#error-style-guide-what-goes-where) <a href="#error-style-guide-what-goes-where" id="error-style-guide-what-goes-where"></a>

主要訊息應該簡短、陳述事實，並避免提及實作細節，例如特定的函式名稱。「簡短」的意思是「在一般情況下應該能放在一行之內」。如果需要讓主要訊息保持簡短，或者你覺得需要提及實作細節（例如失敗的是哪一個系統呼叫），請使用詳細訊息。主要訊息與詳細訊息都應該陳述事實。關於如何修正問題的建議，請使用提示訊息，尤其是當該建議不一定總是適用的時候。

例如，不要寫成：

```

IpcMemoryCreate: shmget(key=%d, size=%u, 0%o) failed: %m
(plus a long addendum that is basically a hint)
```

而要寫成：

```

Primary:    could not create shared memory segment: %m
Detail:     Failed syscall was shmget(key=%d, size=%u, 0%o).
Hint:       The addendum, written as a complete sentence.
```

理由：讓主要訊息保持簡短有助於切中要點，也讓用戶端在安排畫面空間時，可以假設錯誤訊息只需要一行就夠了。詳細訊息與提示訊息可以移到詳盡模式中顯示，或者也許放在彈出式的錯誤細節視窗中。此外，為了節省空間，詳細與提示訊息通常不會寫入伺服器日誌。最好避免提及實作細節，因為不能預期使用者會知道這些細節。

<a id="ERROR-STYLE-GUIDE-FORMATTING"></a>

### 格式 [#](#error-style-guide-formatting) <a href="#error-style-guide-formatting" id="error-style-guide-formatting"></a>

不要在訊息文字中加入任何關於格式的特定假設。要預期用戶端與伺服器日誌會依照它們自己的需要來換行。在較長的訊息中，可以使用換行字元（\n）來表示建議的分段位置。不要以換行字元結束訊息。不要使用定位字元（tab）或其他格式字元。（在顯示錯誤情境時，會自動加上換行來分隔各層情境，例如函式呼叫。）

理由：訊息不一定會顯示在終端機類型的顯示裝置上。在 GUI 顯示畫面或瀏覽器中，這些格式指示充其量只會被忽略。

<a id="ERROR-STYLE-GUIDE-QUOTATION-MARKS"></a>

### 引號 [#](#error-style-guide-quotation-marks) <a href="#error-style-guide-quotation-marks" id="error-style-guide-quotation-marks"></a>

英文文字在適合使用引號時應該使用雙引號。其他語言的文字應該一致地使用同一種引號，並與出版慣例以及其他程式的電腦輸出保持一致。

理由：選擇雙引號而不是單引號多少有點隨意，但往往是較受偏好的用法。有人建議依照 SQL 慣例，根據物件的類型來選擇引號種類（也就是字串用單引號、識別字用雙引號）。但這是程式語言內部的技術問題，許多使用者甚至並不熟悉；它無法推廣到其他種類的引用詞語；它無法套用到其他語言；而且它也相當沒有意義。

<a id="ERROR-STYLE-GUIDE-QUOTES"></a>

### 引號的使用 [#](#error-style-guide-quotes) <a href="#error-style-guide-quotes" id="error-style-guide-quotes"></a>

一律使用引號來界定檔案名稱、使用者提供的識別字、設定變數名稱，以及其他可能包含文字的變數。不要用引號來標示不會包含文字的變數（例如運算子名稱）。

後端中有些函式會視需要自行為其輸出加上雙引號（例如 `format_type_be()`）。不要在這類函式的輸出周圍再加上額外的引號。

理由：物件的名稱在嵌入訊息時可能造成混淆。要一致地標示出嵌入的名稱從哪裡開始、到哪裡結束。但不要讓不必要或重複的引號弄亂訊息。

<a id="ERROR-STYLE-GUIDE-GRAMMAR-PUNCTUATION"></a>

### 文法與標點符號 [#](#error-style-guide-grammar-punctuation) <a href="#error-style-guide-grammar-punctuation" id="error-style-guide-grammar-punctuation"></a>

主要錯誤訊息與詳細／提示訊息的規則不同：

主要錯誤訊息：第一個字母不要大寫。訊息結尾不要加句點。連想都別想以驚嘆號結束訊息。

詳細與提示訊息：使用完整的句子，並且每句都以句點結尾。句子的第一個字要大寫。如果後面還有另一個句子，句點之後要空兩格（適用於英文文字；在其他語言中可能不適當）。

錯誤情境字串：第一個字母不要大寫，字串結尾也不要加句點。情境字串通常不應該是完整的句子。

理由：避免使用標點符號，可以讓用戶端應用程式更容易把訊息嵌入各種不同的文法情境中。反正主要訊息往往本來就不是文法上完整的句子。（而如果它們長到超過一個句子，就應該拆成主要與詳細兩部分。）不過，詳細與提示訊息比較長，可能需要包含多個句子。為了一致起見，即使只有一個句子，它們也應該遵循完整句子的風格。

<a id="ERROR-STYLE-GUIDE-CASE"></a>

### 大寫與小寫 [#](#error-style-guide-case) <a href="#error-style-guide-case" id="error-style-guide-case"></a>

訊息的用字使用小寫，包括主要錯誤訊息的第一個字母。如果訊息中出現 SQL 命令與關鍵字，則使用大寫。

理由：由於有些訊息是完整的句子、有些不是，這樣做比較容易讓所有訊息看起來更一致。

<a id="ERROR-STYLE-GUIDE-PASSIVE-VOICE"></a>

### 避免被動語態 [#](#error-style-guide-passive-voice) <a href="#error-style-guide-passive-voice" id="error-style-guide-passive-voice"></a>

使用主動語態。當有一個執行動作的主詞時，使用完整的句子（「A could not do B」）。如果主詞會是程式本身，則使用省略主詞的電報式寫法；不要用「I」來指稱程式。

理由：程式不是人。不要假裝它是。

<a id="ERROR-STYLE-GUIDE-TENSE"></a>

### 現在式與過去式 [#](#error-style-guide-tense) <a href="#error-style-guide-tense" id="error-style-guide-tense"></a>

如果嘗試做某件事失敗了，但下次也許能夠成功（也許是在修正某個問題之後），使用過去式。如果失敗確定是永久性的，則使用現在式。

下面兩種形式的句子之間，存在不容忽視的語意差異：

```

could not open file "%s": %m
```

與：

```

cannot open file "%s"
```

第一種的意思是嘗試開啟檔案失敗了。訊息應該提供原因，例如「disk full」（磁碟已滿）或「file doesn't exist」（檔案不存在）。使用過去式是適當的，因為下一次磁碟可能已經不再是滿的，或者該檔案可能已經存在。

第二種形式表示程式根本沒有開啟該指定檔案的功能，或者這在概念上是不可能的。使用現在式是適當的，因為這種狀況會無限期地持續下去。

理由：誠然，一般使用者無法單憑訊息的時態得出什麼重大結論，但既然語言提供了文法，我們就應該正確地使用它。

<a id="ERROR-STYLE-GUIDE-OBJECT-TYPE"></a>

### 物件的類型 [#](#error-style-guide-object-type) <a href="#error-style-guide-object-type" id="error-style-guide-object-type"></a>

提到物件名稱時，要說明它是哪一種物件。

理由：否則沒有人會知道「foo.bar.baz」指的是什麼。

<a id="ERROR-STYLE-GUIDE-BRACKETS"></a>

### 方括號 [#](#error-style-guide-brackets) <a href="#error-style-guide-brackets" id="error-style-guide-brackets"></a>

方括號只能用於 (1) 在命令語法摘要中表示選用的引數，或 (2) 表示陣列下標。

理由：其他任何用法都不符合廣為人知的慣用法，會讓人感到困惑。

<a id="ERROR-STYLE-GUIDE-ERROR-MESSAGES"></a>

### 組合錯誤訊息 [#](#error-style-guide-error-messages) <a href="#error-style-guide-error-messages" id="error-style-guide-error-messages"></a>

當訊息中包含在其他地方產生的文字時，請以這種風格嵌入：

```

could not open file %s: %m
```

理由：要考慮到所有可能的錯誤代碼，把這段文字貼成一個通順的句子會很困難，所以需要某種標點符號。也有人建議把嵌入的文字放在括號中，但如果嵌入的文字很可能是訊息中最重要的部分（這是常有的情況），這樣做就不自然。

<a id="ERROR-STYLE-GUIDE-ERROR-REASONS"></a>

### 錯誤的原因 [#](#error-style-guide-error-reasons) <a href="#error-style-guide-error-reasons" id="error-style-guide-error-reasons"></a>

訊息應該一律說明錯誤發生的原因。例如：

```

BAD:    could not open file %s
BETTER: could not open file %s (I/O failure)
```

如果不知道原因，你最好去修正程式碼。

<a id="ERROR-STYLE-GUIDE-FUNCTION-NAMES"></a>

### 函式名稱 [#](#error-style-guide-function-names) <a href="#error-style-guide-function-names" id="error-style-guide-function-names"></a>

不要在錯誤文字中包含回報錯誤之常式的名稱。在需要時，我們有其他機制可以找出這一點，而且對大多數使用者來說，這不是有幫助的資訊。如果錯誤文字少了函式名稱就不太說得通，那就換個說法。

```

BAD:    pg_strtoint32: error in "z": cannot parse "z"
BETTER: invalid input syntax for type integer: "z"
```

也要避免提及被呼叫的函式名稱；改為說明程式碼原本試圖做什麼：

```

BAD:    open() failed: %m
BETTER: could not open file %s: %m
```

如果真的看起來有必要，請在詳細訊息中提及系統呼叫。（在某些情況下，提供實際傳給系統呼叫的值，可能是適合放在詳細訊息中的資訊。）

理由：使用者不知道那些函式都在做什麼。

<a id="ERROR-STYLE-GUIDE-TRICKY-WORDS"></a>

### 應避免的棘手用字 [#](#error-style-guide-tricky-words) <a href="#error-style-guide-tricky-words" id="error-style-guide-tricky-words"></a>

**Unable（無法）。**
「Unable」幾乎就是被動語態。視情況改用「cannot」或「could not」比較好。

**Bad（不良）。**
像「bad result」這樣的錯誤訊息，實在很難合理地解讀。最好寫出結果為什麼「bad」，例如「invalid format」。

**Illegal（非法）。**
「Illegal」表示違反法律，其餘情況都是「invalid」。更好的做法是說明它為什麼無效。

**Unknown（未知）。**
盡量避免使用「unknown」。想想看「error: unknown response」這樣的訊息。如果你不知道回應是什麼，又怎麼知道它是錯誤的？「Unrecognized」通常是更好的選擇。另外，務必要包含被抱怨的那個值。

```

BAD:    unknown node type
BETTER: unrecognized node type: 42
```

**Find 與 Exists。**
如果程式使用了一個不簡單的演算法來找出某項資源（例如路徑搜尋），而該演算法失敗了，那麼說程式無法「find」（找到）該資源是合理的。反之，如果資源的預期位置是已知的，但程式無法在那裡存取它，那就說該資源不「exist」（存在）。在這種情況下使用「find」聽起來語氣薄弱，而且會混淆問題。

**May、Can 與 Might。**
「May」暗示許可（例如「You may borrow my rake.」），在文件或錯誤訊息中用處不大。「Can」暗示能力（例如「I can lift that log.」），而「might」暗示可能性（例如「It might rain today.」）。使用正確的字可以釐清意義，並有助於翻譯。

**縮寫形式。**
避免使用縮寫形式，例如「can't」；改用「cannot」。

**Non-negative（非負）。**
避免使用「non-negative」，因為它對於是否接受零有歧義。最好使用「greater than zero」或「greater than or equal to zero」。

<a id="ERROR-STYLE-GUIDE-SPELLING"></a>

### 正確拼寫 [#](#error-style-guide-spelling) <a href="#error-style-guide-spelling" id="error-style-guide-spelling"></a>

要把字完整拼寫出來。例如，避免使用：

* spec
* stats
* parens
* auth
* xact

理由：這能提高一致性。

<a id="ERROR-STYLE-GUIDE-LOCALIZATION"></a>

### 在地化 [#](#error-style-guide-localization) <a href="#error-style-guide-localization" id="error-style-guide-localization"></a>

請記住，錯誤訊息文字需要被翻譯成其他語言。請遵循[第 56.2.2 節](../nls/nls-programmer.md#nls-guidelines)中的準則，以免讓譯者的工作變得困難。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/error-style-guide.html)（原文版本：18.6；核對日期：2026-10-12）
