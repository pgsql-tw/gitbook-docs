<a id="BASIC-ARCHIVE"></a>

# F.6. basic_archive

[F.6.1. Configuration Parameters](#id-1.11.7.15.5)

[F.6.2. Notes](#id-1.11.7.15.6)

[F.6.3. Author](#id-1.11.7.15.7)

<a id="id-1.11.7.15.2"></a>

`basic_archive` is an example of an archive module. This module copies completed WAL segment files to the specified directory. This may not be especially useful, but it can serve as a starting point for developing your own archive module. For more information about archive modules, see [Chapter 51](../../51.-archive-modules.md).

In order to function, this module must be loaded via [archive_library](https://www.postgresql.org/docs/15/runtime-config-wal.html#GUC-ARCHIVE-LIBRARY), and [archive_mode](https://www.postgresql.org/docs/15/runtime-config-wal.html#GUC-ARCHIVE-MODE) must be enabled.

<a id="id-1.11.7.15.5"></a>

## F.6.1. Configuration Parameters

`basic_archive.archive_directory` (`string`) <a id="id-1.11.7.15.5.2.1.1.3"></a>

The directory where the server should copy WAL segment files. This directory must already exist. The default is an empty string, which effectively halts WAL archiving, but if [archive_mode](https://www.postgresql.org/docs/15/runtime-config-wal.html#GUC-ARCHIVE-MODE) is enabled, the server will accumulate WAL segment files in the expectation that a value will soon be provided.

These parameters must be set in `postgresql.conf`. Typical usage might be:

```

# postgresql.conf
archive_mode = 'on'
archive_library = 'basic_archive'
basic_archive.archive_directory = '/path/to/archive/directory'
```

<a id="id-1.11.7.15.6"></a>

## F.6.2. Notes

Server crashes may leave temporary files with the prefix `archtemp` in the archive directory. It is recommended to delete such files before restarting the server after a crash. It is safe to remove such files while the server is running as long as they are unrelated to any archiving still in progress, but users should use extra caution when doing so.

<a id="id-1.11.7.15.7"></a>

## F.6.3. Author

Nathan Bossart

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/basic-archive.html)（英文原文，待翻譯）
