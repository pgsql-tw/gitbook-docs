# 52.9. pg\_auth\_members

目錄 pg\_auth\_members 顯示角色之間的成員資格關連。允許任何非循環的關連。

由於角色身份是叢集範圍的，因此 pg\_auth\_members 在叢集的所有資料庫之間共享：每個叢集只有一個 pg\_auth\_members 副本，而不是每個資料庫一個副本。

**Table 51.9. `pg_auth_members` Columns**

| Name | Type | References | Description |
| :--- | :--- | :--- | :--- |
| `roleid` | `oid` | \`\`[`pg_authid`](pg_authid.md).oid | 具有成員的角色 ID |
| `member` | `oid` | [`pg_authid`](pg_authid.md).oid | 作為 roleid 成員的角色 ID |
| `grantor` | `oid` | \`\`[`pg_authid`](pg_authid.md).oid | 授予此成員資格的角色 ID |
| `admin_option` | `bool` |   | 如果成員可以將 roleid 的成員資格授予其他人，則為 True |

