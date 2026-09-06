## 44.3. 共用資料 [#](#PLPYTHON-SHARING)

全域字典 `SD` 可用來儲存同一函式多次呼叫之間的私有資料。全域字典 `GD` 則儲存公開資料，工作階段中的所有 Python 函式都能存取，請謹慎使用。<a id="id-1.8.11.11.2.3"></a>

每個函式在 Python 直譯器中都有自己的執行環境，因此 `myfunc` 的全域資料與函式引數無法供 `myfunc2` 使用。例外是前述 `GD` 字典中的資料。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plpython-sharing.html)（原文版本：18.6；核對日期：2026-09-07）
