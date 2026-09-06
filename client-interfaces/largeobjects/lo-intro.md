## 33.1. Introduction [#](#LO-INTRO)

<a id="id-1.7.4.6.2"></a>

All large objects are stored in a single system table named [`pg_largeobject`](../../internals/catalogs/catalog-pg-largeobject.md).
Each large object also has an entry in the system table [`pg_largeobject_metadata`](../../internals/catalogs/catalog-pg-largeobject-metadata.md).
Large objects can be created, modified, and deleted using a read/write API
that is similar to standard operations on files.

PostgreSQL also supports a storage system called
[“TOAST”](../../internals/storage/storage-toast.md),
which automatically stores values
larger than a single database page into a secondary storage area per table.
This makes the large object facility partially obsolete. One
remaining advantage of the large object facility is that it allows values
up to 4 TB in size, whereas TOASTed fields can be at
most 1 GB. Also, reading and updating portions of a large object can be
done efficiently, while most operations on a TOASTed
field will read or write the whole value as a unit.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/lo-intro.html)（英文原文，待翻譯）
