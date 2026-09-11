<a id="MVCC-SERIALIZATION-FAILURE-HANDLING"></a>

## 13.5. 序列化失敗的處理 [#](#MVCC-SERIALIZATION-FAILURE-HANDLING)

<a id="id-1.5.12.8.2"></a><a id="id-1.5.12.8.3"></a>

Repeatable Read 與 Serializable 隔離等級都可能產生旨在防止序列化異常的錯誤。如前所述，使用這些等級的應用程式必須準備好重試因序列化錯誤而失敗的交易。這類錯誤的訊息文字會依確切的情況而有所不同，但一定會具有 SQLSTATE 代碼 `40001`（`serialization_failure`）。

重試死結失敗也可能是明智的。這類失敗的 SQLSTATE 代碼是 `40P01`（`deadlock_detected`）。

在某些情況下，重試唯一鍵失敗（SQLSTATE 代碼 `23505`，`unique_violation`）與排除限制條件失敗（SQLSTATE 代碼 `23P01`，`exclusion_violation`）也是適當的。例如，如果應用程式在檢查目前儲存的鍵之後，為主鍵欄位選擇一個新值，就可能因為另一個應用程式實例同時選擇了相同的新鍵而發生唯一鍵失敗。這實際上是一種序列化失敗，但伺服器不會將它偵測為序列化失敗，因為它無法「看到」插入的值與先前的讀取之間的關聯。另外也有一些特殊情況，即使伺服器原則上擁有足夠的資訊來判定根本原因是序列化問題，它仍然會發出唯一鍵或排除限制條件錯誤。雖然建議無條件地重試 `serialization_failure` 錯誤，但重試這些其他錯誤代碼時需要更加小心，因為它們可能代表持續存在的錯誤狀況，而不是暫時性的失敗。

重要的是要重試完整的交易，包括決定要發出哪些 SQL 與／或使用哪些值的所有邏輯。因此，PostgreSQL 不提供自動重試功能，因為它無法在保證正確性的情況下做到這一點。

重試交易並不保證被重試的交易會完成；可能需要重試多次。在競爭非常激烈的情況下，完成一個交易可能需要嘗試許多次。在涉及衝突的預備交易（prepared transaction）的情況下，可能要等到該預備交易提交或回復之後才能繼續進行。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html)（原文版本：18.6；核對日期：2026-09-11）
