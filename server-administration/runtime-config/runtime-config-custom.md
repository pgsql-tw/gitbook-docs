## 19.16. 自訂選項 [#](#RUNTIME-CONFIG-CUSTOM)

此功能讓附加模組（例如程序語言）能新增 PostgreSQL 原本不認得的參數，使擴充模組也能透過標準方式設定。

自訂選項的名稱由兩部分組成：擴充套件名稱、句點，再接上參數本身的名稱，類似 SQL 中的限定名稱。例如 `plpgsql.variable_conflict`。

由於可能需要在尚未載入相關擴充模組的程序中設定自訂選項，PostgreSQL 會接受任何兩部分參數名稱的設定。這類變數會視為預留位置，在定義它們的模組載入之前不具任何功能。擴充模組載入時，會加入其變數定義，並依照定義轉換既有預留位置的值。若仍有以該擴充套件名稱開頭、但無法辨識的預留位置，則會發出警告並移除它們。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-custom.html)（原文版本：18.6；核對日期：2026-09-07）
