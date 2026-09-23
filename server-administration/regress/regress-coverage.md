<a id="REGRESS-COVERAGE"></a>

## 31.5. 測試涵蓋率檢驗 [#](#REGRESS-COVERAGE)

[31.5.1. 使用 Autoconf 與 Make 檢驗涵蓋率](regress-coverage.md#REGRESS-COVERAGE-CONFIGURE)

[31.5.2. 使用 Meson 檢驗涵蓋率](regress-coverage.md#REGRESS-COVERAGE-MESON)

PostgreSQL 原始碼可以搭配涵蓋率測試工具進行編譯，
如此一來，就能檢驗程式碼中哪些部分，
有被迴歸測試，或是任何其他與該程式碼一併執行的測試套組所涵蓋。
目前使用 GCC 編譯時支援此功能，
且需要 `gcov` 與 `lcov` 套件。

<a id="REGRESS-COVERAGE-CONFIGURE"></a>

### 31.5.1. 使用 Autoconf 與 Make 檢驗涵蓋率 [#](#REGRESS-COVERAGE-CONFIGURE)

典型的工作流程如下所示：

```

./configure --enable-coverage ... OTHER OPTIONS ...
make
make check # or other test suite
make coverage-html
```

接著，將你的 HTML 瀏覽器指向
`coverage/index.html`。

若你沒有安裝 `lcov`，或偏好文字輸出
而非 HTML 報告，可以執行

```

make coverage
```

來取代 `make coverage-html`，
這會為每個與測試相關的原始檔，
產生 `.gcov` 輸出檔案。
（`make coverage` 與 `make
coverage-html` 會彼此覆寫對方的檔案，
因此混用兩者可能會造成混淆。）

你可以在產生涵蓋率報告之前，執行多個不同的測試；
執行次數計數會逐一累加。若你想在
不同的測試執行之間重設執行次數計數，
請執行：

```

make coverage-clean
```

若你只想針對程式碼樹中的一部分產生涵蓋率報告，
可以在某個子目錄中執行 `make coverage-html`
或 `make coverage` 命令。

完成後，請使用 `make distclean` 進行清理。

<a id="REGRESS-COVERAGE-MESON"></a>

### 31.5.2. 使用 Meson 檢驗涵蓋率 [#](#REGRESS-COVERAGE-MESON)

典型的工作流程如下所示：

```

meson setup -Db_coverage=true ... OTHER OPTIONS ... builddir/
meson compile -C builddir/
meson test -C builddir/
cd builddir/
ninja coverage-html
```

接著，將你的 HTML 瀏覽器指向
`./meson-logs/coveragereport/index.html`。

你可以在產生涵蓋率報告之前，執行多個不同的測試；
執行次數計數會逐一累加。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/regress-coverage.html)（原文版本：18.6；核對日期：2026-09-22）
