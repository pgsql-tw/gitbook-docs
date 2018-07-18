---
description: 版本：10
---

# 40.5. 規則及權限

由於PostgreSQL 規則系統重寫了查詢，因此可以存取除原始查詢中使用的資料表/檢視表之外的其他資料表/檢視表。使用規則更新時，可以包括對資料表的寫入存取。

重寫規則沒有單獨的擁有者。關連（資料表或檢視表）的擁有者自動成為為其定義的重寫規則的擁有者。PostgreSQL 規則系統改變了預設存取控制系統的行為。根據規則使用的關連將根據規則擁有者的權限進行檢查，而不是呼叫規則的使用者。這意味著使用者只需要在查詢中明確命名的資料表/檢視表所需的權限。

例如：使用者有一個電話號碼列表，其中一些是私人的，其他的是辦公室助理共享的。使用者可以建構以下內容：

```text
CREATE TABLE phone_data (person text, phone text, private boolean);
CREATE VIEW phone_number AS
    SELECT person, CASE WHEN NOT private THEN phone END AS phone
    FROM phone_data;
GRANT SELECT ON phone_number TO assistant;
```

除了該使用者（以及資料庫超級使用者）之外，沒有人可以存取 phone\_data 資料表。 但是由於 GRANT，assistant 可以在 phone\_number 檢視表上執行 SELECT。規則系統將 phone\_number 中的 SELECT 重寫為來自 phone\_data 的 SELECT。由於使用者是phone\_number的所有者，因此是規則的擁有者，而現在根據使用者的權限檢查對 phone\_data 的讀取，並允許查詢。 還執行了存取 phone\_number 的檢查，但這是針對呼叫使用者完成的，因此除了使用者和助理之外，沒有人可以使用它。

按規則檢查權限。 所以助理現在是唯一可以看到公用電話號碼的人。 但助理可以設定另一個檢視表並向公眾授予存取權限。然後，任何人都可以透過助理的檢視表查看 phone\_number 資料。助理不能做的是建立一個直接存取 phone\_data 的檢視表。（實際上助理可以，但是由於在權限檢查期間每次存取都將被拒絕，所以它將無法使用。）一旦使用者注意到助理打開了他們的 phone\_number 檢視表，使用者就可以撤銷助理的存取權限。馬上，對助理檢視表的任何存取都將失敗。

有人可能認為這種逐規則檢查是一個安全漏洞，但實際上並非如此。 但如果它不能以這種方式工作，助理可以設定一個與 phone\_number 具有相同欄位的資料表，並將資料每天複製到那裡一次。然後它是助理自己的資料，助理可以授予他們想要給每個人的存取權限。GRANT 指令意味著「我相信你」。如果你信任的人做了上面的事情，是時候考慮一下然後使用 REVOKE。

請注意，雖然檢視表可用於使用上面顯示的技術隱藏某些欄位內容，但除非已設定 security\_barrier 旗標，否則它們不能可靠地用於隱藏未顯示資料列的資料。 例如，以下檢視表不安全：

```text
CREATE VIEW phone_number AS
    SELECT person, phone FROM phone_data WHERE phone NOT LIKE '412%';
```

此檢視表可能看起來很安全，因為規則系統會將來自 phone\_number 的任何 SELECT 重寫為來自 phone\_data 的 SELECT，並增加僅需要電話不以 412 開頭項目的限定條件。但是，如果使用者可以建立自己的函數，則說服計劃程序在 NOT LIKE 表示式之前執行使用者定義的函數並不困難。 例如：

```text
CREATE FUNCTION tricky(text, text) RETURNS bool AS $$
BEGIN
    RAISE NOTICE '% => %', $1, $2;
    RETURN true;
END
$$ LANGUAGE plpgsql COST 0.0000000000000000000001;

SELECT * FROM phone_number WHERE tricky(person, phone);
```

phone\_data 資料表中的每個人和電話號碼都將以 NOTICE 輸出，因為計劃程序將選擇在更昂貴的 NOT LIKE 之前執行廉價的複雜功能。即使阻止使用者定義新功能，內建功能也可用於類似的攻擊。（例如，大多數強制轉換函數會在它們産生的錯誤訊息中包含它們的輸入值。）

類似的考慮適用於更新規則。在上一節的範例中，範例資料庫中資料表的擁有者可以將 shoelace 檢視表上的 SELECT，INSERT，UPDATE 和 DELETE 權限授予其他人，但僅在 shoelace\_log 上授予 SELECT。寫入日誌項目的規則操作仍將成功執行，其他用戶可以查看日誌項目。 但他們無法建立假項目，也無法變更或刪除現有項目。在這種情況下，不可能通過說服規劃程予改變操作順序來破壞規則，因為引用 shoelace\_log 的唯一規則是不合格的 INSERT。在更複雜的場景中可能不是這樣。

當檢視表需要提供資料列級安全性時，應將 security\_barrier 屬性套用於檢視表。這可以防止惡意的函數和運算子從資料列傳遞值，直到檢視表完成其工作。例如，如果上面顯示的檢視表是這樣建立，那麼它將是安全的：

```text
CREATE VIEW phone_number WITH (security_barrier) AS
    SELECT person, phone FROM phone_data WHERE phone NOT LIKE '412%';
```

使用 security\_barrier 建立的檢視表可能比沒有此選項建立的檢視表更糟糕。通常，沒有辦法避免這種情況：如果可能危及安全性，則必須拒絕最快的計劃。因此，預設情況下不啟用此選項。

在處理沒有副作用的函數時，查詢規劃程序具有更大的靈活性。 這些函數稱為 LEAKPROOF，包括許多簡單的常用運算子，例如許多相等運算子。查詢計劃程序可以安全地允許在查詢執行過程中的任何時候執行此類函數，因為在使用者不可見的資料列上呼叫它們不會洩漏有關不可見資料列的任何信息。此外，不帶參數或未從安全屏障檢視表傳遞任何參數的函數不必標記為 LEAKPROOF 以便向下推，因為它們從不從檢視表接收資料。相反地，根據作為參數接收的值（例如在溢出或除零時拋出錯誤的函數）可能拋出錯誤的函數都不是防漏的，並且可能提供關於不可見資料列的重要信息，如果在安全檢視表的資料列過濾器之前套用。

重要的是要理解即使是使用 security\_barrier 選項建立的檢視圖也只是在有限的意義上是安全的，即不可見 tuple 的內容不會傳遞給可能不安全的函數。使用者可能還有其他方法可以推斷出看不見的資料；例如，他們可以使用 EXPLAIN 查看查詢計劃，或者根據檢視表測量查詢的執行時間。惡意攻擊者可能能夠推斷出有關未見資料量的訊息，甚至可以獲得有關資料分佈或最常見值的一些訊息（因為這些事情可能會影響計劃的執行時間；甚至，因為它們也會被反映出來。在最佳化程序統計中，選擇計劃）。如果關注這些類型的“隱蔽通道（covert channel）”攻擊，則根本不允許對資料進行任何存取。  


