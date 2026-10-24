<a id="ECPG-LIBRARY"></a>

## 34.11. 函式庫函式 [#](#ecpg-library) <a href="#ecpg-library" id="ecpg-library"></a>

`libecpg` 函式庫主要包含「隱藏」函式，用來實作嵌入式 SQL 命令所表達的功能。不過，也有一些函式適合直接呼叫。請注意，這樣做會使你的程式碼失去可攜性。

* `ECPGdebug(int on, FILE
  *stream)` 若以非零的第一個引數呼叫，會開啟除錯記錄。除錯記錄會寫入 *`stream`*。記錄內容包含所有已代入全部輸入變數的 SQL 陳述式，以及 PostgreSQL 伺服器傳回的結果。在找尋 SQL 陳述式中的錯誤時，這會非常有用。

  ### 注意

  在 Windows 上，如果 ecpg 函式庫與應用程式是以不同的旗標編譯，由於 `FILE` 指標的內部表示方式不同，呼叫此函式會使應用程式當機。具體而言，函式庫與所有使用該函式庫的應用程式，其多執行緒／單執行緒、發行版／除錯版以及靜態／動態等旗標應該相同。
* `ECPGget_PGconn(const char *connection_name)` 會傳回由指定名稱所識別的函式庫資料庫連線控制代碼。若 *`connection_name`* 設為 `NULL`，則傳回目前的連線控制代碼。若無法識別任何連線控制代碼，此函式會傳回 `NULL`。必要時，可以使用傳回的連線控制代碼呼叫 libpq 的任何其他函式。

  ### 注意

  直接以 libpq 常式操作由 ecpg 建立的資料庫連線控制代碼並不是好主意。
* `ECPGtransactionStatus(const char *connection_name)` 會傳回由 *`connection_name`* 所識別之連線目前的交易狀態。關於傳回狀態碼的詳細資訊，請參閱[第 32.2 節](../libpq/libpq-status.md)與 libpq 的 [`PQtransactionStatus`](../libpq/libpq-status.md#LIBPQ-PQTRANSACTIONSTATUS)。
* `ECPGstatus(int lineno,
  const char* connection_name)` 若已連線到資料庫則傳回 true，否則傳回 false。若只使用單一連線，*`connection_name`* 可以為 `NULL`。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-library.html)（原文版本：18.6；核對日期：2026-10-18）
