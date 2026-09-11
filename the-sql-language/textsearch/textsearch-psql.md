<a id="TEXTSEARCH-PSQL"></a>

## 12.10. psql 支援 [#](#TEXTSEARCH-PSQL)

在 psql 中，可以使用一組指令取得文字搜尋設定物件的資訊：

```

\dF{d,p,t}[+] [PATTERN]
```

選用的 `+` 會顯示更多細節。

選用的參數 *`PATTERN`* 可以是文字搜尋物件的名稱，也可以加上 schema 限定。如果省略 *`PATTERN`*，就會顯示所有可見物件的資訊。*`PATTERN`* 可以是正規表示式，並且可以為 schema 名稱與物件名稱提供*各自*的樣式。以下範例說明了這一點：

```

=> \dF *fulltext*
       List of text search configurations
 Schema |  Name        | Description
--------+--------------+-------------
 public | fulltext_cfg |
```

```

=> \dF *.fulltext*
       List of text search configurations
 Schema   |  Name        | Description
----------+----------------------------
 fulltext | fulltext_cfg |
 public   | fulltext_cfg |
```

可用的指令有：

`\dF[+] [PATTERN]`
:   列出文字搜尋設定（加上 `+` 可顯示更多細節）。

```

    => \dF russian
                List of text search configurations
       Schema   |  Name   |            Description
    ------------+---------+------------------------------------
     pg_catalog | russian | configuration for russian language

    => \dF+ russian
    Text search configuration "pg_catalog.russian"
    Parser: "pg_catalog.default"
          Token      | Dictionaries
    -----------------+--------------
     asciihword      | english_stem
     asciiword       | english_stem
     email           | simple
     file            | simple
     float           | simple
     host            | simple
     hword           | russian_stem
     hword_asciipart | english_stem
     hword_numpart   | simple
     hword_part      | russian_stem
     int             | simple
     numhword        | simple
     numword         | simple
     sfloat          | simple
     uint            | simple
     url             | simple
     url_path        | simple
     version         | simple
     word            | russian_stem
    ```

`\dFd[+] [PATTERN]`
:   列出文字搜尋字典（加上 `+` 可顯示更多細節）。

```

    => \dFd
                                 List of text search dictionaries
       Schema   |      Name       |                        Description
    ------------+-----------------+-----------------------------------------------------------
     pg_catalog | arabic_stem     | snowball stemmer for arabic language
     pg_catalog | armenian_stem   | snowball stemmer for armenian language
     pg_catalog | basque_stem     | snowball stemmer for basque language
     pg_catalog | catalan_stem    | snowball stemmer for catalan language
     pg_catalog | danish_stem     | snowball stemmer for danish language
     pg_catalog | dutch_stem      | snowball stemmer for dutch language
     pg_catalog | english_stem    | snowball stemmer for english language
     pg_catalog | estonian_stem   | snowball stemmer for estonian language
     pg_catalog | finnish_stem    | snowball stemmer for finnish language
     pg_catalog | french_stem     | snowball stemmer for french language
     pg_catalog | german_stem     | snowball stemmer for german language
     pg_catalog | greek_stem      | snowball stemmer for greek language
     pg_catalog | hindi_stem      | snowball stemmer for hindi language
     pg_catalog | hungarian_stem  | snowball stemmer for hungarian language
     pg_catalog | indonesian_stem | snowball stemmer for indonesian language
     pg_catalog | irish_stem      | snowball stemmer for irish language
     pg_catalog | italian_stem    | snowball stemmer for italian language
     pg_catalog | lithuanian_stem | snowball stemmer for lithuanian language
     pg_catalog | nepali_stem     | snowball stemmer for nepali language
     pg_catalog | norwegian_stem  | snowball stemmer for norwegian language
     pg_catalog | portuguese_stem | snowball stemmer for portuguese language
     pg_catalog | romanian_stem   | snowball stemmer for romanian language
     pg_catalog | russian_stem    | snowball stemmer for russian language
     pg_catalog | serbian_stem    | snowball stemmer for serbian language
     pg_catalog | simple          | simple dictionary: just lower case and check for stopword
     pg_catalog | spanish_stem    | snowball stemmer for spanish language
     pg_catalog | swedish_stem    | snowball stemmer for swedish language
     pg_catalog | tamil_stem      | snowball stemmer for tamil language
     pg_catalog | turkish_stem    | snowball stemmer for turkish language
     pg_catalog | yiddish_stem    | snowball stemmer for yiddish language
    ```

`\dFp[+] [PATTERN]`
:   列出文字搜尋剖析器（加上 `+` 可顯示更多細節）。

```

    => \dFp
            List of text search parsers
       Schema   |  Name   |     Description
    ------------+---------+---------------------
     pg_catalog | default | default word parser
    => \dFp+
        Text search parser "pg_catalog.default"
         Method      |    Function    | Description
    -----------------+----------------+-------------
     Start parse     | prsd_start     |
     Get next token  | prsd_nexttoken |
     End parse       | prsd_end       |
     Get headline    | prsd_headline  |
     Get token types | prsd_lextype   |

            Token types for parser "pg_catalog.default"
       Token name    |               Description
    -----------------+------------------------------------------
     asciihword      | Hyphenated word, all ASCII
     asciiword       | Word, all ASCII
     blank           | Space symbols
     email           | Email address
     entity          | XML entity
     file            | File or path name
     float           | Decimal notation
     host            | Host
     hword           | Hyphenated word, all letters
     hword_asciipart | Hyphenated word part, all ASCII
     hword_numpart   | Hyphenated word part, letters and digits
     hword_part      | Hyphenated word part, all letters
     int             | Signed integer
     numhword        | Hyphenated word, letters and digits
     numword         | Word, letters and digits
     protocol        | Protocol head
     sfloat          | Scientific notation
     tag             | XML tag
     uint            | Unsigned integer
     url             | URL
     url_path        | URL path
     version         | Version number
     word            | Word, all letters
    (23 rows)
    ```

`\dFt[+] [PATTERN]`
:   列出文字搜尋範本（加上 `+` 可顯示更多細節）。

```

    => \dFt
                               List of text search templates
       Schema   |   Name    |                        Description
    ------------+-----------+-----------------------------------------------------------
     pg_catalog | ispell    | ispell dictionary
     pg_catalog | simple    | simple dictionary: just lower case and check for stopword
     pg_catalog | snowball  | snowball stemmer
     pg_catalog | synonym   | synonym dictionary: replace word by its synonym
     pg_catalog | thesaurus | thesaurus dictionary: phrase by phrase substitution
    ```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-psql.html)（原文版本：18.6；核對日期：2026-09-11）
