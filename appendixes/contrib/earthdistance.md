## F.14. earthdistance — 計算大圓距離 [#](#EARTHDISTANCE)

[F.14.1. 以 Cube 為基礎的地球距離](earthdistance.md#EARTHDISTANCE-CUBE-BASED)

[F.14.2. 以 Point 為基礎的地球距離](earthdistance.md#EARTHDISTANCE-POINT-BASED)

<a id="id-1.11.7.24.2"></a>

`earthdistance` 模組提供兩種計算地球表面大圓距離的方法。第一種方法依賴
`cube` 模組；第二種方法以內建 `point` 資料型別為基礎，使用經度與緯度作為
座標。

此模組假定地球為完美球體。（若這對你而言不夠精確，可能想參考
[PostGIS](https://postgis.net/) 專案。）

必須先安裝 `cube` 模組，才能安裝 `earthdistance`（不過可使用
`CREATE EXTENSION` 的 `CASCADE` 選項，在一個命令中安裝兩者）。

### 注意

強烈建議將 `earthdistance` 與 `cube` 安裝至相同 schema，且該 schema 未曾且不會
授予任何不受信任使用者 CREATE 權限。否則，若 `earthdistance` 的 schema 含有
惡意使用者定義的物件，安裝時會有安全性風險。此外，安裝後使用
`earthdistance` 函式時，整個搜尋路徑應只包含受信任的 schema。

<a id="EARTHDISTANCE-CUBE-BASED"></a>

### F.14.1. 以 Cube 為基礎的地球距離 [#](#EARTHDISTANCE-CUBE-BASED)

資料會以 point cube（兩個角點相同）儲存，使用三個座標表示與地球中心的 x、y、z
距離。模組提供建置於 `cube` 型別上的 [*[domain](../glossary/README.md#GLOSSARY-DOMAIN)*](../glossary/README.md#GLOSSARY-DOMAIN)
`earth`，其中包含限制條件檢查，以確保值符合這些限制且合理接近地球的實際表面。

地球半徑由 `earth()` 函式取得，單位為公尺。但只要變更這一個函式，即可讓模組
使用其他單位，或使用你認為較適當的不同半徑值。

此套件也可用於天文資料庫。天文學家可能會想讓 `earth()` 傳回 `180/pi()` 的
半徑，使距離單位成為度。

提供的函式支援以緯度與經度（度）輸入、輸出緯度與經度、計算兩點之間的大圓距離，
以及方便地指定可用於索引搜尋的邊界方框。

The provided functions are shown
如[表 F.4](earthdistance.md#EARTHDISTANCE-CUBE-FUNCTIONS) 所示。

<a id="EARTHDISTANCE-CUBE-FUNCTIONS"></a>

**表 F.4. 以 Cube 為基礎的 Earthdistance 函式**

<table border="1" class="table" summary="Cube-Based Earthdistance Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.1.1.1.1"></a>
<code class="function">earth</code> ()
        → <code class="returnvalue">float8</code>
</p>
<p>
        傳回假定的地球半徑。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.2.1.1.1"></a>
<code class="function">sec_to_gc</code> ( <code class="type">float8</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        將地球表面兩點間的一般直線（割線）距離轉換為兩點間的大圓距離。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.3.1.1.1"></a>
<code class="function">gc_to_sec</code> ( <code class="type">float8</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        將地球表面兩點間的大圓距離轉換為兩點間的一般直線（割線）距離。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.4.1.1.1"></a>
<code class="function">ll_to_earth</code> ( <code class="type">float8</code>, <code class="type">float8</code> )
        → <code class="returnvalue">earth</code>
</p>
<p>
        根據點的緯度（引數 1）及經度（引數 2）度數，傳回其在地球表面的位置。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.5.1.1.1"></a>
<code class="function">latitude</code> ( <code class="type">earth</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        傳回地球表面上一點的緯度（度）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.6.1.1.1"></a>
<code class="function">longitude</code> ( <code class="type">earth</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        傳回地球表面上一點的經度（度）。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.7.1.1.1"></a>
<code class="function">earth_distance</code> ( <code class="type">earth</code>, <code class="type">earth</code> )
        → <code class="returnvalue">float8</code>
</p>
<p>
        傳回地球表面兩點之間的大圓距離。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.11.7.24.7.7.2.2.8.1.1.1"></a>
<code class="function">earth_box</code> ( <code class="type">earth</code>, <code class="type">float8</code> )
        → <code class="returnvalue">cube</code>
</p>
<p>
        傳回適合索引搜尋的方框，可使用 <code class="type">cube</code>
<code class="literal">@&gt;</code>
        運算子尋找與某位置相隔指定大圓距離內的點。此方框中的某些點與該位置
        相隔的距離會超過指定大圓距離，因此查詢中應包含使用
        <code class="function">earth_distance</code> 的第二次檢查。
       </p></td></tr></tbody></table>

<br>

<a id="EARTHDISTANCE-POINT-BASED"></a>

### F.14.2. 以 Point 為基礎的地球距離 [#](#EARTHDISTANCE-POINT-BASED)

模組的第二部分將地球位置表示為 `point` 型別的值，其中第一個分量表示度數的
經度，第二個分量表示度數的緯度。點採用 (經度, 緯度)，而非相反順序，因為
經度較接近 x 軸、緯度較接近 y 軸的直觀概念。

提供一個運算子，如[表 F.5](earthdistance.md#EARTHDISTANCE-POINT-OPERATORS) 所示。

<a id="EARTHDISTANCE-POINT-OPERATORS"></a>

**表 F.5. 以 Point 為基礎的 Earthdistance 運算子**

<table border="1" class="table" summary="Point-Based Earthdistance Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">point</code> <code class="literal">&lt;@&gt;</code> <code class="type">point</code>
        → <code class="returnvalue">float8</code>
</p>
<p>
        計算地球表面兩點之間的法定英里距離。
       </p></td></tr></tbody></table>

<br>

請注意，與模組以 `cube` 為基礎的部分不同，這裡的單位是固定的；變更 `earth()`
函式不會影響此運算子的結果。

經度／緯度表示法的一項缺點是，必須留意接近極點與經度 +/- 180 度時的邊界
條件。以 `cube` 為基礎的表示法可避免這些不連續性。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/earthdistance.html)
