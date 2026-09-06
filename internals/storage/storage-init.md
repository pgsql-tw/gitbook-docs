## 66.5. The Initialization Fork [#](#STORAGE-INIT)

<a id="id-1.10.18.7.2"></a>

Each unlogged table, and each index on an unlogged table, has an initialization
fork. The initialization fork is an empty table or index of the appropriate
type. When an unlogged table must be reset to empty due to a crash, the
initialization fork is copied over the main fork, and any other forks are
erased (they will be recreated automatically as needed).

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-init.html)（英文原文，待翻譯）
