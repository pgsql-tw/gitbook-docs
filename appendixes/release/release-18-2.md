<a id="RELEASE-18-2"></a>
## E.4. 18.2 版 [#](#RELEASE-18-2)

[E.4.1. 遷移至 18.2 版](release-18-2.md#RELEASE-18-2-MIGRATION)

[E.4.2. 變更內容](release-18-2.md#RELEASE-18-2-CHANGES)

**發佈日期：**2026-02-12

此版本包含自 18.1 以來的多項修正。
關於主要版本 18 的新功能，請參閱
[第 E.6 節](release-18.md)。

<a id="RELEASE-18-2-MIGRATION"></a>

### E.4.1. 遷移至 18.2 版 [#](#RELEASE-18-2-MIGRATION)

執行 18.X 版者不需要進行傾印／還原。

不過，若你在 `ltree` 欄位上建有任何索引，
更新後可能需要重新建立這些索引。請參閱下方第六個變更項目。

<a id="RELEASE-18-2-CHANGES"></a>

### E.4.2. 變更內容 [#](#RELEASE-18-2-CHANGES)

* 防範 `oidvector`／`int2vector` 出現非預期的
  維度 (Tom Lane)
  [§](https://postgr.es/c/3b6588cd9)

  這些資料型別預期是不含 NULL 的一維陣列，
  但有些轉型途徑允許違反這些預期。
  有些函式依賴這些預期卻未加以驗證，因而可能產生異常行為；
  現在為這些函式加入檢查。

  PostgreSQL 專案感謝
  Altan Birler 回報此問題。
  (CVE-2026-2003)
* 強化選擇率估算器，防範它被附加到接受非預期資料型別的運算子上
  (Tom Lane)
  [§](https://postgr.es/c/66ddac698)
  [§](https://postgr.es/c/b69af3dda)

  `contrib/intarray` 含有一個選擇率
  估算函式，由於它未檢查輸入是否為預期的資料型別，
  可能被濫用來執行任意程式碼。第三方擴充功能應該檢查是否有類似的
  風險，並採用 intarray 現在使用的技巧加入防護。
  由於擴充功能的此類修正需要時間，我們現在要求必須具有超級使用者
  權限，才能將非內建的選擇率估算器附加到
  運算子上。

  PostgreSQL 專案感謝
  Daniel Firer（透過 zeroday.cloud）回報此問題。
  (CVE-2026-2004)
* 修正 `contrib/pgcrypto` 的
  PGP 解密函式中的緩衝區溢位 (Michael Paquier)
  [§](https://postgr.es/c/209f387b8)

  解密一則帶有過長工作階段金鑰的特製訊息會造成
  緩衝區溢位，後果可能嚴重到執行任意程式碼。

  PostgreSQL 專案感謝
  Team Xint Code（透過 zeroday.cloud）回報此問題。
  (CVE-2026-2005)
* 修正多位元組字元長度驗證不足的問題
  (Thomas Munro, Noah Misch)
  [§](https://postgr.es/c/df0852fe0)
  [§](https://postgr.es/c/efef05ba9)
  [§](https://postgr.es/c/7b5fc85be)
  [§](https://postgr.es/c/b0f5d25bc)
  [§](https://postgr.es/c/b42709194)
  [§](https://postgr.es/c/4543b02af)

  多項錯誤使能夠送出特製 SQL 的攻擊者可以
  造成字串緩衝區溢位，後果可能嚴重到執行任意程式碼。
  套用這些修正後，當字串函式處理已儲存在資料庫中的無效文字時，
  應用程式可能會看到「invalid byte sequence for encoding」錯誤。

  PostgreSQL 專案感謝 Paul Gerste
  與 Moritz Sanft（透過 zeroday.cloud）回報此
  問題。
  (CVE-2026-2006)
* 強化 `contrib/pg_trgm`，防範字串轉小寫
  行為的變化 (Heikki Linnakangas)
  [§](https://postgr.es/c/e0965fb1a)
  [§](https://postgr.es/c/18548681d)

  修正可能的緩衝區溢位；其起因是在某些語系中，
  將字串轉為小寫可能產生比原字串更多的字元（而非
  位元組）。此行為是版本 18 新出現的，此錯誤也是。

  PostgreSQL 專案感謝
  Heikki Linnakangas 回報此問題。
  (CVE-2026-2007)
* 修正 `contrib/ltree` 中不一致的不分大小寫比對
  (Jeff Davis)
  [§](https://postgr.es/c/806555e30)
  [§](https://postgr.es/c/8993bf099)

  `ltree` 中與索引相關的常式所使用的大小寫摺疊實作，
  與主要運算子所使用的不同。
  只有在預設定序提供者為 libc 且編碼為單位元組時，兩者的行為才相同。

  修正方式是將程式碼改為使用資料庫預設定序進行大小寫摺疊。
  此變更將需要重新建立 `ltree`
  欄位上的索引（不論索引存取方法為何），除非該資料庫
  使用 libc 作為定序提供者且其編碼為單位元組。
  若不重新建立，搜尋這類索引時將無法找到相關的項目。
* 使用 `ALTER TABLE ... ADD CONSTRAINT` 加入
  具有明確名稱的非空值限制條件時，若欄位
  已標記為 NOT NULL，則要求所提供的名稱必須與
  既有的限制條件名稱相符 (Álvaro Herrera, Srinath Reddy Sadipiralla)
  [§](https://postgr.es/c/492a69e14)
* 不允許子查詢中的 CTE 參照決定彙總函式的語意
  層級 (Tom Lane)
  [§](https://postgr.es/c/12bc32917)

  此變更撤銷了兩個次要版本之前所做的變更，改為
  在子查詢參照的 CTE 位於標準 SQL 規則根據其中所含欄位參照與彙總函式
  指派給該彙總函式的語意層級之下時擲出錯誤。先前嘗試的
  修正本身也引發了問題，而且目前仍不清楚
  應該改用什麼做法。由於 SQL 標準完全不允許在彙總函式中使用
  子查詢，將這類情況視為錯誤應該
  已經足夠。
* 修正 CTE 查詢中 `MERGE` 的觸發程序轉換資料表擷取
  (Dean Rasheed)
  [§](https://postgr.es/c/c6ce4dcf9)

  當執行一個資料修改 CTE 查詢，而該查詢在具有
  陳述式層級 `AFTER` 觸發程序的資料表上同時包含
  `MERGE` 與另一個 DML 操作時，傳遞給觸發程序的轉換
  資料表不會包含受 `MERGE` 影響的資料列，
  只包含受其他操作影響的資料列。
* 修正錯誤修剪屬於非關聯範圍表項目（例如子查詢）之
  rowmark 的問題 (Dean Rasheed)
  [§](https://postgr.es/c/f335457e8)

  若擬議的資料列更新需要經由 EvalPlanQual 重新檢查
  加以修改（例如對該資料列有並行更新時就可能發生），此問題會導致不正確的結果。
* 修正當更新或刪除操作的分割目標資料表之所有子資料表
  都已被修剪時發生的失敗 (Amit Langote)
  [§](https://postgr.es/c/9f4b7bfc5)

  在這種情況下，即使實際上不需要做任何事，執行器仍可能回報「could not find junk
  ctid column」錯誤。
* 修正陣列下標中子查詢的運算式求值
  錯誤 (Andres Freund)
  [§](https://postgr.es/c/bdc5dedfc)
* 修正非確定性定序下的文字子字串搜尋
  (Laurenz Albe)
  [§](https://postgr.es/c/18b349315)

  使用非確定性定序時，我們未能偵測到出現在
  被搜尋字串最尾端的相符項目。
* 避免查詢包含重複的視窗函式呼叫時可能發生的規劃器失敗
  (Meng Zhang, David Rowley)
  [§](https://postgr.es/c/ccde5be68)

  對這類呼叫去重複時的混淆，可能導致類似
  「WindowFunc with winref 2 assigned to WindowAgg with
  winref 1」的錯誤。
* 修正規劃器在處理集合回傳函式與分組集時的錯誤
  (Richard Guo)
  [§](https://postgr.es/c/382ce9cb7)

  建構 ProjectSet 計畫節點時，規劃器未能
  偵測到涉及分組運算式的子運算式
  已由輸入計畫計算完成。這會導致低效率的計畫，
  或「variable not found in subplan target
  list」之類的錯誤。
* 當子查詢的分組子句包含易變（volatile）函式或集合回傳函式時，
  避免不正確的最佳化 (Richard Guo)
  [§](https://postgr.es/c/7650eabb6)

  規劃器原本會將參照此類分組欄位的外層查詢限制條件下推，
  因而由於易變函式被多次求值而導致不正確的行為，
  或因集合回傳函式被引入
  子查詢的 `WHERE`／`HAVING`
  子句而導致錯誤。
* 搜尋關於某個運算式的統計資訊時，穿透 PlaceHolderVar 節點
  (Richard Guo)
  [§](https://postgr.es/c/7e9f852a7)

  此變更使規劃器能夠找到有關從子查詢上拉、或用於 `GROUP
  BY` 的運算式之相關統計資訊，而不必退回使用預設估計值。
  （或許我們應該調整所找到的統計資訊，以反映該值為 NULL 的
  機率提高，但我們對於一般的 Var 也從未做過
  對應的處理。）雖然此限制
  早已存在，但 PostgreSQL 版本 18 的變更
  使 PlaceHolderVar 比以前更常見，因此做出此變更，以
  避免受影響情況下的計畫退化。
* 將運算式比對到索引時，穿透無作用的 PlaceHolderVar 節點
  (Richard Guo)
  [§](https://postgr.es/c/b4cf74420)

  由於 PostgreSQL 版本 18 在比以前更多的情況下使用
  PlaceHolderVar，有些先前能夠使用索引的查詢
  變得無法使用。加入邏輯以避免此退化。
* 修正規劃器將 `OR` 子句轉換為
  ScalarArrayOp 索引條件的處理 (Tender Wang, Tom Lane)
  [§](https://postgr.es/c/bf5b13a8a)

  程式碼未正確處理 RelabelType 節點，可能
  產生無效的運算式，或未能執行有效的轉換。
* 即使部分雜湊索引的述詞已蘊含 WHERE 子句為真，
  仍允許對其使用索引掃描 (Tom Lane)
  [§](https://postgr.es/c/a212877dc)

  通常我們會捨棄被述詞蘊含的 WHERE 子句，
  因為測試它毫無意義；它對每個索引
  項目必然成立。然而，若索引要求在前導索引
  鍵上要有 WHERE 子句（雜湊索引即是如此），這樣做可能會使索引掃描計畫無法建立。
  在考慮這類索引時，不要捨棄被蘊含的子句。
* 不為無日誌的 BRIN 索引產生 WAL (Kirill Reshke)
  [§](https://postgr.es/c/d77a5f981)

  某個很少走到的程式碼路徑，即使索引已標記為無日誌，
  仍會錯誤地產生與 BRIN 索引相關的 WAL 記錄。
  當機復原接著會無法重播該記錄，並抱怨
  檔案已存在。
* 在平行建置 GIN 索引時使用正確的排序函式
  (Tomas Vondra)
  [§](https://postgr.es/c/eee71a66c)

  平行處理的程式碼使用預設的排序運算子（由
  欄位資料型別的 btree 運算子類別決定），然而它
  應該使用 GIN 運算子類別所指定的排序函式（若有的話）。
  這會導致資料型別沒有 btree 運算子類別時失敗，
  或在運算子類別指定的排序函式
  與 btree 運算子類別不一致時產生無效的索引。
* 防止截斷仍被未讀取之 `NOTIFY` 訊息所需要的
  CLOG (Joel Jacobson, Heikki
  Linnakangas)
  [§](https://postgr.es/c/321ec5462)
  [§](https://postgr.es/c/7b069a187)
  [§](https://postgr.es/c/82fa6b78d)

  此修正可避免後端程序吸收
  `NOTIFY` 訊息的速度緩慢時，出現「could not access status of
  transaction」錯誤。
* 將處理 `NOTIFY` 訊息期間發生的錯誤
  提升為 FATAL，亦即關閉連線 (Heikki Linnakangas)
  [§](https://postgr.es/c/aab4a84bb)

  先前，若後端程序在吸收
  `NOTIFY` 訊息時發生錯誤，它會越過該
  訊息、將錯誤回報給用戶端，然後繼續執行。不過這種行為
  問題重重。一大顧慮是
  用戶端沒有好方法得知某則通知已遺失，而且
  當然也無從得知其內容。視
  應用程式邏輯而定，遺漏一則通知可能使
  應用程式卡在等待狀態，諸如此類。此外，其餘的
  訊息在有人送出新的
  `NOTIFY` 之前都不會被處理。

  另外，若收到
  `NOTIFY` 信號時連線處於閒置狀態，基於不相關的考量，任何 ERROR 本來就會被提升為
  FATAL。因此，我們選擇
  讓所有情況都這麼做，以求一致，並向應用程式提供
  明確的信號，表示它可能遺漏了某些
  通知。
* 計算查詢 ID 雜湊時納入分組運算式的考量
  (Jian He)
  [§](https://postgr.es/c/9c3caad02)

  先前，兩個只有 `GROUP
  BY` 運算式不同的查詢，會被
  `contrib/pg_stat_statements` 及其他使用
  查詢 ID 的功能合併。
* 修正有並行更新時 `EXPLAIN ANALYZE
  MERGE` 中更新次數計算錯誤的問題 (Dean Rasheed)
  [§](https://postgr.es/c/5749d95d4)

  這種情況會導致 `EXPLAIN` 輸出中「skipped」
  元組的計數不正確，或在啟用斷言的建置中造成斷言
  失敗。
* 修正鎖定元組時追蹤更新鏈的錯誤 (Jasper
  Smit)
  [§](https://postgr.es/c/3e3a80f62)

  此程式碼路徑忽略了檢查更新鏈中第一個新元組的 xmin，
  因此若原本的更新者中止，而該空間又立即被
  `VACUUM` 回收並重新使用，就可能鎖定一個不相關的元組。
  這可能造成非預期的交易延遲或死結。
  也曾觀察到與識別錯誤元組相關的錯誤。
* 修正大型資料表增量備份的錯誤處理
  (Robert Haas, Oleg Tkachenko)
  [§](https://postgr.es/c/c80b0c9d6)

  若超過 1GB（或一般而言，該安裝的區段
  大小）的資料表在基礎
  備份與增量
  備份之間被 `VACUUM` 截斷，pg_combinebackup 可能失敗，
  並出現關於「truncation block length in excess of segment
  size」的錯誤。這會使增量備份無法還原。
* 修正後端程序在結束時，因嘗試在已解除對應的共享記憶體區段中
  釋放鎖定而可能當機的問題
  (Rahila Syed)
  [§](https://postgr.es/c/1943ceb38)
* 修正非同步 I/O 程式碼中的競爭條件 (Andres Freund)
  [§](https://postgr.es/c/7f1b3a4ce)

  非同步 I/O 操作的結果代碼有可能在被
  讀取之前就被覆寫。
* 防範當機後錯誤截斷 multixact 日誌
  (Heikki Linnakangas)
  [§](https://postgr.es/c/09532a78b)
* 修正 `pg_stat_get_backend_activity()` 的結果
  可能編碼錯誤的問題 (Chao Li)
  [§](https://postgr.es/c/06907e864)

  存放工作階段活動字串的共享記憶體緩衝區，結尾可能是
  不完整的多位元組字元。讀取者應該
  截掉任何此類不完整的字元，但此函式
  沒有這麼做。
* 防範遞迴的記憶體上下文日誌記錄 (Fujii Masao)
  [§](https://postgr.es/c/b863d8d87)

  持續不斷要求記錄記憶體上下文的信號，可能
  造成日誌記錄程式碼遞迴執行，理論上可能
  導致堆疊溢位。
* 修正重新初始化平行執行上下文時的記憶體上下文用法
  (Jakub Wartak, Jeevan Chalke)
  [§](https://postgr.es/c/57df5ab80)

  此錯誤可能因某個附屬資料
  結構的生命週期比平行上下文短而導致當機。
  目前未知只使用
  核心 PostgreSQL 就能觸發此問題，但有回報指出
  擴充功能中出現了狀況。
* 建立新的 multixid 時設定下一個 multixid 的偏移量，以移除
  在極端情況下所需的等待迴圈 (Andrey Borodin)
  [§](https://postgr.es/c/e46041fd9)
  [§](https://postgr.es/c/02ba5e3be)

  先前的邏輯可能卡在等待一個永遠
  不會發生的更新。
* 避免資料修改 CTE 被重寫超過一次 (Bernice Southey,
  Dean Rasheed)
  [§](https://postgr.es/c/b880d9a02)

  先前，在更新可自動更新的檢視表或帶有
  規則的關聯時，若原始查詢含有任何資料修改 CTE，重寫器
  會因為遞迴而多次重寫這些 CTE。這
  不但沒有效率，而且若 CTE 包含對
  永遠產生（always-generated）欄位的更新，還可能產生錯誤的錯誤回報。
* 允許重試 DSM 登錄項目的初始化
  (Nathan Bossart)
  [§](https://postgr.es/c/b83bcc0df)

  若動態共享記憶體項目的初始化中途失敗，
  允許下一次嘗試使用該項目時重試
  初始化。先前該項目會停留在
  永久失敗的狀態。
* 避免頁面已被換出時 NUMA 狀態檢視表失敗
  (Tomas Vondra)
  [§](https://postgr.es/c/9796c4f56)
* 避免使用較舊的 libnuma 版本查詢 NUMA 頁面狀態時
  出現「operation not permitted」錯誤 (Tomas Vondra)
  [§](https://postgr.es/c/482e98ac4)
* 若 WAL 未能一路回溯到檢查點記錄所指出的重做（redo）點，
  則使復原失敗 (Nitin Jadhav)
  [§](https://postgr.es/c/68ebdf2b0)

  在開始復原之前加入對此的明確檢查，使其
  不會造成損害，並提供有用的錯誤訊息。先前，
  在這種情況下復原可能當機或損毀資料庫。
* 避免在 `ALTER
  PUBLICATION` 期間竄改來源查詢樹 (Sunil S)
  [§](https://postgr.es/c/bea57a6b4)

  此錯誤造成的可見影響是：為該查詢觸發的事件觸發程序
  只會看到第一個 `publish`
  選項，即使指定了好幾個。若這樣的查詢被
  設定為預備陳述式，重新執行時也會出現異常行為。
* 將 `CREATE SUBSCRIPTION
  ... CONNECTION` 中指定的連線選項傳遞給發佈者的 walsender (Fujii Masao)
  [§](https://postgr.es/c/797fc5d1b)

  在此修正之前，`options` 連線選項
  （若有的話）會被忽略，因此例如無法在
  walsender 工作階段中設定自訂的伺服器參數值。原本的設計就是要讓
  這能夠運作，而且在
  PostgreSQL 版本 15 的重構破壞它之前確實可以運作，因此
  恢復先前的行為。
* 防止新建立或新同步的複寫插槽
  失效 (Zhijie Hou)
  [§](https://postgr.es/c/919c9fa13)
  [§](https://postgr.es/c/1c60f7236)
  [§](https://postgr.es/c/d3ceb2084)

  與並行檢查點之間的競爭條件，可能使複寫插槽所需的 WAL
  被移除，導致該插槽
  立即被標記為無效。
* 修正計算複寫插槽所需 xmin 時的競爭條件
  (Zhijie Hou)
  [§](https://postgr.es/c/fd7c86cfa)

  這可能導致「cannot build an initial slot
  snapshot as oldest safe xid follows snapshot's xmin」錯誤。
* 在邏輯複寫
  訂閱的初始同步期間，於開始複製資料之前，
  先提交新增的
  `pg_replication_origin` 項目 (Zhijie Hou)
  [§](https://postgr.es/c/b07c32619)

  先前，若複製步驟失敗，
  新的 `pg_replication_origin` 項目會因
  交易回復而遺失。這會導致共享記憶體中的
  狀態不一致。
* 平行工作程序套用失敗後，不推進邏輯複寫進度
  (Zhijie Hou)
  [§](https://postgr.es/c/2f7ffe124)

  先前的行為可能使訂閱者
  遺失交易。
* 修正邏輯複寫的插槽同步（slotsync）工作程序，使其正確處理
  LOCK_TIMEOUT 信號 (Zhijie Hou)
  [§](https://postgr.es/c/6c61c69d5)

  先前，逾時信號實際上會被忽略。
* 修正重新啟動串流複寫備援伺服器時，可能以
  「unexpected data beyond EOF」失敗的問題 (Anthonin Bonnefoy)
  [§](https://postgr.es/c/9ed411e08)
* 修正 SQL/JSON 路徑型別不符時的錯誤回報 (Jian He)
  [§](https://postgr.es/c/15ba0702c)

  程式碼可能產生「cache lookup failed for type 0」
  錯誤，而不是原本預期的、指出路徑運算式
  型別不正確的錯誤訊息。
* 修正剖析分割區範圍界限時錯誤追蹤欄位位置的問題
  (myzhen)
  [§](https://postgr.es/c/c35e5dd9a)

  例如，這可能導致在關於將分割區界限值轉型為欄位資料型別的
  錯誤訊息中，引用錯誤的欄位名稱。
* 修正錯誤訊息中的多項小錯誤 (Man Zeng, Tianchen Zhang)
  [§](https://postgr.es/c/acfa422c3)
  [§](https://postgr.es/c/2ca4464b6)
  [§](https://postgr.es/c/ab61f0087)
  [§](https://postgr.es/c/69ee81932)
  [§](https://postgr.es/c/cff2ef984)

  例如，關於備份清單中時間軸編號不符的錯誤回報，
  顯示的是起始時間軸編號，但原意是要
  顯示結束時間軸編號。
* 修正使用 LLVM 17 或更新版本進行 JIT 編譯時，
  無法執行函式內嵌的問題 (Anthonin Bonnefoy)
  [§](https://postgr.es/c/f1c6b153c)
* 調整我們的 JIT 程式碼以支援 LLVM 21 (Holger Hoffstätte)
  [§](https://postgr.es/c/912cfa314)

  先前的程式碼在 aarch64 機器上無法編譯。
* 修正 aarch64 專用程式碼，使其能以舊版（RHEL7 時代）的系統
  標頭檔建置 (Tom Lane)
  [§](https://postgr.es/c/db4eba152)
  [§](https://postgr.es/c/6a5170755)
* 修正 `io_uring_queue_init_mem()` 的
  configure 探測錯誤 (Masahiko Sawada)
  [§](https://postgr.es/c/640772c6d)

  此錯誤使以 autotools 建置時，無法最佳化非同步 I/O 緩衝區
  配置，不過以 meson 建置時程式碼確實能
  運作。此疏漏的主要影響是
  後端程序結束得比必要的更慢。
* 新增伺服器參數 [file_extend_method](../../server-administration/runtime-config/runtime-config-resource.md#GUC-FILE-EXTEND-METHOD)，以
  控制是否使用 `posix_fallocate()` (Thomas Munro)
  [§](https://postgr.es/c/33e3de6d7)

  PostgreSQL 版本 16 及之後的版本，若平台提供
  `posix_fallocate()`，就會使用它來
  擴展關聯檔案。然而，據回報這與某些檔案系統的
  互動不佳：使用 `posix_fallocate()` 會使 BTRFS 壓縮
  失效，而在較舊的 Linux 核心版本上，
  XFS 可能產生不實的 `ENOSPC` 錯誤。為了提供變通方式，
  引入此新的伺服器參數。將 `file_extend_method`
  設為 `write_zeros`，會使伺服器回到
  以寫入全零區塊來擴展檔案的舊方法。
* 在 Windows 上遵循 `open()` 的 `O_CLOEXEC`
  旗標 (Bryan Green, Thomas Munro)
  [§](https://postgr.es/c/bebb281b0)
  [§](https://postgr.es/c/a7d06e74d)
  [§](https://postgr.es/c/4da5c33a3)

  讓此旗標的運作方式與在 POSIX 平台上相同，使我們
  不會將檔案控制代碼洩漏給子程序，例如 `COPY
  TO/FROM PROGRAM`。雖然這種洩漏至今並未造成太多
  問題，但似乎並不理想。
* 修正以 meson 建置的 Solaris 執行檔無法剖析伺服器命令列上
  長選項的問題 (Tom Lane)
  [§](https://postgr.es/c/5eac1d68f)
* 支援在 GNU/Hurd 上變更程序標題 (Michael Banck)
  [§](https://postgr.es/c/bcfca332f)
* 修正 psql 對 `VACUUM` 選項值的
  Tab 鍵自動補全 (Yugo Nagata)
  [§](https://postgr.es/c/4e1376900)
* 在 psql 命令提示字元中，
  沒有伺服器連線時不顯示 `%P`（管線狀態）的值
  (Chao Li)
  [§](https://postgr.es/c/d42735b1e)

  這使 `%P` 的行為與其他值取決於作用中連線的
  提示字元跳脫序列一致。
* 修正 pg_dump 收集
  序列值的邏輯 (Nathan Bossart)
  [§](https://postgr.es/c/39d555576)
  [§](https://postgr.es/c/56e1f5010)

  若某個序列在傾印期間被並行刪除，即使該序列不在要傾印的
  資料庫物件之列，pg_dump 仍會失敗。此外，若呼叫的使用者沒有
  讀取序列值的
  權限，pg_dump 會輸出不正確的值，
  而不是如預期般失敗。
* 修正 pg_dump 對
  `oauth_validator_libraries` 值
  可能加錯引號的問題 (ChangAo Chen)
  [§](https://postgr.es/c/61c78e1f4)

  pg_dump 在需要傾印此設定的值時，
  套用了錯誤的引號規則。
* 避免 pg_dump 在
  二進位升級模式下的斷言失敗 (Vignesh C)
  [§](https://postgr.es/c/573e679a2)

  物件排序程式碼未處理訂閱與關聯（subscription-relation）物件，因而觸發斷言，
  不過在正式版建置中並未造成嚴重的
  不良影響。
* 修正 pgbench 在管線模式中
  遇到多個 `\syncpipeline` 命令時
  不正確的錯誤處理 (Yugo Nagata)
  [§](https://postgr.es/c/00e64e35c)

  若在查詢錯誤之後遇到多個 `\syncpipeline` 命令，
  pgbench
  會回報「failed to exit pipeline mode」，或在
  啟用斷言的建置中發生斷言失敗。
* 讓 pg_resetwal 在變更 OldestXID 時
  印出更新後的值 (Heikki Linnakangas)
  [§](https://postgr.es/c/19594271c)

  它對於其他每個可變更的變數都早已這麼做。
* 讓 pg_resetwal 允許將下一個
  multixact xid 設為 0，或將下一個 multixact 偏移量設為 UINT32_MAX (Maxim
  Orlov)
  [§](https://postgr.es/c/8747b969f)

  這些都是有效的值，因此拒絕它們是不正確的。在
  最壞的情況下，若恰好在 multixact 回捲的時間點
  嘗試執行 pg_upgrade，升級將會失敗。
* 在 `contrib/amcheck` 中，為 btree 索引的父層檢查
  使用正確的快照 (Mihail Nikalayeu)
  [§](https://postgr.es/c/df93f94dd)
  [§](https://postgr.es/c/3c83a2a0a)

  先前的程式碼在檢查以
  `CREATE INDEX CONCURRENTLY` 建立的索引時，會產生不實的錯誤。
* 修正 `contrib/amcheck`，使其
  正確處理「half-dead」的 btree 索引頁面
  (Heikki Linnakangas)
  [§](https://postgr.es/c/19e786727)

  `amcheck` 預期這類頁面具有父層
  下行連結，但實際上並沒有，因而產生
  「mismatch between parent key and child high key」的錯誤誤報。
* 修正 `contrib/amcheck`，使其
  正確處理未完成的 btree 根頁面分裂
  (Heikki Linnakangas)
  [§](https://postgr.es/c/50c63ebb0)

  `amcheck` 可能誤報
  「block is not true root」錯誤。
* 修正 `contrib/pg_buffercache` 中過多的
  記憶體配置 (David Geier)
  [§](https://postgr.es/c/580b5c2f3)

  程式碼為 NUMA
  頁面狀態配置了所需記憶體的兩倍。
* 修正 `contrib/intarray` 的
  `@@` 選擇率估算器中的邊界情況整數溢位
  (Chao Li)
  [§](https://postgr.es/c/07c1c6ec5)

  這可能使涉及最大整數值的情況
  產生不佳的選擇率估計值。
* 修正 `contrib/ltree` 中的多位元組編碼問題
  (Jeff Davis)
  [§](https://postgr.es/c/f79e239e0)

  先前的程式碼可能將不完整的多位元組字元
  傳給 `lower()`，很可能導致不正確的
  行為。
* 避免 `contrib/pg_stat_statements` 在
  `IN` 清單同時包含常數與
  非常數運算式時當機 (Sami Imseih)
  [§](https://postgr.es/c/3304e97b1)
* 將時區資料檔更新為 tzdata
  2025c 版 (Tom Lane)
  [§](https://postgr.es/c/6574bee64)

  唯一的變更是下加利福尼亞（Baja California）1976 年之前時間戳記的
  歷史資料。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-2.html)（原文版本：18.6；核對日期：2026-10-22）
