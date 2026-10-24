<a id="ECPG-PROCESS"></a>

## 34.10. 處理嵌入式 SQL 程式 [#](#ecpg-process) <a href="#ecpg-process" id="ecpg-process"></a>

現在你已經大致了解如何撰寫嵌入式 SQL C 程式，你可能會想知道如何編譯它們。編譯之前，要先讓檔案通過嵌入式 SQL C 前置處理器，它會把你使用的 SQL 陳述式轉換成特殊的函式呼叫。編譯之後，必須與一個包含所需函式的特殊函式庫連結。這些函式會從引數中取得資訊，透過 libpq 介面執行 SQL 命令，並將結果放入指定用於輸出的引數中。

前置處理器程式名為 `ecpg`，包含在一般的 PostgreSQL 安裝中。嵌入式 SQL 程式通常以 `.pgc` 作為副檔名。如果你有一個名為 `prog1.pgc` 的程式檔，只要如下呼叫即可對它進行前置處理：

```

ecpg prog1.pgc
```

這會建立名為 `prog1.c` 的檔案。如果你的輸入檔未遵循建議的命名模式，可以使用 `-o` 選項明確指定輸出檔。

前置處理後的檔案可以照常編譯，例如：

```

cc -c prog1.c
```

產生的 C 原始檔會引入 PostgreSQL 安裝中的標頭檔，因此如果你把 PostgreSQL 安裝在預設不會搜尋的位置，就必須在編譯命令列中加入 `-I/usr/local/pgsql/include` 之類的選項。

要連結嵌入式 SQL 程式，你需要納入 `libecpg` 函式庫，如下所示：

```

cc -o myprog prog1.o prog2.o ... -lecpg
```

同樣地，你可能需要在該命令列中加入 `-L/usr/local/pgsql/lib` 之類的選項。

你可以使用 `pg_config`<a id="id-1.7.5.16.6.2"></a> 或 `pkg-config`<a id="id-1.7.5.16.6.4"></a>（套件名稱為 `libecpg`）取得你的安裝所使用的路徑。

如果你使用 make 管理較大型專案的建置流程，在 makefile（make 的設定檔）中加入下列隱含規則可能會很方便：

```

ECPG = ecpg

%.c: %.pgc
        $(ECPG) $<
```

`ecpg` 命令的完整語法詳見 [ecpg](../../reference/reference-client/app-ecpg.md)。

ecpg 函式庫預設是執行緒安全的。不過，你可能需要使用一些與執行緒相關的命令列選項來編譯你的用戶端程式碼。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-process.html)（原文版本：18.6；核對日期：2026-10-18）
