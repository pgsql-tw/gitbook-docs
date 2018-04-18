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

The role\(s\) to which the policy is to be applied. The default is`PUBLIC`, which will apply the policy to all roles.

`using_expression`

AnySQLconditional expression \(returning`boolean`\). The conditional expression cannot contain any aggregate or window functions. This expression will be added to queries that refer to the table if row level security is enabled. Rows for which the expression returns true will be visible. Any rows for which the expression returns false or null will not be visible to the user \(in a`SELECT`\), and will not be available for modification \(in an`UPDATE`or`DELETE`\). Such rows are silently suppressed; no error is reported.

`check_expression`

AnySQLconditional expression \(returning`boolean`\). The conditional expression cannot contain any aggregate or window functions. This expression will be used in`INSERT`and`UPDATE`queries against the table if row level security is enabled. Only rows for which the expression evaluates to true will be allowed. An error will be thrown if the expression evaluates to false or null for any of the records inserted or any of the records that result from the update. Note that the\_`check_expression`\_is evaluated against the proposed new contents of the row, not the original contents.

### Per-Command Policies

`ALL`

Using`ALL`for a policy means that it will apply to all commands, regardless of the type of command. If an`ALL`policy exists and more specific policies exist, then both the`ALL`policy and the more specific policy \(or policies\) will be applied. Additionally,`ALL`policies will be applied to both the selection side of a query and the modification side, using the`USING`expression for both cases if only a`USING`expression has been defined.

As an example, if an`UPDATE`is issued, then the`ALL`policy will be applicable both to what the`UPDATE`will be able to select as rows to be updated \(applying the`USING`expression\), and to the resulting updated rows, to check if they are permitted to be added to the table \(applying the`WITH CHECK`expression, if defined, and the`USING`expression otherwise\). If an`INSERT`or`UPDATE`command attempts to add rows to the table that do not pass the`ALL`policy's`WITH CHECK`expression, the entire command will be aborted.

`SELECT`

Using`SELECT`for a policy means that it will apply to`SELECT`queries and whenever`SELECT`permissions are required on the relation the policy is defined for. The result is that only those records from the relation that pass the`SELECT`policy will be returned during a`SELECT`query, and that queries that require`SELECT`permissions, such as`UPDATE`, will also only see those records that are allowed by the`SELECT`policy. A`SELECT`policy cannot have a`WITH CHECK`expression, as it only applies in cases where records are being retrieved from the relation.

`INSERT`

Using`INSERT`for a policy means that it will apply to`INSERT`commands. Rows being inserted that do not pass this policy will result in a policy violation error, and the entire`INSERT`command will be aborted. An`INSERT`policy cannot have a`USING`expression, as it only applies in cases where records are being added to the relation.

Note that`INSERT`with`ON CONFLICT DO UPDATE`checks`INSERT`policies'`WITH CHECK`expressions only for rows appended to the relation by the`INSERT`path.

`UPDATE`

Using`UPDATE`for a policy means that it will apply to`UPDATE`,`SELECT FOR UPDATE`and`SELECT FOR SHARE`commands, as well as auxiliary`ON CONFLICT DO UPDATE`clauses of`INSERT`commands. Since`UPDATE`involves pulling an existing record and replacing it with a new modified record,`UPDATE`policies accept both a`USING`expression and a`WITH CHECK`expression. The`USING`expression determines which records the`UPDATE`command will see to operate against, while the`WITH CHECK`expression defines which modified rows are allowed to be stored back into the relation.

Any rows whose updated values do not pass the`WITH CHECK`expression will cause an error, and the entire command will be aborted. If only a`USING`clause is specified, then that clause will be used for both`USING`and`WITH CHECK`cases.

Typically an`UPDATE`command also needs to read data from columns in the relation being updated \(e.g., in a`WHERE`clause or a`RETURNING`clause, or in an expression on the right hand side of the`SET`clause\). In this case,`SELECT`rights are also required on the relation being updated, and the appropriate`SELECT`or`ALL`policies will be applied in addition to the`UPDATE`policies. Thus the user must have access to the row\(s\) being updated through a`SELECT`or`ALL`policy in addition to being granted permission to update the row\(s\) via an`UPDATE`or`ALL`policy.

When an`INSERT`command has an auxiliary`ON CONFLICT DO UPDATE`clause, if the`UPDATE`path is taken, the row to be updated is first checked against the`USING`expressions of any`UPDATE`policies, and then the new updated row is checked against the`WITH CHECK`expressions. Note, however, that unlike a standalone`UPDATE`command, if the existing row does not pass the`USING`expressions, an error will be thrown \(the`UPDATE`path will\_never\_be silently avoided\).

`DELETE`

Using`DELETE`for a policy means that it will apply to`DELETE`commands. Only rows that pass this policy will be seen by a`DELETE`command. There can be rows that are visible through a`SELECT`that are not available for deletion, if they do not pass the`USING`expression for the`DELETE`policy.

In most cases a`DELETE`command also needs to read data from columns in the relation that it is deleting from \(e.g., in a`WHERE`clause or a`RETURNING`clause\). In this case,`SELECT`rights are also required on the relation, and the appropriate`SELECT`or`ALL`policies will be applied in addition to the`DELETE`policies. Thus the user must have access to the row\(s\) being deleted through a`SELECT`or`ALL`policy in addition to being granted permission to delete the row\(s\) via a`DELETE`or`ALL`policy.

A`DELETE`policy cannot have a`WITH CHECK`expression, as it only applies in cases where records are being deleted from the relation, so that there is no new row to check.

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

### Application of Multiple Policies

When multiple policies of different command types apply to the same command \(for example,`SELECT`and`UPDATE`policies applied to an`UPDATE`command\), then the user must have both types of permissions \(for example, permission to select rows from the relation as well as permission to update them\). Thus the expressions for one type of policy are combined with the expressions for the other type of policy using the`AND`operator.

When multiple policies of the same command type apply to the same command, then there must be at least one`PERMISSIVE`policy granting access to the relation, and all of the`RESTRICTIVE`policies must pass. Thus all the`PERMISSIVE`policy expressions are combined using`OR`, all the`RESTRICTIVE`policy expressions are combined using`AND`, and the results are combined using`AND`. If there are no`PERMISSIVE`policies, then access is denied.

Note that, for the purposes of combining multiple policies,`ALL`policies are treated as having the same type as whichever other type of policy is being applied.

For example, in an`UPDATE`command requiring both`SELECT`and`UPDATE`permissions, if there are multiple applicable policies of each type, they will be combined as follows:

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

You must be the owner of a table to create or change policies for it.

While policies will be applied for explicit queries against tables in the database, they are not applied when the system is performing internal referential integrity checks or validating constraints. This means there are indirect ways to determine that a given value exists. An example of this is attempting to insert a duplicate value into a column that is a primary key or has a unique constraint. If the insert fails then the user can infer that the value already exists. \(This example assumes that the user is permitted by policy to insert records which they are not allowed to see.\) Another example is where a user is allowed to insert into a table which references another, otherwise hidden table. Existence can be determined by the user inserting values into the referencing table, where success would indicate that the value exists in the referenced table. These issues can be addressed by carefully crafting policies to prevent users from being able to insert, delete, or update records at all which might possibly indicate a value they are not otherwise able to see, or by using generated values \(e.g., surrogate keys\) instead of keys with external meanings.

Generally, the system will enforce filter conditions imposed using security policies prior to qualifications that appear in user queries, in order to prevent inadvertent exposure of the protected data to user-defined functions which might not be trustworthy. However, functions and operators marked by the system \(or the system administrator\) as`LEAKPROOF`may be evaluated before policy expressions, as they are assumed to be trustworthy.

Since policy expressions are added to the user's query directly, they will be run with the rights of the user running the overall query. Therefore, users who are using a given policy must be able to access any tables or functions referenced in the expression or they will simply receive a permission denied error when attempting to query the table that has row-level security enabled. This does not change how views work, however. As with normal queries and views, permission checks and policies for the tables which are referenced by a view will use the view owner's rights and any policies which apply to the view owner.

Additional discussion and practical examples can be found in [Section 5.7](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/data-definition/57-row-security-policies.md).

## Compatibility

`CREATE POLICY`is a PostgreSQL extension.

## See Also

[ALTER POLICY](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/alter-policy.md), [DROP POLICY](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/drop-policy.md), [ALTER TABLE](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/vi-reference/i-sql-commands/alter-table.md)

## 參考文件

* [PostgreSQL: Documentation: devel: CREATE POLICY](https://www.postgresql.org/docs/devel/static/sql-createpolicy.html)

