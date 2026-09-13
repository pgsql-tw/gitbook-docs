<a id="PLPERL-GLOBAL"></a>

## 43.4. PL/Perl 中的全域值 [#](#PLPERL-GLOBAL)

你可以使用全域 hash（雜湊）`%_SHARED` 來儲存資料（包括程式碼參照），讓資料在目前工作階段的生命週期內於各次函式呼叫之間保留。

以下是一個共享資料的簡單範例：

```

CREATE OR REPLACE FUNCTION set_var(name text, val text) RETURNS text AS $$
    if ($_SHARED{$_[0]} = $_[1]) {
        return 'ok';
    } else {
        return "cannot set shared variable $_[0] to $_[1]";
    }
$$ LANGUAGE plperl;

CREATE OR REPLACE FUNCTION get_var(name text) RETURNS text AS $$
    return $_SHARED{$_[0]};
$$ LANGUAGE plperl;

SELECT set_var('sample', 'Hello, PL/Perl!  How''s tricks?');
SELECT get_var('sample');
```

以下是一個稍微複雜一點、使用程式碼參照的範例：

```

CREATE OR REPLACE FUNCTION myfuncs() RETURNS void AS $$
    $_SHARED{myquote} = sub {
        my $arg = shift;
        $arg =~ s/(['\\])/\\$1/g;
        return "'$arg'";
    };
$$ LANGUAGE plperl;

SELECT myfuncs(); /* initializes the function */

/* Set up a function that uses the quote function */

CREATE OR REPLACE FUNCTION use_quote(TEXT) RETURNS text AS $$
    my $text_to_quote = shift;
    my $qfunc = $_SHARED{myquote};
    return &$qfunc($text_to_quote);
$$ LANGUAGE plperl;
```

（你其實可以把上面的內容換成單行的 `return $_SHARED{myquote}->($_[0]);`，代價是可讀性較差。）

基於安全考量，PL/Perl 會針對每一個 SQL 角色，在各自獨立的 Perl 直譯器中執行由該角色所呼叫的函式。這可以避免某個使用者意外或惡意地干擾另一個使用者的 PL/Perl 函式行為。每個這樣的直譯器都有自己的一份 `%_SHARED` 變數值與其他全域狀態。因此，兩個 PL/Perl 函式若且唯若由同一個 SQL 角色執行時，才會共享相同的 `%_SHARED` 值。在某個應用中，如果單一工作階段會以多個 SQL 角色執行程式碼（透過 `SECURITY DEFINER` 函式、使用 `SET ROLE` 等等），你可能需要採取明確的步驟，以確保 PL/Perl 函式能夠透過 `%_SHARED` 共享資料。要做到這一點，請確認那些應該互相溝通的函式由同一個使用者所擁有，並將它們標記為 `SECURITY DEFINER`。當然，你也必須留意這類函式不能被用來做出任何非預期的事情。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-global.html)（原文版本：18.6；核對日期：2026-09-13）
