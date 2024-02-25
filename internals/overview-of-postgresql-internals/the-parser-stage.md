---
description: 解析器階段
---

# 52.3. 解析器階段

解析器階段由兩部分組合：

* 解析器是透過 Unix 工具 bison 跟 flex  實作出來的並定義在 gram.y 和 scan.l 中。
* 轉換處理(transformation process) 負責將解析器產生出來的資料結構進行修改和加強。

## 52.3.1. 解析器

語法解析器必須檢查送過來的明文查詢字串是否語法正確。如果語法正確會建立一個解析樹( parser tree)並回傳，否則將回傳一個錯誤。語法解析器與詞法解析器是透過著名的 Unix 工具 bison 跟 flex 實作的。

詞法解析器定義在 `scan.l 檔案裡，負責解析 identifiers、SQL keywords 等等。對於每一個找到的 identifier、keyword 會產生一個 token 並回傳給語法解析器。`

語法解析器定義在 `gram.y` 檔案裡由一組 `grammer rules` 和 `actions` 所組成，每當滿足一個 rule 的時候就會觸發對應的 action (由 C 語言實作) 並建立出對應的解析樹。

flex 程式將檔案 `scan.l` 轉換成 `scan.c` C 語言檔案，`bison` 將檔案 `gram.y` 轉換成 `gram.c` C 語言檔案。轉換結束後，C 編譯器就能編譯這些檔案並建立解析器。不應該對這些產生出來的 C 檔案做任何修改，因為每次 flex 或 bison 都會改寫這些檔案。

#### 註記

> 前面提到的轉換和編譯是由定義在 PostgreSQL source code 內的 makefiles 所執行。

對於 bison 或是 `gram.y` 中的語法規則的介紹超出了本文件的教學範圍。有許多相關的書本或是文件都在介紹 flex 和 bison。建議在學習 `gram.y` 中的語法前，先了解 bison 的相關原理，才不會很難理解。

## 52.3.2.&#x20;
