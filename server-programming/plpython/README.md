## 第 44 章 PL/Python — Python 程序語言

**目錄**

[44.1. PL/Python 函式](plpython-funcs.md)

[44.2. 資料值](plpython-data.md)
:   [44.2.1. 資料型別對應](plpython-data.md#PLPYTHON-DATA-TYPE-MAPPING)

    [44.2.2. Null、None](plpython-data.md#PLPYTHON-DATA-NULL)

    [44.2.3. 陣列、清單](plpython-data.md#PLPYTHON-ARRAYS)

    [44.2.4. 複合型別](plpython-data.md#PLPYTHON-DATA-COMPOSITE-TYPES)

    [44.2.5. 回傳集合的函式](plpython-data.md#PLPYTHON-DATA-SET-RETURNING-FUNCS)

[44.3. 共享資料](plpython-sharing.md)

[44.4. 匿名程式碼區塊](plpython-do.md)

[44.5. 觸發程序函式](plpython-trigger.md)

[44.6. 存取資料庫](plpython-database.md)
:   [44.6.1. 資料庫存取函式](plpython-database.md#PLPYTHON-DATABASE-ACCESS-FUNCS)

    [44.6.2. 攔截錯誤](plpython-database.md#PLPYTHON-TRAPPING)

[44.7. 明確子交易](plpython-subtransaction.md)
:   [44.7.1. 子交易情境管理器](plpython-subtransaction.md#PLPYTHON-SUBTRANSACTION-CONTEXT-MANAGERS)

[44.8. 交易管理](plpython-transactions.md)

[44.9. 公用函式](plpython-util.md)

[44.10. Python 2 與 Python 3 的差異](plpython-python23.md)

[44.11. 環境變數](plpython-envar.md)

<a id="id-1.8.11.2"></a><a id="id-1.8.11.3"></a>

PL/Python 程序語言讓 PostgreSQL 函式與程序可以用 [Python 語言](https://www.python.org)撰寫。

若要在特定資料庫中安裝 PL/Python，請使用 `CREATE EXTENSION plpython3u`。

### 提示

如果某個語言已安裝到 `template1` 中，那麼之後所有新建立的資料庫都會自動安裝該語言。

PL/Python 只以「不受信任」語言的形式提供，也就是說它並沒有提供任何限制使用者可以在其中做什麼的方式，因此才會命名為 `plpython3u`。如果未來 Python 開發出安全的執行機制，或許就會推出受信任的變體 `plpython`。撰寫不受信任 PL/Python 函式的人，必須注意該函式不能被用來做任何不想要的事，因為它能做到任何以資料庫管理員身分登入的使用者所能做的事。只有超級使用者才能建立像 `plpython3u` 這類不受信任語言的函式。

### 注意

使用原始碼套件的使用者，必須在安裝過程中特別啟用 PL/Python 的建置（更多資訊請參閱安裝說明）。使用二進位套件的使用者，可能會發現 PL/Python 位於獨立的子套件中。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython.html)（原文版本：18.6；核對日期：2026-09-15）
