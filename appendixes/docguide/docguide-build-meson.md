## J.4. 使用 Meson 建置文件 [#](#DOCGUIDE-BUILD-MESON)

使用 Meson 建置文件時，請先切換至 `build` 目錄再執行以下命令，或在命令中加上 `-C build`。

若只要建置 HTML 版本的文件：

```

build$ ninja html
```

其他文件建置目標的清單，請參閱[第 17.4.4.3 節](../../server-administration/installation/install-meson.md#TARGETS-MESON-DOCUMENTATION)。輸出會位於 `build/doc/src/sgml` 子目錄。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/docguide-build-meson.html)（原文版本：18.6；核對日期：2026-09-07）
