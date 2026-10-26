<a id="PARSER-STAGE"></a>

## 51.3. 剖析器階段 [#](#parser-stage) <a href="#parser-stage" id="parser-stage"></a>

[51.3.1. 剖析器](parser-stage.md#parser-stage-parser)

[51.3.2. 轉換程序](parser-stage.md#parser-stage-transformation-process)

*剖析器階段*由兩個部分組成：

* 定義在 `gram.y` 與 `scan.l` 中的*剖析器*，是使用 Unix 工具 bison 與 flex 建置而成。
* *轉換程序*會對剖析器傳回的資料結構進行修改與擴充。

<a id="PARSER-STAGE-PARSER"></a>

### 51.3.1. 剖析器 [#](#parser-stage-parser) <a href="#parser-stage-parser" id="parser-stage-parser"></a>

剖析器必須檢查查詢字串（以純文字形式傳入）的語法是否有效。若語法正確，就會建構一棵*剖析樹*並將其傳回；否則會傳回錯誤。剖析器與詞法分析器是使用知名的 Unix 工具 bison 與 flex 實作的。

*詞法分析器*定義在檔案 `scan.l` 中，負責辨識*識別字*、*SQL 關鍵字*等。每找到一個關鍵字或識別字，就會產生一個*語彙單元（token）*並交給剖析器。

剖析器定義在檔案 `gram.y` 中，由一組*文法規則*與每當規則被觸發時所執行的*動作*組成。這些動作的程式碼（實際上是 C 程式碼）用來建構剖析樹。

檔案 `scan.l` 會使用程式 flex 轉換成 C 原始檔 `scan.c`，而 `gram.y` 則會使用 bison 轉換成 `gram.c`。完成這些轉換之後，就可以使用一般的 C 編譯器來建立剖析器。絕對不要修改產生出來的 C 檔案，因為下一次呼叫 flex 或 bison 時，它們會被覆寫。

### 注意

上述的轉換與編譯通常會使用 PostgreSQL 原始碼發行版本所附的 *makefile* 自動完成。

詳細說明 bison 或 `gram.y` 中的文法規則，已超出本手冊的範圍。有許多書籍與文件探討 flex 與 bison。在開始研究 `gram.y` 中的文法之前，你應該先熟悉 bison，否則你將無法理解其中發生了什麼事。

<a id="PARSER-STAGE-TRANSFORMATION-PROCESS"></a>

### 51.3.2. 轉換程序 [#](#parser-stage-transformation-process) <a href="#parser-stage-transformation-process" id="parser-stage-transformation-process"></a>

剖析器階段只使用關於 SQL 語法結構的固定規則來建立剖析樹。它不會在系統目錄中進行任何查找，因此不可能理解所要求之操作的詳細語意。剖析器完成之後，*轉換程序*會以剖析器傳回的樹作為輸入，並進行必要的語意解讀，以了解查詢參照了哪些資料表、函式與運算子。為了表示這些資訊而建構的資料結構稱為*查詢樹*。

將原始剖析與語意分析分開的原因是，系統目錄的查找只能在交易內進行，而我們不希望在收到查詢字串時就立即開始一個交易。原始剖析階段已足以識別交易控制命令（`BEGIN`、`ROLLBACK` 等），而這些命令隨後不需任何進一步分析就能正確執行。一旦確定要處理的是實際的查詢（例如 `SELECT` 或 `UPDATE`），若尚未處於交易中，就可以開始一個交易。只有到了這個時候，才能呼叫轉換程序。

轉換程序所建立的查詢樹，在大部分地方的結構都與原始剖析樹類似，但在細節上有許多差異。例如，剖析樹中的 `FuncCall` 節點代表語法上看起來像函式呼叫的東西。視所參照的名稱最後是一般函式還是彙總函式而定，它可能會被轉換成 `FuncExpr` 或 `Aggref` 節點。此外，欄位與運算式結果的實際資料型別資訊也會加入查詢樹中。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/parser-stage.html)（原文版本：18.6；核對日期：2026-10-12）
