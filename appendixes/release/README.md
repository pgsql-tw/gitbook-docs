<a id="RELEASE"></a>

## 附錄 E. 版本說明

**目錄**

- [E.1. 18.6 版](release-18-6.md)
  - [E.1.1. 遷移至 18.6 版](release-18-6.md#release-18-6-migration)

  - [E.1.2. 變更內容](release-18-6.md#RELEASE-18-6-CHANGES)

- [E.2. 18.4 版](release-18-4.md)
  - [E.2.1. 遷移至 18.4 版](release-18-4.md#release-18-4-migration)

  - [E.2.2. 變更內容](release-18-4.md#RELEASE-18-4-CHANGES)

- [E.3. 18.3 版](release-18-3.md)
  - [E.3.1. 遷移至 18.3 版](release-18-3.md#release-18-3-migration)

  - [E.3.2. 變更內容](release-18-3.md#RELEASE-18-3-CHANGES)

- [E.4. 18.2 版](release-18-2.md)
  - [E.4.1. 遷移至 18.2 版](release-18-2.md#release-18-2-migration)

  - [E.4.2. 變更內容](release-18-2.md#RELEASE-18-2-CHANGES)

- [E.5. 18.1 版](release-18-1.md)
  - [E.5.1. 遷移至 18.1 版](release-18-1.md#release-18-1-migration)

  - [E.5.2. 變更內容](release-18-1.md#RELEASE-18-1-CHANGES)

- [E.6. 18 版](release-18.md)
  - [E.6.1. 概覽](release-18.md#release-18-highlights)

  - [E.6.2. 遷移至 18 版](release-18.md#RELEASE-18-MIGRATION)

  - [E.6.3. 變更內容](release-18.md#RELEASE-18-CHANGES)

  - [E.6.4. 致謝](release-18.md#RELEASE-18-ACKNOWLEDGEMENTS)

- [E.7. 先前的版本](release-prior.md)

版本說明列出每個 PostgreSQL 版本的重要變更，主要功能與遷移問題列在最前面。版本說明不包含只影響少數使用者的變更，也不包含屬於內部、因此使用者看不到的變更。例如，最佳化器幾乎在每個版本都有改進，但使用者通常只會感受到查詢變快了。

每個版本完整的變更清單，可以查看該版本的 [Git](../sourcerepo/git.md) 記錄取得。[`pgsql-committers`
郵件清單](https://www.postgresql.org/list/pgsql-committers/)也記錄了所有原始碼變更。另外還有一個[網頁介面](https://git.postgresql.org/gitweb/?p=postgresql.git;a=summary)，可以顯示特定檔案的變更。

每個項目旁列出的姓名代表該項目的主要開發者。當然，所有變更都經過社群討論與修補檔審查，因此每個項目其實都是社群共同努力的成果。

<a id="RELEASE-COMMIT-LINKS"></a>

版本說明中的章節標記（§）連結到 [gitweb](https://git.postgresql.org/gitweb/?p=postgresql.git) 頁面，顯示造成該版本說明項目的主要 git 提交訊息與原始碼樹變更。可能還有其他未列出的 git 提交。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/release.html)（原文版本：18.6；核對日期：2026-10-22）
