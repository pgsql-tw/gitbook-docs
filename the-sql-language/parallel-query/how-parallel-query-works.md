<a id="HOW-PARALLEL-QUERY-WORKS"></a>

## 15.1. 平行查詢的運作方式 [#](#HOW-PARALLEL-QUERY-WORKS)

當最佳化器判定平行查詢是某個查詢最快的執行策略時，它會建立一個包含 *Gather* 或 *Gather Merge* 節點的查詢計畫。以下是一個簡單的範例：

```

EXPLAIN SELECT * FROM pgbench_accounts WHERE filler LIKE '%x%';
                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Gather  (cost=1000.00..217018.43 rows=1 width=97)
   Workers Planned: 2
   ->  Parallel Seq Scan on pgbench_accounts  (cost=0.00..216018.33 rows=1 width=97)
         Filter: (filler ~~ '%x%'::text)
(4 rows)
```

在所有情況下，`Gather` 或 `Gather Merge` 節點都恰好有一個子計畫，也就是將會平行執行的那一部分計畫。如果 `Gather` 或 `Gather Merge` 節點位於計畫樹的最頂端，整個查詢就會平行執行。如果它位於計畫樹中的其他位置，則只有它下方的那部分計畫會平行執行。在上面的範例中，查詢只存取一個資料表，因此除了 `Gather` 節點本身之外只有一個計畫節點；由於該計畫節點是 `Gather` 節點的子節點，它會平行執行。

[使用 EXPLAIN](../performance-tips/using-explain.md) 可以看到規劃器所選擇的工作程序（worker）數量。在查詢執行期間到達 `Gather` 節點時，負責執行使用者工作階段的程序會要求與規劃器所選工作程序數量相同的[背景工作程序](../../server-programming/bgworker/README.md)。規劃器會考慮使用的背景工作程序數量，最多受 [max_parallel_workers_per_gather](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER) 限制。任何時刻可以存在的背景工作程序總數，則同時受 [max_worker_processes](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 與 [max_parallel_workers](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS) 限制。因此，平行查詢有可能以少於計畫數量的工作程序執行，甚至完全沒有工作程序。最佳計畫可能取決於可用的工作程序數量，因此這可能導致查詢效能不佳。如果這種情況經常發生，可以考慮增加 `max_worker_processes` 與 `max_parallel_workers`，讓更多工作程序能夠同時執行；或者降低 `max_parallel_workers_per_gather`，讓規劃器要求較少的工作程序。

為某個平行查詢成功啟動的每個背景工作程序，都會執行計畫的平行部分。領導程序（leader）也會執行計畫的那一部分，但它還有一項額外的職責：它也必須讀取工作程序所產生的所有 tuple。當計畫的平行部分只產生少量 tuple 時，領導程序的行為通常就像是多了一個工作程序，可以加快查詢的執行。反過來說，當計畫的平行部分產生大量 tuple 時，領導程序可能幾乎完全忙於讀取工作程序所產生的 tuple，以及執行 `Gather` 節點或 `Gather Merge` 節點以上層級的計畫節點所需的任何後續處理步驟。在這種情況下，領導程序只會執行計畫平行部分中很少的工作。

當計畫平行部分最頂端的節點是 `Gather Merge` 而不是 `Gather` 時，表示執行計畫平行部分的每個程序都以排序好的順序產生 tuple，而領導程序正在進行保留順序的合併。相較之下，`Gather` 會以任何方便的順序從工作程序讀取 tuple，因而破壞原本可能存在的任何排序順序。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/how-parallel-query-works.html)（原文版本：18.6；核對日期：2026-09-11）
