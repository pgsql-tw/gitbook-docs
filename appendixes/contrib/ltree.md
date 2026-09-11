<a id="LTREE"></a>

## F.22. ltree — 階層式樹狀資料型別 [#](#LTREE)

[F.22.1. 定義](ltree.md#LTREE-DEFINITIONS)

[F.22.2. 運算子與函式](ltree.md#LTREE-OPS-FUNCS)

[F.22.3. 索引](ltree.md#LTREE-INDEXES)

[F.22.4. 範例](ltree.md#LTREE-EXAMPLE)

[F.22.5. 轉換](ltree.md#LTREE-TRANSFORMS)

[F.22.6. 作者](ltree.md#LTREE-AUTHORS)

<a id="id-1.11.7.32.2"></a>

此模組實作資料型別 `ltree`，用以表示儲存在階層式樹狀結構中資料的標籤。它提供廣泛的標籤樹搜尋功能。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="LTREE-DEFINITIONS"></a>

### F.22.1. 定義 [#](#LTREE-DEFINITIONS)

*標籤*是由英數字元、底線與連字號組成的序列。有效的英數字元範圍取決於資料庫地區設定。例如，在 C 地區設定中，允許字元 `A-Za-z0-9_-`。標籤長度不可超過 1000 個字元。

範例：`42`、`Personal_Services`

*標籤路徑*是零個或多個以點分隔的標籤序列，例如 `L1.L2.L3`，表示從階層樹根節點到特定節點的路徑。標籤路徑不可超過 65535 個標籤。

範例：`Top.Countries.Europe.Russia`

`ltree` 模組提供數種資料型別：

* `ltree` 儲存標籤路徑。
* `lquery` 表示類似正規表示式的模式，用於比對 `ltree` 值。簡單單字會比對路徑中的該標籤。星號符號（`*`）會比對零個或多個標籤。它們可使用點連結成必須符合整個標籤路徑的模式。例如：

  ```

  foo         比對完全相同的標籤路徑 foo
  *.foo.*     比對任何包含標籤 foo 的標籤路徑
  *.foo       比對任何最後一個標籤為 foo 的標籤路徑
  ```

  星號符號與簡單單字都可加上量詞，以限制可比對的標籤數：

  ```

  *{n}        比對恰好 n 個標籤
  *{n,}       比對至少 n 個標籤
  *{n,m}      比對至少 n 個、至多 m 個標籤
  *{,m}       比對至多 m 個標籤，等同於 *{0,m}
  foo{n,m}    比對至少 n 次、至多 m 次出現的 foo
  foo{,}      比對任意次數出現的 foo，包括零次
  ```

  沒有明確量詞時，星號符號預設比對任意數量的標籤（亦即 `{,}`），非星號項目的預設值則是恰好比對一次（亦即 `{1}`）。

  可在非星號的 `lquery` 項目結尾加上數種修飾字，使其不僅限於完全比對：

  ```

  @           不區分大小寫比對，例如 a@ 符合 A
  *           比對具有此前綴的任何標籤，例如 foo* 符合 foobar
  %           比對標籤開頭以底線分隔的單字
  ```

  `%` 的行為稍微複雜。它嘗試比對單字而非整個標籤。例如，`foo_bar%` 符合 `foo_bar_baz`，但不符合 `foo_barbaz`。若與 `*` 組合，前綴比對會分別套用於每個單字；例如，`foo_bar%*` 符合 `foo1_bar2_baz`，但不符合 `foo1_br2_baz`。

  此外，可以用 `|`（OR）分隔多個可帶有修飾字的非星號項目，以比對其中任一項目；也可在非星號群組開頭放置 `!`（NOT），以比對不符合任何選項的標籤。量詞（若有）放在群組結尾，表示整個群組的比對次數，也就是有多少個標籤符合任一選項，或不符合任何選項。

  以下是加註解的 `lquery` 範例：

  ```

  Top.*{0,2}.sport*@.!football|tennis{1,}.Russ*|Spain
  a.  b.     c.      d.                   e.
  ```

  此查詢會比對符合下列條件的任何標籤路徑：

  1. 以標籤 `Top` 開始；
  2. 接著在下列標籤之前有零至兩個標籤；
  3. 以不區分大小寫的前綴 `sport` 開始的標籤；
  4. 然後有一個或多個不符合 `football` 與 `tennis` 的標籤；
  5. 最後以 `Russ` 開頭的標籤或完全符合 `Spain` 的標籤結束。
* `ltxtquery` 表示類似全文檢索的模式，用於比對 `ltree` 值。`ltxtquery` 值包含單字，結尾可能帶有修飾字 `@`、`*`、`%`；修飾字的意義與 `lquery` 相同。單字可用 `&`（AND）、`|`（OR）、`!`（NOT）及括號組合。它與 `lquery` 的主要差異在於，`ltxtquery` 比對單字時不考慮其在標籤路徑中的位置。

  以下是 `ltxtquery` 範例：

  ```

  Europe & Russia*@ & !Transportation
  ```

  此範例會比對含有標籤 `Europe` 與任何以 `Russia` 開頭（不區分大小寫）之標籤的路徑，但不比對含有標籤 `Transportation` 的路徑。這些單字在路徑中的位置並不重要。此外，使用 `%` 時，單字可比對標籤內任一以底線分隔的單字，與位置無關。

注意：`ltxtquery` 允許符號之間有空白，但 `ltree` 與 `lquery` 不允許。

<a id="LTREE-OPS-FUNCS"></a>

### F.22.2. 運算子與函式 [#](#LTREE-OPS-FUNCS)

型別 `ltree` 具有一般比較運算子 `=`、`<>`、`<`、`>`、`<=`、`>=`。比較會依樹狀走訪順序排序，節點子項目則依標籤文字排序。此外，還提供[表 F.12](ltree.md#LTREE-OP-TABLE) 所示的專用運算子。

<a id="LTREE-OP-TABLE"></a>

**表 F.12. `ltree` 運算子**

<table border="1" class="table" summary="ltree Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">@&gt;</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側引數是否為右側引數的祖先（或相等）？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">&lt;@</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        左側引數是否為右側引數的子孫（或相等）？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">~</code> <code class="type">lquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery</code> <code class="literal">~</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 是否符合 <code class="type">lquery</code>？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">?</code> <code class="type">lquery[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery[]</code> <code class="literal">?</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 是否符合陣列中的任何 <code class="type">lquery</code>？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">@</code> <code class="type">ltxtquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltxtquery</code> <code class="literal">@</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 是否符合 <code class="type">ltxtquery</code>？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">||</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        串接 <code class="type">ltree</code> 路徑。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree</code> <code class="literal">||</code> <code class="type">text</code>
        → <code class="returnvalue">ltree</code>
</p>
<p class="func_signature">
<code class="type">text</code> <code class="literal">||</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        將文字轉換為 <code class="type">ltree</code> 並串接。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">@&gt;</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltree</code> <code class="literal">&lt;@</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含 <code class="type">ltree</code> 的祖先？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">&lt;@</code> <code class="type">ltree</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltree</code> <code class="literal">@&gt;</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含 <code class="type">ltree</code> 的子孫？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">~</code> <code class="type">lquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery</code> <code class="literal">~</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含符合 <code class="type">lquery</code> 的任何路徑？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?</code> <code class="type">lquery[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">lquery[]</code> <code class="literal">?</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        <code class="type">ltree</code> 陣列是否包含符合任何 <code class="type">lquery</code> 的任何路徑？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">@</code> <code class="type">ltxtquery</code>
        → <code class="returnvalue">boolean</code>
</p>
<p class="func_signature">
<code class="type">ltxtquery</code> <code class="literal">@</code> <code class="type">ltree[]</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        陣列是否包含符合 <code class="type">ltxtquery</code> 的任何路徑？
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?@&gt;</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個為 <code class="type">ltree</code> 祖先的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?&lt;@</code> <code class="type">ltree</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個為 <code class="type">ltree</code> 子孫的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?~</code> <code class="type">lquery</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個符合 <code class="type">lquery</code> 的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">ltree[]</code> <code class="literal">?@</code> <code class="type">ltxtquery</code>
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回第一個符合 <code class="type">ltxtquery</code> 的陣列項目；若沒有則傳回 <code class="literal">NULL</code>。
       </p></td></tr></tbody></table>

<br>

`<@`、`@>`、`@` 與 `~` 運算子有對應的 `^<@`、`^@>`、`^@`、`^~`；它們相同，但不使用索引。這些只適合測試用途。

可用函式列於[表 F.13](ltree.md#LTREE-FUNC-TABLE)。

<a id="LTREE-FUNC-TABLE"></a>

**表 F.13. `ltree` 函式**

<table border="1" class="table" summary="ltree Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.1.1.1.1"></a>
<code class="function">subltree</code> ( <code class="type">ltree</code>, <em class="parameter"><code>start</code></em> <code class="type">integer</code>, <em class="parameter"><code>end</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回 <code class="type">ltree</code> 從位置 <em class="parameter"><code>start</code></em> 到位置 <em class="parameter"><code>end</code></em>-1 的子路徑（從 0 起算）。
       </p>
<p>
<code class="literal">subltree('Top.Child1.Child2', 1, 2)</code>
        → <code class="returnvalue">Child1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.2.1.1.1"></a>
<code class="function">subpath</code> ( <code class="type">ltree</code>, <em class="parameter"><code>offset</code></em> <code class="type">integer</code>, <em class="parameter"><code>len</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回從位置 <em class="parameter"><code>offset</code></em> 開始、長度為 <em class="parameter"><code>len</code></em> 的 <code class="type">ltree</code> 子路徑。若 <em class="parameter"><code>offset</code></em> 為負數，子路徑從距路徑結尾該數量的位置開始。若 <em class="parameter"><code>len</code></em> 為負數，會從路徑結尾移除該數量的標籤。
       </p>
<p>
<code class="literal">subpath('Top.Child1.Child2', 0, 2)</code>
        → <code class="returnvalue">Top.Child1</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">subpath</code> ( <code class="type">ltree</code>, <em class="parameter"><code>offset</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        傳回從位置 <em class="parameter"><code>offset</code></em> 開始並延伸至路徑結尾的 <code class="type">ltree</code> 子路徑。若 <em class="parameter"><code>offset</code></em> 為負數，子路徑從距路徑結尾該數量的位置開始。
       </p>
<p>
<code class="literal">subpath('Top.Child1.Child2', 1)</code>
        → <code class="returnvalue">Child1.Child2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.4.1.1.1"></a>
<code class="function">nlevel</code> ( <code class="type">ltree</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回路徑中的標籤數量。
       </p>
<p>
<code class="literal">nlevel('Top.Child1.Child2')</code>
        → <code class="returnvalue">3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.5.1.1.1"></a>
<code class="function">index</code> ( <em class="parameter"><code>a</code></em> <code class="type">ltree</code>, <em class="parameter"><code>b</code></em> <code class="type">ltree</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回 <em class="parameter"><code>b</code></em> 在 <em class="parameter"><code>a</code></em> 中第一次出現的位置；若找不到則傳回 -1。
       </p>
<p>
<code class="literal">index('0.1.2.3.5.4.5.6.8.5.6.8', '5.6')</code>
        → <code class="returnvalue">6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">index</code> ( <em class="parameter"><code>a</code></em> <code class="type">ltree</code>,  <em class="parameter"><code>b</code></em> <code class="type">ltree</code>, <em class="parameter"><code>offset</code></em> <code class="type">integer</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        傳回 <em class="parameter"><code>b</code></em> 在 <em class="parameter"><code>a</code></em> 中第一次出現的位置；若找不到則傳回 -1。搜尋從位置 <em class="parameter"><code>offset</code></em> 開始；若 <em class="parameter"><code>offset</code></em> 為負數，則從距離路徑結尾 <em class="parameter"><code>-offset</code></em> 個標籤的位置開始。
       </p>
<p>
<code class="literal">index('0.1.2.3.5.4.5.6.8.5.6.8', '5.6', -4)</code>
        → <code class="returnvalue">9</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.7.1.1.1"></a>
<code class="function">text2ltree</code> ( <code class="type">text</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        將 <code class="type">text</code> 轉型為 <code class="type">ltree</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.8.1.1.1"></a>
<code class="function">ltree2text</code> ( <code class="type">ltree</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        將 <code class="type">ltree</code> 轉型為 <code class="type">text</code>。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.32.6.6.2.2.9.1.1.1"></a>
<code class="function">lca</code> ( <code class="type">ltree</code> [<span class="optional">, <code class="type">ltree</code> [<span class="optional">, ... </span>]</span>] )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        計算各路徑最長的共同祖先路徑（最多支援 8 個引數）。
       </p>
<p>
<code class="literal">lca('1.2.3', '1.2.3.4.5.6')</code>
        → <code class="returnvalue">1.2</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">lca</code> ( <code class="type">ltree[]</code> )
        → <code class="returnvalue">ltree</code>
</p>
<p>
        計算陣列中各路徑最長的共同祖先路徑。
       </p>
<p>
<code class="literal">lca(array['1.2.3'::ltree,'1.2.3.4'])</code>
        → <code class="returnvalue">1.2</code>
</p></td></tr></tbody></table>

<br>

<a id="LTREE-INDEXES"></a>

### F.22.3. 索引 [#](#LTREE-INDEXES)

`ltree` 支援數種索引，可加速下列對應運算子的操作：

* `ltree` 的 B-tree 索引：
  `<`, `<=`, `=`,
  `>=`, `>`
* `ltree` 的雜湊索引：
  `=`
* `ltree` 的 GiST 索引（`gist_ltree_ops` 運算子類別）：
  `<`, `<=`, `=`,
  `>=`, `>`,
  `@>`, `<@`,
  `@`, `~`, `?`

  `gist_ltree_ops` GiST 運算子類別以位元映射簽章近似表示一組路徑標籤。其選用的整數參數 `siglen` 決定簽章長度，單位為位元組。預設簽章長度為 8 位元組。長度必須是 `int` 對齊大小（大多數機器為 4 位元組）的正整數倍，且不可超過 2024 位元組。較長的簽章能使搜尋更精確（掃描較小比例的索引與較少的 heap 頁面），代價是索引較大。

  使用預設 8 位元組簽章長度建立此類索引的範例：

  ```

  CREATE INDEX path_gist_idx ON test USING GIST (path);
  ```

  使用 100 位元組簽章長度建立此類索引的範例：

  ```

  CREATE INDEX path_gist_idx ON test USING GIST (path gist_ltree_ops(siglen=100));
  ```
* `ltree[]` 的 GiST 索引（`gist__ltree_ops` 運算子類別）：
  `ltree[] <@ ltree`, `ltree @> ltree[]`,
  `@`, `~`, `?`

  `gist__ltree_ops` GiST 運算子類別的運作方式類似於 `gist_ltree_ops`，也接受簽章長度作為參數。`gist__ltree_ops` 的 `siglen` 預設值為 28 位元組。

  使用預設 28 位元組簽章長度建立此類索引的範例：

  ```

  CREATE INDEX path_gist_idx ON test USING GIST (array_path);
  ```

  使用 100 位元組簽章長度建立此類索引的範例：

  ```

  CREATE INDEX path_gist_idx ON test USING GIST (array_path gist__ltree_ops(siglen=100));
  ```

  注意：此索引類型是有損的。

<a id="LTREE-EXAMPLE"></a>

### F.22.4. 範例 [#](#LTREE-EXAMPLE)

此範例使用下列資料（也可在原始碼發行套件的 `contrib/ltree/ltreetest.sql` 檔案中取得）：

```

CREATE TABLE test (path ltree);
INSERT INTO test VALUES ('Top');
INSERT INTO test VALUES ('Top.Science');
INSERT INTO test VALUES ('Top.Science.Astronomy');
INSERT INTO test VALUES ('Top.Science.Astronomy.Astrophysics');
INSERT INTO test VALUES ('Top.Science.Astronomy.Cosmology');
INSERT INTO test VALUES ('Top.Hobbies');
INSERT INTO test VALUES ('Top.Hobbies.Amateurs_Astronomy');
INSERT INTO test VALUES ('Top.Collections');
INSERT INTO test VALUES ('Top.Collections.Pictures');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy.Stars');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy.Galaxies');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy.Astronauts');
CREATE INDEX path_gist_idx ON test USING GIST (path);
CREATE INDEX path_idx ON test USING BTREE (path);
CREATE INDEX path_hash_idx ON test USING HASH (path);
```

現在，資料表 `test` 已填入描述下列階層結構的資料：

```

                        Top
                     /   |  \
             Science Hobbies Collections
                 /       |              \
        Astronomy   Amateurs_Astronomy Pictures
           /  \                            |
Astrophysics  Cosmology                Astronomy
                                        /  |    \
                                 Galaxies Stars Astronauts
```

我們可以查詢繼承關係：

```

ltreetest=> SELECT path FROM test WHERE path <@ 'Top.Science';
                path
------------------------------------
 Top.Science
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
(4 rows)
```

以下是一些路徑比對範例：

```

ltreetest=> SELECT path FROM test WHERE path ~ '*.Astronomy.*';
                     path
-----------------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
 Top.Collections.Pictures.Astronomy
 Top.Collections.Pictures.Astronomy.Stars
 Top.Collections.Pictures.Astronomy.Galaxies
 Top.Collections.Pictures.Astronomy.Astronauts
(7 rows)

ltreetest=> SELECT path FROM test WHERE path ~ '*.!pictures@.Astronomy.*';
                path
------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
(3 rows)
```

以下是一些全文檢索範例：

```

ltreetest=> SELECT path FROM test WHERE path @ 'Astro*% & !pictures@';
                path
------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
 Top.Hobbies.Amateurs_Astronomy
(4 rows)

ltreetest=> SELECT path FROM test WHERE path @ 'Astro* & !pictures@';
                path
------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
(3 rows)
```

使用函式建構路徑：

```

ltreetest=> SELECT subpath(path,0,2)||'Space'||subpath(path,2) FROM test WHERE path <@ 'Top.Science.Astronomy';
                 ?column?
------------------------------------------
 Top.Science.Space.Astronomy
 Top.Science.Space.Astronomy.Astrophysics
 Top.Science.Space.Astronomy.Cosmology
(3 rows)
```

我們可以建立 SQL 函式，在路徑的指定位置插入標籤，以簡化此操作：

```

CREATE FUNCTION ins_label(ltree, int, text) RETURNS ltree
    AS 'select subpath($1,0,$2) || $3 || subpath($1,$2);'
    LANGUAGE SQL IMMUTABLE;

ltreetest=> SELECT ins_label(path,2,'Space') FROM test WHERE path <@ 'Top.Science.Astronomy';
                ins_label
------------------------------------------
 Top.Science.Space.Astronomy
 Top.Science.Space.Astronomy.Astrophysics
 Top.Science.Space.Astronomy.Cosmology
(3 rows)
```

<a id="LTREE-TRANSFORMS"></a>

### F.22.5. 轉換 [#](#LTREE-TRANSFORMS)

`ltree_plpython3u` 擴充套件為 PL/Python 實作 `ltree` 型別的轉換。若已安裝此擴充套件，並在建立函式時指定此轉換，`ltree` 值就會對應為 Python 串列。（不過，目前尚不支援反向轉換。）

<a id="LTREE-AUTHORS"></a>

### F.22.6. 作者 [#](#LTREE-AUTHORS)

所有工作均由 Teodor Sigaev（`<teodor@stack.net>`）與 Oleg Bartunov（`<oleg@sai.msu.su>`）完成。更多資訊請參閱 <http://www.sai.msu.su/~megera/postgres/gist/>。作者感謝 Eugeny Rodichev 提供有益的討論，並歡迎提供意見與錯誤回報。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ltree.html)（核對日期：2026-09-11）
