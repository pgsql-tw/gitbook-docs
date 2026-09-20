<a id="LOGICALDECODING-STREAMING"></a>
## 47.9. 邏輯解碼的大型交易串流 [#](#LOGICALDECODING-STREAMING)

基本的輸出外掛程式回呼函式（例如 `begin_cb`、`change_cb`、`commit_cb` 與 `message_cb`），只有在交易真正提交時才會被呼叫。變更仍然會從交易日誌中逐步解碼，但只有在提交時（也就是從交易日誌中解碼出提交動作時）才會被傳遞給輸出外掛程式，如果交易中止，這些變更就會被捨棄。

這表示雖然解碼是逐步進行的，而且可能會溢出至磁碟以控制記憶體用量，但所有已解碼的變更，都必須等到交易最終提交時才能傳送（或者更精確地說，是在從交易日誌中解碼出提交動作時）。視交易的大小與網路頻寬而定，這段傳輸時間可能會大幅增加套用延遲。

為了減少大型交易所造成的套用延遲，輸出外掛程式可以提供額外的回呼函式，以支援對進行中交易的漸進式串流。有多個串流回呼函式是必要的（`stream_start_cb`、`stream_stop_cb`、`stream_abort_cb`、`stream_commit_cb` 與 `stream_change_cb`），另外還有兩個選用的回呼函式（`stream_message_cb` 與 `stream_truncate_cb`）。此外，如果要支援兩階段命令的串流，就必須提供額外的回呼函式（詳情請見[第 47.10 節](logicaldecoding-two-phase-commits.md)）。

在串流一個進行中的交易時，變更（與訊息）會以 `stream_start_cb` 與 `stream_stop_cb` 回呼函式所劃分出的區塊方式串流傳送。等到所有已解碼的變更都傳送完畢後，就可以使用 `stream_commit_cb` 回呼函式提交該交易（或使用 `stream_abort_cb` 回呼函式將其中止）。如果支援兩階段提交，則可以使用 `stream_prepare_cb` 回呼函式備妥該交易，再以 `commit_prepared_cb` 回呼函式執行 `COMMIT PREPARED`，或以 `rollback_prepared_cb` 將其中止。

以下是某個交易的串流回呼函式呼叫順序範例：

```

stream_start_cb(...);   <-- start of first block of changes
  stream_change_cb(...);
  stream_change_cb(...);
  stream_message_cb(...);
  stream_change_cb(...);
  ...
  stream_change_cb(...);
stream_stop_cb(...);    <-- end of first block of changes

stream_start_cb(...);   <-- start of second block of changes
  stream_change_cb(...);
  stream_change_cb(...);
  stream_change_cb(...);
  ...
  stream_message_cb(...);
  stream_change_cb(...);
stream_stop_cb(...);    <-- end of second block of changes


[a. when using normal commit]
stream_commit_cb(...);    <-- commit of the streamed transaction

[b. when using two-phase commit]
stream_prepare_cb(...);   <-- prepare the streamed transaction
commit_prepared_cb(...);  <-- commit of the prepared transaction
```

當然，實際的回呼函式呼叫順序可能會更複雜。可能會有多個串流交易各自的區塊、其中某些交易可能會被中止，等等。

與溢出至磁碟的行為類似，當從 WAL 解碼出的變更總量（涵蓋所有進行中的交易）超過 `logical_decoding_work_mem` 設定所定義的限制時，就會觸發串流。此時，系統會選出最大的頂層交易（依目前用於已解碼變更的記憶體用量來衡量）並加以串流。不過，在某些情況下，即使已啟用串流，我們仍然必須溢出至磁碟，因為雖然超過了記憶體門檻，卻仍然尚未解碼出完整的資料列，例如只解碼出了 TOAST 資料表的插入，卻還沒有解碼出主資料表的插入。

即使在串流大型交易時，變更仍然會依提交順序套用，維持與非串流模式相同的保證。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logicaldecoding-streaming.html)（原文版本：18.6；核對日期：2026-09-15）
