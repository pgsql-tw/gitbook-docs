## 第 31 章 迴歸測試

**目錄**

[31.1. 執行測試](regress-run.md)
:   [31.1.1. 針對暫時安裝執行測試](regress-run.md#REGRESS-RUN-TEMP-INST)

    [31.1.2. 針對既有安裝執行測試](regress-run.md#REGRESS-RUN-EXISTING-INST)

    [31.1.3. 額外的測試套組](regress-run.md#REGRESS-ADDITIONAL)

    [31.1.4. 地區設定與編碼](regress-run.md#REGRESS-RUN-LOCALE)

    [31.1.5. 自訂伺服器設定](regress-run.md#REGRESS-RUN-CUSTOM-SETTINGS)

    [31.1.6. 額外測試](regress-run.md#REGRESS-RUN-EXTRA-TESTS)

[31.2. 測試評估](regress-evaluation.md)
:   [31.2.1. 錯誤訊息差異](regress-evaluation.md#REGRESS-EVALUATION-MESSAGE-DIFFERENCES)

    [31.2.2. 地區設定差異](regress-evaluation.md#REGRESS-EVALUATION-LOCALE-DIFFERENCES)

    [31.2.3. 日期與時間差異](regress-evaluation.md#REGRESS-EVALUATION-DATE-TIME-DIFFERENCES)

    [31.2.4. 浮點數差異](regress-evaluation.md#REGRESS-EVALUATION-FLOAT-DIFFERENCES)

    [31.2.5. 資料列順序差異](regress-evaluation.md#REGRESS-EVALUATION-ORDERING-DIFFERENCES)

    [31.2.6. 堆疊深度不足](regress-evaluation.md#REGRESS-EVALUATION-STACK-DEPTH)

    [31.2.7. 「random」測試](regress-evaluation.md#REGRESS-EVALUATION-RANDOM-TEST)

    [31.2.8. 組態參數](regress-evaluation.md#REGRESS-EVALUATION-CONFIG-PARAMS)

[31.3. 變體比對檔案](regress-variant.md)

[31.4. TAP 測試](regress-tap.md)
:   [31.4.1. 環境變數](regress-tap.md#REGRESS-TAP-VARS)

[31.5. 測試涵蓋率檢驗](regress-coverage.md)
:   [31.5.1. 使用 Autoconf 與 Make 檢驗涵蓋率](regress-coverage.md#REGRESS-COVERAGE-CONFIGURE)

    [31.5.2. 使用 Meson 檢驗涵蓋率](regress-coverage.md#REGRESS-COVERAGE-MESON)

<a id="id-1.6.18.2"></a><a id="id-1.6.18.3"></a>

迴歸測試是針對 PostgreSQL 中 SQL 實作方式的一套完整測試。
這些測試涵蓋標準 SQL 運作方式，
以及 PostgreSQL 的擴充功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/regress.html)（原文版本：18.6；核對日期：2026-09-22）
