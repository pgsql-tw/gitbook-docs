## Chapter 11. Indexes

**Table of Contents**

[11.1. Introduction](indexes-intro.md)

[11.2. Index Types](indexes-types.md)
:   [11.2.1. B-Tree](indexes-types.md#INDEXES-TYPES-BTREE)

    [11.2.2. Hash](indexes-types.md#INDEXES-TYPES-HASH)

    [11.2.3. GiST](indexes-types.md#INDEXES-TYPE-GIST)

    [11.2.4. SP-GiST](indexes-types.md#INDEXES-TYPE-SPGIST)

    [11.2.5. GIN](indexes-types.md#INDEXES-TYPES-GIN)

    [11.2.6. BRIN](indexes-types.md#INDEXES-TYPES-BRIN)

[11.3. Multicolumn Indexes](indexes-multicolumn.md)

[11.4. Indexes and `ORDER BY`](indexes-ordering.md)

[11.5. Combining Multiple Indexes](indexes-bitmap-scans.md)

[11.6. Unique Indexes](indexes-unique.md)

[11.7. Indexes on Expressions](indexes-expressional.md)

[11.8. Partial Indexes](indexes-partial.md)

[11.9. Index-Only Scans and Covering Indexes](indexes-index-only-scans.md)

[11.10. Operator Classes and Operator Families](indexes-opclass.md)

[11.11. Indexes and Collations](indexes-collations.md)

[11.12. Examining Index Usage](indexes-examine.md)

<a id="id-1.5.10.2"></a>

Indexes are a common way to enhance database performance. An index
allows the database server to find and retrieve specific rows much
faster than it could do without an index. But indexes also add
overhead to the database system as a whole, so they should be used
sensibly.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/indexes.html)（英文原文，待翻譯）
