## 70.1. Backup Manifest Top-level Object [#](#BACKUP-MANIFEST-TOPLEVEL)

The backup manifest JSON document contains the following keys.

`PostgreSQL-Backup-Manifest-Version`
:   The associated value is an integer. Beginning in
    PostgreSQL `17`,
    it is `2`; in older versions, it is `1`.

`System-Identifier`
:   The database system identifier of the
    PostgreSQL instance where the backup was
    taken. This field is present only when
    `PostgreSQL-Backup-Manifest-Version` is
    `2`.

`Files`
:   The associated value is always a list of objects, each describing one
    file that is present in the backup. No entries are present in this
    list for the WAL files that are needed in order to use the backup,
    or for the backup manifest itself. The structure of each object in the
    list is described in [Section 70.2](backup-manifest-files.md).

`WAL-Ranges`
:   The associated value is always a list of objects, each describing a
    range of WAL records that must be readable from a particular timeline
    in order to make use of the backup. The structure of these objects is
    further described in [Section 70.3](backup-manifest-wal-ranges.md).

`Manifest-Checksum`
:   This key is always present on the last line of the backup manifest file.
    The associated value is a SHA-256 checksum of all the preceding lines.
    We use a fixed checksum method here to make it possible for clients
    to do incremental parsing of the manifest. While a SHA-256 checksum
    is significantly more expensive than a CRC-32C checksum, the manifest
    should normally be small enough that the extra computation won't matter
    very much.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/backup-manifest-toplevel.html)（英文原文，待翻譯）
