<a id="ERROR-MESSAGE-REPORTING"></a>

## 55.2. 在伺服器內回報錯誤 [#](#error-message-reporting) <a href="#error-message-reporting" id="error-message-reporting"></a>

<a id="id-1.10.7.3.2"></a><a id="id-1.10.7.3.3"></a>

伺服器程式碼中產生的錯誤、警告與日誌訊息，應該使用 `ereport` 或它較舊的近親 `elog` 來建立。這個函式的用法相當複雜，需要一些說明。

每則訊息都有兩個必要元素：嚴重性等級（範圍從 `DEBUG` 到 `PANIC`，定義於 `src/include/utils/elog.h`）與主要訊息文字。此外還有一些選用元素，其中最常見的是遵循 SQL 規格 SQLSTATE 慣例的錯誤識別代碼。`ereport` 本身只是一個外殼巨集，存在的主要目的是提供語法上的便利，讓訊息的產生在 C 原始碼中看起來像單一函式呼叫。`ereport` 直接接受的唯一參數是嚴重性等級。主要訊息文字與任何選用的訊息元素，則是在 `ereport` 呼叫之中，透過呼叫輔助函式（例如 `errmsg`）來產生。

典型的 `ereport` 呼叫可能如下：

```

ereport(ERROR,
        errcode(ERRCODE_DIVISION_BY_ZERO),
        errmsg("division by zero"));
```

這指定了錯誤嚴重性等級 `ERROR`（一般常見的錯誤）。`errcode` 呼叫使用 `src/include/utils/errcodes.h` 中定義的巨集來指定 SQLSTATE 錯誤代碼。`errmsg` 呼叫提供主要訊息文字。

你也會經常看到這種較舊的風格，在輔助函式呼叫外多加一組括號：

```

ereport(ERROR,
        (errcode(ERRCODE_DIVISION_BY_ZERO),
         errmsg("division by zero")));
```

在 PostgreSQL 第 12 版之前，這組額外的括號是必要的，但現在是選用的。

以下是一個較複雜的範例：

```

ereport(ERROR,
        errcode(ERRCODE_AMBIGUOUS_FUNCTION),
        errmsg("function %s is not unique",
               func_signature_string(funcname, nargs,
                                     NIL, actual_arg_types)),
        errhint("Unable to choose a best candidate function. "
                "You might need to add explicit typecasts."));
```

這示範了如何使用格式代碼把執行期的值嵌入訊息文字中。此外，也提供了一則選用的「提示」訊息。輔助函式呼叫可以用任何順序撰寫，但依慣例，`errcode` 與 `errmsg` 會出現在最前面。

如果嚴重性等級為 `ERROR` 或更高，`ereport` 會中止目前查詢的執行，而且不會回到呼叫者。如果嚴重性等級低於 `ERROR`，`ereport` 會正常返回。

`ereport` 可用的輔助常式有：

* `errcode(sqlerrcode)` 為該狀況指定 SQLSTATE 錯誤識別代碼。如果沒有呼叫這個常式，錯誤識別代碼的預設值為：錯誤嚴重性等級為 `ERROR` 或更高時是 `ERRCODE_INTERNAL_ERROR`，錯誤等級為 `WARNING` 時是 `ERRCODE_WARNING`，其他情況（`NOTICE` 及以下）則是 `ERRCODE_SUCCESSFUL_COMPLETION`。雖然這些預設值通常很方便，但在省略 `errcode()` 呼叫之前，一定要想想它們是否合適。
* `errmsg(const char *msg, ...)` 指定主要錯誤訊息文字，以及可能要插入其中的執行期值。插入的內容以 `sprintf` 風格的格式代碼指定。除了 `sprintf` 接受的標準格式代碼之外，還可以使用格式代碼 `%m` 來插入 `strerror` 針對 `errno` 目前值所傳回的錯誤訊息。[<a id="id-1.10.7.3.10.2.2.1.7"></a>[18]](#ftn.id-1.10.7.3.10.2.2.1.7) `%m` 不需要在 `errmsg` 的參數列表中有任何對應的項目。請注意，訊息字串會在處理格式代碼之前先經過 `gettext`，以便進行可能的在地化。
* `errmsg_internal(const char *msg, ...)` 與 `errmsg` 相同，差別在於訊息字串不會被翻譯，也不會被納入國際化訊息字典中。這應該用於那些大概不值得花費翻譯功夫的「不可能發生」情況。
* `errmsg_plural(const char *fmt_singular, const char *fmt_plural,
  unsigned long n, ...)` 類似 `errmsg`，但支援訊息的各種複數形式。*`fmt_singular`* 是英文的單數格式，*`fmt_plural`* 是英文的複數格式，*`n`* 是決定需要哪一種複數形式的整數值，其餘參數則依照所選的格式字串來格式化。更多資訊請參閱[第 56.2.2 節](../nls/nls-programmer.md#NLS-GUIDELINES)。
* `errdetail(const char *msg, ...)` 提供一則選用的「詳細」訊息；當有額外資訊似乎不適合放在主要訊息中時使用。訊息字串的處理方式與 `errmsg` 完全相同。
* `errdetail_internal(const char *msg, ...)` 與 `errdetail` 相同，差別在於訊息字串不會被翻譯，也不會被納入國際化訊息字典中。這應該用於不值得花費翻譯功夫的詳細訊息，例如因為它們太過技術性，對大多數使用者沒有用處。
* `errdetail_plural(const char *fmt_singular, const char *fmt_plural,
  unsigned long n, ...)` 類似 `errdetail`，但支援訊息的各種複數形式。更多資訊請參閱[第 56.2.2 節](../nls/nls-programmer.md#NLS-GUIDELINES)。
* `errdetail_log(const char *msg, ...)` 與 `errdetail` 相同，差別在於這個字串只會送到伺服器日誌，永遠不會送到用戶端。如果同時使用了 `errdetail`（或上述其等效函式之一）與 `errdetail_log`，則一個字串會送到用戶端，另一個送到日誌。這對於太過涉及安全性、或太過龐大而不適合放進送給用戶端之報告的錯誤細節很有用。
* `errdetail_log_plural(const char *fmt_singular, const char
  *fmt_plural, unsigned long n, ...)` 類似 `errdetail_log`，但支援訊息的各種複數形式。更多資訊請參閱[第 56.2.2 節](../nls/nls-programmer.md#NLS-GUIDELINES)。
* `errhint(const char *msg, ...)` 提供一則選用的「提示」訊息；用於提供如何修正問題的建議，而不是關於出了什麼錯的事實細節。訊息字串的處理方式與 `errmsg` 完全相同。
* `errhint_plural(const char *fmt_singular, const char *fmt_plural,
  unsigned long n, ...)` 類似 `errhint`，但支援訊息的各種複數形式。更多資訊請參閱[第 56.2.2 節](../nls/nls-programmer.md#NLS-GUIDELINES)。
* `errcontext(const char *msg, ...)` 通常不會直接在 `ereport` 訊息呼叫處被呼叫；而是用在 `error_context_stack` 回呼函式中，提供錯誤發生時的情境資訊，例如在 PL 函式中的目前位置。訊息字串的處理方式與 `errmsg` 完全相同。與其他輔助函式不同，它在每次 `ereport` 呼叫中可以被呼叫超過一次；如此提供的各個字串會以換行分隔並串接起來。
* `errposition(int cursorpos)` 指定錯誤在查詢字串中的文字位置。目前它只對查詢處理的詞法分析與語法分析階段所偵測到的錯誤有用。
* `errtable(Relation rel)` 指定一個關聯，其名稱與綱要名稱應該作為輔助欄位納入錯誤報告中。
* `errtablecol(Relation rel, int attnum)` 指定一個欄位，其名稱、資料表名稱與綱要名稱應該作為輔助欄位納入錯誤報告中。
* `errtableconstraint(Relation rel, const char *conname)` 指定一個資料表限制條件，其名稱、資料表名稱與綱要名稱應該作為輔助欄位納入錯誤報告中。就此目的而言，索引應該被視為限制條件，無論它們是否有相關聯的 `pg_constraint` 項目。請小心，要傳入底層的堆積（heap）關聯作為 `rel`，而不是索引本身。
* `errdatatype(Oid datatypeOid)` 指定一個資料型別，其名稱與綱要名稱應該作為輔助欄位納入錯誤報告中。
* `errdomainconstraint(Oid datatypeOid, const char *conname)` 指定一個網域限制條件，其名稱、網域名稱與綱要名稱應該作為輔助欄位納入錯誤報告中。
* `errcode_for_file_access()` 是一個便利函式，會為檔案存取相關系統呼叫的失敗選擇適當的 SQLSTATE 錯誤識別代碼。它使用已儲存的 `errno` 來決定要產生哪個錯誤代碼。通常應該與主要錯誤訊息文字中的 `%m` 搭配使用。
* `errcode_for_socket_access()` 是一個便利函式，會為通訊端（socket）相關系統呼叫的失敗選擇適當的 SQLSTATE 錯誤識別代碼。
* `errhidestmt(bool hide_stmt)` 可以被呼叫，用來指定在 postmaster 日誌中隱藏訊息的 `STATEMENT:` 部分。一般來說，如果訊息文字已經包含目前的陳述式，這樣做是合適的。
* `errhidecontext(bool hide_ctx)` 可以被呼叫，用來指定在 postmaster 日誌中隱藏訊息的 `CONTEXT:` 部分。這只應該用於那些重複納入情境資訊會讓日誌過度膨脹的詳盡除錯訊息。

### 注意

在一次 `ereport` 呼叫中，`errtable`、`errtablecol`、`errtableconstraint`、`errdatatype` 或 `errdomainconstraint` 這些函式最多應該只使用其中一個。這些函式的存在，是為了讓應用程式能夠擷取與錯誤狀況相關聯的資料庫物件名稱，而不必去檢查可能已經在地化的錯誤訊息文字。對於應用程式很可能會希望自動處理錯誤的錯誤報告，應該使用這些函式。截至 PostgreSQL 9.3，只有 SQLSTATE 類別 23（違反完整性限制條件）中的錯誤有完整的涵蓋，但未來很可能會擴大。

還有一個較舊的函式 `elog` 仍被大量使用。一個 `elog` 呼叫：

```

elog(level, "format string", ...);
```

完全等同於：

```

ereport(level, errmsg_internal("format string", ...));
```

請注意，SQLSTATE 錯誤代碼一律使用預設值，而且訊息字串不會被翻譯。因此，`elog` 只應該用於內部錯誤與低階的除錯日誌記錄。任何一般使用者可能感興趣的訊息，都應該透過 `ereport`。儘管如此，系統中仍有足夠多的內部「不可能發生」錯誤檢查，使得 `elog` 依然廣泛使用；對於這些訊息，因為它寫法簡單，所以偏好使用它。

關於撰寫良好錯誤訊息的建議，請參閱[第 55.3 節](error-style-guide.md)。

<br>

---

<a id="ftn.id-1.10.7.3.10.2.2.1.7"></a>

[[18]](#id-1.10.7.3.10.2.2.1.7) 也就是執行到 `ereport` 呼叫時當下的值；在輔助回報常式中對 `errno` 的變更不會影響它。如果你在 `errmsg` 的參數列表中明確寫出 `strerror(errno)`，情況就不是這樣了；因此，請不要這樣做。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/error-message-reporting.html)（原文版本：18.6；核對日期：2026-10-12）
