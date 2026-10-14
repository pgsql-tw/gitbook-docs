<a id="SOURCE-CONVENTIONS"></a>

## 55.4. 其他程式碼撰寫慣例 [#](#SOURCE-CONVENTIONS)

<a id="SOURCE-CONVENTIONS-C-STANDARD"></a>

### C 標準 [#](#SOURCE-CONVENTIONS-C-STANDARD)

PostgreSQL 中的程式碼應該只依賴 C99 標準中提供的語言功能。也就是說，符合 C99 標準的編譯器必須能夠編譯 postgres，至少除了少數與平台相關的部分之外是如此。

C99 標準中包含的少數功能，目前不允許在 PostgreSQL 核心程式碼中使用。目前這包括可變長度陣列、宣告與程式碼交錯、`//` 註解、通用字元名稱（universal character names）。原因包括可攜性與歷史慣例。

C 標準較新修訂版的功能或編譯器特有的功能，若有提供替代方案（fallback），就可以使用。

例如，目前有使用 `_Static_assert()` 與 `__builtin_constant_p`，儘管它們分別來自 C 標準較新的修訂版與 GCC 擴充功能。若無法使用，我們分別會退而使用一個執行相同檢查、但會發出相當晦澀訊息的 C99 相容替代實作，以及不使用 `__builtin_constant_p`。

<a id="SOURCE-CONVENTIONS-MACROS-INLINE"></a>

### 類函式巨集與行內函式 [#](#SOURCE-CONVENTIONS-MACROS-INLINE)

帶有參數的巨集與 `static inline` 函式都可以使用。如果寫成巨集會有多次求值的風險，則以後者為佳，例如下面這種情況：

```

#define Max(x, y)       ((x) > (y) ? (x) : (y))
```

或者巨集會非常長的時候。在其他情況下，只能使用巨集，或者至少使用巨集比較容易。例如因為需要把各種不同型別的運算式傳給巨集。

當行內函式的定義參照了只在後端中才有的符號（即變數、函式）時，從前端程式碼引入（include）時，該函式可能是不可見的。

```

#ifndef FRONTEND
static inline MemoryContext
MemoryContextSwitchTo(MemoryContext context)
{
    MemoryContext old = CurrentMemoryContext;

    CurrentMemoryContext = context;
    return old;
}
#endif   /* FRONTEND */
```

在這個範例中，參照了只在後端中才有的 `CurrentMemoryContext`，因此該函式以 `#ifndef FRONTEND` 隱藏起來。之所以有這條規則，是因為有些編譯器即使函式未被使用，也會發出對行內函式中所含符號的參照。

<a id="SOURCE-CONVENTIONS-SIGNAL-HANDLERS"></a>

### 撰寫訊號處理常式 [#](#SOURCE-CONVENTIONS-SIGNAL-HANDLERS)

要適合在訊號處理常式中執行，程式碼必須寫得非常小心。根本問題在於，除非訊號被阻擋，否則訊號處理常式可能在任何時刻中斷程式碼。如果訊號處理常式內的程式碼與外部程式碼使用相同的狀態，就可能造成混亂。舉例來說，想想看如果訊號處理常式試圖取得一個被中斷的程式碼已經持有的鎖定，會發生什麼事。

除非有特別的安排，訊號處理常式中的程式碼只可以呼叫非同步訊號安全（async-signal safe）的函式（依 POSIX 定義），並存取型別為 `volatile sig_atomic_t` 的變數。`postgres` 中也有少數函式被視為訊號安全，其中重要的是 `SetLatch()`。

在大多數情況下，訊號處理常式應該只記下訊號已經到達，並使用閂鎖（latch）喚醒在處理常式之外執行的程式碼，除此之外不做任何事。這種處理常式的範例如下：

```

static void
handle_sighup(SIGNAL_ARGS)
{
    got_SIGHUP = true;
    SetLatch(MyLatch);
}
```

<a id="SOURCE-CONVENTIONS-FUNCTION-POINTERS"></a>

### 呼叫函式指標 [#](#SOURCE-CONVENTIONS-FUNCTION-POINTERS)

為了清楚起見，如果指標是一個單純的變數，在呼叫其所指向的函式時，建議明確地對函式指標取值（dereference），例如：

```

(*emit_log_hook) (edata);
```

（儘管 `emit_log_hook(edata)` 也能運作。）當函式指標是某個結構的一部分時，額外的標點符號可以省略，而且通常應該省略，例如：

```

paramInfo->paramFetch(paramInfo, paramId);
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/source-conventions.html)（原文版本：18.6；核對日期：2026-10-12）
