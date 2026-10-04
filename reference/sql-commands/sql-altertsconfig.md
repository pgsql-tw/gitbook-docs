<a id="SQL-ALTERTSCONFIG"></a><a id="id-1.9.3.37.1"></a>

## ALTER TEXT SEARCH CONFIGURATION

ALTER TEXT SEARCH CONFIGURATION — 變更文字搜尋設定的定義

<a id="id-1.9.3.37.4"></a>

## 語法

```

ALTER TEXT SEARCH CONFIGURATION name
    ADD MAPPING FOR token_type [, ... ] WITH dictionary_name [, ... ]
ALTER TEXT SEARCH CONFIGURATION name
    ALTER MAPPING FOR token_type [, ... ] WITH dictionary_name [, ... ]
ALTER TEXT SEARCH CONFIGURATION name
    ALTER MAPPING REPLACE old_dictionary WITH new_dictionary
ALTER TEXT SEARCH CONFIGURATION name
    ALTER MAPPING FOR token_type [, ... ] REPLACE old_dictionary WITH new_dictionary
ALTER TEXT SEARCH CONFIGURATION name
    DROP MAPPING [ IF EXISTS ] FOR token_type [, ... ]
ALTER TEXT SEARCH CONFIGURATION name RENAME TO new_name
ALTER TEXT SEARCH CONFIGURATION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TEXT SEARCH CONFIGURATION name SET SCHEMA new_schema
```

<a id="id-1.9.3.37.5"></a>

## 說明

`ALTER TEXT SEARCH CONFIGURATION` 會變更文字搜尋設定的定義。你可以修改其從語彙單元類型到字典的對應，或變更該設定的名稱或擁有者。

你必須是該設定的擁有者，才能使用
`ALTER TEXT SEARCH CONFIGURATION`。

<a id="id-1.9.3.37.6"></a>

## 參數

*`name`*
:   現有文字搜尋設定的名稱（可選擇以綱要限定）。

*`token_type`*
:   由該設定之剖析器所產生的語彙單元類型名稱。

*`dictionary_name`*
:   要針對指定的語彙單元類型查詢的文字搜尋字典名稱。若列出多個字典，會依指定的順序查詢。

*`old_dictionary`*
:   對應中要被取代的文字搜尋字典名稱。

*`new_dictionary`*
:   要用來取代 *`old_dictionary`* 的文字搜尋字典名稱。

*`new_name`*
:   文字搜尋設定的新名稱。

*`new_owner`*
:   文字搜尋設定的新擁有者。

*`new_schema`*
:   文字搜尋設定的新綱要。

`ADD MAPPING FOR` 形式會為指定的語彙單元類型設置一份要查詢的字典清單；若其中任何語彙單元類型已有對應，則會發生錯誤。
`ALTER MAPPING FOR` 形式的作用相同，但會先移除這些語彙單元類型的任何現有對應。
`ALTER MAPPING REPLACE` 形式會在 *`old_dictionary`* 出現的任何位置，以 *`new_dictionary`* 取代它。
當出現 `FOR` 時，只會對指定的語彙單元類型進行此操作；未出現時，則對該設定的所有對應進行。
`DROP MAPPING` 形式會移除指定語彙單元類型的所有字典，使這些類型的語彙單元被該文字搜尋設定忽略。若這些語彙單元類型沒有對應，則會發生錯誤，除非出現 `IF EXISTS`。

<a id="id-1.9.3.37.7"></a>

## 範例

下列範例會在 `my_config` 中使用 `english` 字典的任何位置，以 `swedish` 字典取代 `english` 字典。

```

ALTER TEXT SEARCH CONFIGURATION my_config
  ALTER MAPPING REPLACE english WITH swedish;
```

<a id="id-1.9.3.37.8"></a>

## 相容性

SQL 標準中沒有 `ALTER TEXT SEARCH CONFIGURATION` 陳述式。

<a id="id-1.9.3.37.9"></a>

## 另請參閱

[CREATE TEXT SEARCH CONFIGURATION](sql-createtsconfig.md), [DROP TEXT SEARCH CONFIGURATION](sql-droptsconfig.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-altertsconfig.html)（原文版本：18.6；核對日期：2026-10-04）
