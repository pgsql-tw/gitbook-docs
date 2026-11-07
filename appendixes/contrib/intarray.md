<a id="INTARRAY"></a>

## F.19. intarray — 操作整數陣列 [#](#intarray) <a href="#intarray" id="intarray"></a>

[F.19.1. `intarray` 函式與運算子](intarray/intarray-funcs-ops.md#intarray-funcs-ops)

[F.19.2. 索引支援](intarray.md#intarray-index)

[F.19.3. 範例](intarray.md#intarray-example)

[F.19.4. 效能測試](intarray.md#intarray-benchmark)

[F.19.5. 作者](intarray.md#intarray-authors)

<a id="id-1.11.7.29.2"></a>

`intarray` 模組提供數個實用函式與運算子，用於操作不含 NULL 的整數陣列。部分運算子也支援使用索引進行搜尋。

若提供的陣列含有任何 NULL 元素，所有這些操作都會引發錯誤。

許多操作只對一維陣列有意義。雖然它們接受較多維度的輸入陣列，但資料會依儲存順序視為線性陣列處理。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

### F.19.1. `intarray` 函式與運算子 [#](#intarray-funcs-ops) <a href="#intarray-funcs-ops" id="intarray-funcs-ops"></a>

完整內容請見 [F.19.1. intarray 函式與運算子](intarray/intarray-funcs-ops.md#intarray-funcs-ops)。

<a id="INTARRAY-INDEX"></a>

### F.19.2. 索引支援 [#](#intarray-index) <a href="#intarray-index" id="intarray-index"></a>

`intarray` 為 `&&`、`@>` 與 `@@` 運算子及一般陣列相等比較提供索引支援。

提供兩個參數化 GiST 索引運算子類別：`gist__int_ops`（預設使用）適用於小型至中型資料集，而 `gist__intbig_ops` 使用較大的簽章，較適合為大型資料集（亦即含有大量相異陣列值的欄位）建立索引。實作使用內建有失壓縮的 RD-tree 資料結構。

`gist__int_ops` 會將整數集合近似為整數範圍的陣列。其可選整數參數 `numranges` 決定一個索引鍵中的最大範圍數。`numranges` 預設值為 100。有效值介於 1 至 253 之間。使用較大的陣列作為 GiST 索引鍵可帶來更精確的搜尋（掃描較小比例的索引與較少的堆積頁面），代價是索引較大。

`gist__intbig_ops` 會將整數集合近似為點陣圖簽章。其可選整數參數 `siglen` 決定簽章長度（以位元組計）。預設簽章長度為 16 位元組。有效的簽章長度介於 1 至 2024 位元組之間。較長的簽章可帶來更精確的搜尋（掃描較小比例的索引與較少的堆積頁面），代價是索引較大。

另有非預設的 GIN 運算子類別 `gin__int_ops`，它除了支援這些運算子外，也支援 `<@`。

GiST 與 GIN 索引之間的選擇，取決於其他章節所討論的兩者相對效能特性。

<a id="INTARRAY-EXAMPLE"></a>

### F.19.3. 範例 [#](#intarray-example) <a href="#intarray-example" id="intarray-example"></a>

```

-- a message can be in one or more “sections”
CREATE TABLE message (mid INT PRIMARY KEY, sections INT[], ...);

-- create specialized index with signature length of 32 bytes
CREATE INDEX message_rdtree_idx ON message USING GIST (sections gist__intbig_ops (siglen = 32));

-- select messages in section 1 OR 2 - OVERLAP operator
SELECT message.mid FROM message WHERE message.sections && '{1,2}';

-- select messages in sections 1 AND 2 - CONTAINS operator
SELECT message.mid FROM message WHERE message.sections @> '{1,2}';

-- the same, using QUERY operator
SELECT message.mid FROM message WHERE message.sections @@ '1&2'::query_int;
```

<a id="INTARRAY-BENCHMARK"></a>

### F.19.4. 效能測試 [#](#intarray-benchmark) <a href="#intarray-benchmark" id="intarray-benchmark"></a>

原始碼目錄 `contrib/intarray/bench` 包含效能測試套件，可針對已安裝的 PostgreSQL 伺服器執行。（它也需要安裝 `DBD::Pg`。）執行方式如下：

```

cd .../contrib/intarray/bench
createdb TEST
psql -c "CREATE EXTENSION intarray" TEST
./create_test.pl | psql TEST
./bench.pl
```

`bench.pl` 指令碼具有許多選項；在不帶任何引數執行時會顯示這些選項。

<a id="INTARRAY-AUTHORS"></a>

### F.19.5. 作者 [#](#intarray-authors) <a href="#intarray-authors" id="intarray-authors"></a>

所有工作由 Teodor Sigaev（`<teodor@sigaev.ru>`）與 Oleg Bartunov（`<oleg@sai.msu.su>`）完成。詳細資訊請參閱 <http://www.sai.msu.su/~megera/postgres/gist/>。Andrey Oktyabrski 對新增函式與操作做出了重要貢獻。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/intarray.html)
