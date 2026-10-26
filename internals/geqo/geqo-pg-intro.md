<a id="GEQO-PG-INTRO"></a>

## 61.3. PostgreSQL 中的遺傳式查詢最佳化（GEQO） [#](#geqo-pg-intro) <a href="#geqo-pg-intro" id="geqo-pg-intro"></a>

[61.3.1. 以 GEQO 產生可能的計畫](geqo-pg-intro.md#geqo-pg-intro-gen-possible-plans)

[61.3.2. PostgreSQL GEQO 未來的實作工作](geqo-pg-intro.md#geqo-future)

GEQO 模組把查詢最佳化問題當作知名的旅行推銷員問題（TSP）來處理。
可能的查詢計畫被編碼為整數字串。每個字串
代表查詢中從一個關聯到下一個關聯的連接順序。
例如，以下連接樹

```

   /\
  /\ 2
 /\ 3
4  1
```

被編碼為整數字串 '4-1-3-2'，
意思是先連接關聯 '4' 與 '1'，接著連接 '3'，
然後是 '2'，其中 1、2、3、4 是
PostgreSQL 最佳化器內部的關聯 ID。

PostgreSQL 中 GEQO
實作的具體特性
如下：

* 使用*穩態*（steady state）GA（替換族群中適應度最低的
  個體，而非整個世代替換），
  可以快速收斂到更好的查詢計畫。這對於
  在合理時間內完成查詢處理是不可或缺的；
* 使用*邊重組交配*（edge recombination crossover），
  它特別適合在以
  GA 求解 TSP 時
  讓邊的損失保持在低水準；
* 突變作為遺傳運算子已被棄用，因此不需要修復
  機制來產生合法的 TSP 路徑。

GEQO 模組的部分內容改編自 D. Whitley 的
Genitor 演算法。

GEQO 模組讓
PostgreSQL 查詢最佳化器能夠
透過非窮舉式搜尋，有效地支援大型連接查詢。

<a id="GEQO-PG-INTRO-GEN-POSSIBLE-PLANS"></a>

### 61.3.1. 以 GEQO 產生可能的計畫 [#](#geqo-pg-intro-gen-possible-plans) <a href="#geqo-pg-intro-gen-possible-plans" id="geqo-pg-intro-gen-possible-plans"></a>

GEQO 規劃過程使用標準的規劃器
程式碼來產生個別關聯的掃描計畫。接著再以遺傳方法
發展連接計畫。如上所示，每個
候選連接計畫都以連接基礎關聯的順序來表示。在初始階段，GEQO
程式碼只是隨機產生一些可能的連接順序。對於
所考慮的每個連接順序，都會呼叫標準規劃器程式碼，
估算以該連接順序執行查詢的成本。
（對於連接順序的每一步，都會考慮全部三種可能的連接策略；
而且所有最初決定的關聯掃描計畫
都可以使用。估算成本是這些
可能性中最便宜的一個。）估算成本較低的連接順序被視為
比成本較高者「更適應」。遺傳演算法
會捨棄適應度最低的候選者。接著透過
組合適應度較高之候選者的基因來產生新的候選者 — 也就是使用
已知低成本連接順序中隨機選取的部分，來建立
新的順序以供考慮。此過程會反覆進行，直到
考慮過預設數量的連接順序為止；然後使用搜尋過程中
任何時間點找到的最佳順序來產生最終的
計畫。

由於在初始族群選擇以及隨後對最佳候選者的
「突變」中都會做出隨機選擇，此過程本質上是非確定性的。為了避免
所選計畫出現令人意外的變化，GEQO 演算法每次執行時都會以目前的 [geqo_seed](../../server-administration/runtime-config/runtime-config-query.md#GUC-GEQO-SEED)
參數設定重新啟動其亂數產生器。只要 `geqo_seed` 與其他
GEQO 參數保持固定，對於給定的查詢
（以及統計資訊等其他規劃器輸入）就會產生相同的計畫。若要嘗試
不同的搜尋路徑，可以試著變更 `geqo_seed`。

<a id="GEQO-FUTURE"></a>

### 61.3.2. PostgreSQL GEQO 未來的實作工作 [#](#geqo-future) <a href="#geqo-future" id="geqo-future"></a>

遺傳演算法的參數設定仍有待改進。
在檔案 `src/backend/optimizer/geqo/geqo_main.c` 的
常式
`gimme_pool_size` 與 `gimme_number_generations` 中，
我們必須在參數設定上找到折衷，
以滿足兩個相互競爭的需求：

* 查詢計畫的最佳性
* 計算時間

在目前的實作中，每個候選連接
順序的適應度，是透過從頭執行標準規劃器的連接選擇
與成本估算程式碼來估算的。只要不同的
候選者使用相似的連接子序列，就會有大量工作
被重複執行。若保留子連接的成本估算，
速度可以大幅提升。問題在於要避免為了保留這些狀態
而耗用不合理的記憶體量。

從更根本的層面來看，用為 TSP 設計的 GA 演算法來解決查詢最佳化
是否恰當，並不明確。在 TSP 的情況下，
任何子字串（部分路徑）的相關成本與路徑的其餘部分無關，
但對查詢最佳化而言，這顯然不成立。
因此，邊重組交配是否為最有效的突變程序，
是值得懷疑的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/geqo-pg-intro.html)（原文版本：18.6；核對日期：2026-10-17）
