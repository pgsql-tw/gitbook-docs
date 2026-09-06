## O.4. `pg_resetxlog` renamed to `pg_resetwal` [#](#APP-PGRESETXLOG)

<a id="id-1.11.16.6.2"></a>

PostgreSQL 9.6 and below provided a command named
`pg_resetxlog`
<a id="id-1.11.16.6.3.2"></a>
to reset the write-ahead-log (WAL) files. This command was renamed to `pg_resetwal`, see
[pg_resetwal](../../reference/reference-server/app-pgresetwal.md) for documentation of `pg_resetwal` and see
[the release notes for PostgreSQL 10](../release/release-prior.md) for details
on this change.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/app-pgresetxlog.html)（英文原文，待翻譯）
