<a id="REGRESS-EVALUATION"></a>

## 31.2. 測試評估 [#](#REGRESS-EVALUATION)

[31.2.1. 錯誤訊息差異](regress-evaluation.md#REGRESS-EVALUATION-MESSAGE-DIFFERENCES)

[31.2.2. 地區設定差異](regress-evaluation.md#REGRESS-EVALUATION-LOCALE-DIFFERENCES)

[31.2.3. 日期與時間差異](regress-evaluation.md#REGRESS-EVALUATION-DATE-TIME-DIFFERENCES)

[31.2.4. 浮點數差異](regress-evaluation.md#REGRESS-EVALUATION-FLOAT-DIFFERENCES)

[31.2.5. 資料列順序差異](regress-evaluation.md#REGRESS-EVALUATION-ORDERING-DIFFERENCES)

[31.2.6. 堆疊深度不足](regress-evaluation.md#REGRESS-EVALUATION-STACK-DEPTH)

[31.2.7. 「random」測試](regress-evaluation.md#REGRESS-EVALUATION-RANDOM-TEST)

[31.2.8. 組態參數](regress-evaluation.md#REGRESS-EVALUATION-CONFIG-PARAMS)

有些正確安裝且功能完全正常的
PostgreSQL 安裝，
可能會因為平台特有的差異，
例如浮點數表示方式與訊息用字的不同，
而使部分迴歸測試「失敗」。目前這些測試，
是透過與參考系統上所產生的輸出進行單純的
`diff` 比對來評估的，因此結果會對
系統間的微小差異很敏感。當某項測試被回報為
「失敗」時，請務必檢視預期結果與實際結果之間的差異；
你可能會發現這些差異並不重要。儘管如此，
我們仍致力於在所有受支援的平台上，
維護準確的參考檔案，因此一般而言，
應可預期所有測試都會通過。

迴歸測試的實際輸出，位於
`src/test/regress/results` 目錄中的檔案裡。
測試指令碼會使用 `diff`，
將每個輸出檔案，與儲存在
`src/test/regress/expected` 目錄中的
參考輸出進行比對。任何差異，
都會被儲存在
`src/test/regress/regression.diffs`
中供你檢視。
（當你執行的是核心測試以外的其他測試套組時，
這些檔案當然會出現在相關的子目錄中，
而非 `src/test/regress` 中。）

若你不喜歡預設使用的 `diff` 選項，
可設定環境變數 `PG_REGRESS_DIFF_OPTS`，
例如 `PG_REGRESS_DIFF_OPTS='-c'`。
（或者，若你偏好，也可以自行執行
`diff`。）

若因為某種原因，特定平台針對某項測試
產生了「失敗」，但你檢視輸出後認為
該結果是有效的，你可以新增一份比對檔案，
以在未來的測試執行中消除該失敗報告。詳情請參閱
[31.3 節](regress-variant.md)。

<a id="REGRESS-EVALUATION-MESSAGE-DIFFERENCES"></a>

### 31.2.1. 錯誤訊息差異 [#](#REGRESS-EVALUATION-MESSAGE-DIFFERENCES)

部分迴歸測試會涉及刻意輸入的無效值。
錯誤訊息可能來自 PostgreSQL 程式碼本身，
也可能來自主機平台的系統常式。在後者的情況下，
訊息內容可能因平台而異，但應反映出類似的資訊。
這些訊息上的差異，會導致迴歸測試「失敗」，
但可透過檢視內容加以驗證。

<a id="REGRESS-EVALUATION-LOCALE-DIFFERENCES"></a>

### 31.2.2. 地區設定差異 [#](#REGRESS-EVALUATION-LOCALE-DIFFERENCES)

若你針對以非 C 定序順序地區設定初始化的伺服器
執行測試，可能會因排序順序而出現差異，
進而導致後續失敗。迴歸測試套組已設定為
透過提供替代結果檔案來因應此問題，
這些檔案合起來已知能涵蓋為數眾多的地區設定。

若要在使用暫時安裝方法時，以不同的地區設定執行測試，
請在 `make` 命令列上傳入適當的
地區設定相關環境變數，例如：

```

make check LANG=de_DE.utf8
```

（迴歸測試驅動程式會取消設定 `LC_ALL`，
因此透過該變數選擇地區設定並不會生效。）若要不使用
任何地區設定，可以取消設定所有地區設定相關的環境變數
（或將其設為 `C`），或使用以下
特殊呼叫方式：

```

make check NO_LOCALE=1
```

當你針對既有安裝執行測試時，地區設定
是由該既有安裝所決定的。若要變更此設定，
請透過傳入適當的選項給
`initdb`，以不同的地區設定
初始化資料庫叢集。

一般而言，建議你嘗試以正式環境
實際會使用的地區設定來執行迴歸測試，
因為這樣能測試到正式環境中實際會用到的
地區設定與編碼相關程式碼部分。依作業系統環境而定，
你可能會遇到失敗的情況，但至少能事先了解
執行實際應用程式時，應預期哪些與地區設定相關的行為。

<a id="REGRESS-EVALUATION-DATE-TIME-DIFFERENCES"></a>

### 31.2.3. 日期與時間差異 [#](#REGRESS-EVALUATION-DATE-TIME-DIFFERENCES)

大多數日期與時間結果，都取決於時區環境。
參考檔案是針對時區
`America/Los_Angeles` 產生的，
若測試並非以該時區設定執行，就會出現看似失敗的情況。
迴歸測試驅動程式會將環境變數
`PGTZ` 設為 `America/Los_Angeles`，
這通常能確保結果正確。

<a id="REGRESS-EVALUATION-FLOAT-DIFFERENCES"></a>

### 31.2.4. 浮點數差異 [#](#REGRESS-EVALUATION-FLOAT-DIFFERENCES)

部分測試涉及從資料表欄位計算 64 位元浮點數
（`double precision`）。
我們觀察到，涉及 `double precision`
欄位數學函式運算的結果會出現差異。
`float8` 與 `geometry` 測試，
特別容易在不同平台之間，
甚至在不同的編譯器最佳化設定下，出現微小差異。
這些差異通常出現在小數點右側第 10 位，
需要以肉眼比對，才能判斷其真正的重要性。

有些系統會將負零顯示為 `-0`，
有些系統則只顯示 `0`。

有些系統回報 `pow()` 與
`exp()` 錯誤的方式，
與目前 PostgreSQL 程式碼
所預期的機制不同。

<a id="REGRESS-EVALUATION-ORDERING-DIFFERENCES"></a>

### 31.2.5. 資料列順序差異 [#](#REGRESS-EVALUATION-ORDERING-DIFFERENCES)

你可能會看到，同樣一批資料列，
輸出順序卻與預期檔案中所呈現的不同。
嚴格來說，在大多數情況下，這並不算是錯誤。
大多數迴歸測試指令碼，並沒有嚴謹到
為每一個 `SELECT` 都加上 `ORDER BY`，
因此依 SQL 規格而言，其結果資料列順序
本來就沒有明確定義。實務上，
由於我們是在相同的軟體、針對相同的資料，
執行相同的查詢，因此通常在所有平台上，
都能得到相同的結果順序，
所以未使用 `ORDER BY` 通常不成問題。
然而，有些查詢確實會出現跨平台的順序差異。
在針對已安裝伺服器進行測試時，
順序差異也可能是由非 C 地區設定，
或非預設的參數設定所導致的，
例如自訂的 `work_mem` 值，
或規劃器成本參數。

因此，若你看到順序上的差異，通常不需要擔心，
除非該查詢確實含有 `ORDER BY`，
而你的結果違反了該排序。不過，
仍請將此情況回報給我們，
以便我們能為該特定查詢加上 `ORDER BY`，
在未來的版本中消除這種虛假的「失敗」。

你可能會好奇，為何我們不乾脆為所有迴歸測試查詢
都明確指定排序，一勞永逸地解決這個問題。
原因是，這麼做反而會降低迴歸測試的實用性，
因為這會使測試傾向於只使用會產生排序結果的
查詢計畫類型，而排除那些不會的類型。

<a id="REGRESS-EVALUATION-STACK-DEPTH"></a>

### 31.2.6. 堆疊深度不足 [#](#REGRESS-EVALUATION-STACK-DEPTH)

若 `errors` 測試在執行
`select infinite_recurse()` 命令時
導致伺服器當機，代表該平台上程序堆疊大小的限制，
小於 [max_stack_depth](../runtime-config/runtime-config-resource.md#GUC-MAX-STACK-DEPTH)
參數所指示的值。你可以透過在較高的堆疊大小限制下
執行伺服器來解決此問題（在
`max_stack_depth` 使用預設值時，
建議使用 4MB）。若你無法這麼做，
另一個替代方案是降低 `max_stack_depth`
的值。

在支援 `getrlimit()` 的平台上，
伺服器應會自動選擇一個安全的
`max_stack_depth` 值；因此，
除非你已手動覆寫此設定，否則發生這類失敗，
即屬於可回報的錯誤。

<a id="REGRESS-EVALUATION-RANDOM-TEST"></a>

### 31.2.7. 「random」測試 [#](#REGRESS-EVALUATION-RANDOM-TEST)

`random` 測試指令碼的用意，
就是要產生隨機結果。在極少數情況下，
這會導致該迴歸測試失敗。輸入：

```

diff results/random.out expected/random.out
```

應該只會產生一行或少數幾行差異。
除非 random 測試反覆失敗，否則不需要擔心。

<a id="REGRESS-EVALUATION-CONFIG-PARAMS"></a>

### 31.2.8. 組態參數 [#](#REGRESS-EVALUATION-CONFIG-PARAMS)

當你針對既有安裝執行測試時，
某些非預設的參數設定，可能會導致測試失敗。
例如，變更 `enable_seqscan` 或
`enable_indexscan` 等參數，
可能會導致查詢計畫改變，
進而影響使用 `EXPLAIN` 之測試的結果。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/regress-evaluation.html)（原文版本：18.6；核對日期：2026-09-24）
