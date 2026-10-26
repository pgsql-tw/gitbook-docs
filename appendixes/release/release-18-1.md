<a id="RELEASE-18-1"></a>
## E.5. 18.1 版 [#](#release-18-1) <a href="#release-18-1" id="release-18-1"></a>

[E.5.1. 遷移至 18.1 版](release-18-1.md#release-18-1-migration)

[E.5.2. 變更內容](release-18-1.md#release-18-1-changes)

**發佈日期：**2025-11-13

此版本包含自 18.0 以來的多項修正。
關於主要版本 18 的新功能，請參閱
[第 E.6 節](release-18.md)。

<a id="RELEASE-18-1-MIGRATION"></a>

### E.5.1. 遷移至 18.1 版 [#](#release-18-1-migration) <a href="#release-18-1-migration" id="release-18-1-migration"></a>

執行 18.X 版者不需要進行傾印／還原。

<a id="RELEASE-18-1-CHANGES"></a>

### E.5.2. 變更內容 [#](#release-18-1-changes) <a href="#release-18-1-changes" id="release-18-1-changes"></a>

* 在 `CREATE STATISTICS` 中檢查綱要上的
  `CREATE` 權限 (Jelte Fennema-Nio)
  [§](https://postgr.es/c/00eb646ea)

  此疏漏使資料表擁有者可以在任何綱要中建立統計資訊，
  可能導致非預期的名稱衝突。

  PostgreSQL 專案感謝
  Jelte Fennema-Nio 回報此問題。
  (CVE-2025-12817)
* 避免 libpq 內配置大小計算中的整數溢位
  (Jacob Champion)
  [§](https://postgr.es/c/7eb8fcad8)

  libpq 中有幾處在計算記憶體配置所需大小時不夠謹慎。
  足夠大的輸入可能造成整數溢位，導致緩衝區配置過小，
  進而寫入超出緩衝區結尾的位置。

  PostgreSQL 專案感謝 Positive Technologies 的 Aleksey
  Solovev 回報此問題。
  (CVE-2025-12818)
* 當 SQL/JSON 函式（例如 `JSON_VALUE`）的
  `DEFAULT` 子句含有
  `COLLATE` 運算式時，避免出現「unrecognized node type」錯誤 (Jian He)
  [§](https://postgr.es/c/dc9125111)
  [§](https://postgr.es/c/1baae827e)
* 避免對搭配分組集的不含變數之 `HAVING` 子句進行錯誤的最佳化
  (Richard Guo)
  [§](https://postgr.es/c/40c242830)
  [§](https://postgr.es/c/ee49f2cf4)
* 雜湊右半連接不使用平行處理 (Richard Guo)
  [§](https://postgr.es/c/ef6168baf)

  由於更新該連接的共享雜湊表時存在競爭條件，此情況無法可靠運作。
* 建立有序附加（ordered-append）計畫時，避免可能發生的除以零
  (Richard Guo)
  [§](https://postgr.es/c/500f64636)

  此錯誤可能導致選錯成本最低的路徑，或在除錯建置中造成斷言失敗。
* 修正規劃器在處理可以有序存取、但不支援僅索引掃描的索引類型時失敗的問題
  (Maxime Schoemans)
  [§](https://postgr.es/c/74197bdc8)

  此疏忽會導致「no data returned for index-only scan」這類錯誤。
  任何核心內建的索引類型都不會出現這種情況，但有些擴充功能遇到了此問題。
* 移除 btree 索引清理中有誤的斷言 (Peter Geoghegan)
  [§](https://postgr.es/c/61de81a49)
* 避免平行建置 GIN 索引時可能發生的記憶體不足或
  「invalid memory alloc request size」失敗 (Tomas Vondra)
  [§](https://postgr.es/c/a26b753a0)
* 確保 BRIN 自動摘要會為需要快照的索引運算式提供快照
  (Álvaro Herrera)
  [§](https://postgr.es/c/419ffde23)
  [§](https://postgr.es/c/8733f0b54)

  先前，對於這類索引，自動摘要會失敗，並留下佔位用的索引元組，
  導致索引隨時間膨脹。
* 修正資料表包含接近 2^32（2 的 32 次方）個頁面時，
  BRIN 索引掃描的整數溢位風險 (Sunil S)
  [§](https://postgr.es/c/715983a81)

  此疏忽可能導致無窮迴圈，或掃描不需要的資料表頁面。
* 修正 JIT 產生的元組解構（tuple deforming）程式碼對儲存值進行錯誤零擴展的問題
  (David Rowley)
  [§](https://postgr.es/c/ceb51d09b)

  不使用 JIT 時，等效的程式碼進行的是符號擴展而非零擴展，
  使小型整數資料型別的 Datum 表示方式不同。此不一致在多數情況下被掩蓋，
  但已知在使用 Memoize 計畫節點時會導致「could not find memoization table
  entry」錯誤，而且可能還有其他症狀。
* 修正處理雜湊 `GROUPING
  SETS` 查詢時罕見的當機 (David Rowley)
  [§](https://postgr.es/c/0b6a02f03)
* 修復雜湊連接中有誤的雜湊表大小選擇邏輯
  (Tomas Vondra)
  [§](https://postgr.es/c/aa151022e)

  雜湊連接有時會使用超出預期的記憶體，或未能以有效率的方式分配記憶體。
* 改進統計資訊操作函式中的關聯查找邏輯
  (Nathan Bossart)
  [§](https://postgr.es/c/c8af5019b)
  [§](https://postgr.es/c/15d7dded0)

  修正 `pg_restore_relation_stats()`、
  `pg_clear_relation_stats()`、
  `pg_restore_attribute_stats()` 與
  `pg_clear_attribute_stats()`，使其在取得目標關聯的鎖定之前
  （而非之後）檢查權限。
* 修正為觸發程序快取結果關聯資訊的錯誤邏輯
  (David Rowley, Amit Langote)
  [§](https://postgr.es/c/a2387c32f)

  當分割區的欄位集合與其上層分割資料表的欄位集合在實體上不完全相同時，
  此疏忽可能導致當機。
* 修正對分割資料表進行 EvalPlanQual 重新檢查時的當機 (David
  Rowley, Amit Langote)
  [§](https://postgr.es/c/1296dcf18)
* 修正 EvalPlanQual 對於未替 EPQ 準備替代本地連接計畫之外部或自訂連接的處理 (Masahiko
  Sawada, Etsuro Fujita)
  [§](https://postgr.es/c/b14144325)

  在這種情況下，應該正常呼叫外部或自訂存取方法，但實際上並未如此，
  通常會導致當機。
* 避免在 `DETACH
  CONCURRENTLY` 期間重複產生雜湊分割區限制條件 (Haiyang Li)
  [§](https://postgr.es/c/08c037dff)

  `ALTER TABLE DETACH PARTITION CONCURRENTLY` 原本的寫法
  會將分割限制條件的副本加到剛卸離的分割區上。這是不妥的做法，
  部分原因是非並行的 `DETACH` 並不會這麼做，但主要原因是
  在雜湊分割的情況下，限制條件運算式包含對上層資料表 OID 的參照。
  這會在傾印／還原期間，或上層資料表在
  `DETACH` 之後被刪除時造成問題。在 v19 及之後的版本中，我們將完全不再
  建立任何此類複製的限制條件。在已發行的分支中，為了將非預期後果的風險
  降到最低，只有在雜湊分割的情況下才略過加入複製的限制條件。
* 禁止在分割鍵中使用產生欄位
  (Jian He, Ashutosh Bapat)
  [§](https://postgr.es/c/ba99c9491)

  原本就不允許這麼做，但檢查遺漏了某些情況，
  例如欄位參照隱含在整列參照之中的情況。
* 禁止在 `COPY ... FROM
  ... WHERE` 子句中使用產生欄位 (Peter Eisentraut, Jian He)
  [§](https://postgr.es/c/0f9e0068b)

  先前，嘗試參照這類欄位會導致不正確的行為或難以理解的錯誤訊息，
  因為在進行 `WHERE` 過濾的時間點，產生欄位尚未計算出來。
* 若欄位具有非空值限制條件、但該限制條件被標記為無效，
  則禁止將該欄位設為識別欄位 (Jian He)
  [§](https://postgr.es/c/d9ffc2729)

  識別欄位必須為非空值，但相關檢查遺漏了這個邊界情況。
* 避免平行 vacuum 中可能發生的釋放後使用（use-after-free） (Kevin Oommen
  Anish)
  [§](https://postgr.es/c/76613b539)

  此錯誤在標準建置中似乎不會造成任何後果，但理論上仍是一種風險。
* 修正 `pg_temp` 中統計資訊物件的可見性檢查 (Noah Misch)
  [§](https://postgr.es/c/d024160ff)

  位於暫存綱要中的統計資訊物件，無法在不加綱要限定的情況下指名，
  但 `pg_statistics_obj_is_visible()` 沒有考慮到這一點，
  可能不論如何都傳回「true」。連帶地，
  `pg_describe_object()` 等函式可能無法如預期般
  以綱要限定物件的名稱。
* 修正建立資料庫的 WAL 重播期間的輕微記憶體洩漏
  (Nathan Bossart)
  [§](https://postgr.es/c/33e7b4a7c)
* 修正 `pg_stat_replication` 檢視表中複寫延遲的錯誤回報 (Fujii Masao)
  [§](https://postgr.es/c/9670032cc)

  若任何待命伺服器的重播 LSN 停止前進，
  `write_lag`
  與 `flush_lag` 欄位最終會停止更新。
* 避免針對無效的 `primary_slot_name` 設定
  重複記錄日誌訊息 (Fujii Masao)
  [§](https://postgr.es/c/6ff7ba9fe)
* 避免 `synchronized_standby_slots`
  參照不存在的複寫插槽時發生失敗 (Shlok Kyal)
  [§](https://postgr.es/c/b45a8d7d8)
* 將複寫插槽的狀態寫入磁碟失敗後，移除未完成的插槽狀態檔
  (Michael Paquier)
  [§](https://postgr.es/c/9a6ea00ac)

  先前，像磁碟空間不足這類失敗，會留下暫存的
  `state.tmp` 檔案。這是有問題的，
  因為它會阻擋之後所有寫入狀態的嘗試，需要手動介入清理。
* 修正邏輯複寫平行套用工作程序對鎖定逾時信號的錯誤處理
  (Hayato Kuroda)
  [§](https://postgr.es/c/37fc5de43)

  工作程序關閉與鎖定逾時使用了相同的信號編號，因而造成混淆。
* 從串流切換為封存 WAL 來源時，避免非預期地關閉 WAL 接收程序
  (Xuneng Zhou)
  [§](https://postgr.es/c/a14201073)

  在時間軸變更期間，待命伺服器的 WAL 接收程序應該保持運作，
  等待新的 WAL 串流起始點。但實際上它卻不斷關閉、又立即被重新啟動，
  可能使狀態監控程式碼產生混淆。
* 修正 pgoutput 邏輯解碼外掛所維護之關聯同步快取中的
  釋放後使用問題 (Vignesh C, Masahiko Sawada)
  [§](https://postgr.es/c/32b95fc71)

  邏輯解碼期間發生的錯誤，可能導致同一工作階段中
  後續的邏輯解碼嘗試當機。
  只有透過 SQL 函式呼叫 pgoutput
  時才會遇到此情況。
* 避免不必要地使邏輯複寫插槽失效
  (Bertrand Drouvot)
  [§](https://postgr.es/c/bf3dba508)
* 在語系設定中恢復 `C` 定序的特殊處理
  (Jeff Davis)
  [§](https://postgr.es/c/3ebea75f9)

  這修正了在後端啟動初期、尚未選定資料庫之前，存取共享系統目錄時的退化問題。
  目前未知任何核心 PostgreSQL 程式碼
  會因此出問題，但有些擴充功能因而無法正常運作。
* 修正在檢查使用者是否具有 Windows 系統管理員權限失敗時，
  相關訊息輸出錯誤的問題 (Bryan Green)
  [§](https://postgr.es/c/b48ae226e)

  這段程式碼原本會當機，或至少印出亂碼。
  不過目前尚無此類案例的回報，顯示這些系統呼叫失敗的情況極為罕見。
* 避免以特定 libsanitizer 選項測試
  PostgreSQL 時當機
  (Emmanuel Sibi, Jacob Champion)
  [§](https://postgr.es/c/6d8acb777)
* 修正 64 位元 Windows 上除錯建置中，記憶體上下文檢查的誤報警告
  (David Rowley)
  [§](https://postgr.es/c/af3a79e08)
* 正確處理 PL/pgSQL 指派陳述式中的 `GROUP BY DISTINCT`
  (Tom Lane)
  [§](https://postgr.es/c/78a284b0b)

  剖析器在此情境中未能記錄 `DISTINCT` 選項，
  使命令的行為如同單純的 `GROUP BY`。
* 避免在 PL/Python 中處理 SQL 錯誤時洩漏記憶體
  (Tom Lane)
  [§](https://postgr.es/c/447a794f6)

  這修正了在我們先前的次要版本中引入、會持續整個工作階段的記憶體洩漏。
* 修正 libpq 的 GSSAPI 邏輯在 Windows 上
  對通訊端（socket）相關錯誤的處理 (Ning Wu, Tom Lane)
  [§](https://postgr.es/c/d83879a32)

  以 GSSAPI 加密／解密傳輸資料的程式碼，未能正確辨識連線通訊端上的錯誤狀況，
  因為 Windows 回報這類錯誤的方式與其他平台不同。
  這導致在 Windows 上無法建立此類連線。
* 修正繼承資料表欄位上非繼承之非空值限制條件的傾印
  (Dilip Kumar)
  [§](https://postgr.es/c/0fe07fa11)

  從 v18 之前的伺服器傾印時，pg_dump 未能保留
  此類限制條件。
* 修正 pg_dump 對外鍵限制條件的
  排序 (Álvaro Herrera)
  [§](https://postgr.es/c/162e70ea0)

  確保這些資料庫物件的排序一致，如同其他物件類型早已做到的一樣。
* 修正 pg_dump
  與 pg_restore 資料壓縮邏輯中的多項錯誤
  (Daniel Gustafsson, Tom Lane)
  [§](https://postgr.es/c/8980c724b)
  [§](https://postgr.es/c/6a4009747)
  [§](https://postgr.es/c/aa1fcd087)

  有幾處的錯誤檢查缺漏或不正確，也有一些會在大端序（big-endian）硬體上
  出現的可攜性問題。這些問題之所以一直未被發現，是因為這段程式碼
  只用於讀取目錄格式傾印中經過壓縮的 TOC 檔案。pg_dump 從不產生這種
  傾印；只有在事後手動壓縮 TOC 檔案時才會遇到此情況，
  這是受支援的做法，但非常少見。
* 修正 pgbench，使其在開始
  `COPY` 操作時乾淨地以錯誤結束 (Anthonin Bonnefoy)
  [§](https://postgr.es/c/c00637b5f)

  pgbench 並不打算支援此情況，但先前它會陷入無窮迴圈。
* 修正 pgbench 對多個錯誤的回報
  (Yugo Nagata)
  [§](https://postgr.es/c/29aabbc43)

  當連續兩次 `PQgetResult` 呼叫
  都失敗時，pgbench 可能回報錯誤的
  錯誤訊息。
* 在 pgbench 中，修正關於
  管線模式中錯誤的有誤斷言 (Yugo Nagata)
  [§](https://postgr.es/c/c736808e0)
* 修正 pg_combinebackup 中每個檔案的記憶體洩漏
  (Tom Lane)
  [§](https://postgr.es/c/e2072b47b)
* 確保 `contrib/pg_buffercache` 的函式
  可以被取消 (Satyanarayana Narlapuram, Yuhang Qiu)
  [§](https://postgr.es/c/71aa2e114)
  [§](https://postgr.es/c/0beb7e933)

  有些程式碼路徑可能長時間執行而不檢查中斷。
* 修正 `contrib/pg_prewarm` 對索引的
  權限檢查 (Ayush Vatsa, Nathan Bossart)
  [§](https://postgr.es/c/3ccf8e9ac)
  [§](https://postgr.es/c/c29d32d27)

  `pg_prewarm()` 要求對要預熱的關聯具有 `SELECT`
  權限。然而，由於索引本身沒有自己的 SQL 權限，這導致非超級使用者
  無法預熱索引。改為檢查
  索引所屬資料表的 `SELECT` 權限。
* 在 `contrib/pg_stat_statements` 中，避免
  兩個或更多常數被標記為位於 SQL 陳述式文字中同一位置時
  發生當機 (Sami Imseih, Dmitry Dolgov)
  [§](https://postgr.es/c/b1635c166)
* 讓 `contrib/pgstattuple` 在面對
  空白或無效的索引頁面時更加穩健 (Nitin Motiani)
  [§](https://postgr.es/c/fc295beb7)

  將全為零的頁面計為可用空間，並忽略依頁面特殊空間大小的檢查判定為無效的頁面。
  btree 索引的程式碼原本就會將全為零的頁面計為可用空間，
  但 hash 與 gist 的程式碼會報錯，這已被認為對使用者
  遠不夠友善。同樣地，讓三種情況一致地
  忽略損壞的頁面，而不是擲出錯誤。
* 強化讀取與寫入屏障巨集，以滿足 Clang 的要求
  (Thomas Munro)
  [§](https://postgr.es/c/f8ccab0e9)

  我們原本假設 `__atomic_thread_fence()` 是
  足以防止 C 編譯器在其前後重新排列記憶體存取的屏障，
  但對 Clang 而言似乎並非如此，
  使它至少可能為 RISC-V、MIPS
  與 LoongArch 機器產生不正確的程式碼。加入明確的編譯器屏障來修正此問題。
* 修正 PGXS 建置基礎架構，以支援為擴充功能建置
  NLS `po` 檔案 (Ryo Matsumura)
  [§](https://postgr.es/c/6aa04a60c)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-1.html)（原文版本：18.6；核對日期：2026-10-22）
