<a id="SQL-CREATETSDICTIONARY"></a><a id="id-1.9.3.89.1"></a>

## CREATE TEXT SEARCH DICTIONARY

CREATE TEXT SEARCH DICTIONARY — 定義新的文字搜尋字典

<a id="id-1.9.3.89.4"></a>

## 語法

```

CREATE TEXT SEARCH DICTIONARY name (
    TEMPLATE = template
    [, option = value [, ... ]]
)
```

<a id="id-1.9.3.89.5"></a>

## 說明

`CREATE TEXT SEARCH DICTIONARY` 會建立新的文字搜尋字典。文字搜尋字典指定一種方式，用來辨識對搜尋而言有意義或無意義的詞。字典相依於文字搜尋範本，範本指定實際執行工作的函式。通常字典會提供一些選項，用來控制範本函式的細部行為。

若有指定綱要名稱，則文字搜尋字典會建立在指定的綱要中。否則，它會建立在目前的綱要中。

定義文字搜尋字典的使用者會成為其擁有者。

更多資訊請參閱[第 12 章](../../the-sql-language/textsearch/README.md)。

<a id="id-1.9.3.89.6"></a>

## 參數

*`name`*
:   要建立之文字搜尋字典的名稱。名稱可以用綱要限定。

*`template`*
:   將定義此字典基本行為之文字搜尋範本的名稱。

*`option`*
:   要為此字典設定之範本特有選項的名稱。

*`value`*
:   範本特有選項所要使用的值。若該值不是簡單的識別字或數字，就必須加上引號（但若您希望，也可以一律加上引號）。

選項可以以任何順序出現。

<a id="id-1.9.3.89.7"></a>

## 範例

下列範例命令會建立一個以 Snowball 為基礎、並使用非標準停用詞列表的字典。

```

CREATE TEXT SEARCH DICTIONARY my_russian (
    template = snowball,
    language = russian,
    stopwords = myrussian
);
```

<a id="id-1.9.3.89.8"></a>

## 相容性

SQL 標準中沒有 `CREATE TEXT SEARCH DICTIONARY` 陳述式。

<a id="id-1.9.3.89.9"></a>

## 另請參閱

[ALTER TEXT SEARCH DICTIONARY](sql-altertsdictionary.md), [DROP TEXT SEARCH DICTIONARY](sql-droptsdictionary.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtsdictionary.html)（原文版本：18.6；核對日期：2026-10-03）
