<a id="SQL-CREATETABLE"></a><a id="id-1.9.3.85.1"></a>

## CREATE TABLE

CREATE TABLE — 定義新的資料表

<a id="id-1.9.3.85.4"></a>

## 語法

```

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name ( [
  { column_name data_type [ STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT } ] [ COMPRESSION compression_method ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
] )
[ INHERITS ( parent_table [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    OF type_name [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    PARTITION OF parent_table [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ] { FOR VALUES partition_bound_spec | DEFAULT }
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

where column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL [ NO INHERIT ]  |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ] |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters |
  PRIMARY KEY index_parameters |
  REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{ CHECK ( expression ) [ NO INHERIT ] |
  NOT NULL column_name [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  PRIMARY KEY ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
  FOREIGN KEY ( column_name [, ... ] [, PERIOD column_name ] ) REFERENCES reftable [ ( refcolumn [, ... ] [, PERIOD refcolumn ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and like_option is:

{ INCLUDING | EXCLUDING } { COMMENTS | COMPRESSION | CONSTRAINTS | DEFAULTS | GENERATED | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )

index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( column_name [, ... ] ) ]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
[ USING INDEX TABLESPACE tablespace_name ]

exclude_element in an EXCLUDE constraint is:

{ column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

referential_action in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( column_name [, ... ] ) ] | SET DEFAULT [ ( column_name [, ... ] ) ] }
```

<a id="SQL-CREATETABLE-DESCRIPTION"></a>

## 說明

`CREATE TABLE` 會在目前的資料庫中建立一個新的、初始為空的資料表。該資料表的擁有者是發出此命令的使用者。

若指定了綱要名稱（例如 `CREATE TABLE
myschema.mytable ...`），資料表就會建立在指定的綱要中；否則會建立在目前的綱要中。暫存資料表存在於一個特殊的綱要中，因此建立暫存資料表時不能指定綱要名稱。資料表的名稱必須與同一綱要中任何其他關聯（資料表、序列、索引、檢視表、具體化檢視表或外部資料表）的名稱不同。

`CREATE TABLE` 也會自動建立一個資料型別，表示對應於該資料表一個資料列的複合型別。因此，資料表不能與同一綱要中任何現有的資料型別同名。

選用的限制條件子句指定了新增或更新的資料列必須滿足的限制條件（檢驗），插入或更新操作才能成功。限制條件是一種 SQL 物件，以各種方式協助定義資料表中有效值的集合。

定義限制條件的方式有兩種：資料表限制條件與欄位限制條件。欄位限制條件是作為欄位定義的一部分來定義的。資料表限制條件的定義不與特定欄位綁定，而且可以涵蓋超過一個欄位。每個欄位限制條件也都可以寫成資料表限制條件；欄位限制條件只是在限制條件僅影響一個欄位時使用的簡便寫法。

要能建立資料表，你必須分別擁有所有欄位型別或 `OF` 子句中型別的 `USAGE` 權限。

<a id="id-1.9.3.85.6"></a>

## 參數

<a id="SQL-CREATETABLE-TEMPORARY"></a>

`TEMPORARY` 或 `TEMP` [#](#SQL-CREATETABLE-TEMPORARY)
:   若有指定，資料表會建立為暫存資料表。暫存資料表會在工作階段結束時自動移除，或者也可選擇在目前交易結束時移除（請參閱下方的 `ON COMMIT`）。預設的 search_path 會先包含暫存綱要，因此當暫存資料表存在時，同名的現有永久資料表不會被新的查詢計畫選用，除非以綱要限定的名稱參照它們。在暫存資料表上建立的任何索引也會自動成為暫存的。

    [autovacuum 常駐程式](../../server-administration/maintenance/routine-vacuuming.md#AUTOVACUUM)無法存取暫存資料表，因此也無法對其執行 vacuum 或 analyze。基於這個原因，應該透過工作階段中的 SQL 命令執行適當的 vacuum 與 analyze 操作。例如，若暫存資料表將用於複雜的查詢，明智的做法是在填入資料後對該暫存資料表執行 `ANALYZE`。

    可以選擇在 `TEMPORARY` 或 `TEMP` 之前寫上 `GLOBAL` 或 `LOCAL`。這在 PostgreSQL 中目前沒有任何差別，且已不建議使用；請參閱下方的[相容性](sql-createtable.md#SQL-CREATETABLE-COMPATIBILITY)。
<a id="SQL-CREATETABLE-UNLOGGED"></a>

`UNLOGGED` [#](#SQL-CREATETABLE-UNLOGGED)
:   若有指定，資料表會建立為無日誌資料表。寫入無日誌資料表的資料不會寫入預寫式日誌（請參閱[第 28 章](../../server-administration/wal/README.md)），因此它們比一般資料表快得多。不過，它們並不具備當機安全性：無日誌資料表會在當機或非正常關閉後自動被截斷。無日誌資料表的內容也不會複寫到備用伺服器。在無日誌資料表上建立的任何索引也會自動成為無日誌的。

    若有指定此選項，與無日誌資料表一併建立的任何序列（用於識別欄位或 serial 欄位）也會建立為無日誌的。

    分割資料表不支援此形式。
<a id="SQL-CREATETABLE-PARMS-IF-NOT-EXISTS"></a>

`IF NOT EXISTS` [#](#SQL-CREATETABLE-PARMS-IF-NOT-EXISTS)
:   若已存在同名的關聯，不擲出錯誤；此情況會發出 notice。請注意，並不保證現有的關聯與原本會建立的關聯有任何相似之處。
<a id="SQL-CREATETABLE-PARMS-TABLE-NAME"></a>

*`table_name`* [#](#SQL-CREATETABLE-PARMS-TABLE-NAME)
:   要建立的資料表名稱（可選擇以綱要限定）。
<a id="SQL-CREATETABLE-PARMS-TYPE-NAME"></a>

`OF type_name` [#](#SQL-CREATETABLE-PARMS-TYPE-NAME)
:   建立一個*型別化資料表*（typed table），其結構取自指定的獨立複合型別（也就是使用 [CREATE TYPE](sql-createtype.md) 建立的複合型別），但它仍然會產生一個新的複合型別。該資料表會相依於所參照的型別，這表示對該型別進行的串聯修改與移除動作會傳遞到該資料表。

    型別化資料表的欄位名稱與資料型別一律與其衍生來源的型別相同，因此你不能指定額外的欄位。但 `CREATE TABLE` 命令可以為資料表加上預設值與限制條件，也可以指定儲存參數。
<a id="SQL-CREATETABLE-PARMS-COLUMN-NAME"></a>

*`column_name`* [#](#SQL-CREATETABLE-PARMS-COLUMN-NAME)
:   要在新資料表中建立的欄位名稱。
<a id="SQL-CREATETABLE-PARMS-DATA-TYPE"></a>

*`data_type`* [#](#SQL-CREATETABLE-PARMS-DATA-TYPE)
:   欄位的資料型別。這可以包含陣列指定子。關於 PostgreSQL 所支援資料型別的更多資訊，請參閱[第 8 章](../../the-sql-language/datatype/README.md)。
<a id="SQL-CREATETABLE-PARMS-COLLATE"></a>

`COLLATE collation` [#](#SQL-CREATETABLE-PARMS-COLLATE)
:   `COLLATE` 子句為欄位指定定序（該欄位必須是可定序的資料型別）。若未指定，則使用該欄位資料型別的預設定序。
<a id="SQL-CREATETABLE-PARMS-STORAGE"></a>

`STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }` <a id="id-1.9.3.85.6.2.9.1.2"></a> [#](#SQL-CREATETABLE-PARMS-STORAGE)
:   此形式設定欄位的儲存模式。它控制此欄位是以內嵌方式保存，還是保存在次要的 TOAST 資料表中，以及資料是否要壓縮。`PLAIN` 必須用於固定長度的值，例如 `integer`，它是內嵌、不壓縮的。`MAIN` 用於內嵌、可壓縮的資料。`EXTERNAL` 用於外部、不壓縮的資料，而 `EXTENDED` 用於外部、壓縮的資料。寫 `DEFAULT` 會將儲存模式設為該欄位資料型別的預設模式。對大多數支援非 `PLAIN` 儲存的資料型別而言，`EXTENDED` 是預設值。使用 `EXTERNAL` 會讓對非常大的 `text` 與 `bytea` 值所做的子字串操作執行得更快，代價是增加儲存空間。更多資訊請參閱[第 66.2 節](../../internals/storage/storage-toast.md)。
<a id="SQL-CREATETABLE-PARMS-COMPRESSION"></a>

`COMPRESSION compression_method` [#](#SQL-CREATETABLE-PARMS-COMPRESSION)
:   `COMPRESSION` 子句設定欄位的壓縮方法。只有變動寬度的資料型別支援壓縮，而且只在欄位的儲存模式為 `main` 或 `extended` 時才會使用。（關於欄位儲存模式的資訊，請參閱 [ALTER TABLE](sql-altertable.md)。）為分割資料表設定此屬性沒有直接效果，因為這類資料表本身沒有儲存空間，但所設定的值會由新建立的分割區繼承。支援的壓縮方法為 `pglz` 與 `lz4`。（只有在建置 PostgreSQL 時使用了 `--with-lz4`，`lz4` 才可使用。）此外，*`compression_method`* 可以是 `default`，用以明確指定預設行為，也就是在插入資料時參考 [default_toast_compression](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION) 設定來決定要使用的方法。
<a id="SQL-CREATETABLE-PARMS-INHERITS"></a>

`INHERITS ( parent_table [, ... ] )` [#](#SQL-CREATETABLE-PARMS-INHERITS)
:   選用的 `INHERITS` 子句指定一份資料表清單，新資料表會自動從這些資料表繼承所有欄位。父資料表可以是一般資料表或外部資料表。

    使用 `INHERITS` 會在新的子資料表與其父資料表之間建立持續的關係。對父資料表的綱要修改通常也會傳遞到子資料表，而且預設情況下，子資料表的資料會包含在對父資料表的掃描中。

    若同一個欄位名稱存在於超過一個父資料表中，除非這些欄位在每個父資料表中的資料型別都相符，否則會回報錯誤。若沒有衝突，重複的欄位會合併成新資料表中的單一欄位。若新資料表的欄位名稱清單包含一個也被繼承的欄位名稱，其資料型別同樣必須與繼承來的欄位相符，而這些欄位定義會合併為一個。若新資料表為該欄位明確指定了預設值，此預設值會覆寫該欄位繼承宣告中的任何預設值。否則，任何為該欄位指定預設值的父資料表都必須指定相同的預設值，否則會回報錯誤。

    `CHECK` 限制條件的合併方式基本上與欄位相同：若多個父資料表和／或新資料表定義中包含同名的 `CHECK` 限制條件，這些限制條件必須都具有相同的檢查運算式，否則會回報錯誤。名稱與運算式都相同的限制條件會合併為一份。父資料表中標記為 `NO INHERIT` 的限制條件不會被納入考慮。請注意，新資料表中未命名的 `CHECK` 限制條件永遠不會被合併，因為系統一律會為它選擇一個唯一的名稱。

    欄位的 `STORAGE` 設定也會從父資料表複製過來。

    若父資料表中的某個欄位是識別欄位，該屬性不會被繼承。如有需要，可以將子資料表中的欄位宣告為識別欄位。
<a id="SQL-CREATETABLE-PARMS-PARTITION-BY"></a>

`PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ opclass ] [, ...] )` [#](#SQL-CREATETABLE-PARMS-PARTITION-BY)
:   選用的 `PARTITION BY` 子句指定資料表的分割策略。如此建立的資料表稱為*分割*資料表。以括號括起的欄位或運算式清單構成資料表的*分割鍵*。使用範圍分割或雜湊分割時，分割鍵可以包含多個欄位或運算式（最多 32 個，但這個限制可以在建置 PostgreSQL 時更改），但對於清單分割，分割鍵必須只由單一欄位或運算式組成。

    範圍分割與清單分割需要 btree 運算子類別，而雜湊分割需要 hash 運算子類別。若沒有明確指定運算子類別，就會使用適當型別的預設運算子類別；若不存在預設運算子類別，則會引發錯誤。使用雜湊分割時，所使用的運算子類別必須實作支援函式 2（詳細資訊請參閱[第 36.16.3 節](../../server-programming/extend/xindex.md#XINDEX-SUPPORT)）。

    分割資料表會被劃分為子資料表（稱為分割區），這些子資料表是使用個別的 `CREATE TABLE` 命令建立的。分割資料表本身是空的。插入資料表的資料列會根據分割鍵中欄位或運算式的值，被導向某個分割區。若沒有任何現有分割區符合新資料列中的值，就會回報錯誤。

    關於資料表分割的更多討論，請參閱[第 5.12 節](../../the-sql-language/ddl/ddl-partitioning.md)。
<a id="SQL-CREATETABLE-PARTITION"></a>

`PARTITION OF parent_table { FOR VALUES partition_bound_spec | DEFAULT }` [#](#SQL-CREATETABLE-PARTITION)
:   將資料表建立為指定父資料表的*分割區*。該資料表可以使用 `FOR VALUES` 建立為針對特定值的分割區，也可以使用 `DEFAULT` 建立為預設分割區。父資料表中存在的任何索引、限制條件以及使用者定義的資料列層級觸發程序，都會複製到新的分割區上。

    *`partition_bound_spec`* 必須對應於父資料表的分割方法與分割鍵，而且不得與該父資料表的任何現有分割區重疊。含 `IN` 的形式用於清單分割，含 `FROM` 與 `TO` 的形式用於範圍分割，而含 `WITH` 的形式用於雜湊分割。

    *`partition_bound_expr`* 是任何不含變數的運算式（不允許子查詢、視窗函式、彙總函式與傳回集合的函式）。其資料型別必須與對應分割鍵欄位的資料型別相符。該運算式會在建立資料表時求值一次，因此它甚至可以包含 volatile 運算式，例如 `CURRENT_TIMESTAMP`。

    建立清單分割區時，可以指定 `NULL`，表示該分割區允許分割鍵欄位為 null。不過，對於給定的父資料表，這樣的清單分割區不能超過一個。範圍分割區不能指定 `NULL`。

    建立範圍分割區時，以 `FROM` 指定的下界是包含性界限，而以 `TO` 指定的上界是排除性界限。也就是說，`FROM` 清單中指定的值是此分割區對應分割鍵欄位的有效值，而 `TO` 清單中的值則不是。請注意，這段敘述必須依照逐列比較的規則（[第 9.25.5 節](../../the-sql-language/functions/functions-comparisons.md#ROW-WISE-COMPARISON)）來理解。例如，給定 `PARTITION BY RANGE (x,y)`，分割區界限 `FROM (1, 2) TO (3, 4)` 允許 `x=1` 搭配任何 `y>=2`、`x=2` 搭配任何非 null 的 `y`，以及 `x=3` 搭配任何 `y<4`。

    建立範圍分割區時，可以使用特殊值 `MINVALUE` 與 `MAXVALUE`，表示該欄位的值沒有下界或上界。例如，使用 `FROM (MINVALUE) TO (10)` 定義的分割區允許任何小於 10 的值，而使用 `FROM (10) TO (MAXVALUE)` 定義的分割區允許任何大於或等於 10 的值。

    建立涉及超過一個欄位的範圍分割區時，將 `MAXVALUE` 用作下界的一部分、將 `MINVALUE` 用作上界的一部分也可能是合理的。例如，使用 `FROM (0, MAXVALUE) TO (10, MAXVALUE)` 定義的分割區允許第一個分割鍵欄位大於 0 且小於或等於 10 的任何資料列。同樣地，使用 `FROM ('a', MINVALUE) TO ('b', MINVALUE)` 定義的分割區允許第一個分割鍵欄位以 "a" 開頭的任何資料列。

    請注意，若分割界限的某一個欄位使用了 `MINVALUE` 或 `MAXVALUE`，則所有後續欄位都必須使用相同的值。例如，`(10, MINVALUE, 0)` 不是有效的界限；你應該寫成 `(10, MINVALUE, MINVALUE)`。

    另請注意，某些元素型別（例如 `timestamp`）具有 "infinity" 的概念，它只是另一個可以儲存的值。這與 `MINVALUE` 和 `MAXVALUE` 不同，它們並不是可以儲存的實際值，而是表示該值沒有界限的方式。可以將 `MAXVALUE` 視為大於任何其他值（包括 "infinity"），並將 `MINVALUE` 視為小於任何其他值（包括 "minus infinity"）。因此，範圍 `FROM ('infinity') TO (MAXVALUE)` 不是空範圍；它恰好允許儲存一個值——"infinity"。

    若指定了 `DEFAULT`，該資料表會建立為父資料表的預設分割區。雜湊分割的資料表無法使用此選項。不適合放入給定父資料表任何其他分割區的分割鍵值，會被導向預設分割區。

    當資料表已有一個 `DEFAULT` 分割區，又為它新增一個分割區時，必須掃描預設分割區，以確認其中不包含任何理應屬於新分割區的資料列。若預設分割區包含大量資料列，這可能會很慢。若預設分割區是外部資料表，或它具有一個能證明其不可能包含應放入新分割區之資料列的限制條件，則會略過此掃描。

    建立雜湊分割區時，必須指定模數與餘數。模數必須是正整數，餘數必須是小於模數的非負整數。一般而言，初次設定雜湊分割資料表時，你應該選擇等於分割區數量的模數，並為每個資料表指定相同的模數與不同的餘數（請參閱下方的範例）。不過，並不要求每個分割區都具有相同的模數，只要求雜湊分割資料表各分割區中出現的每個模數，都是下一個較大模數的因數。這使得分割區數量可以逐步增加，而不需要一次搬移所有資料。例如，假設你有一個具有 8 個分割區的雜湊分割資料表，每個分割區的模數都是 8，但發現有必要將分割區數量增加到 16。你可以分離其中一個模數為 8 的分割區，建立兩個涵蓋相同鍵空間部分的新模數 16 分割區（其中一個的餘數等於被分離分割區的餘數，另一個的餘數等於該值加 8），然後將資料重新填入它們。接著你可以對每個模數為 8 的分割區重複此步驟（或許在稍後的時間），直到全部處理完為止。雖然這在每個步驟中仍可能涉及大量的資料搬移，但仍比必須建立一個全新的資料表並一次搬移所有資料要好。

    分割區必須具有與其所屬分割資料表相同的欄位名稱與型別。對分割資料表欄位名稱或型別的修改，會自動傳遞到所有分割區。`CHECK` 限制條件會自動由每個分割區繼承，但個別分割區可以指定額外的 `CHECK` 限制條件；與父資料表中名稱和條件都相同的額外限制條件，會與父資料表的限制條件合併。每個分割區可以個別指定預設值。但請注意，透過分割資料表插入元組時，不會套用分割區的預設值。

    插入分割資料表的資料列會自動導向正確的分割區。若不存在合適的分割區，就會發生錯誤。

    像 `TRUNCATE` 這類通常會影響一個資料表及其所有繼承子資料表的操作，會串聯到所有分割區，但也可以在個別分割區上執行。

    請注意，使用 `PARTITION OF` 建立分割區需要取得父分割資料表上的 `ACCESS EXCLUSIVE` 鎖定。同樣地，使用 `DROP TABLE` 移除分割區需要取得父資料表上的 `ACCESS EXCLUSIVE` 鎖定。可以使用 [`ALTER
    TABLE ATTACH/DETACH PARTITION`](sql-altertable.md) 以較弱的鎖定來執行這些操作，從而減少對分割資料表上並行操作的干擾。
<a id="SQL-CREATETABLE-PARMS-LIKE"></a>

`LIKE source_table [ like_option ... ]` [#](#SQL-CREATETABLE-PARMS-LIKE)
:   `LIKE` 子句指定一個資料表，新資料表會自動從中複製所有欄位名稱、其資料型別以及其非 null 限制條件。

    與 `INHERITS` 不同，新資料表與原始資料表在建立完成後就完全脫鉤。對原始資料表的變更不會套用到新資料表，而且無法在對原始資料表的掃描中包含新資料表的資料。

    同樣與 `INHERITS` 不同的是，由 `LIKE` 複製的欄位與限制條件不會與名稱相似的欄位與限制條件合併。若明確指定了相同的名稱，或在另一個 `LIKE` 子句中指定了相同的名稱，就會發出錯誤。

    選用的 *`like_option`* 子句指定要複製原始資料表的哪些額外屬性。指定 `INCLUDING` 會複製該屬性，指定 `EXCLUDING` 則會省略該屬性。`EXCLUDING` 是預設值。若對同一類物件做了多次指定，則使用最後一個。可用的選項有：

    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-COMMENTS"></a>

    `INCLUDING COMMENTS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-COMMENTS)
    :   會複製所複製欄位、檢查限制條件、非 null 限制條件、索引與擴充統計資訊的註解。預設行為是排除註解，使新資料表中對應的物件沒有註解。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-COMPRESSION"></a>

    `INCLUDING COMPRESSION` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-COMPRESSION)
    :   會複製欄位的壓縮方法。預設行為是排除壓縮方法，使欄位具有預設的壓縮方法。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-CONSTRAINTS"></a>

    `INCLUDING CONSTRAINTS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-CONSTRAINTS)
    :   會複製 `CHECK` 限制條件。欄位限制條件與資料表限制條件之間不做區分。非 null 限制條件一律會複製到新資料表。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-DEFAULTS"></a>

    `INCLUDING DEFAULTS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-DEFAULTS)
    :   會複製所複製欄位定義的預設值運算式。否則不會複製預設值運算式，使新資料表中所複製的欄位具有 null 預設值。請注意，複製呼叫了修改資料庫之函式（例如 `nextval`）的預設值，可能會在原始資料表與新資料表之間建立功能上的連結。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-GENERATED"></a>

    `INCLUDING GENERATED` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-GENERATED)
    :   會複製所複製欄位定義的任何產生運算式，以及 stored／virtual 的選擇。預設情況下，新欄位會是一般的基本欄位。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-IDENTITY"></a>

    `INCLUDING IDENTITY` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-IDENTITY)
    :   會複製所複製欄位定義的任何識別規格。新資料表的每個識別欄位都會建立一個新的序列，與舊資料表所關聯的序列分開。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-INDEXES"></a>

    `INCLUDING INDEXES` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-INDEXES)
    :   原始資料表上的索引、`PRIMARY KEY`、`UNIQUE` 與 `EXCLUDE` 限制條件會建立在新資料表上。新索引與限制條件的名稱會依照預設規則選擇，不論原本的名稱為何。（此行為可避免新索引可能發生的名稱重複失敗。）
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-STATISTICS"></a>

    `INCLUDING STATISTICS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-STATISTICS)
    :   擴充統計資訊會複製到新資料表。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-STORAGE"></a>

    `INCLUDING STORAGE` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-STORAGE)
    :   會複製所複製欄位定義的 `STORAGE` 設定。預設行為是排除 `STORAGE` 設定，使新資料表中所複製的欄位具有型別特定的預設設定。關於 `STORAGE` 設定的更多資訊，請參閱[第 66.2 節](../../internals/storage/storage-toast.md)。
    <a id="SQL-CREATETABLE-PARMS-LIKE-OPT-ALL"></a>

    `INCLUDING ALL` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-ALL)
    :   `INCLUDING ALL` 是選取所有可用個別選項的縮寫形式。（在 `INCLUDING ALL` 之後寫上個別的 `EXCLUDING` 子句，以選取除了某些特定選項以外的所有選項，可能會很有用。）

    `LIKE` 子句也可以用來從檢視表、外部資料表或複合型別複製欄位定義。不適用的選項（例如對檢視表使用 `INCLUDING INDEXES`）會被忽略。
<a id="SQL-CREATETABLE-PARMS-CONSTRAINT"></a>

`CONSTRAINT constraint_name` [#](#SQL-CREATETABLE-PARMS-CONSTRAINT)
:   欄位或資料表限制條件的選用名稱。若違反了限制條件，錯誤訊息中會出現限制條件名稱，因此可以使用像 `col must be positive` 這樣的限制條件名稱，向用戶端應用程式傳達有用的限制條件資訊。（要指定包含空格的限制條件名稱，需要使用雙引號。）若未指定限制條件名稱，系統會產生一個名稱。
<a id="SQL-CREATETABLE-PARMS-NOT-NULL"></a>

`NOT NULL [ NO INHERIT ]` [#](#SQL-CREATETABLE-PARMS-NOT-NULL)
:   不允許該欄位包含 null 值。

    標記為 `NO INHERIT` 的限制條件不會傳遞到子資料表。
<a id="SQL-CREATETABLE-PARMS-NULL"></a>

`NULL` [#](#SQL-CREATETABLE-PARMS-NULL)
:   允許該欄位包含 null 值。這是預設行為。

    提供此子句只是為了與非標準的 SQL 資料庫相容。不建議在新的應用程式中使用它。
<a id="SQL-CREATETABLE-PARMS-CHECK"></a>

`CHECK ( expression ) [ NO INHERIT ]` [#](#SQL-CREATETABLE-PARMS-CHECK)
:   `CHECK` 子句指定一個產生布林結果的運算式，新增或更新的資料列必須滿足它，插入或更新操作才能成功。求值結果為 TRUE 或 UNKNOWN 的運算式即為成功。若插入或更新操作的任何資料列產生 FALSE 結果，就會引發錯誤例外，而該插入或更新不會變更資料庫。指定為欄位限制條件的檢查限制條件應該只參照該欄位的值，而出現在資料表限制條件中的運算式則可以參照多個欄位。

    目前，`CHECK` 運算式不能包含子查詢，也不能參照目前資料列欄位以外的變數（請參閱[第 5.5.1 節](../../the-sql-language/ddl/ddl-constraints.md#DDL-CONSTRAINTS-CHECK-CONSTRAINTS)）。可以參照系統欄位 `tableoid`，但不能參照任何其他系統欄位。

    標記為 `NO INHERIT` 的限制條件不會傳遞到子資料表。

    當資料表有多個 `CHECK` 限制條件時，會在檢查 `NOT NULL` 限制條件之後，依名稱的字母順序對每個資料列進行檢驗。（9.5 之前的 PostgreSQL 版本不遵循 `CHECK` 限制條件的任何特定觸發順序。）
<a id="SQL-CREATETABLE-PARMS-DEFAULT"></a>

`DEFAULT default_expr` [#](#SQL-CREATETABLE-PARMS-DEFAULT)
:   `DEFAULT` 子句為其所在欄位定義的欄位指定預設資料值。該值是任何不含變數的運算式（特別是，不允許交叉參照目前資料表中的其他欄位）。子查詢也不允許。預設值運算式的資料型別必須與欄位的資料型別相符。

    任何未為該欄位指定值的插入操作，都會使用預設值運算式。若欄位沒有預設值，則預設值為 null。
<a id="SQL-CREATETABLE-PARMS-GENERATED-STORED"></a>

`GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ]`<a id="id-1.9.3.85.6.2.20.1.2"></a> [#](#SQL-CREATETABLE-PARMS-GENERATED-STORED)
:   此子句將欄位建立為*產生欄位*。該欄位無法寫入，讀取時會傳回指定運算式的結果。

    指定 `VIRTUAL` 時，該欄位會在讀取時計算，而且不會佔用任何儲存空間。指定 `STORED` 時，該欄位會在寫入時計算並儲存在磁碟上。`VIRTUAL` 是預設值。

    產生運算式可以參照資料表中的其他欄位，但不能參照其他產生欄位。所使用的任何函式與運算子都必須是 immutable 的。不允許參照其他資料表。

    虛擬產生欄位不能具有使用者定義的型別，而且虛擬產生欄位的產生運算式不得參照使用者定義的函式或型別，也就是說，它只能使用內建的函式或型別。這也間接適用，例如作為運算子或型別轉換基礎的函式或型別。（儲存產生欄位沒有此限制。）
<a id="SQL-CREATETABLE-PARMS-GENERATED-IDENTITY"></a>

`GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]` [#](#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY)
:   此子句將欄位建立為*識別欄位*。它會附帶一個隱含的序列，而在新插入的資料列中，該欄位會自動被指派來自該序列的值。這樣的欄位隱含為 `NOT NULL`。

    子句 `ALWAYS` 與 `BY DEFAULT` 決定在 `INSERT` 與 `UPDATE` 命令中如何處理使用者明確指定的值。

    在 `INSERT` 命令中，若選擇了 `ALWAYS`，只有在 `INSERT` 陳述式指定了 `OVERRIDING SYSTEM
    VALUE` 時，才會接受使用者指定的值。若選擇了 `BY DEFAULT`，則以使用者指定的值為優先。詳細資訊請參閱 [INSERT](sql-insert.md)。（在 `COPY` 命令中，不論此設定為何，一律使用使用者指定的值。）

    在 `UPDATE` 命令中，若選擇了 `ALWAYS`，任何將該欄位更新為 `DEFAULT` 以外之值的操作都會被拒絕。若選擇了 `BY
    DEFAULT`，則可以正常更新該欄位。（`UPDATE` 命令沒有 `OVERRIDING` 子句。）

    選用的 *`sequence_options`* 子句可用來覆寫序列的參數。可用的選項包括 [CREATE SEQUENCE](sql-createsequence.md) 所列出的選項，再加上 `SEQUENCE NAME name`、`LOGGED` 與 `UNLOGGED`，可用來選擇序列的名稱與持久性層級。若沒有 `SEQUENCE NAME`，系統會為序列選擇一個未使用的名稱。若沒有 `LOGGED` 或 `UNLOGGED`，序列的持久性層級會與資料表相同。
<a id="SQL-CREATETABLE-PARMS-UNIQUE"></a>

`UNIQUE [ NULLS [ NOT ] DISTINCT ]`（欄位限制條件）<br>`UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] )` [ `INCLUDE ( column_name [, ...])` ]（資料表限制條件） [#](#SQL-CREATETABLE-PARMS-UNIQUE)
:   `UNIQUE` 限制條件指定資料表中由一個或多個欄位組成的一組欄位只能包含唯一的值。唯一資料表限制條件的行為與唯一欄位限制條件相同，只是多了可以跨越多個欄位的能力。因此，此限制條件強制任兩個資料列在這些欄位中至少有一個欄位不同。

    若為最後一個欄位指定了 `WITHOUT OVERLAPS` 選項，則該欄位會檢查是否重疊，而非是否相等。在這種情況下，只要重複值在 `WITHOUT OVERLAPS` 欄位中不重疊，該限制條件的其他欄位就允許重複。（若該欄位是日期或時間戳記的範圍，這有時稱為 temporal key（時態鍵），但 PostgreSQL 允許任何基本型別上的範圍。）實際上，這樣的限制條件是以 `EXCLUDE` 限制條件而非 `UNIQUE` 限制條件來強制執行的。因此，例如 `UNIQUE (id, valid_at WITHOUT OVERLAPS)` 的行為就如同 `EXCLUDE USING GIST (id WITH =, valid_at WITH
    &&)`。`WITHOUT OVERLAPS` 欄位必須是範圍或多重範圍型別。不允許空範圍／空多重範圍。該限制條件中非 `WITHOUT OVERLAPS` 的欄位可以是任何能在 GiST 索引中比較相等性的型別。預設只支援範圍型別，但你可以透過加入 [btree_gist](../../appendixes/contrib/btree-gist.md) 擴充功能來使用其他型別（這是使用此功能的預期方式）。

    就唯一限制條件而言，null 值不被視為相等，除非指定了 `NULLS NOT DISTINCT`。

    每個唯一限制條件所指定的欄位集合，應該與該資料表上定義的任何其他唯一限制條件或主鍵限制條件所指定的欄位集合不同。（否則，多餘的唯一限制條件會被捨棄。）

    為多層分割階層建立唯一限制條件時，目標分割資料表的分割鍵中的所有欄位，以及其所有後代分割資料表的分割鍵中的所有欄位，都必須包含在限制條件定義中。

    加入唯一限制條件時，會自動在限制條件所使用的欄位或欄位群組上建立唯一值 btree 索引。但若限制條件包含 `WITHOUT OVERLAPS` 子句，則會使用 GiST 索引。所建立的索引與唯一限制條件同名。

    選用的 `INCLUDE` 子句會在該索引中加入一個或多個單純作為「承載資料」（payload）的欄位：這些欄位不強制唯一性，也無法根據這些欄位搜尋索引。不過，可以透過僅索引掃描（index-only scan）取得它們。請注意，雖然限制條件不在被納入的欄位上強制執行，但仍然相依於這些欄位。因此，對這類欄位的某些操作（例如 `DROP COLUMN`）可能會導致限制條件與索引被串聯刪除。
<a id="SQL-CREATETABLE-PARMS-PRIMARY-KEY"></a>

`PRIMARY KEY`（欄位限制條件）<br>`PRIMARY KEY ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] )` [ `INCLUDE ( column_name [, ...])` ]（資料表限制條件） [#](#SQL-CREATETABLE-PARMS-PRIMARY-KEY)
:   `PRIMARY KEY` 限制條件指定資料表的一個或多個欄位只能包含唯一（不重複）且非 null 的值。一個資料表只能指定一個主鍵，不論是作為欄位限制條件還是資料表限制條件。

    主鍵限制條件所指定的欄位集合，應該與同一資料表上定義的任何唯一限制條件所指定的欄位集合不同。（否則，該唯一限制條件是多餘的，會被捨棄。）

    `PRIMARY KEY` 所強制的資料限制，與 `UNIQUE` 加上 `NOT
    NULL` 的組合相同。不過，將一組欄位識別為主鍵，也提供了關於綱要設計的中繼資料，因為主鍵意味著其他資料表可以依賴這組欄位作為資料列的唯一識別碼。

    放在分割資料表上時，`PRIMARY KEY` 限制條件也有先前針對 `UNIQUE` 限制條件所述的那些限制。

    加入 `PRIMARY KEY` 限制條件時，會自動在限制條件所使用的欄位或欄位群組上建立唯一值 btree 索引；若指定了 `WITHOUT OVERLAPS`，則建立 GiST 索引。

    選用的 `INCLUDE` 子句會在該索引中加入一個或多個單純作為「承載資料」（payload）的欄位：這些欄位不強制唯一性，也無法根據這些欄位搜尋索引。不過，可以透過僅索引掃描（index-only scan）取得它們。請注意，雖然限制條件不在被納入的欄位上強制執行，但仍然相依於這些欄位。因此，對這類欄位的某些操作（例如 `DROP COLUMN`）可能會導致限制條件與索引被串聯刪除。
<a id="SQL-CREATETABLE-EXCLUDE"></a>

`EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ]` [#](#SQL-CREATETABLE-EXCLUDE)
:   `EXCLUDE` 子句定義一個排除限制條件，它保證若使用指定的運算子在指定的欄位或運算式上比較任兩個資料列，這些比較不會全部傳回 `TRUE`。若所有指定的運算子都是檢驗相等性，這就等同於 `UNIQUE` 限制條件，不過一般的唯一限制條件會比較快。然而，排除限制條件可以指定比單純相等更一般化的限制條件。例如，你可以使用 `&&` 運算子指定一個限制條件，使資料表中沒有任兩個資料列包含重疊的圓（請參閱[第 8.8 節](../../the-sql-language/datatype/datatype-geometric.md)）。這些運算子必須具備交換律。

    排除限制條件是使用一個與限制條件同名的索引來實作的，因此每個指定的運算子都必須與索引存取方法 *`index_method`* 的適當運算子類別相關聯（請參閱[第 11.10 節](../../the-sql-language/indexes/indexes-opclass.md)）。每個 *`exclude_element`* 定義索引的一個欄位，因此它可以選擇性地指定定序、運算子類別、運算子類別參數和／或排序選項；這些在 [CREATE INDEX](sql-createindex.md) 中有完整說明。

    存取方法必須支援 `amgettuple`（請參閱[第 63 章](../../internals/indexam/README.md)）；目前這表示不能使用 GIN。雖然是允許的，但在排除限制條件中使用 B-tree 或 hash 索引意義不大，因為這樣做所能達成的，一般的唯一限制條件都能做得更好。因此實務上，存取方法一律會是 GiST 或 SP-GiST。

    *`predicate`* 讓你可以在資料表的子集合上指定排除限制條件；在內部，這會建立一個部分索引。請注意，謂詞前後必須加上括號。

    為多層分割階層建立排除限制條件時，目標分割資料表的分割鍵中的所有欄位，以及其所有後代分割資料表的分割鍵中的所有欄位，都必須包含在限制條件定義中。此外，這些欄位必須使用相等運算子進行比較。這些限制確保可能衝突的資料列會存在於同一個分割區中。限制條件也可以參照不屬於任何分割鍵的其他欄位，這些欄位可以使用任何適當的運算子進行比較。
<a id="SQL-CREATETABLE-PARMS-REFERENCES"></a>

`REFERENCES reftable [ ( refcolumn ) ] [ MATCH matchtype ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ]`（欄位限制條件）<br>`FOREIGN KEY ( column_name [, ... ] [, PERIOD column_name ] ) REFERENCES reftable [ ( refcolumn [, ... ] [, PERIOD refcolumn ] ) ] [ MATCH matchtype ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ]`（資料表限制條件） [#](#SQL-CREATETABLE-PARMS-REFERENCES)
:   這些子句指定外鍵限制條件，它要求新資料表中由一個或多個欄位組成的一組欄位，只能包含與被參照資料表某個資料列中被參照欄位的值相符的值。若省略 *`refcolumn`* 清單，則使用 *`reftable`* 的主鍵。否則，*`refcolumn`* 清單必須參照某個不可延遲的唯一限制條件或主鍵限制條件的欄位，或者是某個非部分唯一值索引的欄位。

    若最後一個欄位標記了 `PERIOD`，它會以特殊方式處理。非 `PERIOD` 欄位會比較相等性（而且這類欄位必須至少有一個），但 `PERIOD` 欄位則不會。取而代之的是，若被參照資料表具有相符的紀錄（依據鍵的非 `PERIOD` 部分），而這些紀錄合併後的 `PERIOD` 值完全涵蓋參照紀錄的值，就視為滿足該限制條件。換句話說，參照在其整個期間內都必須有一個被參照對象。此欄位必須是範圍或多重範圍型別。此外，被參照資料表必須具有以 `WITHOUT
    OVERLAPS` 宣告的主鍵或唯一限制條件。最後，若外鍵具有 PERIOD *`column_name`* 規格，則對應的 *`refcolumn`*（若有的話）也必須標記為 `PERIOD`。若省略 *`refcolumn`* 子句，因而選用 reftable 的主鍵限制條件，則該主鍵的最後一個欄位必須標記為 `WITHOUT OVERLAPS`。

    對於每一對參照欄位與被參照欄位，若它們屬於可定序的資料型別，則其定序必須要嘛都是確定性的（deterministic），要嘛彼此相同。這確保兩個欄位對相等性有一致的概念。

    使用者必須擁有被參照資料表（整個資料表，或特定的被參照欄位）上的 `REFERENCES` 權限。加入外鍵限制條件需要被參照資料表上的 `SHARE ROW EXCLUSIVE` 鎖定。請注意，不能在暫存資料表與永久資料表之間定義外鍵限制條件。

    插入參照欄位的值，會使用給定的比對類型，與被參照資料表及被參照欄位的值進行比對。比對類型有三種：`MATCH
    FULL`、`MATCH PARTIAL` 與 `MATCH
    SIMPLE`（這是預設值）。`MATCH
    FULL` 不允許多欄位外鍵的其中一個欄位為 null，除非所有外鍵欄位都是 null；若它們全部都是 null，則該資料列不需要在被參照資料表中有相符的資料列。`MATCH SIMPLE` 允許任何外鍵欄位為 null；若其中任何一個為 null，則該資料列不需要在被參照資料表中有相符的資料列。`MATCH PARTIAL` 尚未實作。（當然，可以在參照欄位上套用 `NOT NULL` 限制條件，以避免發生這些情況。）

    此外，當被參照欄位中的資料變更時，會對此資料表欄位中的資料執行特定的動作。`ON DELETE` 子句指定當被參照資料表中被參照的資料列正在被刪除時要執行的動作。同樣地，`ON UPDATE` 子句指定當被參照資料表中被參照的欄位正被更新為新值時要執行的動作。若資料列被更新，但被參照的欄位實際上並未變更，則不會執行任何動作。參照動作會作為資料變更命令的一部分執行，即使限制條件已延遲也是如此。每個子句可能的動作如下：

    <a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-NO-ACTION"></a>

    `NO ACTION` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-NO-ACTION)
    :   若刪除或更新會造成違反外鍵限制條件，就產生錯誤。若限制條件已延遲，而在檢查限制條件時仍存在任何參照的資料列，就會在那時產生此錯誤。這是預設動作。
    <a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-RESTRICT"></a>

    `RESTRICT` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-RESTRICT)
    :   若要刪除或更新的資料列與參照資料表中的某個資料列相符，就產生錯誤。即使動作之後的狀態不會違反外鍵限制條件，這也會阻止該動作。特別是，它會阻止將被參照的資料列更新為不同但比較結果相等的值。（但它不會阻止將欄位更新為相同值的「無操作」更新。）

        在時態外鍵中不支援此選項。
    <a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-CASCADE"></a>

    `CASCADE` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-CASCADE)
    :   分別為：刪除參照了被刪除資料列的任何資料列，或將參照欄位的值更新為被參照欄位的新值。

        在時態外鍵中不支援此選項。
    <a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-NULL"></a>

    `SET NULL [ ( column_name [, ... ] ) ]` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-NULL)
    :   將所有參照欄位，或參照欄位中指定的子集合，設為 null。只有 `ON DELETE` 動作才能指定欄位的子集合。

        在時態外鍵中不支援此選項。
    <a id="SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-DEFAULT"></a>

    `SET DEFAULT [ ( column_name [, ... ] ) ]` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-DEFAULT)
    :   將所有參照欄位，或參照欄位中指定的子集合，設為其預設值。只有 `ON DELETE` 動作才能指定欄位的子集合。（若預設值不是 null，被參照資料表中必須存在與預設值相符的資料列，否則操作會失敗。）

        在時態外鍵中不支援此選項。

    若被參照的欄位經常變更，明智的做法可能是在參照欄位上加入索引，以便更有效率地執行與外鍵限制條件相關的參照動作。
<a id="SQL-CREATETABLE-PARMS-DEFERRABLE"></a>

`DEFERRABLE`<br>`NOT DEFERRABLE` [#](#SQL-CREATETABLE-PARMS-DEFERRABLE)
:   這控制限制條件是否可以延遲。不可延遲的限制條件會在每個命令之後立即檢查。可延遲之限制條件的檢查可以延後到交易結束時（使用 [`SET CONSTRAINTS`](sql-set-constraints.md) 命令）。`NOT DEFERRABLE` 是預設值。目前只有 `UNIQUE`、`PRIMARY KEY`、`EXCLUDE` 與 `REFERENCES`（外鍵）限制條件接受此子句。`NOT NULL` 與 `CHECK` 限制條件不可延遲。請注意，在包含 `ON CONFLICT` 子句的 `INSERT` 陳述式中，可延遲的限制條件不能用作衝突仲裁者。
<a id="SQL-CREATETABLE-PARMS-INITIALLY"></a>

`INITIALLY IMMEDIATE`<br>`INITIALLY DEFERRED` [#](#SQL-CREATETABLE-PARMS-INITIALLY)
:   若限制條件是可延遲的，此子句指定檢查該限制條件的預設時機。若限制條件為 `INITIALLY IMMEDIATE`，則會在每個陳述式之後檢查。這是預設值。若限制條件為 `INITIALLY DEFERRED`，則只會在交易結束時檢查。限制條件的檢查時機可以使用 [`SET CONSTRAINTS`](sql-set-constraints.md) 命令更改。
<a id="SQL-CREATETABLE-PARMS-ENFORCED"></a>

`ENFORCED`<br>`NOT ENFORCED` [#](#SQL-CREATETABLE-PARMS-ENFORCED)
:   當限制條件為 `ENFORCED` 時，資料庫系統會在適當的時機（視情況在每個陳述式之後或在交易結束時）檢查限制條件，以確保該限制條件得到滿足。這是預設值。若限制條件為 `NOT ENFORCED`，資料庫系統不會檢查該限制條件，此時就要由應用程式的程式碼來確保限制條件得到滿足。在不影響結果正確性的情況下，資料庫系統仍可能為了最佳化決策而假設資料確實滿足該限制條件。

    若在執行時實際檢查限制條件的成本過高，`NOT ENFORCED` 限制條件可以作為有用的文件。

    目前只有外鍵限制條件與 `CHECK` 限制條件支援此功能。
<a id="SQL-CREATETABLE-METHOD"></a>

`USING method` [#](#SQL-CREATETABLE-METHOD)
:   此選用子句指定用來儲存新資料表內容的資料表存取方法；該方法必須是 `TABLE` 類型的存取方法。更多資訊請參閱[第 62 章](../../internals/tableam/README.md)。若未指定此選項，新資料表會選用預設的資料表存取方法。更多資訊請參閱 [default_table_access_method](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD)。

    建立分割區時，若其分割資料表設定了資料表存取方法，則分割區的資料表存取方法即為其分割資料表的存取方法。
<a id="SQL-CREATETABLE-PARMS-WITH"></a>

`WITH ( storage_parameter [= value] [, ... ] )` [#](#SQL-CREATETABLE-PARMS-WITH)
:   此子句為資料表或索引指定選用的儲存參數；更多資訊請參閱下方的[儲存參數](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS)。為了向後相容性，資料表的 `WITH` 子句也可以包含 `OIDS=FALSE`，以指定新資料表的資料列不應包含 OID（物件識別碼），`OIDS=TRUE` 已不再支援。
<a id="SQL-CREATETABLE-PARMS-WITHOUT-OIDS"></a>

`WITHOUT OIDS` [#](#SQL-CREATETABLE-PARMS-WITHOUT-OIDS)
:   這是宣告資料表為 `WITHOUT OIDS` 的向後相容語法，建立 `WITH
    OIDS` 的資料表已不再支援。
<a id="SQL-CREATETABLE-PARMS-ON-COMMIT"></a>

`ON COMMIT` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT)
:   暫存資料表在交易區塊結束時的行為可以使用 `ON COMMIT` 控制。三個選項為：

    <a id="SQL-CREATETABLE-PARMS-ON-COMMIT-PRESERVE-ROWS"></a>

    `PRESERVE ROWS` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT-PRESERVE-ROWS)
    :   在交易結束時不採取任何特殊動作。這是預設行為。
    <a id="SQL-CREATETABLE-PARMS-ON-COMMIT-DELETE-ROWS"></a>

    `DELETE ROWS` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT-DELETE-ROWS)
    :   暫存資料表中的所有資料列會在每個交易區塊結束時被刪除。基本上，每次提交時都會自動執行一次 [`TRUNCATE`](sql-truncate.md)。用在分割資料表上時，此動作不會串聯到其分割區。
    <a id="SQL-CREATETABLE-PARMS-ON-COMMIT-DROP"></a>

    `DROP` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT-DROP)
    :   暫存資料表會在目前交易區塊結束時被移除。用在分割資料表上時，此動作會移除其分割區；用在具有繼承子資料表的資料表上時，則會移除相依的子資料表。
<a id="SQL-CREATETABLE-TABLESPACE"></a>

`TABLESPACE tablespace_name` [#](#SQL-CREATETABLE-TABLESPACE)
:   *`tablespace_name`* 是要在其中建立新資料表的資料表空間名稱。若未指定，則會參考 [default_tablespace](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLESPACE)；若資料表是暫存的，則參考 [temp_tablespaces](../../server-administration/runtime-config/runtime-config-client.md#GUC-TEMP-TABLESPACES)。對於分割資料表，由於資料表本身不需要儲存空間，在沒有明確指定其他資料表空間時，所指定的資料表空間會取代 `default_tablespace`，作為任何新建立分割區所使用的預設資料表空間。
<a id="SQL-CREATETABLE-PARMS-USING-INDEX-TABLESPACE"></a>

`USING INDEX TABLESPACE tablespace_name` [#](#SQL-CREATETABLE-PARMS-USING-INDEX-TABLESPACE)
:   此子句允許選擇與 `UNIQUE`、`PRIMARY
    KEY` 或 `EXCLUDE` 限制條件相關聯之索引要建立在哪個資料表空間中。若未指定，則會參考 [default_tablespace](../../server-administration/runtime-config/runtime-config-client.md#GUC-DEFAULT-TABLESPACE)；若資料表是暫存的，則參考 [temp_tablespaces](../../server-administration/runtime-config/runtime-config-client.md#GUC-TEMP-TABLESPACES)。

<a id="SQL-CREATETABLE-STORAGE-PARAMETERS"></a>

### 儲存參數

<a id="id-1.9.3.85.6.3.2"></a>

`WITH` 子句可以為資料表，以及與 `UNIQUE`、`PRIMARY KEY` 或 `EXCLUDE` 限制條件相關聯的索引，指定*儲存參數*。索引的儲存參數記載於 [CREATE INDEX](sql-createindex.md)。目前可用於資料表的儲存參數列於下方。如下所示，其中許多參數都另有一個加上 `toast.` 前綴的同名參數，用來控制該資料表的次要 TOAST 資料表（若有的話）的行為（關於 TOAST 的更多資訊，請參閱[第 66.2 節](../../internals/storage/storage-toast.md)）。若設定了資料表參數值，而對應的 `toast.` 參數沒有設定，TOAST 資料表就會使用該資料表的參數值。不支援為分割資料表指定這些參數，但你可以為個別的葉分割區指定它們。

<a id="RELOPTION-FILLFACTOR"></a>

`fillfactor` (`integer`) <a id="id-1.9.3.85.6.3.4.1.1.3"></a> [#](#RELOPTION-FILLFACTOR)
:   資料表的 fillfactor 是介於 10 到 100 之間的百分比。100（完全填滿）是預設值。指定較小的 fillfactor 時，`INSERT` 操作只會將資料表頁面填到所指定的百分比；每個頁面上剩餘的空間會保留給更新該頁面上的資料列使用。這讓 `UPDATE` 有機會將資料列更新後的副本放在與原始資料列相同的頁面上，這比放在不同的頁面上更有效率，也讓[僅堆積元組（heap-only tuple）更新](../../internals/storage/storage-hot.md)更有可能發生。對於項目從不更新的資料表，完全填滿是最佳選擇，但在大量更新的資料表中，較小的 fillfactor 較為合適。TOAST 資料表不能設定此參數。
<a id="RELOPTION-TOAST-TUPLE-TARGET"></a>

`toast_tuple_target` (`integer`) <a id="id-1.9.3.85.6.3.4.2.1.3"></a> [#](#RELOPTION-TOAST-TUPLE-TARGET)
:   toast_tuple_target 指定在我們嘗試將過長的欄位值壓縮和／或移入 TOAST 資料表之前所需的最小元組長度，也是一旦開始 TOAST 處理後，我們嘗試將長度縮減到其以下的目標長度。這會影響標記為 External（搬移）、Main（壓縮）或 Extended（兩者皆是）的欄位，而且只適用於新的元組。對現有的資料列沒有影響。預設情況下，此參數的設定會讓每個區塊至少容納 4 個元組，以預設的區塊大小而言是 2040 位元組。有效值介於 128 位元組與（區塊大小 - 標頭）之間；以預設區塊大小而言，此上限為 8160 位元組。對於非常短或非常長的資料列，更改此值可能沒有幫助。請注意，預設設定通常已接近最佳，而設定此參數在某些情況下可能會產生負面影響。TOAST 資料表不能設定此參數。
<a id="RELOPTION-PARALLEL-WORKERS"></a>

`parallel_workers` (`integer`) <a id="id-1.9.3.85.6.3.4.3.1.3"></a> [#](#RELOPTION-PARALLEL-WORKERS)
:   此參數設定應該用來協助平行掃描此資料表的工作程序（worker）數量。若未設定，系統會根據關聯的大小決定一個值。規劃器或使用平行掃描的公用程式陳述式實際選擇的工作程序數量可能會較少，例如由於 [max_worker_processes](../../server-administration/runtime-config/runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) 的設定。
<a id="RELOPTION-AUTOVACUUM-ENABLED"></a>

`autovacuum_enabled`, `toast.autovacuum_enabled` (`boolean`) <a id="id-1.9.3.85.6.3.4.4.1.4"></a> [#](#RELOPTION-AUTOVACUUM-ENABLED)
:   啟用或停用特定資料表的 autovacuum 常駐程式。若為 true，autovacuum 常駐程式會依照[第 24.1.6 節](../../server-administration/maintenance/routine-vacuuming.md#autovacuum)所討論的規則，對此資料表執行自動的 `VACUUM` 和／或 `ANALYZE` 操作。若為 false，則不會對此資料表執行 autovacuum，但為了防止交易 ID 迴繞（wraparound）時除外。關於防止迴繞的更多資訊，請參閱[第 24.1.5 節](../../server-administration/maintenance/routine-vacuuming.md#vacuum-for-wraparound)。請注意，若 [autovacuum](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM) 參數為 false，autovacuum 常駐程式就完全不會執行（為了防止交易 ID 迴繞時除外）；設定個別資料表的儲存參數並不會覆寫該設定。因此，明確將此儲存參數設為 `true` 幾乎沒有意義，只有設為 `false` 才有意義。
<a id="RELOPTION-VACUUM-INDEX-CLEANUP"></a>

`vacuum_index_cleanup`, `toast.vacuum_index_cleanup` (`enum`) <a id="id-1.9.3.85.6.3.4.5.1.4"></a> [#](#RELOPTION-VACUUM-INDEX-CLEANUP)
:   在此資料表上執行 `VACUUM` 時，強制執行或停用索引清理。預設值為 `AUTO`。設為 `OFF` 時停用索引清理，設為 `ON` 時啟用索引清理，而設為 `AUTO` 時，則會在每次執行 `VACUUM` 時動態做出決定。這種動態行為讓 `VACUUM` 可以避免為了移除極少量的死亡資料列而不必要地掃描索引。強制停用所有索引清理可以大幅加快 `VACUUM`，但若資料表修改頻繁，也可能導致索引嚴重膨脹。若有指定 [`VACUUM`](sql-vacuum.md) 的 `INDEX_CLEANUP` 參數，它會覆寫此選項的值。
<a id="RELOPTION-VACUUM-TRUNCATE"></a>

`vacuum_truncate`, `toast.vacuum_truncate` (`boolean`) <a id="id-1.9.3.85.6.3.4.6.1.4"></a> [#](#RELOPTION-VACUUM-TRUNCATE)
:   個別資料表的 [vacuum_truncate](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-TRUNCATE) 參數值。若有指定 [`VACUUM`](sql-vacuum.md) 的 `TRUNCATE` 參數，它會覆寫此選項的值。
<a id="RELOPTION-AUTOVACUUM-VACUUM-THRESHOLD"></a>

`autovacuum_vacuum_threshold`, `toast.autovacuum_vacuum_threshold` (`integer`) <a id="id-1.9.3.85.6.3.4.7.1.4"></a> [#](#RELOPTION-AUTOVACUUM-VACUUM-THRESHOLD)
:   個別資料表的 [autovacuum_vacuum_threshold](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-THRESHOLD) 參數值。
<a id="RELOPTION-AUTOVACUUM-VACUUM-MAX-THRESHOLD"></a>

`autovacuum_vacuum_max_threshold`, `toast.autovacuum_vacuum_max_threshold` (`integer`) <a id="id-1.9.3.85.6.3.4.8.1.4"></a> [#](#RELOPTION-AUTOVACUUM-VACUUM-MAX-THRESHOLD)
:   個別資料表的 [autovacuum_vacuum_max_threshold](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD) 參數值。
<a id="RELOPTION-AUTOVACUUM-VACUUM-SCALE-FACTOR"></a>

`autovacuum_vacuum_scale_factor`, `toast.autovacuum_vacuum_scale_factor` (`floating point`) <a id="id-1.9.3.85.6.3.4.9.1.4"></a> [#](#RELOPTION-AUTOVACUUM-VACUUM-SCALE-FACTOR)
:   個別資料表的 [autovacuum_vacuum_scale_factor](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR) 參數值。
<a id="RELOPTION-AUTOVACUUM-VACUUM-INSERT-THRESHOLD"></a>

`autovacuum_vacuum_insert_threshold`, `toast.autovacuum_vacuum_insert_threshold` (`integer`) <a id="id-1.9.3.85.6.3.4.10.1.4"></a> [#](#RELOPTION-AUTOVACUUM-VACUUM-INSERT-THRESHOLD)
:   個別資料表的 [autovacuum_vacuum_insert_threshold](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD) 參數值。可以使用特殊值 -1 來停用此資料表上由插入觸發的 vacuum。
<a id="RELOPTION-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR"></a>

`autovacuum_vacuum_insert_scale_factor`, `toast.autovacuum_vacuum_insert_scale_factor` (`floating point`) <a id="id-1.9.3.85.6.3.4.11.1.4"></a> [#](#RELOPTION-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR)
:   個別資料表的 [autovacuum_vacuum_insert_scale_factor](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR) 參數值。
<a id="RELOPTION-AUTOVACUUM-ANALYZE-THRESHOLD"></a>

`autovacuum_analyze_threshold` (`integer`) <a id="id-1.9.3.85.6.3.4.12.1.3"></a> [#](#RELOPTION-AUTOVACUUM-ANALYZE-THRESHOLD)
:   個別資料表的 [autovacuum_analyze_threshold](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-ANALYZE-THRESHOLD) 參數值。
<a id="RELOPTION-AUTOVACUUM-ANALYZE-SCALE-FACTOR"></a>

`autovacuum_analyze_scale_factor` (`floating point`) <a id="id-1.9.3.85.6.3.4.13.1.3"></a> [#](#RELOPTION-AUTOVACUUM-ANALYZE-SCALE-FACTOR)
:   個別資料表的 [autovacuum_analyze_scale_factor](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR) 參數值。
<a id="RELOPTION-AUTOVACUUM-VACUUM-COST-DELAY"></a>

`autovacuum_vacuum_cost_delay`, `toast.autovacuum_vacuum_cost_delay` (`floating point`) <a id="id-1.9.3.85.6.3.4.14.1.4"></a> [#](#RELOPTION-AUTOVACUUM-VACUUM-COST-DELAY)
:   個別資料表的 [autovacuum_vacuum_cost_delay](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-COST-DELAY) 參數值。
<a id="RELOPTION-AUTOVACUUM-VACUUM-COST-LIMIT"></a>

`autovacuum_vacuum_cost_limit`, `toast.autovacuum_vacuum_cost_limit` (`integer`) <a id="id-1.9.3.85.6.3.4.15.1.4"></a> [#](#RELOPTION-AUTOVACUUM-VACUUM-COST-LIMIT)
:   個別資料表的 [autovacuum_vacuum_cost_limit](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-COST-LIMIT) 參數值。
<a id="RELOPTION-AUTOVACUUM-FREEZE-MIN-AGE"></a>

`autovacuum_freeze_min_age`, `toast.autovacuum_freeze_min_age` (`integer`) <a id="id-1.9.3.85.6.3.4.16.1.4"></a> [#](#RELOPTION-AUTOVACUUM-FREEZE-MIN-AGE)
:   個別資料表的 [vacuum_freeze_min_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-FREEZE-MIN-AGE) 參數值。請注意，autovacuum 會忽略大於全系統 [autovacuum_freeze_max_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) 設定一半的個別資料表 `autovacuum_freeze_min_age` 參數。
<a id="RELOPTION-AUTOVACUUM-FREEZE-MAX-AGE"></a>

`autovacuum_freeze_max_age`, `toast.autovacuum_freeze_max_age` (`integer`) <a id="id-1.9.3.85.6.3.4.17.1.4"></a> [#](#RELOPTION-AUTOVACUUM-FREEZE-MAX-AGE)
:   個別資料表的 [autovacuum_freeze_max_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) 參數值。請注意，autovacuum 會忽略大於全系統設定的個別資料表 `autovacuum_freeze_max_age` 參數（它只能設得比全系統設定小）。
<a id="RELOPTION-AUTOVACUUM-FREEZE-TABLE-AGE"></a>

`autovacuum_freeze_table_age`, `toast.autovacuum_freeze_table_age` (`integer`) <a id="id-1.9.3.85.6.3.4.18.1.4"></a> [#](#RELOPTION-AUTOVACUUM-FREEZE-TABLE-AGE)
:   個別資料表的 [vacuum_freeze_table_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-FREEZE-TABLE-AGE) 參數值。
<a id="RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-MIN-AGE"></a>

`autovacuum_multixact_freeze_min_age`, `toast.autovacuum_multixact_freeze_min_age` (`integer`) <a id="id-1.9.3.85.6.3.4.19.1.4"></a> [#](#RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-MIN-AGE)
:   個別資料表的 [vacuum_multixact_freeze_min_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE) 參數值。請注意，autovacuum 會忽略大於全系統 [autovacuum_multixact_freeze_max_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE) 設定一半的個別資料表 `autovacuum_multixact_freeze_min_age` 參數。
<a id="RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE"></a>

`autovacuum_multixact_freeze_max_age`, `toast.autovacuum_multixact_freeze_max_age` (`integer`) <a id="id-1.9.3.85.6.3.4.20.1.4"></a> [#](#RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE)
:   個別資料表的 [autovacuum_multixact_freeze_max_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE) 參數值。請注意，autovacuum 會忽略大於全系統設定的個別資料表 `autovacuum_multixact_freeze_max_age` 參數（它只能設得比全系統設定小）。
<a id="RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-TABLE-AGE"></a>

`autovacuum_multixact_freeze_table_age`, `toast.autovacuum_multixact_freeze_table_age` (`integer`) <a id="id-1.9.3.85.6.3.4.21.1.4"></a> [#](#RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-TABLE-AGE)
:   個別資料表的 [vacuum_multixact_freeze_table_age](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE) 參數值。
<a id="RELOPTION-LOG-AUTOVACUUM-MIN-DURATION"></a>

`log_autovacuum_min_duration`, `toast.log_autovacuum_min_duration` (`integer`) <a id="id-1.9.3.85.6.3.4.22.1.4"></a> [#](#RELOPTION-LOG-AUTOVACUUM-MIN-DURATION)
:   個別資料表的 [log_autovacuum_min_duration](../../server-administration/runtime-config/runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION) 參數值。
<a id="RELOPTION-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE"></a>

`vacuum_max_eager_freeze_failure_rate`, `toast.vacuum_max_eager_freeze_failure_rate` (`floating point`) <a id="id-1.9.3.85.6.3.4.23.1.4"></a> [#](#RELOPTION-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE)
:   個別資料表的 [vacuum_max_eager_freeze_failure_rate](../../server-administration/runtime-config/runtime-config-vacuum.md#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE) 參數值。
<a id="RELOPTION-USER-CATALOG-TABLE"></a>

`user_catalog_table` (`boolean`) <a id="id-1.9.3.85.6.3.4.24.1.3"></a> [#](#RELOPTION-USER-CATALOG-TABLE)
:   將此資料表宣告為額外的目錄資料表，以供邏輯複寫使用。詳細資訊請參閱[第 47.6.2 節](../../server-programming/logicaldecoding/logicaldecoding-output-plugin.md#logicaldecoding-capabilities)。TOAST 資料表不能設定此參數。

<a id="SQL-CREATETABLE-NOTES"></a>

## 注意事項

PostgreSQL 會為每個唯一限制條件與主鍵限制條件自動建立索引，以強制唯一性。因此，不需要為主鍵欄位明確建立索引。（更多資訊請參閱 [CREATE INDEX](sql-createindex.md)。）

在目前的實作中，唯一限制條件與主鍵不會被繼承。這使得繼承與唯一限制條件的組合相當不實用。

一個資料表不能有超過 1600 個欄位。（實務上，由於元組長度的限制，有效上限通常更低。）

<a id="SQL-CREATETABLE-EXAMPLES"></a>

## 範例

建立資料表 `films` 與資料表 `distributors`：

```

CREATE TABLE films (
    code        char(5) CONSTRAINT firstkey PRIMARY KEY,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
);

CREATE TABLE distributors (
     did    integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
     name   varchar(40) NOT NULL CHECK (name <> '')
);
```

建立一個含有二維陣列的資料表：

```

CREATE TABLE array_int (
    vector  int[][]
);
```

為資料表 `films` 定義唯一資料表限制條件。唯一資料表限制條件可以定義在資料表的一個或多個欄位上：

```

CREATE TABLE films (
    code        char(5),
    title       varchar(40),
    did         integer,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute,
    CONSTRAINT production UNIQUE(date_prod)
);
```

定義檢查欄位限制條件：

```

CREATE TABLE distributors (
    did     integer CHECK (did > 100),
    name    varchar(40)
);
```

定義檢查資料表限制條件：

```

CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    CONSTRAINT con1 CHECK (did > 100 AND name <> '')
);
```

為資料表 `films` 定義主鍵資料表限制條件：

```

CREATE TABLE films (
    code        char(5),
    title       varchar(40),
    did         integer,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute,
    CONSTRAINT code_title PRIMARY KEY(code,title)
);
```

為資料表 `distributors` 定義主鍵限制條件。以下兩個範例是等效的，第一個使用資料表限制條件語法，第二個使用欄位限制條件語法：

```

CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    PRIMARY KEY(did)
);

CREATE TABLE distributors (
    did     integer PRIMARY KEY,
    name    varchar(40)
);
```

為欄位 `name` 指定一個字面常數預設值，安排欄位 `did` 的預設值透過選取序列物件的下一個值來產生，並讓 `modtime` 的預設值為目前交易的開始時間（也就是插入該資料列之交易開始的時間；同一交易內插入的多筆資料列會得到相同的時間）：

```

CREATE TABLE distributors (
    name      varchar(40) DEFAULT 'Luso Films',
    did       integer DEFAULT nextval('distributors_serial'),
    modtime   timestamp DEFAULT current_timestamp
);
```

在資料表 `distributors` 上定義兩個 `NOT NULL` 欄位限制條件，其中一個明確指定了名稱：

```

CREATE TABLE distributors (
    did     integer CONSTRAINT no_null NOT NULL,
    name    varchar(40) NOT NULL
);
```

為 `name` 欄位定義唯一限制條件：

```

CREATE TABLE distributors (
    did     integer,
    name    varchar(40) UNIQUE
);
```

相同的限制條件，改以資料表限制條件指定：

```

CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    UNIQUE(name)
);
```

建立相同的資料表，為資料表及其唯一值索引都指定 70% 的填充因子（fill factor）：

```

CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    UNIQUE(name) WITH (fillfactor=70)
)
WITH (fillfactor=70);
```

建立帶有排除限制條件的資料表 `circles`，以防止任兩個圓重疊：

```

CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

在資料表空間 `diskvol1` 中建立資料表 `cinemas`：

```

CREATE TABLE cinemas (
        id serial,
        name text,
        location text
) TABLESPACE diskvol1;
```

建立一個複合型別與一個型別化資料表：

```

CREATE TYPE employee_type AS (name text, salary numeric);

CREATE TABLE employees OF employee_type (
    PRIMARY KEY (name),
    salary WITH OPTIONS DEFAULT 1000
);
```

建立範圍分割資料表：

```

CREATE TABLE measurement (
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (logdate);
```

建立分割鍵中包含多個欄位的範圍分割資料表：

```

CREATE TABLE measurement_year_month (
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (EXTRACT(YEAR FROM logdate), EXTRACT(MONTH FROM logdate));
```

建立清單分割資料表：

```

CREATE TABLE cities (
    city_id      bigserial not null,
    name         text not null,
    population   bigint
) PARTITION BY LIST (left(lower(name), 1));
```

建立雜湊分割資料表：

```

CREATE TABLE orders (
    order_id     bigint not null,
    cust_id      bigint not null,
    status       text
) PARTITION BY HASH (order_id);
```

建立範圍分割資料表的分割區：

```

CREATE TABLE measurement_y2016m07
    PARTITION OF measurement (
    unitsales DEFAULT 0
) FOR VALUES FROM ('2016-07-01') TO ('2016-08-01');
```

為分割鍵中包含多個欄位的範圍分割資料表建立幾個分割區：

```

CREATE TABLE measurement_ym_older
    PARTITION OF measurement_year_month
    FOR VALUES FROM (MINVALUE, MINVALUE) TO (2016, 11);

CREATE TABLE measurement_ym_y2016m11
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 11) TO (2016, 12);

CREATE TABLE measurement_ym_y2016m12
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 12) TO (2017, 01);

CREATE TABLE measurement_ym_y2017m01
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2017, 01) TO (2017, 02);
```

建立清單分割資料表的分割區：

```

CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b');
```

建立清單分割資料表的分割區，該分割區本身再進一步分割，然後為它加入一個分割區：

```

CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b') PARTITION BY RANGE (population);

CREATE TABLE cities_ab_10000_to_100000
    PARTITION OF cities_ab FOR VALUES FROM (10000) TO (100000);
```

建立雜湊分割資料表的分割區：

```

CREATE TABLE orders_p1 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE orders_p2 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE orders_p3 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE orders_p4 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

建立預設分割區：

```

CREATE TABLE cities_partdef
    PARTITION OF cities DEFAULT;
```

<a id="SQL-CREATETABLE-COMPATIBILITY"></a>

## 相容性

`CREATE TABLE` 命令符合 SQL 標準，但有下列例外。

<a id="id-1.9.3.85.9.3"></a>

### 暫存資料表

雖然 `CREATE TEMPORARY TABLE` 的語法與 SQL 標準相似，但效果並不相同。在標準中，暫存資料表只需定義一次，就會自動存在於每個需要它們的工作階段中（以空的內容開始）。PostgreSQL 則要求每個工作階段為每個要使用的暫存資料表，各自發出自己的 `CREATE TEMPORARY
TABLE` 命令。這讓不同的工作階段可以將相同的暫存資料表名稱用於不同的用途，而標準的做法則限制了給定暫存資料表名稱的所有實例都必須具有相同的資料表結構。

標準對暫存資料表行為的定義普遍被忽略。PostgreSQL 在這一點上的行為與其他幾個 SQL 資料庫相似。

SQL 標準也區分了全域暫存資料表與區域暫存資料表，其中區域暫存資料表在每個工作階段內的每個 SQL 模組中各有一組獨立的內容，不過其定義仍然在各工作階段之間共用。由於 PostgreSQL 不支援 SQL 模組，這項區分在 PostgreSQL 中並不適用。

為了相容性，PostgreSQL 在暫存資料表宣告中會接受 `GLOBAL` 與 `LOCAL` 關鍵字，但它們目前沒有任何作用。不建議使用這些關鍵字，因為未來版本的 PostgreSQL 可能會對其含義採用更符合標準的解讀。

暫存資料表的 `ON COMMIT` 子句也與 SQL 標準相似，但有一些差異。若省略 `ON COMMIT` 子句，SQL 規定預設行為是 `ON COMMIT DELETE ROWS`。然而，PostgreSQL 中的預設行為是 `ON COMMIT PRESERVE ROWS`。`ON COMMIT
DROP` 選項在 SQL 中並不存在。

<a id="id-1.9.3.85.9.4"></a>

### 非延遲的唯一性限制條件

當 `UNIQUE` 或 `PRIMARY KEY` 限制條件不可延遲時，PostgreSQL 會在每次插入或修改資料列時立即檢查唯一性。SQL 標準規定唯一性應該只在陳述式結束時強制執行；例如，當單一命令更新多個鍵值時，這就會造成差異。要獲得符合標準的行為，請將限制條件宣告為 `DEFERRABLE` 但不延遲（即 `INITIALLY
IMMEDIATE`）。請注意，這可能比立即檢查唯一性慢得多。

<a id="id-1.9.3.85.9.5"></a>

### 欄位檢查限制條件

SQL 標準規定 `CHECK` 欄位限制條件只能參照其所套用的欄位；只有 `CHECK` 資料表限制條件可以參照多個欄位。PostgreSQL 不強制執行此限制；它對欄位檢查限制條件與資料表檢查限制條件一視同仁。

<a id="id-1.9.3.85.9.6"></a>

### `EXCLUDE` 限制條件

`EXCLUDE` 限制條件類型是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.85.9.7"></a>

### 外鍵限制條件

在外鍵動作 `SET DEFAULT` 與 `SET NULL` 中指定欄位清單的能力，是 PostgreSQL 的擴充語法。

外鍵限制條件可以參照唯一值索引的欄位，而非主鍵或唯一限制條件的欄位，這是 PostgreSQL 的擴充。

<a id="id-1.9.3.85.9.8"></a>

### `NULL`「限制條件」

`NULL`「限制條件」（實際上並不是限制條件）是 PostgreSQL 對 SQL 標準的擴充，納入它是為了與某些其他資料庫系統相容（也是為了與 `NOT
NULL` 限制條件對稱）。由於任何欄位預設都允許 NULL，它的存在純粹是多餘的。

<a id="id-1.9.3.85.9.9"></a>

### 限制條件命名

SQL 標準規定，資料表限制條件與網域限制條件的名稱，在包含該資料表或網域的綱要中必須是唯一的。PostgreSQL 較為寬鬆：它只要求限制條件名稱在附加於特定資料表或網域的限制條件之間是唯一的。然而，以索引為基礎的限制條件（`UNIQUE`、`PRIMARY KEY` 與 `EXCLUDE` 限制條件）並沒有這項額外的自由，因為相關聯的索引與限制條件同名，而索引名稱在同一綱要內的所有關聯之間必須是唯一的。

<a id="id-1.9.3.85.9.10"></a>

### 繼承

透過 `INHERITS` 子句的多重繼承是 PostgreSQL 的語言擴充。SQL:1999 及其後的標準使用不同的語法與不同的語義定義了單一繼承。PostgreSQL 尚未支援 SQL:1999 風格的繼承。

<a id="id-1.9.3.85.9.11"></a>

### 零欄位資料表

PostgreSQL 允許建立沒有欄位的資料表（例如 `CREATE TABLE foo();`）。這是對 SQL 標準的擴充，SQL 標準不允許零欄位資料表。零欄位資料表本身並不是很有用，但禁止它們會為 `ALTER TABLE
DROP COLUMN` 造成奇怪的特殊情況，因此忽略這項規格限制似乎比較簡潔。

<a id="id-1.9.3.85.9.12"></a>

### 多個識別欄位

PostgreSQL 允許一個資料表擁有超過一個識別欄位。標準規定一個資料表最多只能有一個識別欄位。放寬這項限制主要是為了在進行綱要變更或遷移時提供更多彈性。請注意，`INSERT` 命令只支援一個套用於整個陳述式的覆寫子句，因此對於具有不同行為的多個識別欄位，支援並不完善。

<a id="id-1.9.3.85.9.13"></a>

### 產生欄位

選項 `STORED` 與 `VIRTUAL` 並非標準，但其他 SQL 實作也有使用。SQL 標準並未規定產生欄位的儲存方式。

<a id="id-1.9.3.85.9.14"></a>

### `LIKE` 子句

雖然 SQL 標準中有 `LIKE` 子句，但 PostgreSQL 為它所接受的許多選項並不在標準中，而標準中的某些選項 PostgreSQL 也沒有實作。

<a id="id-1.9.3.85.9.15"></a>

### `WITH` 子句

`WITH` 子句是 PostgreSQL 的擴充語法；儲存參數不在標準之中。

<a id="id-1.9.3.85.9.16"></a>

### 資料表空間

PostgreSQL 的資料表空間概念並不屬於標準的一部分。因此，`TABLESPACE` 與 `USING INDEX TABLESPACE` 子句是擴充語法。

<a id="id-1.9.3.85.9.17"></a>

### 型別化資料表

型別化資料表實作了 SQL 標準的一個子集。根據標準，型別化資料表具有對應於底層複合型別的欄位，以及另外一個「自我參照欄位」。PostgreSQL 並未明確支援自我參照欄位。

<a id="id-1.9.3.85.9.18"></a>

### `PARTITION BY` 子句

`PARTITION BY` 子句是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.85.9.19"></a>

### `PARTITION OF` 子句

`PARTITION OF` 子句是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.85.10"></a>

## 另請參閱

[ALTER TABLE](sql-altertable.md), [DROP TABLE](sql-droptable.md), [CREATE TABLE AS](sql-createtableas.md), [CREATE TABLESPACE](sql-createtablespace.md), [CREATE TYPE](sql-createtype.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtable.html)（原文版本：18.6；核對日期：2026-10-04）
