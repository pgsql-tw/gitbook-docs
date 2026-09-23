<a id="REGRESS-TAP"></a>

## 31.4. TAP 測試 [#](#REGRESS-TAP)

[31.4.1. 環境變數](regress-tap.md#REGRESS-TAP-VARS)

各種測試，特別是 `src/bin` 底下的用戶端程式測試，
會使用 Perl TAP 工具，並透過 Perl 測試程式
`prove` 執行。你可以透過設定
`make` 變數 `PROVE_FLAGS`，
將命令列選項傳遞給 `prove`，例如：

```

make -C src/bin check PROVE_FLAGS='--timer'
```

詳情請參閱 `prove` 的操作手冊頁面。

`make` 變數 `PROVE_TESTS`
可用來定義一份以空白分隔的路徑清單，
這些路徑相對於呼叫 `prove` 的
`Makefile`，用來執行指定的測試子集合，
以取代預設的 `t/*.pl`。例如：

```

make check PROVE_TESTS='t/001_test1.pl t/003_test3.pl'
```

TAP 測試需要 Perl 模組 `IPC::Run`。
此模組可從
[CPAN](https://metacpan.org/dist/IPC-Run)
或作業系統套件取得。
另外也需要 PostgreSQL 以
`--enable-tap-tests` 選項進行組態設定。

概略而言，若你執行 `make installcheck`，
TAP 測試會測試先前已安裝之安裝樹中的執行檔；
若你執行 `make check`，
則會從目前的原始碼建置一個新的本機安裝樹。
在這兩種情況下，測試都會初始化一個本機執行個體
（資料目錄），並在其中暫時執行一個伺服器。
其中部分測試會執行不只一個伺服器。因此，
這些測試可能相當耗費資源。

有一點很重要，你必須了解：即使你執行
`make installcheck`，TAP 測試仍會啟動測試伺服器；
這與傳統的非 TAP 測試架構不同——
在該情況下，傳統架構預期會使用一個已在執行中的測試伺服器。
部分 PostgreSQL 子目錄同時含有傳統風格與
TAP 風格的測試，這代表
`make installcheck` 會產生一組
混合了暫時性伺服器與已在執行中的測試伺服器的結果。

<a id="REGRESS-TAP-VARS"></a>

### 31.4.1. 環境變數 [#](#REGRESS-TAP-VARS)

資料目錄會依測試檔名命名，若測試失敗，
就會被保留下來。若設定了環境變數
`PG_TEST_NOCLEAN`，則無論測試狀態為何，
資料目錄都會被保留。舉例來說，
若要在執行 pg_dump 測試時，
無論測試結果為何都保留資料目錄：

```

PG_TEST_NOCLEAN=1 make -C src/bin/pg_dump check
```

此環境變數也會防止測試的暫存目錄被移除。

測試套組中的許多操作，使用 180 秒的逾時限制，
在速度較慢的主機上，可能因負載而導致逾時。
將環境變數 `PG_TEST_TIMEOUT_DEFAULT`
設為較高的數值，就能變更此預設值，以避免此問題。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/regress-tap.html)（原文版本：18.6；核對日期：2026-09-22）
