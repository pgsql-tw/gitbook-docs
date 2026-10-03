<a id="SQL-CREATETYPE"></a><a id="id-1.9.3.94.1"></a>

## CREATE TYPE

CREATE TYPE — 定義新的資料型別

<a id="id-1.9.3.94.4"></a>

## 語法

```

CREATE TYPE name AS
    ( [ attribute_name data_type [ COLLATE collation ] [, ... ] ] )

CREATE TYPE name AS ENUM
    ( [ 'label' [, ... ] ] )

CREATE TYPE name AS RANGE (
    SUBTYPE = subtype
    [ , SUBTYPE_OPCLASS = subtype_operator_class ]
    [ , COLLATION = collation ]
    [ , CANONICAL = canonical_function ]
    [ , SUBTYPE_DIFF = subtype_diff_function ]
    [ , MULTIRANGE_TYPE_NAME = multirange_type_name ]
)

CREATE TYPE name (
    INPUT = input_function,
    OUTPUT = output_function
    [ , RECEIVE = receive_function ]
    [ , SEND = send_function ]
    [ , TYPMOD_IN = type_modifier_input_function ]
    [ , TYPMOD_OUT = type_modifier_output_function ]
    [ , ANALYZE = analyze_function ]
    [ , SUBSCRIPT = subscript_function ]
    [ , INTERNALLENGTH = { internallength | VARIABLE } ]
    [ , PASSEDBYVALUE ]
    [ , ALIGNMENT = alignment ]
    [ , STORAGE = storage ]
    [ , LIKE = like_type ]
    [ , CATEGORY = category ]
    [ , PREFERRED = preferred ]
    [ , DEFAULT = default ]
    [ , ELEMENT = element ]
    [ , DELIMITER = delimiter ]
    [ , COLLATABLE = collatable ]
)

CREATE TYPE name
```

<a id="id-1.9.3.94.5"></a>

## 說明

`CREATE TYPE` 會註冊一個新的資料型別，供目前資料庫使用。定義型別的使用者會成為該型別的擁有者。

若指定了綱要名稱，型別會建立在指定的綱要中；否則會建立在目前的綱要中。型別名稱必須與同一綱要中任何現有型別或網域的名稱不同。（由於資料表具有相關聯的資料型別，型別名稱也必須與同一綱要中任何現有資料表的名稱不同。）

如上方語法摘要所示，`CREATE TYPE` 有五種形式，分別建立*複合型別*、*列舉型別*、*範圍型別*、*基礎型別*或*殼型別*（shell type）。前四種將在下文依序討論。殼型別只是供稍後定義之型別使用的預留位置；發出只帶型別名稱、不帶其他參數的 `CREATE TYPE` 即可建立。如相關各節所述，建立範圍型別與基礎型別時，需要以殼型別作為前向參照。

<a id="id-1.9.3.94.5.5"></a>

### 複合型別

`CREATE TYPE` 的第一種形式會建立複合型別。複合型別由屬性名稱與資料型別的清單來指定。若屬性的資料型別可定序，也可以指定該屬性的定序。複合型別本質上與資料表的資料列型別相同，但若只是想定義一個型別，使用 `CREATE TYPE` 就不需要建立實際的資料表。舉例來說，獨立的複合型別可用作函式的引數型別或回傳型別。

若要建立複合型別，你必須對所有屬性型別具有 `USAGE` 權限。

<a id="SQL-CREATETYPE-ENUM"></a>

### 列舉型別

`CREATE TYPE` 的第二種形式會建立列舉（enum）型別，如[第 8.7 節](../../the-sql-language/datatype/datatype-enum.md)所述。列舉型別接受一串加上引號的標籤，每個標籤的長度都必須小於 `NAMEDATALEN` 個位元組（在標準的 PostgreSQL 建置中為 64 個位元組）。（可以建立沒有任何標籤的列舉型別，但在使用 [`ALTER TYPE`](sql-altertype.md) 加入至少一個標籤之前，這種型別無法用來存放值。）

<a id="SQL-CREATETYPE-RANGE"></a>

### 範圍型別

`CREATE TYPE` 的第三種形式會建立新的範圍型別，如[第 8.17 節](../../the-sql-language/datatype/rangetypes.md)所述。

範圍型別的 *`subtype`* 可以是任何具有相關聯 b-tree 運算子類別的型別（用以決定範圍型別中值的排序）。通常會使用子型別預設的 b-tree 運算子類別來決定排序；若要使用非預設的運算子類別，請以 *`subtype_opclass`* 指定其名稱。若子型別可定序，且你希望在範圍的排序中使用非預設的定序，請以 *`collation`* 選項指定所需的定序。

選用的 *`canonical`* 函式必須接受一個屬於所定義範圍型別的引數，並回傳同一型別的值。在適用的情況下，此函式用於將範圍值轉換為正規形式。更多資訊請參閱[第 8.17.8 節](../../the-sql-language/datatype/rangetypes.md#RANGETYPES-DEFINING)。建立 *`canonical`* 函式有點棘手，因為它必須在範圍型別能夠宣告之前就先定義。為此，你必須先建立一個殼型別，這是一種除了名稱與擁有者之外沒有任何屬性的預留位置型別。做法是發出命令 `CREATE TYPE name`，不帶其他參數。接著就可以使用該殼型別作為引數與結果來宣告函式，最後再使用相同的名稱宣告範圍型別。這會自動以有效的範圍型別取代殼型別的項目。

選用的 *`subtype_diff`* 函式必須接受兩個 *`subtype`* 型別的值作為引數，並回傳一個 `double precision` 值，表示這兩個給定值之間的差。雖然此函式是選用的，但提供它可以大幅提升範圍型別欄位上 GiST 索引的效率。更多資訊請參閱[第 8.17.8 節](../../the-sql-language/datatype/rangetypes.md#RANGETYPES-DEFINING)。

選用的 *`multirange_type_name`* 參數指定對應之多重範圍型別的名稱。若未指定，此名稱會依下列方式自動選定。若範圍型別名稱包含子字串 `range`，則多重範圍型別名稱的形成方式，是將範圍型別名稱中的子字串 `range` 替換為 `multirange`。否則，多重範圍型別名稱的形成方式，是在範圍型別名稱後附加後綴 `_multirange`。

若要建立範圍型別，你必須對子型別具有 `USAGE` 權限。

<a id="id-1.9.3.94.5.8"></a>

### 基礎型別

`CREATE TYPE` 的第四種形式會建立新的基礎型別（純量型別）。若要建立新的基礎型別，你必須是超級使用者。（設下此限制是因為錯誤的型別定義可能使伺服器混亂，甚至導致伺服器當機。）

這些參數可以依任何順序出現，不限於上方所示的順序，而且大多數都是選用的。在定義型別之前，你必須先（使用 `CREATE FUNCTION`）註冊兩個或更多函式。支援函式 *`input_function`* 與 *`output_function`* 是必要的，而函式 *`receive_function`*、*`send_function`*、*`type_modifier_input_function`*、*`type_modifier_output_function`*、*`analyze_function`* 與 *`subscript_function`* 則是選用的。這些函式通常必須以 C 或其他低階語言撰寫。

*`input_function`* 會將型別的外部文字表示形式，轉換為該型別所定義之運算子與函式所使用的內部表示形式。*`output_function`* 則執行反向的轉換。輸入函式可以宣告為接受一個 `cstring` 型別的引數，或宣告為接受三個型別分別為 `cstring`、`oid`、`integer` 的引數。第一個引數是以 C 字串表示的輸入文字，第二個引數是該型別本身的 OID（陣列型別除外，陣列型別收到的是其元素型別的 OID），第三個引數則是目標欄位的 `typmod`（若已知；若未知則會傳入 -1）。輸入函式必須回傳該資料型別本身的值。通常，輸入函式應該宣告為 STRICT；若不是，則在讀取 NULL 輸入值時，會以 NULL 作為第一個參數來呼叫它。在此情況下，該函式仍必須回傳 NULL，除非它引發錯誤。（此情況主要是為了支援網域的輸入函式，這類函式可能需要拒絕 NULL 輸入。）輸出函式必須宣告為接受一個新資料型別的引數。輸出函式必須回傳 `cstring` 型別。對於 NULL 值，不會呼叫輸出函式。

選用的 *`receive_function`* 會將型別的外部二進位表示形式轉換為內部表示形式。若未提供此函式，該型別就無法參與二進位輸入。二進位表示形式應該選擇轉換成內部形式時成本低廉、同時又具有合理可攜性的形式。（例如，標準整數資料型別使用網路位元組順序作為外部二進位表示形式，而內部表示形式則採用機器原生的位元組順序。）接收函式應該進行足夠的檢查，以確保值是有效的。接收函式可以宣告為接受一個 `internal` 型別的引數，或宣告為接受三個型別分別為 `internal`、`oid`、`integer` 的引數。第一個引數是指向存放所接收位元組字串之 `StringInfo` 緩衝區的指標；其餘選用引數與文字輸入函式的相同。接收函式必須回傳該資料型別本身的值。通常，接收函式應該宣告為 STRICT；若不是，則在讀取 NULL 輸入值時，會以 NULL 作為第一個參數來呼叫它。在此情況下，該函式仍必須回傳 NULL，除非它引發錯誤。（此情況主要是為了支援網域的接收函式，這類函式可能需要拒絕 NULL 輸入。）同樣地，選用的 *`send_function`* 會從內部表示形式轉換為外部二進位表示形式。若未提供此函式，該型別就無法參與二進位輸出。傳送函式必須宣告為接受一個新資料型別的引數。傳送函式必須回傳 `bytea` 型別。對於 NULL 值，不會呼叫傳送函式。

此時你應該會感到疑惑：輸入與輸出函式必須在新型別建立之前就先建立，那它們要如何宣告為以新型別作為結果或引數？答案是應該先將該型別定義為*殼型別*，這是一種除了名稱與擁有者之外沒有任何屬性的預留位置型別。做法是發出命令 `CREATE TYPE name`，不帶其他參數。接著就可以定義參照該殼型別的 C 輸入／輸出函式。最後，帶有完整定義的 `CREATE TYPE` 會以完整且有效的型別定義取代殼型別的項目，之後新型別就可以正常使用。

若型別支援修飾詞，也就是附加在型別宣告上的選用限制條件，例如 `char(5)` 或 `numeric(30,2)`，則需要選用的 *`type_modifier_input_function`* 與 *`type_modifier_output_function`*。PostgreSQL 允許使用者自訂型別接受一個或多個簡單的常數或識別字作為修飾詞。不過，這些資訊必須能夠打包成單一的非負整數值，以便儲存在系統目錄中。*`type_modifier_input_function`* 會以 `cstring` 陣列的形式接收所宣告的修飾詞。它必須檢查這些值是否有效（若值有誤則擲出錯誤），若值正確，則回傳單一的非負 `integer` 值，該值會儲存為欄位的「typmod」。若型別沒有 *`type_modifier_input_function`*，型別修飾詞會被拒絕。*`type_modifier_output_function`* 會將內部的整數 typmod 值轉換回適合顯示給使用者的正確形式。它必須回傳一個 `cstring` 值，該值是要附加在型別名稱後的確切字串；例如 `numeric` 的函式可能會回傳 `(30,2)`。可以省略 *`type_modifier_output_function`*，此時預設的顯示格式就只是以括號括住的已儲存 typmod 整數值。

選用的 *`analyze_function`* 會為該資料型別的欄位執行特定於型別的統計資料收集。預設情況下，若該型別有預設的 b-tree 運算子類別，`ANALYZE` 會嘗試使用該型別的「等於」與「小於」運算子來收集統計資料。對於非純量型別，這種行為很可能不適用，因此可以指定自訂的分析函式來覆寫它。分析函式必須宣告為接受單一個 `internal` 型別的引數，並回傳 `boolean` 結果。分析函式的詳細 API 請見 `src/include/commands/vacuum.h`。

選用的 *`subscript_function`* 允許在 SQL 命令中對該資料型別使用下標。指定此函式並不會使該型別被視為「真正的」陣列型別；例如，它不會成為 `ARRAY[]` 建構式結果型別的候選。但若對該型別的值使用下標，是從中擷取資料的自然表示法，就可以撰寫 *`subscript_function`* 來定義其意義。下標函式必須宣告為接受單一個 `internal` 型別的引數，並回傳 `internal` 結果，該結果是一個指向方法（函式）結構的指標，這些方法實作了下標操作。下標函式的詳細 API 請見 `src/include/nodes/subscripting.h`。閱讀 `src/backend/utils/adt/arraysubs.c` 中的陣列實作，或 `contrib/hstore/hstore_subs.c` 中較簡單的程式碼，也可能有所幫助。更多資訊請見下方的[陣列型別](sql-createtype.md#SQL-CREATETYPE-ARRAY)。

雖然新型別內部表示形式的細節只有輸入／輸出函式以及你為處理該型別而建立的其他函式知道，但內部表示形式有幾項屬性必須向 PostgreSQL 宣告。其中最重要的是 *`internallength`*。基礎資料型別可以是固定長度，此時 *`internallength`* 為正整數；也可以是變動長度，以將 *`internallength`* 設為 `VARIABLE` 來表示。（在內部，這是以將 `typlen` 設為 -1 來表示。）所有變動長度型別的內部表示形式，都必須以一個 4 位元組整數開頭，表示該型別這個值的總長度。（請注意，長度欄位經常經過編碼，如[第 66.2 節](../../internals/storage/storage-toast.md)所述；直接存取它並不明智。）

選用旗標 `PASSEDBYVALUE` 表示此資料型別的值以傳值方式傳遞，而非以傳參考方式傳遞。以傳值方式傳遞的型別必須是固定長度，且其內部表示形式不能大於 `Datum` 型別的大小（在某些機器上為 4 個位元組，在其他機器上為 8 個位元組）。

*`alignment`* 參數指定該資料型別所需的儲存對齊方式。允許的值相當於在 1、2、4 或 8 位元組邊界上對齊。請注意，變動長度型別的對齊必須至少為 4，因為它們必然以一個 `int4` 作為第一個組成部分。

*`storage`* 參數可為變動長度資料型別選擇儲存策略。（固定長度型別只允許 `plain`。）`plain` 指定該型別的資料一律以內嵌（in-line）方式儲存，且不壓縮。`extended` 指定系統會先嘗試壓縮過長的資料值，若壓縮後仍然太長，則將該值移出主資料表的資料列。`external` 允許將值移出主資料表，但系統不會嘗試壓縮它。`main` 允許壓縮，但不鼓勵將值移出主資料表。（若沒有其他方法能讓資料列容納得下，採用此儲存策略的資料項目仍可能被移出主資料表，但相較於 `extended` 與 `external` 項目，它們會優先保留在主資料表中。）

除了 `plain` 之外的所有 *`storage`* 值，都意味著該資料型別的函式能夠處理經過 *TOAST 處理*（toasted）的值，如[第 66.2 節](../../internals/storage/storage-toast.md)與[第 36.13.1 節](../../server-programming/extend/xtypes.md#XTYPES-TOAST)所述。所給定的特定其他值，只決定可 TOAST 資料型別之欄位的預設 TOAST 儲存策略；使用者可以使用 `ALTER TABLE SET STORAGE` 為個別欄位選擇其他策略。

*`like_type`* 參數提供另一種指定資料型別基本表示屬性的方法：從某個現有型別複製這些屬性。*`internallength`*、*`passedbyvalue`*、*`alignment`* 與 *`storage`* 的值會從所指名的型別複製而來。（可以藉由在 `LIKE` 子句之外同時指定其中某些值來覆寫它們，但這通常並不理想。）當新型別的低階實作以某種方式「搭便車」建立在現有型別之上時，以這種方式指定表示形式特別有用。

*`category`* 與 *`preferred`* 參數可用來協助控制在模稜兩可的情況下要套用哪一種隱含轉型。每個資料型別都屬於一個以單一 ASCII 字元命名的類別，而每個型別在其類別中要嘛是「偏好」型別，要嘛不是。當此規則有助於解析多載的函式或運算子時，剖析器會偏好轉型為偏好型別（但只從同一類別中的其他型別轉型）。更多細節請參閱[第 10 章](../../the-sql-language/typeconv/README.md)。對於與任何其他型別之間都沒有隱含轉型的型別，將這些設定保留為預設值就足夠了。不過，對於一組具有隱含轉型的相關型別，將它們全部標記為屬於同一類別，並選擇其中一兩個「最通用」的型別作為該類別中的偏好型別，通常會有所幫助。在將使用者自訂型別加入現有的內建類別（例如數值或字串型別）時，*`category`* 參數特別有用。不過，也可以建立全新、完全由使用者自訂的型別類別。可以選擇除了大寫字母以外的任何 ASCII 字元來命名這種類別。

若使用者希望該資料型別的欄位預設為 null 值以外的其他值，可以指定預設值。使用 `DEFAULT` 關鍵字指定預設值。（這種預設值可以被附加在特定欄位上的明確 `DEFAULT` 子句覆寫。）

若要表示某個型別是固定長度的陣列型別，請使用 `ELEMENT` 關鍵字指定陣列元素的型別。例如，若要定義 4 位元組整數（`int4`）的陣列，請指定 `ELEMENT = int4`。更多細節請參閱下方的[陣列型別](sql-createtype.md#SQL-CREATETYPE-ARRAY)。

若要指定此型別之陣列的外部表示形式中，值與值之間所使用的分隔符號，可以將 *`delimiter`* 設定為特定字元。預設的分隔符號是逗號（`,`）。請注意，分隔符號是與陣列元素型別相關聯，而不是與陣列型別本身相關聯。

若選用的布林參數 *`collatable`* 為真，則該型別的欄位定義與運算式可以透過 `COLLATE` 子句攜帶定序資訊。是否實際使用定序資訊，取決於操作該型別之函式的實作；僅僅將型別標記為可定序，並不會自動做到這一點。

<a id="SQL-CREATETYPE-ARRAY"></a>

### 陣列型別

每當建立使用者自訂型別時，PostgreSQL 都會自動建立一個相關聯的陣列型別，其名稱由元素型別的名稱前面加上底線構成，並在必要時截斷，使其長度小於 `NAMEDATALEN` 個位元組。（若如此產生的名稱與現有的型別名稱衝突，則會重複此過程，直到找到不衝突的名稱為止。）這個隱含建立的陣列型別是變動長度，並使用內建的輸入與輸出函式 `array_in` 與 `array_out`。此外，系統在處理該使用者自訂型別上的 `ARRAY[]` 等建構式時，所使用的就是這個型別。陣列型別會追蹤其元素型別之擁有者或綱要的任何變更，且若元素型別被移除，陣列型別也會被移除。

你可能會合理地問：既然系統會自動建立正確的陣列型別，為什麼還有 `ELEMENT` 選項？使用 `ELEMENT` 的主要情況，是當你建立的固定長度型別在內部恰好是由若干個相同項目組成的陣列，而且除了你打算為整個型別提供的任何操作之外，你還希望允許透過下標直接存取這些項目。例如，`point` 型別的表示形式就只是兩個浮點數，可以使用 `point[0]` 與 `point[1]` 來存取。請注意，此功能只適用於內部形式恰好是一連串相同固定長度欄位的固定長度型別。由於歷史因素（也就是說，這顯然是錯誤的，但要更改已經太遲了），固定長度陣列型別的下標從零開始，而不是像變動長度陣列那樣從一開始。

指定 `SUBSCRIPT` 選項可以讓資料型別使用下標，即使系統在其他方面並不將它視為陣列型別。上述固定長度陣列的行為，實際上是由 `SUBSCRIPT` 處理函式 `raw_array_subscript_handler` 實作的；若你為固定長度型別指定了 `ELEMENT`，卻沒有同時寫出 `SUBSCRIPT`，就會自動使用此處理函式。

指定自訂的 `SUBSCRIPT` 函式時，不需要指定 `ELEMENT`，除非 `SUBSCRIPT` 處理函式需要查詢 `typelem` 才能得知要回傳什麼。請注意，指定 `ELEMENT` 會使系統假設新型別包含元素型別，或以某種方式在實體上相依於元素型別；因此，舉例來說，若有任何欄位屬於相依型別，就不允許變更元素型別的屬性。

<a id="id-1.9.3.94.6"></a>

## 參數

*`name`*
:   要建立之型別的名稱（可選擇以綱要限定）。

*`attribute_name`*
:   複合型別之屬性（欄位）的名稱。

*`data_type`*
:   一個現有資料型別的名稱，該型別將成為複合型別的一個欄位。

*`collation`*
:   一個現有定序的名稱，將與複合型別的欄位或範圍型別相關聯。

*`label`*
:   一個字串常值，表示與列舉型別的某一個值相關聯的文字標籤。

*`subtype`*
:   範圍型別所表示之範圍的元素型別名稱。

*`subtype_operator_class`*
:   子型別之 b-tree 運算子類別的名稱。

*`canonical_function`*
:   範圍型別之正規化函式的名稱。

*`subtype_diff_function`*
:   子型別之差值函式的名稱。

*`multirange_type_name`*
:   對應之多重範圍型別的名稱。

*`input_function`*
:   一個函式的名稱，該函式將資料從型別的外部文字形式轉換為內部形式。

*`output_function`*
:   一個函式的名稱，該函式將資料從型別的內部形式轉換為外部文字形式。

*`receive_function`*
:   一個函式的名稱，該函式將資料從型別的外部二進位形式轉換為內部形式。

*`send_function`*
:   一個函式的名稱，該函式將資料從型別的內部形式轉換為外部二進位形式。

*`type_modifier_input_function`*
:   一個函式的名稱，該函式將型別的修飾詞陣列轉換為內部形式。

*`type_modifier_output_function`*
:   一個函式的名稱，該函式將型別修飾詞的內部形式轉換為外部文字形式。

*`analyze_function`*
:   一個函式的名稱，該函式為該資料型別執行統計分析。

*`subscript_function`*
:   一個函式的名稱，該函式定義對該資料型別的值使用下標時的作用。

*`internallength`*
:   一個數值常數，指定新型別內部表示形式的長度（以位元組為單位）。預設假設它是變動長度。

*`alignment`*
:   該資料型別的儲存對齊要求。若有指定，必須是 `char`、`int2`、`int4` 或 `double`；預設為 `int4`。

*`storage`*
:   該資料型別的儲存策略。若有指定，必須是 `plain`、`external`、`extended` 或 `main`；預設為 `plain`。

*`like_type`*
:   一個現有資料型別的名稱，新型別將具有與其相同的表示形式。*`internallength`*、*`passedbyvalue`*、*`alignment`* 與 *`storage`* 的值會從該型別複製而來，除非在此 `CREATE TYPE` 命令的其他地方以明確指定的方式覆寫。

*`category`*
:   此型別的類別代碼（單一 ASCII 字元）。預設為 `'U'`，表示「使用者自訂型別」。其他標準類別代碼可在[表 52.65](../../internals/catalogs/catalog-pg-type.md#CATALOG-TYPCATEGORY-TABLE)中找到。你也可以選擇其他 ASCII 字元來建立自訂類別。

*`preferred`*
:   若此型別是其型別類別中的偏好型別則為真，否則為假。預設為假。在現有的型別類別中建立新的偏好型別時要非常小心，因為這可能導致令人意外的行為變化。

*`default`*
:   該資料型別的預設值。若省略，預設值為 null。

*`element`*
:   所建立的型別是陣列；此參數指定陣列元素的型別。

*`delimiter`*
:   以此型別構成的陣列中，值與值之間所使用的分隔字元。

*`collatable`*
:   若此型別的操作可以使用定序資訊則為真。預設為假。

<a id="SQL-CREATETYPE-NOTES"></a>

## 注意事項

由於資料型別一旦建立後，其使用就沒有任何限制，因此建立基礎型別或範圍型別，就等同於將型別定義中提及之函式的執行權限授予 public。對於型別定義中會用到的那類函式而言，這通常不成問題。但若你設計的型別在轉換為外部形式或從外部形式轉換時，需要用到「機密」資訊，就應該三思。

在 PostgreSQL 8.3 版之前，所產生之陣列型別的名稱一律恰好是元素型別的名稱前面加上一個底線字元（`_`）。（因此，型別名稱的長度限制比其他名稱少一個字元。）雖然現在通常仍是如此，但在名稱達到最大長度，或與以底線開頭的使用者型別名稱衝突時，陣列型別名稱可能與此不同。因此，不建議撰寫依賴此慣例的程式碼。請改用 `pg_type`.`typarray` 來找出與給定型別相關聯的陣列型別。

或許最好避免使用以底線開頭的型別名稱與資料表名稱。雖然伺服器會變更所產生的陣列型別名稱，以避免與使用者給定的名稱衝突，但仍有造成混淆的風險，尤其是對於可能假設以底線開頭的型別名稱一律代表陣列的舊版用戶端軟體。

在 PostgreSQL 8.2 版之前，並沒有建立殼型別的語法 `CREATE TYPE name`。當時建立新基礎型別的方式，是先建立其輸入函式。在這種做法中，PostgreSQL 會先將新資料型別的名稱視為輸入函式的回傳型別。在此情況下會隱含建立殼型別，之後就可以在其餘輸入／輸出函式的定義中參照它。這種做法仍然有效，但已不建議使用，且可能在未來的某個版本中被禁止。此外，為了避免因函式定義中的單純打字錯誤而意外讓系統目錄中堆滿殼型別，只有在輸入函式以 C 撰寫時，才會以這種方式建立殼型別。

在 PostgreSQL 16 版及更新版本中，基礎型別的輸入函式最好使用新的 `errsave()`/`ereturn()` 機制回傳「軟性」錯誤，而不是像先前版本那樣擲出 `ereport()` 例外。更多資訊請參閱 `src/backend/utils/fmgr/README`。

<a id="id-1.9.3.94.8"></a>

## 範例

此範例建立一個複合型別，並在函式定義中使用它：

```

CREATE TYPE compfoo AS (f1 int, f2 text);

CREATE FUNCTION getfoo() RETURNS SETOF compfoo AS $$
    SELECT fooid, fooname FROM foo
$$ LANGUAGE SQL;
```

此範例建立一個列舉型別，並在資料表定義中使用它：

```

CREATE TYPE bug_status AS ENUM ('new', 'open', 'closed');

CREATE TABLE bug (
    id serial,
    description text,
    status bug_status
);
```

此範例建立一個範圍型別：

```

CREATE TYPE float8_range AS RANGE (subtype = float8, subtype_diff = float8mi);
```

此範例建立基礎資料型別 `box`，然後在資料表定義中使用該型別：

```

CREATE TYPE box;

CREATE FUNCTION my_box_in_function(cstring) RETURNS box AS ... ;
CREATE FUNCTION my_box_out_function(box) RETURNS cstring AS ... ;

CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function
);

CREATE TABLE myboxes (
    id integer,
    description box
);
```

若 `box` 的內部結構是由四個 `float4` 元素組成的陣列，我們或許可以改用：

```

CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function,
    ELEMENT = float4
);
```

這樣就可以透過下標存取 box 值的各個組成數字。除此之外，該型別的行為與先前相同。

此範例建立一個大型物件型別，並在資料表定義中使用它：

```

CREATE TYPE bigobj (
    INPUT = lo_filein, OUTPUT = lo_fileout,
    INTERNALLENGTH = VARIABLE
);
CREATE TABLE big_objs (
    id integer,
    obj bigobj
);
```

更多範例（包括合適的輸入與輸出函式）請參閱[第 36.13 節](../../server-programming/extend/xtypes.md)。

<a id="SQL-CREATETYPE-COMPATIBILITY"></a>

## 相容性

`CREATE TYPE` 命令的第一種形式（建立複合型別）符合 SQL 標準。其他形式則是 PostgreSQL 的擴充功能。SQL 標準中的 `CREATE TYPE` 陳述式還定義了 PostgreSQL 未實作的其他形式。

能夠建立沒有任何屬性的複合型別，是 PostgreSQL 特有、偏離標準之處（類似於 `CREATE TABLE` 中的相同情況）。

<a id="SQL-CREATETYPE-SEE-ALSO"></a>

## 另請參閱

[ALTER TYPE](sql-altertype.md), [CREATE DOMAIN](sql-createdomain.md), [CREATE FUNCTION](sql-createfunction.md), [DROP TYPE](sql-droptype.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtype.html)（原文版本：18.6；核對日期：2026-10-03）
