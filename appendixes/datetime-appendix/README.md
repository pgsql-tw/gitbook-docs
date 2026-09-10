## 附錄 B. 日期／時間支援

**目錄**

[B.1. 日期／時間輸入解讀](datetime-input-rules.md)

[B.2. 處理無效或模稜兩可的時間戳記](datetime-invalid-input.md)

[B.3. 日期／時間關鍵字](datetime-keywords.md)

[B.4. 日期／時間設定檔](datetime-config-files.md)

[B.5. POSIX 時區規格](datetime-posix-timezone-specs.md)

[B.6. 單位的歷史](datetime-units-history.md)

[B.7. 儒略日期](datetime-julian-dates.md)

PostgreSQL 使用內部啟發式剖析器支援所有日期／時間輸入。日期與時間會以
字串輸入，並拆分為不同欄位；剖析器會先判定欄位可能包含的資訊類型。每個欄位
接著會被解讀，並被指派數值、忽略或拒絕。剖析器為所有文字欄位維護內部查詢表，
其中包括月份、星期幾與時區。

本附錄說明這些查詢表的內容，並描述剖析器解碼日期與時間時所使用的步驟。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datetime-appendix.html)（原文版本：18.6；核對日期：2026-09-10）
