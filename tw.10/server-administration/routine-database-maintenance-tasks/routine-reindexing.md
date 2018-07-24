# 24.2. Routine Reindexing

In some situations it is worthwhile to rebuild indexes periodically with the [REINDEX](https://www.postgresql.org/docs/current/static/sql-reindex.html) command or a series of individual rebuilding steps.

B-tree index pages that have become completely empty are reclaimed for re-use. However, there is still a possibility of inefficient use of space: if all but a few index keys on a page have been deleted, the page remains allocated. Therefore, a usage pattern in which most, but not all, keys in each range are eventually deleted will see poor use of space. For such usage patterns, periodic reindexing is recommended.

The potential for bloat in non-B-tree indexes has not been well researched. It is a good idea to periodically monitor the index's physical size when using any non-B-tree index type.

Also, for B-tree indexes, a freshly-constructed index is slightly faster to access than one that has been updated many times because logically adjacent pages are usually also physically adjacent in a newly built index. \(This consideration does not apply to non-B-tree indexes.\) It might be worthwhile to reindex periodically just to improve access speed.

[REINDEX](https://www.postgresql.org/docs/current/static/sql-reindex.html) can be used safely and easily in all cases. But since the command requires an exclusive table lock, it is often preferable to execute an index rebuild with a sequence of creation and replacement steps. Index types that support [CREATE INDEX](https://www.postgresql.org/docs/current/static/sql-createindex.html) with the `CONCURRENTLY` option can instead be recreated that way. If that is successful and the resulting index is valid, the original index can then be replaced by the newly built one using a combination of [ALTER INDEX](https://www.postgresql.org/docs/current/static/sql-alterindex.html) and [DROP INDEX](https://www.postgresql.org/docs/current/static/sql-dropindex.html). When an index is used to enforce uniqueness or other constraints, [ALTER TABLE](https://www.postgresql.org/docs/current/static/sql-altertable.html) might be necessary to swap the existing constraint with one enforced by the new index. Review this alternate multistep rebuild approach carefully before using it as there are limitations on which indexes can be reindexed this way, and errors must be handled.

