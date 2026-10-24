<a id="ECPG-DEVELOP"></a>

## 34.17. 內部運作 [#](#ecpg-develop) <a href="#ecpg-develop" id="ecpg-develop"></a>

本節說明 ECPG 的內部運作方式。這些資訊有時可以幫助使用者理解如何使用 ECPG。

`ecpg` 寫入輸出的前四行是固定的。其中兩行是註解，兩行是與函式庫介接所需的 include 行。接著前置處理器會讀過整個檔案並寫出輸出。通常它只是將所有內容原樣輸出。

當它看到 `EXEC SQL` 陳述式時，就會介入並加以改寫。該命令以 `EXEC
SQL` 開頭，以 `;` 結尾。兩者之間的所有內容都會被視為 SQL 陳述式，並為了變數代換而進行剖析。

當符號以冒號（`:`）開頭時，就會進行變數代換。前置處理器會在先前於 `EXEC SQL DECLARE` 區段中宣告的變數裡，查找具有該名稱的變數。

函式庫中最重要的函式是 `ECPGdo`，它負責執行大多數的命令。它接受可變數量的引數。引數數量很容易就累積到 50 個左右，我們希望這在任何平台上都不會造成問題。

引數如下：

<a id="ECPG-DEVELOP-LINE-NUMBER"></a>

行號 [#](#ECPG-DEVELOP-LINE-NUMBER)
:   這是原始程式行的行號；只用於錯誤訊息。
<a id="ECPG-DEVELOP-STRING"></a>

字串 [#](#ECPG-DEVELOP-STRING)
:   這是要發出的 SQL 命令。它會依輸入變數而修改；輸入變數是指編譯時尚未得知、但要填入命令中的變數。字串中應放入變數的位置會是 `?`。
<a id="ECPG-DEVELOP-INPUT-VARIABLES"></a>

輸入變數 [#](#ECPG-DEVELOP-INPUT-VARIABLES)
:   每個輸入變數都會產生十個引數。（見下文。）
<a id="ECPG-DEVELOP-ECPGT-EOIT"></a>

*`ECPGt_EOIT`* [#](#ECPG-DEVELOP-ECPGT-EOIT)
:   一個 `enum` 值，表示後面已沒有其他輸入變數。
<a id="ECPG-DEVELOP-OUTPUT-VARIABLES"></a>

輸出變數 [#](#ECPG-DEVELOP-OUTPUT-VARIABLES)
:   每個輸出變數都會產生十個引數。（見下文。）這些變數由該函式填入。
<a id="ECPG-DEVELOP-ECPGT-EORT"></a>

*`ECPGt_EORT`* [#](#ECPG-DEVELOP-ECPGT-EORT)
:   一個 `enum` 值，表示後面已沒有其他變數。

對於 SQL 命令中的每個變數，此函式都會收到十個引數：

1. 以特殊符號表示的型別。
2. 指向值的指標，或指向該指標的指標。
3. 若變數為 `char` 或 `varchar`，則為變數的大小。
4. 陣列中的元素個數（用於陣列擷取）。
5. 到陣列中下一個元素的位移量（用於陣列擷取）。
6. 以特殊符號表示的指示變數型別。
7. 指向指示變數的指標。
8. 0
9. 指示變數陣列中的元素個數（用於陣列擷取）。
10. 到指示變數陣列中下一個元素的位移量（用於陣列擷取）。

請注意，並非所有 SQL 命令都以這種方式處理。例如，像下面這樣開啟游標的陳述式：

```

EXEC SQL OPEN cursor;
```

並不會被複製到輸出中。取而代之的是，在 `OPEN` 命令的位置使用該游標的 `DECLARE` 命令，因為實際開啟游標的正是它。

以下是一個完整範例，說明前置處理器處理檔案 `foo.pgc` 後的輸出（細節可能會隨前置處理器的版本而改變）：

```

EXEC SQL BEGIN DECLARE SECTION;
int index;
int result;
EXEC SQL END DECLARE SECTION;
...
EXEC SQL SELECT res INTO :result FROM mytable WHERE index = :index;
```

會被轉換為：

```

/* Processed by ecpg (2.6.0) */
/* These two include files are added by the preprocessor */
#include <ecpgtype.h>;
#include <ecpglib.h>;

/* exec sql begin declare section */

#line 1 "foo.pgc"

 int index;
 int result;
/* exec sql end declare section */
...
ECPGdo(__LINE__, NULL, "SELECT res FROM mytable WHERE index = ?     ",
        ECPGt_int,&(index),1L,1L,sizeof(int),
        ECPGt_NO_INDICATOR, NULL , 0L, 0L, 0L, ECPGt_EOIT,
        ECPGt_int,&(result),1L,1L,sizeof(int),
        ECPGt_NO_INDICATOR, NULL , 0L, 0L, 0L, ECPGt_EORT);
#line 147 "foo.pgc"
```

（此處的縮排是為了便於閱讀而加上的，並不是前置處理器產生的。）

譯註：上方輸出範例依原文保留，僅在此說明兩點：一是兩行 #include 指令的行尾多了分號，這不是正確的前置處理指令寫法（C 編譯器通常會對此發出警告），正確寫法行尾不應有分號；二是範例中 ECPGdo 在 __LINE__ 之後的 NULL 引數（連線名稱）並未列在上文的引數清單中，而目前版本的 ecpg 實際產生的 ECPGdo 呼叫在 SQL 字串之前還有更多引數，與此範例不同（如原文所述，細節會隨前置處理器版本而改變）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-develop.html)（原文版本：18.6；核對日期：2026-10-22）
