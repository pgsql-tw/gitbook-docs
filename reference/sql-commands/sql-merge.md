<a id="id-1.9.3.156.1"></a>

## MERGE

MERGE — 依條件插入、更新或刪除資料表中的資料列

## 語法

```

[ WITH with_query [, ...] ]
MERGE INTO [ ONLY ] target_table_name [ * ] [ [ AS ] target_alias ]
    USING data_source ON join_condition
    when_clause [...]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]

where data_source is:

    { [ ONLY ] source_table_name [ * ] | ( source_query ) } [ [ AS ] source_alias ]

and when_clause is:

    { WHEN MATCHED [ AND condition ] THEN { merge_update | merge_delete | DO NOTHING } |
      WHEN NOT MATCHED BY SOURCE [ AND condition ] THEN { merge_update | merge_delete | DO NOTHING } |
      WHEN NOT MATCHED [ BY TARGET ] [ AND condition ] THEN { merge_insert | DO NOTHING } }

and merge_insert is:

    INSERT [( column_name [, ...] )]
        [ OVERRIDING { SYSTEM | USER } VALUE ]
        { VALUES ( { expression | DEFAULT } [, ...] ) | DEFAULT VALUES }

and merge_update is:

    UPDATE SET { column_name = { expression | DEFAULT } |
                 ( column_name [, ...] ) = [ ROW ] ( { expression | DEFAULT } [, ...] ) |
                 ( column_name [, ...] ) = ( sub-SELECT )
               } [, ...]

and merge_delete is:

    DELETE
```

<a id="id-1.9.3.156.5"></a>

## 說明

`MERGE` 會使用 *`data_source`*，對以 *`target_table_name`* 指名的目標資料表中的資料列，執行修改動作。`MERGE` 提供了單一的 SQL 陳述式，就能依條件執行 `INSERT`、`UPDATE` 或 `DELETE`，這項工作若不這麼做，就需要多道程序性語言陳述式才能完成。

`MERGE` 指令首先會將 *`data_source`* 與目標資料表進行連接（join），產生零筆或多筆候選變更資料列。對每一筆候選變更資料列，只會設定一次 `MATCHED`、`NOT MATCHED BY SOURCE` 或 `NOT MATCHED [BY TARGET]` 狀態，之後再依指定順序求值各個 `WHEN` 子句。對每一筆候選變更資料列，會執行第一個求值為 true 的子句。針對任一候選變更資料列，最多只會執行一個 `WHEN` 子句。

`MERGE` 的動作，效果與同名的一般 `UPDATE`、`INSERT` 或 `DELETE` 指令相同。不過這些指令的語法有所不同，特別是沒有 `WHERE` 子句，也不需指定資料表名稱。所有動作都是針對目標資料表而言，不過也可以透過觸發程序對其他資料表進行修改。

指定 `DO NOTHING` 時，來源資料列會被略過。由於各項動作是依指定順序求值的，`DO NOTHING` 可以方便地用來在進行更精細的處理之前，先略過不感興趣的來源資料列。

選用的 `RETURNING` 子句，會讓 `MERGE` 根據每一筆被插入、更新或刪除的資料列，計算並傳回值。可以計算任何使用來源或目標資料表欄位的運算式，或是使用 [`merge_action()`](../../the-sql-language/functions/functions-merge-support.md#MERGE-ACTION) 函式。依預設，執行 `INSERT` 或 `UPDATE` 動作時，會使用目標資料表欄位的新值；執行 `DELETE` 時，則會使用目標資料表欄位的舊值；不過也可以明確要求傳回新舊值。`RETURNING` 清單的語法與 `SELECT` 的輸出清單語法相同。

`MERGE` 沒有獨立的權限。若你指定了更新動作，你必須對 `SET` 子句中所參照之目標資料表的欄位擁有 `UPDATE` 權限。若你指定了插入動作，你必須對目標資料表擁有 `INSERT` 權限。若你指定了刪除動作，你必須對目標資料表擁有 `DELETE` 權限。若你指定了 `DO NOTHING` 動作，你必須至少對目標資料表的一個欄位擁有 `SELECT` 權限。你也需要對任何 `condition`（包括 `join_condition`）或 `expression` 中所參照之 *`data_source`* 及目標資料表的欄位擁有 `SELECT` 權限。權限會在陳述式開始時檢查一次，不論特定的 `WHEN` 子句是否實際執行都會檢查。

若目標資料表是具體化檢視表、外部資料表，或其上定義了任何規則，則不支援使用 `MERGE`。

<a id="id-1.9.3.156.6"></a>

## 參數

*`with_query`*
:   `WITH` 子句可讓你指定一個或多個子查詢，並在 `MERGE` 查詢中以名稱參照它們。詳情請參閱[第 7.8 節](../../the-sql-language/queries/queries-with.md)與 [SELECT](sql-select.md)。請注意，`MERGE` 不支援 `WITH RECURSIVE`。

*`target_table_name`*
:   要合併進去的目標資料表或檢視表名稱（可加上綱要限定）。若在資料表名稱前指定了 `ONLY`，相符的資料列就只會在指名的資料表中被更新或刪除。若未指定 `ONLY`，相符的資料列也會在繼承自該指名資料表的任何資料表中被更新或刪除。你也可以選擇在資料表名稱後加上 `*`，明確表示要包含子資料表。`ONLY` 關鍵字與 `*` 選項不會影響插入動作，插入動作一律只會插入到指名的資料表中。

    若 *`target_table_name`* 是檢視表，它必須是可自動更新、且沒有 `INSTEAD OF` 觸發程序的檢視表，或是必須針對 `WHEN` 子句中指定的每一種動作類型（`INSERT`、`UPDATE` 與 `DELETE`）都具備 `INSTEAD OF` 觸發程序。不支援帶有規則的檢視表。

*`target_alias`*
:   目標資料表的替代名稱。若提供了別名，就會完全隱藏該資料表的實際名稱。舉例來說，若寫成 `MERGE INTO foo AS f`，則 `MERGE` 陳述式其餘的部分都必須以 `f` 而非 `foo` 來參照這個資料表。

*`source_table_name`*
:   來源資料表、檢視表或轉換資料表（transition table）的名稱（可加上綱要限定）。若在資料表名稱前指定了 `ONLY`，就只會納入來自指名資料表中相符的資料列。若未指定 `ONLY`，也會納入來自繼承自該指名資料表之任何資料表中相符的資料列。你也可以選擇在資料表名稱後加上 `*`，明確表示要包含子資料表。

*`source_query`*
:   提供要合併進目標資料表之資料列的查詢（`SELECT` 陳述式或 `VALUES` 陳述式）。語法說明請參閱 [SELECT](sql-select.md) 陳述式或 [VALUES](sql-values.md) 陳述式。

*`source_alias`*
:   資料來源的替代名稱。若提供了別名，就會完全隱藏該資料表的實際名稱，或掩蓋此處使用的其實是一個查詢的事實。

*`join_condition`*
:   *`join_condition`* 是一個求值結果為 `boolean` 型別的運算式（類似 `WHERE` 子句），用來指定 *`data_source`* 中哪些資料列與目標資料表中的資料列相符。

    ### 警告

    *`join_condition`* 中應該只出現用來嘗試比對 *`data_source`* 資料列的目標資料表欄位。只參照目標資料表欄位的 *`join_condition`* 子運算式，可能會以令人意外的方式影響最終採取哪個動作。

    若同時指定了 `WHEN NOT MATCHED BY SOURCE` 與 `WHEN NOT MATCHED [BY TARGET]` 子句，`MERGE` 指令就會在 *`data_source`* 與目標資料表之間執行 `FULL` 連接。為使其能正常運作，*`join_condition`* 的子運算式中，必須至少有一個使用支援雜湊連接（hash join）的運算子，否則所有子運算式都必須使用支援合併連接（merge join）的運算子。

*`when_clause`*
:   至少需要一個 `WHEN` 子句。

    `WHEN` 子句可以指定 `WHEN MATCHED`、`WHEN NOT MATCHED BY SOURCE` 或 `WHEN NOT MATCHED [BY TARGET]`。請注意，SQL 標準只定義了 `WHEN MATCHED` 與 `WHEN NOT MATCHED`（其定義為沒有相符的目標資料列）。`WHEN NOT MATCHED BY SOURCE` 是 SQL 標準的擴充功能，在 `WHEN NOT MATCHED` 後加上 `BY TARGET` 選項、以更明確表達其意義，同樣也是擴充功能。

    若 `WHEN` 子句指定了 `WHEN MATCHED`，且候選變更資料列將 *`data_source`* 中的某資料列與目標資料表中的某資料列相符，則在 *`condition`* 未指定或求值為 `true` 時，就會執行該 `WHEN` 子句。

    若 `WHEN` 子句指定了 `WHEN NOT MATCHED BY SOURCE`，且候選變更資料列代表目標資料表中某筆未與 *`data_source`* 中任何資料列相符的資料列，則在 *`condition`* 未指定或求值為 `true` 時，就會執行該 `WHEN` 子句。

    若 `WHEN` 子句指定了 `WHEN NOT MATCHED [BY TARGET]`，且候選變更資料列代表 *`data_source`* 中某筆未與目標資料表中任何資料列相符的資料列，則在 *`condition`* 未指定或求值為 `true` 時，就會執行該 `WHEN` 子句。

*`condition`*
:   傳回 `boolean` 型別數值的運算式。若某 `WHEN` 子句的此運算式求值為 `true`，就會對該資料列執行該子句的動作。

    `WHEN MATCHED` 子句上的條件，可以參照來源與目標關聯兩者中的欄位。`WHEN NOT MATCHED BY SOURCE` 子句上的條件，則只能參照目標關聯中的欄位，因為依定義並不存在相符的來源資料列。`WHEN NOT MATCHED [BY TARGET]` 子句上的條件，則只能參照來源關聯中的欄位，因為依定義並不存在相符的目標資料列。只能存取目標資料表的系統屬性。

*`merge_insert`*
:   指定一項 `INSERT` 動作，用來將一筆資料列插入目標資料表。目標欄位名稱可以依任意順序列出。若完全未給定欄位名稱清單，預設會採用該資料表宣告順序中的所有欄位。

    任何未出現在明確或隱含欄位清單中的欄位，都會填入預設值，也就是其宣告的預設值；若沒有預設值，則填入 null。

    若目標資料表是分區資料表，每一列資料都會被繞送至適當的分區並插入其中。若目標資料表是某個分區，當任一筆輸入的資料列違反分區限制條件時，就會發生錯誤。

    欄位名稱不得重複指定。`INSERT` 動作不得包含子選取（sub-select）。

    只能指定一個 `VALUES` 子句。`VALUES` 子句只能參照來源關聯中的欄位，因為依定義並不存在相符的目標資料列。

*`merge_update`*
:   指定一項 `UPDATE` 動作，用來更新目標資料表的目前資料列。欄位名稱不得重複指定。

    不允許指定資料表名稱，也不允許 `WHERE` 子句。

*`merge_delete`*
:   指定一項 `DELETE` 動作，用來刪除目標資料表的目前資料列。不要像一般使用 [DELETE](sql-delete.md) 指令那樣包含資料表名稱或任何其他子句。

*`column_name`*
:   目標資料表中某個欄位的名稱。若有需要，欄位名稱可以加上子欄位名稱或陣列下標加以限定。（若只對複合欄位的部分欄位進行插入，其餘欄位會保留為 null。）目標欄位的指定不應包含資料表名稱。

`OVERRIDING SYSTEM VALUE`
:   若沒有此子句，對定義為 `GENERATED ALWAYS` 的識別欄位指定明確的值（`DEFAULT` 除外）會產生錯誤。此子句可解除此限制。

`OVERRIDING USER VALUE`
:   若指定此子句，則為定義為 `GENERATED BY DEFAULT` 的識別欄位所提供的任何數值都會被忽略，並套用預設的序列產生數值。

`DEFAULT VALUES`
:   所有欄位都會填入其預設值。（此形式不允許使用 `OVERRIDING` 子句。）

*`expression`*
:   要指派給該欄位的運算式。若用於 `WHEN MATCHED` 子句，此運算式可以使用來自目標資料表中原始資料列的數值，以及來自 *`data_source`* 資料列的數值。若用於 `WHEN NOT MATCHED BY SOURCE` 子句，此運算式只能使用來自目標資料表中原始資料列的數值。若用於 `WHEN NOT MATCHED [BY TARGET]` 子句，此運算式只能使用來自 *`data_source`* 資料列的數值。

`DEFAULT`
:   將該欄位設為其預設值（若未對該欄位指定特定的預設運算式，則為 `NULL`）。

*`sub-SELECT`*
:   一個 `SELECT` 子查詢，其產生的輸出欄位數目，須與其前方括號中所列的欄位清單數目相同。此子查詢執行時傳回的資料列不得超過一筆。若傳回一筆資料列，其欄位數值會指派給目標欄位；若沒有傳回任何資料列，則會將 NULL 值指派給目標欄位。若用於 `WHEN MATCHED` 子句，此子查詢可以參照來自目標資料表中原始資料列的數值，以及來自 *`data_source`* 資料列的數值。若用於 `WHEN NOT MATCHED BY SOURCE` 子句，此子查詢只能參照來自目標資料表中原始資料列的數值。

*`output_alias`*
:   `RETURNING` 清單中 `OLD` 或 `NEW` 資料列的選用替代名稱。

    依預設，可以撰寫 `OLD.column_name` 或 `OLD.*` 來傳回來自目標資料表的舊數值，也可以撰寫 `NEW.column_name` 或 `NEW.*` 來傳回新數值。若提供了別名，這些名稱就會被隱藏，必須改用該別名來參照新舊資料列。例如 `RETURNING WITH (OLD AS o, NEW AS n) o.*, n.*`。

*`output_expression`*
:   每筆資料列變更（不論是插入、更新或刪除）後，要由 `MERGE` 指令計算並傳回的運算式。此運算式可以使用來源或目標資料表的任何欄位，或使用 [`merge_action()`](../../the-sql-language/functions/functions-merge-support.md#MERGE-ACTION) 函式來傳回關於所執行動作的額外資訊。

    撰寫 `*` 會傳回來源資料表的所有欄位，接著是目標資料表的所有欄位。由於來源與目標資料表通常有許多相同的欄位，這麼做往往會產生大量重複。可以用來源或目標資料表的名稱或別名限定 `*`，來避免這種情況。

    欄位名稱或 `*` 也可以使用 `OLD` 或 `NEW`，或是對應於 `OLD` 或 `NEW` 的 *`output_alias`* 加以限定，以傳回來自目標資料表的舊值或新值。未加限定、來自目標資料表的欄位名稱，或是以目標資料表名稱或別名限定的欄位名稱或 `*`，對於 `INSERT` 與 `UPDATE` 動作會傳回新值，對於 `DELETE` 動作則會傳回舊值。

*`output_name`*
:   用於所傳回欄位的名稱。

<a id="id-1.9.3.156.7"></a>

## 輸出

成功完成後，`MERGE` 指令會傳回下列形式的指令標記：

```

MERGE total_count
```

*`total_count`* 是被變更（不論是插入、更新或刪除）的資料列總數。若 *`total_count`* 為 0，代表沒有任何資料列受到任何形式的變更。

若 `MERGE` 指令包含 `RETURNING` 子句，其結果會類似於一個 `SELECT` 陳述式的結果，其中包含 `RETURNING` 清單所定義的欄位與數值，並根據該指令所插入、更新或刪除的資料列計算而得。

<a id="id-1.9.3.156.8"></a>

## 注意事項

`MERGE` 執行期間會發生下列步驟。

1. 針對所有指定的動作，執行 `BEFORE STATEMENT` 觸發程序，不論其 `WHEN` 子句是否相符。
2. 執行來源與目標資料表的連接。所產生的查詢會以一般方式進行最佳化，並產生一組候選變更資料列。對每一筆候選變更資料列：

   1. 判斷該資料列是 `MATCHED`、`NOT MATCHED BY SOURCE` 還是 `NOT MATCHED [BY TARGET]`。
   2. 依指定順序測試各個 `WHEN` 條件，直到有一個傳回 true 為止。
   3. 當某個條件傳回 true 時，執行下列動作：

      1. 執行該動作事件類型所觸發的任何 `BEFORE ROW` 觸發程序。
      2. 執行指定的動作，並觸發目標資料表上的任何檢查限制條件。
      3. 執行該動作事件類型所觸發的任何 `AFTER ROW` 觸發程序。

      若目標關聯是帶有該動作事件類型之 `INSTEAD OF ROW` 觸發程序的檢視表，則會改用這些觸發程序來執行該動作。
3. 針對所指定的動作，執行任何 `AFTER STATEMENT` 觸發程序，不論這些動作是否實際發生。這與不影響任何資料列的 `UPDATE` 陳述式之行為類似。

總結來說，只要我們*指定*了某種事件類型（例如 `INSERT`）的動作，該事件類型的陳述式觸發程序就會被觸發。相對地，資料列層級的觸發程序只會針對實際*執行*的特定事件類型觸發。因此，即使只觸發了 `UPDATE` 的資料列觸發程序，`MERGE` 指令仍可能同時觸發 `UPDATE` 與 `INSERT` 的陳述式觸發程序。

你應確保這個連接對每一筆目標資料列最多只產生一筆候選變更資料列。換句話說，一筆目標資料列不應該與一筆以上的資料來源資料列相連接。若確實發生這種情況，就只會有其中一筆候選變更資料列被用來修改該目標資料列；之後嘗試修改該資料列的動作則會造成錯誤。若資料列觸發程序對目標資料表做出變更，而這些被修改過的資料列之後又再次被 `MERGE` 修改，同樣也可能發生這種情況。若重複的動作是 `INSERT`，就會造成唯一性違反；若重複的是 `UPDATE` 或 `DELETE`，則會造成基數違反（cardinality violation）；後者的行為是 SQL 標準所要求的。這與 PostgreSQL 過去在 `UPDATE` 與 `DELETE` 陳述式中對連接的行為不同，過去對同一資料列的第二次及後續修改嘗試，只會單純被忽略。

若某個 `WHEN` 子句省略了 `AND` 子句，它就會成為該種類（`MATCHED`、`NOT MATCHED BY SOURCE` 或 `NOT MATCHED [BY TARGET]`）最終可觸及的子句。若之後又為該種類指定了另一個 `WHEN` 子句，該子句就會被證明為不可觸及，因而產生錯誤。若兩種種類皆未指定最終可觸及的子句，則某筆候選變更資料列有可能不會採取任何動作。

依預設，資料來源產生資料列的順序是不確定的。若有需要，可以使用 *`source_query`* 來指定一致的順序，這可能是避免並行交易之間發生死結所需要的。

當 `MERGE` 與其他修改目標資料表的指令並行執行時，適用一般的交易隔離規則；關於各隔離等級下的行為說明，請參閱[第 13.2 節](../../the-sql-language/mvcc/transaction-iso.md)。你也可以考慮改用 `INSERT ... ON CONFLICT` 作為替代陳述式，它提供了在發生並行 `INSERT` 時執行 `UPDATE` 的能力。這兩種陳述式類型之間存在許多差異與限制，並不能互相替換。

<a id="id-1.9.3.156.9"></a>

## 範例

依據新的 `recent_transactions` 對 `customer_accounts` 進行維護。

```

MERGE INTO customer_account ca
USING recent_transactions t
ON t.customer_id = ca.customer_id
WHEN MATCHED THEN
  UPDATE SET balance = balance + transaction_value
WHEN NOT MATCHED THEN
  INSERT (customer_id, balance)
  VALUES (t.customer_id, t.transaction_value);
```

嘗試插入一項新的庫存項目連同其庫存數量。若該項目已存在，則改為更新既有項目的庫存數。不允許庫存為零的項目。傳回所有變更的詳細內容。

```

MERGE INTO wines w
USING wine_stock_changes s
ON s.winename = w.winename
WHEN NOT MATCHED AND s.stock_delta > 0 THEN
  INSERT VALUES(s.winename, s.stock_delta)
WHEN MATCHED AND w.stock + s.stock_delta > 0 THEN
  UPDATE SET stock = w.stock + s.stock_delta
WHEN MATCHED THEN
  DELETE
RETURNING merge_action(), w.winename, old.stock AS old_stock, new.stock AS new_stock;
```

`wine_stock_changes` 資料表，舉例來說，可能是一個最近才載入資料庫的暫存資料表。

根據替換用的酒單，更新 `wines`：對任何新的庫存插入資料列、更新已變更的庫存項目，並刪除任何不在新酒單中的酒款。

```

MERGE INTO wines w
USING new_wine_list s
ON s.winename = w.winename
WHEN NOT MATCHED BY TARGET THEN
  INSERT VALUES(s.winename, s.stock)
WHEN MATCHED AND w.stock != s.stock THEN
  UPDATE SET stock = s.stock
WHEN NOT MATCHED BY SOURCE THEN
  DELETE;
```

<a id="id-1.9.3.156.10"></a>

## 相容性

此指令符合 SQL 標準。

`WITH` 子句、`WHEN NOT MATCHED` 的 `BY SOURCE` 與 `BY TARGET` 限定詞、`DO NOTHING` 動作，以及 `RETURNING` 子句，都是 SQL 標準的擴充功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-merge.html)（原文版本：18.6；核對日期：2026-09-28）
