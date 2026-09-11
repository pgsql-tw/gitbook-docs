## 第 12 章 全文檢索

**目錄**

[12.1. 簡介](textsearch-intro.md)
:   [12.1.1. 什麼是文件？](textsearch-intro.md#TEXTSEARCH-DOCUMENT)

    [12.1.2. 基本文字比對](textsearch-intro.md#TEXTSEARCH-MATCHING)

    [12.1.3. 設定](textsearch-intro.md#TEXTSEARCH-INTRO-CONFIGURATIONS)

[12.2. 資料表與索引](textsearch-tables.md)
:   [12.2.1. 搜尋資料表](textsearch-tables.md#TEXTSEARCH-TABLES-SEARCH)

    [12.2.2. 建立索引](textsearch-tables.md#TEXTSEARCH-TABLES-INDEX)

[12.3. 控制文字搜尋](textsearch-controls.md)
:   [12.3.1. 剖析文件](textsearch-controls.md#TEXTSEARCH-PARSING-DOCUMENTS)

    [12.3.2. 剖析查詢](textsearch-controls.md#TEXTSEARCH-PARSING-QUERIES)

    [12.3.3. 搜尋結果排名](textsearch-controls.md#TEXTSEARCH-RANKING)

    [12.3.4. 標示搜尋結果](textsearch-controls.md#TEXTSEARCH-HEADLINE)

[12.4. 其他功能](textsearch-features.md)
:   [12.4.1. 操作文件](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSVECTOR)

    [12.4.2. 操作查詢](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSQUERY)

    [12.4.3. 自動更新用的觸發程序](textsearch-features.md#TEXTSEARCH-UPDATE-TRIGGERS)

    [12.4.4. 收集文件統計資訊](textsearch-features.md#TEXTSEARCH-STATISTICS)

[12.5. 剖析器](textsearch-parsers.md)

[12.6. 字典](textsearch-dictionaries.md)
:   [12.6.1. 停用詞](textsearch-dictionaries.md#TEXTSEARCH-STOPWORDS)

    [12.6.2. Simple 字典](textsearch-dictionaries.md#TEXTSEARCH-SIMPLE-DICTIONARY)

    [12.6.3. 同義詞字典](textsearch-dictionaries.md#TEXTSEARCH-SYNONYM-DICTIONARY)

    [12.6.4. 同義詞庫字典](textsearch-dictionaries.md#TEXTSEARCH-THESAURUS)

    [12.6.5. Ispell 字典](textsearch-dictionaries.md#TEXTSEARCH-ISPELL-DICTIONARY)

    [12.6.6. Snowball 字典](textsearch-dictionaries.md#TEXTSEARCH-SNOWBALL-DICTIONARY)

[12.7. 設定範例](textsearch-configuration.md)

[12.8. 測試與除錯文字搜尋](textsearch-debugging.md)
:   [12.8.1. 設定測試](textsearch-debugging.md#TEXTSEARCH-CONFIGURATION-TESTING)

    [12.8.2. 剖析器測試](textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING)

    [12.8.3. 字典測試](textsearch-debugging.md#TEXTSEARCH-DICTIONARY-TESTING)

[12.9. 文字搜尋的建議索引型別](textsearch-indexes.md)

[12.10. psql 支援](textsearch-psql.md)

[12.11. 限制](textsearch-limitations.md)

<a id="id-1.5.11.2"></a><a id="id-1.5.11.3"></a>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch.html)（原文版本：18.6；核對日期：2026-09-11）
