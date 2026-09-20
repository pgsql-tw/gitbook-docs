<a id="LOGICALDECODING-TWO-PHASE-COMMITS"></a>
## 47.10. 邏輯解碼的兩階段提交支援 [#](#LOGICALDECODING-TWO-PHASE-COMMITS)

若只使用基本的輸出外掛程式回呼函式（例如 `begin_cb`、`change_cb`、`commit_cb` 與 `message_cb`），則不會解碼像 `PREPARE TRANSACTION`、`COMMIT PREPARED` 與 `ROLLBACK PREPARED` 這樣的兩階段提交命令。`PREPARE TRANSACTION` 會被忽略，而 `COMMIT PREPARED` 會被解碼為 `COMMIT`，`ROLLBACK PREPARED` 則會被解碼為 `ROLLBACK`。

若要支援兩階段命令的串流，輸出外掛程式需要提供額外的回呼函式。有多個兩階段提交回呼函式是必要的（`begin_prepare_cb`、`prepare_cb`、`commit_prepared_cb`、`rollback_prepared_cb` 與 `stream_prepare_cb`），另外還有一個選用的回呼函式（`filter_prepare_cb`）。

如果提供了用來解碼兩階段提交命令的輸出外掛程式回呼函式，那麼在執行 `PREPARE TRANSACTION` 時，該交易的變更就會被解碼、傳遞給輸出外掛程式，並呼叫 `prepare_cb` 回呼函式。這與基本的解碼設定不同，在基本設定中，變更只有在交易提交時才會被傳遞給輸出外掛程式。已備妥交易的開始，會以 `begin_prepare_cb` 回呼函式來表示。

當使用 `ROLLBACK PREPARED` 回復一個已備妥的交易時，會呼叫 `rollback_prepared_cb` 回呼函式；而當使用 `COMMIT PREPARED` 提交已備妥的交易時，則會呼叫 `commit_prepared_cb` 回呼函式。

輸出外掛程式也可以選擇性地透過 `filter_prepare_cb` 定義篩選規則，只以兩階段方式解碼特定的交易。這可以透過對 *`gid`* 進行樣式比對，或是使用 *`xid`* 查詢來達成。

想要解碼已備妥交易的使用者，需要注意以下幾點：

* 如果已備妥的交易以互斥方式鎖定了［使用者的］目錄資料表，那麼解碼備妥動作可能會被阻塞，直到主交易提交為止。
* 使用這項功能來建構分散式兩階段提交的邏輯複寫解決方案，如果已備妥的交易以互斥方式鎖定了［使用者的］目錄資料表，就可能發生死結。為了避免這種情況，使用者必須避免在這類交易中對目錄資料表加鎖（例如明確的 `LOCK` 命令）。詳情請參閱[第 47.8.2 節](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-two-phase-commits.html)（原文版本：18.6；核對日期：2026-09-15）
