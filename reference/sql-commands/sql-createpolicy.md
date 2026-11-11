<a id="SQL-CREATEPOLICY"></a><a id="id-1.9.3.75.1"></a>

## CREATE POLICY

CREATE POLICY — 為資料表定義新的資料列層級安全性政策

<a id="id-1.9.3.75.4"></a>

## 語法

```

CREATE POLICY name ON table_name
    [ AS { PERMISSIVE | RESTRICTIVE } ]
    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
    [ TO { role_name | PUBLIC | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( using_expression ) ]
    [ WITH CHECK ( check_expression ) ]
```

<a id="id-1.9.3.75.5"></a>

## 說明

`CREATE POLICY` 命令會為資料表定義新的資料列層級安全性政策。請注意，資料表必須啟用資料列層級安全性（使用 `ALTER TABLE ... ENABLE ROW LEVEL
SECURITY`），所建立的政策才會被套用。

政策會授予選取、插入、更新或刪除符合相關政策運算式之資料列的權限。現有的資料表資料列會依據 `USING` 中指定的運算式進行檢查，而透過 `INSERT` 或 `UPDATE` 將要建立的新資料列，則會依據 `WITH CHECK` 中指定的運算式進行檢查。當 `USING` 運算式對某個資料列傳回 true 時，該資料列對使用者可見；若傳回 false 或 null，則該資料列不可見。通常，資料列不可見時不會發生錯誤，但例外情況請參閱[表 300](sql-createpolicy/policy-by-command.md#sql-createpolicy-summary)。當 `WITH CHECK` 運算式對某個資料列傳回 true 時，該資料列就會被插入或更新；若傳回 false 或 null，則會發生錯誤。

對於 `INSERT`、`UPDATE` 與 `MERGE` 陳述式，`WITH CHECK` 運算式會在 `BEFORE` 觸發程序觸發之後、實際修改任何資料之前執行檢查。因此，`BEFORE ROW` 觸發程序可能會修改要插入的資料，進而影響安全性政策檢查的結果。`WITH CHECK` 運算式會在任何其他限制條件之前執行檢查。

政策名稱是以資料表為單位。因此，同一個政策名稱可以用於許多不同的資料表，並在每個資料表上各自具有適合該資料表的定義。

政策可以套用於特定命令或特定角色。除非另有指定，新建立的政策預設會套用於所有命令與角色。單一命令可能會套用多個政策；詳情請見下文。[表 300](sql-createpolicy/policy-by-command.md#sql-createpolicy-summary) 彙整了不同類型的政策如何套用於特定命令。

對於可以同時具有 `USING` 與 `WITH CHECK` 運算式的政策（`ALL` 與 `UPDATE`），若未定義 `WITH CHECK` 運算式，則 `USING` 運算式會同時用來判斷哪些資料列可見（一般的 `USING` 情況），以及允許加入哪些新資料列（`WITH CHECK` 情況）。

若資料表啟用了資料列層級安全性，但不存在任何適用的政策，則會假定採用「預設拒絕」政策，因此沒有任何資料列可見或可更新。

<a id="id-1.9.3.75.6"></a>

## 參數

*`name`*
:   要建立的政策名稱。此名稱必須與該資料表上任何其他政策的名稱不同。

*`table_name`*
:   政策所套用之資料表的名稱（可選擇以綱要限定）。

`PERMISSIVE`
:   指定將政策建立為寬鬆政策。適用於某個查詢的所有寬鬆政策，會使用布林「OR」運算子組合在一起。透過建立寬鬆政策，管理員可以擴大可存取的紀錄集合。政策預設為寬鬆政策。

`RESTRICTIVE`

指定將政策建立為限制性政策。適用於某個查詢的所有限制性政策，會使用布林「AND」運算子組合在一起。透過建立限制性政策，管理員可以縮小可存取的紀錄集合，因為每一筆紀錄都必須通過所有限制性政策。

請注意，必須至少有一個寬鬆政策授予對紀錄的存取權，限制性政策才能有效地用來縮小該存取範圍。若只存在限制性政策，則沒有任何紀錄可以存取。當寬鬆政策與限制性政策同時存在時，只有在至少一個寬鬆政策通過、且所有限制性政策也都通過的情況下，紀錄才可以存取。

*`command`*
:   政策所套用的命令。有效的選項為 `ALL`、`SELECT`、`INSERT`、`UPDATE` 與 `DELETE`。`ALL` 是預設值。關於這些選項如何套用的具體細節，請見下文。

*`role_name`*
:   政策所要套用的角色（一個或多個）。預設值為 `PUBLIC`，會將政策套用到所有角色。

*`using_expression`*
:   任何 SQL 條件運算式（傳回 `boolean`）。此條件運算式不能包含任何彙總函式或視窗函式。若啟用了資料列層級安全性，此運算式會被加入參照該資料表的查詢中。運算式傳回 true 的資料列將會可見。運算式傳回 false 或 null 的任何資料列，對使用者將不可見（在 `SELECT` 中），也無法被修改（在 `UPDATE` 或 `DELETE` 中）。通常，這類資料列會被靜默地略去，不會回報錯誤（但例外情況請參閱[表 300](sql-createpolicy/policy-by-command.md#sql-createpolicy-summary)）。

*`check_expression`*
:   任何 SQL 條件運算式（傳回 `boolean`）。此條件運算式不能包含任何彙總函式或視窗函式。若啟用了資料列層級安全性，此運算式會用於針對該資料表的 `INSERT` 與 `UPDATE` 查詢。只有運算式求值為 true 的資料列才會被允許。對於任何被插入的紀錄，或任何由更新產生的紀錄，若運算式求值為 false 或 null，就會擲出錯誤。請注意，*`check_expression`* 是針對資料列擬議的新內容進行求值，而不是針對原本的內容。

### 各命令的政策

完整內容請見 [各命令的政策](sql-createpolicy/policy-by-command.md#ge-ming-ling-de-zheng-ce)。

<a id="id-1.9.3.75.6.4"></a>

### 多個政策的套用

當不同命令類型的多個政策套用於同一個命令時（例如，`SELECT` 與 `UPDATE` 政策套用於 `UPDATE` 命令），使用者必須同時具有這兩種類型的權限（例如，既有從關聯中選取資料列的權限，也有更新這些資料列的權限）。因此，某一類型政策的運算式，會使用 `AND` 運算子與另一類型政策的運算式組合在一起。

當相同命令類型的多個政策套用於同一個命令時，必須至少有一個 `PERMISSIVE` 政策授予對該關聯的存取權，而且所有 `RESTRICTIVE` 政策都必須通過。因此，所有 `PERMISSIVE` 政策運算式會使用 `OR` 組合，所有 `RESTRICTIVE` 政策運算式會使用 `AND` 組合，而這兩者的結果再使用 `AND` 組合。若沒有任何 `PERMISSIVE` 政策，則拒絕存取。

請注意，為了組合多個政策，`ALL` 政策會被視為與目前正在套用的另一類型政策屬於相同類型。

舉例來說，在同時需要 `SELECT` 與 `UPDATE` 權限的 `UPDATE` 命令中，若每種類型都有多個適用的政策，它們會依下列方式組合：

```

expression from RESTRICTIVE SELECT/ALL policy 1
AND
expression from RESTRICTIVE SELECT/ALL policy 2
AND
...
AND
(
  expression from PERMISSIVE SELECT/ALL policy 1
  OR
  expression from PERMISSIVE SELECT/ALL policy 2
  OR
  ...
)
AND
expression from RESTRICTIVE UPDATE/ALL policy 1
AND
expression from RESTRICTIVE UPDATE/ALL policy 2
AND
...
AND
(
  expression from PERMISSIVE UPDATE/ALL policy 1
  OR
  expression from PERMISSIVE UPDATE/ALL policy 2
  OR
  ...
)
```

<a id="id-1.9.3.75.7"></a>

## 注意事項

你必須是資料表的擁有者，才能為該資料表建立或變更政策。

雖然政策會套用於對資料庫中資料表的明確查詢，但當系統執行內部參照完整性檢查或驗證限制條件時，並不會套用政策。這表示存在一些間接的方式，可以判斷出某個給定的值存在。其中一個例子是嘗試將重複的值插入作為主鍵或具有唯一值限制條件的欄位。若插入失敗，使用者就可以推斷該值已經存在。（此例假設政策允許使用者插入他們不被允許看到的紀錄。）另一個例子是，使用者被允許插入某個資料表，而該資料表參照了另一個原本隱藏的資料表。使用者可以藉由將值插入參照資料表來判斷存在與否，若插入成功，就表示該值存在於被參照的資料表中。要解決這些問題，可以謹慎地設計政策，讓使用者完全無法插入、刪除或更新可能透露出他們原本無法看到之值的紀錄；或者使用產生的值（例如代理鍵）來取代具有外部意義的鍵值。

一般而言，系統會在使用者查詢中出現的條件之前，先強制執行透過安全性政策所施加的篩選條件，以防止受保護的資料意外暴露給可能不可信任的使用者自訂函式。不過，被系統（或系統管理員）標記為 `LEAKPROOF` 的函式與運算子，可能會在政策運算式之前被求值，因為它們被假定為可信任的。

由於政策運算式是直接加入使用者的查詢中，它們會以執行整個查詢之使用者的權限來執行。因此，使用某個政策的使用者必須能夠存取該運算式中參照的任何資料表或函式，否則在嘗試查詢已啟用資料列層級安全性的資料表時，只會收到權限遭拒的錯誤。不過，這並不會改變檢視表的運作方式。如同一般查詢與檢視表，檢視表所參照之資料表的權限檢查與政策，會使用檢視表擁有者的權限以及適用於檢視表擁有者的任何政策，除非該檢視表是使用 `security_invoker` 選項定義的（請參閱 [`CREATE VIEW`](sql-createview.md)）。

`MERGE` 沒有獨立的政策。相反地，執行 `MERGE` 時，會依據所執行的動作，套用為 `SELECT`、`INSERT`、`UPDATE` 與 `DELETE` 定義的政策。

更多討論與實際範例請參閱[第 5.9 節](../../the-sql-language/ddl/ddl-rowsecurity.md)。

<a id="id-1.9.3.75.8"></a>

## 相容性

`CREATE POLICY` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.75.9"></a>

## 另請參閱

[ALTER POLICY](sql-alterpolicy.md), [DROP POLICY](sql-droppolicy.md), [ALTER TABLE](sql-altertable.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createpolicy.html)（原文版本：18.6；核對日期：2026-10-05）
