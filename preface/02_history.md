# 2. PostgreSQL 沿革

現在被稱為 PostgreSQL 的物件關聯式資料庫管理系統，是根據美國加州伯克萊大學所研發的 POSTGRES 衍生而成。經過超過二十年以上的演進，PostgreSQL 現在是世界上最先進的開源資料庫系統。

## 2.1. 伯克萊大學 POSTGRES 專案

POSTGRES 專案是由 Michael Stonebraker 教授領導的團隊進行研發，由美國國防高等研究計劃署（DARPA, Defense Advanced Research Projects Agency）、美國陸軍研究辦公室（ARO, the Army Research Office）、美國國家科學基金會（NSF, the National Science Foundation）及美國電磁系統實驗室（ESL, Inc）所贊助。POSTGRES 專案始於 1986 年，最原始的設計，＂The design of POSTGRES＂，作為開端，其最初的資料結構模型則揭露於＂The POSTGRES data model＂。規則系統設計發表於＂The design of the POSTGRES rules system＂，而當時的關連式資料儲存的架構則刊載於＂The design of the POSTGRES storage system＂。

POSTGRES 接下進行了幾次重大的變革。第一代的＂demoware＂在 1987 年真的實作成為可用的系統，並在 1988 年的 ACM-SIGMOD 研討會中進行展示，並在 1989 年六月，釋出了第一版可供外部使用者使用的資料庫系統。為了回應當時使用者對於第一代規則系統的批評，其規則系統重新進行設計，並在隔年 1990 年的六月份，隨即推出第二版系統，搭載新的規則系統設計。第三版系統則於 1991 年發表，新增支援多重儲存管理機制，改善查詢處理器，並又改寫了規則系統。如此直到 Postgres 95 誕生之前，主要都專注於移植性及可信賴度的發展。

POSTGRES 接下來開始被運用在許多不同的研究和產品上，財務資料分析系統、噴氣引擎效能監控系統、小行星追蹤資料庫、醫療資訊系統、以及數個地理資訊系統。POSTGRES 也被好幾所大學用於其教學工具。最後，由 Illustra Information Technologies（後來併入 [Informix](http://www.informix.com/)，而 Informix 目前為 [IBM](http://www.ibm.com/) 所擁有）技術移轉，並將其商業化。於 1992 年末，POSTGRES 成為 [Sequoia 2000 scientific computing project](http://meteora.ucsd.edu/s2k/s2k\_home.html) 主要的資料管理系統。

在 1993 年間，用戶數量呈現倍數成長，伴隨而來的是大量的程式碼維護與服務支援，占去絕大部份原來應該進行研究的時間。為了減少維運的負擔，伯克萊的 POSTGRES 專案正式終止於 4.2 版。

## 2.2. Postgres95

1994年，Andrew Yu 和 Jolly Chen 在 POSTGRES 增加了 SQL 語法的直譯器，並且以新的 Postgres95 為名，在網路上開放讓全世界的人使用，他們成為伯克萊 POSTGRES 原始碼最初的繼承者。

Postgres95 的程式碼是完全以 ANSI C 開發，並且輕量化了 25%。許多內部的改良增進了效率及可維護性。當時 Wisconsin Benchmark 進行測試，Postgres95 在 1.0.x 時的效能比原始的 POSTGRES 4.2 快了約 30% 至 50%。除了一些錯誤修正之外，還有下面這些主要的改良：

* 原有的 PostQUEL 以 SQL（實作於伺服器端）所取代。（連接介面在 PostQUEL 之後便採 [libpq](https://www.postgresql.org/docs/current/libpq.html) 函式庫）子查詢一直到 PostgreSQL 出現之前都還未支援，但在 Postgres95 便已能使用自訂的 SQL 函數，聚合函數 Aggregate function 則被重新實作。`GROUP BY` 查詢語句也在此時被加入。
* 提供新的工具 `psql` 可進行互動式的 SQL 操作，採用的是 GNU Readline 的技術，大量地取代了老舊的管理工具。
* 提供新的前端函式庫 `libpgtcl`，支援 Tcl-based 用戶端程式。還有一個簡易的 shell 接口 `pgtclsh`，使用新的 Tcl 命令來和 Postgres95 伺服器進行操作。
* 重新改寫了大型物件的交換介面，只保留大型物件翻轉（inversion）作為儲存大型物件的唯一機制。（移除了 inversion 檔案系統）
* 淘汰了實例層級（instance-level）的規則系統，但其規則仍用於重構規則所使用。
* 製作了一個簡短的說明，介紹標準的 SQL 功能，並隨 Postgres95 原始碼發佈。
* 使用 GNU make（取代 BSD make）來編譯程式碼。除此之外，Postgres95 也支援使用未修正的 GCC 編譯器（修正高精度資料對齊問題）。

## 2.3. PostgreSQL

1996 年，「Postgres95」這個名稱很明顯不再適合。於是我們選擇了新的名稱「PostgreSQL」來呈現出與原始 POSTGRES 之間的源由，也彰顯了結合 SQL 力量的意義。同時，我們設定其版本由 6.0 開始，重回伯克萊 POSTGRES 專案的版號序列。

許多人持續使用「Postgres」（現在已經很少使用全大寫字母表現）來代表 PostgreSQL，是因為傳統，也可能是因為比較好發音。這樣的用法也廣為用於暱稱或別名。

Postgres95 的發展主要在於瞭解及定義伺服器程式既有的問題，而 PostgreSQL 則更重視系統的能力與爭議性的功能上，不過所有的工作是全面性的。

更多有關於 PostgreSQL 的發展，請參閱 [附錄 E](https://www.postgresql.org/docs/current/release.html)。
