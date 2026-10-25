<a id="CUSTOM-SCAN-PLAN"></a>

## 60.2. 建立自訂掃描計畫 [#](#custom-scan-plan) <a href="#custom-scan-plan" id="custom-scan-plan"></a>

[60.2.1. 自訂掃描計畫回呼函式](custom-scan-plan.md#CUSTOM-SCAN-PLAN-CALLBACKS)

自訂掃描在完成的計畫樹中以下列結構表示：

```

typedef struct CustomScan
{
    Scan      scan;
    uint32    flags;
    List     *custom_plans;
    List     *custom_exprs;
    List     *custom_private;
    List     *custom_scan_tlist;
    Bitmapset *custom_relids;
    const CustomScanMethods *methods;
} CustomScan;
```

`scan` 必須像其他任何掃描一樣初始化，包括估計成本、目標清單、條件（qualifications）等等。`flags` 是位元遮罩，其意義與 `CustomPath` 中的相同。`custom_plans` 可以用來儲存子 `Plan` 節點。`custom_exprs` 應該用來儲存需要由 `setrefs.c` 與 `subselect.c` 修正的運算式樹，而 `custom_private` 應該用來儲存只有自訂掃描提供者本身會使用的其他私有資料。掃描基礎關聯時，`custom_scan_tlist` 可以為 NIL，表示自訂掃描傳回的掃描元組（tuple）符合基礎關聯的資料列型別。否則，它是描述實際掃描元組的目標清單。對於連接，必須提供 `custom_scan_tlist`；如果自訂掃描提供者能計算某些非 Var 的運算式，掃描時也可以提供它。`custom_relids` 由核心程式碼設定為此掃描節點所處理的關聯集合（範圍表索引）；除非此掃描是在取代連接，否則它只會有一個成員。`methods` 必須指向一個實作所需自訂掃描方法的物件（通常是靜態配置的），這些方法將在下文進一步詳述。

當 `CustomScan` 掃描單一關聯時，`scan.scanrelid` 必須是要掃描之資料表的範圍表索引。當它取代連接時，`scan.scanrelid` 應該為零。

計畫樹必須能夠使用 `copyObject` 複製，因此儲存在「custom」欄位中的所有資料，都必須由該函式能夠處理的節點組成。此外，自訂掃描提供者不能用嵌入了 `CustomScan` 的較大結構來取代該結構本身；而對於 `CustomPath` 或 `CustomScanState`，這樣做是可行的。

<a id="CUSTOM-SCAN-PLAN-CALLBACKS"></a>

### 60.2.1. 自訂掃描計畫回呼函式 [#](#CUSTOM-SCAN-PLAN-CALLBACKS)

```

Node *(*CreateCustomScanState) (CustomScan *cscan);
```

為此 `CustomScan` 配置一個 `CustomScanState`。實際配置的大小通常會大於一般 `CustomScanState` 所需，因為許多提供者會希望將它嵌入為某個較大結構的第一個欄位。傳回的值必須適當設定節點標記與 `methods`，但其他欄位在此階段應該保持為零；在 `ExecInitCustomScan` 執行基本初始化之後，會呼叫 `BeginCustomScan` 回呼函式，讓自訂掃描提供者有機會進行其他所需的任何工作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/custom-scan-plan.html)（原文版本：18.6；核對日期：2026-10-17）
