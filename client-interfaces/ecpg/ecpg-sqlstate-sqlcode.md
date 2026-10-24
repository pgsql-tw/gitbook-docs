<a id="ECPG-SQLSTATE-SQLCODE"></a>

## 34.8.3. `SQLSTATE` 與 `SQLCODE` 的比較 [#](#ecpg-sqlstate-sqlcode) <a href="#ecpg-sqlstate-sqlcode" id="ecpg-sqlstate-sqlcode"></a>

欄位 `sqlca.sqlstate` 與 `sqlca.sqlcode` 是提供錯誤碼的兩種不同體系。兩者都源自 SQL 標準，但 `SQLCODE` 在 SQL-92 版標準中已被標示為已棄用，並在之後的版本中被移除。因此，強烈建議新的應用程式使用 `SQLSTATE`。

`SQLSTATE` 是由五個字元組成的陣列。這五個字元包含數字或大寫字母，代表各種錯誤與警告情況的代碼。`SQLSTATE` 採用階層式體系：前兩個字元表示該情況的大類，後三個字元表示該大類下的子類。成功狀態以代碼 `00000` 表示。`SQLSTATE` 代碼大部分定義於 SQL 標準中。PostgreSQL 伺服器原生支援 `SQLSTATE` 錯誤碼；因此，在所有應用程式中一致使用這套錯誤碼體系，可以達到高度的一致性。進一步的資訊請參閱[附錄 A](../../appendixes/errcodes-appendix/README.md)。

`SQLCODE` 是已棄用的錯誤碼體系，它是一個簡單的整數。值為 0 表示成功，正值表示成功但附帶額外資訊，負值表示錯誤。SQL 標準只定義了正值 +100，表示上一個命令傳回或影響了零個資料列，並未定義任何特定的負值。因此，這套體系的可攜性很差，也沒有階層式的代碼分配。歷來，PostgreSQL 的嵌入式 SQL 處理器為自身用途指定了一些特定的 `SQLCODE` 值，以下連同其數值與符號名稱一併列出。請記得，這些值無法移植到其他 SQL 實作。為了簡化將應用程式移植到 `SQLSTATE` 體系的工作，也一併列出了對應的 `SQLSTATE`。不過，這兩套體系之間並不是一對一或一對多的對應關係（實際上是多對多），因此每種情況都應該查閱[附錄 A](../../appendixes/errcodes-appendix/README.md) 中完整的 `SQLSTATE` 清單。

以下是已指定的 `SQLCODE` 值：

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NO-ERROR"></a>

### 0 (`ECPG_NO_ERROR`) [#](#ecpg-sqlstate-sqlcode-ecpg-no-error) <a href="#ecpg-sqlstate-sqlcode-ecpg-no-error" id="ecpg-sqlstate-sqlcode-ecpg-no-error"></a>

表示沒有錯誤。（SQLSTATE 00000）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NOT-FOUND"></a>

### 100 (`ECPG_NOT_FOUND`) [#](#ecpg-sqlstate-sqlcode-ecpg-not-found) <a href="#ecpg-sqlstate-sqlcode-ecpg-not-found" id="ecpg-sqlstate-sqlcode-ecpg-not-found"></a>

這是無害的情況，表示上一個命令擷取或處理了零個資料列，或是你已到達游標的結尾。（SQLSTATE 02000）

在迴圈中處理游標時，可以用這個代碼來偵測何時該中止迴圈，例如：

```

    while (1)
    {
        EXEC SQL FETCH ... ;
        if (sqlca.sqlcode == ECPG_NOT_FOUND)
            break;
    }
```

不過 `WHENEVER NOT FOUND DO BREAK` 在內部實際上就是這麼做，因此明確寫出這段程式碼通常沒有什麼好處。

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-OUT-OF-MEMORY"></a>

### -12 (`ECPG_OUT_OF_MEMORY`) [#](#ecpg-sqlstate-sqlcode-ecpg-out-of-memory) <a href="#ecpg-sqlstate-sqlcode-ecpg-out-of-memory" id="ecpg-sqlstate-sqlcode-ecpg-out-of-memory"></a>

表示虛擬記憶體已耗盡。其數值定義為 `-ENOMEM`。（SQLSTATE YE001）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UNSUPPORTED"></a>

### -200 (`ECPG_UNSUPPORTED`) [#](#ecpg-sqlstate-sqlcode-ecpg-unsupported) <a href="#ecpg-sqlstate-sqlcode-ecpg-unsupported" id="ecpg-sqlstate-sqlcode-ecpg-unsupported"></a>

表示前置處理器產生了函式庫無法識別的內容。可能是你使用的前置處理器與函式庫版本不相容。（SQLSTATE YE002）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-ARGUMENTS"></a>

### -201 (`ECPG_TOO_MANY_ARGUMENTS`) [#](#ecpg-sqlstate-sqlcode-ecpg-too-many-arguments) <a href="#ecpg-sqlstate-sqlcode-ecpg-too-many-arguments" id="ecpg-sqlstate-sqlcode-ecpg-too-many-arguments"></a>

這表示命令指定的主機變數多於該命令預期的數量。（SQLSTATE 07001 或 07002）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TOO-FEW-ARGUMENTS"></a>

### -202 (`ECPG_TOO_FEW_ARGUMENTS`) [#](#ecpg-sqlstate-sqlcode-ecpg-too-few-arguments) <a href="#ecpg-sqlstate-sqlcode-ecpg-too-few-arguments" id="ecpg-sqlstate-sqlcode-ecpg-too-few-arguments"></a>

這表示命令指定的主機變數少於該命令預期的數量。（SQLSTATE 07001 或 07002）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-MATCHES"></a>

### -203 (`ECPG_TOO_MANY_MATCHES`) [#](#ecpg-sqlstate-sqlcode-ecpg-too-many-matches) <a href="#ecpg-sqlstate-sqlcode-ecpg-too-many-matches" id="ecpg-sqlstate-sqlcode-ecpg-too-many-matches"></a>

這表示查詢傳回了多個資料列，但該陳述式只準備好儲存一個結果資料列（例如，因為所指定的變數不是陣列）。（SQLSTATE 21000）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INT-FORMAT"></a>

### -204 (`ECPG_INT_FORMAT`) [#](#ecpg-sqlstate-sqlcode-ecpg-int-format) <a href="#ecpg-sqlstate-sqlcode-ecpg-int-format" id="ecpg-sqlstate-sqlcode-ecpg-int-format"></a>

主機變數的型別為 `int`，而資料庫中的資料是不同的型別，且其值無法解讀為 `int`。函式庫使用 `strtol()` 進行此轉換。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UINT-FORMAT"></a>

### -205 (`ECPG_UINT_FORMAT`) [#](#ecpg-sqlstate-sqlcode-ecpg-uint-format) <a href="#ecpg-sqlstate-sqlcode-ecpg-uint-format" id="ecpg-sqlstate-sqlcode-ecpg-uint-format"></a>

主機變數的型別為 `unsigned int`，而資料庫中的資料是不同的型別，且其值無法解讀為 `unsigned
    int`。函式庫使用 `strtoul()` 進行此轉換。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-FLOAT-FORMAT"></a>

### -206 (`ECPG_FLOAT_FORMAT`) [#](#ecpg-sqlstate-sqlcode-ecpg-float-format) <a href="#ecpg-sqlstate-sqlcode-ecpg-float-format" id="ecpg-sqlstate-sqlcode-ecpg-float-format"></a>

主機變數的型別為 `float`，而資料庫中的資料是其他型別，且其值無法解讀為 `float`。函式庫使用 `strtod()` 進行此轉換。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NUMERIC-FORMAT"></a>

### -207 (`ECPG_NUMERIC_FORMAT`) [#](#ecpg-sqlstate-sqlcode-ecpg-numeric-format) <a href="#ecpg-sqlstate-sqlcode-ecpg-numeric-format" id="ecpg-sqlstate-sqlcode-ecpg-numeric-format"></a>

主機變數的型別為 `numeric`，而資料庫中的資料是其他型別，且其值無法解讀為 `numeric` 值。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INTERVAL-FORMAT"></a>

### -208 (`ECPG_INTERVAL_FORMAT`) [#](#ecpg-sqlstate-sqlcode-ecpg-interval-format) <a href="#ecpg-sqlstate-sqlcode-ecpg-interval-format" id="ecpg-sqlstate-sqlcode-ecpg-interval-format"></a>

主機變數的型別為 `interval`，而資料庫中的資料是其他型別，且其值無法解讀為 `interval` 值。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-DATE-FORMAT"></a>

### -209 (`ECPG_DATE_FORMAT`) [#](#ecpg-sqlstate-sqlcode-ecpg-date-format) <a href="#ecpg-sqlstate-sqlcode-ecpg-date-format" id="ecpg-sqlstate-sqlcode-ecpg-date-format"></a>

主機變數的型別為 `date`，而資料庫中的資料是其他型別，且其值無法解讀為 `date` 值。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TIMESTAMP-FORMAT"></a>

### -210 (`ECPG_TIMESTAMP_FORMAT`) [#](#ecpg-sqlstate-sqlcode-ecpg-timestamp-format) <a href="#ecpg-sqlstate-sqlcode-ecpg-timestamp-format" id="ecpg-sqlstate-sqlcode-ecpg-timestamp-format"></a>

主機變數的型別為 `timestamp`，而資料庫中的資料是其他型別，且其值無法解讀為 `timestamp` 值。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-CONVERT-BOOL"></a>

### -211 (`ECPG_CONVERT_BOOL`) [#](#ecpg-sqlstate-sqlcode-ecpg-convert-bool) <a href="#ecpg-sqlstate-sqlcode-ecpg-convert-bool" id="ecpg-sqlstate-sqlcode-ecpg-convert-bool"></a>

這表示主機變數的型別為 `bool`，而資料庫中的資料既不是 `'t'`，也不是 `'f'`。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-EMPTY"></a>

### -212 (`ECPG_EMPTY`) [#](#ecpg-sqlstate-sqlcode-ecpg-empty) <a href="#ecpg-sqlstate-sqlcode-ecpg-empty" id="ecpg-sqlstate-sqlcode-ecpg-empty"></a>

送往 PostgreSQL 伺服器的陳述式是空的。（這在嵌入式 SQL 程式中通常不會發生，因此可能表示發生了內部錯誤。）（SQLSTATE YE002）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-MISSING-INDICATOR"></a>

### -213 (`ECPG_MISSING_INDICATOR`) [#](#ecpg-sqlstate-sqlcode-ecpg-missing-indicator) <a href="#ecpg-sqlstate-sqlcode-ecpg-missing-indicator" id="ecpg-sqlstate-sqlcode-ecpg-missing-indicator"></a>

傳回了 null 值，但未提供 null 指示變數。（SQLSTATE 22002）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NO-ARRAY"></a>

### -214 (`ECPG_NO_ARRAY`) [#](#ecpg-sqlstate-sqlcode-ecpg-no-array) <a href="#ecpg-sqlstate-sqlcode-ecpg-no-array" id="ecpg-sqlstate-sqlcode-ecpg-no-array"></a>

在需要陣列的地方使用了一般變數。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-DATA-NOT-ARRAY"></a>

### -215 (`ECPG_DATA_NOT_ARRAY`) [#](#ecpg-sqlstate-sqlcode-ecpg-data-not-array) <a href="#ecpg-sqlstate-sqlcode-ecpg-data-not-array" id="ecpg-sqlstate-sqlcode-ecpg-data-not-array"></a>

資料庫在需要陣列值的地方傳回了一般變數。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-ARRAY-INSERT"></a>

### -216 (`ECPG_ARRAY_INSERT`) [#](#ecpg-sqlstate-sqlcode-ecpg-array-insert) <a href="#ecpg-sqlstate-sqlcode-ecpg-array-insert" id="ecpg-sqlstate-sqlcode-ecpg-array-insert"></a>

無法將該值插入陣列中。（SQLSTATE 42804）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NO-CONN"></a>

### -220 (`ECPG_NO_CONN`) [#](#ecpg-sqlstate-sqlcode-ecpg-no-conn) <a href="#ecpg-sqlstate-sqlcode-ecpg-no-conn" id="ecpg-sqlstate-sqlcode-ecpg-no-conn"></a>

程式嘗試存取不存在的連線。（SQLSTATE 08003）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-NOT-CONN"></a>

### -221 (`ECPG_NOT_CONN`) [#](#ecpg-sqlstate-sqlcode-ecpg-not-conn) <a href="#ecpg-sqlstate-sqlcode-ecpg-not-conn" id="ecpg-sqlstate-sqlcode-ecpg-not-conn"></a>

程式嘗試存取一個確實存在但未開啟的連線。（這是內部錯誤。）（SQLSTATE YE002）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-STMT"></a>

### -230 (`ECPG_INVALID_STMT`) [#](#ecpg-sqlstate-sqlcode-ecpg-invalid-stmt) <a href="#ecpg-sqlstate-sqlcode-ecpg-invalid-stmt" id="ecpg-sqlstate-sqlcode-ecpg-invalid-stmt"></a>

你嘗試使用的陳述式尚未預備。（SQLSTATE 26000）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-DUPLICATE-KEY"></a>

### -239 (`ECPG_INFORMIX_DUPLICATE_KEY`) [#](#ecpg-sqlstate-sqlcode-ecpg-informix-duplicate-key) <a href="#ecpg-sqlstate-sqlcode-ecpg-informix-duplicate-key" id="ecpg-sqlstate-sqlcode-ecpg-informix-duplicate-key"></a>

重複鍵錯誤，違反唯一限制條件（Informix 相容模式）。（SQLSTATE 23505）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR"></a>

### -240 (`ECPG_UNKNOWN_DESCRIPTOR`) [#](#ecpg-sqlstate-sqlcode-ecpg-unknown-descriptor) <a href="#ecpg-sqlstate-sqlcode-ecpg-unknown-descriptor" id="ecpg-sqlstate-sqlcode-ecpg-unknown-descriptor"></a>

找不到所指定的描述區。你嘗試使用的陳述式尚未預備。（SQLSTATE 33000）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-DESCRIPTOR-INDEX"></a>

### -241 (`ECPG_INVALID_DESCRIPTOR_INDEX`) [#](#ecpg-sqlstate-sqlcode-ecpg-invalid-descriptor-index) <a href="#ecpg-sqlstate-sqlcode-ecpg-invalid-descriptor-index" id="ecpg-sqlstate-sqlcode-ecpg-invalid-descriptor-index"></a>

所指定的描述區索引超出範圍。（SQLSTATE 07009）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR-ITEM"></a>

### -242 (`ECPG_UNKNOWN_DESCRIPTOR_ITEM`) [#](#ecpg-sqlstate-sqlcode-ecpg-unknown-descriptor-item) <a href="#ecpg-sqlstate-sqlcode-ecpg-unknown-descriptor-item" id="ecpg-sqlstate-sqlcode-ecpg-unknown-descriptor-item"></a>

要求了無效的描述區項目。（這是內部錯誤。）（SQLSTATE YE002）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-NUMERIC"></a>

### -243 (`ECPG_VAR_NOT_NUMERIC`) [#](#ecpg-sqlstate-sqlcode-ecpg-var-not-numeric) <a href="#ecpg-sqlstate-sqlcode-ecpg-var-not-numeric" id="ecpg-sqlstate-sqlcode-ecpg-var-not-numeric"></a>

在執行動態陳述式期間，資料庫傳回了數值，但主機變數不是數值型別。（SQLSTATE 07006）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-CHAR"></a>

### -244 (`ECPG_VAR_NOT_CHAR`) [#](#ecpg-sqlstate-sqlcode-ecpg-var-not-char) <a href="#ecpg-sqlstate-sqlcode-ecpg-var-not-char" id="ecpg-sqlstate-sqlcode-ecpg-var-not-char"></a>

在執行動態陳述式期間，資料庫傳回了非數值的值，但主機變數是數值型別。（SQLSTATE 07006）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-SUBSELECT-NOT-ONE"></a>

### -284 (`ECPG_INFORMIX_SUBSELECT_NOT_ONE`) [#](#ecpg-sqlstate-sqlcode-ecpg-informix-subselect-not-one) <a href="#ecpg-sqlstate-sqlcode-ecpg-informix-subselect-not-one" id="ecpg-sqlstate-sqlcode-ecpg-informix-subselect-not-one"></a>

子查詢的結果不是單一資料列（Informix 相容模式）。（SQLSTATE 21000）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-PGSQL"></a>

### -400 (`ECPG_PGSQL`) [#](#ecpg-sqlstate-sqlcode-ecpg-pgsql) <a href="#ecpg-sqlstate-sqlcode-ecpg-pgsql" id="ecpg-sqlstate-sqlcode-ecpg-pgsql"></a>

由 PostgreSQL 伺服器所引起的某種錯誤。訊息中包含來自 PostgreSQL 伺服器的錯誤訊息。

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-TRANS"></a>

### -401 (`ECPG_TRANS`) [#](#ecpg-sqlstate-sqlcode-ecpg-trans) <a href="#ecpg-sqlstate-sqlcode-ecpg-trans" id="ecpg-sqlstate-sqlcode-ecpg-trans"></a>

PostgreSQL 伺服器表示無法開始、提交或回復該交易。（SQLSTATE 08007）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-CONNECT"></a>

### -402 (`ECPG_CONNECT`) [#](#ecpg-sqlstate-sqlcode-ecpg-connect) <a href="#ecpg-sqlstate-sqlcode-ecpg-connect" id="ecpg-sqlstate-sqlcode-ecpg-connect"></a>

連線到資料庫的嘗試沒有成功。（SQLSTATE 08001）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-DUPLICATE-KEY"></a>

### -403 (`ECPG_DUPLICATE_KEY`) [#](#ecpg-sqlstate-sqlcode-ecpg-duplicate-key) <a href="#ecpg-sqlstate-sqlcode-ecpg-duplicate-key" id="ecpg-sqlstate-sqlcode-ecpg-duplicate-key"></a>

重複鍵錯誤，違反唯一限制條件。（SQLSTATE 23505）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-SUBSELECT-NOT-ONE"></a>

### -404 (`ECPG_SUBSELECT_NOT_ONE`) [#](#ecpg-sqlstate-sqlcode-ecpg-subselect-not-one) <a href="#ecpg-sqlstate-sqlcode-ecpg-subselect-not-one" id="ecpg-sqlstate-sqlcode-ecpg-subselect-not-one"></a>

子查詢的結果不是單一資料列。（SQLSTATE 21000）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-UNKNOWN-PORTAL"></a>

### -602 (`ECPG_WARNING_UNKNOWN_PORTAL`) [#](#ecpg-sqlstate-sqlcode-ecpg-warning-unknown-portal) <a href="#ecpg-sqlstate-sqlcode-ecpg-warning-unknown-portal" id="ecpg-sqlstate-sqlcode-ecpg-warning-unknown-portal"></a>

指定了無效的游標名稱。（SQLSTATE 34000）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-IN-TRANSACTION"></a>

### -603 (`ECPG_WARNING_IN_TRANSACTION`) [#](#ecpg-sqlstate-sqlcode-ecpg-warning-in-transaction) <a href="#ecpg-sqlstate-sqlcode-ecpg-warning-in-transaction" id="ecpg-sqlstate-sqlcode-ecpg-warning-in-transaction"></a>

交易正在進行中。（SQLSTATE 25001）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-NO-TRANSACTION"></a>

### -604 (`ECPG_WARNING_NO_TRANSACTION`) [#](#ecpg-sqlstate-sqlcode-ecpg-warning-no-transaction) <a href="#ecpg-sqlstate-sqlcode-ecpg-warning-no-transaction" id="ecpg-sqlstate-sqlcode-ecpg-warning-no-transaction"></a>

沒有作用中（進行中）的交易。（SQLSTATE 25P01）

<a id="ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-PORTAL-EXISTS"></a>

### -605 (`ECPG_WARNING_PORTAL_EXISTS`) [#](#ecpg-sqlstate-sqlcode-ecpg-warning-portal-exists) <a href="#ecpg-sqlstate-sqlcode-ecpg-warning-portal-exists" id="ecpg-sqlstate-sqlcode-ecpg-warning-portal-exists"></a>

指定了已存在的游標名稱。（SQLSTATE 42P03）

[返回 34.8. 錯誤處理](ecpg-errors.md#ecpg-errors)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-errors.html)（原文版本：18.6；核對日期：2026-10-22）
