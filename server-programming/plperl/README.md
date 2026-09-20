## 第 43 章 PL/Perl — Perl 程序語言

**目錄**

[43.1. PL/Perl 函式與引數](plperl-funcs.md)

[43.2. PL/Perl 中的資料值](plperl-data.md)

[43.3. 內建函式](plperl-builtins.md)
:   [43.3.1. 從 PL/Perl 存取資料庫](plperl-builtins.md#PLPERL-DATABASE)

    [43.3.2. PL/Perl 中的公用函式](plperl-builtins.md#PLPERL-UTILITY-FUNCTIONS)

[43.4. PL/Perl 中的全域值](plperl-global.md)

[43.5. 受信任與不受信任的 PL/Perl](plperl-trusted.md)

[43.6. PL/Perl 觸發程序](plperl-triggers.md)

[43.7. PL/Perl 事件觸發程序](plperl-event-triggers.md)

[43.8. PL/Perl 的內部運作](plperl-under-the-hood.md)
:   [43.8.1. 組態設定](plperl-under-the-hood.md#PLPERL-CONFIG)

    [43.8.2. 限制與缺少的功能](plperl-under-the-hood.md#PLPERL-MISSING)

<a id="id-1.8.10.2"></a><a id="id-1.8.10.3"></a>

PL/Perl 是一種可載入的程序語言，讓你能夠以 [Perl 程式語言](https://www.perl.org)撰寫 PostgreSQL 函式與程序。

使用 PL/Perl 的主要優點，在於它讓你可以在已儲存的函式與程序中，使用 Perl 所提供的各式各樣「字串處理」運算子與函式。相較於 PL/pgSQL 所提供的字串函式與控制結構，使用 Perl 剖析複雜字串可能會比較容易。

若要在特定資料庫中安裝 PL/Perl，請使用 `CREATE EXTENSION plperl`。

### 提示

如果某個語言已安裝到 `template1` 中，那麼之後所有新建立的資料庫都會自動安裝該語言。

### 注意

使用原始碼套件的使用者，必須在安裝過程中特別啟用 PL/Perl 的建置（更多資訊請參閱[第 17 章](../../server-administration/installation/README.md)）。使用二進位套件的使用者，可能會發現 PL/Perl 位於獨立的子套件中。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl.html)（原文版本：18.6；核對日期：2026-09-15）
