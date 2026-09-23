<a id="EXTEND-EXTENSIONS"></a>
## 36.17. 將相關物件封裝成擴充功能 [#](#EXTEND-EXTENSIONS)

[36.17.1. 擴充功能檔案](extend-extensions.md#EXTEND-EXTENSIONS-FILES)

[36.17.2. 擴充功能的可重新定位性](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION)

[36.17.3. 擴充功能組態資料表](extend-extensions.md#EXTEND-EXTENSIONS-CONFIG-TABLES)

[36.17.4. 擴充功能更新](extend-extensions.md#EXTEND-EXTENSIONS-UPDATES)

[36.17.5. 使用更新指令碼安裝擴充功能](extend-extensions.md#EXTEND-EXTENSIONS-UPDATE-SCRIPTS)

[36.17.6. 擴充功能的安全性考量](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY)

[36.17.7. 擴充功能範例](extend-extensions.md#EXTEND-EXTENSIONS-EXAMPLE)

<a id="id-1.8.3.20.2"></a>

一個有用的 PostgreSQL 擴充功能，通常
包含多個 SQL 物件；舉例來說，一個新的資料型別，
會需要新的函式、新的運算子，也可能需要新的索引
運算子類別。將所有這些物件收集成一個單一的
套件，有助於簡化資料庫管理。PostgreSQL
將這樣的套件稱為*擴充功能（extension）*。要定義一個擴充功能，
您至少需要一個*指令碼檔案（script file）*，
其中包含用來建立該擴充功能物件的 SQL 指令，
以及一個*控制檔（control file）*，
用來指定該擴充功能本身的一些基本屬性。若該擴充功能包含
C 程式碼，通常還會有一個共享程式庫檔案，
C 程式碼會被建置成這個檔案。準備好這些檔案後，
只要一個簡單的
[`CREATE EXTENSION`](../../reference/sql-commands/sql-createextension.md) 指令，
就能將這些物件載入到您的資料庫中。

使用擴充功能，而不是單純執行 SQL
指令碼，將一堆「鬆散」的物件載入資料庫，
其主要優點在於，PostgreSQL 能夠
理解該擴充功能的物件是一個整體。您可以用單一一個
[`DROP EXTENSION`](../../reference/sql-commands/sql-dropextension.md)
指令，刪除所有物件（不需要另外維護一份「解除安裝」指令碼）。
更有用的是，pg_dump 知道不應該
傾印該擴充功能的個別成員物件 — 它只會
在傾印中，包含一個 `CREATE EXTENSION` 指令。
這大幅簡化了遷移到擴充功能新版本的過程，
即使新版本可能包含更多或不同的物件。不過請注意，
當您將這樣的傾印載入新資料庫時，
必須讓該擴充功能的控制檔、指令碼檔及其他檔案，
都是可用的。

PostgreSQL 不允許您刪除某個
擴充功能中所包含的個別物件，除非刪除整個擴充功能。
此外，雖然您可以變更擴充功能成員物件的定義
（舉例來說，透過對函式使用 `CREATE OR REPLACE FUNCTION`），
但請記住，修改後的定義並不會被 pg_dump
傾印出來。這樣的變更，通常只有在您
同時對該擴充功能的指令碼檔案，做出相同變更時，才有意義。
（不過，對於包含組態資料的資料表，另有特殊規定；
請參閱[36.17.3 節](extend-extensions.md#EXTEND-EXTENSIONS-CONFIG-TABLES)。）
在正式環境中，通常最好建立一個擴充功能
更新指令碼，來對擴充功能成員物件進行變更。

擴充功能指令碼，可以使用
`GRANT` 與 `REVOKE`
陳述式，設定屬於該擴充功能的物件之權限。
每個物件的最終權限集合（若有設定的話），
會被儲存在
[`pg_init_privs`](../../internals/catalogs/catalog-pg-init-privs.md)
系統目錄中。當使用 pg_dump 時，
傾印中會包含 `CREATE EXTENSION` 指令，
後面接著必要的一連串 `GRANT` 與
`REVOKE` 陳述式，將這些物件的權限，
設定回傾印當下的狀態。

PostgreSQL 目前不支援在擴充功能指令碼中
發出 `CREATE POLICY` 或 `SECURITY LABEL`
陳述式。這些預期會在該擴充功能建立完成後才設定。
擴充功能物件上的所有 RLS 政策與安全標籤，
都會包含在 pg_dump 所建立的傾印中。

擴充功能機制也有相關規定，可以封裝一些修改
指令碼，用來調整擴充功能中所包含 SQL 物件的定義。
舉例來說，若擴充功能的 1.1 版，比起 1.0 版，
多加了一個函式，並變更了另一個函式的主體，
該擴充功能的作者就可以提供一份*更新
指令碼（update script）*，只做出這兩項變更。接著，
就可以使用 `ALTER EXTENSION UPDATE` 指令，
套用這些變更，並追蹤某個特定資料庫中，
實際安裝的是哪一個版本的擴充功能。

可以作為擴充功能成員的 SQL 物件種類，
顯示於
[`ALTER EXTENSION`](../../reference/sql-commands/sql-alterextension.md) 的說明中。
特別要注意的是，資料庫叢集層級的物件，
例如資料庫、角色與表空間，都不能作為擴充功能的成員，
因為擴充功能只在單一一個資料庫中被認識。
（雖然並不禁止擴充功能指令碼建立這類物件，
但若這麼做，它們就不會被追蹤為該擴充功能的一部分。）
此外請注意，雖然資料表可以是擴充功能的成員，
但其附屬物件，例如索引，並不會被直接視為
該擴充功能的成員。
另一個重點是，綱要可以屬於擴充功能，但反過來卻不行：
擴充功能本身有一個不帶綱要修飾的名稱，
並不存在於任何綱要「之內」。不過，擴充功能的成員物件，
在其物件型別合適的情況下，仍會屬於某個綱要。
至於擴充功能是否應該擁有其成員物件所在的
綱要，則視情況而定，未必如此。

若某個擴充功能的指令碼建立了任何暫存物件
（例如暫存資料表），這些物件在目前工作階段的其餘
時間內，會被視為該擴充功能的成員，但會在
工作階段結束時，如同任何暫存物件一樣自動被刪除。這是
「擴充功能成員物件，若不刪除整個擴充功能，
就無法被刪除」這項規則的一個例外。

<a id="EXTEND-EXTENSIONS-FILES"></a>

### 36.17.1. 擴充功能檔案 [#](#EXTEND-EXTENSIONS-FILES)

<a id="id-1.8.3.20.11.2"></a>

`CREATE EXTENSION` 指令，
依賴每個擴充功能各自的控制檔，其命名
必須與該擴充功能相同，並加上 `.control`
後綴，且必須放在安裝環境的
`SHAREDIR/extension` 目錄下。同時
必須至少有一個 SQL 指令碼檔案，其命名遵循
`extension--version.sql`
的樣式（舉例來說，擴充功能 `foo` 的
`1.0` 版，其指令碼檔案為 `foo--1.0.sql`）。
預設情況下，這些指令碼檔案，也會放在
`SHAREDIR/extension` 目錄下；但控制檔
可以為這些指令碼檔案，指定不同的目錄。

擴充功能控制檔的額外位置，可以使用
參數 [extension_control_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH) 來設定。

擴充功能控制檔的檔案格式，與
`postgresql.conf` 檔案相同，
也就是每行一則
*`parameter_name`* `=` *`value`*
指定。允許空白行，以及以
`#` 開頭的註解。對於任何非單一單字或數字的值，
請務必加上引號。

控制檔可以設定以下這些參數：

<a id="EXTEND-EXTENSIONS-FILES-DIRECTORY"></a>

`directory`（`string`） [#](#EXTEND-EXTENSIONS-FILES-DIRECTORY)
:   包含該擴充功能 SQL 指令碼檔案的目錄。
    除非給定的是絕對路徑，否則該名稱是相對於
    找到控制檔的目錄。預設情況下，
    系統會在找到控制檔的同一個目錄中，
    尋找這些指令碼檔案。
<a id="EXTEND-EXTENSIONS-FILES-DEFAULT-VERSION"></a>

`default_version`（`string`） [#](#EXTEND-EXTENSIONS-FILES-DEFAULT-VERSION)
:   該擴充功能的預設版本（若 `CREATE EXTENSION`
    中未指定版本，就會安裝這個版本）。雖然
    這個參數可以省略，但這麼做會導致
    `CREATE EXTENSION` 在未給定 `VERSION`
    選項時失敗，因此一般而言，您並不會想這麼做。
<a id="EXTEND-EXTENSIONS-FILES-COMMENT"></a>

`comment`（`string`） [#](#EXTEND-EXTENSIONS-FILES-COMMENT)
:   關於該擴充功能的註解（任意字串）。這則註解，
    會在初次建立擴充功能時套用，但不會在擴充功能更新期間套用
    （因為這樣可能會覆蓋使用者所加入的註解）。另一種做法，
    是在指令碼檔案中撰寫一則
    [COMMENT](../../reference/sql-commands/sql-comment.md) 指令，來設定該擴充功能的註解。
<a id="EXTEND-EXTENSIONS-FILES-ENCODING"></a>

`encoding`（`string`） [#](#EXTEND-EXTENSIONS-FILES-ENCODING)
:   指令碼檔案所使用的字元集編碼。若這些
    指令碼檔案包含任何非 ASCII 字元，就應該指定此參數。
    否則，這些檔案會被假設為採用資料庫編碼。
<a id="EXTEND-EXTENSIONS-FILES-MODULE-PATHNAME"></a>

`module_pathname`（`string`） [#](#EXTEND-EXTENSIONS-FILES-MODULE-PATHNAME)
:   這個參數的值，會取代指令碼檔案中，每一處
    `MODULE_PATHNAME` 出現的位置。若未
    設定，則不會進行任何取代。一般而言，這通常會設定為
    `shared_library_name`，
    接著 `MODULE_PATHNAME`，就會用於 C 語言函式的
    `CREATE
    FUNCTION` 指令中，如此一來，指令碼
    檔案就不需要將共享程式庫的名稱寫死。
<a id="EXTEND-EXTENSIONS-FILES-REQUIRES"></a>

`requires`（`string`） [#](#EXTEND-EXTENSIONS-FILES-REQUIRES)
:   此擴充功能所依賴的擴充功能名稱清單，
    舉例來說 `requires = 'foo, bar'`。那些
    擴充功能，必須先安裝，此擴充功能才能安裝。
<a id="EXTEND-EXTENSIONS-FILES-NO-RELOCATE"></a>

`no_relocate`（`string`） [#](#EXTEND-EXTENSIONS-FILES-NO-RELOCATE)
:   此擴充功能所依賴的擴充功能名稱清單，
    這些擴充功能應該被禁止透過 `ALTER
    EXTENSION ... SET SCHEMA` 變更其綱要。
    當此擴充功能的指令碼中，以無法追蹤更名的方式，
    參照了某個必要擴充功能綱要的名稱
    （使用 `@extschema:name@`
    語法）時，就需要這麼做。
<a id="EXTEND-EXTENSIONS-FILES-SUPERUSER"></a>

`superuser`（`boolean`） [#](#EXTEND-EXTENSIONS-FILES-SUPERUSER)
:   若此參數為 `true`（這是預設值），
    則只有超級使用者能夠建立該擴充功能，或將其更新
    到新版本（但另請參閱下方的 `trusted`）。
    若設定為 `false`，則只需要
    執行安裝或更新指令碼中指令所需的權限即可。
    若指令碼中有任何指令需要超級使用者權限，
    通常應該將此參數設為 `true`。（這類指令
    無論如何都會失敗，但事先提供錯誤，對使用者來說
    比較友善。）
<a id="EXTEND-EXTENSIONS-FILES-TRUSTED"></a>

`trusted`（`boolean`） [#](#EXTEND-EXTENSIONS-FILES-TRUSTED)
:   若這個參數設為 `true`（這不是
    預設值），就會允許部分非超級使用者，
    安裝 `superuser` 設為 `true`
    的擴充功能。具體來說，
    在目前資料庫上具備 `CREATE`
    權限的任何人，都會被允許進行安裝。
    當執行 `CREATE EXTENSION` 的使用者不是
    超級使用者，但依此參數被允許安裝時，
    安裝或更新指令碼會以啟動用超級使用者（bootstrap
    superuser）身分執行，而不是以呼叫方使用者身分執行。
    若 `superuser` 為
    `false`，此參數就不相關。
    一般而言，若某個擴充功能，可能讓使用者取得
    原本只有超級使用者才有的能力，例如
    檔案系統存取，就不應該將此參數設為 true。
    此外，將擴充功能標記為 trusted，
    需要付出相當額外的心力，才能安全地撰寫該擴充功能的
    安裝與更新指令碼；
    請參閱[36.17.6 節](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY)。
<a id="EXTEND-EXTENSIONS-FILES-RELOCATABLE"></a>

`relocatable`（`boolean`） [#](#EXTEND-EXTENSIONS-FILES-RELOCATABLE)
:   若某個擴充功能，可以在初次建立之後，
    將其所包含的物件移動到不同的綱要中，
    則稱為*可重新定位（relocatable）*的。預設值為
    `false`，也就是該擴充功能不可重新定位。
    詳情請參閱[36.17.2 節](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION)。
<a id="EXTEND-EXTENSIONS-FILES-SCHEMA"></a>

`schema`（`string`） [#](#EXTEND-EXTENSIONS-FILES-SCHEMA)
:   這個參數，只能為不可重新定位的擴充功能設定。
    它強制該擴充功能，只能被載入到指定名稱的綱要中，
    而不能是其他任何綱要。
    `schema` 參數，只有在初次建立擴充功能時，
    才會被參考，在擴充功能更新期間則不會。
    詳情請參閱[36.17.2 節](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION)。

除了主要的控制檔
`extension.control` 之外，
擴充功能還可以擁有以
`extension--version.control`
樣式命名的次要控制檔。
若有提供，這些檔案必須位於指令碼檔案目錄中。
次要控制檔，遵循與主要控制檔相同的格式。
在安裝或更新到某個版本的擴充功能時，
次要控制檔中所設定的任何參數，都會覆蓋主要
控制檔中的設定。不過，`directory` 與
`default_version` 這兩個參數，不能在次要控制檔中設定。

擴充功能的 SQL 指令碼檔案，可以包含任何 SQL 指令，
但交易控制指令（`BEGIN`、
`COMMIT` 等）除外，以及無法在
交易區塊內執行的指令（例如 `VACUUM`）
也除外。這是因為指令碼檔案，是隱含地
在一個交易區塊內執行的。

擴充功能的 SQL 指令碼檔案，也可以包含以
`\echo` 開頭的行，這些行會被擴充功能機制
忽略（視為註解）。這項規定，通常用於
在指令碼檔案被餵給 psql，而非透過
`CREATE EXTENSION` 載入時，拋出錯誤（請參閱
[36.17.7 節](extend-extensions.md#EXTEND-EXTENSIONS-EXAMPLE)中的範例指令碼）。
若沒有這項規定，使用者可能會不小心，
將該擴充功能的內容，當作「鬆散」的物件載入，
而不是當作一個擴充功能載入，這種狀態，
要復原起來相當繁瑣。

若擴充功能指令碼中包含
字串 `@extowner@`，該字串會被替換為呼叫
`CREATE
EXTENSION` 或 `ALTER EXTENSION` 的使用者名稱
（並附帶適當的引號）。通常，這項功能
是由標記為 trusted 的擴充功能所使用，用來將所選物件的
擁有權，指定給呼叫方使用者，而非啟動用超級使用者。
（不過，這麼做時應該格外小心。
舉例來說，將一個 C 語言函式的擁有權，
指定給非超級使用者，就會為該使用者建立一條
權限提升的路徑。）

雖然指令碼檔案可以包含指定編碼所允許的任何字元，
但控制檔應該只包含純 ASCII，因為
PostgreSQL 沒有辦法得知控制檔
是採用什麼編碼的。實務上，這只有在您想要
在擴充功能的註解中使用非 ASCII 字元時，才會構成問題。
在這種情況下，建議的做法，是不要使用控制檔的
`comment` 參數，而是改用指令碼檔案中的
`COMMENT ON EXTENSION`
來設定該註解。

<a id="EXTEND-EXTENSIONS-RELOCATION"></a>

### 36.17.2. 擴充功能的可重新定位性 [#](#EXTEND-EXTENSIONS-RELOCATION)

使用者經常希望，將擴充功能所包含的物件，
載入到與該擴充功能作者原本設想不同的綱要中。共有
三種支援的可重新定位層級：

* 完全可重新定位的擴充功能，可以在任何時候，
  甚至在它已經被載入到資料庫之後，被移動到
  另一個綱要中。這是透過 `ALTER EXTENSION SET SCHEMA`
  指令完成的，它會自動將所有成員物件，
  更名到新的綱要中。一般而言，這只有在
  該擴充功能不包含任何關於其物件所在綱要的
  內部假設時，才有可能。此外，該擴充功能的物件，
  一開始都必須位於同一個綱要中（忽略不屬於任何
  綱要的物件，例如程序語言）。若要將某個擴充功能
  標記為完全可重新定位，請在其控制檔中設定
  `relocatable = true`。
* 某個擴充功能，可能在安裝期間可重新定位，
  但之後就不行了。若該擴充功能的指令碼
  檔案，需要明確參照目標綱要，例如
  在為 SQL 函式設定 `search_path` 屬性時，
  通常就會是這種情況。對於這樣的擴充功能，
  請在其控制檔中設定 `relocatable = false`，
  並在指令碼檔案中使用 `@extschema@`
  來參照目標綱要。在指令碼執行之前，
  這個字串的所有出現位置，都會被替換為
  實際目標綱要的名稱（若有必要，會加上雙引號）。
  使用者可以透過 `CREATE EXTENSION` 的
  `SCHEMA` 選項，來設定目標綱要。
* 若該擴充功能完全不支援重新定位，
  請在其控制檔中設定 `relocatable = false`，
  並同時設定 `schema` 為預期目標綱要的名稱。這樣
  就會阻止使用 `CREATE
  EXTENSION` 的 `SCHEMA` 選項，除非該選項
  指定的綱要，與控制檔中指定的綱要相同。當該擴充功能
  包含無法透過使用 `@extschema@` 取代的、
  關於其綱要名稱的內部假設時，通常就有必要
  這麼做。在這種情況下，`@extschema@`
  取代機制同樣可用，不過因為
  綱要名稱是由控制檔決定的，其用途有限。

在所有情況下，指令碼檔案在執行時，
[search_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-SEARCH-PATH) 都會先被設定為指向目標
綱要；也就是說，`CREATE EXTENSION`
會做等同於以下的事：

```

SET LOCAL search_path TO @extschema@, pg_temp;
```

這讓指令碼檔案所建立的物件，能夠進入目標
綱要。若指令碼檔案願意，也可以變更 `search_path`，
但通常並不建議這麼做。`CREATE EXTENSION`
完成後，`search_path` 會還原為先前的設定。

目標綱要的決定方式為：若控制檔中給定了
`schema` 參數，則以此為準；否則，
若給定了 `CREATE EXTENSION` 的 `SCHEMA`
選項，則以此為準；否則，則使用目前預設的
物件建立綱要（也就是呼叫方
`search_path` 中的第一個）。當使用控制檔的
`schema` 參數時，若目標綱要尚不存在，
就會建立它，但在另外兩種情況下，
該綱要必須已經存在。

若控制檔的 `requires` 中，
列出了任何必要的擴充功能，它們的目標綱要，
會被加入 `search_path` 的初始設定中，
並排在新擴充功能的目標綱要之後。這讓
它們的物件，能夠讓新擴充功能的指令碼檔案看見。

基於安全考量，在所有情況下，
`pg_temp` 都會自動附加到
`search_path` 的最後。

雖然不可重新定位的擴充功能，可以擁有分散在
多個綱要中的物件，但通常最好將所有供外部使用
的物件，放入單一一個綱要中，並將其視為該擴充功能的
目標綱要。這樣的安排，在建立依賴的
擴充功能時，能與 `search_path` 的預設
設定配合得很順暢。

若某個擴充功能參照了屬於另一個擴充功能的物件，
建議對這些參照加上綱要修飾。要這麼做，
請在該擴充功能的指令碼檔案中，寫上
`@extschema:name@`，
其中 *`name`* 是另一個擴充功能的名稱
（該名稱必須列在此擴充功能的
`requires` 清單中）。這個字串，會被替換為
該擴充功能目標綱要的名稱（若有必要，
會加上雙引號）。
雖然這種寫法，避免了在擴充功能指令碼檔案中，
對綱要名稱做出寫死的假設，但它的使用，
可能會將另一個擴充功能的綱要名稱，
嵌入到此擴充功能所安裝的物件中。（通常，
這種情況會發生在
`@extschema:name@`
被用在字串常值內部時，例如函式主體或
`search_path` 設定。在其他情況下，
物件參照會在剖析期間，被化簡為一個 OID，
不需要後續的查詢。）若另一個擴充功能的綱要名稱，
就這樣被嵌入了，您應該防止該擴充功能，
在您的擴充功能安裝之後被重新定位，做法是將
該擴充功能的名稱，加入這個擴充功能的
`no_relocate` 清單中。

<a id="EXTEND-EXTENSIONS-CONFIG-TABLES"></a>

### 36.17.3. 擴充功能組態資料表 [#](#EXTEND-EXTENSIONS-CONFIG-TABLES)

有些擴充功能，包含組態資料表，
其中含有使用者在安裝該擴充功能後，
可能會新增或變更的資料。一般而言，若某個資料表
是擴充功能的一部分，pg_dump 既不會傾印該資料表
的定義，也不會傾印其內容。但對於組態
資料表而言，這樣的行為並不理想；使用者所做的任何資料
變更，都需要包含在傾印中，否則該擴充功能
在傾印及還原之後，行為就會不一樣。

<a id="id-1.8.3.20.13.3"></a>

為了解決這個問題，擴充功能的指令碼檔案，
可以將它所建立的某個資料表或序列，標記為組態關係，
這會讓 pg_dump 在傾印中，
包含該資料表或序列的內容（而非其定義）。要這麼做，
請在建立該資料表或序列之後，呼叫函式
`pg_extension_config_dump(regclass, text)`，例如

```

CREATE TABLE my_config (key text, value text);
CREATE SEQUENCE my_config_seq;

SELECT pg_catalog.pg_extension_config_dump('my_config', '');
SELECT pg_catalog.pg_extension_config_dump('my_config_seq', '');
```

可以用這種方式標記任意數量的資料表或序列。
與 `serial` 或 `bigserial` 欄位
相關聯的序列，同樣也可以被標記。

當 `pg_extension_config_dump` 的第二個引數
是空字串時，該資料表的全部內容，都會被 pg_dump
傾印出來。這通常只有在該資料表最初是
由擴充功能指令碼建立為空資料表時，才是正確的做法。
若資料表中，混合了初始資料與使用者提供的資料，
則 `pg_extension_config_dump` 的第二個引數，
可以提供一個 `WHERE` 條件，
用來選取要傾印的資料。舉例來說，您可以這樣做：

```

CREATE TABLE my_config (key text, value text, standard_entry boolean);

SELECT pg_catalog.pg_extension_config_dump('my_config', 'WHERE NOT standard_entry');
```

接著確保 `standard_entry` 只有在由該擴充功能
指令碼所建立的列中，才會是 true。

對於序列而言，`pg_extension_config_dump`
的第二個引數沒有作用。

更複雜的情況，例如可能會被使用者修改的初始
提供資料列，可以透過在組態資料表上建立觸發程序，
來確保已修改的資料列被正確標記。

您可以透過再次呼叫 `pg_extension_config_dump`，
變更與某個組態資料表相關聯的篩選條件。（這通常
會在擴充功能更新指令碼中派上用場。）要將某個資料表
標記為不再是組態資料表，唯一的方法，
是透過 `ALTER EXTENSION ... DROP TABLE`，
將它與該擴充功能解除關聯。

請注意，這些資料表之間的外部鍵關係，
會決定 pg_dump 傾印這些資料表的順序。
具體來說，pg_dump 會嘗試在參照它的資料表之前，
先傾印被參照的資料表。由於外部鍵關係，
是在 CREATE EXTENSION 時建立的（在資料被載入
資料表之前），因此不支援循環相依。
當存在循環相依時，資料仍然會被傾印出來，
但該傾印將無法直接還原，需要
使用者介入處理。

與 `serial` 或 `bigserial` 欄位
相關聯的序列，需要直接被標記，才能傾印它們的狀態。
只標記它們所屬的父關係，並不足夠。

<a id="EXTEND-EXTENSIONS-UPDATES"></a>

### 36.17.4. 擴充功能更新 [#](#EXTEND-EXTENSIONS-UPDATES)

擴充功能機制的優點之一，是它提供了方便的
方式，管理定義擴充功能物件的 SQL 指令的更新。
做法是將版本名稱或版本號，與該擴充功能
安裝指令碼的每個發行版本建立關聯。
此外，若您希望使用者能夠動態地，
將他們的資料庫從一個版本更新到下一個版本，
您應該提供*更新指令碼（update script）*，
執行從一個版本移動到下一個版本所需的變更。更新指令碼
遵循以下命名樣式
`extension--old_version--target_version.sql`
（舉例來說，`foo--1.0--1.1.sql` 中，
包含了將擴充功能 `foo` 的
`1.0` 版修改為 `1.1` 版的指令）。

只要有合適的更新指令碼可用，
`ALTER EXTENSION UPDATE` 指令，就能將已安裝的
擴充功能更新到指定的新版本。更新指令碼，
是在與 `CREATE EXTENSION` 為安裝指令碼所提供的
相同環境中執行的：具體來說，`search_path`
的設定方式相同，且該指令碼所建立的任何新物件，
都會自動加入該擴充功能中。此外，若指令碼選擇
刪除擴充功能成員物件，它們也會自動與
該擴充功能解除關聯。

若某個擴充功能有次要控制檔，則用於更新
指令碼的控制參數，是與該指令碼的目標（新）版本
相關聯的那些。

`ALTER EXTENSION` 能夠執行一連串的更新
指令碼檔案，以達成要求的更新。舉例來說，
若只有 `foo--1.0--1.1.sql` 與
`foo--1.1--2.0.sql` 可用，
則當目前已安裝 `1.0`，而要求更新到
`2.0` 版時，`ALTER EXTENSION`
會依序套用它們。

PostgreSQL 對版本名稱的屬性，
不做任何假設：舉例來說，它並不知道
`1.1` 是否接在 `1.0` 之後。它只是
比對可用的版本名稱，並選擇需要套用
最少更新指令碼的路徑。
（版本名稱實際上可以是任何不包含
`--`、也不以 `-` 開頭或結尾的字串。）

有時候，提供「降級」指令碼會很有用，
舉例來說，`foo--1.1--1.0.sql` 可用來
還原與 `1.1` 版相關的變更。若您這麼做，
請小心一種可能性：降級指令碼，可能會因為
它形成較短的路徑，而意外地被套用。
較危險的情況是，同時存在一個「快速路徑」更新指令碼，
一次跳過好幾個版本，以及一個回到該快速路徑
起始點的降級指令碼。先套用降級，
再套用快速路徑，可能所需的步驟，
比一次一個版本地往前更新還要少。若降級指令碼，
刪除了任何不可替代的物件，就會產生不理想的結果。

若要檢查是否有意外的更新路徑，請使用以下指令：

```

SELECT * FROM pg_extension_update_paths('extension_name');
```

這會顯示指定擴充功能中，每一對相異已知版本名稱，
以及從來源版本到目標版本所會採取的
更新路徑順序，若沒有可用的更新路徑，
則顯示 `NULL`。該路徑以文字形式顯示，
以 `--` 分隔。若您偏好陣列
格式，可以使用
`regexp_split_to_array(path,'--')`。

<a id="EXTEND-EXTENSIONS-UPDATE-SCRIPTS"></a>

### 36.17.5. 使用更新指令碼安裝擴充功能 [#](#EXTEND-EXTENSIONS-UPDATE-SCRIPTS)

一個存在了一段時間的擴充功能，可能會有
好幾個版本，作者需要為它們撰寫更新指令碼。
舉例來說，若您已經發行了 `foo` 擴充功能的
`1.0`、`1.1` 與 `1.2` 版，
就應該要有更新指令碼 `foo--1.0--1.1.sql`
與 `foo--1.1--1.2.sql`。
在 PostgreSQL 10 之前，還需要另外建立
新的指令碼檔案 `foo--1.1.sql` 與 `foo--1.2.sql`，
直接建置較新的擴充功能版本，否則
較新版本就無法直接安裝，只能透過先
安裝 `1.0`、再進行更新的方式。這既繁瑣
又重複，但現在已經不需要了，因為 `CREATE
EXTENSION` 能夠自動依循更新鏈。
舉例來說，若只有指令碼
檔案 `foo--1.0.sql`、`foo--1.0--1.1.sql`
與 `foo--1.1--1.2.sql` 可用，
則要求安裝 `1.2` 版時，會依序執行
這三個指令碼來完成。這個處理過程，
與您先安裝 `1.0`、再更新到 `1.2`
是一樣的。（與 `ALTER EXTENSION UPDATE` 相同，
若有多條路徑可用，會偏好較短的那一條。）以這種
風格安排擴充功能的指令碼檔案，可以減少
產生小型更新所需付出的維護心力。

若您在以這種風格維護的擴充功能中，
使用次要（特定版本）控制檔，請記得，
即使某個版本沒有獨立的安裝指令碼，
每個版本仍然需要一個控制檔，因為該控制檔，
將決定該版本隱含更新的執行方式。舉例來說，
若 `foo--1.0.control` 指定了 `requires
= 'bar'`，但 `foo` 的其他控制檔沒有指定，
則在從 `1.0` 更新到另一個版本時，
該擴充功能對 `bar` 的相依關係，就會被移除。

<a id="EXTEND-EXTENSIONS-SECURITY"></a>

### 36.17.6. 擴充功能的安全性考量 [#](#EXTEND-EXTENSIONS-SECURITY)

廣泛發行的擴充功能，應該對其所在的資料庫，
盡量不做假設。因此，撰寫擴充功能所提供的函式時，
採用不會被以 search-path 為基礎的攻擊
所攻破的安全風格，是相當恰當的做法。

`superuser` 屬性設為 true 的擴充功能，
也必須考量其安裝與更新指令碼中，
所執行動作的安全風險。惡意使用者要建立
木馬物件，來破壞之後不夠謹慎撰寫的
擴充功能指令碼的執行，讓該使用者取得
超級使用者權限，並不會太困難。

若某個擴充功能被標記為 `trusted`，
則安裝該擴充功能的使用者，可以自行選擇其安裝
綱要，該使用者有可能為了取得超級使用者
權限，而刻意使用不安全的綱要。因此，
從安全的角度來看，trusted 的擴充功能，
暴露的風險極高，其所有指令碼指令，
都必須經過仔細檢查，以確保不會有任何可能的破綻。

關於如何安全地撰寫函式的建議，
請見下方的[36.17.6.1 節](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY-FUNCS)，
關於如何安全地撰寫安裝指令碼的建議，
請見[36.17.6.2 節](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY-SCRIPTS)。

<a id="EXTEND-EXTENSIONS-SECURITY-FUNCS"></a>

#### 36.17.6.1. 擴充功能函式的安全性考量 [#](#EXTEND-EXTENSIONS-SECURITY-FUNCS)

由擴充功能提供的 SQL 語言與 PL 語言函式，
在執行時，有可能面臨以 search-path 為基礎的攻擊，
因為這些函式的剖析，是在執行時、
而非建立時進行的。

[`CREATE
FUNCTION`](../../reference/sql-commands/sql-createfunction.md#SQL-CREATEFUNCTION-SECURITY) 參考頁面，
包含了關於如何安全地撰寫 `SECURITY DEFINER`
函式的建議。對於擴充功能所提供的任何函式，
都適合套用這些技巧，因為該函式，
可能會被高權限的使用者呼叫。

若您無法將 `search_path` 設定為只包含
安全的綱要，請假設每一個不帶綱要修飾的名稱，
都有可能解析到惡意使用者所定義的物件。請留意
隱含依賴 `search_path` 的結構；舉例來說，
`IN`
與 `CASE expression WHEN`，
永遠都會使用搜尋路徑，來選取運算子。請改用
`OPERATOR(schema.=) ANY`
與 `CASE WHEN expression`，
取代這些寫法。

一個通用用途的擴充功能，通常不應該假設
它已被安裝在一個安全的綱要中，這代表即使是
對自己物件的、帶綱要修飾的參照，
也並非完全沒有風險。舉例來說，
若該擴充功能定義了
函式 `myschema.myfunc(bigint)`，那麼像
`myschema.myfunc(42)` 這樣的呼叫，
就有可能被惡意的函式
`myschema.myfunc(integer)` 攔截。請務必小心，
確保函式與運算子參數的資料型別，
與宣告的引數型別完全相符，必要時使用明確的轉型。

<a id="EXTEND-EXTENSIONS-SECURITY-SCRIPTS"></a>

#### 36.17.6.2. 擴充功能指令碼的安全性考量 [#](#EXTEND-EXTENSIONS-SECURITY-SCRIPTS)

擴充功能的安裝或更新指令碼，應該撰寫成
能夠防範在指令碼執行時，
以 search-path 為基礎的攻擊。若指令碼中的
某個物件參照，能被誘導解析到指令碼作者
原本意圖以外的其他物件，那麼破壞可能會
立即發生，或者稍後在這個定義有誤的
擴充功能物件被使用時發生。

像是 `CREATE FUNCTION`
與 `CREATE OPERATOR CLASS` 這樣的 DDL 指令，
通常是安全的，但請留意任何包含
通用用途運算式作為組成部分的指令。舉例來說，
`CREATE VIEW` 需要經過審查，
`CREATE FUNCTION` 中的 `DEFAULT`
運算式也是如此。

有時候，擴充功能指令碼可能需要執行通用用途的
SQL，舉例來說，為了進行無法透過
DDL 完成的目錄調整。請務必以
安全的 `search_path` 來執行這類指令；
*不要*信任 `CREATE/ALTER EXTENSION`
所提供的路徑是安全的。最佳做法，
是暫時將 `search_path` 設定為 `pg_catalog,
pg_temp`，並在需要的地方，
明確插入對該擴充功能安裝綱要的參照。
（這種做法，對於建立檢視表，也可能有幫助。）
相關範例，可以在
PostgreSQL 原始碼發行套件中的
`contrib` 模組中找到。

安全的跨擴充功能參照，通常需要
使用 `@extschema:name@`
語法，對另一個擴充功能物件的名稱，
進行綱要修飾，此外，也需要仔細比對
函式與運算子的引數型別。

<a id="EXTEND-EXTENSIONS-EXAMPLE"></a>

### 36.17.7. 擴充功能範例 [#](#EXTEND-EXTENSIONS-EXAMPLE)

以下是一個純 SQL 擴充功能的完整範例，
一個雙元素的複合型別，可以在其名為「k」與「v」
的欄位中，儲存任何型別的值。非文字
值，會自動被強制轉型為文字以供儲存。

指令碼檔案 `pair--1.0.sql` 看起來像這樣：

```

-- complain if script is sourced in psql, rather than via CREATE EXTENSION
\echo Use "CREATE EXTENSION pair" to load this file. \quit

CREATE TYPE pair AS ( k text, v text );

CREATE FUNCTION pair(text, text)
RETURNS pair LANGUAGE SQL AS 'SELECT ROW($1, $2)::@extschema@.pair;';

CREATE OPERATOR ~> (LEFTARG = text, RIGHTARG = text, FUNCTION = pair);

-- "SET search_path" is easy to get right, but qualified names perform better.
CREATE FUNCTION lower(pair)
RETURNS pair LANGUAGE SQL
AS 'SELECT ROW(lower($1.k), lower($1.v))::@extschema@.pair;'
SET search_path = pg_temp;

CREATE FUNCTION pair_concat(pair, pair)
RETURNS pair LANGUAGE SQL
AS 'SELECT ROW($1.k OPERATOR(pg_catalog.||) $2.k,
               $1.v OPERATOR(pg_catalog.||) $2.v)::@extschema@.pair;';
```

控制檔 `pair.control` 看起來像這樣：

```

# pair extension
comment = 'A key/value pair data type'
default_version = '1.0'
# cannot be relocatable because of use of @extschema@
relocatable = false
```

雖然您幾乎不需要 makefile，就能將這兩個檔案
安裝到正確的目錄中，但您也可以使用包含以下內容的
`Makefile`：

```

EXTENSION = pair
DATA = pair--1.0.sql

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
```

這個 makefile 依賴 PGXS，說明請見
[36.18 節](extend-pgxs.md)。指令 `make install`，
會依照 pg_config 所回報的結果，
將控制檔與指令碼檔案，安裝到正確的目錄中。

一旦這些檔案安裝完成，就可以使用
`CREATE EXTENSION` 指令，將這些物件，
載入任何特定的資料庫中。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/extend-extensions.html)（原文版本：18.6；核對日期：2026-09-22）
