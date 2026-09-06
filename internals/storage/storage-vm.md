## 66.4. Visibility Map [#](#STORAGE-VM)

<a id="id-1.10.18.6.2"></a><a id="id-1.10.18.6.3"></a>

Each heap relation has a Visibility Map
(VM) to keep track of which pages contain only tuples that are known to be
visible to all active transactions; it also keeps track of which pages contain
only frozen tuples. It's stored
alongside the main relation data in a separate relation fork, named after the
filenode number of the relation, plus a `_vm` suffix. For example,
if the filenode of a relation is 12345, the VM is stored in a file called
`12345_vm`, in the same directory as the main relation file.
Note that indexes do not have VMs.

The visibility map stores two bits per heap page. The first bit, if set,
indicates that the page is all-visible, or in other words that the page does
not contain any tuples that need to be vacuumed.
This information can also be used
by [*index-only
scans*](../../the-sql-language/indexes/indexes-index-only-scans.md) to answer queries using only the index tuple.
The second bit, if set, means that all tuples on the page have been frozen.
That means that even an anti-wraparound vacuum need not revisit the page.

The map is conservative in the sense that we make sure that whenever a bit is
set, we know the condition is true, but if a bit is not set, it might or
might not be true. Visibility map bits are only set by vacuum, but are
cleared by any data-modifying operations on a page.

The [pg_visibility](../../appendixes/contrib/pgvisibility.md) module can be used to examine the
information stored in the visibility map.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/storage-vm.html)（英文原文，待翻譯）
