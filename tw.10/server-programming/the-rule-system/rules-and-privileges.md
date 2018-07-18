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

Every person and phone number in the `phone_data` table will be printed as a `NOTICE`, because the planner will choose to execute the inexpensive `tricky` function before the more expensive `NOT LIKE`. Even if the user is prevented from defining new functions, built-in functions can be used in similar attacks. \(For example, most casting functions include their input values in the error messages they produce.\)

Similar considerations apply to update rules. In the examples of the previous section, the owner of the tables in the example database could grant the privileges `SELECT`, `INSERT`, `UPDATE`, and `DELETE` on the `shoelace` view to someone else, but only `SELECT` on `shoelace_log`. The rule action to write log entries will still be executed successfully, and that other user could see the log entries. But they could not create fake entries, nor could they manipulate or remove existing ones. In this case, there is no possibility of subverting the rules by convincing the planner to alter the order of operations, because the only rule which references `shoelace_log` is an unqualified `INSERT`. This might not be true in more complex scenarios.

When it is necessary for a view to provide row level security, the `security_barrier` attribute should be applied to the view. This prevents maliciously-chosen functions and operators from being passed values from rows until after the view has done its work. For example, if the view shown above had been created like this, it would be secure:

```text
CREATE VIEW phone_number WITH (security_barrier) AS
    SELECT person, phone FROM phone_data WHERE phone NOT LIKE '412%';
```

Views created with the `security_barrier` may perform far worse than views created without this option. In general, there is no way to avoid this: the fastest possible plan must be rejected if it may compromise security. For this reason, this option is not enabled by default.

The query planner has more flexibility when dealing with functions that have no side effects. Such functions are referred to as `LEAKPROOF`, and include many simple, commonly used operators, such as many equality operators. The query planner can safely allow such functions to be evaluated at any point in the query execution process, since invoking them on rows invisible to the user will not leak any information about the unseen rows. Further, functions which do not take arguments or which are not passed any arguments from the security barrier view do not have to be marked as `LEAKPROOF` to be pushed down, as they never receive data from the view. In contrast, a function that might throw an error depending on the values received as arguments \(such as one that throws an error in the event of overflow or division by zero\) is not leak-proof, and could provide significant information about the unseen rows if applied before the security view's row filters.

It is important to understand that even a view created with the `security_barrier` option is intended to be secure only in the limited sense that the contents of the invisible tuples will not be passed to possibly-insecure functions. The user may well have other means of making inferences about the unseen data; for example, they can see the query plan using `EXPLAIN`, or measure the run time of queries against the view. A malicious attacker might be able to infer something about the amount of unseen data, or even gain some information about the data distribution or most common values \(since these things may affect the run time of the plan; or even, since they are also reflected in the optimizer statistics, the choice of plan\). If these types of "covert channel" attacks are of concern, it is probably unwise to grant any access to the data at all.  


