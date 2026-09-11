## F.20. isn — 國際標準號碼的資料型別（ISBN、EAN、UPC 等） [#](#ISN)

[F.20.1. 資料型別](isn.md#ISN-DATA-TYPES)

[F.20.2. 型別轉換](isn.md#ISN-CASTS)

[F.20.3. 函式與運算子](isn.md#ISN-FUNCS-OPS)

[F.20.4. 組態參數](isn.md#ISN-CONFIGURATION-PARAMETERS)

[F.20.5. 範例](isn.md#ISN-EXAMPLES)

[F.20.6. 參考資料](isn.md#ISN-BIBLIOGRAPHY)

[F.20.7. 作者](isn.md#ISN-AUTHOR)

<a id="id-1.11.7.30.2"></a>

`isn` 模組為下列國際產品編號標準提供資料型別：EAN13、UPC、ISBN（書籍）、ISMN（音樂）與 ISSN（連續出版品）。輸入時，會依硬式編碼的前綴清單驗證號碼；輸出時也會使用此前綴清單將號碼加上連字號。由於不時會指派新的前綴，前綴清單可能已過時。希望此模組的未來版本能從一個或多個使用者可依需求輕易更新的資料表取得前綴清單；但目前只能修改原始碼並重新編譯以更新清單。或者，此模組未來版本可能移除前綴驗證與連字號支援。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="ISN-DATA-TYPES"></a>

### F.20.1. 資料型別 [#](#ISN-DATA-TYPES)

[表 F.10](isn.md#ISN-DATATYPES) 顯示 `isn` 模組提供的資料型別。

<a id="ISN-DATATYPES"></a>

**表 F.10. `isn` 資料型別**

<table border="1" class="table" summary="isn Data Types"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>資料型別</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">EAN13</code></td><td>
       歐洲商品編碼，一律以 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISBN13</code></td><td>
       國際標準書號，以新的 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISMN13</code></td><td>
       國際標準音樂作品編號，以新的 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISSN13</code></td><td>
       國際標準期刊號，以新的 EAN13 顯示格式顯示
      </td></tr><tr><td><code class="type">ISBN</code></td><td>
       國際標準書號，以舊的簡短顯示格式顯示
      </td></tr><tr><td><code class="type">ISMN</code></td><td>
       國際標準音樂作品編號，以舊的簡短顯示格式顯示
      </td></tr><tr><td><code class="type">ISSN</code></td><td>
       國際標準期刊號，以舊的簡短顯示格式顯示
      </td></tr><tr><td><code class="type">UPC</code></td><td>
       通用產品代碼
      </td></tr></tbody></table>

<br>

注意事項：

1. ISBN13、ISMN13、ISSN13 號碼都是 EAN13 號碼。
2. EAN13 號碼不一定是 ISBN13、ISMN13 或 ISSN13（有些是）。
3. 部分 ISBN13 號碼可顯示為 ISBN。
4. 部分 ISMN13 號碼可顯示為 ISMN。
5. 部分 ISSN13 號碼可顯示為 ISSN。
6. UPC 號碼是 EAN13 號碼的子集（基本上是移除第一個 `0` 數字的 EAN13）。
7. 所有 UPC、ISBN、ISMN 與 ISSN 號碼都可表示為 EAN13 號碼。

在內部，所有這些型別使用相同表示法（64 位元整數），並可相互轉換。提供多種型別是為了控制顯示格式，以及對應該表示某個特定號碼型別的輸入進行更嚴格的有效性檢查。

`ISBN`、`ISMN` 與 `ISSN` 型別會在可能時顯示號碼短版（ISxN 10），而不適用短版的號碼則顯示為 ISxN 13 格式。`EAN13`、`ISBN13`、`ISMN13` 與 `ISSN13` 型別一律顯示 ISxN 的長版（EAN13）。

<a id="ISN-CASTS"></a>

### F.20.2. 型別轉換 [#](#ISN-CASTS)

`isn` 模組提供下列成對的型別轉換：

* ISBN13 <=> EAN13
* ISMN13 <=> EAN13
* ISSN13 <=> EAN13
* ISBN <=> EAN13
* ISMN <=> EAN13
* ISSN <=> EAN13
* UPC <=> EAN13
* ISBN <=> ISBN13
* ISMN <=> ISMN13
* ISSN <=> ISSN13

從 `EAN13` 轉換為另一型別時，執行期間會檢查值是否在另一型別的定義域內；若否，會引發錯誤。其他轉換只是重新標示，必定成功。

<a id="ISN-FUNCS-OPS"></a>

### F.20.3. 函式與運算子 [#](#ISN-FUNCS-OPS)

`isn` 模組提供標準比較運算子，以及所有這些資料型別的 B-tree 與雜湊索引支援。此外，還有數個專用函式，列於[表 F.11](isn.md#ISN-FUNCTIONS)。在此表中，`isn` 表示模組的任何一種資料型別。

<a id="ISN-FUNCTIONS"></a>

**表 F.11. `isn` 函式**

<table border="1" class="table" summary="isn Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.30.7.3.2.2.1.1.1.1"></a>
<code class="function">make_valid</code> ( <code class="type">isn</code> )
        → <code class="returnvalue">isn</code>
</p>
<p>
        清除值的無效檢查碼旗標。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.30.7.3.2.2.2.1.1.1"></a>
<code class="function">is_valid</code> ( <code class="type">isn</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢查是否存在無效檢查碼旗標。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.30.7.3.2.2.3.1.1.1"></a>
<code class="function">isn_weak</code> ( <code class="type">boolean</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        設定弱輸入模式，並傳回新設定。此函式是為了向後相容而保留。建議透過 <code class="varname">isn.weak</code> 組態參數設定弱模式。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">isn_weak</code> ()
        → <code class="returnvalue">boolean</code>
</p>
<p>
        傳回弱模式目前的狀態。此函式是為了向後相容而保留。建議透過 <code class="varname">isn.weak</code> 組態參數檢查弱模式。
       </p></td></tr></tbody></table>

<br>

<a id="ISN-CONFIGURATION-PARAMETERS"></a>

### F.20.4. 組態參數 [#](#ISN-CONFIGURATION-PARAMETERS)

<a id="ISN-CONFIGURATION-PARAMETERS-WEAK"></a>

`isn.weak` (`boolean`) <a id="id-1.11.7.30.8.2.1.1.3"></a> [#](#ISN-CONFIGURATION-PARAMETERS-WEAK)
:   `isn.weak` 啟用弱輸入模式，即使 ISN 輸入值的檢查碼錯誤也可接受。預設值為 `false`，會拒絕無效的檢查碼。

為何要使用弱模式？可能是您有大量 ISBN 號碼，其中有些因不明原因具有錯誤的檢查碼（例如從印刷清單掃描時 OCR 辨識錯誤，或手動擷取號碼時出錯）。您可能想清理這些資料，但仍希望將所有號碼保留在資料庫中，並可能使用外部工具找出資料庫中的無效號碼，以便更容易驗證資訊並確認有效性；例如，您可能想選取資料表中所有無效號碼。

以弱模式將無效號碼插入資料表時，會以修正後的檢查碼插入該號碼，但顯示時會在末端加上驚嘆號（`!`），例如 `0-11-000322-5!`。可使用 `is_valid` 函式檢查此無效標記，並使用 `make_valid` 函式清除它。

即使未啟用弱模式，也可在號碼末端附加 `!` 字元，強制插入標記為無效的號碼。

另一項特殊功能是，輸入時可在檢查碼位置寫入 `?`，系統會自動插入正確的檢查碼。

<a id="ISN-EXAMPLES"></a>

### F.20.5. 範例 [#](#ISN-EXAMPLES)

```

--Using the types directly:
SELECT isbn('978-0-393-04002-9');
SELECT isbn13('0901690546');
SELECT issn('1436-4522');

--Casting types:
-- note that you can only cast from ean13 to another type when the
-- number would be valid in the realm of the target type;
-- thus, the following will NOT work: select isbn(ean13('0220356483481'));
-- but these will:
SELECT upc(ean13('0220356483481'));
SELECT ean13(upc('220356483481'));

--Create a table with a single column to hold ISBN numbers:
CREATE TABLE test (id isbn);
INSERT INTO test VALUES('9780393040029');

--Automatically calculate check digits (observe the '?'):
INSERT INTO test VALUES('220500896?');
INSERT INTO test VALUES('978055215372?');

SELECT issn('3251231?');
SELECT ismn('979047213542?');

--Using the weak mode:
SET isn.weak TO true;
INSERT INTO test VALUES('978-0-11-000533-4');
INSERT INTO test VALUES('9780141219307');
INSERT INTO test VALUES('2-205-00876-X');
SET isn.weak TO false;

SELECT id FROM test WHERE NOT is_valid(id);
UPDATE test SET id = make_valid(id) WHERE id = '2-205-00876-X!';

SELECT * FROM test;

SELECT isbn13(id) FROM test;
```

<a id="ISN-BIBLIOGRAPHY"></a>

### F.20.6. 參考資料 [#](#ISN-BIBLIOGRAPHY)

實作此模組的資訊蒐集自數個網站，包括：

* <https://www.isbn-international.org/>
* <https://www.issn.org/>
* <https://www.ismn-international.org/>
* <https://www.wikipedia.org/>

用於連字號的前綴也彙整自：

* <https://www.gs1.org/standards/id-keys>
* <https://en.wikipedia.org/wiki/List_of_ISBN_registration_groups>
* <https://www.isbn-international.org/content/isbn-users-manual/29>
* <https://en.wikipedia.org/wiki/International_Standard_Music_Number>
* <https://www.ismn-international.org/ranges/tools>

建立演算法時格外謹慎，並依官方 ISBN、ISMN、ISSN 使用者手冊中建議的演算法仔細驗證。

<a id="ISN-AUTHOR"></a>

### F.20.7. 作者 [#](#ISN-AUTHOR)

Germán Méndez Bravo (Kronuz), 2004–2006

此模組受到 Garrett A. Wollman 的 `isbn_issn` 程式碼啟發。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/isn.html)
