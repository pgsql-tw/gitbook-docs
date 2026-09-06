## J.4. Building the Documentation with Meson [#](#DOCGUIDE-BUILD-MESON)

To build the documentation using Meson, change to the
`build` directory before running one of these commands,
or add `-C build` to the command.

To build just the HTML version of the documentation:

```

build$ ninja html
```

For a list of other documentation targets see
[Section 17.4.4.3](../../server-administration/installation/install-meson.md#TARGETS-MESON-DOCUMENTATION).
The output appears in the
subdirectory `build/doc/src/sgml`.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/docguide-build-meson.html)（英文原文，待翻譯）
