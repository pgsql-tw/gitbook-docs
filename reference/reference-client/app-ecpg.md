<a id="APP-ECPG"></a><a id="id-1.9.4.8.1"></a>

## ecpg

ecpg — 嵌入式 SQL C 前置處理器

<a id="id-1.9.4.8.4"></a>

## 語法

<a id="id-1.9.4.8.4.1"></a>

`ecpg` [*`option`*...] *`file`*...

<a id="APP-ECPG-DESCRIPTION"></a>

## 說明

`ecpg` 是 C 程式的嵌入式 SQL 前置處理器。它會將 SQL 呼叫替換為特殊的函式呼叫，藉此把含有嵌入式 SQL 陳述式的 C 程式轉換為一般的 C 程式碼。之後即可用任何 C 編譯器工具鏈處理輸出檔案。

`ecpg` 會將命令列上指定的每個輸入檔案轉換為對應的 C 輸出檔案。若輸入檔名沒有任何副檔名，則假定為 `.pgc`。檔案的副檔名會被替換為 `.c` 來構成輸出檔名。不過，可以使用 `-o` 選項覆寫輸出檔名。

若輸入檔名只是 `-`，`ecpg` 會從標準輸入讀取程式（並寫到標準輸出，除非以 `-o` 覆寫）。

本參考頁不說明嵌入式 SQL 語言。關於該主題的更多資訊，請參閱[第 34 章](../../client-interfaces/ecpg/README.md)。

<a id="id-1.9.4.8.6"></a>

## 選項

`ecpg` 接受下列命令列引數：

`-c`
:   從 SQL 程式碼自動產生某些 C 程式碼。目前這適用於 `EXEC SQL TYPE`。

`-C mode`
:   設定相容模式。*`mode`* 可以是 `INFORMIX`、`INFORMIX_SE` 或 `ORACLE`。

`-D symbol[=value]`
:   定義一個前置處理器符號，等同於 `EXEC SQL
    DEFINE` 指令。若未指定 *`value`*，該符號會以值 `1` 定義。

`-h`
:   處理標頭檔。指定此選項時，輸出檔案的副檔名會變成 `.h` 而不是 `.c`，預設的輸入檔案副檔名則是 `.pgh` 而不是 `.pgc`。此外，`-c` 選項會被強制開啟。

`-i`
:   也剖析系統 include 檔案。

`-I directory`
:   指定額外的 include 路徑，用來尋找透過 `EXEC SQL INCLUDE` 引入的檔案。預設值依序為 `.`（目前目錄）、`/usr/local/include`、在編譯時定義的 PostgreSQL include 目錄（預設：`/usr/local/pgsql/include`），以及 `/usr/include`。

`-o filename`
:   指定 `ecpg` 應該將其所有輸出寫到指定的 *`filename`*。寫成 `-o -` 可將所有輸出傳送到標準輸出。

`-r option`

選擇執行期行為。*`Option`* 可以是下列之一：

- `no_indicator`

  不使用指示變數（indicator），而是改用特殊值來表示空值。過去曾有資料庫使用這種做法。

- `prepare`

  在使用所有陳述式之前先預備它們。Libecpg 會保留預備陳述式的快取，並在陳述式再次被執行時重複使用它。若快取已滿，libecpg 會釋放最少使用的陳述式。

- `questionmarks`

  基於相容性的理由，允許使用問號作為預留位置。很久以前這曾是預設行為。

`-t`
:   開啟交易的自動提交。在此模式下，每個 SQL 命令都會自動提交，除非它位於明確的交易區塊內。在預設模式下，只有在發出 `EXEC SQL COMMIT` 時才會提交命令。

`-v`
:   印出額外資訊，包括版本與「include」路徑。

`--version`
:   印出 ecpg 的版本後結束。

`-?`<br>`--help`
:   顯示 ecpg 命令列引數的說明後結束。

<a id="id-1.9.4.8.7"></a>

## 注意事項

編譯經過前置處理的 C 程式碼檔案時，編譯器需要能在 PostgreSQL include 目錄中找到 ECPG 標頭檔。因此，呼叫編譯器時你可能必須使用 `-I` 選項（例如 `-I/usr/local/pgsql/include`）。

使用含嵌入式 SQL 之 C 程式碼的程式，必須與 `libecpg` 函式庫連結，例如使用連結器選項 `-L/usr/local/pgsql/lib -lecpg`。

這兩個目錄中適用於該安裝的值，可以使用 [pg_config](app-pgconfig.md) 查得。

<a id="id-1.9.4.8.8"></a>

## 範例

若你有一個名為 `prog1.pgc` 的嵌入式 SQL C 原始檔，可以使用下列命令序列建立可執行程式：

```

ecpg prog1.pgc
cc -I/usr/local/pgsql/include -c prog1.c
cc -o prog1 prog1.o -L/usr/local/pgsql/lib -lecpg
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-ecpg.html)（原文版本：18.6；核對日期：2026-10-09）
