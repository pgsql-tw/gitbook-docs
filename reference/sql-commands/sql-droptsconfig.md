<a id="SQL-DROPTSCONFIG"></a><a id="id-1.9.3.136.1"></a>

## DROP TEXT SEARCH CONFIGURATION

DROP TEXT SEARCH CONFIGURATION — 移除文字搜尋設定

<a id="id-1.9.3.136.4"></a>

## 語法

```

DROP TEXT SEARCH CONFIGURATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.136.5"></a>

## 說明

`DROP TEXT SEARCH CONFIGURATION` 會移除現有的文字搜尋設定。要執行此命令，您必須是該設定的擁有者。

<a id="id-1.9.3.136.6"></a>

## 參數

`IF EXISTS`
:   文字搜尋設定不存在時不擲出錯誤；此情況會發出 notice。

*`name`*
:   現有文字搜尋設定的名稱（可選擇以綱要限定）。

`CASCADE`
:   自動移除相依於文字搜尋設定的物件，以及相依於這些物件的所有物件
    （請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件相依於文字搜尋設定則拒絕移除。這是預設行為。

<a id="id-1.9.3.136.7"></a>

## 範例

移除文字搜尋設定 `my_english`：

```

DROP TEXT SEARCH CONFIGURATION my_english;
```

若有任何現有索引在 `to_tsvector` 呼叫中引用該設定，此命令將不會成功。加上 `CASCADE` 即可將這些索引連同文字搜尋設定一併移除。

<a id="id-1.9.3.136.8"></a>

## 相容性

SQL 標準中沒有 `DROP TEXT SEARCH CONFIGURATION` 陳述式。

<a id="id-1.9.3.136.9"></a>

## 另請參閱

[ALTER TEXT SEARCH CONFIGURATION](sql-altertsconfig.md), [CREATE TEXT SEARCH CONFIGURATION](sql-createtsconfig.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-droptsconfig.html)（原文版本：18.6；核對日期：2026-10-03）
