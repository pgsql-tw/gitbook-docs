<a id="CUSTOM-SCAN-EXECUTION"></a>

## 60.3. 執行自訂掃描 [#](#custom-scan-execution) <a href="#custom-scan-execution" id="custom-scan-execution"></a>

[60.3.1. 自訂掃描執行回呼函式](custom-scan-execution.md#CUSTOM-SCAN-EXECUTION-CALLBACKS)

執行 `CustomScan` 時，它的執行狀態以 `CustomScanState` 表示，其宣告如下：

```

typedef struct CustomScanState
{
    ScanState ss;
    uint32    flags;
    const CustomExecMethods *methods;
} CustomScanState;
```

`ss` 會像其他任何掃描狀態一樣初始化，只是如果掃描的對象是連接而不是基礎關聯，`ss.ss_currentRelation` 會保持為 NULL。`flags` 是位元遮罩，其意義與 `CustomPath` 和 `CustomScan` 中的相同。`methods` 必須指向一個實作所需自訂掃描狀態方法的物件（通常是靜態配置的），這些方法將在下文進一步詳述。通常，`CustomScanState`（它不需要支援 `copyObject`）實際上會是一個較大的結構，並將上述結構嵌入為其第一個成員。

<a id="CUSTOM-SCAN-EXECUTION-CALLBACKS"></a>

### 60.3.1. 自訂掃描執行回呼函式 [#](#CUSTOM-SCAN-EXECUTION-CALLBACKS)

```

void (*BeginCustomScan) (CustomScanState *node,
                         EState *estate,
                         int eflags);
```

完成所提供之 `CustomScanState` 的初始化。標準欄位已經由 `ExecInitCustomScan` 初始化，但任何私有欄位都應該在此初始化。

```

TupleTableSlot *(*ExecCustomScan) (CustomScanState *node);
```

擷取下一個掃描元組（tuple）。如果還有剩餘的元組，它應該以目前掃描方向上的下一個元組填入 `ps_ResultTupleSlot`，然後傳回該元組槽（tuple slot）。如果沒有，則應該傳回 `NULL` 或空的元組槽。

```

void (*EndCustomScan) (CustomScanState *node);
```

清理與 `CustomScanState` 相關聯的任何私有資料。此方法為必要，但如果沒有相關聯的資料，或者資料會被自動清理，它就不需要做任何事。

```

void (*ReScanCustomScan) (CustomScanState *node);
```

將目前的掃描倒回開頭，並準備重新掃描該關聯。

```

void (*MarkPosCustomScan) (CustomScanState *node);
```

儲存目前的掃描位置，以便之後能由 `RestrPosCustomScan` 回呼函式還原。此回呼函式為選用，只有在設定了 `CUSTOMPATH_SUPPORT_MARK_RESTORE` 旗標時才需要提供。

```

void (*RestrPosCustomScan) (CustomScanState *node);
```

還原先前由 `MarkPosCustomScan` 回呼函式所儲存的掃描位置。此回呼函式為選用，只有在設定了 `CUSTOMPATH_SUPPORT_MARK_RESTORE` 旗標時才需要提供。

```

Size (*EstimateDSMCustomScan) (CustomScanState *node,
                               ParallelContext *pcxt);
```

估計平行作業所需的動態共享記憶體數量。估計值可以高於實際使用量，但不得低於實際使用量。傳回值以位元組為單位。此回呼函式為選用，只有在此自訂掃描提供者支援平行執行時才需要提供。

```

void (*InitializeDSMCustomScan) (CustomScanState *node,
                                 ParallelContext *pcxt,
                                 void *coordinate);
```

初始化平行作業所需的動態共享記憶體。`coordinate` 指向一塊共享記憶體區域，其大小等於 `EstimateDSMCustomScan` 的傳回值。此回呼函式為選用，只有在此自訂掃描提供者支援平行執行時才需要提供。

```

void (*ReInitializeDSMCustomScan) (CustomScanState *node,
                                   ParallelContext *pcxt,
                                   void *coordinate);
```

當自訂掃描計畫節點即將被重新掃描時，重新初始化平行作業所需的動態共享記憶體。此回呼函式為選用，只有在此自訂掃描提供者支援平行執行時才需要提供。建議的做法是：此回呼函式只重設共享狀態，而 `ReScanCustomScan` 回呼函式只重設本地狀態。目前此回呼函式會在 `ReScanCustomScan` 之前被呼叫，但最好不要依賴這個順序。

```

void (*InitializeWorkerCustomScan) (CustomScanState *node,
                                    shm_toc *toc,
                                    void *coordinate);
```

依據領導程序在 `InitializeDSMCustomScan` 期間所設定的共享狀態，初始化平行工作程序的本地狀態。此回呼函式為選用，只有在此自訂掃描提供者支援平行執行時才需要提供。

```

void (*ShutdownCustomScan) (CustomScanState *node);
```

在預期該節點不會被執行到完成時釋放資源。並非所有情況都會呼叫此函式；有時候，`EndCustomScan` 可能會在未先呼叫此函式的情況下被呼叫。由於平行查詢所使用的 DSM 區段會在此回呼函式被呼叫後隨即銷毀，希望在 DSM 區段消失之前採取某些動作的自訂掃描提供者，應該實作此方法。

```

void (*ExplainCustomScan) (CustomScanState *node,
                           List *ancestors,
                           ExplainState *es);
```

為自訂掃描計畫節點的 `EXPLAIN` 輸出額外資訊。此回呼函式為選用。即使沒有此回呼函式，儲存在 `ScanState` 中的一般資料（例如目標清單與掃描關聯）也會顯示，但此回呼函式可用來顯示額外的私有狀態。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/custom-scan-execution.html)（原文版本：18.6；核對日期：2026-10-17）
