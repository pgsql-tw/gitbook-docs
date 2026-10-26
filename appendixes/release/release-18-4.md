<a id="RELEASE-18-4"></a>
## E.2. 18.4 版 [#](#release-18-4) <a href="#release-18-4" id="release-18-4"></a>

[E.2.1. 遷移至 18.4 版](release-18-4.md#release-18-4-migration)

[E.2.2. 變更內容](release-18-4.md#release-18-4-changes)

**發佈日期：**2026-05-14

此版本包含自 18.3 以來的多項修正。
關於主要版本 18 的新功能，請參閱
[第 E.6 節](release-18.md)。

<a id="RELEASE-18-4-MIGRATION"></a>

### E.2.1. 遷移至 18.4 版 [#](#release-18-4-migration) <a href="#release-18-4-migration" id="release-18-4-migration"></a>

執行 18.X 版者不需要進行傾印／還原。

不過，若你是從早於 18.2 的版本升級，
請參閱[第 E.4 節](release-18-2.md)。

<a id="RELEASE-18-4-CHANGES"></a>

### E.2.2. 變更內容 [#](#release-18-4-changes) <a href="#release-18-4-changes" id="release-18-4-changes"></a>

* 防止處理啟動封包時發生無限制的遞迴
  (Michael Paquier)
  [§](https://postgr.es/c/f7a191f53)

  惡意用戶端可以藉由無限次交替送出會被拒絕的 SSL 與 GSS 加密請求，
  使所連線的後端程序當機。

  PostgreSQL 專案感謝 Calif.io
  （與 Claude 及 Anthropic Research 合作）回報
  此問題。
  (CVE-2026-6479)
* 修正記憶體配置計算中的多項整數溢位
  (Tom Lane, Nathan Bossart, Heikki Linnakangas)
  [§](https://postgr.es/c/e1c30458a)
  [§](https://postgr.es/c/01e568b8c)
  [§](https://postgr.es/c/f3cee4dc4)
  [§](https://postgr.es/c/dd8af778d)
  [§](https://postgr.es/c/55328e3a9)
  [§](https://postgr.es/c/67dd6243d)
  [§](https://postgr.es/c/8d1489d50)
  [§](https://postgr.es/c/c7fb9f765)
  [§](https://postgr.es/c/3fbec9e50)

  有多處在計算要配置多少記憶體時，未充分考慮整數
  溢位的可能性。溢位會導致配置過小的緩衝區，而呼叫端
  接著會寫入超出其結尾的位置。這至少會觸發伺服器
  當機，而且很可能被利用來執行任意程式碼。
  在許多（但絕非全部）情況下，此風險只存在於
  32 位元建置中。

  PostgreSQL 專案感謝 Xint Code、
  Bruce Dang、Sven Klemm 與 Pavel Kohout 回報這些問題。
  (CVE-2026-6473)
* 在 pg_createsubscriber 中
  正確地為訂閱名稱加上引號 (Nathan Bossart)
  [§](https://postgr.es/c/c2e44c370)

  所給定的訂閱名稱未加引號就被插入 SQL 命令中，
  因此在訂閱名稱來自不受信任來源的（或許不太可能發生的）
  情況下，可能遭到 SQL 注入攻擊。

  PostgreSQL 專案感謝
  Yu Kunpeng 回報此問題。
  (CVE-2026-6476)
* 在邏輯複寫來源檢查中，正確地為物件名稱加上引號
  (Pavel Kohout)
  [§](https://postgr.es/c/cb35d7306)

  `ALTER SUBSCRIPTION ... REFRESH PUBLICATION`
  將綱要與關聯名稱未加引號就插入 SQL 命令中，
  使得在發佈者上執行任意 SQL 成為可能。

  PostgreSQL 專案感謝
  Pavel Kohout 回報此問題。
  (CVE-2026-6638)
* 拒絕 `ts_headline()` 中過長的選項
  (Michael Paquier)
  [§](https://postgr.es/c/62ad26266)

  `StartSel`、`StopSel`
  與 `FragmentDelimiter` 字串的長度不得超過
  32Kb，但先前並未檢查這一點。過長的值
  通常會使伺服器當機。

  PostgreSQL 專案感謝
  Xint Code 回報此問題。
  (CVE-2026-6473)
* 還原屬性 MCV 統計資訊時偵測有誤的輸入
  (Michael Paquier)
  [§](https://postgr.es/c/661095c40)

  統計資訊還原函式在驗證最常見值（most-common-value）統計資訊時
  不夠謹慎，會接受
  之後可能使規劃器當機的值。

  PostgreSQL 專案感謝
  Jeroen Gui 回報此問題。
  (CVE-2026-6575)
* 在 `timeofday()`
  與 `pg_strftime()` 中防範惡意的時區名稱 (Tom Lane)
  [§](https://postgr.es/c/ba27389c2)
  [§](https://postgr.es/c/c6e7a9ef3)

  特製的時區設定可能將 `%`
  序列傳給 `snprintf()`，可能造成
  當機或洩漏伺服器記憶體內容。另一條導致類似
  結果的途徑，是使 `pg_strftime()` 所用的
  有限大小輸出緩衝區溢位。

  PostgreSQL 專案感謝
  Xint Code 回報此問題。
  (CVE-2026-6474)
* 建立多重範圍（multirange）型別時，確保使用者
  在為該多重範圍型別指定的綱要上具有 `CREATE` 權限
  (Jelte Fennema-Nio)
  [§](https://postgr.es/c/a44780f41)

  多重範圍型別可以放在與其
  上層範圍型別不同的綱要中，但這樣做時我們忽略了套用必要的權限
  檢查。

  PostgreSQL 專案感謝
  Jelte Fennema-Nio 回報此問題。
  (CVE-2026-6472)
* 在認證程式碼中使用時間安全（timing-safe）的字串比較
  (Michael Paquier)
  [§](https://postgr.es/c/d93ef4131)

  檢查密碼、雜湊值等時，改用 `timingsafe_bcmp()`，
  取代 `memcmp()` 或 `strcmp()`。
  目前不清楚在這些地方，這些函式的資料相依性
  是否可以被有效利用，但為了安全起見，仍將其替換。

  PostgreSQL 專案感謝
  Joe Conway 回報此問題。
  (CVE-2026-6478)
* 將 `PQfn()` 標記為不安全，並避免在
  libpq 內部使用它 (Nathan Bossart)
  [§](https://postgr.es/c/be0136440)

  對於非整數的結果型別，`PQfn()` 不會
  被傳入輸出緩衝區的大小，因此無法檢查
  伺服器傳回的資料是否放得下。惡意伺服器因此
  可能覆寫用戶端記憶體。不變更 API 就無法修正此問題，
  因此將該函式標記為已棄用。在
  libpq 內部，則改用一個可以
  套用缺少之檢查的變體版本。

  PostgreSQL 專案感謝
  Yu Kunpeng 與 Martin Heistermann 回報此問題。
  (CVE-2026-6477)
* 防止 pg_basebackup
  與 pg_rewind 中的路徑穿越 (Michael Paquier)
  [§](https://postgr.es/c/6a67c540a)

  這些應用程式未驗證從其輸入讀取的輸出檔案路徑，
  因此惡意來源可以覆寫這些應用程式
  可寫入的任何檔案。現在藉由拒絕絕對路徑或含有上層目錄
  參照的路徑，限制資料可以寫入的位置。

  PostgreSQL 專案感謝 Tencent Xuanwu Lab 的
  XlabAI Team 與 Valery Gubanov 回報此問題。
  (CVE-2026-6475)
* 防範 `contrib/intarray` 的 `query_int`
  型別與 `contrib/ltree` 的 `ltxtquery`
  型別中的欄位溢位 (Tom Lane)
  [§](https://postgr.es/c/c5790ec4f)
  [§](https://postgr.es/c/05e73b5c3)

  剖析這些查詢結構時並未檢查 16 位元欄位
  是否溢位，因此可能建構出無效的查詢樹。
  執行該查詢時可能使伺服器當機。

  PostgreSQL 專案感謝
  Xint Code 回報此問題。
  (CVE-2026-6473)
* 防範 `contrib/ltree` 的 `lquery` 型別
  出現過長的值
  (Michael Paquier)
  [§](https://postgr.es/c/7f019f341)

  超過 64K 個項目的值會造成內部溢位，
  可能導致堆疊破壞或錯誤的結果。

  PostgreSQL 專案感謝
  Vergissmeinnicht、A1ex 與 Jihe Wang
  回報此問題。
  (CVE-2026-6473)
* 防止 `contrib/spi` 中的 SQL 注入與緩衝區溢位
  (Nathan Bossart)
  [§](https://postgr.es/c/1ebda7da9)

  `check_foreign_key()` 在為鍵值加上引號時
  不夠謹慎，而且使用固定長度的緩衝區來
  建構查詢。雖然此模組只是作為範例
  程式碼，但仍不應該包含如此危險的錯誤。

  PostgreSQL 專案感謝
  Nikolay Samokhvalov 回報此問題。
  (CVE-2026-6637)
* 在假設可定序型別上的相等條件蘊含唯一性之前，
  先檢查是否為非確定性定序
  (Richard Guo)
  [§](https://postgr.es/c/e8fd5e579)
  [§](https://postgr.es/c/1132af22c)
  [§](https://postgr.es/c/5c214b58b)
  [§](https://postgr.es/c/b62f514ac)
  [§](https://postgr.es/c/bed3ffbf9)

  許多規劃器最佳化都假設，例如，若 `x` 上有
  唯一值索引，則至多只有一個資料表資料列能滿足 `WHERE x = 'abc'`。然而，若索引與 `WHERE`
  子句附有不同的定序，此結論一般而言並不
  安全。當兩個定序都是確定性定序時是安全的，因為該性質本質上
  要求兩個字串相等即表示逐位元相等。但
  非確定性定序並非如此，因此只要
  `WHERE` 子句或索引其中之一使用
  非確定性定序，基於唯一相符的假設進行最佳化就可能產生錯誤的查詢結果。
* 修正在連接移除期間，未完整移除
  `RestrictInfo` 結構中關聯參照的問題
  (Tom Lane)
  [§](https://postgr.es/c/16fb94605)

  已證實此疏忽會導致規劃器失敗，例如
  非預期的「FULL JOIN is only supported with merge-joinable or
  hash-joinable join conditions」錯誤。它也可能
  在其他情況下導致未能考慮有效的計畫。
* 改進規劃器將分割鍵欄位比對到子查詢
  輸出的處理 (Richard Guo)
  [§](https://postgr.es/c/8e8b2bef7)

  在將運算元與分割鍵比較之前，先剝除運算元中無作用的 PlaceHolderVar。
  此變更使分割區修剪在
  某些先前未能辨識出某個分割區
  不需要被掃描的情況下得以成功。
* 修正自我連接移除，使其能處理本身就是布林
  欄位的連接子句，例如 `ON t1.boolcol` (Andrei Lepikhov,
  Tender Wang, Alexander Korotkov)
  [§](https://postgr.es/c/e8b9d6497)

  先前這種情況會導致「no relation entry
  for relid *`N`*」錯誤。
* 修正 `UPDATE/DELETE ... WHERE CURRENT OF`，使其可用於
  具有虛擬產生欄位的資料表 (Satyanarayana Narlapuram,
  Dean Rasheed)
  [§](https://postgr.es/c/f3d03fbd5)
* 修正 `INSERT
  ... ON CONFLICT` 中 `EXCLUDED` 欄位參照裡
  虛擬產生欄位的展開 (Satyanarayana Narlapuram, Dean Rasheed)
  [§](https://postgr.es/c/cf38dedf6)
* 修正規則動作與規則條件中對 `NEW` 產生欄位的
  錯誤處理 (Richard Guo, Dean Rasheed)
  [§](https://postgr.es/c/e528bfe97)

  先前，這類欄位參照在 `INSERT` 的情況下會產生 NULL，
  在 `UPDATE` 的情況下則等同於
  `OLD` 的值。
* 修正不實的「indexes on virtual generated columns are not
  supported」錯誤 (Robert Haas)
  [§](https://postgr.es/c/cceb9c18a)

  建立運算式索引時，有時會錯誤地回報
  此錯誤。
* 修正不實的「generated columns are not supported in COPY FROM
  WHERE conditions」錯誤 (Tom Lane)
  [§](https://postgr.es/c/11c2c0cc8)

  在 `COPY FROM WHERE`
  條件中使用系統欄位時，有時會錯誤地回報此錯誤。
* 當 `MERGE` 在可重複讀取或可序列化模式下
  遇到被並行更新的元組時，正確地回報序列化失敗
  (Tender Wang)
  [§](https://postgr.es/c/13fab378e)

  先前，這類情況的行為與較低隔離
  層級時相同。
* 修正來源資料表有已刪除欄位時的
  `CREATE TABLE ... LIKE ... INCLUDING
  STATISTICS` (Julien Tachoires)
  [§](https://postgr.es/c/149c875fc)

  在這類情況下，擴充統計資訊物件可能被錯誤地複製，
  或命令可能給出不正確的錯誤。
* 允許 `ALTER INDEX ... ATTACH PARTITION` 在適當時
  將上層索引標記為有效 (Sami Imseih)
  [§](https://postgr.es/c/5713ac248)

  在某些邊界情況下，即使分割索引的所有葉節點索引都有效，
  它仍可能維持被標記為無效。此
  變更提供一種機制，讓使用者無須
  手動更新系統目錄就能修正這種情況。
* 修正 `ALTER TABLE ... SET NOT NULL`，使其只在完成系統目錄
  變更之後才呼叫物件存取掛鉤函式
  (Artur Zakirov)
  [§](https://postgr.es/c/6958077ce)
* 修正 `ALTER FOREIGN DATA WRAPPER`，使其不會刪除
  包裝器物件對其處理函式的相依關係 (Jeff Davis)
  [§](https://postgr.es/c/c11f87b1a)
* 修正外鍵觸發程序遺失可延遲性的問題 (Yasuo Honda)
  [§](https://postgr.es/c/5db5e3396)

  先前，定義為 `DEFERRABLE INITIALLY
  DEFERRED` 的外鍵，在被設為 `NOT ENFORCED` 狀態、
  然後再設回 `ENFORCED` 之後，
  其行為會如同 `NOT DEFERRABLE`。

  若你有外鍵遇到此問題，可以（在安裝此更新之後）
  再次將其設為 `NOT
  ENFORCED`，然後再設回 `ENFORCED` 來修復。
* 修正 `WITHOUT OVERLAPS`，使其允許網域 (Jian He)
  [§](https://postgr.es/c/49f3cb453)

  `UNIQUE/PRIMARY KEY ... WITHOUT OVERLAPS` 要求
  不重疊欄位必須是範圍或多重範圍，但它也應該
  允許建立在這類型別之上的網域。
* 禁止透過多重範圍使複合型別成為其自身的成員
  (Heikki Linnakangas)
  [§](https://postgr.es/c/ff8f27d6e)

  當中間型別是網域、陣列、複合型別或範圍時，
  我們早已禁止這類情況；但先前遺漏了多重範圍。
* 修正 datum 映像比較，使其不受符號擴展
  差異的影響 (David Rowley)
  [§](https://postgr.es/c/49315de0c)

  這修正了一些先前會導致「could not
  find memoization table entry」錯誤或錯誤查詢結果的情況。
* 修正搭配非嚴格（non-strict）相等運算子時，雜湊 `IN`／`NOT
  IN` 的錯誤邏輯 (Chengpeng Yan)
  [§](https://postgr.es/c/035c520db)

  先前的程式碼可能當機或給出錯誤的結果。所有內建
  資料型別都具有嚴格的相等運算子，因此此問題
  只可能發生在擴充功能的資料型別上。
* 截斷 `to_char()` 中過長的語系特定數字符號
  (Tom Lane)
  [§](https://postgr.es/c/580e7be88)

  若某個語系指定的貨幣符號、千分位分隔符號、
  小數點符號或正負號符號超過 8 個位元組，就可能發生緩衝區溢位。
  現實中並不存在這樣的語系，而且
  無特權的攻擊者在實務上也難以在 Postgres 伺服器底下安裝惡意的
  語系定義；但為了安全起見，
  仍檢查是否有過長的符號，並在必要時加以截斷。
* 剖析 `Ispell` 字典的 affix 檔時，
  防止緩衝區溢位 (Tom Lane)
  [§](https://postgr.es/c/00c6e0819)
  [§](https://postgr.es/c/c2bfeb3bb)

  損毀或惡意的 affix 檔可能使伺服器當機。
  由於文字搜尋設定檔被假定為可信任的，這不被視為安全性問題，
  但仍值得修正。
* 防範計算視窗彙總函式的框架起始與結束位置時
  發生整數溢位 (Richard Guo)
  [§](https://postgr.es/c/bfc7dff26)

  使用者指定的非常大的偏移量（接近 INT64_MAX）可能導致
  錯誤或不正確的查詢結果。
* 修正 `array_agg_array_combine()`，使其正確合併
  各陣列的 null 位元映像 (Dmytro Astapov)
  [§](https://postgr.es/c/14bf2c39e)

  此錯誤使平行化的 `array_agg(anyarray)` 計算
  有時產生不正確的輸出。
* 當 `sync_file_range()` 傳回錯誤
  代碼 `EINTR` 時重試 (DaeMyung Kang)
  [§](https://postgr.es/c/6cb307251)
* 修正 `pg_stat_reset_single_table_counters()` 用於
  共享系統目錄時的錯誤行為 (Chao Li)
  [§](https://postgr.es/c/b081c5b07)

  這類情況會產生重設
  目前資料庫之 `stat_reset_timestamp` 的副作用，
  而這並非預期的行為。
* 在平行套用工作程序閒置時更新活動統計資訊
  (Zhijie Hou)
  [§](https://postgr.es/c/44c8dc280)

  先前，最近完成之交易的統計資訊可能
  長時間未被回報，在工作負載較輕時尤其如此。
* 修正在估算集合運算中的陣列長度時發生的
  「no relation entry for relid 0」失敗 (Tender Wang)
  [§](https://postgr.es/c/13e20d1c9)
* 修正 `pglz_decompress()` 收到損毀輸入時的
  緩衝區過度讀取 (Andrew Dunstan)
  [§](https://postgr.es/c/c3e436b1c)

  它可能讀取超出輸入結尾的數個位元組，
  在非常不幸的情況下可能導致當機。
* 修正增量 JSON 剖析器對跨越輸入緩衝區邊界之數字詞元的處理
  (Andrew Dunstan)
  [§](https://postgr.es/c/3e4955630)

  先前可能接受格式不正確的數字，導致
  之後發生失敗。
* 防止還原增量備份期間關聯的可見性對應表膨脹
  (Robert Haas)
  [§](https://postgr.es/c/9540c0e5d)

  由於預期檔案長度的計算錯誤，還原可能會在可見性對應表後面
  附加許多全零區塊。這不會
  造成資料損毀，但可能浪費大量
  磁碟空間。
* 在文字欄位的系統目錄快取查找中，使用 C 定序，而非資料庫的預設定序
  (Jeff Davis)
  [§](https://postgr.es/c/03c4f243e)

  這可避免在實體複寫啟動等邊界情況下發生失敗；
  在這類情況下沒有已識別的資料庫，因此無法決定預設
  定序。
* 防止卡住的插槽同步（slotsync）工作程序阻擋待命伺服器的
  提升 (Nisha Moond, Ajin Cherian)
  [§](https://postgr.es/c/58c1188a3)
  [§](https://postgr.es/c/acf49bfed)
  [§](https://postgr.es/c/94efd308b)

  徒勞等待主伺服器回應的工作程序，
  會將提升延遲過長的時間。
* 修正閒置的插槽同步工作程序產生過多日誌輸出的問題
  (Zhijie Hou)
  [§](https://postgr.es/c/540fe8fb5)
* 確保 tuplestore 資料結構即使在發生錯誤之後，內部仍保持一致
  (Tom Lane)
  [§](https://postgr.es/c/adb7873bb)

  先前的程式碼對此並不謹慎；這在大多數
  時候沒有問題，但對於支撐
  `WITH HOLD` 游標的 tuplestore 則會出問題。在 v15 及之前的版本中，這
  會導致容易重現的當機；之後的分支目前未知
  有此弱點，但最好在所有分支中都維持一致性。
* 讓 `pg_aios` 系統
  檢視表的 `pid` 欄位，在項目沒有所屬程序時
  顯示 NULL 而非 0 (ChangAo Chen)
  [§](https://postgr.es/c/882bdcf9f)
* 修正 `pg_stat_replication` 中過早回報 NULL 延遲的問題
  (Shinya Kato)
  [§](https://postgr.es/c/98e96e579)

  即使正在進行複寫活動，延遲欄位也經常讀到 NULL。
* 修正平行 btree 索引掃描所用共享記憶體配置不足的問題
  (Siddharth Kothari)
  [§](https://postgr.es/c/1e71970d2)

  在邊界情況下，這可能導致伺服器當機。
* 避免使用不寫入 WAL 的 GiST 索引時罕見的刷寫失敗
  (Tomas Vondra)
  [§](https://postgr.es/c/5b3f63a1b)

  不寫入日誌的 GiST 索引，有時仍可能
  產生「xlog flush request *`n/nnnn`*
  is not satisfied」錯誤，原因是在選擇代表插入點的
  「fake LSN」時有誤。
* 修正對非規則大小區段之 DSA 頁面對應表所需大小的低估
  (Paul Bunn)
  [§](https://postgr.es/c/a0f38604d)

  此計算錯誤會導致越界存取，進而造成伺服器
  當機。
* 修正共享記憶體中最舊 multixact 陣列的索引計算
  (Yura Sokolov)
  [§](https://postgr.es/c/0a50ef094)
  [§](https://postgr.es/c/fa3b328e6)

  此錯誤可能使已準備但尚未提交之
  交易的資料列鎖定對其他工作階段不可見，或使
  此類交易的結果出現其他可見性問題。
  在 max_connections 設定非常小時，還可能發生記憶體踩踏。
* 修正安裝過多 `EXPLAIN` 擴充
  選項時的陣列溢位 (Joel Jacobson)
  [§](https://postgr.es/c/730c98d03)
* 修正處理擴充功能資料型別之運算式上的擴充統計資訊時，
  伺服器可能當機的問題 (Michael Paquier)
  [§](https://postgr.es/c/83671c0da)

  若資料型別的 typanalyze 函式未計算出任何有用的統計資訊，
  可能發生 NULL 指標解參照。
  核心內建的 typanalyze 函式都不會這樣，但擴充功能
  有可能。
* 正確顯示用於 `GROUP
  BY` 的連接別名 Var (Tom Lane)
  [§](https://postgr.es/c/c2c1962a6)

  在包含類似 `SELECT ... t1 LEFT JOIN t2
  USING (x) GROUP BY x` 查詢的檢視表中，`GROUP BY`
  子句在反剖析時可能被錯誤地顯示，導致
  傾印／還原失敗。只有在
  `t1.x` 與 `t2.x` 的資料型別
  不完全相同，且 `t1.x` 是
  需要隱含強制轉型的那一側時，才會發生失敗。
* 修正以 ICU 為基礎的字串處理中的輕微記憶體洩漏 (Jeff Davis)
  [§](https://postgr.es/c/4abf63c62)
* 若啟動程序失敗，在結束 postmaster 之前，
  正確地關閉其他子程序 (Ayush Tiwari)
  [§](https://postgr.es/c/affdb2dd5)

  對此情況的處理，仰賴一個早已過時的假設：
  啟動程序執行期間不存在其他 postmaster 子程序，
  因此 postmaster 立即結束是可以接受的。
  孤立的子程序最終會察覺 postmaster 已終止並
  自行結束，但較乾淨的關閉程序是比較理想的做法。
* 修正檢查點的 WAL 重播與 multixact
  ID 建立之間的競爭條件 (Heikki Linnakangas)
  [§](https://postgr.es/c/0852643e1)

  追隨較舊次要版本主伺服器之 WAL 的待命伺服器，
  可能陷入「當機後重新啟動」的循環，並抱怨
  「could not access status of transaction」。
* 防止 walsender 程序在關閉時無限期等待
  (Anthonin Bonnefoy)
  [§](https://postgr.es/c/3eb2fecdb)
  [§](https://postgr.es/c/980498138)

  在關閉正在發佈邏輯複寫資料的叢集時，
  walsender 會等待所有待處理的 WAL 寫出。
  但它並未正確地要求進行寫出，因此在某些
  情況下可能變成無限期等待。
* 確保復原期間對資料表可用空間對應表的變更會被持久保存
  (Alexey Makhmutov)
  [§](https://postgr.es/c/ac3b97db3)

  先前，雖然 WAL 重播在重播應該改變可用空間對應表的操作時
  確實會更新它，但若啟用了檢查碼，對應表頁面的緩衝區
  不會被標記為髒（dirty），因此這些變更
  可能永遠不會被寫出。在待命伺服器上，隨著時間經過，這
  會使對應表與資料表的實際
  內容大相逕庭。雖然對應表只被用作提示，但這種狀況
  可能在待命伺服器被提升為作用中伺服器之後的一段時間內，
  造成顯著的效能下降，直到
  對應表大部分已被更新修復為止。
* 修正某些 ecpg 函式在
  未建立任何連線的情況下被呼叫時的當機 (Shruthi Gowda)
  [§](https://postgr.es/c/e2688ea5e)
* 強化 tar 檔剖析邏輯，以因應無法處理的封存檔
  (Tom Lane)
  [§](https://postgr.es/c/698eae7db)

  pg_basebackup
  與 pg_verifybackup 所使用的 tar 檔讀取程式碼，
  完全沒有驗證輸入是否為 tar 檔，
  更不用說是否屬於我們能處理的有效 tar 檔子集。在輸入檔案
  是由 PostgreSQL 程式碼產生的一般情境下，
  這不是問題，但若輸入是由其他 tar 程式產生的，
  就可能成為
  問題。
* 修正備份解壓縮與 tar 剖析程式碼中的多項錯誤
  (Andrew Dunstan, Tom Lane, Chao Li)
  [§](https://postgr.es/c/5095f3f4a)
  [§](https://postgr.es/c/a01a592b1)
  [§](https://postgr.es/c/78dc9a808)

  pg_basebackup
  與 pg_verifybackup 所使用的解壓縮與 tar 檔讀取程式碼，
  會錯誤處理 tar 檔的填補資料、在邊界情況下可能損毀 LZ4 壓縮資料、
  未檢查某些不尋常的錯誤狀況、在壓縮／解壓縮錯誤後
  未能結束（導致連鎖的錯誤回報），
  而且有記憶體洩漏。
* 在 pg_dump 中，保留 `NOT NULL`
  限制條件的 `NO
  INHERIT` 屬性 (Jian He)
  [§](https://postgr.es/c/c3c8b63d7)

  某些情況下遺漏了輸出 `NO INHERIT` 子句。
* 在 pg_dumpall 中，不要略過
  具有懸空授與者 OID 的角色 `GRANT`
  (Tom Lane)
  [§](https://postgr.es/c/b09158cc7)

  改為以輸出不帶任何 `GRANTED BY` 子句的 `GRANT`
  來處理這類情況，就像 v16 之前的做法一樣。
  這可以在可預見的情況下避免遺失授權，因為
  v16 之前的伺服器不會阻止刪除授與者角色。仍會繼續
  針對缺少的授與者發出警告，但只在來源
  伺服器為 v16 或更新版本時才這麼做。
* 在 pg_upgrade 中，連線到較舊的來源伺服器時，
  注意使用正確的協定版本
  (Jacob Champion)
  [§](https://postgr.es/c/1b2773179)

  嘗試從 2018 年之前的伺服器升級時，
  這可能造成問題。
* 在 `contrib/basic_archive` 中，允許封存
  目錄在啟動時不存在 (Nathan Bossart)
  [§](https://postgr.es/c/bde9ad315)

  先前，若
  `basic_archive.archive_directory` 的設定
  未指向既有的目錄，就會被拒絕。這並不理想，
  因為即使該目錄之後出現，封存仍會無限期卡住。
* 修正 `contrib/ltree`，使其能因應大小寫摺疊
  改變字串位元組長度的情況 (Jeff Davis)
  [§](https://postgr.es/c/b3c2a3d38)
  [§](https://postgr.es/c/53a57cae1)

  先前，指定不分大小寫比對的 `lquery` 模式，
  可能無法比對到應該相符的標籤。
* 修正
  `contrib/pg_overexplain` 的
  `RANGE_TABLE` 選項輸出結構錯誤的問題 (Satyanarayana Narlapuram)
  [§](https://postgr.es/c/6723d462d)

  在 JSON、YAML 與 XML 格式中，有些欄位放錯了位置，
  導致輸出的結構無效。
* 在 `contrib/pg_stat_statements` 中，剖析
  `pgss_query_texts.stat` 檔案時若發生錯誤，
  不要洩漏記憶體 (Heikki Linnakangas)
  [§](https://postgr.es/c/25b02320e)
* 在 `contrib/postgres_fdw` 中，避免因過早清理
  失敗的連線而當機 (Etsuro Fujita)
  [§](https://postgr.es/c/c318777da)

  若遠端連線在中止清理時失敗，我們就無法再
  使用它。但要將關閉連線物件延後到交易結束時，
  因為在開啟中的游標等資料結構內
  可能仍有對它的參照。
* 將時區資料檔更新為 tzdata
  2026b 版 (Tom Lane)
  [§](https://postgr.es/c/8a431b6d6)

  英屬哥倫比亞（America/Vancouver）自 2026 年 11 月起將全年採用 UTC-07
  （實質上即永久日光節約時間）。此
  版本假設其時區縮寫自該時起將
  為 `MST`。這很可能
  會改變，但目前還不清楚將使用什麼新的縮寫。
  另外也對摩爾多瓦做了歷史修正：自 2022 年起，他們一直遵循歐盟的日光節約時間
  轉換時間。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-4.html)（原文版本：18.6；核對日期：2026-10-22）
