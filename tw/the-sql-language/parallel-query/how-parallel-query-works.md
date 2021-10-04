# 15.1. 如何運作？

當優化器確定平行查詢是某個查詢的最快執行策略時，它將建立一個查詢計劃，其中包含一個 Gather 或 Gather Merge 節點。這是一個簡單的例子：

```text
EXPLAIN SELECT * FROM pgbench_accounts WHERE filler LIKE '%x%';
                                     QUERY PLAN                                      
-------------------------------------------------------------------------------------
 Gather  (cost=1000.00..217018.43 rows=1 width=97)
   Workers Planned: 2
   ->  Parallel Seq Scan on pgbench_accounts  (cost=0.00..216018.33 rows=1 width=97)
         Filter: (filler ~~ '%x%'::text)
(4 rows)
```

在所有情況下，Gather 或 Gather Merge 合併節點都只有一個子計劃，它是平行執行計劃的一部分。如果 Gather 或 Gather Merge 節點位於計劃樹的頂部，則整個查詢將會平行執行。如果它在計劃樹中的其他位置，那麼只有它下面的計劃部分將平行運行。在上面的範例中，查詢只存取一個資料表，因此除了 Gather 節點本身之外，只有一個計劃節點；由於該計劃節點是 Gather 節點的子節點，因此它將平行運行。

[使用 EXPLAIN](../performance-tips/using-explain.md)，您可以看到規劃器選擇的後端程序數量。當在查詢執行過程中到達 Gather 節點時，執行使用者連線的程序將請求與規劃器選擇的背景程序數量相等的[背景工作程序](../../server-programming/background-worker-processes.md)。規劃器將考慮使用的背景工作程序數量最多限制為 max\_parallel\_workers\_per\_gather。任何時候可以存在的背景工作程序總數受 max\_worker\_processes 和 max\_parallel\_workers 限制。因此，平行查詢可以用比計劃更少的工作程序運行，甚至根本不需要工作程序。最佳計劃可能取決於可用的工作程序數量，因此這可能會導致查詢性能較差。如果頻繁發生，請考慮增加 max\_worker\_processes 和 max\_parallel\_workers，以便可以同時運行更多工作程序，或者減少 max\_parallel\_workers\_per\_gather，以便規劃器請求更少的工作程序。

為給予的平行查詢成功啟動的每個背景工作程序都將執行計劃的平行部分。領導程序也會執行計劃的一部分，但它還有一個額外的責任：它還必須讀取其他後諯程序所生成的所有資料。當計劃的平行處理部分只産生少量資料時，領導程序通常會表現得非常像一個額外的背景程序，而加快了查詢的執行速度。相反地，當計劃的平行處理部分産生大量資料時，領導程序可能幾乎完全被讀取由背景程序産生的資料所佔據，並且執行 Gather 節點級之上的計劃節點所需的任何進一步處理步驟或是扮演 Gather Merge 節點。在這種情況下，領導程序將會少量執行計劃的平行部分。

當計劃的平行部分頂部的節點是 Gather Merge 而不是 Gather 時，它表示執行計劃的平行部分的每個程序正在按排序順序産生資料，並且領導程序正依序執行保持合併。相反地，Gather 只以便利的順序讀取後端程序的資料，會破壞可能存在的任何排序順序。

