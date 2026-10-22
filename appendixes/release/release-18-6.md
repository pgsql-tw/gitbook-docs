<a id="RELEASE-18-6"></a>
## E.1. 18.6 版 [#](#RELEASE-18-6)

[E.1.1. 遷移至 18.6 版](release-18-6.md#RELEASE-18-6-MIGRATION)

[E.1.2. 變更內容](release-18-6.md#RELEASE-18-6-CHANGES)

**發佈日期：**2026-08-13

此版本包含自 18.4 以來的多項修正。
關於主要版本 18 的新功能，請參閱
[第 E.6 節](release-18.md)。

注意：由於在封裝（wrap）之後發現了一個迴歸問題，18.5 版
從未發佈。

<a id="RELEASE-18-6-MIGRATION"></a>

### E.1.1. 遷移至 18.6 版 [#](#RELEASE-18-6-MIGRATION)

執行 18.X 版者不需要進行傾印／還原。

不過，下方前三個安全性項目說明了更新後你可能需要
進行的設定調整與資料清理。

此外，若你有任何 GIN 索引，請參閱下方關於這類索引所屬資料表的
`reltuples` 值可能損毀的變更項目。

此外，若你使用 `contrib/btree_gist`
或 `contrib/ltree`，可能需要重建以這些擴充功能
建立的索引；請參閱下方的相關項目。

此外，若你是從早於 18.2 的版本升級，
請參閱[第 E.4 節](release-18-2.md)。

<a id="RELEASE-18-6-CHANGES"></a>

### E.1.2. 變更內容 [#](#RELEASE-18-6-CHANGES)

* 將邏輯解碼輸出外掛程式限制在新伺服器參數
  `output_plugin_libraries` 所指定的集合內
  (Jacob Champion)
  [§](https://postgr.es/c/2a29b607d)
  [§](https://postgr.es/c/82fd68801)

  先前，複寫使用者可以選擇任何可載入的程式庫進行
  邏輯解碼，因而可能遭到各種方式的利用。為了能夠
  鎖定此行為，同時不破壞先前可正常運作的設定，
  新增了允許的輸出外掛程式白名單。

  預設情況下，只有隨
  PostgreSQL 一起提供的輸出外掛程式
  （`pgoutput` 與 `test_decoding`）
  會包含在 `output_plugin_libraries` 中。
  依賴其他輸出外掛程式的安裝環境，必須在
  更新伺服器後將它們加入，例如

  ```

  output_plugin_libraries = 'pgoutput, test_decoding, my_trusted_decoder'
  ```

  另外，從 17 及更新版本遷移時，若新叢集的
  `output_plugin_libraries` 參數不允許
  舊叢集上邏輯複寫插槽所使用的外掛程式，
  `pg_upgrade --check` 將會失敗。
  請在執行 pg_upgrade 之前，
  先在新叢集的設定中加入必要的項目。

  PostgreSQL 專案感謝
  Vladimir Tokarev 與 Yu Kunpeng
  回報此問題。
  (CVE-2026-6471)
* 修正 `contrib/pgcrypto` 的 PGP 加密，使其能偵測
  不支援的加密演算法 (Daniel Gustafsson)
  [§](https://postgr.es/c/fe32b10fc)
  [§](https://postgr.es/c/4c5128ca0)

  先前，若 OpenSSL 拒絕所要求的加密演算法（例如
  因為它在 FIPS 模式下執行，或尚未載入 legacy provider），
  pgcrypto 並不會察覺到失敗，而是直接將未加密的區塊與
  明文進行 XOR 運算，使得這種「加密」可以被輕易
  破解。這通常會發生在已棄用或非 FIPS 的
  加密演算法上（cipher-algo=blowfish/bf、twofish、cast5 或
  3des）。

  現在 pgcrypto 預設將無法
  解密任何以這種方式受影響的訊息。為了能夠
  取回這類資料，已在
  `pgp_pub_decrypt()`
  與 `pgp_sym_decrypt()` 中新增選項
  `ignore-cipher-failure`。
  設定 `ignore-cipher-failure=1` 會恢復
  它們先前的行為，從而可以剝除有缺陷的加密包裝：

  ```

  pgp_sym_decrypt(encrypted_column, any key, 'ignore-cipher-failure=1')
  ```

  找出受影響的訊息並剝除其包裝之後，便可以使用
  現代的演算法重新加密。不過重要的是，OpenSSL 的行為
  必須與建立這些有缺陷訊息時相同：若不支援的演算法集合
  不同，這種做法將無法運作。請參閱
  `ignore-cipher-failure` 的說明文件。

  PostgreSQL 專案感謝
  Shishir Sharma
  回報此問題。
  (CVE-2026-14663)
* 修正 psql，使其略過以指令碼執行的
  `COPY ... FROM STDIN` 命令之後的行內資料，即使
  該 `COPY` 在送出
  `PGRES_COPY_IN` 之前就已失敗 (Tom Lane)
  [§](https://postgr.es/c/29921259e)
  [§](https://postgr.es/c/900894d35)

  先前，若 `COPY` 命令在啟動時就失敗
  （例如因為目標資料表不存在），
  psql 不會察覺，而是
  繼續將其後的行內資料當作 SQL 命令讀取。在
  最好的情況下這是錯誤的行為，最壞的情況下則有 SQL 注入
  風險。現在 psql 會辨識
  語法正確的 `COPY ... FROM STDIN` 命令，
  並在伺服器沒有回應
  `PGRES_COPY_IN` 時自行略過資料。

  雖然此修正不太可能影響任何正式環境的 SQL 指令碼，
  但測試指令碼可能會刻意執行失敗的 `COPY
  ... FROM STDIN` 命令。這些指令碼需要在每個這類
  命令之後加上一行 `\.` 資料結束標記。

  PostgreSQL 專案感謝
  Alexander Lakhin
  回報此問題。
  (CVE-2026-6464)
* 交叉檢查執行 `EXECUTE` 或 `FETCH` 之
  portal 的輸出資料列型別
  (Robert Haas)
  [§](https://postgr.es/c/37b8f3b0e)

  `EXECUTE` 與 `FETCH` 使用兩個
  portal：外層的 portal 用於陳述式本身，內層的 portal 則
  代為執行所要執行的查詢。先前
  有可能使這兩個 portal 宣告的資料列型別不一致，
  導致伺服器記憶體內容外洩與任意程式碼執行。

  PostgreSQL 專案感謝
  Ben Morris（與 Claude 及 Anthropic Research 合作）
  與 Peter Geoghegan
  回報此問題。
  (CVE-2026-16239)
* 修正 `to_char()` 中時區縮寫過長時的
  緩衝區溢位 (Tom Lane)
  [§](https://postgr.es/c/4fafe2380)

  這很容易使伺服器當機，且已有導致任意
  程式碼執行的攻擊手法被回報。

  PostgreSQL 專案感謝
  Hcamael、Amjad Shahzad、AntAISecurityLab 的 Tan Zhen、Tomer Fichman、
  Zheng Yu、Amy Burnett (OpenAI Codex Security)、Rick de Jager、Heewon
  Song、Sylvie Mayer、Aleksander Alekseev 與 Hillai Ben Sasson
  回報此問題。
  (CVE-2026-14669)
* 修正正規表示式比對／分割函式中的緩衝區溢位 (Masahiko Sawada)
  [§](https://postgr.es/c/b7e5c3f63)

  若傳入編碼無效的資料，這些函式可能寫入超過
  其轉換緩衝區的結尾。

  PostgreSQL 專案感謝
  Francesco Verardi
  回報此問題。
  (CVE-2026-14664)
* 強化 `ascii()` 函式對無效
  輸入的防護 (Michael Paquier)
  [§](https://postgr.es/c/08e812c02)

  藉由提供編碼無效的輸入，可以誘使此函式
  讀取並傳回少量不應讀取的資料位元組。在
  啟用斷言的建置中，也可能觸發其斷言。

  PostgreSQL 專案感謝
  Hcamael
  回報此問題。
  (CVE-2026-18024)
* 修正 `pg_restore_attribute_stats()` 中
  多範圍（multirange）型別的處理
  (OpenAI Security Research Team)
  [§](https://postgr.es/c/08454e8b2)
  [§](https://postgr.es/c/8d428c6e6)

  `pg_restore_attribute_stats()` 將多範圍
  型別視同其底層的範圍型別處理。這對於
  邊界直方圖可以正確運作，但對其他所有
  統計資訊種類則是錯誤的。

  PostgreSQL 專案感謝
  Amy Burnett (OpenAI Codex Security)
  回報此問題。
  (CVE-2026-16238)
* 讓 `scalarineqsel()` 檢查它預期為 `tid` 型別的
  常數是否確實是該型別 (Tom Lane)
  [§](https://postgr.es/c/a2cb5a1cf)

  對於所有使用此估算函式的內建運算子，這個預期都會成立，
  但惡意建構的運算子可能違反它，
  導致當機或伺服器記憶體內容外洩。

  PostgreSQL 專案感謝
  Hcamael
  回報此問題。
  (CVE-2026-14668)
* 強化 `tsvector` 與 `tsquery` 程式碼對
  過長值（包括個別詞素長度以及向量／查詢的總長度）
  的防護 (Tom Lane)
  [§](https://postgr.es/c/e25135057)
  [§](https://postgr.es/c/dddc8a69f)

  文件所記載的限制並未在所有程式碼路徑中強制執行。

  PostgreSQL 專案感謝
  Yuhang Wu、Zhenpeng Lin、Zheng Yu 與 Hcamael
  回報這些問題。
  (CVE-2026-14662)
* 修正多個誤以為不需要處理超過 `FUNC_MAX_ARGS` 個
  函式參數的地方 (Tom Lane)
  [§](https://postgr.es/c/7f0e1aac7)
  [§](https://postgr.es/c/2a03f21da)

  值得注意的是，伺服器對彙總函式參數數量的實際限制
  是 `FUNC_MAX_ARGS - 1`，但
  剖析器並未強制執行此限制，因而在後續處理中造成風險。

  PostgreSQL 專案感謝
  Zheng Yu、ylwangtju 與 Masahiko Sawada
  回報這些問題。
  (CVE-2026-14679)
* 拒絕從 SQL 呼叫接受或傳回
  `internal` 型別的函式 (Tom Lane)
  [§](https://postgr.es/c/54649de65)
  [§](https://postgr.es/c/722695db1)

  既有的防護措施已被證明不足以防止這種呼叫，
  因此加入更明確的檢查。

  PostgreSQL 專案感謝
  Amy Burnett (OpenAI Codex Security)
  回報此問題。
  (CVE-2026-14680)
* 在 `ALTER TABLE` 重建擴充統計資訊物件時，
  保留其擁有權 (Masahiko Sawada)
  [§](https://postgr.es/c/a1fa24127)

  先前，執行 `ALTER TABLE` 的角色會取得
  這類物件的擁有權，但這似乎並不恰當。

  PostgreSQL 專案感謝
  Noah Misch
  回報此問題。
  (CVE-2026-6469)
* 反剖析 `EXTRACT()` 函式呼叫時，
  視需要為欄位名稱加上引號 (Nathan Bossart)
  [§](https://postgr.es/c/0ddd9098a)

  剖析器接受任何字串常數作為
  `EXTRACT()` 中的欄位名稱，並將驗證延後到
  執行時才進行。若該呼叫被儲存後再反剖析（例如
  在 pg_dump 期間），字串內容會被
  原封不動地輸出，因而可能遭到 SQL 注入。

  PostgreSQL 專案感謝
  Ben Morris（與 Claude 及 Anthropic Research 合作）
  回報此問題。
  (CVE-2026-15741)
* 在先前未檢查資料型別 `USAGE` 權限的地方
  加入此項檢查 (Nathan Bossart)
  [§](https://postgr.es/c/2e91f8548)
  [§](https://postgr.es/c/57f59ca1d)
  [§](https://postgr.es/c/278053843)

  `CREATE TYPE AS RANGE` 沒有檢查，
  `ALTER TABLE OF` 沒有檢查，建立
  預存運算式的命令也沒有檢查。這些疏漏使得
  沒有 `USAGE` 權限的角色仍然可以建立
  相依於該型別的物件，可能使型別的擁有者
  日後無法變更該型別。

  PostgreSQL 專案感謝
  Jingzhou Fu
  回報此問題。
  (CVE-2026-6470)
* 角色變更後，使與角色相關的快取計畫失效
  (Ilya Staroverov, Shinya Kato, Nathan Bossart)
  [§](https://postgr.es/c/0b12f56bf)

  角色成員資格、角色屬性與資料庫擁有權的變更，可能
  影響資料列層級安全原則的預期行為，但
  先前我們仍會繼續使用依據
  舊狀態所建立的快取計畫。

  PostgreSQL 專案感謝
  Ilya Staroverov 與 Shinya Kato
  回報此問題。
  (CVE-2026-14666)
* 在直接 SSL 連線之後拒絕 GSSEncRequest (Michael Paquier)
  [§](https://postgr.es/c/203a48209)

  在建立 TLS 加密連線之後，伺服器
  仍會接受 GSSAPI 加密的請求。若該請求成功，
  連線會繼續使用 TLS 加密，但在
  `pg_hba` 規則看來，它會像是一個 GSS 連線。
  因此，意圖禁止 TLS 的 `pg_hba` 原則
  將無法正確執行。

  PostgreSQL 專案感謝
  p4p3r
  回報此問題。
  (CVE-2026-14681)
* 讓模擬的 SCRAM 認證祕密更加逼真 (Nathan Bossart)
  [§](https://postgr.es/c/822143c4d)

  若對不存在或沒有 SCRAM 祕密的角色嘗試 SCRAM 登入，
  我們會產生一個模擬祕密，並照常進行
  認證交握，以避免向攻擊者洩露這些事實。
  但模擬祕密是以固定的迭代次數產生的，
  這本身就可能成為一種可觀察到的回應差異。
  改用設定參數 `scram_iterations`，
  讓模擬祕密看起來更像該安裝環境中
  真正的祕密。

  PostgreSQL 專案感謝
  Radim Marek
  回報此問題。
  (CVE-2026-14672)
* 修正 ecpg 應用程式中，因從伺服器收到無效的
  `bytea` 資料而造成的越界寫入
  (Michael Paquier)
  [§](https://postgr.es/c/a14ba29b1)

  ecpg 未經檢查就假設
  任何 `bytea` 值都必定以 `\x` 開頭。
  損壞或惡意的伺服器可能送出短於 2 個
  位元組的字串，導致應用程式中的記憶體遭到覆寫。

  PostgreSQL 專案感謝
  ylwangtju
  回報此問題。
  (CVE-2026-16241)
* 不對 psql 的 `\unrestrict`
  命令的參數進行反引號展開 (Nathan Bossart)
  [§](https://postgr.es/c/71ca694c7)

  CVE-2025-8714 修正中的這個疏漏，使惡意
  伺服器可以將 shell 命令注入純文字傾印輸出中，
  這些命令會在還原時於執行
  psql 的機器上執行，而這正是
  CVE-2025-8714 原本要防止的情境。

  PostgreSQL 專案感謝
  Lucas Velgus、Filip Janus 與 Daniel Bakker
  回報此問題。
  (CVE-2026-18408)
* 移除 pg_dump 對
  `pg_proc`.`protrftypes`
  的項目數不會超過 `FUNC_MAX_ARGS` 的假設
  (Tom Lane)
  [§](https://postgr.es/c/3392cce5c)

  由於輸入參數與輸出參數都可能有項目，
  此陣列的長度確實有可能超過
  `FUNC_MAX_ARGS`（它只限制輸入
  參數）。即使並非如此，
  pg_dump 也不能假設伺服器
  建置時所用的 `FUNC_MAX_ARGS` 值與
  它本身相同。溢位會導致
  pg_dump 內部的記憶體遭到覆寫。

  PostgreSQL 專案感謝
  Masahiko Sawada
  回報此問題。
  (CVE-2026-19385)
* 強化 PL/Perl
  對「tied」（繫結的）Perl 陣列與雜湊的防護 (Tom Lane)
  [§](https://postgr.es/c/87c4b8219)

  行為與一般物件不同的繫結物件，可能導致
  記憶體遭到覆寫，或建構出損毀的結果陣列（這
  很可能在稍後造成問題）。

  PostgreSQL 專案感謝
  Hcamael
  回報此問題。
  (CVE-2026-14670)
* 修正 PL/Perl
  與 PL/Tcl 中記憶體配置計算的整數溢位 (Heikki Linnakangas)
  [§](https://postgr.es/c/028ee716a)

  這與 CVE-2026-6473 是同一類問題，只是發生在
  程式碼的不同部分，並以相同方式修正。

  PostgreSQL 專案感謝
  Tulya Project (Team Dhiutsa, Bitecope Technologies Private Ltd)
  回報此問題。
  (CVE-2026-14677)
* 確保 `contrib/amcheck` 函式在執行索引
  運算式之前，先限制 `search_path`
  (Noah Misch)
  [§](https://postgr.es/c/0a61fcde0)

  由於 amcheck 會以資料表擁有者的身分執行這類索引運算式，
  呼叫者有可能
  劫持相依於 `search_path` 的函式，以資料表擁有者的身分
  執行任意程式碼。預設情況下這並不構成
  漏洞，因為只有超級使用者可以呼叫 amcheck
  函式；但若該權限已授與他人，所造成的風險
  就比文件所說的更大。

  PostgreSQL 專案感謝
  Yuelin Wang 與 Jacob Brazeal
  回報此問題。
  (CVE-2026-14673)
* 修正 `contrib/fuzzystrmatch` 的
  `levenshtein()`
  與 `levenshtein_less_equal()` 函式中的整數溢位
  (Nathan Bossart)
  [§](https://postgr.es/c/e88eb4e76)

  傳入很大的成本值給這些函式可能造成整數
  溢位，因而產生無意義的結果，在某些情況下甚至會造成
  越界寫入。

  PostgreSQL 專案感謝
  Ben Morris（與 Claude 及 Anthropic Research 合作）
  回報此問題。
  (CVE-2026-15742)
* 修正 `contrib/pg_stat_statements`
  中的緩衝區溢位 (Álvaro Herrera)
  [§](https://postgr.es/c/8a31ffc2d)

  查詢正規化未能準確計算正規化後的字串
  所需的空間大小。

  PostgreSQL 專案感謝
  Sajeeb Lohani（與 TrendAI Zero Day Initiative 合作）與 Yuelin Wang
  回報此問題。
  (CVE-2026-14676)
* 修正 `contrib/pg_trgm` 的 GiST
  picksplit 函式中的資料型別錯誤 (Heikki Linnakangas)
  [§](https://postgr.es/c/849019a50)

  這個錯誤會導致讀取超過緩衝區的結尾，
  通常造成不佳的分割決策；但若運氣非常不好，
  也可能導致當機。

  PostgreSQL 專案感謝
  Mehmet D. Ince
  回報此問題。
  (CVE-2026-14678)
* 移除 `contrib/refint` 中的計畫快取
  (Ayush Tiwari)
  [§](https://postgr.es/c/79a506228)

  這個快取行為有數個嚴重的錯誤，其中值得注意的是
  `check_foreign_key()` 會將新的鍵值嵌入
  它的串聯 UPDATE 查詢中，因此快取的計畫會重複使用
  最初所需的值，而非應該使用的鍵值。
  最簡單的解決方法就是將它移除。

  PostgreSQL 專案感謝
  Hcamael
  回報此問題。
  (CVE-2026-14671)
* 確保平行 GIN 索引建置會正確更新資料表的
  `pg_class`.`reltuples`
  值 (Jan Nidzwetzki, Tomas Vondra)
  [§](https://postgr.es/c/d4420a972)

  平行工作程序可能會為其所處理的資料列數
  回報一個未初始化的值，導致
  `reltuples` 出現錯誤的值，甚至是 Infinity 或 NaN。
  這樣的值可能導致後續的 autovacuum 與 autoanalyze
  作業永遠不會判定該資料表需要處理。
  若是如此，這種情況不會自行修復。需要手動執行
  `ANALYZE` 命令，或建立另一個索引，
  才能將 `reltuples` 重設為
  正確的值。若你有任何包含 GIN 索引的資料表，
  建議檢查它們的 `reltuples` 項目
  看起來是否合理。
  像下面這樣的查詢可能會有幫助：

  ```

  SELECT DISTINCT t.oid::regclass, t.reltuples
  FROM pg_class t
    JOIN pg_index i ON t.oid = i.indrelid
    JOIN pg_class ic ON i.indexrelid = ic.oid
  WHERE t.relhasindex AND ic.relam = 2742;
  ```
* 修正重新掃描非同步 Append 計畫節點時，
  對非同步讀取的錯誤處理 (Alexander Korotkov, Gleb Kashkin,
  Etsuro Fujita)
  [§](https://postgr.es/c/4ea497a92)

  當上層計畫節點在讀取完整個 Append 輸出之前就重新掃描該 Append 時，
  我們需要捨棄所有已送往外部伺服器、
  尚在進行中的請求（例如由 `postgres_fdw`
  送出的請求）。在子計畫有參數變更，
  或在下一次掃描中被分割區修剪捨棄的情況下，這一點並未正確處理。
  其結果可能是錯誤的查詢結果、無窮
  迴圈，或斷言失敗。
* 修正 RANGE 分割資料表在分割區修剪時的錯誤
  (David Rowley)
  [§](https://postgr.es/c/02e69be47)

  在某些情況下，DEFAULT 分割區會在不應略過時
  被略過，可能導致查詢結果中缺少資料列。
* 在修剪結果關聯之後，正確更新 ModifyTable 計畫
  節點中的外部資料包裝器狀態 (Ayush Tiwari, Rafia Sabih)
  [§](https://postgr.es/c/1ef917e3a)
  [§](https://postgr.es/c/bba4e095d)

  先前，若執行期分割區修剪判定分割目標資料表的某些
  分割區不需要掃描，
  而該資料表又有任何外部資料表分割區，則很可能
  發生當機或錯誤的行為。
* 修正對具有 `BEFORE UPDATE` 觸發程序之資料表執行
  帶 `RETURNING OLD` 的 `UPDATE` 時，
  遺漏並行更新的問題 (Dean Rasheed)
  [§](https://postgr.es/c/4908225be)

  若目標資料列被並行更新，則在隔離
  等級 `READ COMMITTED` 下，`RETURNING` 中任何 `OLD`
  值都應該反映更新後的
  資料列。但若有觸發程序，傳回的卻是過時的值
  （雖然觸發程序本身以及最終的輸出資料列看到的是
  正確的值）。
* 修正有多個連接鍵且有許多 NULL 值時，
  雜湊連接的效能問題 (David Rowley)
  [§](https://postgr.es/c/f70acc8a2)

  鍵為 null 的元組不應插入雜湊表中，因為
  它們永遠不會與任何其他元組相符。若
  null 出現在非最後一個連接欄位中，程式碼的處理就是錯的；若許多
  輸入都含有 null，會使雜湊表大幅膨脹。
* 修正 `RETURNING` 運算式中
  加上括號的 `OLD`/`NEW`
  的剖析 (Marko Grujic)
  [§](https://postgr.es/c/9108fed3e)

  像 `(old).colname`
  與 `(old).*` 這樣的運算式處理有誤，實際上
  會被轉換成 `NEW` 參照。
* 修正規劃器對 `value IN
  (array)` 運算式
  的可為 null 性與嚴格性檢查
  (Ayush Tiwari)
  [§](https://postgr.es/c/277122036)

  只有在已知陣列運算元
  非空時，這些檢查才應該成立，但先前遺漏了這項考量，使得
  不應套用的最佳化被套用。若陣列實際上是空的，
  可能導致錯誤的查詢結果。
* 修正錯誤的連接移除邏輯 (Matheus Alcantara, Richard Guo)
  [§](https://postgr.es/c/21f5e659e)
  [§](https://postgr.es/c/9e40d07e1)

  在邊界情況下，來自外部連接可為 null 那一側內部的
  常數輸出值，有可能在應該被 NULL 取代時
  未被取代。
* 在連接移除期間更徹底地清理 PlaceHolderVar
  (Richard Guo, Arne Roland)
  [§](https://postgr.es/c/e02526795)
  [§](https://postgr.es/c/18105e6db)

  此修正更正了各種可能觸發斷言或
  產生錯誤計畫的邊界情況。
* 補上對容器資料型別（陣列、複合型別、範圍）之相等比較
  可雜湊性的遺漏檢查 (Andrei Lepikhov,
  Tom Lane)
  [§](https://postgr.es/c/11aed8d19)

  規劃器在決定可以使用以雜湊為基礎的計畫類型之前，
  必須先驗證容器之組成型別的可雜湊性。
  某些地方遺漏了這個步驟，導致在執行時發生
  “could not identify a hash function”失敗。
* 避免將 `WHERE` 子句下推越過具有不同
  等價規則的分組步驟 (Richard Guo)
  [§](https://postgr.es/c/fe5d62951)

  對以非確定性定序進行分組的分組欄位所做的測試，
  只有在它是使用同一個定序的比較時，
  才能安全地下推。否則，它可能會過濾掉一些分組
  原本會合併的資料列。
* 修正具有 `EXCLUDE` 子句或
  缺少 `ORDER BY` 的 `COUNT` 視窗函式
  的錯誤最佳化 (Chengpeng Yan, David Rowley)
  [§](https://postgr.es/c/cf184ec77)

  這些視窗函式在不應被視為單調時
  被當成單調函式處理，因而可能算出錯誤的結果。
* 避免規劃器查詢 `"char"` 型別欄位的統計資訊時，
  發生“cache lookup failed for collation 0”錯誤
  (Feng Wu)
  [§](https://postgr.es/c/5fd1c3f28)
* 修正 `ALTER COLUMN ... DROP EXPRESSION`，使其在
  有多層分割區時也能運作 (Alberto Piai)
  [§](https://postgr.es/c/c374f2807)
* 修正附加屬於排除限制條件之索引的分割區
  (Japin Li)
  [§](https://postgr.es/c/19e3aa704)

  值得注意的是，這個疏漏使分割的排除
  限制條件無法正確傾印與還原。
* 禁止透過 `ALTER CONSTRAINT` 對
  分割的 `NOT NULL` 限制條件設定
  `NO INHERIT` (Andreas Karlsson)
  [§](https://postgr.es/c/41247cdf6)

  分割資料表上的 `NOT NULL` 限制條件
  應該由所有分割區繼承，因此不可以
  被標記為 `NO INHERIT`。建立限制條件時
  會正確強制執行這條規則，但 `ALTER TABLE
  ... ALTER CONSTRAINT` 則沒有。
* 禁止將規則重新命名為 `_RETURN` (Tom Lane)
  [§](https://postgr.es/c/a7f7958ab)

  這個名稱保留給檢視表的 `ON SELECT`
  規則使用，但 `ALTER RULE` 允許將其他規則重新命名
  為 `_RETURN`，在稍後造成問題。
* 修正 `DROP
  OWNED BY` 中角色成員資格授權遺漏釋放鎖定的問題 (Jeff Davis)
  [§](https://postgr.es/c/a0daa0b41)

  這個疏漏會產生一則警告訊息，接著
  對該成員資格授權的鎖定會一直保留到交易結束。
* 修正 `EXPLAIN` 在
  反剖析 `SQL/JSON` 彙總函式時的失敗 (Richard Guo)
  [§](https://postgr.es/c/45364e496)

  某些計畫結構會導致“invalid JsonConstructorExpr underlying node type”錯誤。
* 修正搭配延遲唯一性限制條件使用
  `REINDEX CONCURRENTLY` 的問題 (Nitin Motiani)
  [§](https://postgr.es/c/e4527519b)

  在 `REINDEX
  CONCURRENTLY` 期間建立的暫時索引副本，被錯誤地標記為強制執行立即
  唯一性檢查，導致誤報違反限制條件。
* 修正使用非確定性定序與反斜線時的
  `LIKE` 比對 (Nitin Motiani, Tom Lane)
  [§](https://postgr.es/c/a99bd8d58)
  [§](https://postgr.es/c/51652c42d)

  使用非確定性定序時，`LIKE`
  錯誤處理了跳脫的反斜線（`\\`），實際上
  將它視為不存在。對於位在一般字元前面的
  前導反斜線，它的處理也是錯的；在這種情況下，
  反斜線實際上應該被忽略，但它卻使該一般
  字元被精確比對，而不是讓
  非確定性定序決定是否相符。
* 修正針對完全相符模式之索引掃描的 `LIKE`／正規表示式最佳化
  (Jelte Fennema-Nio)
  [§](https://postgr.es/c/d0bb49e61)

  為非確定性定序而對 `LIKE` 所做的重構，
  意外破壞了在索引定序與運算式定序不相符時，
  將 `LIKE` 或正規表示式的完全相符模式轉換為
  相等索引條件的最佳化。此問題的影響之一，
  是使 psql 的
  `\d tablename`
  命令變得慢很多。
* 修正 `to_date()` 中當地語言月份／星期名稱的比對
  (Heikki Linnakangas)
  [§](https://postgr.es/c/011384ba4)
  [§](https://postgr.es/c/5f003855e)

  在大小寫轉換會改變字串位元組長度的情況下，
  比對邏輯會出錯。
* 更正希臘文字尾 sigma 的大小寫轉換規則 (Jeff Davis)
  [§](https://postgr.es/c/66ec24276)

  若字串前面只有 Case Ignorable 字元，則不要
  將它視為字尾 sigma。這只影響
  內建的 `pg_unicode_fast` 區域設定。
* 修正韓文字母 U+11A7 (TBASE) 錯誤的 NFC 重組
  (Diego Frias, Michael Paquier)
  [§](https://postgr.es/c/273fe9485)

  此字元被當成有效的 T 音節（實際上並不是），
  因而在正規化期間被悄悄吞掉。
* 避免不區分大小寫的
  `synonym` 字典可能截斷輸出詞素 (Jeff Davis)
  [§](https://postgr.es/c/89e648498)

  若轉換為小寫增加了詞素的位元組長度，
  輸出時它會被錯誤地截斷為原本的位元組長度。
* 在大小寫轉換邏輯中防範被截斷的 UTF-8 字元
  (Jeff Davis)
  [§](https://postgr.es/c/9021c8f3c)
* 修正 `hash_record_extended()` 中的筆誤 (Man Zeng)
  [§](https://postgr.es/c/b3f13c032)

  這段程式碼未初始化傳給
  FunctionCallInvoke() 的第二個 isnull 參數。對於現有的核心內建
  擴充雜湊支援函式而言，這並無害處，因為它們不會檢查該值。
  不過，若擴充功能所提供的雜湊函式會
  檢查 `PG_ARGISNULL(1)`，就可能受到影響。
* 修正 `pg_get_publication_tables()`，使其在
  可發佈的資料表被並行移除時不會失敗 (Bharath Rupireddy)
  [§](https://postgr.es/c/73d63d1c1)
* 防止 `satisfies_hash_partition()` 在
  遇到 `VARIADIC NULL` 時當機 (Robert Haas)
  [§](https://postgr.es/c/0c06ebf12)
* 在 `tsvector_filter()` 及相關函式中，
  更清楚且一致地回報無效權重錯誤
  (Ewan Young)
  [§](https://postgr.es/c/c5194139c)

  特別是，對於非可列印 ASCII 的權重字元，
  會以八進位形式（`\nnn`）回報，
  與 `charout()` 的呈現方式相同。這可避免
  產生編碼無效的錯誤訊息。
* 拒絕 `uuidv7()` 中超出範圍的時間戳記位移值
  (Baji Shaik)
  [§](https://postgr.es/c/c31b0fca0)

  位移值不可大到使產生的時間戳記超出
  v7 UUID 所能表示的範圍。先前會產生
  無意義的 UUID 值。
* 修正 `xpath()` 中對命名空間節點的錯誤處理
  (Michael Paquier)
  [§](https://postgr.es/c/4c777d6dd)
  [§](https://postgr.es/c/0d145be2c)

  此修正可避免非預期的“could not copy node”
  錯誤。
* 修正 `jsonpath` 的 `.decimal` 方法，使其
  在精確度或小數位數不正確時不擲出硬性錯誤 (Ewan Young)
  [§](https://postgr.es/c/84001a04d)
  [§](https://postgr.es/c/90789900b)

  靜默（silent）模式應該抑制這些錯誤，但先前沒有做到。
* 修正 `IS JSON` 或類似
  語法結構的參數屬於字串類別、但缺少
  轉型為 `text` 型別的轉換時，發生的 NULL 指標當機 (Ayush Tiwari)
  [§](https://postgr.es/c/35d9a6263)

  核心 PostgreSQL 中沒有這類資料型別，
  但使用某些擴充功能的型別時，
  就可能遇到此問題。
* 確保 `SQL/JSON` 的 `ON EMPTY / ON ERROR
  DEFAULT` 值會被強制轉換為正確的 typmod (Ewan Young)
  [§](https://postgr.es/c/441e4c8d6)

  例如，`numeric` 目標欄位所宣告的精確度與小數位數，
  先前並未套用到預設
  值上。
* 避免將最小的
  `money` 值除以 -1 時出現與機器相關的行為 (Andrey Rachitskiy)
  [§](https://postgr.es/c/6298a41b4)
* 修正在為文字搜尋字典建立快取項目途中，
  發生記憶體不足失敗後的當機 (Tom Lane)
  [§](https://postgr.es/c/81b1e7916)
* 修正處理不正確的 ispell/hunspell
  字典檔時的記憶體安全錯誤 (Andrey Rachitskiy)
  [§](https://postgr.es/c/4689ea9ce)
* 防止存取其他工作階段的暫存資料表 (Jim Jones,
  Daniil Davydov, Alexander Korotkov)
  [§](https://postgr.es/c/1b0dd0815)
  [§](https://postgr.es/c/3aaefe892)

  某些程式碼路徑未能防止這種存取，導致悄悄產生錯誤
  （不一致）的結果。
* 防止存取暫存資料表期間發生“no empty local buffer available”錯誤
  (Melanie Plageman)
  [§](https://postgr.es/c/ed8050370)

  限制讀取串流機制可以使用的
  本地緩衝區數量。先前，
  `effective_io_concurrency` 的值很大時，可能讓單一
  串流用盡所有緩衝區，導致失敗。
* 修正 autovacuum 處理資料庫的順序
  (Rustam Khamidullin)
  [§](https://postgr.es/c/4cc49cb70)

  它在無意間依分數由低到高處理資料庫，
  但應該反過來才對。
* 在 `VACUUM` 的回捲安全防護模式中，
  恢復完整使用共享緩衝池
  (Melanie Plageman)
  [§](https://postgr.es/c/585181e07)
  [§](https://postgr.es/c/7c25cdb1e)

  一般的 `VACUUM` 只能使用少數幾個
  共享緩衝區，以免過度干擾其他處理。
  然而，在安全防護模式中，我們希望盡快回收交易 ID，
  因此應該放棄這項限制，
  讓清理作業能以最快的速度進行。這個行為
  在 v18 的重構期間意外遭到破壞；現在予以恢復。
* 修正平行 vacuum 工作程序中的記憶體洩漏 (Baji Shaik)
  [§](https://postgr.es/c/4154a1482)

  平行工作程序每回報一次進度約會洩漏 1kB，
  而這些浪費會在該工作程序的整個生命週期中累積。
* 在 GIN 索引 posting tree
  清理期間，遵循查詢取消與 vacuum 延遲 (Paul Kim, Alexander Korotkov)
  [§](https://postgr.es/c/7becb647d)

  常見值的 posting tree 可能很大，因此
  缺少這項檢查可能使 vacuum 執行很長一段時間後
  才注意到中斷。
* 修正 GiST 與 SP-GiST
  僅索引掃描期間可能錯誤解碼索引元組的問題 (Peter Geoghegan)
  [§](https://postgr.es/c/959b7fa2c)

  此錯誤可能導致僅索引掃描計畫輸出損毀的資料。
  唯一受影響的核心運算子類別是 GiST 的 range_ops，而且
  只有在範圍欄位不是第一個索引
  欄位時才會失敗。
* 確保大量擴充之資料表的新最後一個區塊，會即時加入
  其可用空間對應表 (Jingtang Zhang)
  [§](https://postgr.es/c/eabc9a9dd)

  一個差一錯誤導致多區塊資料表擴充的最後一個區塊
  未在對應表中被標記為可用。這最終
  會由 vacuum 更正，但在此之前，該空間不會
  被使用。
* 避免交易中止期間的資源清理可能發生的重複釋放，
  或無窮的錯誤復原迴圈 (Tom Lane)
  [§](https://postgr.es/c/ac6a58a70)
* 建立目錄時，容許同一個目錄被並行建立
  (Andrew Dunstan, Tom Lane)
  [§](https://postgr.es/c/aa80c34c8)
* 修正 JIT 編譯的元組解構程式碼，使其正確考量
  虛擬產生欄位 (David Rowley)
  [§](https://postgr.es/c/e9692de1d)
* 藉由對任何被相依的物件取得
  共享鎖定，防止建立懸空的物件相依關係 (Bertrand Drouvot)
  [§](https://postgr.es/c/c8cd3d697)
  [§](https://postgr.es/c/f9d5a52da)

  共享鎖定會與任何嘗試移除
  被相依物件的動作衝突，從而消除先前存在的
  競爭條件。例如，若某個工作階段移除一個綱要（在它看來
  是空的），同時另一個工作階段正在該綱要中建立
  函式，先前兩筆交易都可能提交，
  留下無效的函式定義。現在，其中一筆交易
  會失敗。
* 修正 `SERIALIZABLE` 隔離模式中
  衝突偵測的競爭條件
  (Peter Geoghegan)
  [§](https://postgr.es/c/d560e730e)

  在檢查一個最初為空的 btree
  索引時，可能遺漏衝突，因而不當地
  允許互相衝突的交易提交，使可序列化性失效。
* 修正 ProcSignalBarrier 程式碼中的競爭條件 (Masahiko Sawada)
  [§](https://postgr.es/c/1a9b1cc18)

  此錯誤可能導致程序卡住，通常是在
  回報“still waiting for backend with PID *`nnnn`* to accept ProcSignalBarrier”之後。
* 修正屬於同一個鎖定群組的一組程序
  同時結束時的競爭條件 (Vlad Lesin)
  [§](https://postgr.es/c/ae08eb168)
  [§](https://postgr.es/c/12c9b8b42)

  這些錯誤可能導致 PANIC 中止，並出現
  “latch already owned”之類的訊息。在一般的平行查詢中，
  這個問題通常不會發生，因為領導者在
  看到其工作程序完成之前不會結束；但某些擴充功能會遇到這個問題。
* 修正清除資料表可見性對應表位元之操作的 WAL 記錄
  (Melanie Plageman, Andres Freund)
  [§](https://postgr.es/c/d0fb1da21)
  [§](https://postgr.es/c/f581fa729)
  [§](https://postgr.es/c/4d7feebfb)

  WAL 摘要程序會遺漏這類 VM 變更，可能
  導致錯誤的增量備份。我們也未能在需要時
  記錄這類 VM 頁面的完整頁面映像，可能使
  頁面寫入撕裂未被修正。這可能在之後造成異常行為，
  例如僅索引掃描產生錯誤的結果。
* 防止 WAL 摘要程序在時間軸
  切換時卡住 (Robert Haas)
  [§](https://postgr.es/c/18f0de6b8)
  [§](https://postgr.es/c/1d299d6ab)
* 修正待命伺服器提升期間，邏輯解碼中時間軸選擇的競爭條件
  (Bertrand Drouvot)
  [§](https://postgr.es/c/b4bd13850)
  [§](https://postgr.es/c/4bff3aa51)

  在待命伺服器上進行的邏輯解碼可能會因
  “requested WAL segment has already been removed”
  錯誤而失敗。重試一次就會成功，因此不會造成永久性
  問題，但存在可用性上的風險。
* 避免在時間軸跳轉期間暴露 WAL 接收程序的完整連線字串
  (Chao Li)
  [§](https://postgr.es/c/b903d1792)

  `pg_stat_wal_receiver` 檢視表應該顯示
  經過清理、不含敏感資料的連線字串版本。
  但在我們重複使用既有的
  WAL 接收程序時，它會短暫顯示完整的字串。
* 在邏輯複寫期間，使用執行期檢查而不只是 Assert，
  來驗證所收到元組中的欄位數是否正確 (Varik
  Matevosyan)
  [§](https://postgr.es/c/dc3db3a83)

  惡意或有錯誤的發佈者可能送出數量不一致的
  欄位。雖然我們找不到這會造成
  嚴重不良影響的情境，但額外的謹慎似乎是值得的。
* 清理所建構之複寫命令中字串參數的引號處理
  (Tom Lane)
  [§](https://postgr.es/c/abb582555)

  多個產生複寫命令的地方，在為複寫插槽名稱
  以及其他需要插入這些命令的參數加上引號時
  不夠謹慎。這可能導致這些命令中出現
  非預期的語法錯誤。理論上，
  精心構造的複寫插槽名稱可能導致 SQL 注入；但
  這種情境在實務上似乎極不可能發生，因為
  複寫作業只能由擁有高度權限的
  使用者執行，而他們沒有理由使用來自
  不可信來源的插槽名稱。
* 修正空的預備交易的邏輯解碼 (Masahiko Sawada)
  [§](https://postgr.es/c/b563fc6bd)

  未產生任何可解碼更新的預備交易，可能
  導致在前面沒有 `PREPARE` 的情況下，
  將 `COMMIT/ROLLBACK PREPARED` 送給
  輸出外掛程式。對於
  內建的訂閱者而言，這會破壞複寫，其他外掛程式
  大概也不會樂見這種情況。
* 修正待命伺服器提升後無日誌序列的損毀
  (Fujii Masao)
  [§](https://postgr.es/c/627605713)

  先前，若在主要伺服器上建立無日誌序列並
  複寫到待命伺服器，在提升該待命伺服器後存取該序列，
  可能會因“bad magic number in sequence”
  或相關錯誤而失敗。
* 修正串聯待命伺服器在退回使用封存後重新連線失敗的問題
  (Marco Nenciarini)
  [§](https://postgr.es/c/331016322)

  串聯待命伺服器在退回到封存復原之後，
  可能無法重新連線到其上游待命伺服器，並出現
  “requested starting point ... is ahead of the WAL flush position”。
* 防止在 WAL 重播達到一致的資料庫狀態之前
  就接受熱待命連線 (Nikhil Sontakke)
  [§](https://postgr.es/c/311e66df9)
* 不要嘗試在待命伺服器上於本地清除
  `pg_database`.`dathasloginevt`
  (Ayush Tiwari)
  [§](https://postgr.es/c/97b5c5aaa)

  事件觸發程序清理除了在主要伺服器上，也會嘗試在待命
  伺服器上執行此動作。這在待命伺服器上無法運作，
  而且也沒有必要，因為重播主要伺服器的資料庫
  變更很快就會修正它。
* 移除過時的複寫插槽時避免競爭條件
  (Xuneng Zhou)
  [§](https://postgr.es/c/08458bcae)

  若另一個工作階段立即重複使用被移除插槽的共享記憶體項目，
  可能發生錯誤的解鎖與日誌訊息。
* 移除暫時性複寫插槽時避免競爭條件
  (Zhijie Hou)
  [§](https://postgr.es/c/f833c9207)

  釋放插槽的程式碼在釋放插槽之後，還會對
  複寫插槽的共享記憶體項目進行一些額外的更新。
  這並不安全，因為另一個工作階段可能會立即重複使用
  被移除插槽的共享記憶體項目。對於暫時性插槽，
  略過這些更新。
* 修正邏輯複寫資料表
  同步期間過時的進度回報 (Shinya Kato)
  [§](https://postgr.es/c/d9cd9b4d7)

  先前，即使資料複製已經完成，
  訂閱者中的 `pg_stat_progress_copy` 檢視表
  仍會繼續將
  初始的 `COPY` 作業顯示為進行中。這個過時的項目
  會一直可見，直到同步趕上發佈者為止。
* 備份失敗時清除基礎備份進度 (Chao Li)
  [§](https://postgr.es/c/e7564ee8c)
  [§](https://postgr.es/c/e2ad214dd)

  先前，失敗之後 `pg_stat_progress_basebackup`
  檢視表會繼續顯示過時的進度項目，
  直到複寫用戶端
  中斷連線為止。pg_basebackup 通常會
  立即中斷連線，但其他用戶端可能不會。
* 修正啟用 `track_functions` 時，
  因 pgstats 項目被並行移除而可能發生的 PANIC (Sami Imseih,
  Michael Paquier)
  [§](https://postgr.es/c/5cc59834b)
  [§](https://postgr.es/c/8a4f389dd)
  [§](https://postgr.es/c/fe464e9e6)
* 在無法為對應的共享雜湊表項目取得空間後，
  清理損壞的本地 pgstats 項目 (Niall Newman)
  [§](https://postgr.es/c/2fd8d45ec)

  未進行這項清理，會在下次使用該本地項目時
  導致空指標解參考。
* 避免在讀取或寫入失敗後記錄錯誤的 I/O 作業統計資訊
  (Bertrand Drouvot)
  [§](https://postgr.es/c/13f940b4b)
* 在 PL/Perl 中，避免處理
  無效的 `PostgreSQL::InServer::ARRAY` 物件時
  發生 NULL 指標解參考當機 (Xing Guo)
  [§](https://postgr.es/c/e430ecc59)
* 在 PL/Python 中，處理序列（sequence）與對應（mapping）物件時
  正確檢查錯誤 (Richard Guo)
  [§](https://postgr.es/c/53482fcb9)

  先前，損壞的物件或未處理的例外可能
  導致 NULL 指標解參考當機。
* 在 libpq 中，於
  `pqReadData()` 期間一律清空
  SSL 或 GSS 解密緩衝區中所有待處理的位元組 (Jacob Champion)
  [§](https://postgr.es/c/2167302b7)
  [§](https://postgr.es/c/bb0a54518)
  [§](https://postgr.es/c/27761c015)
  [§](https://postgr.es/c/87c3a79ea)

  這可避免某些邊界情況：libpq 或其
  呼叫端應用程式在等待更多資料抵達 socket，但
  實際上所有資料都已抵達。
* 改善 libpq 對記憶體不足
  情況的處理 (Anthonin Bonnefoy)
  [§](https://postgr.es/c/6b46a5d1b)
* 修正 libpq 的追蹤功能，使其正確輸出
  新式的 BackendKeyData 與 CancelRequest 訊息
  (Anthonin Bonnefoy)
  [§](https://postgr.es/c/dd5eca055)
* 允許 libpq 接受
  超過 30000 位元組的 ParameterDescription 訊息 (Ning Sun)
  [§](https://postgr.es/c/b1ab4bc52)

  先前，在 libpq 的有效性啟發式規則中，
  這種訊息類型並不屬於可能很長的類型。
  這項限制導致參數超過 7498 個的預備查詢失敗；
  這種情況雖然不太可能發生，但是受支援的。
* 修正 ecpg 編譯器中的空指標當機
  (Jehan-Guillaume de Rorthais)
  [§](https://postgr.es/c/917fdbc63)

  ecpg 在處理
  包含巢狀於 struct 內之 union 的 `DECLARE` 區段時會失敗。
* 拒絕 ecpg 的 `GET/SET
  DESCRIPTOR` 陳述式中出現多個描述區標頭項目
  (Masashi Kamura)
  [§](https://postgr.es/c/081434b0f)

  先前文法允許這種語法，但產生的 C 程式碼有誤。
  現在調整文法與說明文件，只允許
  一個標頭項目。
* 修正 psql 中管線模式下
  延遲錯誤的問題 (Michael Paquier)
  [§](https://postgr.es/c/1e9bc4074)

  在伺服器回應 Sync 訊息時回報錯誤（例如延遲限制條件
  違反）的某些情境中，psql 可能會卡住或發生
  斷言失敗。
* 讓 psql 的擴展對齊輸出格式中
  各行寬度一致 (Pavel Stehule)
  [§](https://postgr.es/c/07a6c262b)

  當資料表的資料列比記錄標頭行窄時，
  加寬資料列以符合標頭，避免輸出不美觀。
* 強制執行 psql 特殊變數
  `WATCH_INTERVAL`
  預期的上限
  (Sven Klemm, Daniel Gustafsson)
  [§](https://postgr.es/c/e0c641ebb)

  若指定的值過大，psql
  會回報錯誤，但仍然套用該設定。
* 修正 psql 在 `\l+` 中顯示
  資料庫大小時的權限檢查 (Christoph Berg)
  [§](https://postgr.es/c/f2d6cf880)

  底層的伺服器函式允許
  具有 `pg_read_all_stats` 權限的使用者查看
  所有資料庫的大小，即使他們沒有 `CONNECT`
  權限。但 psql 不知道這項
  規定，除非使用者
  具有 `CONNECT` 權限，否則不會呼叫該函式。
* 修正 psql 對
  `\df` 的 Tab 鍵補全，使其也考慮程序
  (Erik Wienhold)
  [§](https://postgr.es/c/598af79b1)
* 修正 pgbench 中執行緒安全的錯誤
  (Fujii Masao)
  [§](https://postgr.es/c/98dd6c204)

  當 pgbench 以多個執行緒
  搭配 `--verbose-errors` 選項執行時，不同執行緒
  可能嘗試使用同一個緩衝區來建構錯誤訊息，
  導致日誌輸出損毀。
* 在 pg_combinebackup 中，防止來源檔案
  比預期短時發生無窮迴圈 (Peter Eisentraut)
  [§](https://postgr.es/c/d36b72894)
* 修正 pg_createsubscriber 發生錯誤後
  對發佈者端物件的清理 (Nisha Moond)
  [§](https://postgr.es/c/196b4b5ae)

  當 pg_createsubscriber 在
  建立邏輯複寫物件後失敗時，應該移除它在發佈者上
  建立的發佈與複寫插槽。
  某些錯誤情況並未這麼做。
* pg_recvlogical 的輸出檔案
  使用來源叢集的群組讀取檔案權限
  (Fujii Masao)
  [§](https://postgr.es/c/89b4b3ae3)

  文件記載 pg_recvlogical 會
  有這種行為，但它實際上從未啟用群組讀取權限。
* 修正 pg_restore 搭配
  `--statistics`
  或 `--statistics-only` 時不一致的行為
  (Chao Li, Michael Paquier)
  [§](https://postgr.es/c/42ffdedcf)
  [§](https://postgr.es/c/477efef08)

  與 `--schema` 等其他選擇性還原選項
  合併使用時，這些選項未能還原
  預期的項目，與 pg_dump 搭配
  類似選項時的行為不同。
* 修正 `vacuumdb --missing-stats-only`，使其忽略
  分割的運算式索引 (Baji Shaik)
  [§](https://postgr.es/c/7e085aabd)

  先前，vacuumdb 一律會嘗試
  對分割資料表執行 `ANALYZE`，但這沒有任何作用，
  因為統計資訊從不會為分割索引建立，
  只會為其葉索引建立。
* 在 `contrib/amcheck` 中，修正未能回報
  btree 中繼頁面 `allequalimage`
  旗標損毀的問題 (Chao Li)
  [§](https://postgr.es/c/12c32bbc8)
* 在 `contrib/amcheck` 中，修正驗證 GIN 索引時
  在查詢生命週期內的記憶體洩漏 (Kirill Reshke)
  [§](https://postgr.es/c/1f8ab91c1)
* 在 `contrib/amcheck` 中，正確處理短標頭的 varlena
  datum (Andrey Borodin)
  [§](https://postgr.es/c/897e79486)

  此錯誤可能導致驗證 btree
  索引時做了多餘的工作，但似乎沒有造成更嚴重的後果。
* 在 `contrib/btree_gist` 中，
  修正 `float4`
  與 `float8` 運算子類別對 `NaN` 的處理 (Bill Kim, Tom Lane)
  [§](https://postgr.es/c/1e1d07792)

  比較以及 GiST penalty 與距離函式都
  沒有考慮到 `NaN`，遇到它時會給出錯誤的
  結果。若浮點數欄位中有可能存在
  `NaN` 項目，建議在
  安裝此更新後，重建這些欄位上的 `btree_gist` 索引。
* 在 `contrib/btree_gist` 中，修正 GiST 索引
  建構期間 `bit`/`varbit` 項目的排序
  (Tom Lane)
  [§](https://postgr.es/c/558c4ea9a)

  bit 型別的值被當作
  `bytea` 來排序，這雖然沒有造成任何明顯的失敗，
  但由於兩者的內部表示方式不同，會產生效率不佳的索引。
  建議在安裝此更新後，
  重建 bit 欄位上的 `btree_gist` 索引。
* 在 `contrib/btree_gist` 中，修正使用
  不等於運算子的搜尋 (Ayush Tiwari)
  [§](https://postgr.es/c/12c519207)

  對於變動長度資料型別，掃描非葉索引
  頁面的程式碼套用了錯誤的比較函式，導致錯誤的
  結果，甚至可能當機。
* 在 `contrib/dblink`
  與 `contrib/postgres_fdw` 中，確保使用者對應
  的 `use_scram_passthrough` 設定會覆寫
  外部伺服器的設定 (Matheus Alcantara)
  [§](https://postgr.es/c/88d7748d2)
  [§](https://postgr.es/c/130396e6c)

  先前的優先順序正好相反，但這與
  其他外部資料表選項的行為不一致。
* 拒絕在 `contrib/dblink` 外部資料包裝器上
  設定 `use_scram_passthrough`
  (Matheus Alcantara)
  [§](https://postgr.es/c/cd777e27e)

  此選項只在外部伺服器與使用者
  對應上有意義，但 dblink 錯誤地也允許在 FDW 層級
  設定它（然後將其忽略）。
* 修正
  `contrib/hstore_plperl`、
  `contrib/jsonb_plperl` 與
  `contrib/jsonb_plpython` 中
  未受防護的遞迴與迴圈
  (Aleksander Alekseev)
  [§](https://postgr.es/c/e3b7a43fa)
  [§](https://postgr.es/c/d65cf6f80)

  防止處理深層
  巢狀的 `jsonb` 值時發生堆疊溢位，並允許中斷
  嘗試解參考循環的 Perl 物件參照鏈時
  所造成的無窮迴圈。
* 修正 `contrib/intarray` 中
  遺漏釋放統計資訊 catcache 項目的問題 (Man Zeng)
  [§](https://postgr.es/c/e7544c518)

  這個疏漏會導致類似“resource was not closed: cache pg_statistic”的警告。
* 在 `contrib/ltree` 中，修正比較時的
  整數溢位 (Ayush Tiwari)
  [§](https://postgr.es/c/c3e36a9a5)

  包含超過約 14,653 個標籤的 `ltree` 值
  會因溢位而產生錯誤的比較結果。若 btree
  索引包含這樣的值，它很可能已經損毀，應在
  安裝此更新後重建索引。
* 在 `contrib/pgcrypto` 中，避免使用 OSSLCipher 物件時
  遇到錯誤後發生重複釋放當機
  (Yuelin Wang)
  [§](https://postgr.es/c/020426268)
* 修正 `contrib/pg_prewarm` 的 autoprewarm 工作程序中
  的越界存取
  (Matheus Alcantara)
  [§](https://postgr.es/c/3bf2cb225)

  這段程式碼嘗試從陣列結尾之後的一個位置擷取值，
  有發生 segfault 的風險。
* 修正 `contrib/pg_surgery` 的
  `heap_force_kill` 與
  `heap_force_freeze` 函式中的陣列溢位 (Michael Paquier)
  [§](https://postgr.es/c/2b09f8a91)

  嘗試變更偏移編號等於
  MaxHeapTuplesPerPage 的 TID 時，會寫入超過所配置
  陣列結尾一個位元組的位置，可能使伺服器當機。
* 在 `contrib/pg_surgery` 中，避免 TID 陣列
  元素超過 64K 個時發生無窮迴圈 (Andrey Rachitskiy)
  [§](https://postgr.es/c/19f0391df)
* 避免 `contrib/refint` 的
  `check_foreign_key()` 中的 NULL 指標解參考 (Ayush Tiwari)
  [§](https://postgr.es/c/ed0c4d5af)

  在 on-update-cascade 的情況下，被參照欄位的 null 值
  會導致當機。這是 CVE-2026-6637 修正中的疏漏，
  但在那之前的程式碼其實也不完全正確。
* 修正 `contrib/seg`，使其正確輸出
  帶有 `~` 確定性指示符的線段
  (Ewan Young)
  [§](https://postgr.es/c/0004cab4d)

  由於一個筆誤，`seg_out()` 不會輸出
  附加在線段上界的 `~` 確定性指示符。
  更糟的是，若下界
  帶有 `~` 而上界沒有指示符，
  上界就完全不會被輸出，錯誤地將
  該值轉換為開區間。
* 修正 `contrib/xml2` 的
  `xpath_nodeset()` 函式處理命名空間節點時的當機 (Andrey Chernyy,
  Michael Paquier)
  [§](https://postgr.es/c/91b57eade)
* 支援以 OpenSSL 4 建置
  PostgreSQL (Daniel Gustafsson)
  [§](https://postgr.es/c/27cf3b5af)
* 將時區資料檔案更新為 tzdata
  2026c 版 (Tom Lane)
  [§](https://postgr.es/c/5f67124fa)

  Alberta（America/Edmonton）將自 2026 年 11 月起全年使用 UTC-06
  （實際上即永久日光節約時間）。此
  版本假設其時區縮寫自那時起將
  為 `CST`。這看來很可能會
  改變，但目前尚不清楚會使用什麼新的縮寫。

  摩洛哥（Africa/Casablanca）將於 2026-09-20 改為永久使用 UTC+00，
  不再有日光節約時間的轉換。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release-18-6.html)（原文版本：18.6；核對日期：2026-10-22）
