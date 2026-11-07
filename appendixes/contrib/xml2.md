<a id="XML2"></a>

## F.50. xml2 — XPath 查詢與 XSLT 功能 [#](#xml2) <a href="#xml2" id="xml2"></a>

[F.50.1. 淘汰通知](xml2.md#xml2-deprecation)

[F.50.2. 函式說明](xml2/xml2-functions.md#xml2-functions)

[F.50.3. `xpath_table`](xml2/xml2-xpath-table.md#xml2-xpath-table)

[F.50.4. XSLT 函式](xml2.md#xml2-xslt)

[F.50.5. 作者](xml2.md#xml2-author)

<a id="id-1.11.7.60.2"></a>

`xml2` 模組提供 XPath 查詢與 XSLT 功能。

<a id="XML2-DEPRECATION"></a>

### F.50.1. 淘汰通知 [#](#xml2-deprecation) <a href="#xml2-deprecation" id="xml2-deprecation"></a>

自 PostgreSQL 8.3 起，核心伺服器已具備以 SQL/XML 標準為基礎的 XML 相關功能。這些功能涵蓋 XML 語法檢查與 XPath 查詢（也就是此模組所做的事），而且還有更多功能，但其 API 完全不相容。我們計畫在未來的 PostgreSQL 版本中移除此模組，改用較新的標準 API，因此建議你嘗試轉換你的應用程式。若你發現此模組的某些功能在較新的 API 中沒有以適當的形式提供，請將你的問題說明寄至 `<pgsql-hackers@lists.postgresql.org>`，以便解決這項不足。

### F.50.2. 函式說明 [#](#xml2-functions) <a href="#xml2-functions" id="xml2-functions"></a>

完整內容請見 [F.50.2. 函式說明](xml2/xml2-functions.md#xml2-functions)。

### F.50.3. `xpath_table` [#](#xml2-xpath-table) <a href="#xml2-xpath-table" id="xml2-xpath-table"></a>

完整內容請見 [F.50.3. xpath_table](xml2/xml2-xpath-table.md#xml2-xpath-table)。

<a id="XML2-XSLT"></a>

### F.50.4. XSLT 函式 [#](#xml2-xslt) <a href="#xml2-xslt" id="xml2-xslt"></a>

若已安裝 libxslt，即可使用下列函式：

<a id="XML2-XSLT-XSLT-PROCESS"></a>

#### F.50.4.1. `xslt_process` [#](#XML2-XSLT-XSLT-PROCESS)

<a id="id-1.11.7.60.7.3.2"></a>

```

xslt_process(text document, text stylesheet, text paramlist) returns text
```

此函式將 XSL 樣式表套用至文件，並傳回轉換後的結果。`paramlist` 是轉換中要使用的參數指派清單，以 `a=1,b=2` 的形式指定。請注意，參數剖析的方式非常簡陋：參數值不能包含逗號！

另外還有雙參數版本的 `xslt_process`，它不會傳遞任何參數給轉換。

<a id="XML2-AUTHOR"></a>

### F.50.5. 作者 [#](#xml2-author) <a href="#xml2-author" id="xml2-author"></a>

John Gray `<jgray@azuli.co.uk>`

此模組的開發由 Torchbox Ltd.（www.torchbox.com）贊助。它採用與 PostgreSQL 相同的 BSD 授權。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xml2.html)（原文版本：18.6；核對日期：2026-10-22）
