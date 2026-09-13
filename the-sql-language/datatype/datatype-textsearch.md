<a id="DATATYPE-TEXTSEARCH"></a>

## 8.11. 全文檢索型別 [#](#DATATYPE-TEXTSEARCH)

[8.11.1. `tsvector`](datatype-textsearch.md#DATATYPE-TSVECTOR)

[8.11.2. `tsquery`](datatype-textsearch.md#DATATYPE-TSQUERY)

<a id="id-1.5.7.19.2"></a><a id="id-1.5.7.19.3"></a>

PostgreSQL 提供兩種資料型別，用來支援全文檢索；所謂全文檢索，就是在一批自然語言*文件*中進行搜尋，以找出最符合某個*查詢*的那些文件。`tsvector` 型別以針對全文檢索最佳化過的形式表示一份文件；`tsquery` 型別則類似地表示一個文字查詢。[第 12 章](../textsearch/README.md)對這項功能有詳細的說明，而[第 9.13 節](../functions/functions-textsearch.md)則整理了相關的函式與運算子。

<a id="DATATYPE-TSVECTOR"></a>

### 8.11.1. `tsvector` [#](#DATATYPE-TSVECTOR)

<a id="id-1.5.7.19.5.2"></a>

`tsvector` 值是一份由不重複之*詞素*所組成的已排序清單，這些詞素是經過*正規化*處理、將同一個單字的不同變化形式合併後的字詞（詳情請參閱[第 12 章](../textsearch/README.md)）。排序與去除重複的工作會在輸入時自動完成，如以下範例所示：

```

SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector;
                      tsvector
----------------------------------------------------
 'a' 'and' 'ate' 'cat' 'fat' 'mat' 'on' 'rat' 'sat'
```

若要表示含有空白字元或標點符號的詞素，請用引號把它們括起來：

```

SELECT $$the lexeme '    ' contains spaces$$::tsvector;
                 tsvector
-------------------------------------------
 '    ' 'contains' 'lexeme' 'spaces' 'the'
```

（在這個例子與下一個例子中，我們使用以錢字號括起的字串常數，以避免在常數中還要把引號寫成兩個而造成混淆。）內嵌的引號與反斜線必須寫成兩個：

```

SELECT $$the lexeme 'Joe''s' contains a quote$$::tsvector;
                    tsvector
------------------------------------------------
 'Joe''s' 'a' 'contains' 'lexeme' 'quote' 'the'
```

此外，也可以選擇為詞素附上整數*位置*：

```

SELECT 'a:1 fat:2 cat:3 sat:4 on:5 a:6 mat:7 and:8 ate:9 a:10 fat:11 rat:12'::tsvector;
                                  tsvector
-------------------------------------------------------------------​------------
 'a':1,6,10 'and':8 'ate':9 'cat':3 'fat':2,11 'mat':7 'on':5 'rat':12 'sat':4
```

位置通常代表來源單字在文件中的所在位置。位置資訊可以用於*鄰近度排名*。位置值的範圍可以是 1 到 16383；更大的數字會被靜默地設為 16383。同一個詞素若有重複的位置，重複的部分會被捨棄。

具有位置的詞素還可以再標上*權重*，權重可以是 `A`、`B`、`C` 或 `D`。`D` 是預設值，因此不會顯示在輸出中：

```

SELECT 'a:1A fat:2B,4C cat:5D'::tsvector;
          tsvector
----------------------------
 'a':1A 'cat':5 'fat':2B,4C
```

權重通常用來反映文件結構，例如把標題中的字詞與內文中的字詞做不同的標記。全文檢索的排名函式可以為不同的權重標記指定不同的優先程度。

有一點很重要必須瞭解：`tsvector` 型別本身並不會執行任何字詞正規化；它假設所給定的字詞已經針對應用程式做過適當的正規化。例如，

```

SELECT 'The Fat Rats'::tsvector;
      tsvector
--------------------
 'Fat' 'Rats' 'The'
```

對大多數英文文字搜尋的應用程式而言，上述字詞會被視為未經正規化，但 `tsvector` 並不在意。原始的文件文字通常應該先經過 `to_tsvector` 處理，才能把字詞正規化成適合搜尋的形式：

```

SELECT to_tsvector('english', 'The Fat Rats');
   to_tsvector
-----------------
 'fat':2 'rat':3
```

同樣地，更多細節請參閱[第 12 章](../textsearch/README.md)。

<a id="DATATYPE-TSQUERY"></a>

### 8.11.2. `tsquery` [#](#DATATYPE-TSQUERY)

<a id="id-1.5.7.19.6.2"></a>

`tsquery` 值儲存要搜尋的詞素，並且可以使用布林運算子 `&`（AND）、`|`（OR）與 `!`（NOT），以及片語搜尋運算子 `<->`（FOLLOWED BY）來組合它們。FOLLOWED BY 運算子還有一種變體 `<N>`，其中 *`N`* 是一個整數常數，用來指定所要搜尋的兩個詞素之間的距離。`<->` 等同於 `<1>`。

可以使用小括號來強制這些運算子的分組方式。在沒有小括號的情況下，`!`（NOT）的結合力最強，其次是 `<->`（FOLLOWED BY），再來是 `&`（AND），而 `|`（OR）的結合力最弱。

以下是一些例子：

```

SELECT 'fat & rat'::tsquery;
    tsquery
---------------
 'fat' & 'rat'

SELECT 'fat & (rat | cat)'::tsquery;
          tsquery
---------------------------
 'fat' & ( 'rat' | 'cat' )

SELECT 'fat & rat & ! cat'::tsquery;
        tsquery
------------------------
 'fat' & 'rat' & !'cat'
```

此外，`tsquery` 中的詞素也可以標上一個或多個權重字母，這會限制它們只能比對具有其中某個權重的 `tsvector` 詞素：

```

SELECT 'fat:ab & cat'::tsquery;
    tsquery
------------------
 'fat':AB & 'cat'
```

另外，`tsquery` 中的詞素也可以標上 `*`，以指定進行前綴比對：

```

SELECT 'super:*'::tsquery;
  tsquery
-----------
 'super':*
```

這個查詢會比對 `tsvector` 中任何以「super」開頭的字詞。

詞素的引號規則與前面針對 `tsvector` 中詞素所述的規則相同；而且與 `tsvector` 一樣，字詞所需的任何正規化都必須在轉換成 `tsquery` 型別之前完成。`to_tsquery` 函式可以方便地執行這類正規化：

```

SELECT to_tsquery('Fat:ab & Cats');
    to_tsquery
------------------
 'fat':AB & 'cat'
```

請注意，`to_tsquery` 處理前綴的方式與處理其他字詞相同，這表示以下這個比較會回傳 true：

```

SELECT to_tsvector( 'postgraduate' ) @@ to_tsquery( 'postgres:*' );
 ?column?
----------
 t
```

因為 `postgres` 會被取詞幹為 `postgr`：

```

SELECT to_tsvector( 'postgraduate' ), to_tsquery( 'postgres:*' );
  to_tsvector  | to_tsquery
---------------+------------
 'postgradu':1 | 'postgr':*
```

而它會比對到 `postgraduate` 的詞幹形式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-textsearch.html)（原文版本：18.6；核對日期：2026-09-12）
