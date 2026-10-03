<a id="SQL-CREATETSPARSER"></a><a id="id-1.9.3.90.1"></a>

## CREATE TEXT SEARCH PARSER

CREATE TEXT SEARCH PARSER — 定義新的文字搜尋剖析器

<a id="id-1.9.3.90.4"></a>

## 語法

```

CREATE TEXT SEARCH PARSER name (
    START = start_function ,
    GETTOKEN = gettoken_function ,
    END = end_function ,
    LEXTYPES = lextypes_function
    [, HEADLINE = headline_function ]
)
```

<a id="id-1.9.3.90.5"></a>

## 說明

`CREATE TEXT SEARCH PARSER` 會建立新的文字搜尋剖析器。文字搜尋剖析器定義了將文字字串切分為語彙單元（token），並為這些語彙單元指派類型（類別）的方法。剖析器本身並不特別有用，必須與一些文字搜尋字典一起綁定到文字搜尋設定中，才能用於搜尋。

若給定了綱要名稱，文字搜尋剖析器就會建立在指定的綱要中；否則會建立在目前的綱要中。

您必須是超級使用者才能使用 `CREATE TEXT SEARCH PARSER`。
（之所以有此限制，是因為錯誤的文字搜尋剖析器定義可能會使伺服器混亂，甚至當機。）

更多資訊請參閱[第 12 章](../../the-sql-language/textsearch/README.md)。

<a id="id-1.9.3.90.6"></a>

## 參數

*`name`*
:   要建立的文字搜尋剖析器名稱。名稱可以用綱要限定。

*`start_function`*
:   剖析器的開始函式名稱。

*`gettoken_function`*
:   剖析器的取得下一個語彙單元（get-next-token）函式名稱。

*`end_function`*
:   剖析器的結束函式名稱。

*`lextypes_function`*
:   剖析器的 lextypes 函式名稱（此函式會傳回剖析器所產生之語彙單元類型集合的相關資訊）。

*`headline_function`*
:   剖析器的 headline 函式名稱（此函式會為一組語彙單元產生摘要）。

如有需要，函式名稱可以用綱要限定。不需提供引數型別，因為每一種函式的引數列表都是預先決定的。除了 headline 函式之外，其餘函式皆為必要。

這些引數可以依任意順序出現，不限於上面所示的順序。

<a id="id-1.9.3.90.7"></a>

## 相容性

SQL 標準中沒有
`CREATE TEXT SEARCH PARSER` 陳述式。

<a id="id-1.9.3.90.8"></a>

## 另請參閱

[ALTER TEXT SEARCH PARSER](sql-altertsparser.md), [DROP TEXT SEARCH PARSER](sql-droptsparser.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtsparser.html)（原文版本：18.6；核對日期：2026-10-03）
