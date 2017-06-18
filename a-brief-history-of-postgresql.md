# 2. PostgreSQL沿革[^1]

PostgreSQL目前為眾所皆知的物件導向的關連式資料庫管理系統，其由美國加州伯克萊大學所研發的POSTGRES衍生而成。經過超過二十年以上的演進，PostgreSQL現在是世界上最先進的開源資料庫系統。

### 2.1. 伯克萊大學POSTGRES專案

POSTGRES專案是由Michael Stonebraker教授領導的團隊進行研發，其受到Defense Advanced Research Projects Agency \(DARPA\)，the Army Research Office \(ARO\)，the National Science Foundation \(NSF\),及ESL, Inc的贊助。POSTGRES專案始於1986年，最原始的設計，＂The design of POSTGRES＂[^2]，作為開端，其最初的資料結構模型則揭露於＂The POSTGRES data model＂[^3]。規則系統設計發表於＂The design of the POSTGRES rules system＂[^4]，而當時的關連式資料儲存的架構則刊載於＂The design of the POSTGRES storage system＂[^5]。

POSTGRES接下進行了幾次重大的變革。第一代的＂demoware＂在1987年真的實作成為可用的系統，並在1988年的ACM-SIGMOD研討會中進行展示，並在1989年6月，釋出了第1版可供外部使用者使用的資料庫系統[^6]。為了回應當時使用者對於第一代規則系統的批評[^7]，其規則系統重新進行設計[^8]，並在隔年1990年的6月份，隨即推出第2版系統，搭載新的規則系統設計。第3版系統則於1991年發表，新增支援多重儲存管理機制，改善查詢處理器，並又改寫了規則系統。如此直到Postgres 95誕生之前，主要都專注於移植性及可信賴度的發展。

POSTGRES接下來開始被運用在許多不同的研究和產品上，財務資料分析系統、噴氣引擎效能監控系統、小行星追蹤資料庫、醫療資訊系統、以及數個地理資訊系統。POSTGRES也被好幾所大學用於其教學工具。最後，由Illustra Information Technologies（後來併入[Informix](http://www.informix.com/)，而Informix目前為[IBM](http://www.ibm.com/)所擁有）技術移轉，並將其商業化。於1992年末，POSTGRES成為[Sequoia 2000 scientific computing project](http://meteora.ucsd.edu/s2k/s2k_home.html)主要的資料管理系統。

在1993年間，用戶數量呈現倍數成長，伴隨而來的是大量的程式碼維護與服務支援，占去絕大部份原來應該進行研究的時間。為了減少維運的負擔，伯克萊的POSTGRES專案正式終止於4.2版。

### 2.2. Postgres 95

1994年，Andrew Yu和Jolly Chen在POSTGRES增加了SQL語法的直譯器，並且以新的Postgres 95為名，在網路上開放讓全世界的人使用。他們成為伯克萊POSTGRES原始碼最初的繼承者。

Postgres 95的程式碼是完全以ANSI C開發，並且輕量化了25%。許多內部的改良增進了效率及可維護性。當時Wisconsin Benchmark進行測試，Postgres 95在1.0.x時的效能比原始的POSTGRES 4.2快了約30%至50%。除了一些錯誤修正之外，還有下面這些主要的改良：

* 原有的PostQUEL以SQL（實作於伺服器端）所取代。（連接介面在PostQUEL之後便採libpq函式庫）
  子查詢一直到PostgreSQL出現之前都還未支援，但在Postgres 95便已能使用自訂的SQL函數，聚合函數Aggregate function則被重新實作。GROUP BY查詢語句也在此時被加入。

* 新的工具psql可進行互動式的SQL操作，其採用的是GNU Readline的技術。psql開始大量取代老舊的管理工具。

* 新的前端函式庫，libpgtcl，支援Tcl-based用戶端程式。還有一個簡易的命令列介面工具pgtclsh，使用新的Tcl命令和Postgres 95伺服器進行操作。

* 重新改寫了large-object處理的交換介面，僅使inversion作為儲存大型物件的唯一機制。（inversion檔案系統就此移除）

* Instance-level的規則系統被淘汰了，但其規則仍用於重構規則所使用。

* 製作了一個簡短的說明，介紹標準的SQL功能，並隨Postgres 95原始碼發佈。

* 使用GNU make（取代BSD make）編譯程式碼，Postgres 95也支援使用未修正的GCC編譯器（修正高精度資料對齊問題）。

### 2.3. PostgreSQL

1996年，＂Postgres 95＂這個名稱很明顯不再適合。我們選擇了新的名稱，PostgreSQL，其呈現出與原始POSTGRES之間的源由，也彰顯了結合SQL力量的意義。同時，我們設定其版本由6.0開始，重回伯克萊POSTGRES專案的版號序列。

許多人持續使用＂Postgres＂（現在已經很少使用全大寫字母表現）來代表PostgreSQL，是因為傳統，也可能是因為比較好發音。這樣的用法也廣為用於暱稱或別名。

Postgres 95的發展主要在於瞭解及定義伺服器程式既有的問題，而PostgreSQL則更重視系統的能力與爭議性的功能上，不過所有的工作是全面性的。

更多有關於PostgreSQL的發展，請參閱附錄E。



[^1]: [PostgreSQL: Documentation: 10: 2. A Brief History of PostgreSQL](https://www.postgresql.org/docs/10/static/history.html)

[^2]: “[The design of POSTGRES](http://db.cs.berkeley.edu/papers/ERL-M85-95.pdf)”. M. Stonebraker and L. Rowe. ACM-SIGMOD Conference on Management of Data, May 1986.

[^3]: “[The POSTGRES data model](http://db.cs.berkeley.edu/papers/ERL-M87-13.pdf)”. L. Rowe and M. Stonebraker. VLDB Conference, Sept. 1987.

[^4]: “The design of the POSTGRES rules system”. M. Stonebraker, E. Hanson, and C. H. Hong. IEEE Conference on Data Engineering, Feb. 1987.

[^5]: “[The design of the POSTGRES storage system](http://db.cs.berkeley.edu/papers/ERL-M87-06.pdf)”. M. Stonebraker. VLDB Conference, Sept. 1987.

[^6]: “[The implementation of POSTGRES](http://db.cs.berkeley.edu/papers/ERL-M90-34.pdf)”. M. Stonebraker, L. A. Rowe, and M. Hirohama. Transactions on Knowledge and Data Engineering 2\(1\). IEEE. March 1990.

[^7]: “[A commentary on the POSTGRES rules system](http://db.cs.berkeley.edu/papers/ERL-M89-82.pdf)”. M. Stonebraker, M. Hearst, and S. Potamianos. SIGMOD Record 18\(3\). Sept. 1989.

[^8]: “[On Rules, Procedures, Caching and Views in Database Systems](http://db.cs.berkeley.edu/papers/ERL-M90-36.pdf)”. M. Stonebraker, A. Jhingran, J. Goh, and S. Potamianos. ACM-SIGMOD Conference on Management of Data, June 1990.

