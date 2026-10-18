<a id="ECPG-PREPROC"></a>

## 34.9. 前置處理器指令 [#](#ECPG-PREPROC)

[34.9.1. 引入檔案](ecpg-preproc.md#ECPG-INCLUDE)

[34.9.2. define 與 undef 指令](ecpg-preproc.md#ECPG-DEFINE)

[34.9.3. ifdef、ifndef、elif、else 與 endif 指令](ecpg-preproc.md#ECPG-IFDEF)

有幾個前置處理器指令可用來改變 `ecpg` 前置處理器剖析與處理檔案的方式。

<a id="ECPG-INCLUDE"></a>

### 34.9.1. 引入檔案 [#](#ECPG-INCLUDE)

要將外部檔案引入嵌入式 SQL 程式，請使用：

```

EXEC SQL INCLUDE filename;
EXEC SQL INCLUDE <filename>;
EXEC SQL INCLUDE "filename";
```

嵌入式 SQL 前置處理器會尋找名為 `filename.h` 的檔案，對它進行前置處理，並將它納入產生的 C 輸出中。因此，被引入檔案中的嵌入式 SQL 陳述式也能被正確處理。

`ecpg` 前置處理器會依下列順序在數個目錄中搜尋檔案：

* 目前目錄
* `/usr/local/include`
* PostgreSQL 的引入檔（include）目錄，於建置時定義（例如 `/usr/local/pgsql/include`）
* `/usr/include`

但使用 `EXEC SQL INCLUDE
"filename"` 時，只會搜尋目前目錄。

在每個目錄中，前置處理器會先尋找與所給名稱相同的檔案；若找不到，則會在檔名後附加 `.h` 再試一次（除非指定的檔名已經帶有該副檔名）。

請注意，`EXEC SQL INCLUDE` 與下列寫法*不*相同：

```

#include <filename.h>
```

因為這樣引入的檔案不會經過 SQL 命令的前置處理。當然，你仍然可以使用 C 的 `#include` 指令來引入其他標頭檔。

### 注意

引入檔的名稱區分大小寫，即使 `EXEC SQL INCLUDE` 命令的其餘部分遵循一般的 SQL 大小寫規則。

<a id="ECPG-DEFINE"></a>

### 34.9.2. define 與 undef 指令 [#](#ECPG-DEFINE)

類似於 C 中常見的 `#define` 指令，嵌入式 SQL 也有類似的概念：

```

EXEC SQL DEFINE name;
EXEC SQL DEFINE name value;
```

因此你可以定義一個名稱：

```

EXEC SQL DEFINE HAVE_FEATURE;
```

也可以定義常數：

```

EXEC SQL DEFINE MYNUMBER 12;
EXEC SQL DEFINE MYSTRING 'abc';
```

使用 `undef` 移除先前的定義：

```

EXEC SQL UNDEF MYNUMBER;
```

當然，你仍然可以在嵌入式 SQL 程式中使用 C 版本的 `#define` 與 `#undef`。差別在於你定義的值在何處求值。如果你使用 `EXEC SQL
DEFINE`，則由 `ecpg` 前置處理器對這些定義求值並替換其值。例如，如果你寫：

```

EXEC SQL DEFINE MYNUMBER 12;
...
EXEC SQL UPDATE Tbl SET col = MYNUMBER;
```

那麼 `ecpg` 就已經完成替換，你的 C 編譯器永遠不會看到任何名稱或識別字 `MYNUMBER`。請注意，對於要在嵌入式 SQL 查詢中使用的常數，你不能使用 `#define`，因為在這種情況下，嵌入式 SQL 預先編譯器看不到這項宣告。

如果在 `ecpg` 前置處理器的命令列上指定了多個輸入檔，`EXEC SQL
DEFINE` 與 `EXEC SQL UNDEF` 的效果不會延續到其他檔案：每個檔案開始時，只有命令列上以 `-D` 參數定義的符號。

<a id="ECPG-IFDEF"></a>

### 34.9.3. ifdef、ifndef、elif、else 與 endif 指令 [#](#ECPG-IFDEF)

你可以使用下列指令有條件地編譯程式碼區段：

<a id="ECPG-IFDEF-IFDEF"></a>

`EXEC SQL ifdef name;` [#](#ECPG-IFDEF-IFDEF)
:   檢查 *`name`*，若 *`name`* 已透過 `EXEC SQL define
    name` 定義，則處理後續各行。
<a id="ECPG-IFDEF-IFNDEF"></a>

`EXEC SQL ifndef name;` [#](#ECPG-IFDEF-IFNDEF)
:   檢查 *`name`*，若 *`name`* *尚未*透過 `EXEC SQL define name` 定義，則處理後續各行。
<a id="ECPG-IFDEF-ELIF"></a>

`EXEC SQL elif name;` [#](#ECPG-IFDEF-ELIF)
:   在 `EXEC SQL ifdef name` 或 `EXEC SQL ifndef name` 指令之後，開始一個選用的替代區段。`elif` 區段可以出現任意多個。若 *`name`* 已定義，*而且*同一個 `ifdef`/`ifndef`...`endif` 結構中先前沒有任何區段被處理過，則會處理 `elif` 之後的各行。
<a id="ECPG-IFDEF-ELSE"></a>

`EXEC SQL else;` [#](#ECPG-IFDEF-ELSE)
:   在 `EXEC SQL ifdef name` 或 `EXEC SQL ifndef name` 指令之後，開始一個選用的最終替代區段。若同一個 `ifdef`/`ifndef`...`endif` 結構中先前沒有任何區段被處理過，則會處理後續各行。
<a id="ECPG-IFDEF-ENDIF"></a>

`EXEC SQL endif;` [#](#ECPG-IFDEF-ENDIF)
:   結束一個 `ifdef`/`ifndef`...`endif` 結構。後續各行會照常處理。

`ifdef`/`ifndef`...`endif` 結構可以巢狀使用，最多 127 層。

此範例會在三個 `SET
TIMEZONE` 命令中恰好編譯其中一個：

```

EXEC SQL ifdef TZVAR;
EXEC SQL SET TIMEZONE TO TZVAR;
EXEC SQL elif TZNAME;
EXEC SQL SET TIMEZONE TO TZNAME;
EXEC SQL else;
EXEC SQL SET TIMEZONE TO 'GMT';
EXEC SQL endif;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-preproc.html)（原文版本：18.6；核對日期：2026-10-18）
