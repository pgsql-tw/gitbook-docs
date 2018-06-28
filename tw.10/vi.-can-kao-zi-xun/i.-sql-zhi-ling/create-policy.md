# CREATE POLICY

CREATE POLICY — 為資料表定義新的資料列級的安全原則

## 語法

```text
CREATE POLICY name ON table_name
    [ AS { PERMISSIVE | RESTRICTIVE } ]
    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
    [ TO { role_name | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( using_expression ) ]
    [ WITH CHECK ( check_expression ) ]
```

## 說明

CREATE POLICY 指令用於為資料表定義新的資料列級安全原則。請注意，你必須在資料表上啟用資料列級安全性（使用 ALTER TABLE ... ENABLE ROW LEVEL SECURITY）以便套用所建立的原則。

安全原則會授予 SELECT、INSERT、UPDATE 或 DELETE 與相關安全原則表示式所匹配的資料列的權限。根據 USING 中指定的表示式檢查現有的資料列，同時根據 WITH CHECK 中指定的表示式檢查透過 INSERT 或 UPDATE 建立的新資料列。當 USING 表示式對給定的資料列回傳 true 時，那麼該資料對使用者是可見的，而如果回傳 false 或 null，那麼該資料列為不可見。當 WITH CHECK 表示式對一筆資料列回傳 true 時，則插入或更新該資料列，而如果回傳 false 或 null，則會產生錯誤。

對於 INSERT 和 UPDATE 語句而言，在觸發 BEFORE 觸發器之後，以及在進行任何實際的資料修改之前，WITH CHECK 表示式都會強制執行。因此，BEFORE ROW 觸發器可能會修改要插入的資料，從而影響安全原則檢查的結果。WITH CHECK 表示式會在任何其他限制條件之前執行。

安全原則的名稱是對應每個資料表的。因此，一個原則名稱可用於許多不同的資料表，並為每個資料表定義適合該表格的定義。

安全原則可以應用於特定的指令或特定角色。新建立的安全原則預設適用於所有的指令和角色，除非另有設定。多個原則可能適用於單個命令；請參閱下面的詳細訊息。[Table 240](create-policy.md#table-240-policies-applied-by-command-type) 總結了不同類型的原則如何應用於特定指令。

對於同時具有 USING 和 WITH CHECK 表達式（ALL 和 UPDATE）的安全原則，如果沒有定義 WITH CHECK 表示式，那麼 USING 表示式將用於確定哪些資料列為可見（一般的 USING 情況）以及哪些新資料列將會允許新增（WITH CHECK 情況下）。

如果對資料表啟用資料列級安全性，但卻沒有適用的原則，則會假定「預設拒絕」的原則，不會顯示或更新任何資料列。

## 參數

`name`

要建立的原則名稱。它必須與資料表的任何其他原則的名稱不同。

`table_name`

該原則適用的資料表名稱（可選擇性加上 schema）。

`PERMISSIVE`

指定將原則建立為寬鬆的原則。所有適用查詢的寬鬆原則將使用布林運算的「OR」運算組合在一起。通過建立寬鬆的原則，管理者可以增加可以存取的資料。安全原則預設就是寬容的。

`RESTRICTIVE`

指定將該原則建立為限制性原則。所有適用查詢的限制性原則將使用布林運算「AND」運算組合在一起。透過建立限制性原則，管理者可以減少可以存取的資料集合大小，因為必須為每條資料都會檢核所有限制性策略。

請注意，在限制性原則可用於減少存取權限之前，需要至少有一項允許原則來授予對於資料列的存取權限。如果只有限制性原則存在，則不能存取任何資料列。 如果存在一系列的寬鬆原則和限制性原則，那麼除了所有限制性原則之外，只有在至少有一項寬鬆原則通過的情況下才能得得資料。

`command`

該原則適用的指令。有效的選項是 ALL、SELECT、INSERT、UPDATE 和 DELETE。ALL 是預設值。請參閱下面有關如何應用這些選項的細節。

`role_name`

要適用該原則的角色。預設值是 PUBLIC，它將會把原則適用於所有角色。

`using_expression`

可以是任何的 SQL 條件表示式（回傳布林值）。 條件表示式不能包含任何彙總函數或窗函數。如果啟用了資料列的安全原則，則將此表示式加入到引用該資料表的查詢中。表示式回傳 true 的資料列將會是可見的。表示式回傳 false 或 null 的任何資料列對使用者來說都是不可見的（在 SELECT 中），並且不可用於資料更新（在 UPDATE 或 DELETE 中）。這樣的資料列被無聲地壓制；不會有錯誤的回報。

`check_expression`

為一 SQL 條件表示式（回傳布林值）。 條件表示式不能包含任何彙總函數或窗函數。如果啟用了資料列的安全原則，則將在針對該資料表的 INSERT 和 UPDATE 查詢中使用此表示式。只有表示式認定為 true 的資料列才會被允許操作。如果對於插入的任何資料或由更新產生的任何資料，表示式的計算結果為 false 或 null，則會引發錯誤。請注意，check\_expression 將根據資料列的建議新內容進行評估，而不是原始內容。

### 個別指令安全原則

`ALL`

將 ALL 用於安全原則中意味著它將適用於所有指令，而不管指令的類型如何。如果同時存在 ALL 原則及更具體的原則，則兩個原則都會適用。 此外，如果僅定義了 USING 表示式，則所有原則都將適用於查詢類操作的和更新類操作，對兩種情況均使用 USING 表示式。

舉例來說，當執行 UPDATE 時，ALL 原則將適用於 UPDATE 將能夠選擇作為要更新的資料列（適用 USING 表示式）和更新後的資料列，以檢查它們是否它們允許增加到資料表中（如果定義了 WITH CHECK 表示式，則使用 WITH CHECK 表示式，否則使用 USING 表示式）。如果 INSERT 或 UPDATE 指令嘗試將資料列加入到未通過 ALL 原則的 WITH CHECK 表示式的資料表中，則整個指令將被中止。

`SELECT`

將 SELECT 用於原則意味著它將適用於 SELECT 查詢，所有當定義原則的關連需要 SELECT 權限的時候。結果是只有通過 SELECT 原則的那些資料才會在 SELECT 查詢中回傳，而那些需要 SELECT 權限的查詢（如 UPDATE）也只能看到 SELECT 原則允許的那些資料。SELECT 原則不能有 WITH CHECK 表示式，因為它只適用於從關連中檢索資料的情況。

`INSERT`

在原則中使用 INSERT 意味著它將適用於 INSERT 指令。插入的資料列不通過此原則將導致原則違規錯誤，並且整個 INSERT 指令將被中止。INSERT 原則不能有 USING 表示式，因為它只適用於資料被增加到關連中的情況。

請注意，帶有 ON CONFLICT DO UPDATE 的 INSERT 只對於隨 INSERT 路徑追加到關連的資料列檢查 INSERT 原則的 WITH CHECK 表示式。

`UPDATE`

在安全原則中使用 UPDATE 意味著它將適用於 UPDATE、SELECT FOR UPDATE 和 SELECT FOR SHARE 指令，以及 INSERT 指令的輔助 ON CONFLICT DO UPDATE 子句。由於 UPDATE 涉及取得現有資料並用新的更新資料替換它，所以 UPDATE 原則同時接受 USING 表示式和 WITH CHECK 表示式。USING 表示式定義 UPDATE 命令將查看哪些資料進行操作，而 WITH CHECK 表示式則定義允許哪些修改後的資料儲回關連之中。

任何未通過 WITH CHECK 表示式的資料列都會導致錯誤，並且使得整個命令被中止。如果僅指定 USING 子句，則該子句將同時用於 USING 和 WITH CHECK 兩種情況。

通常，UPDATE 指令還需要從正在更新中的欄位（例如，在 WHERE 子句或 RETURNING 子句中，又或者在 SET 子句的右側的表示式中）讀取資料。在這種情況下，正在更新的關連也需要 SELECT 權限，除 UPDATE 原則外，還將適用適當的 SELECT 或 ALL 原則。因此，除了被授予通過 UPDATE 或 ALL 原則更新資料列的權限之外，用戶還必須能夠存取通過 SELECT 或 ALL 原則更新的資料列。

當 INSERT 指令具有輔助的 ON CONFLICT DO UPDATE 子句時，如果採用 UPDATE 執行路徑，則首先針對任何 UPDATE 原則的 USING 表示式檢查要更新的資料列，然後根據 WITH CHECK 表示式檢查即將更新的資料列。 但是請注意，與獨立的 UPDATE 指令不同，如果現有的資料列未通過 USING 表示式，則會引發錯誤（UPDATE 執行路徑永遠不會被默默地忽視）。

`DELETE`

將 DELETE 用於原則意味著它將適用於 DELETE 命令。只有通過此原則的資料列才會被 DELETE 指令看到。如果不能通過 DELETE 原則的 USING 表達式，但可以透過 SELECT 顯示不能刪除的資料列。

在大多數情況下，DELETE 指令還需要從正在刪除中的關連（例如，在 WHERE 子句或 RETURNING 子句中）的欄位讀取資料。在這種情況下，就還需要 SELECT 權限，所以除了 DELETE 原則外，還將適用適當的 SELECT 或 ALL 策略。因此，除了被授予通過 DELETE 或 ALL 原則刪除資料列的權限外，使用者還必須能夠存取通過 SELECT 或 ALL 原則刪除的資料列。

DELETE 原則不能有 WITH CHECK 表示式，因為它只適用於從關連中刪除資料的情況，所以沒有新的資料需要檢查。

#### **Table 240. Policies Applied by Command Type**

|  | Command | `SELECT/ALL policy` | `INSERT/ALL policy` | `UPDATE/ALL policy` | `DELETE/ALL policy` |
| :--- | :--- | :--- | :--- | :--- | :--- |
|  | `USING expression` | `WITH CHECK expression` | `USING expression` | `WITH CHECK expression` | `USING expression` |
| `SELECT` | Existing row | — | — | — | — |
| `SELECT FOR UPDATE/SHARE` | Existing row | — | Existing row | — | — |
| `INSERT` | — | New row | — | — | — |
| `INSERT ... RETURNING` | New row[\[a\]](https://www.postgresql.org/docs/10/static/sql-createpolicy.html#ftn.RLS-SELECT-PRIV) | New row | — | — | — |
| `UPDATE` | Existing & new rows[\[a\]](https://www.postgresql.org/docs/10/static/sql-createpolicy.html#ftn.RLS-SELECT-PRIV) | — | Existing row | New row | — |
| `DELETE` | Existing row[\[a\]](https://www.postgresql.org/docs/10/static/sql-createpolicy.html#ftn.RLS-SELECT-PRIV) | — | — | — | Existing row |
| `ON CONFLICT DO UPDATE` | Existing & new rows | — | Existing row | New row | — |
|  |  |  |  |  | [\[a\]](https://www.postgresql.org/docs/10/static/sql-createpolicy.html#RLS-SELECT-PRIV)If read access is required to the existing or new row \(for example, a`WHERE`or`RETURNING`clause that refers to columns from the relation\). |

### 多安全原則的套用方式

當不同命令類型的多個原則適用於同一指令（例如，適用於 UPDATE 指令的 SELECT 和 UPDATE 原則）時，使用者必須同時具有這兩種類型指令的權限（例如，從關連中查詢資料列的權限以及允許可以更新它們）。因此將會使用 AND 運算將一種原則類型的表示式與其他類型原則的表示式組合在一起。

當相同指令類型的多個原則套用於同一個指令時，必須至少有一個 PERMISSIVE 原則授予的存取權限，而所有 RESTRICTIVE 原則都必須通過。也就是，所有的 PERMISSIVE 原則表示式均使用 OR 組合，而所有 RESTRICTIVE 原則表示式都使用 AND 進行組合，並使用 AND 組合其結果。 如果沒有 PERMISSIVE 原則，則存取將會被拒絕。

請注意，出於合併多個原則的目的，所有原則都被視為與正在套用的其他任何類型的原則具有相同的類型。

例如，在需要 SELECT 和 UPDATE 權限的 UPDATE 指令中，如果每種類型都有多個適用的原則，則它們將按如下方式組合：

```text
expression from RESTRICTIVE SELECT/ALL policy 1
AND
expression from RESTRICTIVE SELECT/ALL policy 2
AND
...
AND
( expression from PERMISSIVE SELECT/ALL policy 1
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
( expression from PERMISSIVE UPDATE/ALL policy 1
  OR
  expression from PERMISSIVE UPDATE/ALL policy 2
  OR
  ...
)
```

## Notes

您必須是資料表的擁有者才能為其建立或變更安全原則。

雖然安全原則是應用於對資料庫中資料表的查詢，但系統在內部執行參考完整性檢查或驗證限制條件時並不會套用安全原則。這意味著有間接的方法來確認給定的值是否存在。其中的一個例子是嘗試將重複值插入到主鍵或具有唯一值限制的欄位中。如果插入失敗，則使用者可以推斷該值已經存在。（這個例子假定使用者在安全原則下允許插入他們不允許看到的資料。）另一個例子是允許使用者插入資料表，而該表引用了另一個資料表，即使資料表被隱藏了。存在值可以由使用者在引用資料表中插入值來確定，如果成功表示該值存在於引用表中。這些問題可以透過仔細制定安全原則來解決，以防止用戶能夠以插入、刪除或更新所有可能表明他們無法看到的值的資料，或者使用衍生的值（例如代理鍵）而不是具有外在意義的鍵。

通常，為了防止受保護數據無意中暴露給可能不可信的使用者自訂函數，系統將在出現在使用者查詢的資格之前執行使用安全原則施加的過濾條件。但是，系統（或系統管理員）標記為 LEAKPROOF 功能的操作員可以在原則表示式之前進行執行函式，因為它們被認為是可信的。

由於原則表示式是直接加到使用者的查詢中，它們將以執行整個查詢的使用者的權限執行。因此，使用給定原則的使用者必須能夠存取表示式中所引用的任何資料表或函數，否則當嘗試查詢啟用了資料列級安全性的資料表時，它們將會收到拒絕權限的錯誤。然而，這並不會改變 View 的工作方式。與普通查詢和 View 一樣，View 所引用的資料表權限檢查和原則將使用 View 擁有者的權限並套用於視圖擁有者的任何原則。

更多討論和實際案例可以在 [5.7 節](../../ii.-sql-cha-xun-yu-yan/5.-ding-yi-zi-liao-jie-gou/5.7.-zi-liao-lie-an-quan-yuan-ze.md)中瞭解。

## Compatibility

`CREATE POLICY 屬於 PostgreSQL 延伸指令。`

## See Also

[ALTER POLICY](alter-policy.md), [DROP POLICY](drop-policy.md), [ALTER TABLE](alter-table.md)

## 參考文件

* [PostgreSQL: Documentation: devel: CREATE POLICY](https://www.postgresql.org/docs/devel/static/sql-createpolicy.html)

