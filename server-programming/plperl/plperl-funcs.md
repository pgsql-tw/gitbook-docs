<a id="PLPERL-FUNCS"></a>
## 43.1. PL/Perl 函式與引數 [#](#PLPERL-FUNCS)

若要建立 PL/Perl 語言的函式，請使用標準的
[CREATE FUNCTION](../../reference/sql-commands/sql-createfunction.md)
語法：

```

CREATE FUNCTION funcname (argument-types)
RETURNS return-type
-- function attributes can go here
AS $$
    # PL/Perl function body goes here
$$ LANGUAGE plperl;
```

函式的主體是一般的 Perl 程式碼。事實上，PL/Perl 的
膠合程式碼會將它包裝在一個 Perl 子常式中。PL/Perl 函式
是在純量情境（scalar context）下呼叫的，因此無法傳回串列。您可以透過傳回參照的方式，
傳回非純量的值（陣列、記錄與集合），詳情將於下文討論。

在 PL/Perl 程序（procedure）中，Perl 程式碼傳回的任何值都會被忽略。

PL/Perl 也支援使用
[DO](../../reference/sql-commands/sql-do.md) 陳述式呼叫的匿名程式碼區塊：

```

DO $$
    # PL/Perl code
$$ LANGUAGE plperl;
```

匿名程式碼區塊不會接收任何引數，它可能傳回的任何值
也都會被捨棄。除此之外，它的行為就跟函式一樣。

### 注意

在 Perl 中使用具名的巢狀子常式是危險的，尤其是當
它們參照到外圍作用範圍中的詞法變數（lexical variable）時。由於 PL/Perl
函式被包裝在一個子常式中，任何您放在其中的具名子常式都會變成巢狀的。
一般而言，建立匿名子常式，再透過 coderef 呼叫它們，
會安全得多。若要了解更多資訊，請參閱
perldiag 手冊頁中關於
`Variable "%s" will not stay shared` 與
`Variable "%s" is not available` 的條目，或
在網路上搜尋「perl nested named subroutine」。

`CREATE FUNCTION` 指令的語法要求
函式主體必須寫成字串常值。通常
最方便的做法是對字串常值使用錢字符號引用（dollar quoting，請參閱[4.1.2.4 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)）。
若您選擇使用逸出字串語法 `E''`，
則函式主體中使用的任何單引號（`'`）與反斜線
（`\`）都必須加倍
（請參閱[4.1.2.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)）。

引數與結果的處理方式，與任何其他 Perl 子常式相同：
引數是透過 `@_` 傳入的，結果值
則是以 `return` 傳回，或是函式中最後求值的
運算式的值。

舉例來說，一個傳回兩個整數值中較大者的函式，
可以定義如下：

```

CREATE FUNCTION perl_max (integer, integer) RETURNS integer AS $$
    if ($_[0] > $_[1]) { return $_[0]; }
    return $_[1];
$$ LANGUAGE plperl;
```

### 注意

引數會從資料庫的編碼轉換為 UTF-8
以供 PL/Perl 內部使用，並在傳回時再從 UTF-8
轉換回資料庫編碼。

若傳給函式的是一個 SQL null 值<a id="id-1.8.10.9.10.1"></a>，
則該引數值在 Perl 中會顯示為「undefined」（未定義）。上述
函式定義在遇到 null 輸入時，行為並不會很理想
（事實上，它的行為會如同輸入的是零）。我們可以
在函式定義中加入 `STRICT`，讓
PostgreSQL 做出比較合理的處理方式：
若傳入 null 值，該函式將完全不會被呼叫，
而是直接自動傳回 null 結果。另一種做法是，
我們可以在函式主體中檢查未定義的輸入。舉例來說，
假設我們希望 `perl_max` 在其中一個引數為
null、另一個引數為非 null 時，傳回非 null 的那個引數，
而不是傳回 null 值：

```

CREATE FUNCTION perl_max (integer, integer) RETURNS integer AS $$
    my ($x, $y) = @_;
    if (not defined $x) {
        return undef if not defined $y;
        return $y;
    }
    return $x if not defined $y;
    return $x if $x > $y;
    return $y;
$$ LANGUAGE plperl;
```

如上所示，若要從 PL/Perl 函式傳回 SQL null 值，
只要傳回一個未定義的值即可。無論函式是否為
strict，這個做法都可行。

函式引數中任何不是參照的內容都是
字串，其格式為相關資料型別
所使用的標準 PostgreSQL
外部文字表示法。若是一般的數值或文字型別，Perl 會自動
做正確的處理，程式設計人員通常不需要為此操心。不過，在
其他情況下，引數需要先轉換成在 Perl 中
較為可用的形式。舉例來說，`decode_bytea`
函式可用來將 `bytea` 型別的引數
轉換為未逸出的二進位資料。

同樣地，傳回給 PostgreSQL 的值，
也必須符合外部文字表示法格式。舉例來說，
`encode_bytea` 函式可用來
將二進位資料逸出，成為 `bytea` 型別的傳回值。

有一種特別重要的情況，就是布林值。如同前面
所提到的，`bool` 值預設會以文字形式傳遞給 Perl，
也就是 `'t'` 或
`'f'`。這是有問題的，因為 Perl 並不會
把 `'f'` 視為假值！我們可以透過使用一種
「轉換」（transform，請參閱
[CREATE TRANSFORM](../../reference/sql-commands/sql-createtransform.md)）來改善這個狀況。
`bool_plperl` 擴充功能
提供了合適的轉換。若要使用它，請安裝
該擴充功能：

```

CREATE EXTENSION bool_plperl;  -- or bool_plperlu for PL/PerlU
```

接著，針對接受或傳回 `bool` 的
PL/Perl 函式，使用
`TRANSFORM` 函式屬性，例如：

```

CREATE FUNCTION perl_and(bool, bool) RETURNS bool
TRANSFORM FOR TYPE bool
AS $$
  my ($a, $b) = @_;
  return $a && $b;
$$ LANGUAGE plperl;
```

當套用此轉換時，`bool` 引數在 Perl 中
將會顯示為 `1` 或空值，因此可正確對應到
true 或 false。若函式的結果型別為 `bool`，
則會依照 Perl 對傳回值求值的結果為真或假，
來決定其結果為 true 或 false。
在函式內執行 SPI 查詢時，
布林值的查詢引數與結果同樣也會進行類似的轉換
（[43.3.1 節](plperl-builtins.md#PLPERL-DATABASE)）。

Perl 可以將 PostgreSQL 陣列
以 Perl 陣列參照的形式傳回。以下是一個範例：

```

CREATE OR REPLACE function returns_array()
RETURNS text[][] AS $$
    return [['a"b','c,d'],['e\\f','g']];
$$ LANGUAGE plperl;

select returns_array();
```

Perl 會將 PostgreSQL 陣列以一個
經過祝福（blessed）的
`PostgreSQL::InServer::ARRAY` 物件形式傳遞。此物件可被視為陣列
參照或字串，因此能與
PostgreSQL 9.1 以前版本所撰寫的 Perl
程式碼向下相容。舉例來說：

```

CREATE OR REPLACE FUNCTION concat_array_elements(text[]) RETURNS TEXT AS $$
    my $arg = shift;
    my $result = "";
    return undef if (!defined $arg);

    # as an array reference
    for (@$arg) {
        $result .= $_;
    }

    # also works as a string
    $result .= $arg;

    return $result;
$$ LANGUAGE plperl;

SELECT concat_array_elements(ARRAY['PL','/','Perl']);
```

### 注意

多維陣列是以每個 Perl 程式設計人員都熟悉的方式，
表示為指向較低維度陣列參照的參照。

複合型別引數會以雜湊（hash）參照的形式傳遞給函式。
雜湊的鍵就是複合型別的屬性名稱。以下是一個範例：

```

CREATE TABLE employee (
    name text,
    basesalary integer,
    bonus integer
);

CREATE FUNCTION empcomp(employee) RETURNS integer AS $$
    my ($emp) = @_;
    return $emp->{basesalary} + $emp->{bonus};
$$ LANGUAGE plperl;

SELECT name, empcomp(employee.*) FROM employee;
```

PL/Perl 函式可以使用相同的做法傳回複合型別的結果：
傳回一個指向具備所需屬性的雜湊的參照。
舉例來說：

```

CREATE TYPE testrowperl AS (f1 integer, f2 text, f3 text);

CREATE OR REPLACE FUNCTION perl_row() RETURNS testrowperl AS $$
    return {f2 => 'hello', f1 => 1, f3 => 'world'};
$$ LANGUAGE plperl;

SELECT * FROM perl_row();
```

已宣告的結果資料型別中，任何未出現在
該雜湊中的欄位，都會被傳回為 null 值。

同樣地，程序（procedure）的輸出引數，也可以用雜湊
參照的形式傳回：

```

CREATE PROCEDURE perl_triple(INOUT a integer, INOUT b integer) AS $$
    my ($a, $b) = @_;
    return {a => $a * 3, b => $b * 3};
$$ LANGUAGE plperl;

CALL perl_triple(5, 10);
```

PL/Perl 函式也可以傳回純量型別或複合型別的集合。
通常您會想要一次傳回一列，這樣既能加快
啟動時間，也能避免將整個結果集
先排入記憶體佇列。您可以如下所示，
使用 `return_next` 來達成這一點。請注意，
在最後一次 `return_next` 之後，您必須
放上 `return`，或者（更好的做法是）
`return undef`。

```

CREATE OR REPLACE FUNCTION perl_set_int(int)
RETURNS SETOF INTEGER AS $$
    foreach (0..$_[0]) {
        return_next($_);
    }
    return undef;
$$ LANGUAGE plperl;

SELECT * FROM perl_set_int(5);

CREATE OR REPLACE FUNCTION perl_set()
RETURNS SETOF testrowperl AS $$
    return_next({ f1 => 1, f2 => 'Hello', f3 => 'World' });
    return_next({ f1 => 2, f2 => 'Hello', f3 => 'PostgreSQL' });
    return_next({ f1 => 3, f2 => 'Hello', f3 => 'PL/Perl' });
    return undef;
$$ LANGUAGE plperl;
```

對於較小的結果集，您可以傳回一個陣列的參照，
其中包含純量、陣列參照或雜湊參照，
分別對應簡單型別、陣列型別與複合型別。以下是一些
以陣列參照傳回整個結果集的簡單範例：

```

CREATE OR REPLACE FUNCTION perl_set_int(int) RETURNS SETOF INTEGER AS $$
    return [0..$_[0]];
$$ LANGUAGE plperl;

SELECT * FROM perl_set_int(5);

CREATE OR REPLACE FUNCTION perl_set() RETURNS SETOF testrowperl AS $$
    return [
        { f1 => 1, f2 => 'Hello', f3 => 'World' },
        { f1 => 2, f2 => 'Hello', f3 => 'PostgreSQL' },
        { f1 => 3, f2 => 'Hello', f3 => 'PL/Perl' }
    ];
$$ LANGUAGE plperl;

SELECT * FROM perl_set();
```

若您希望在自己的程式碼中使用 `strict` 語用（pragma），
有幾種選擇。若只是暫時性的全域使用，您可以將
`plperl.use_strict` `SET`
為 true。
這會影響往後在目前工作階段中編譯的 PL/Perl
函式，但不會影響目前工作階段中已經編譯過的函式。
若要永久性地全域使用，您可以在
`postgresql.conf` 檔案中，將 `plperl.use_strict`
設為 true。

若要在特定函式中永久使用，您只需要在函式主體
最上方加上：

```

use strict;
```

即可。

若您的 Perl 版本為 5.10.0 或更新版本，`feature` 語用同樣可供 `use` 使用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-funcs.html)（原文版本：18.6；核對日期：2026-09-16）
