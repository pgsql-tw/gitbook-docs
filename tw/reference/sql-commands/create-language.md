# CREATE LANGUAGE

CREATE LANGUAGE — 宣告一種新的程序語言

### 語法

```text
CREATE [ OR REPLACE ] [ PROCEDURAL ] LANGUAGE name
CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE name
    HANDLER call_handler [ INLINE inline_handler ] [ VALIDATOR valfunction ]
```

### 說明

CREATE LANGUAGE 使用 PostgreSQL 資料庫註冊新的程序語言。隨後即可使用這種新語言定義函數和觸發器程序。

**注意**  
從 PostgreSQL 9.1 開始，大多數程序語言都被製作成「extension」，因此應該使用 [CREATE EXTENSION](create-extension.md) 而不是 CREATE LANGUAGE 安裝。現在應該直接使用 CREATE LANGUAGE 來限制性的延伸套件安裝腳本。如果資料庫中存在有純粹的程序語言（可能是升級後的結果），則可以使用 CREATE EXTENSION langname FROM unpackaged 將其轉換為延伸套件。

CREATE LANGUAGE 有效地將語言名稱與負責執行用該語言撰寫的函數與語言處理函數相關聯。有關語言處理程序的更多訊息，請參閱[第 55 章](../../internals/writing-a-procedural-language-handler.md)。

CREATE LANGUAGE 指令有兩種形式。在第一種形式中，使用者只提供所需語言的名稱，PostgreSQL 伺服器查詢 pg\_pltemplatesystem 目錄以確定正確的參數。在第二種形式中，使用者提供語言參數以及語言名稱。第二種形式可用於建立未在 pg\_pltemplate 中定義的語言，但此方法被視為是過時的。

當伺服器在 pg\_pltemplate 目錄中找到指定的語言名稱項目時，即使該命令包含語言參數，它也將使用目錄的資訊。此行為簡化了舊的備份檔案載入，這些備份檔案可能包含有關語言支援功能但過時的訊息。

通常，使用者必須具有 PostgreSQL 超級使用者權限才能註冊新的語言。但是，如果語言在 pg\_pltemplate 目錄中列出並且標記為允許由資料庫擁有者建立（tmpldbacreate 為 true），則資料庫的擁有者可以在該資料庫中註冊新的語言。預設情況下，資料庫擁有者可以建立受信任的語言，但超級使用者可以透過修改 pg\_pltemplate 的內容來調整它。語言的建立者成為其擁有者，以後可以將其移除，重新命名或將其分配給新的擁有者。

CREATE OR REPLACE LANGUAGE 將註冊新的語言或更換現有的定義。如果該語言已存在，則其參數將根據指定的值或從 pg\_pltemplate 取得，但語言的擁有權和權限設定不會更改，並且假定使用該語言撰寫的任何現有函數仍然有效。除了建立語言的普通權限要求之外，使用者還必須是現有語言的擁有者或超級使用者。REPLACE 主要用於確保語言存在。如果該語言具有 pg\_pltemplate 項目，則 REPLACE 實際上不會變更現有定義的任何內容，除非在建立語言後修改了 pg\_pltemplate 項目的特殊情況。

### 參數

`TRUSTED`

TRUSTED 表該語言不會授予使用者不應該擁有的資料存取權限。如果在註冊語言時省略了此關鍵字，則只有具有 PostgreSQL 超級使用者權限的使用者才能使用該語言建立新的函數。

`PROCEDURAL`

這是一個無功能的修飾詞。

_`name`_

新的程序語言名稱。此名稱在資料庫中的語言中必須是唯一的。

為了向下相容，名稱可以用單引號括起來。

`HANDLER` _`call_handler`_

call\_handler 是先前註冊的函數名稱，將呼叫該函數來執行程序語言的函數。程序語言的呼叫處理程序必須用編譯語言撰寫，例如 C with version 1 convention，並在 PostgreSQL 中註冊為不帶參數的函數，回傳 language\_handlertype，這是一種 placeholder 型別，僅用於將函數識別為呼叫處理程序

`INLINE` _`inline_handler`_

inline\_handler 是先前註冊的函數名稱，該函數將被呼叫以執行此語言的匿名代碼區塊（[DO](do.md) 指令）。如果未指定 inline\_handlerfunction，則該語言不支援匿名代碼區塊。處理函數必須使用一個型別為 internal 的參數，它將是 DO 指令的內部形式，並且通常回傳是 void。處理程序的回傳值將被忽略。

`VALIDATOR` _`valfunction`_

valfunction 是先前註冊的函數名稱，該函數將在宣告語言中的新函數時呼叫，以驗證新函數。如果未指定驗證程序功能，則在建立新函數時不會檢查該函數。驗證程序函數必須使用一個型別為 oid 的參數，該參數將是要建立的函數 OID，並且通常回傳為 void。

驗證程序函數通常會檢查函數的語法正確性，但它也可以查看函數的其他屬性。例如，如果語言無法處理某些參數型別。要發出錯誤信號，驗證程序函數應使用ereport\(\) 函數。該函數的回傳值將被忽略。

如果伺服器在 pg\_pltemplate 中具有指定語言名稱的項目，則忽略 TRUSTED 選項和支援函數名稱。

### 注意

使用 [DROP LANGUAGE](drop-language.md) 移除程序語言。

系統目錄 pg\_language（參閱[第 51.29 節](../../internals/system-catalogs/pg_language.md)）記錄有關目前安裝的語言訊息。此外，psql 指令 \dL 可列出已安裝的語言。

要以程序語言建立函數，使用者必須具有該語言的 USAGE 權限。預設情況下，USAGE 被授予 PUBLIC（即每個人）在可信任的語言上。如果需要，可以撤銷此權限。

程序語言在各個資料庫之間是獨立。但是，可以在 template1 資料庫中安裝一種語言，這將使其在所有後續建立的資料庫中自動可用。

如果伺務器在 pg\_pltemplate 中沒有該語言的項目，則必須已存在呼叫處理函數，內嵌處理函數（如果有）和驗證程序函數（如果有）。但是當有項目時，處理函數就不一定需要存在；如果資料庫中不存在，它們將會自動被定義。（如果實作該語言的共享函式庫在安裝環境中不可用，則可能導致 CREATE LANGUAGE 失敗。）

在 7.3 之前的 PostgreSQL 版本中，有必要將處理函數宣告為回傳 placeholder 型別 opaque，而不是 language\_handler。為了支援載入舊的備份檔案，CREATE LANGUAGE 將接受宣告為回傳 opaque 的函數，但它會發出通知並將函數宣告的回傳型別變更為 language\_handler。

### 範例

建立任何標準程序語言的最好方式是：

```text
CREATE LANGUAGE plperl;
```

對於 pg\_pltemplate 目錄中未知的語言，需要這樣的指令程序：

```text
CREATE FUNCTION plsample_call_handler() RETURNS language_handler
    AS '$libdir/plsample'
    LANGUAGE C;
CREATE LANGUAGE plsample
    HANDLER plsample_call_handler;
```

### 相容性

CREATE LANGUAGE 是 PostgreSQL 的延伸功能。

### 參閱

[ALTER LANGUAGE](alter-language.md), [CREATE FUNCTION](create-function.md), [DROP LANGUAGE](drop-language.md), [GRANT](grant.md), [REVOKE](revoke.md)

