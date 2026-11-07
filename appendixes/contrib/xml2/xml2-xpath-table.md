# F.50.3. xpath_table

<a id="XML2-XPATH-TABLE"></a>

## F.50.3. `xpath_table` [#](#xml2-xpath-table) <a href="#xml2-xpath-table" id="xml2-xpath-table"></a>

<a id="id-1.11.7.60.6.2"></a>

```

xpath_table(text key, text document, text relation, text xpaths, text criteria) returns setof record
```

`xpath_table` 是一個資料表函式，它會對一組文件中的每一份文件執行一組 XPath 查詢，並將結果以資料表形式傳回。原始文件資料表的主鍵欄位會作為結果的第一個欄位傳回，使結果集可以直接用於連接。各參數的說明請參閱[表 F.38](#xml2-xpath-table-parameters)。

<a id="XML2-XPATH-TABLE-PARAMETERS"></a>

### 表 F.38. `xpath_table` 參數 [#](#xml2-xpath-table-parameters) <a href="#xml2-xpath-table-parameters" id="xml2-xpath-table-parameters"></a>

<table border="1" class="table" summary="xpath_table 參數"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>參數</th><th>說明</th></tr></thead><tbody><tr><td><em class="parameter"><code>key</code></em></td><td>
<p>
        <span class="quote">“<span class="quote">key</span>”</span>欄位的名稱——這只是要作為輸出資料表第一個欄位的欄位，也就是說，它用來識別每一筆輸出資料列來自哪一筆記錄（請參閱下文關於多值的說明）
       </p>
</td></tr><tr><td><em class="parameter"><code>document</code></em></td><td>
<p>
        包含 XML 文件之欄位的名稱
       </p>
</td></tr><tr><td><em class="parameter"><code>relation</code></em></td><td>
<p>
        包含這些文件之資料表或檢視表的名稱
       </p>
</td></tr><tr><td><em class="parameter"><code>xpaths</code></em></td><td>
<p>
        一個或多個 XPath 運算式，以 <code class="literal">|</code> 分隔
</p>
</td></tr><tr><td><em class="parameter"><code>criteria</code></em></td><td>
<p>
        WHERE 子句的內容。此參數不可省略，因此若要處理該關聯中的所有資料列，請使用 <code class="literal">true</code> 或 <code class="literal">1=1</code>
       </p>
</td></tr></tbody></table>

<br>

這些參數（XPath 字串除外）只是被直接代入一般的 SQL SELECT 陳述式中，因此你有一些彈性——該陳述式為

`SELECT <key>, <document> FROM <relation> WHERE <criteria>`

所以這些參數可以是在這些特定位置中有效的*任何*內容。此 SELECT 的結果必須恰好傳回兩個欄位（除非你試圖為 key 或 document 列出多個欄位，否則一定會是如此）。請注意，這種簡單的做法要求你驗證任何使用者提供的值，以避免 SQL 注入攻擊。

此函式必須用在 `FROM` 運算式中，並以 `AS` 子句指定輸出欄位；例如

```

SELECT * FROM
xpath_table('article_id',
            'article_xml',
            'articles',
            '/article/author|/article/pages|/article/title',
            'date_entered > ''2003-01-01'' ')
AS t(article_id integer, author text, page_count integer, title text);
```

`AS` 子句定義輸出資料表中各欄位的名稱與型別。第一個是「key」欄位，其餘則對應各個 XPath 查詢。若 XPath 查詢比結果欄位多，多出的查詢會被忽略；若結果欄位比 XPath 查詢多，多出的欄位會是 NULL。

請注意，此範例將 `page_count` 結果欄位定義為整數。此函式在內部處理的是字串表示，因此當你指定輸出中要有整數時，它會取得 XPath 結果的字串表示，並使用 PostgreSQL 輸入函式將其轉換為整數（或 `AS` 子句所要求的任何型別）。若無法轉換——例如結果為空時——就會產生錯誤，因此若你認為資料可能有任何問題，或許只使用 `text` 作為欄位型別會比較好。

呼叫端的 `SELECT` 陳述式不一定只能是 `SELECT *`——它可以依名稱參照輸出欄位，或將輸出欄位與其他資料表連接。此函式產生一個虛擬資料表，你可以對它執行任何想要的操作（例如彙總、連接、排序等）。因此我們也可以寫成：

```

SELECT t.title, p.fullname, p.email
FROM xpath_table('article_id', 'article_xml', 'articles',
                 '/article/title|/article/author/@id',
                 'xpath_string(article_xml,''/article/@date'') > ''2003-03-20'' ')
       AS t(article_id integer, title text, author_id integer),
     tblPeopleInfo AS p
WHERE t.author_id = p.person_id;
```

這是較複雜的範例。當然，為了方便，你也可以將這一切包裝在檢視表中。

<a id="XML2-XPATH-TABLE-MULTIVALUED-RESULTS"></a>

### F.50.3.1. 多值結果 [#](#xml2-xpath-table-multivalued-results) <a href="#xml2-xpath-table-multivalued-results" id="xml2-xpath-table-multivalued-results"></a>

`xpath_table` 函式假設每個 XPath 查詢的結果都可能是多值的，因此函式傳回的資料列數可能與輸入文件的數量不同。傳回的第一筆資料列包含各查詢的第一個結果，第二筆資料列包含各查詢的第二個結果。若某個查詢的值比其他查詢少，則會改為傳回 null 值。

在某些情況下，使用者會知道某個 XPath 查詢只會傳回單一結果（例如唯一的文件識別碼）——若與傳回多個結果的 XPath 查詢一起使用，單值結果只會出現在結果的第一筆資料列。解決方法是以 key 欄位作為連接條件的一部分，與另一個較簡單的 XPath 查詢進行連接。例如：

```

CREATE TABLE test (
    id int PRIMARY KEY,
    xml text
);

INSERT INTO test VALUES (1, '<doc num="C1">
<line num="L1"><a>1</a><b>2</b><c>3</c></line>
<line num="L2"><a>11</a><b>22</b><c>33</c></line>
</doc>');

INSERT INTO test VALUES (2, '<doc num="C2">
<line num="L1"><a>111</a><b>222</b><c>333</c></line>
<line num="L2"><a>111</a><b>222</b><c>333</c></line>
</doc>');

SELECT * FROM
  xpath_table('id','xml','test',
              '/doc/@num|/doc/line/@num|/doc/line/a|/doc/line/b|/doc/line/c',
              'true')
  AS t(id int, doc_num varchar(10), line_num varchar(10), val1 int, val2 int, val3 int)
WHERE id = 1 ORDER BY doc_num, line_num

 id | doc_num | line_num | val1 | val2 | val3
----+---------+----------+------+------+------
  1 | C1      | L1       |    1 |    2 |    3
  1 |         | L2       |   11 |   22 |   33
```

若要讓每一行都有 `doc_num`，解決方法是呼叫兩次 `xpath_table` 並連接其結果：

```

SELECT t.*,i.doc_num FROM
  xpath_table('id', 'xml', 'test',
              '/doc/line/@num|/doc/line/a|/doc/line/b|/doc/line/c',
              'true')
    AS t(id int, line_num varchar(10), val1 int, val2 int, val3 int),
  xpath_table('id', 'xml', 'test', '/doc/@num', 'true')
    AS i(id int, doc_num varchar(10))
WHERE i.id=t.id AND i.id=1
ORDER BY doc_num, line_num;

 id | line_num | val1 | val2 | val3 | doc_num
----+----------+------+------+------+---------
  1 | L1       |    1 |    2 |    3 | C1
  1 | L2       |   11 |   22 |   33 | C1
(2 rows)
```

[返回 F.50. xml2 — XPath 查詢與 XSLT 功能](../xml2.md#xml2)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/xml2.html)（原文版本：18.6；核對日期：2026-10-22）
