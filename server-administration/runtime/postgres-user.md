## 18.1. PostgreSQL 使用者帳號 [#](#POSTGRES-USER)

<a id="id-1.6.5.4.2"></a>

如同任何可由外界存取的伺服器背景程式，建議以獨立的使用者帳號執行 PostgreSQL。此帳號應只擁有伺服器所管理的資料，且不應與其他背景程式共用。（例如，使用 `nobody` 使用者並不恰當。）尤其建議此帳號不要擁有 PostgreSQL 執行檔，以確保遭入侵的伺服器程序無法修改這些執行檔。

預先封裝的 PostgreSQL 版本通常會在安裝套件時自動建立適當的使用者帳號。

若要在系統中新增 Unix 使用者帳號，請找尋 `useradd` 或 `adduser` 命令。常用的使用者名稱是 postgres，本書也都以此名稱為例，但你可以自行選用其他名稱。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/postgres-user.html)（原文版本：18.6；核對日期：2026-09-07）
