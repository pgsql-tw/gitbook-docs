<a id="SQL-CREATETSTEMPLATE"></a><a id="id-1.9.3.91.1"></a>

## CREATE TEXT SEARCH TEMPLATE

CREATE TEXT SEARCH TEMPLATE — 定義新的文字搜尋範本

<a id="id-1.9.3.91.4"></a>

## 語法

```

CREATE TEXT SEARCH TEMPLATE name (
    [ INIT = init_function , ]
    LEXIZE = lexize_function
)
```

<a id="id-1.9.3.91.5"></a>

## 說明

`CREATE TEXT SEARCH TEMPLATE` 會建立新的文字搜尋範本。文字搜尋範本定義了實作文字搜尋字典的函式。範本本身並沒有用處，必須實體化為字典才能使用。字典通常會指定要提供給範本函式的參數。

若給定了綱要名稱，文字搜尋範本就會建立在指定的綱要中；否則會建立在目前的綱要中。

您必須是超級使用者才能使用 `CREATE TEXT SEARCH
TEMPLATE`。之所以有此限制，是因為錯誤的文字搜尋範本定義可能會使伺服器混亂，甚至當機。將範本與字典分開的理由在於，範本封裝了定義字典時「不安全」的部分。定義字典時可以設定的參數，讓無特權的使用者設定是安全的，因此建立字典不需要是具特權的操作。

更多資訊請參閱[第 12 章](../../the-sql-language/textsearch/README.md)。

<a id="id-1.9.3.91.6"></a>

## 參數

*`name`*
:   要建立的文字搜尋範本名稱。名稱可以用綱要限定。

*`init_function`*
:   範本的 init 函式名稱。

*`lexize_function`*
:   範本的 lexize 函式名稱。

如有需要，函式名稱可以用綱要限定。不需提供引數型別，因為每一種函式的引數列表都是預先決定的。lexize 函式為必要，init 函式則可省略。

這些引數可以依任意順序出現，不限於上面所示的順序。

<a id="id-1.9.3.91.7"></a>

## 相容性

SQL 標準中沒有
`CREATE TEXT SEARCH TEMPLATE` 陳述式。

<a id="id-1.9.3.91.8"></a>

## 另請參閱

[ALTER TEXT SEARCH TEMPLATE](sql-altertstemplate.md), [DROP TEXT SEARCH TEMPLATE](sql-droptstemplate.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtstemplate.html)（原文版本：18.6；核對日期：2026-10-03）
