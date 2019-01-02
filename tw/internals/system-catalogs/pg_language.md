---
description: 版本：11
---

# 52.29. pg\_language

目錄 pg\_language 註冊了可以撰寫函數或 stored procedure 的語言。有關語言處理程序的更多訊息，請參閱 [CREATE LANGUAGE](../../reference/sql-commands/create-language.md) 和[第 41 章](../../server-programming/the-rule-system/)。

#### **Table 51.29. `pg_language` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `oid` | `oid` |   | 資料列識別指標（隱藏屬性；必須明確選擇） |
| `lanname` | `name` |   | 語言名稱 |
| `lanowner` | `oid` | \`\`[`pg_authid`](pg_authid.md).oid | 語言的所有者 |
| `lanispl` | `bool` |   | 對於內部語言（例如 SQL）而言這是 false 的，對於使用者定義的語言則是 true。目前，pg\_dump 仍然使用它來決定需要轉存哪些語言，但將來可能會被不同的機制所取代。 |
| `lanpltrusted` | `bool` |   | 如果這是一種受信任的語言，則為 True，這意味著它被認為不會授予對正常 SQL 執行環境之外任何內容的存取權限。只有超級使用者才能以不受信任的語言建立函數。 |
| `lanplcallfoid` | `oid` | \`\`[`pg_proc`](pg_proc.md).oid | 對於非內部語言，這引用了語言處理程序，它是一個特殊的函數，負責執行使用特定語言所編寫的所有函數。 |
| `laninline` | `oid` | \`\`[`pg_proc`](pg_proc.md).oid | 這引用了一個負責執行 “inline” 匿名程式區塊（[DO](../../reference/sql-commands/do.md) 區塊）的函數。如果不支援 inline 區塊，則為零。 |
| `lanvalidator` | `oid` | \`\`[`pg_proc`](pg_proc.md).oid | 這引用了一個語言驗證器函數，該函數負責在建立新函數時檢查它們的語法和有效性。如果未提供驗證器，則為零。 |
| `lanacl` | `aclitem[]` |   | 存取權限；有關詳細訊息，請參閱 [GRANT](../../reference/sql-commands/grant.md) 和 [REVOKE](../../reference/sql-commands/revoke.md) |

