<a id="SQL-ALTERTSDICTIONARY"></a><a id="id-1.9.3.38.1"></a>

## ALTER TEXT SEARCH DICTIONARY

ALTER TEXT SEARCH DICTIONARY — 變更文字搜尋字典的定義

<a id="id-1.9.3.38.4"></a>

## 語法

```

ALTER TEXT SEARCH DICTIONARY name (
    option [ = value ] [, ... ]
)
ALTER TEXT SEARCH DICTIONARY name RENAME TO new_name
ALTER TEXT SEARCH DICTIONARY name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TEXT SEARCH DICTIONARY name SET SCHEMA new_schema
```

<a id="id-1.9.3.38.5"></a>

## 說明

`ALTER TEXT SEARCH DICTIONARY` 會變更文字搜尋字典的定義。你可以變更字典的範本專屬選項，或變更字典的名稱或擁有者。

你必須是字典的擁有者才能使用 `ALTER TEXT SEARCH DICTIONARY`。

<a id="id-1.9.3.38.6"></a>

## 參數

*`name`*
:   現有文字搜尋字典的名稱（可選擇以綱要限定）。

*`option`*
:   要為此字典設定的範本專屬選項名稱。

*`value`*
:   範本專屬選項要使用的新值。
    若省略等號與值，則會從字典中移除該選項先前的任何設定，使其改用預設值。

*`new_name`*
:   文字搜尋字典的新名稱。

*`new_owner`*
:   文字搜尋字典的新擁有者。

*`new_schema`*
:   文字搜尋字典的新綱要。

範本專屬選項可以任意順序出現。

<a id="id-1.9.3.38.7"></a>

## 範例

下列範例命令會變更基於 Snowball 之字典的停用詞清單。其他參數維持不變。

```

ALTER TEXT SEARCH DICTIONARY my_dict ( StopWords = newrussian );
```

下列範例命令會將 language 選項改為 `dutch`，並完全移除停用詞選項。

```

ALTER TEXT SEARCH DICTIONARY my_dict ( language = dutch, StopWords );
```

下列範例命令會「更新」字典的定義，但實際上不會變更任何東西。

```

ALTER TEXT SEARCH DICTIONARY my_dict ( dummy );
```

（此方式之所以可行，是因為選項移除程式碼在該選項不存在時不會報錯。）這個技巧在變更字典的設定檔時很有用：`ALTER` 會強制現有的資料庫工作階段重新讀取設定檔；否則，先前已讀取過這些檔案的工作階段永遠不會再重新讀取它們。

<a id="id-1.9.3.38.8"></a>

## 相容性

SQL 標準中沒有 `ALTER TEXT SEARCH DICTIONARY` 陳述式。

<a id="id-1.9.3.38.9"></a>

## 另請參閱

[CREATE TEXT SEARCH DICTIONARY](sql-createtsdictionary.md), [DROP TEXT SEARCH DICTIONARY](sql-droptsdictionary.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertsdictionary.html)（原文版本：18.6；核對日期：2026-10-04）
