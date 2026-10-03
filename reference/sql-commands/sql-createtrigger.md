<a id="SQL-CREATETRIGGER"></a><a id="id-1.9.3.93.1"></a><a id="id-1.9.3.93.2"></a>

## CREATE TRIGGER

CREATE TRIGGER — 定義新的觸發程序

<a id="id-1.9.3.93.5"></a>

## 語法

```

CREATE [ OR REPLACE ] [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
    ON table_name
    [ FROM referenced_table_name ]
    [ NOT DEFERRABLE | [ DEFERRABLE ] [ INITIALLY IMMEDIATE | INITIALLY DEFERRED ] ]
    [ REFERENCING { { OLD | NEW } TABLE [ AS ] transition_relation_name } [ ... ] ]
    [ FOR [ EACH ] { ROW | STATEMENT } ]
    [ WHEN ( condition ) ]
    EXECUTE { FUNCTION | PROCEDURE } function_name ( arguments )

where event can be one of:

    INSERT
    UPDATE [ OF column_name [, ... ] ]
    DELETE
    TRUNCATE
```

<a id="id-1.9.3.93.6"></a>

## 說明

`CREATE TRIGGER` 會建立新的觸發程序。`CREATE OR REPLACE TRIGGER` 會建立新的觸發程序，或是取代現有的觸發程序。觸發程序將與指定的資料表、檢視表或外部資料表相關聯，並在對該資料表執行特定操作時執行指定的函式 *`function_name`*。

若要取代現有觸發程序目前的定義，請使用 `CREATE OR REPLACE TRIGGER`，並指定現有觸發程序的名稱及其所屬的上層資料表。所有其他屬性都會被取代。

觸發程序可以指定為在對某一資料列嘗試操作之前觸發（在檢查限制條件並嘗試 `INSERT`、`UPDATE` 或 `DELETE` 之前）；或在操作完成之後觸發（在檢查限制條件且 `INSERT`、`UPDATE` 或 `DELETE` 已完成之後）；或取代該操作（在對檢視表進行插入、更新或刪除的情況下）。若觸發程序在事件之前或取代事件而觸發，觸發程序可以略過對目前資料列的操作，或變更正要插入的資料列（僅限 `INSERT` 與 `UPDATE` 操作）。若觸發程序在事件之後觸發，則所有變更（包括其他觸發程序的作用）對該觸發程序而言都是「可見的」。

標示為 `FOR EACH ROW` 的觸發程序，會針對操作所修改的每一筆資料列各呼叫一次。例如，影響 10 筆資料列的 `DELETE`，會使目標關聯上的任何 `ON DELETE` 觸發程序被分別呼叫 10 次，每筆被刪除的資料列各一次。相對地，標示為 `FOR EACH STATEMENT` 的觸發程序，對任何給定的操作只會執行一次，不論該操作修改了多少資料列（特別是，修改零筆資料列的操作仍然會導致執行任何適用的 `FOR
EACH STATEMENT` 觸發程序）。

指定為 `INSTEAD OF` 觸發程序事件而觸發的觸發程序，必須標示為 `FOR EACH ROW`，而且只能定義在檢視表上。檢視表上的 `BEFORE` 與 `AFTER` 觸發程序必須標示為 `FOR EACH STATEMENT`。

此外，觸發程序也可以定義為針對 `TRUNCATE` 觸發，但只能是 `FOR EACH STATEMENT`。

下表摘要說明哪些類型的觸發程序可以用於資料表、檢視表與外部資料表：

<a id="SUPPORTED-TRIGGER-TYPES"></a>

<table border="1" class="informaltable"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>時機</th><th>事件</th><th>資料列層級</th><th>陳述式層級</th></tr></thead><tbody><tr><td align="center" rowspan="2"><code class="literal">BEFORE</code></td><td align="center"><code class="command">INSERT</code>/<code class="command">UPDATE</code>/<code class="command">DELETE</code></td><td align="center">資料表與外部資料表</td><td align="center">資料表、檢視表與外部資料表</td></tr><tr><td align="center"><code class="command">TRUNCATE</code></td><td align="center">—</td><td align="center">資料表與外部資料表</td></tr><tr><td align="center" rowspan="2"><code class="literal">AFTER</code></td><td align="center"><code class="command">INSERT</code>/<code class="command">UPDATE</code>/<code class="command">DELETE</code></td><td align="center">資料表與外部資料表</td><td align="center">資料表、檢視表與外部資料表</td></tr><tr><td align="center"><code class="command">TRUNCATE</code></td><td align="center">—</td><td align="center">資料表與外部資料表</td></tr><tr><td align="center" rowspan="2"><code class="literal">INSTEAD OF</code></td><td align="center"><code class="command">INSERT</code>/<code class="command">UPDATE</code>/<code class="command">DELETE</code></td><td align="center">檢視表</td><td align="center">—</td></tr><tr><td align="center"><code class="command">TRUNCATE</code></td><td align="center">—</td><td align="center">—</td></tr></tbody></table>

此外，觸發程序定義可以指定一個布林 `WHEN` 條件，用來測試是否應該觸發該觸發程序。在資料列層級觸發程序中，`WHEN` 條件可以檢查該資料列欄位的舊值和／或新值。陳述式層級觸發程序也可以有 `WHEN` 條件，不過這項功能對它們並沒有那麼有用，因為條件無法參照資料表中的任何值。

若為同一事件定義了多個相同種類的觸發程序，它們會依名稱的字母順序觸發。

指定 `CONSTRAINT` 選項時，此命令會建立一個*限制條件觸發程序*。<a id="id-1.9.3.93.6.12.3"></a>它與一般觸發程序相同，差別在於觸發程序觸發的時機可以使用 [`SET CONSTRAINTS`](sql-set-constraints.md) 調整。限制條件觸發程序必須是一般資料表（而非外部資料表）上的 `AFTER ROW` 觸發程序。它們可以在引發觸發事件之陳述式的結尾觸發，也可以在所屬交易的結尾觸發；後者的情況稱為*延遲*。待處理的延遲觸發也可以使用 `SET
CONSTRAINTS` 強制立即發生。限制條件觸發程序預期在其所實作的限制條件遭到違反時引發例外。

`REFERENCING` 選項可以收集*轉換關聯*（transition relation），也就是包含目前 SQL 陳述式所插入、刪除或修改之所有資料列的資料列集合。這項功能讓觸發程序能看到陳述式所做之事的整體樣貌，而不只是一次一筆資料列。此選項只允許用於一般資料表（而非外部資料表）上的 `AFTER` 觸發程序。該觸發程序不應該是限制條件觸發程序。此外，若觸發程序是 `UPDATE` 觸發程序，則使用此選項時不得指定 *`column_name`* 列表。`OLD TABLE` 只能指定一次，而且只能用於可在 `UPDATE` 或 `DELETE` 時觸發的觸發程序；它會建立一個轉換關聯，其中包含該陳述式所更新或刪除之所有資料列的*前映像*（before-image）。同樣地，`NEW TABLE` 只能指定一次，而且只能用於可在 `UPDATE` 或 `INSERT` 時觸發的觸發程序；它會建立一個轉換關聯，其中包含該陳述式所更新或插入之所有資料列的*後映像*（after-image）。

`SELECT` 不會修改任何資料列，因此您無法建立 `SELECT` 觸發程序。對於看似需要 `SELECT` 觸發程序的問題，規則與檢視表可能可以提供可行的解決方案。

關於觸發程序的更多資訊，請參閱[第 37 章](../../server-programming/triggers/README.md)。

<a id="id-1.9.3.93.7"></a>

## 參數

*`name`*
:   要賦予新觸發程序的名稱。此名稱必須與同一資料表上任何其他觸發程序的名稱不同。名稱不能以綱要限定——觸發程序會繼承其資料表的綱要。對於限制條件觸發程序，這也是使用 `SET CONSTRAINTS` 修改該觸發程序行為時所使用的名稱。

`BEFORE`<br>`AFTER`<br>`INSTEAD OF`
:   決定函式是在事件之前、之後或取代事件而被呼叫。限制條件觸發程序只能指定為 `AFTER`。

*`event`*
:   `INSERT`、`UPDATE`、`DELETE` 或 `TRUNCATE` 其中之一；這指定將觸發該觸發程序的事件。可以使用 `OR` 指定多個事件，但要求轉換關聯時除外。

    對於 `UPDATE` 事件，可以使用以下語法指定欄位列表：

    ```

    UPDATE OF column_name1 [, column_name2 ... ]
    ```

    只有在所列欄位中至少有一個被提及為 `UPDATE` 命令的目標，或所列欄位中有一個是相依於 `UPDATE` 目標欄位的產生欄位時，觸發程序才會觸發。

    `INSTEAD OF UPDATE` 事件不允許欄位列表。要求轉換關聯時，也不能指定欄位列表。

*`table_name`*
:   觸發程序所針對之資料表、檢視表或外部資料表的名稱（可選擇以綱要限定）。

*`referenced_table_name`*
:   限制條件所參照之另一個資料表的名稱（可能以綱要限定）。此選項用於外鍵限制條件，不建議一般使用。這只能為限制條件觸發程序指定。

`DEFERRABLE`<br>`NOT DEFERRABLE`<br>`INITIALLY IMMEDIATE`<br>`INITIALLY DEFERRED`
:   觸發程序的預設時機。這些限制條件選項的詳細資訊請參閱 [CREATE TABLE](sql-createtable.md) 文件。這只能為限制條件觸發程序指定。

`REFERENCING`
:   此關鍵字緊接在一個或兩個關聯名稱的宣告之前，這些關聯名稱提供對觸發陳述式之轉換關聯的存取。

`OLD TABLE`<br>`NEW TABLE`
:   此子句指出後面的關聯名稱是用於前映像轉換關聯，還是後映像轉換關聯。

*`transition_relation_name`*
:   在觸發程序內部用於此轉換關聯的名稱（不加限定）。

`FOR EACH ROW`<br>`FOR EACH STATEMENT`
:   這指定觸發程序函式應該針對受觸發事件影響的每一筆資料列各觸發一次，還是每個 SQL 陳述式只觸發一次。若兩者都未指定，則預設為 `FOR EACH
    STATEMENT`。限制條件觸發程序只能指定為 `FOR EACH ROW`。

*`condition`*
:   決定觸發程序函式是否實際執行的布林運算式。若指定了 `WHEN`，則只有在 *`condition`* 傳回 `true` 時才會呼叫該函式。在 `FOR EACH ROW` 觸發程序中，`WHEN` 條件可以分別藉由撰寫 `OLD.column_name` 或 `NEW.column_name` 來參照舊資料列值或新資料列值的欄位。當然，`INSERT` 觸發程序不能參照 `OLD`，而 `DELETE` 觸發程序不能參照 `NEW`。

    `INSTEAD OF` 觸發程序不支援 `WHEN` 條件。

    目前，`WHEN` 運算式不能包含子查詢。

    請注意，對於限制條件觸發程序，`WHEN` 條件的求值不會延遲，而是在資料列更新操作執行之後立即進行。若條件的求值結果不為真，則觸發程序不會被排入佇列以進行延遲執行。

*`function_name`*
:   使用者提供的函式，宣告為不接受任何引數並傳回型別 `trigger`，會在觸發程序觸發時執行。

    在 `CREATE TRIGGER` 的語法中，關鍵字 `FUNCTION` 與 `PROCEDURE` 是等效的，但無論如何，所參照的函式都必須是函式，而不是程序。此處使用關鍵字 `PROCEDURE` 是歷史因素，且已被棄用。

*`arguments`*
:   一個選擇性的、以逗號分隔的引數列表，會在執行觸發程序時提供給函式。這些引數是字面字串常數。簡單名稱與數值常數也可以寫在這裡，但它們全都會被轉換為字串。請查閱觸發程序函式之實作語言的說明，以了解如何在函式內存取這些引數；其方式可能與一般函式引數不同。

<a id="SQL-CREATETRIGGER-NOTES"></a>

## 注意事項

若要在資料表上建立或取代觸發程序，使用者必須具有該資料表的 `TRIGGER` 權限。使用者也必須具有觸發程序函式的 `EXECUTE` 權限。

使用 [`DROP TRIGGER`](sql-droptrigger.md) 移除觸發程序。

在分割資料表上建立資料列層級觸發程序，會在其每個現有分割區上建立一個相同的「複製」觸發程序；之後建立或附加的任何分割區也都會有相同的觸發程序。若子分割區上已經存在名稱衝突的觸發程序，則會發生錯誤，除非使用 `CREATE OR REPLACE
TRIGGER`，在這種情況下，該觸發程序會被取代為複製觸發程序。當分割區從其上層資料表卸離時，它的複製觸發程序會被移除。

欄位專屬的觸發程序（使用 `UPDATE OF
column_name` 語法定義的觸發程序），會在其任一欄位被列為 `UPDATE` 命令之 `SET` 列表中的目標時觸發。即使觸發程序沒有觸發，欄位的值也可能改變，因為 `BEFORE UPDATE` 觸發程序對資料列內容所做的變更不會被納入考量。反過來說，像 `UPDATE ... SET x = x ...` 這樣的命令會觸發欄位 `x` 上的觸發程序，即使該欄位的值並未改變。

在 `BEFORE` 觸發程序中，`WHEN` 條件會在函式執行（或將要執行）之前一刻求值，因此使用 `WHEN` 與在觸發程序函式開頭測試相同條件並沒有實質上的差別。特別要注意的是，條件所看到的 `NEW` 資料列是目前的值，可能已被先前的觸發程序修改過。此外，`BEFORE` 觸發程序的 `WHEN` 條件不允許檢查 `NEW` 資料列的系統欄位（例如 `ctid`），因為這些欄位尚未被設定。

在 `AFTER` 觸發程序中，`WHEN` 條件會在資料列更新發生之後立即求值，並決定是否要將一個事件排入佇列，以便在陳述式結尾觸發該觸發程序。因此，當 `AFTER` 觸發程序的 `WHEN` 條件未傳回 true 時，就不必將事件排入佇列，也不必在陳述式結尾重新擷取該資料列。若觸發程序只需要針對少數資料列觸發，這可以讓修改許多資料列的陳述式明顯加速。

在某些情況下，單一 SQL 命令可能觸發超過一種的觸發程序。例如，帶有 `ON CONFLICT DO UPDATE` 子句的 `INSERT` 可能同時造成插入與更新操作，因此它會視需要觸發這兩種觸發程序。提供給觸發程序的轉換關聯是其事件類型所專屬的；因此 `INSERT` 觸發程序只會看到被插入的資料列，而 `UPDATE` 觸發程序只會看到被更新的資料列。

由外鍵強制執行動作（例如 `ON UPDATE CASCADE` 或 `ON DELETE SET NULL`）所造成的資料列更新或刪除，會被視為造成它們之 SQL 命令的一部分（請注意，這類動作永遠不會延遲）。受影響資料表上的相關觸發程序會被觸發，因此這提供了另一種 SQL 命令可能觸發與其類型不直接相符之觸發程序的方式。在簡單的情況下，要求轉換關聯的觸發程序，會將單一原始 SQL 命令在其資料表中造成的所有變更視為單一轉換關聯來看待。不過，在某些情況下，存在要求轉換關聯的 `AFTER ROW` 觸發程序，會使單一 SQL 命令所引發的外鍵強制執行動作被拆分成多個步驟，每個步驟都有自己的轉換關聯。在這種情況下，任何存在的陳述式層級觸發程序都會在每建立一組轉換關聯時觸發一次，以確保觸發程序在轉換關聯中看到每一筆受影響的資料列一次且僅一次。

檢視表上的陳述式層級觸發程序，只有在對檢視表的動作是由資料列層級的 `INSTEAD OF` 觸發程序處理時才會觸發。若該動作是由 `INSTEAD` 規則處理，則規則所產生的任何陳述式會取代原本指名該檢視表的陳述式來執行，因此將被觸發的觸發程序是替代陳述式中所指名之資料表上的觸發程序。同樣地，若檢視表可自動更新，則該動作會藉由自動將陳述式改寫為對檢視表之基礎資料表的動作來處理，因此被觸發的是基礎資料表的陳述式層級觸發程序。

修改分割資料表或具有繼承子資料表的資料表時，會觸發附加在明確指名之資料表上的陳述式層級觸發程序，但不會觸發其分割區或子資料表的陳述式層級觸發程序。相對地，資料列層級觸發程序會針對受影響之分割區或子資料表中的資料列觸發，即使查詢中並未明確指名它們。若陳述式層級觸發程序定義了由 `REFERENCING` 子句命名的轉換關聯，則來自所有受影響分割區或子資料表的資料列前映像與後映像都是可見的。在繼承子資料表的情況下，資料列映像只包含觸發程序所附加之資料表中存在的欄位。

目前，具有轉換關聯的資料列層級觸發程序不能定義在分割區或繼承子資料表上。此外，分割資料表上的觸發程序不能是 `INSTEAD OF`。

目前，限制條件觸發程序不支援 `OR REPLACE` 選項。

不建議在已經對觸發程序之資料表執行過更新動作的交易中取代現有的觸發程序。已經做出的觸發決策（或部分觸發決策）不會被重新考量，因此其效果可能出乎意料。

有一些內建的觸發程序函式可以用來解決常見問題，而不必撰寫您自己的觸發程序程式碼；請參閱[第 9.29 節](../../the-sql-language/functions/functions-trigger.md)。

<a id="SQL-CREATETRIGGER-EXAMPLES"></a>

## 範例

每當資料表 `accounts` 的某一筆資料列即將被更新時，執行函式 `check_account_update`：

```

CREATE TRIGGER check_update
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    EXECUTE FUNCTION check_account_update();
```

修改該觸發程序定義，使其只在欄位 `balance` 被指定為 `UPDATE` 命令的目標時才執行函式：

```

CREATE OR REPLACE TRIGGER check_update
    BEFORE UPDATE OF balance ON accounts
    FOR EACH ROW
    EXECUTE FUNCTION check_account_update();
```

這種形式只在欄位 `balance` 的值確實改變時才執行函式：

```

CREATE TRIGGER check_update
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    WHEN (OLD.balance IS DISTINCT FROM NEW.balance)
    EXECUTE FUNCTION check_account_update();
```

呼叫函式來記錄 `accounts` 的更新，但只在有內容改變時才這麼做：

```

CREATE TRIGGER log_update
    AFTER UPDATE ON accounts
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION log_account_update();
```

針對每一筆資料列執行函式 `view_insert_row`，以將資料列插入檢視表底層的資料表中：

```

CREATE TRIGGER view_insert
    INSTEAD OF INSERT ON my_view
    FOR EACH ROW
    EXECUTE FUNCTION view_insert_row();
```

針對每個陳述式執行函式 `check_transfer_balances_to_zero`，以確認 `transfer` 資料列相互抵銷後淨額為零：

```

CREATE TRIGGER transfer_insert
    AFTER INSERT ON transfer
    REFERENCING NEW TABLE AS inserted
    FOR EACH STATEMENT
    EXECUTE FUNCTION check_transfer_balances_to_zero();
```

針對每一筆資料列執行函式 `check_matching_pairs`，以確認成對的項目是同時（由同一個陳述式）進行變更：

```

CREATE TRIGGER paired_items_update
    AFTER UPDATE ON paired_items
    REFERENCING NEW TABLE AS newtab OLD TABLE AS oldtab
    FOR EACH ROW
    EXECUTE FUNCTION check_matching_pairs();
```

[第 37.4 節](../../server-programming/triggers/trigger-example.md)包含一個以 C 撰寫之觸發程序函式的完整範例。

<a id="SQL-CREATETRIGGER-COMPATIBILITY"></a>

## 相容性

PostgreSQL 中的 `CREATE TRIGGER` 陳述式實作了 SQL 標準的一個子集。目前缺少以下功能：

* 雖然 `AFTER` 觸發程序的轉換資料表名稱是以標準方式使用 `REFERENCING` 子句指定，但 `FOR EACH ROW` 觸發程序中使用的資料列變數不能在 `REFERENCING` 子句中指定。它們的取得方式取決於撰寫觸發程序函式所用的語言，但對於任何一種語言而言都是固定的。有些語言實際上的行為就如同有一個包含 `OLD ROW AS OLD NEW ROW AS NEW` 的 `REFERENCING` 子句。
* 標準允許轉換資料表與欄位專屬的 `UPDATE` 觸發程序一起使用，但此時轉換資料表中應該可見的資料列集合取決於觸發程序的欄位列表。PostgreSQL 目前尚未實作這一點。
* PostgreSQL 只允許執行使用者定義的函式作為觸發動作。標準允許執行許多其他 SQL 命令（例如 `CREATE TABLE`）作為觸發動作。這項限制不難繞過，只要建立一個執行所需命令的使用者定義函式即可。

SQL 規定多個觸發程序應該依建立時間的順序觸發。PostgreSQL 則使用名稱順序，這被認為較為方便。

SQL 規定串聯刪除時的 `BEFORE DELETE` 觸發程序要在串聯的 `DELETE` 完成*之後*才觸發。PostgreSQL 的行為則是 `BEFORE
DELETE` 一律在刪除動作之前觸發，即使是串聯的刪除動作也一樣。這被認為較為一致。此外，若 `BEFORE` 觸發程序在由參照動作所造成的更新期間修改資料列或阻止更新，也會出現非標準的行為。這可能導致違反限制條件，或導致儲存的資料不符合參照限制條件。

能夠使用 `OR` 為單一觸發程序指定多個動作，是 PostgreSQL 對 SQL 標準的擴充。

能夠針對 `TRUNCATE` 觸發觸發程序，是 PostgreSQL 對 SQL 標準的擴充，能夠在檢視表上定義陳述式層級觸發程序也是如此。

`CREATE CONSTRAINT TRIGGER` 是 PostgreSQL 對 SQL 標準的擴充。`OR REPLACE` 選項也是如此。

<a id="id-1.9.3.93.11"></a>

## 另請參閱

[ALTER TRIGGER](sql-altertrigger.md), [DROP TRIGGER](sql-droptrigger.md), [CREATE FUNCTION](sql-createfunction.md), [SET CONSTRAINTS](sql-set-constraints.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createtrigger.html)（原文版本：18.6；核對日期：2026-10-03）
