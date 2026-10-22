<a id="RELEASE-18-3"></a>
## E.3. 18.3 版 [#](#RELEASE-18-3)

[E.3.1. 遷移至 18.3 版](release-18-3.md#RELEASE-18-3-MIGRATION)

[E.3.2. 變更內容](release-18-3.md#RELEASE-18-3-CHANGES)

**發佈日期：**2026-02-26

此版本包含自 18.2 以來的少量修正。
關於主要版本 18 的新功能，請參閱
[第 E.6 節](release-18.md)。

<a id="RELEASE-18-3-MIGRATION"></a>

### E.3.1. 遷移至 18.3 版 [#](#RELEASE-18-3-MIGRATION)

執行 18.X 版者不需要進行傾印／還原。

不過，若你是從早於 18.2 的版本升級，
請參閱[第 E.4 節](release-18-2.md)。

<a id="RELEASE-18-3-CHANGES"></a>

### E.3.2. 變更內容 [#](#RELEASE-18-3-CHANGES)

* 修正重播由較舊次要版本產生的 WAL 中的 multixid 截斷記錄後
  發生的失敗 (Heikki Linnakangas)
  [§](https://postgr.es/c/817f74600)

  為了配合先前版本處理 multixid 回捲的方式而設計的邏輯有誤，
  導致重播失敗，並出現類似
  “could not access status of transaction”的訊息。
  可能發生此情況的典型情境，是最新次要版本的待命伺服器
  使用來自較舊版本主要伺服器的 WAL。
* 避免對「TOAST 化」（“toasted”）資料套用 `substring()` 時，
  錯誤地回報編碼無效
  (Noah Misch)
  [§](https://postgr.es/c/6e045e1a6)
  [§](https://postgr.es/c/d04b34d68)
  [§](https://postgr.es/c/4174e41b9)

  CVE-2026-2006 的修正過於嚴格，在實際上有效的情況下，
  也可能擲出字元不完整的錯誤。
* 修正 CVE-2026-2007 修正中的疏漏 (Zsolt Parragi)
  [§](https://postgr.es/c/041e02e6a)

  若因輸入包含的三元組（trigram）多於最初的預估，
  而需要擴大「bounds」陣列，
  `generate_trgm_only` 並未將修改後的
  陣列指標傳回給呼叫端。這會導致
  `strict_word_similarity()` 及相關函式
  產生錯誤的輸出，在少數情況下甚至會當機。當輸入字串
  轉換為小寫後變長時，就會執行到這段有缺陷的程式碼。
  目前已知唯一會發生這種情況的，是在某些單位元組編碼下
  使用 ICU 區域設定時。
* 修正
  `json_strip_nulls()`
  與 `jsonb_strip_nulls()` 的揮發性標記 (Andrew Dunstan)
  [§](https://postgr.es/c/2f6ee7b38)

  這兩個函式一向被視為不可變（immutable），但第 18 版的
  重構意外地將它們標記為穩定（stable）。
  這使它們無法用於索引運算式，並可能在查詢中造成
  不必要的重複求值。此修正會更正新初始化之資料庫叢集
  （包括以 pg_upgrade 升級至 18.3 或更新版本的叢集）中的標記。
  然而，對於以 18.0 至 18.2 建立的既有叢集，此修正沒有幫助。

  若這個錯誤影響到你對這些函式的使用，
  對既有叢集建議的修正方式是手動更新系統目錄。
  請以超級使用者身分，

  ```

  UPDATE pg_catalog.pg_proc SET provolatile = 'i' WHERE oid IN ('3261','3262');
  ```

  在每個受影響的資料庫中執行上述命令。`template0`
  與 `template1` 也要一併更新，讓日後
  建立的資料庫也套用此修正。
* 修正 `LATERAL UNION ALL` 子查詢之輸出
  可能被設為 null 的外部連接集合之計算
  (Richard Guo)
  [§](https://postgr.es/c/ed57c207c)

  此錯誤可能導致誤以為 `NOT NULL` 測試沒有必要
  而將其略過，造成錯誤的查詢輸出。
* 避免使用者自行撰寫的限制條件，與自動命名的 `NOT NULL` 限制條件
  發生名稱衝突
  (Laurenz Albe)
  [§](https://postgr.es/c/8d9a97e0b)

  自第 18 版起，`NOT NULL` 限制條件擁有
  完整的 `pg_constraint` 項目，因此
  需要名稱。為未命名的 `NOT NULL` 限制條件
  選擇名稱的邏輯，未能避免與同一個
  `CREATE TABLE` 陳述式中其他地方
  使用者自行撰寫的限制條件衝突。
* 修正 `pg_stat_get_backend_wait_event()`
  與 `pg_stat_get_backend_wait_event_type()`，
  使其為輔助程序回報值 (Heikki Linnakangas)
  [§](https://postgr.es/c/53463b4b2)

  先前這些函式對輔助程序傳回 NULL，
  但這與
  `pg_stat_activity` 檢視表不一致。
* 修正從 PL/pgSQL 函式傳回複合型別變數的值時，
  將其轉型為網域型別的問題 (Tom Lane)
  [§](https://postgr.es/c/ce4b7e3a1)

  若該變數的值為 NULL，會產生
  “cache lookup failed for type 0”錯誤。
* 修正 `contrib/hstore` 二進位輸入函式中
  可能發生的空指標解參考
  (Michael Paquier)
  [§](https://postgr.es/c/4a0843c53)

  `hstore` 的接收（receive）函式在輸入包含重複鍵時會當機。
  由 Postgres 產生的 `hstore` 值
  永遠不會包含重複鍵，因此這個錯誤
  一直沒有被發現。惡意或損毀的資料可能引發此當機。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-3.html)（原文版本：18.6；核對日期：2026-10-22）
