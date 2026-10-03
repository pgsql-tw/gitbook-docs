<a id="SQL-CREATETSCONFIG"></a><a id="id-1.9.3.88.1"></a>

## CREATE TEXT SEARCH CONFIGURATION

CREATE TEXT SEARCH CONFIGURATION — 定義新的文字搜尋設定

<a id="id-1.9.3.88.4"></a>

## 語法

```

CREATE TEXT SEARCH CONFIGURATION name (
    PARSER = parser_name |
    COPY = source_config
)
```

<a id="id-1.9.3.88.5"></a>

## 說明

`CREATE TEXT SEARCH CONFIGURATION` 會建立新的文字搜尋設定。文字搜尋設定指定一個可以將字串切分為語彙單元的文字搜尋剖析器，以及可用來判斷哪些語彙單元是搜尋所關注之對象的字典。

若只指定剖析器，則新的文字搜尋設定一開始沒有從語彙單元類型到字典的對應，因此會忽略所有單字。之後必須使用 `ALTER TEXT SEARCH
CONFIGURATION` 命令建立對應，才能讓此設定發揮作用。或者，也可以複製現有的文字搜尋設定。

若指定了綱要名稱，文字搜尋設定就會建立在指定的綱要中；否則會建立在目前的綱要中。

定義文字搜尋設定的使用者會成為其擁有者。

詳細資訊請參閱[第 12 章](../../the-sql-language/textsearch/README.md)。

<a id="id-1.9.3.88.6"></a>

## 參數

*`name`*
:   要建立的文字搜尋設定名稱。此名稱可以用綱要限定。

*`parser_name`*
:   此設定所要使用的文字搜尋剖析器名稱。

*`source_config`*
:   要複製的現有文字搜尋設定名稱。

<a id="id-1.9.3.88.7"></a>

## 注意事項

`PARSER` 與 `COPY` 選項是互斥的，因為複製現有設定時，其剖析器選擇也會一併複製。

<a id="id-1.9.3.88.8"></a>

## 相容性

SQL 標準中沒有 `CREATE TEXT SEARCH CONFIGURATION` 陳述式。

<a id="id-1.9.3.88.9"></a>

## 另請參閱

[ALTER TEXT SEARCH CONFIGURATION](sql-altertsconfig.md), [DROP TEXT SEARCH CONFIGURATION](sql-droptsconfig.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtsconfig.html)（原文版本：18.6；核對日期：2026-10-03）
