<a id="FUNCTIONS-JSON"></a>

## 9.16. JSON 函式與運算子 [#](#functions-json) <a href="#functions-json" id="functions-json"></a>

[9.16.1. 處理與建立 JSON 資料](functions-json/functions-json-processing.md#functions-json-processing)

[9.16.2. SQL/JSON 路徑語言](functions-json/functions-sqljson-path.md#functions-sqljson-path)

[9.16.3. SQL/JSON 查詢函式](functions-json/sqljson-query-functions.md#sqljson-query-functions)

[9.16.4. JSON_TABLE](functions-json.md#functions-sqljson-table)

<a id="id-1.5.8.22.2"></a><a id="id-1.5.8.22.3"></a>

本節說明：

* 用於處理與建立 JSON 資料的函式與運算子
* SQL/JSON 路徑語言
* SQL/JSON 查詢函式

為了在 SQL 環境中原生支援 JSON 資料型別，PostgreSQL 實作了 *SQL/JSON 資料模型*。這個模型由項目的序列所組成。每個項目可以存放 SQL 純量值（另外加上一個 SQL/JSON null 值），以及使用 JSON 陣列與物件的複合資料結構。這個模型是將 JSON 規格 [RFC 7159](https://datatracker.ietf.org/doc/html/rfc7159) 中隱含的資料模型加以形式化的結果。

SQL/JSON 讓你能夠在交易支援之下，將 JSON 資料與一般的 SQL 資料一併處理，包括：

* 將 JSON 資料上傳到資料庫，並以字元字串或二進位字串的形式儲存在一般的 SQL 欄位中。
* 從關聯式資料產生 JSON 物件與陣列。
* 使用 SQL/JSON 查詢函式與 SQL/JSON 路徑語言運算式來查詢 JSON 資料。

若要進一步了解 SQL/JSON 標準，請參閱 [[sqltr-19075-6]](../../bibliography.md#SQLTR-19075-6)。關於 PostgreSQL 所支援之 JSON 型別的詳細資訊，請參閱[第 8.14 節](../datatype/datatype-json.md)。

### 9.16.1. 處理與建立 JSON 資料 [#](#functions-json-processing) <a href="#functions-json-processing" id="functions-json-processing"></a>

完整內容請見 [9.16.1. 處理與建立 JSON 資料](functions-json/functions-json-processing.md#functions-json-processing)。

### 9.16.2. SQL/JSON 路徑語言 [#](#functions-sqljson-path) <a href="#functions-sqljson-path" id="functions-sqljson-path"></a>

完整內容請見 [9.16.2. SQL/JSON 路徑語言](functions-json/functions-sqljson-path.md#functions-sqljson-path)。

### 9.16.3. SQL/JSON 查詢函式 [#](#sqljson-query-functions) <a href="#sqljson-query-functions" id="sqljson-query-functions"></a>

完整內容請見 [9.16.3. SQL/JSON 查詢函式](functions-json/sqljson-query-functions.md#sqljson-query-functions)。

<a id="FUNCTIONS-SQLJSON-TABLE"></a>

### 9.16.4. JSON_TABLE [#](#functions-sqljson-table) <a href="#functions-sqljson-table" id="functions-sqljson-table"></a>

<a id="id-1.5.8.22.11.2"></a>

`JSON_TABLE` 是一個 SQL/JSON 函式，它會查詢 JSON 資料，並將結果呈現為關聯式檢視表，讓你可以像一般 SQL 資料表那樣存取。你可以在 `SELECT`、`UPDATE` 或 `DELETE` 的 `FROM` 子句中使用 `JSON_TABLE`，也可以在 `MERGE` 陳述句中將它作為資料來源。

`JSON_TABLE` 以 JSON 資料作為輸入，使用 JSON 路徑運算式擷取所提供資料的一部分，作為所建構之檢視表的*資料列模式*（row pattern）。由資料列模式所給出的每個 SQL/JSON 值，都會作為所建構檢視表中一個獨立資料列的來源。

為了將資料列模式拆分為欄位，`JSON_TABLE` 提供了 `COLUMNS` 子句，用來定義所建立之檢視表的綱要。對於每個欄位，可以指定一個獨立的 JSON 路徑運算式，針對資料列模式進行求值，以取得一個 SQL/JSON 值，該值將成為指定輸出資料列中指定欄位的值。

儲存在資料列模式之巢狀層級中的 JSON 資料，可以使用 `NESTED PATH` 子句擷取。每個 `NESTED PATH` 子句都可以使用資料列模式某個巢狀層級的資料，產生一個或多個欄位。這些欄位可以使用外觀類似於最上層 COLUMNS 子句的 `COLUMNS` 子句來指定。由 NESTED COLUMNS 建構的資料列稱為*子資料列*（child row），它們會與由上層 `COLUMNS` 子句所指定之欄位建構出的資料列聯結，以得到最終檢視表中的資料列。子欄位本身也可以包含 `NESTED PATH` 規格，因此可以擷取位於任意巢狀層級的資料。在同一層級由多個 `NESTED PATH` 產生的欄位，彼此被視為*兄弟*（sibling），而它們與上層資料列聯結後的資料列會使用 UNION 加以合併。

`JSON_TABLE` 產生的資料列會以 lateral 方式聯結到產生它們的資料列，因此你不必明確地將所建構的檢視表與存放 JSON 資料的原始資料表進行聯結。

語法為：

```

JSON_TABLE (
    context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...] ]
    COLUMNS ( json_table_column [, ...] )
    [ { ERROR | EMPTY [ARRAY]} ON ERROR ]
)


where json_table_column is:

  name FOR ORDINALITY
  | name type
        [ FORMAT JSON [ENCODING UTF8]]
        [ PATH path_expression ]
        [ { WITHOUT | WITH { CONDITIONAL | [UNCONDITIONAL] } } [ ARRAY ] WRAPPER ]
        [ { KEEP | OMIT } QUOTES [ ON SCALAR STRING ] ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON EMPTY ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON ERROR ]
  | name type EXISTS [ PATH path_expression ]
        [ { ERROR | TRUE | FALSE | UNKNOWN } ON ERROR ]
  | NESTED [ PATH ] path_expression [ AS json_path_name ] COLUMNS ( json_table_column [, ...] )
```

下面會更詳細地說明每個語法元素。

`context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...]]`
:   *`context_item`* 指定要查詢的輸入文件，*`path_expression`* 是定義查詢的 SQL/JSON 路徑運算式，而 *`json_path_name`* 則是 *`path_expression`* 的選用名稱。選用的 `PASSING` 子句為 *`path_expression`* 中提到的變數提供資料值。使用上述元素對輸入資料求值的結果稱為*資料列模式*，用來作為所建構之檢視表中資料列值的來源。

`COLUMNS` ( *`json_table_column`* [, ...] )

`COLUMNS` 子句定義所建構之檢視表的綱要。在這個子句中，你可以指定每個欄位要填入的 SQL/JSON 值，該值是透過針對資料列模式套用 JSON 路徑運算式所取得。*`json_table_column`* 有下列幾種變形：

- *`name`* `FOR ORDINALITY`

  加入一個序數欄位，提供從 1 開始的循序資料列編號。每個 `NESTED PATH`（見下文）對於其中任何巢狀的序數欄位，都有自己的計數器。

- `name type [FORMAT JSON [ENCODING UTF8]] [ PATH path_expression ]`

  將針對資料列模式套用 *`path_expression`* 所取得的 SQL/JSON 值，強制轉換為指定的 *`type`* 之後，插入檢視表的輸出資料列中。

  指定 `FORMAT JSON` 可明確表示你預期該值是有效的 `json` 物件。只有當 *`type`* 是 `bpchar`、`bytea`、`character varying`、`name`、`json`、`jsonb`、`text` 之一，或是以這些型別為基礎的領域（domain）時，指定 `FORMAT JSON` 才有意義。

  你可以選擇性地指定 `WRAPPER` 與 `QUOTES` 子句來格式化輸出。請注意，如果同時指定了 `OMIT QUOTES` 與 `FORMAT JSON`，前者會覆寫後者，因為沒有加引號的字面值並不構成有效的 `json` 值。

  你可以選擇性地使用 `ON EMPTY` 與 `ON ERROR` 子句，分別指定當 JSON 路徑求值的結果為空時，以及當 JSON 路徑求值期間或將 SQL/JSON 值強制轉換為指定型別時發生錯誤時，要拋出錯誤還是回傳指定的值。兩者的預設都是回傳 `NULL` 值。

  **注意**

  這個子句在內部會被轉換為 `JSON_VALUE` 或 `JSON_QUERY`，並具有與其相同的語意。如果指定的型別不是純量型別，或是出現了 `FORMAT JSON`、`WRAPPER` 或 `QUOTES` 子句中的任何一個，就會轉換為後者。

- *`name`* *`type`* `EXISTS` [ `PATH` *`path_expression`* ]

  將針對資料列模式套用 *`path_expression`* 所取得的布林值，強制轉換為指定的 *`type`* 之後，插入檢視表的輸出資料列中。

  該值對應於將 `PATH` 運算式套用到資料列模式後，是否產生任何值。

  指定的 *`type`* 應該要有從 `boolean` 型別轉換過來的型別轉換。

  你可以選擇性地使用 `ON ERROR`，指定當 JSON 路徑求值期間或將 SQL/JSON 值強制轉換為指定型別時發生錯誤時，要拋出錯誤還是回傳指定的值。預設是回傳布林值 `FALSE`。

  **注意**

  這個子句在內部會被轉換為 `JSON_EXISTS`，並具有與其相同的語意。

- `NESTED [ PATH ]` *`path_expression`* [ `AS` *`json_path_name`* ] `COLUMNS` ( *`json_table_column`* [, ...] )

  從資料列模式的巢狀層級中擷取 SQL/JSON 值，依照 `COLUMNS` 子子句的定義產生一個或多個欄位，並將擷取出的 SQL/JSON 值插入這些欄位中。`COLUMNS` 子子句中的 *`json_table_column`* 運算式，使用與上層 `COLUMNS` 子句相同的語法。

  `NESTED PATH` 語法是遞迴的，因此你可以透過將數個 `NESTED PATH` 子子句彼此巢狀指定，向下深入多個巢狀層級。它讓你能夠在單一的函式呼叫中，將 JSON 物件與陣列的階層結構展開，而不必在 SQL 陳述句中串接多個 `JSON_TABLE` 運算式。

**注意**

在上述 *`json_table_column`* 的每一種變形中，如果省略了 `PATH` 子句，就會使用路徑運算式 `$.name`，其中 *`name`* 是所提供的欄位名稱。

`AS` *`json_path_name`*
:   選用的 *`json_path_name`* 作為所提供之 *`path_expression`* 的識別符號。這個名稱必須是唯一的，且不得與欄位名稱相同。

{ `ERROR` | `EMPTY` } `ON ERROR`
:   選用的 `ON ERROR` 可用來指定在對最上層 *`path_expression`* 求值時如何處理錯誤。如果你希望拋出錯誤，請使用 `ERROR`；若要回傳空的資料表，也就是包含 0 筆資料列的資料表，請使用 `EMPTY`。請注意，這個子句不會影響對欄位求值時發生的錯誤，那些錯誤的行為取決於是否針對該欄位指定了 `ON ERROR` 子句。

範例

在接下來的範例中，將會使用下面這個包含 JSON 資料的資料表：

```

CREATE TABLE my_films ( js jsonb );

INSERT INTO my_films VALUES (
'{ "favorites" : [
   { "kind" : "comedy", "films" : [
     { "title" : "Bananas",
       "director" : "Woody Allen"},
     { "title" : "The Dinner Game",
       "director" : "Francis Veber" } ] },
   { "kind" : "horror", "films" : [
     { "title" : "Psycho",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "thriller", "films" : [
     { "title" : "Vertigo",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "drama", "films" : [
     { "title" : "Yojimbo",
       "director" : "Akira Kurosawa" } ] }
  ] }');
```

下面的查詢展示了如何使用 `JSON_TABLE`，將 `my_films` 資料表中的 JSON 物件轉換為一個檢視表，其中包含原始 JSON 中的鍵 `kind`、`title` 與 `director` 所對應的欄位，以及一個序數欄位：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*]' COLUMNS (
   id FOR ORDINALITY,
   kind text PATH '$.kind',
   title text PATH '$.films[*].title' WITH WRAPPER,
   director text PATH '$.films[*].director' WITH WRAPPER)) AS jt;
```

```

 id |   kind   |             title              |             director
----+----------+--------------------------------+----------------------------------
  1 | comedy   | ["Bananas", "The Dinner Game"] | ["Woody Allen", "Francis Veber"]
  2 | horror   | ["Psycho"]                     | ["Alfred Hitchcock"]
  3 | thriller | ["Vertigo"]                    | ["Alfred Hitchcock"]
  4 | drama    | ["Yojimbo"]                    | ["Akira Kurosawa"]
(4 rows)
```

下面是上述查詢的修改版本，展示了在最上層 JSON 路徑運算式所指定的篩選中使用 `PASSING` 引數，以及個別欄位的各種選項：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
     COLUMNS (
     id FOR ORDINALITY,
     kind text PATH '$.kind',
     title text FORMAT JSON PATH '$.films[*].title' OMIT QUOTES,
     director text PATH '$.films[*].director' KEEP QUOTES)) AS jt;
```

```

 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

下面是上述查詢的修改版本，展示了使用 `NESTED PATH` 來填入 title 與 director 欄位，說明它們如何與上層的 id 與 kind 欄位聯結：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```

 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

下面是相同的查詢，但在根路徑中沒有篩選：

```

SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*]'
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```

 id |   kind   |      title      |      director
----+----------+-----------------+--------------------
  1 | comedy   | Bananas         | "Woody Allen"
  1 | comedy   | The Dinner Game | "Francis Veber"
  2 | horror   | Psycho          | "Alfred Hitchcock"
  3 | thriller | Vertigo         | "Alfred Hitchcock"
  4 | drama    | Yojimbo         | "Akira Kurosawa"
(5 rows)
```

下面展示了另一個使用不同 `JSON` 物件作為輸入的查詢。它展示了 `NESTED` 路徑 `$.movies[*]` 與 `$.books[*]` 之間的 UNION「兄弟聯結」（sibling join），以及在 `NESTED` 層級使用 `FOR ORDINALITY` 欄位（欄位 `movie_id`、`book_id` 與 `author_id`）：

```

SELECT * FROM JSON_TABLE (
'{"favorites":
    [{"movies":
      [{"name": "One", "director": "John Doe"},
       {"name": "Two", "director": "Don Joe"}],
     "books":
      [{"name": "Mystery", "authors": [{"name": "Brown Dan"}]},
       {"name": "Wonder", "authors": [{"name": "Jun Murakami"}, {"name":"Craig Doe"}]}]
}]}'::json, '$.favorites[*]'
COLUMNS (
  user_id FOR ORDINALITY,
  NESTED '$.movies[*]'
    COLUMNS (
    movie_id FOR ORDINALITY,
    mname text PATH '$.name',
    director text),
  NESTED '$.books[*]'
    COLUMNS (
      book_id FOR ORDINALITY,
      bname text PATH '$.name',
      NESTED '$.authors[*]'
        COLUMNS (
          author_id FOR ORDINALITY,
          author_name text PATH '$.name'))));
```

```

 user_id | movie_id | mname | director | book_id |  bname  | author_id | author_name
---------+----------+-------+----------+---------+---------+-----------+--------------
       1 |        1 | One   | John Doe |         |         |           |
       1 |        2 | Two   | Don Joe  |         |         |           |
       1 |          |       |          |       1 | Mystery |         1 | Brown Dan
       1 |          |       |          |       2 | Wonder  |         1 | Jun Murakami
       1 |          |       |          |       2 | Wonder  |         2 | Craig Doe
(5 rows)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-json.html)（原文版本：18.6；核對日期：2026-09-11）
