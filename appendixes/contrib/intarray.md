## F.19. intarray — 操作整數陣列 [#](#INTARRAY)

[F.19.1. `intarray` 函式與運算子](intarray.md#INTARRAY-FUNCS-OPS)

[F.19.2. 索引支援](intarray.md#INTARRAY-INDEX)

[F.19.3. 範例](intarray.md#INTARRAY-EXAMPLE)

[F.19.4. 效能測試](intarray.md#INTARRAY-BENCHMARK)

[F.19.5. 作者](intarray.md#INTARRAY-AUTHORS)

<a id="id-1.11.7.29.2"></a>

`intarray` 模組提供數個實用函式與運算子，用於操作不含 NULL 的整數陣列。部分運算子也支援使用索引進行搜尋。

若提供的陣列含有任何 NULL 元素，所有這些操作都會引發錯誤。

許多操作只對一維陣列有意義。雖然它們接受較多維度的輸入陣列，但資料會依儲存順序視為線性陣列處理。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="INTARRAY-FUNCS-OPS"></a>

### F.19.1. `intarray` 函式與運算子 [#](#INTARRAY-FUNCS-OPS)

`intarray` 模組提供的函式列於[表 F.8](intarray.md#INTARRAY-FUNC-TABLE)，運算子列於[表 F.9](intarray.md#INTARRAY-OP-TABLE)。

<a id="INTARRAY-FUNC-TABLE"></a>

**表 F.8. `intarray` 函式**

<table border="1" class="table" summary="intarray Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.1.1.1.1"></a>
<code class="function">icount</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回陣列中的元素數量。
       </p>
<p>
<code class="literal">icount('{1,2,3}'::integer[])</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.2.1.1.1"></a>
<code class="function">sort</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>dir</code></em> <code class="type">text</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        以遞增或遞減順序排序陣列。<em class="parameter"><code>dir</code></em> 必須是 <code class="literal">asc</code> 或 <code class="literal">desc</code>。
       </p>
<p>
<code class="literal">sort('{1,3,2}'::integer[], 'desc')</code>
        → <code class="returnvalue">{3,2,1}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">sort</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.3.1.2.1"></a>
<code class="function">sort_asc</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        以遞增順序排序。
       </p>
<p>
<code class="literal">sort(array[11,77,44])</code>
        → <code class="returnvalue">{11,44,77}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.4.1.1.1"></a>
<code class="function">sort_desc</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        以遞減順序排序。
       </p>
<p>
<code class="literal">sort_desc(array[11,77,44])</code>
        → <code class="returnvalue">{77,44,11}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.5.1.1.1"></a>
<code class="function">uniq</code> ( <code class="type">integer[]</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        移除相鄰的重複項目。常與 <code class="function">sort</code> 搭配使用，以移除所有重複項目。
       </p>
<p>
<code class="literal">uniq('{1,2,2,3,1,1}'::integer[])</code>
        → <code class="returnvalue">{1,2,3,1}</code>
</p>
<p>
<code class="literal">uniq(sort('{1,2,3,2,1}'::integer[]))</code>
        → <code class="returnvalue">{1,2,3}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.6.1.1.1"></a>
<code class="function">idx</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>item</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回第一個符合 <em class="parameter"><code>item</code></em> 的陣列元素索引；若沒有符合項目則傳回 0。
       </p>
<p>
<code class="literal">idx(array[11,22,33,22,11], 22)</code>
        → <code class="returnvalue">2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.7.1.1.1"></a>
<code class="function">subarray</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code>, <em class="parameter"><code>len</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        擷取從位置 <em class="parameter"><code>start</code></em> 開始、含有 <em class="parameter"><code>len</code></em> 個元素的陣列部分。
       </p>
<p>
<code class="literal">subarray('{1,2,3,2,1}'::integer[], 2, 3)</code>
        → <code class="returnvalue">{2,3,2}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">subarray</code> ( <code class="type">integer[]</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        擷取從位置 <em class="parameter"><code>start</code></em> 開始的陣列部分。
       </p>
<p>
<code class="literal">subarray('{1,2,3,2,1}'::integer[], 2)</code>
        → <code class="returnvalue">{2,3,2,1}</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.29.7.3.2.2.9.1.1.1"></a>
<code class="function">intset</code> ( <code class="type">integer</code> )
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        建立單一元素陣列。
       </p>
<p>
<code class="literal">intset(42)</code>
        → <code class="returnvalue">{42}</code>
</p></td></tr></tbody></table>

<br><a id="INTARRAY-OP-TABLE"></a>

**表 F.9. `intarray` 運算子**

<table border="1" class="table" summary="intarray Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">&amp;&amp;</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否重疊（至少有一個共同元素）？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">@&gt;</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側陣列是否包含右側陣列？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">&lt;@</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側陣列是否包含於右側陣列？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type"></code> <code class="literal">#</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回陣列中的元素數量。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">#</code> <code class="type">integer</code>
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回第一個符合右側引數的陣列元素索引；若沒有符合項目則傳回 0。（與 <code class="function">idx</code> 函式相同。）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">+</code> <code class="type">integer</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        將元素新增至陣列末端。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">+</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        串接陣列。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">-</code> <code class="type">integer</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        從陣列移除符合右側引數的項目。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">-</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        從左側陣列移除右側陣列的元素。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">|</code> <code class="type">integer</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        計算引數的聯集。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">|</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        計算引數的聯集。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">&amp;</code> <code class="type">integer[]</code>
        → <code class="returnvalue">integer[]</code>
</p>
<p>
        計算引數的交集。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">integer[]</code> <code class="literal">@@</code> <code class="type">query_int</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否滿足查詢？（見下文）
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">query_int</code> <code class="literal">~~</code> <code class="type">integer[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否滿足查詢？（<code class="literal">@@</code> 的交換子）
       </p></td></tr></tbody></table>

<br>

`&&`、`@>` 與 `<@` 運算子等同於 PostgreSQL 同名內建運算子，但它們僅可處理不含 NULL 的整數陣列，而內建運算子可處理任何陣列型別。這項限制使它們在許多情況下比內建運算子更快。

`@@` 與 `~~` 運算子測試陣列是否滿足*查詢*；查詢以專用資料型別 `query_int` 的值表示。*查詢*由要與陣列元素比對的整數值組成，可能使用 `&`（AND）、`|`（OR）與 `!`（NOT）運算子組合。可視需要使用括號。例如，查詢 `1&(2|3)` 符合包含 1 且包含 2 或 3 其中之一的陣列。

<a id="INTARRAY-INDEX"></a>

### F.19.2. 索引支援 [#](#INTARRAY-INDEX)

`intarray` 為 `&&`、`@>` 與 `@@` 運算子及一般陣列相等比較提供索引支援。

提供兩個參數化 GiST 索引運算子類別：`gist__int_ops`（預設使用）適用於小型至中型資料集，而 `gist__intbig_ops` 使用較大的簽章，較適合為大型資料集（亦即含有大量相異陣列值的欄位）建立索引。實作使用內建有失壓縮的 RD-tree 資料結構。

`gist__int_ops` 會將整數集合近似為整數範圍的陣列。其可選整數參數 `numranges` 決定一個索引鍵中的最大範圍數。`numranges` 預設值為 100。有效值介於 1 至 253 之間。使用較大的陣列作為 GiST 索引鍵可帶來更精確的搜尋（掃描較小比例的索引與較少的堆積頁面），代價是索引較大。

`gist__intbig_ops` 會將整數集合近似為點陣圖簽章。其可選整數參數 `siglen` 決定簽章長度（以位元組計）。預設簽章長度為 16 位元組。有效的簽章長度介於 1 至 2024 位元組之間。較長的簽章可帶來更精確的搜尋（掃描較小比例的索引與較少的堆積頁面），代價是索引較大。

另有非預設的 GIN 運算子類別 `gin__int_ops`，它除了支援這些運算子外，也支援 `<@`。

GiST 與 GIN 索引之間的選擇，取決於其他章節所討論的兩者相對效能特性。

<a id="INTARRAY-EXAMPLE"></a>

### F.19.3. 範例 [#](#INTARRAY-EXAMPLE)

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

### F.19.4. 效能測試 [#](#INTARRAY-BENCHMARK)

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

### F.19.5. 作者 [#](#INTARRAY-AUTHORS)

所有工作由 Teodor Sigaev（`<teodor@sigaev.ru>`）與 Oleg Bartunov（`<oleg@sai.msu.su>`）完成。詳細資訊請參閱 <http://www.sai.msu.su/~megera/postgres/gist/>。Andrey Oktyabrski 對新增函式與操作做出了重要貢獻。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/intarray.html)
