<a id="DYNAMIC-TRACE"></a>

## 27.5. 動態追蹤 [#](#dynamic-trace) <a href="#dynamic-trace" id="dynamic-trace"></a>

[27.5.1. 為動態追蹤編譯](dynamic-trace.md#compiling-for-trace)

[27.5.2. 內建探針](dynamic-trace/trace-points.md#trace-points)

[27.5.3. 使用探針](dynamic-trace.md#using-trace-points)

[27.5.4. 定義新探針](dynamic-trace.md#defining-trace-points)

<a id="id-1.6.14.10.2"></a>

PostgreSQL 提供了支援對資料庫伺服器
進行動態追蹤的功能。這能讓外部工具，
在程式碼中的特定位置被呼叫，藉此追蹤執行過程。

原始碼中已經插入了許多探針（probe）或追蹤點（trace point）。
這些探針的用意，是供資料庫開發人員與管理人員使用。
依預設，這些探針不會被編譯進 PostgreSQL 中；
使用者需要明確告知 configure 指令碼，
才能讓這些探針可供使用。

目前支援
[DTrace](https://en.wikipedia.org/wiki/DTrace)
工具，在撰寫本文時，該工具可在 Solaris、macOS、
FreeBSD、NetBSD，以及 Oracle Linux 上使用。
Linux 上的
[SystemTap](https://sourceware.org/systemtap/) 專案
提供了與 DTrace 相當的功能，同樣可供使用。
理論上，只要變更
`src/include/utils/probes.h` 中巨集的定義，
就能支援其他動態追蹤工具。

<a id="COMPILING-FOR-TRACE"></a>

### 27.5.1. 為動態追蹤編譯 [#](#compiling-for-trace) <a href="#compiling-for-trace" id="compiling-for-trace"></a>

依預設，探針並不可用，因此你需要明確告知 configure
指令碼，讓探針在 PostgreSQL 中可供使用。
若要納入 DTrace 支援，請在 configure 時指定
`--enable-dtrace`。詳情請參閱
[17.3.3.6 節](../installation/install-make.md#CONFIGURE-OPTIONS-DEVEL)。

### 27.5.2. 內建探針 [#](#trace-points) <a href="#trace-points" id="trace-points"></a>

完整內容請見 [27.5.2. 內建探針](dynamic-trace/trace-points.md#trace-points)。

<a id="USING-TRACE-POINTS"></a>

### 27.5.3. 使用探針 [#](#using-trace-points) <a href="#using-trace-points" id="using-trace-points"></a>

以下範例展示了一支 DTrace 指令碼，
用來分析系統中的交易計數，
可作為在效能測試前後對
`pg_stat_database` 拍攝快照的替代方案：

```

#!/usr/sbin/dtrace -qs

postgresql$1:::transaction-start
{
      @start["Start"] = count();
      self->ts  = timestamp;
}

postgresql$1:::transaction-abort
{
      @abort["Abort"] = count();
}

postgresql$1:::transaction-commit
/self->ts/
{
      @commit["Commit"] = count();
      @time["Total time (ns)"] = sum(timestamp - self->ts);
      self->ts=0;
}
```

執行後，此範例 D 指令碼會產生類似下列的輸出：

```

# ./txn_count.d `pgrep -n postgres` or ./txn_count.d <PID>
^C

Start                                          71
Commit                                         70
Total time (ns)                        2312105013
```

### 注意

SystemTap 用於追蹤指令碼的表示法，
與 DTrace 不同，即使底層的追蹤點是相容的。
值得留意的一點是，在撰寫本文時，
SystemTap 指令碼必須以雙底線取代連字號來參照探針名稱。
預期此問題會在未來的 SystemTap 版本中修正。

請務必記得，DTrace 指令碼需要謹慎撰寫並除錯，
否則所蒐集到的追蹤資訊可能毫無意義。
在大多數發現問題的情況下，出問題的往往是插樁（instrumentation）機制本身，
而非底層系統。在討論透過動態追蹤所發現的資訊時，
請務必一併附上所使用的指令碼，
以便他人也能檢查並討論該指令碼。

<a id="DEFINING-TRACE-POINTS"></a>

### 27.5.4. 定義新探針 [#](#defining-trace-points) <a href="#defining-trace-points" id="defining-trace-points"></a>

開發人員可以依需求，在程式碼中的任何位置定義新探針，
不過這需要重新編譯。以下是插入新探針的步驟：

1. 決定探針名稱，以及要透過探針提供哪些資料
2. 將探針定義加入 `src/backend/utils/probes.d`
3. 若含有探針點的模組中尚未含有 `pg_trace.h`，
   請將其納入，並在原始碼中所需的位置，
   插入 `TRACE_POSTGRESQL` 探針巨集
4. 重新編譯，並確認新的探針可供使用

**範例：**
以下範例展示了如何加入一個探針，
用來依交易 ID 追蹤所有新交易。

1. 決定此探針名稱為 `transaction-start`，
   且需要一個 `LocalTransactionId` 型別的參數
2. 將探針定義加入 `src/backend/utils/probes.d`：

   ```

   probe transaction__start(LocalTransactionId);
   ```

   請注意，探針名稱中使用了雙底線。在使用此探針的
   DTrace 指令碼中，雙底線需要替換為連字號，
   因此 `transaction-start` 才是要用於文件中、
   供使用者參考的名稱。
3. 在編譯時，`transaction__start` 會被轉換為一個
   名為 `TRACE_POSTGRESQL_TRANSACTION_START`
   的巨集（請注意，這裡的底線是單一底線），
   只要納入 `pg_trace.h` 即可使用。
   請將此巨集呼叫加入原始碼中適當的位置。
   在此範例中，看起來會像下列這樣：

   ```

   TRACE_POSTGRESQL_TRANSACTION_START(vxid.localTransactionId);
   ```
4. 重新編譯並執行新的二進位檔後，
   透過執行以下 DTrace 命令，
   檢查你新加入的探針是否可供使用。
   你應該會看到類似的輸出：

   ```

   # dtrace -ln transaction-start
      ID    PROVIDER          MODULE           FUNCTION NAME
   18705 postgresql49878     postgres     StartTransactionCommand transaction-start
   18755 postgresql49877     postgres     StartTransactionCommand transaction-start
   18805 postgresql49876     postgres     StartTransactionCommand transaction-start
   18855 postgresql49875     postgres     StartTransactionCommand transaction-start
   18986 postgresql49873     postgres     StartTransactionCommand transaction-start
   ```

在 C 程式碼中加入追蹤巨集時，有幾件事需要留意：

* 你應留意，為探針參數所指定的資料型別，
  必須與巨集中所使用之變數的資料型別相符，
  否則就會產生編譯錯誤。
* 在大多數平台上，若 PostgreSQL 是以
  `--enable-dtrace` 建置的，
  則每當控制流程通過該巨集時，追蹤巨集的引數
  都會被求值，*即使當時並未進行任何追蹤*。
  若你只是要回報幾個區域變數的值，
  通常不需要為此擔心。但請留意，
  不要在引數中放入代價高昂的函式呼叫。
  若你確實需要這麼做，可考慮先檢查該追蹤是否確實已啟用，
  以此保護該巨集：

  ```

  if (TRACE_POSTGRESQL_TRANSACTION_START_ENABLED())
      TRACE_POSTGRESQL_TRANSACTION_START(some_function(...));
  ```

  每個追蹤巨集，都有一個對應的 `ENABLED` 巨集。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dynamic-trace.html)（原文版本：18.6；核對日期：2026-09-26）
