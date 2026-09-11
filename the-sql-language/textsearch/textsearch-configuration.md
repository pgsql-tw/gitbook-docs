<a id="TEXTSEARCH-CONFIGURATION"></a>

## 12.7. 設定範例 [#](#TEXTSEARCH-CONFIGURATION)

文字搜尋設定指定了將文件轉換為 `tsvector` 所需的所有選項：用來將文字切分為語彙單元的剖析器，以及用來將每個語彙單元轉換為詞素的字典。每次呼叫 `to_tsvector` 或 `to_tsquery` 時，都需要一個文字搜尋設定來進行處理。設定參數 [default_text_search_config](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) 指定預設設定的名稱，當文字搜尋函式省略明確的設定參數時，就會使用這個設定。它可以在 `postgresql.conf` 中設定，也可以使用 `SET` 指令為個別工作階段設定。

系統提供了數個預先定義的文字搜尋設定，你也可以輕鬆建立自訂的設定。為了方便管理文字搜尋物件，系統提供了一組 SQL 指令，另外也有數個 psql 指令可以顯示文字搜尋物件的資訊（[第 12.10 節](textsearch-psql.md)）。

我們以建立一個名為 `pg` 的設定為例，首先複製內建的 `english` 設定：

```

CREATE TEXT SEARCH CONFIGURATION public.pg ( COPY = pg_catalog.english );
```

我們將使用一份 PostgreSQL 專用的同義詞清單，並將它儲存在 `$SHAREDIR/tsearch_data/pg_dict.syn`。檔案內容如下：

```

postgres    pg
pgsql       pg
postgresql  pg
```

我們像這樣定義同義詞字典：

```

CREATE TEXT SEARCH DICTIONARY pg_dict (
    TEMPLATE = synonym,
    SYNONYMS = pg_dict
);
```

接著註冊 Ispell 字典 `english_ispell`，它有自己的設定檔：

```

CREATE TEXT SEARCH DICTIONARY english_ispell (
    TEMPLATE = ispell,
    DictFile = english,
    AffFile = english,
    StopWords = english
);
```

現在我們可以在設定 `pg` 中設定單字的對應：

```

ALTER TEXT SEARCH CONFIGURATION pg
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
                      word, hword, hword_part
    WITH pg_dict, english_ispell, english_stem;
```

我們選擇不為某些內建設定會處理的語彙單元類型建立索引或進行搜尋：

```

ALTER TEXT SEARCH CONFIGURATION pg
    DROP MAPPING FOR email, url, url_path, sfloat, float;
```

現在我們可以測試這個設定：

```

SELECT * FROM ts_debug('public.pg', '
PostgreSQL, the highly scalable, SQL compliant, open source object-relational
database management system, is now undergoing beta testing of the next
version of our software.
');
```

下一步是設定工作階段，讓它使用這個建立在 `public` schema 中的新設定：

```

=> \dF
   List of text search configurations
 Schema  | Name | Description
---------+------+-------------
 public  | pg   |

SET default_text_search_config = 'public.pg';
SET

SHOW default_text_search_config;
 default_text_search_config
----------------------------
 public.pg
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-configuration.html)（原文版本：18.6；核對日期：2026-09-11）
