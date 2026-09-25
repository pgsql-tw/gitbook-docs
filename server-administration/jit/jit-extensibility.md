<a id="JIT-EXTENSIBILITY"></a>

## 30.4. 可擴充性 [#](#JIT-EXTENSIBILITY)

[30.4.1. 擴充套件的內嵌支援](jit-extensibility.md#JIT-EXTENSIBILITY-BITCODE)

[30.4.2. 可插拔的 JIT 提供者](jit-extensibility.md#JIT-PLUGGABLE)

<a id="JIT-EXTENSIBILITY-BITCODE"></a>

### 30.4.1. 擴充套件的內嵌支援 [#](#JIT-EXTENSIBILITY-BITCODE)

PostgreSQL 的 JIT
實作可以將型別為 `C` 與 `internal` 的函式本體，
以及基於這類函式的運算子予以內嵌。若要對擴充套件中的函式進行內嵌，
就需要讓這些函式的定義可供取用。當使用 [PGXS](../../server-programming/extend/extend-pgxs.md) 針對已使用 LLVM JIT 支援編譯的伺服器建置擴充套件時，
相關檔案會自動建置並安裝。

相關檔案必須安裝至
`$pkglibdir/bitcode/$extension/`，並將其摘要安裝至
`$pkglibdir/bitcode/$extension.index.bc`，其中
`$pkglibdir` 是
`pg_config --pkglibdir` 所傳回的目錄，`$extension`
則是該擴充套件共享函式庫的基底名稱。

### 注意

對於內建於 PostgreSQL 本身的函式，
其 bitcode 會安裝至
`$pkglibdir/bitcode/postgres`。

<a id="JIT-PLUGGABLE"></a>

### 30.4.2. 可插拔的 JIT 提供者 [#](#JIT-PLUGGABLE)

PostgreSQL 提供一個基於 LLVM 的 JIT
實作。JIT 提供者的介面是可插拔的，該提供者可以在
不重新編譯的情況下更換（雖然目前建置流程僅
提供 LLVM 的內嵌支援資料）。
使用中的提供者是透過設定
[jit_provider](../runtime-config/runtime-config-client.md#GUC-JIT-PROVIDER) 來選擇。

<a id="JIT-PLUGGABLE-PROVIDER-INTERFACE"></a>

#### 30.4.2.1. JIT 提供者介面 [#](#JIT-PLUGGABLE-PROVIDER-INTERFACE)

JIT 提供者是透過動態載入具名的共享函式庫來載入的。系統會使用
一般的函式庫搜尋路徑來尋找該函式庫。若要提供所需的
JIT 提供者回呼函式，並表明該函式庫確實是一個
JIT 提供者，它需要提供一個名為
`_PG_jit_provider_init` 的 C 函式。此函式會被傳入一個
結構，該結構需要填入各項動作對應的回呼函式指標：

```

struct JitProviderCallbacks
{
    JitProviderResetAfterErrorCB reset_after_error;
    JitProviderReleaseContextCB release_context;
    JitProviderCompileExprCB compile_expr;
};

extern void _PG_jit_provider_init(JitProviderCallbacks *cb);
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/jit-extensibility.html)（原文版本：18.6；核對日期：2026-09-24）
