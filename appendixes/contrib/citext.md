## F.9. citext — 不區分大小寫的字元字串型別 [#](#CITEXT)

[F.9.1. 原理](citext.md#CITEXT-RATIONALE)

[F.9.2. 使用方式](citext.md#CITEXT-HOW-TO-USE-IT)

[F.9.3. 字串比較行為](citext.md#CITEXT-STRING-COMPARISON-BEHAVIOR)

[F.9.4. 限制](citext.md#CITEXT-LIMITATIONS)

[F.9.5. 作者](citext.md#CITEXT-AUTHOR)

<a id="id-1.11.7.19.2"></a>

`citext` 模組提供不區分大小寫的字元字串型別 `citext`。本質上，它在比較值時會於內部呼叫 `lower`；除此之外，其行為幾乎完全與 `text` 相同。

### 提示

請考慮使用*非決定性定序*（請參閱[第 23.2.2.4 節](../../server-administration/charset/collation.md#COLLATION-NONDETERMINISTIC)）取代此模組。它們可用於不區分大小寫的比較、不區分重音符號的比較及其他組合，且能更正確地處理更多 Unicode 特殊情況。

此模組被視為「受信任」，也就是可由在目前資料庫中具有 `CREATE` 權限的非超級使用者安裝。

<a id="CITEXT-RATIONALE"></a>

### F.9.1. 原理 [#](#CITEXT-RATIONALE)

PostgreSQL 中進行不區分大小寫比對的標準方式，是在比較值時使用 `lower` 函式，例如：

```

SELECT * FROM tab WHERE lower(col) = LOWER(?);
```

此方式運作得相當好，但有幾個缺點：

* 它使 SQL 陳述式冗長，且必須永遠記得在欄位和查詢值上都使用 `lower`。
* 除非建立使用 `lower` 的函式索引，否則不會使用索引。
* 若將欄位宣告為 `UNIQUE` 或 `PRIMARY KEY`，隱含建立的索引會區分大小寫。因此它無法用於不區分大小寫的搜尋，也不會以不區分大小寫的方式強制唯一性。

`citext` 資料型別可免除 SQL 查詢中對 `lower` 的呼叫，並讓主鍵不區分大小寫。`citext` 與 `text` 一樣會辨識 locale，這表示大小寫字元的比對取決於資料庫 `LC_CTYPE` 設定的規則。此行為同樣等同於查詢中使用 `lower`；但因為由資料型別透明處理，所以不必記得在查詢中執行任何特殊動作。

<a id="CITEXT-HOW-TO-USE-IT"></a>

### F.9.2. 使用方式 [#](#CITEXT-HOW-TO-USE-IT)

以下是簡單的使用範例：

```

CREATE TABLE users (
    nick CITEXT PRIMARY KEY,
    pass TEXT   NOT NULL
);

INSERT INTO users VALUES ( 'larry',  sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'Tom',    sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'Damian', sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'NEAL',   sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'Bjørn',  sha256(random()::text::bytea) );

SELECT * FROM users WHERE nick = 'Larry';
```

即使 `nick` 欄位設定為 `larry`，而查詢使用 `Larry`，此 `SELECT` 陳述式仍會傳回一個 tuple。

<a id="CITEXT-STRING-COMPARISON-BEHAVIOR"></a>

### F.9.3. 字串比較行為 [#](#CITEXT-STRING-COMPARISON-BEHAVIOR)

`citext` 會先將每個字串轉為小寫（如同呼叫 `lower`），再以一般方式比較結果。因此，若 `lower` 對兩個字串產生相同結果，它們就會被視為相等。

為盡可能模擬不區分大小寫的定序，`citext` 提供多個字串處理運算子和函式的特定版本。例如，套用至 `citext` 時，正規表示式運算子 `~` 與 `~*` 的行為相同：兩者都不區分大小寫地比對。`!~` 與 `!~*`，以及 `LIKE` 運算子 `~~`、`~~*`、`!~~` 與 `!~~*` 也是如此。若要區分大小寫比對，可將運算子的引數轉型為 `text`。

同樣地，若引數為 `citext`，下列函式都會不區分大小寫地比對：

* `regexp_match()`
* `regexp_matches()`
* `regexp_replace()`
* `regexp_split_to_array()`
* `regexp_split_to_table()`
* `replace()`
* `split_part()`
* `strpos()`
* `translate()`

對 regexp 函式而言，若要區分大小寫比對，可指定「c」旗標強制區分大小寫比對。否則，若要區分大小寫行為，必須在使用這些函式前轉型為 `text`。

<a id="CITEXT-LIMITATIONS"></a>

### F.9.4. 限制 [#](#CITEXT-LIMITATIONS)

* `citext` 的大小寫摺疊行為取決於資料庫的 `LC_CTYPE` 設定。因此，比較值的方式會在建立資料庫時決定。依 Unicode 標準定義，它不是真正不區分大小寫。實際上，若你滿意目前定序，應也會滿意 `citext` 的比較；但若資料庫中儲存不同語言的資料，當定序屬於另一種語言時，某一語言的使用者可能發現查詢結果不如預期。
* 自 PostgreSQL 9.1 起，可將 `COLLATE` 規格附加至 `citext` 欄位或資料值。目前，`citext` 運算子比較已進行大小寫摺疊的字串時會遵守非預設 `COLLATE` 規格，但初始的小寫摺疊一律依資料庫的 `LC_CTYPE` 設定執行（也就是如同指定 `COLLATE "default"`）。未來版本可能變更為讓兩個步驟都遵循輸入的 `COLLATE` 規格。
* `citext` 不如 `text` 有效率，因為運算子函式和 B-tree 比較函式必須複製資料並轉為小寫以進行比較。此外，只有 `text` 可支援 B-tree 去重複。不過，`citext` 比使用 `lower` 取得不區分大小寫的比對稍微有效率。
* 若需要在某些情境區分大小寫比較、在其他情境不區分大小寫比較，`citext` 幫助不大。標準做法是使用 `text` 型別，並在需要不區分大小寫比較時手動使用 `lower` 函式；若只偶爾需要不區分大小寫比較，此法運作良好。若大多時候需要不區分大小寫、很少需要區分大小寫，請考慮將資料儲存為 `citext`，並在需要區分大小寫比較時明確將欄位轉型為 `text`。無論哪種情況，若希望兩種搜尋都很快，都需要兩個索引。
* 包含 `citext` 運算子的 schema 必須在目前 `search_path` 中（通常為 `public`）；否則會改為呼叫一般區分大小寫的 `text` 運算子。
* 為比較而將字串轉為小寫的方法無法正確處理某些 Unicode 特殊情況，例如一個大寫字母有兩個等效小寫字母時。Unicode 因此區分*大小寫映射*與*大小寫摺疊*。請使用非決定性定序取代 `citext` 以正確處理此問題。

<a id="CITEXT-AUTHOR"></a>

### F.9.5. 作者 [#](#CITEXT-AUTHOR)

David E. Wheeler `<david@kineticode.com>`

靈感來自 Donald Fraser 的原始 `citext` 模組。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/citext.html)
