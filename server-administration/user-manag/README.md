## 第 21 章 資料庫角色

**目錄**

[21.1. 資料庫角色](database-roles.md)

[21.2. 角色屬性](role-attributes.md)

[21.3. 角色成員資格](role-membership.md)

[21.4. 移除角色](role-removal.md)

[21.5. 預先定義角色](predefined-roles.md)

[21.6. 函式安全性](perm-functions.md)

PostgreSQL 使用*角色*概念管理資料庫存取權限。角色可依設定視為資料庫使用者或資料庫使用者群組。角色可擁有資料庫物件（例如資料表與函式），並將這些物件的權限授與其他角色，以控制誰可存取哪些物件。此外，可將角色的*成員資格*授與另一角色，讓成員角色使用指派給另一角色的權限。

角色概念涵蓋「使用者」與「群組」概念。在 PostgreSQL 8.1 之前，使用者與群組是不同類型的實體；現在則只有角色。任何角色都可作為使用者、群組或兩者。

本章說明如何建立與管理角色。角色權限對各種資料庫物件的影響，請參閱[第 5.8 節](../../the-sql-language/ddl/ddl-priv.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/user-manag.html)（原文版本：18.6；核對日期：2026-09-11）
