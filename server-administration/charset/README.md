<a id="CHARSET"></a>

## 第 23 章 在地化

**目錄**

- [23.1. 區域設定支援](locale.md)
  - [23.1.1. 概觀](locale.md#locale-overview)

  - [23.1.2. 行為](locale.md#locale-behavior)

  - [23.1.3. 選擇區域設定](locale.md#locale-selecting-locales)

  - [23.1.4. 區域設定提供者](locale.md#locale-providers)

  - [23.1.5. ICU 區域設定](locale.md#icu-locales)

  - [23.1.6. 問題](locale.md#locale-problems)

- [23.2. 定序支援](collation.md)
  - [23.2.1. 概念](collation.md#collation-concepts)

  - [23.2.2. 管理定序](collation.md#collation-managing)

  - [23.2.3. ICU 自訂定序](collation.md#icu-custom-collations)

- [23.3. 字元集支援](multibyte.md)
  - [23.3.1. 支援的字元集](multibyte.md#multibyte-charset-supported)

  - [23.3.2. 設定字元集](multibyte.md#multibyte-setting)

  - [23.3.3. 伺服器與用戶端間的自動字元集轉換](multibyte.md#multibyte-automatic-conversion)

  - [23.3.4. 可用的字元集轉換](multibyte.md#multibyte-conversions-supported)

  - [23.3.5. 延伸閱讀](multibyte.md#multibyte-further-reading)

本章從管理者的角度說明可用的在地化功能。
PostgreSQL 支援兩種在地化機制：

* 使用作業系統的區域設定功能，提供區域特定的定序順序、數字格式、翻譯後的訊息等。
  這部分內容在[第 23.1 節](locale.md)與
  [第 23.2 節](collation.md)中說明。
* 提供多種不同的字元集，以支援儲存各種語言的文字，並提供用戶端與伺服器之間的字元集轉換。
  這部分內容在[第 23.3 節](multibyte.md)中說明。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/charset.html)（原文版本：18.6；核對日期：2026-09-28）
