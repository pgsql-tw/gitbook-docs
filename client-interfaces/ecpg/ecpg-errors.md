<a id="ECPG-ERRORS"></a>

## 34.8. 錯誤處理 [#](#ecpg-errors) <a href="#ecpg-errors" id="ecpg-errors"></a>

[34.8.1. 設定回呼](ecpg-whenever.md#ecpg-whenever)

[34.8.2. sqlca](ecpg-errors.md#ecpg-sqlca)

[34.8.3. `SQLSTATE` 與 `SQLCODE` 的比較](ecpg-sqlstate-sqlcode.md#ecpg-sqlstate-sqlcode)

本節說明如何在嵌入式 SQL 程式中處理例外情況與警告。為此有兩種機制，兩者並不互斥，可以同時使用。

* 可以使用 `WHENEVER` 命令設定回呼，以處理警告與錯誤情況。
* 可以從 `sqlca` 變數取得關於錯誤或警告的詳細資訊。

<a id="ECPG-WHENEVER"></a>

### 34.8.1. 設定回呼 [#](#ecpg-whenever) <a href="#ecpg-whenever" id="ecpg-whenever"></a>

本節內容請參閱[34.8.1. 設定回呼](ecpg-whenever.md#ecpg-whenever)。

<a id="ECPG-SQLCA"></a>

### 34.8.2. sqlca [#](#ecpg-sqlca) <a href="#ecpg-sqlca" id="ecpg-sqlca"></a>

為了提供更強大的錯誤處理，嵌入式 SQL 介面提供了一個名為 `sqlca`（SQL 通訊區，SQL communication area）的全域變數，其結構如下：

```

struct
{
    char sqlcaid[8];
    long sqlabc;
    long sqlcode;
    struct
    {
        int sqlerrml;
        char sqlerrmc[SQLERRMC_LEN];
    } sqlerrm;
    char sqlerrp[8];
    long sqlerrd[6];
    char sqlwarn[8];
    char sqlstate[5];
} sqlca;
```

（在多執行緒程式中，每個執行緒都會自動取得自己的 `sqlca` 副本。這與標準 C 全域變數 `errno` 的處理方式類似。）

`sqlca` 同時涵蓋警告與錯誤。若在執行一個陳述式期間發生多個警告或錯誤，`sqlca` 只會包含最後一個的資訊。

若上一個 SQL 陳述式沒有發生錯誤，`sqlca.sqlcode` 會是 0，而 `sqlca.sqlstate` 會是 `"00000"`。若發生了警告或錯誤，`sqlca.sqlcode` 會是負值，而 `sqlca.sqlstate` 會不同於 `"00000"`。`sqlca.sqlcode` 為正值表示無害的情況，例如上一個查詢傳回零個資料列。`sqlcode` 與 `sqlstate` 是兩種不同的錯誤碼體系；詳情見下文。

若上一個 SQL 陳述式執行成功，則 `sqlca.sqlerrd[1]` 會包含所處理資料列的 OID（若適用），而 `sqlca.sqlerrd[2]` 會包含所處理或傳回的資料列數（若該命令適用）。

發生錯誤或警告時，`sqlca.sqlerrm.sqlerrmc` 會包含描述該錯誤的字串。欄位 `sqlca.sqlerrm.sqlerrml` 包含儲存在 `sqlca.sqlerrm.sqlerrmc` 中之錯誤訊息的長度（即 `strlen()` 的結果，對 C 程式設計師來說其實沒什麼用處）。請注意，有些訊息太長，無法放進固定大小的 `sqlerrmc` 陣列；這些訊息會被截斷。

發生警告時，`sqlca.sqlwarn[2]` 會設為 `W`。（在其他所有情況下，它會設為不同於 `W` 的值。）若 `sqlca.sqlwarn[1]` 設為 `W`，表示有某個值在存入主機變數時被截斷。若其他任何元素被設定為表示警告，`sqlca.sqlwarn[0]` 就會設為 `W`。

欄位 `sqlcaid`、`sqlabc`、`sqlerrp`，以及 `sqlerrd` 與 `sqlwarn` 的其餘元素，目前都不包含有用的資訊。

`sqlca` 結構並未定義在 SQL 標準中，但有其他幾個 SQL 資料庫系統實作了它。各家定義的核心部分相似，但如果你想撰寫可攜的應用程式，應該仔細研究各種不同的實作。

以下範例結合使用 `WHENEVER` 與 `sqlca`，在發生錯誤時輸出 `sqlca` 的內容。在安裝更「使用者友善」的錯誤處理程序之前，這或許有助於應用程式的除錯或雛型開發。

```

EXEC SQL WHENEVER SQLERROR CALL print_sqlca();

void
print_sqlca()
{
    fprintf(stderr, "==== sqlca ====\n");
    fprintf(stderr, "sqlcode: %ld\n", sqlca.sqlcode);
    fprintf(stderr, "sqlerrm.sqlerrml: %d\n", sqlca.sqlerrm.sqlerrml);
    fprintf(stderr, "sqlerrm.sqlerrmc: %s\n", sqlca.sqlerrm.sqlerrmc);
    fprintf(stderr, "sqlerrd: %ld %ld %ld %ld %ld %ld\n", sqlca.sqlerrd[0],sqlca.sqlerrd[1],sqlca.sqlerrd[2],
                                                          sqlca.sqlerrd[3],sqlca.sqlerrd[4],sqlca.sqlerrd[5]);
    fprintf(stderr, "sqlwarn: %d %d %d %d %d %d %d %d\n", sqlca.sqlwarn[0], sqlca.sqlwarn[1], sqlca.sqlwarn[2],
                                                          sqlca.sqlwarn[3], sqlca.sqlwarn[4], sqlca.sqlwarn[5],
                                                          sqlca.sqlwarn[6], sqlca.sqlwarn[7]);
    fprintf(stderr, "sqlstate: %5s\n", sqlca.sqlstate);
    fprintf(stderr, "===============\n");
}
```

譯註：上方範例以 %5s 輸出 sqlca.sqlstate，但 sqlstate 是長度為 5 的字元陣列，不保證以零位元組結尾，而 %5s 中的 5 只是最小欄寬，並不限制讀取長度，可能會讀到陣列範圍之外；應寫作 %.5s 才能只輸出這 5 個字元。範例程式碼依原文保留。

輸出結果可能如下所示（此處是因資料表名稱拼錯而產生的錯誤）：

```

==== sqlca ====
sqlcode: -400
sqlerrm.sqlerrml: 49
sqlerrm.sqlerrmc: relation "pg_databasep" does not exist on line 38
sqlerrd: 0 0 0 0 0 0
sqlwarn: 0 0 0 0 0 0 0 0
sqlstate: 42P01
===============
```

<a id="ECPG-SQLSTATE-SQLCODE"></a>

### 34.8.3. `SQLSTATE` 與 `SQLCODE` 的比較 [#](#ecpg-sqlstate-sqlcode) <a href="#ecpg-sqlstate-sqlcode" id="ecpg-sqlstate-sqlcode"></a>

本節內容請參閱[34.8.3. `SQLSTATE` 與 `SQLCODE` 的比較](ecpg-sqlstate-sqlcode.md#ecpg-sqlstate-sqlcode)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-errors.html)（原文版本：18.6；核對日期：2026-10-22）
