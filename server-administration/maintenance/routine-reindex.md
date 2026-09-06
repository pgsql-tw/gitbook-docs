## 24.2. Routine Reindexing [#](#ROUTINE-REINDEX)

<a id="id-1.6.11.11.2"></a>

In some situations it is worthwhile to rebuild indexes periodically
with the [REINDEX](../../reference/sql-commands/sql-reindex.md) command or a series of individual
rebuilding steps.

B-tree index pages that have become completely empty are reclaimed for
re-use. However, there is still a possibility
of inefficient use of space: if all but a few index keys on a page have
been deleted, the page remains allocated. Therefore, a usage
pattern in which most, but not all, keys in each range are eventually
deleted will see poor use of space. For such usage patterns,
periodic reindexing is recommended.

The potential for bloat in non-B-tree indexes has not been well
researched. It is a good idea to periodically monitor the index's physical
size when using any non-B-tree index type.

Also, for B-tree indexes, a freshly-constructed index is slightly faster to
access than one that has been updated many times because logically
adjacent pages are usually also physically adjacent in a newly built index.
(This consideration does not apply to non-B-tree indexes.) It
might be worthwhile to reindex periodically just to improve access speed.

[REINDEX](../../reference/sql-commands/sql-reindex.md) can be used safely and easily in all cases.
This command requires an `ACCESS EXCLUSIVE` lock by
default, hence it is often preferable to execute it with its
`CONCURRENTLY` option, which requires only a
`SHARE UPDATE EXCLUSIVE` lock.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/routine-reindex.html)（英文原文，待翻譯）
