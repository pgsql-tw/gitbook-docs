<a id="DATATYPE-XML"></a>

## 8.13. XML 型別 [#](#DATATYPE-XML)

[8.13.1. 建立 XML 值](datatype-xml.md#DATATYPE-XML-CREATING)

[8.13.2. 編碼處理](datatype-xml.md#DATATYPE-XML-ENCODING-HANDLING)

[8.13.3. 存取 XML 值](datatype-xml.md#DATATYPE-XML-ACCESSING-XML-VALUES)

<a id="id-1.5.7.21.2"></a>

`xml` 資料型別可以用來儲存 XML 資料。相較於把 XML 資料存放在 `text` 欄位中，它的優點是會檢查輸入值是否格式正確，而且有支援函式可以對它執行型別安全的操作；請參閱[第 9.15 節](../functions/functions-xml.md)。要使用這個資料型別，安裝環境必須是以 `configure --with-libxml` 建置的。

`xml` 型別可以儲存 XML 標準所定義之格式正確的「文件」，也可以儲存「內容」片段；後者是參照 XQuery 與 XPath 資料模型中較為寬鬆的[「文件節點」](https://www.w3.org/TR/2010/REC-xpath-datamodel-20101214/#DocumentNode)所定義的。大致上，這表示內容片段可以有一個以上的頂層元素或字元節點。運算式 `xmlvalue IS DOCUMENT` 可以用來判斷某個 `xml` 值是完整的文件，還是只是一個內容片段。

`xml` 資料型別的限制與相容性注意事項可以在[第 D.3 節](../../appendixes/features/xml-limits-conformance.md)找到。

<a id="DATATYPE-XML-CREATING"></a>

### 8.13.1. 建立 XML 值 [#](#DATATYPE-XML-CREATING)

若要從字元資料產生 `xml` 型別的值，請使用 `xmlparse` 函式：<a id="id-1.5.7.21.6.2.3"></a>

```

XMLPARSE ( { DOCUMENT | CONTENT } value)
```

範例：

```

XMLPARSE (DOCUMENT '<?xml version="1.0"?><book><title>Manual</title><chapter>...</chapter></book>')
XMLPARSE (CONTENT 'abc<foo>bar</foo><bar>foo</bar>')
```

雖然依照 SQL 標準，這是把字元字串轉換成 XML 值的唯一方式，但也可以使用 PostgreSQL 特有的語法：

```

xml '<foo>bar</foo>'
'<foo>bar</foo>'::xml
```

`xml` 型別不會依照文件型別宣告（DTD）來驗證輸入值，<a id="id-1.5.7.21.6.3.2"></a>即使輸入值本身指定了 DTD 也一樣。目前也沒有內建支援依照其他 XML 綱要語言（例如 XML Schema）進行驗證。

相反的操作，也就是從 `xml` 產生字元字串值，則是使用 `xmlserialize` 函式：<a id="id-1.5.7.21.6.4.3"></a>

```

XMLSERIALIZE ( { DOCUMENT | CONTENT } value AS type [ [ NO ] INDENT ] )
```

*`type`* 可以是 `character`、`character varying` 或 `text`（或這些型別的別名）。同樣地，依照 SQL 標準，這是在 `xml` 型別與字元型別之間轉換的唯一方式，但 PostgreSQL 也允許你直接對該值進行型別轉換。

`INDENT` 選項會讓結果以美化的方式排版，而 `NO INDENT`（這是預設值）則只會輸出原本的輸入字串。轉換成字元型別同樣會產生原本的字串。

當字元字串值與 `xml` 型別之間的轉換，並未分別透過 `XMLPARSE` 或 `XMLSERIALIZE` 進行時，要採用 `DOCUMENT` 還是 `CONTENT`，是由「XML option」
<a id="id-1.5.7.21.6.6.7"></a>
這個工作階段組態參數決定的，它可以用標準指令來設定：

```

SET XML OPTION { DOCUMENT | CONTENT };
```

或使用比較有 PostgreSQL 風格的語法

```

SET xmloption TO { DOCUMENT | CONTENT };
```

預設值是 `CONTENT`，因此各種形式的 XML 資料都被允許。

<a id="DATATYPE-XML-ENCODING-HANDLING"></a>

### 8.13.2. 編碼處理 [#](#DATATYPE-XML-ENCODING-HANDLING)

在處理用戶端、伺服器，以及在兩者之間傳遞的 XML 資料中的多種字元編碼時，必須格外小心。當使用文字模式把查詢傳給伺服器、把查詢結果傳給用戶端時（這是一般的模式），PostgreSQL 會把在用戶端與伺服器之間雙向傳遞的所有字元資料，轉換成各自那一端的字元編碼；請參閱[第 23.3 節](../../server-administration/charset/multibyte.md)。這也包括 XML 值的字串表示法，例如上面那些例子。這通常表示，當字元資料在用戶端與伺服器之間往返而被轉換成其他編碼時，XML 資料中所含的編碼宣告可能會變得不正確，因為內嵌的編碼宣告並不會被更動。為了因應這種行為，提供給 `xml` 型別作為輸入之字元字串中所含的編碼宣告會被*忽略*，並假設內容採用目前的伺服器編碼。因此，為了正確處理，XML 資料的字元字串必須由用戶端以目前的用戶端編碼送出。用戶端有責任在把文件送往伺服器之前先將其轉換成目前的用戶端編碼，或是適當地調整用戶端編碼。在輸出時，`xml` 型別的值不會帶有編碼宣告，用戶端應該假設所有資料都採用目前的用戶端編碼。

當使用二進位模式把查詢參數傳給伺服器、把查詢結果傳回用戶端時，並不會進行編碼轉換，因此情況有所不同。在這種情況下，XML 資料中的編碼宣告會被遵循；如果沒有編碼宣告，資料則會被假設為 UTF-8（這是 XML 標準的要求；請注意，PostgreSQL 並不支援 UTF-16）。在輸出時，資料會帶有指定用戶端編碼的編碼宣告，除非用戶端編碼就是 UTF-8，這時就會省略編碼宣告。

不用說，如果 XML 資料編碼、用戶端編碼與伺服器編碼都相同，用 PostgreSQL 處理 XML 資料就比較不容易出錯，效率也比較高。由於 XML 資料在內部是以 UTF-8 處理的，所以當伺服器編碼也是 UTF-8 時，運算的效率會最好。

### 警示

當伺服器編碼不是 UTF-8 時，有些與 XML 相關的函式對非 ASCII 資料可能完全無法運作。已知這對 `xmltable()` 與 `xpath()` 尤其是個問題。

<a id="DATATYPE-XML-ACCESSING-XML-VALUES"></a>

### 8.13.3. 存取 XML 值 [#](#DATATYPE-XML-ACCESSING-XML-VALUES)

`xml` 資料型別很特別的一點是，它並未提供任何比較運算子。這是因為對 XML 資料而言，並沒有定義明確且普遍適用的比較演算法。這麼做的一個後果是，你無法藉由把 `xml` 欄位與搜尋值做比較來取得資料列。因此，XML 值通常應該搭配一個獨立的鍵欄位，例如 ID。比較 XML 值的另一種替代做法，是先把它們轉換成字元字串，但請注意，字元字串比較與有用的 XML 比較方法幾乎毫無關係。

由於 `xml` 資料型別沒有比較運算子，因此無法直接在這種型別的欄位上建立索引。如果希望能快速搜尋 XML 資料，可行的變通做法包括把運算式轉換成字元字串型別並為它建立索引，或是為某個 XPath 運算式建立索引。當然，實際的查詢也必須調整成依照被索引的運算式來搜尋。

PostgreSQL 中的全文檢索功能也可以用來加速對 XML 資料的整份文件搜尋。不過，PostgreSQL 發行版本中目前還沒有提供必要的前置處理支援。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-xml.html)（原文版本：18.6；核對日期：2026-09-13）
