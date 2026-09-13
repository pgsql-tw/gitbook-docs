<a id="PLPERL-TRUSTED"></a>

## 43.5. 受信任與不受信任的 PL/Perl [#](#PLPERL-TRUSTED)

<a id="id-1.8.10.13.2"></a>

一般來說，PL/Perl 會以名為 `plperl` 的「受信任」程式語言安裝。在這樣的設定下，某些 Perl 操作會被停用以維護安全。整體而言，受限制的是那些會與環境互動的操作。這包括檔案處理（file handle）操作、`require` 以及 `use`（用於外部模組）。沒有任何方式可以存取資料庫伺服器程序的內部，也無法以伺服器程序的權限取得作業系統層級的存取能力，而 C 函式則可以做到這些事。因此，任何沒有特權的資料庫使用者都可以被允許使用這個語言。

### 警告

受信任的 PL/Perl 仰賴 Perl 的 `Opcode` 模組來維護安全。Perl 的[文件](https://perldoc.perl.org/Opcode#WARNING)指出，該模組對於受信任 PL/Perl 這種使用情境並不有效。如果你的安全需求無法接受該警告中的不確定性，請考慮執行 `REVOKE USAGE ON LANGUAGE plperl FROM PUBLIC`。

以下是一個因為基於安全理由不允許檔案系統操作而無法運作的函式範例：

```

CREATE FUNCTION badfunc() RETURNS integer AS $$
    my $tmpfile = "/tmp/badfile";
    open my $fh, '>', $tmpfile
        or elog(ERROR, qq{could not open the file "$tmpfile": $!});
    print $fh "Testing writing to a file\n";
    close $fh or elog(ERROR, qq{could not close the file "$tmpfile": $!});
    return 1;
$$ LANGUAGE plperl;
```

這個函式的建立會失敗，因為它使用了被禁止的操作，而這會被驗證器攔截。

有時候我們會希望撰寫不受限制的 Perl 函式。例如，可能會想要一個能寄送郵件的 Perl 函式。為了處理這類情況，PL/Perl 也可以安裝成「不受信任」的語言（通常稱為 PL/PerlU<a id="id-1.8.10.13.6.3"></a>）。在這種情況下，完整的 Perl 語言都可以使用。安裝該語言時，語言名稱 `plperlu` 會選擇不受信任的 PL/Perl 變體。

PL/PerlU 函式的撰寫者必須注意，該函式不能被用來做出任何不樂見的事情，因為它能做到的事情，等同於以資料庫管理者身分登入的使用者所能做的一切。請注意，資料庫系統只允許資料庫超級使用者以不受信任的語言建立函式。

如果上面那個函式是由超級使用者以 `plperlu` 語言建立的，執行就會成功。

同樣地，以 Perl 撰寫的匿名程式碼區塊，若語言指定為 `plperlu` 而非 `plperl`，也可以使用受限制的操作，但呼叫端必須是超級使用者。

### 注意

雖然 PL/Perl 函式會針對每個 SQL 角色在各自獨立的 Perl 直譯器中執行，但在某個給定工作階段中執行的所有 PL/PerlU 函式都在單一個 Perl 直譯器中執行（而它並不是 PL/Perl 函式所使用的任何一個直譯器）。這讓 PL/PerlU 函式可以自由地共享資料，但 PL/Perl 與 PL/PerlU 函式之間無法進行任何溝通。

### 注意

Perl 無法在單一程序中支援多個直譯器，除非它是以適當的旗標建置的，也就是 `usemultiplicity` 或 `useithreads` 其中之一。（除非你真的需要使用執行緒，否則建議採用 `usemultiplicity`。更多細節請參閱 perlembed 線上手冊頁。）如果 PL/Perl 搭配的是並非以這種方式建置的 Perl，那麼每個工作階段就只能有一個 Perl 直譯器，因此任何單一工作階段只能執行 PL/PerlU 函式，或是全部由同一個 SQL 角色呼叫的 PL/Perl 函式。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-trusted.html)（原文版本：18.6；核對日期：2026-09-13）
