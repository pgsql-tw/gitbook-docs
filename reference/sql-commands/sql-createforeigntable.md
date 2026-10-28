<a id="SQL-CREATEFOREIGNTABLE"></a><a id="id-1.9.3.66.1"></a>

## CREATE FOREIGN TABLE

CREATE FOREIGN TABLE — 定義新的外部資料表

<a id="id-1.9.3.66.4"></a>

## 語法

```

CREATE FOREIGN TABLE [ IF NOT EXISTS ] table_name ( [
  { column_name data_type [ OPTIONS ( option 'value' [, ... ] ) ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
] )
[ INHERITS ( parent_table [, ... ] ) ]
  SERVER server_name
[ OPTIONS ( option 'value' [, ... ] ) ]

CREATE FOREIGN TABLE [ IF NOT EXISTS ] table_name
  PARTITION OF parent_table [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ]
{ FOR VALUES partition_bound_spec | DEFAULT }
  SERVER server_name
[ OPTIONS ( option 'value' [, ... ] ) ]

where column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL [ NO INHERIT ] |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ] }
[ ENFORCED | NOT ENFORCED ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{  NOT NULL column_name [ NO INHERIT ] |
   CHECK ( expression ) [ NO INHERIT ] }
[ ENFORCED | NOT ENFORCED ]

and like_option is:

{ INCLUDING | EXCLUDING } { COMMENTS | CONSTRAINTS | DEFAULTS | GENERATED | STATISTICS | ALL }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )
```

<a id="SQL-CREATEFOREIGNTABLE-DESCRIPTION"></a>

## 說明

`CREATE FOREIGN TABLE` 會在目前的資料庫中建立新的外部資料表。該資料表的擁有者會是執行此命令的使用者。

若有提供綱要名稱（例如 `CREATE FOREIGN TABLE
myschema.mytable ...`），資料表會建立在指定的綱要中；否則會建立在目前的綱要中。外部資料表的名稱必須與同一綱要中任何其他關聯（資料表、序列、索引、檢視表、具體化檢視表或外部資料表）的名稱不同。

`CREATE FOREIGN TABLE` 也會自動建立一個資料型別，代表與外部資料表的一筆資料列相對應的複合型別。因此，外部資料表不能與同一綱要中任何現有的資料型別同名。

若指定了 `PARTITION OF` 子句，資料表會建立為 `parent_table` 的分割區，並具有指定的邊界。

要建立外部資料表，你必須在外部伺服器上具有 `USAGE` 權限，並且在資料表中使用的所有欄位型別上具有 `USAGE` 權限。

<a id="id-1.9.3.66.6"></a>

## 參數

`IF NOT EXISTS`
:   若已存在同名的關聯，不擲出錯誤；此情況會發出 notice。請注意，並不保證現有的關聯與原本會建立的關聯有任何相似之處。

*`table_name`*
:   要建立之資料表的名稱（可選擇以綱要限定）。

*`column_name`*
:   要在新資料表中建立之欄位的名稱。

*`data_type`*
:   欄位的資料型別。這可以包含陣列指定符。關於 PostgreSQL 所支援之資料型別的更多資訊，請參閱[第 8 章](../../the-sql-language/datatype/README.md)。

`COLLATE collation`
:   `COLLATE` 子句會為欄位指定定序（該欄位必須是可定序的資料型別）。若未指定，則使用欄位資料型別的預設定序。

`INHERITS ( parent_table [, ... ] )`
:   選用的 `INHERITS` 子句指定一份資料表清單，新的外部資料表會自動繼承這些資料表的所有欄位。父資料表可以是一般資料表或外部資料表。更多細節請參閱 [`CREATE TABLE`](sql-createtable.md) 的類似形式。

`PARTITION OF parent_table { FOR VALUES partition_bound_spec | DEFAULT }`
:   此形式可用來將外部資料表建立為指定父資料表的分割區，並具有指定的分割區邊界值。更多細節請參閱 [`CREATE TABLE`](sql-createtable.md) 的類似形式。請注意，若父資料表上有 `UNIQUE` 索引，目前不允許將外部資料表建立為該父資料表的分割區。（另請參閱 [`ALTER TABLE ATTACH PARTITION`](sql-altertable.md)。）

`LIKE source_table [ like_option ... ]`
:   `LIKE` 子句指定一個資料表，新資料表會自動從該資料表複製所有欄位名稱、其資料型別，以及其非 NULL 限制條件。

    與 `INHERITS` 不同，新資料表與原始資料表在建立完成後就完全脫鉤。對原始資料表的變更不會套用到新資料表，而且也無法在掃描原始資料表時納入新資料表的資料。

    同樣與 `INHERITS` 不同的是，由 `LIKE` 複製的欄位與限制條件，不會與名稱相似的欄位與限制條件合併。若同一個名稱被明確指定，或在另一個 `LIKE` 子句中指定，就會發出錯誤。

    選用的 *`like_option`* 子句指定要複製原始資料表的哪些額外屬性。指定 `INCLUDING` 會複製該屬性，指定 `EXCLUDING` 則會略過該屬性。`EXCLUDING` 是預設值。若對同一種物件做了多個指定，則使用最後一個。可用的選項有：

    `INCLUDING COMMENTS`
    :   複製之欄位、限制條件與擴充統計資訊的註解會被複製。預設行為是排除註解，使新資料表中對應的物件沒有註解。

    `INCLUDING CONSTRAINTS`
    :   會複製 `CHECK` 限制條件。欄位限制條件與資料表限制條件之間不做區分。非 NULL 限制條件一律會複製到新資料表。

    `INCLUDING DEFAULTS`
    :   會複製所複製之欄位定義的預設值運算式。否則不會複製預設值運算式，使新資料表中所複製的欄位以 NULL 為預設值。請注意，複製呼叫資料庫修改函式（例如 `nextval`）的預設值，可能會在原始資料表與新資料表之間建立功能上的連結。

    `INCLUDING GENERATED`
    :   會複製所複製之欄位定義的任何產生運算式。預設情況下，新欄位會是一般的基本欄位。

    `INCLUDING STATISTICS`
    :   擴充統計資訊會複製到新資料表。

    `INCLUDING ALL`
    :   `INCLUDING ALL` 是選取所有可用個別選項的簡寫形式。（在 `INCLUDING ALL` 之後撰寫個別的 `EXCLUDING` 子句，以選取除了某些特定選項以外的所有選項，可能會很有用。）

`CONSTRAINT constraint_name`
:   欄位限制條件或資料表限制條件的選用名稱。若違反限制條件，限制條件名稱會出現在錯誤訊息中，因此可以使用像 `col must be positive` 這樣的限制條件名稱，向用戶端應用程式傳達有用的限制條件資訊。（要指定包含空格的限制條件名稱，需要使用雙引號。）若未指定限制條件名稱，系統會產生一個名稱。

`NOT NULL` [ NO INHERIT ]

該欄位不允許包含 NULL 值。

標記為 `NO INHERIT` 的限制條件不會傳播到子資料表。

`NULL`

該欄位允許包含 NULL 值。這是預設行為。

提供此子句只是為了與非標準的 SQL 資料庫相容。不建議在新的應用程式中使用它。

`CHECK ( expression ) [ NO INHERIT ]`

`CHECK` 子句指定一個產生布林結果的運算式，外部資料表中的每一筆資料列都應該滿足此運算式；也就是說，對於外部資料表中的所有資料列，此運算式應該產生 TRUE 或 UNKNOWN，絕不能產生 FALSE。指定為欄位限制條件的檢查限制條件應該只參照該欄位的值，而出現在資料表限制條件中的運算式則可以參照多個欄位。

目前，`CHECK` 運算式既不能包含子查詢，也不能參照目前資料列之欄位以外的變數。可以參照系統欄位 `tableoid`，但不能參照任何其他系統欄位。

標記為 `NO INHERIT` 的限制條件不會傳播到子資料表。

`DEFAULT default_expr`

`DEFAULT` 子句會為其所在欄位定義的欄位指定預設資料值。該值可以是任何不含變數的運算式（不允許子查詢，也不允許交互參照目前資料表中的其他欄位）。預設值運算式的資料型別必須與欄位的資料型別相符。

任何未對該欄位指定值的插入操作，都會使用預設值運算式。若欄位沒有預設值，則預設值為 NULL。

`GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ]`<a id="id-1.9.3.66.6.2.14.1.2"></a>

此子句會將欄位建立為*產生欄位*。該欄位無法寫入，讀取時會傳回指定運算式的結果。

指定 `VIRTUAL` 時，欄位會在讀取時計算。（外部資料包裝器在新資料列中會將它視為 NULL 值，並可能選擇將它儲存為 NULL 值，或完全忽略它。）指定 `STORED` 時，欄位會在寫入時計算。（計算出的值會提供給外部資料包裝器儲存，且在讀取時必須傳回。）`VIRTUAL` 是預設值。

產生運算式可以參照資料表中的其他欄位，但不能參照其他產生欄位。所使用的任何函式與運算子都必須是不可變的（immutable）。不允許參照其他資料表。

*`server_name`*
:   外部資料表所要使用之現有外部伺服器的名稱。關於定義伺服器的細節，請參閱 [CREATE SERVER](sql-createserver.md)。

`OPTIONS ( option 'value' [, ...] )`
:   要與新外部資料表或其某個欄位相關聯的選項。允許的選項名稱與值是各個外部資料包裝器專屬的，並由該外部資料包裝器的驗證函式進行驗證。不允許重複的選項名稱（不過資料表選項與欄位選項同名是可以的）。

<a id="id-1.9.3.66.7"></a>

## 注意事項

外部資料表上的限制條件（例如 `CHECK` 或 `NOT NULL` 子句）不會由 PostgreSQL 核心系統強制執行，而且大多數外部資料包裝器也不會嘗試強制執行它們；也就是說，限制條件只是被假設為成立。這種強制執行沒有什麼意義，因為它只會套用到透過外部資料表插入或更新的資料列，而不會套用到以其他方式（例如直接在遠端伺服器上）修改的資料列。相反地，外部資料表上附加的限制條件應該代表由遠端伺服器強制執行的限制條件。

某些特殊用途的外部資料包裝器，可能是存取其資料的唯一機制；在這種情況下，由外部資料包裝器本身執行限制條件的強制檢查可能是合適的。但除非包裝器的文件有此說明，否則你不應該假設它會這麼做。

雖然 PostgreSQL 不會嘗試強制執行外部資料表上的限制條件，但它確實會為了查詢最佳化的目的，假設這些限制條件是正確的。若外部資料表中有可見的資料列不滿足所宣告的限制條件，對該資料表的查詢可能會產生錯誤或不正確的答案。確保限制條件定義與實際情況相符，是使用者的責任。

<a id="id-1.9.3.66.7.5"></a>

### 小心

當外部資料表被用作分割資料表的分割區時，會有一個隱含的限制條件：其內容必須滿足分割規則。同樣地，確保這一點成立是使用者的責任，最好的做法是在遠端伺服器上設置相符的限制條件。

在包含外部資料表分割區的分割資料表中，若外部資料包裝器支援資料列路由，變更分割鍵值的 `UPDATE` 可以使資料列從本機分割區移動到外部資料表分割區。然而，目前無法將資料列從外部資料表分割區移動到另一個分割區。需要這麼做的 `UPDATE` 會因分割限制條件而失敗，前提是該限制條件已由遠端伺服器正確強制執行。

類似的考量也適用於產生欄位。儲存式產生欄位會在本機 PostgreSQL 伺服器上於插入或更新時計算，並交給外部資料包裝器寫出到外部資料儲存區，但並不強制要求對外部資料表的查詢所傳回之儲存式產生欄位的值與產生運算式一致。同樣地，這可能導致不正確的查詢結果。

<a id="SQL-CREATEFOREIGNTABLE-EXAMPLES"></a>

## 範例

建立外部資料表 `films`，它將透過伺服器 `film_server` 存取：

```

CREATE FOREIGN TABLE films (
    code        char(5) NOT NULL,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
)
SERVER film_server;
```

建立外部資料表 `measurement_y2016m07`，它將透過伺服器 `server_07` 存取，並作為範圍分割資料表 `measurement` 的分割區：

```

CREATE FOREIGN TABLE measurement_y2016m07
    PARTITION OF measurement FOR VALUES FROM ('2016-07-01') TO ('2016-08-01')
    SERVER server_07;
```

<a id="SQL-CREATEFOREIGNTABLE-COMPATIBILITY"></a>

## 相容性

`CREATE FOREIGN TABLE` 命令大致符合 SQL 標準；不過，如同 [`CREATE TABLE`](sql-createtable.md) 一樣，它允許 `NULL` 限制條件與零欄位的外部資料表。指定欄位預設值的能力也是 PostgreSQL 的擴充語法。PostgreSQL 所定義形式的資料表繼承是非標準的。此命令所支援的 `LIKE` 子句是非標準的。

<a id="id-1.9.3.66.10"></a>

## 另請參閱

[ALTER FOREIGN TABLE](sql-alterforeigntable.md), [DROP FOREIGN TABLE](sql-dropforeigntable.md), [CREATE TABLE](sql-createtable.md), [CREATE SERVER](sql-createserver.md), [IMPORT FOREIGN SCHEMA](sql-importforeignschema.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createforeigntable.html)（原文版本：18.6；核對日期：2026-10-04）
