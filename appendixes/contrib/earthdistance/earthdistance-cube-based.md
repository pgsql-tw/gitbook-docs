# F.14.1. 以 Cube 為基礎的地球距離

<a id="EARTHDISTANCE-CUBE-BASED"></a>

## F.14.1. 以 Cube 為基礎的地球距離 [#](#earthdistance-cube-based) <a href="#earthdistance-cube-based" id="earthdistance-cube-based"></a>

資料會以 point cube（兩個角點相同）儲存，使用三個座標表示與地球中心的 x、y、z
距離。模組提供建置於 `cube` 型別上的 [*domain*](../../glossary/README.md#glossary-domain)
`earth`，其中包含限制條件檢查，以確保值符合這些限制且合理接近地球的實際表面。

地球半徑由 `earth()` 函式取得，單位為公尺。但只要變更這一個函式，即可讓模組
使用其他單位，或使用你認為較適當的不同半徑值。

此套件也可用於天文資料庫。天文學家可能會想讓 `earth()` 傳回 `180/pi()` 的
半徑，使距離單位成為度。

提供的函式支援以緯度與經度（度）輸入、輸出緯度與經度、計算兩點之間的大圓距離，
以及方便地指定可用於索引搜尋的邊界方框。

提供的函式如[表 F.4](#earthdistance-cube-functions) 所示。

<a id="EARTHDISTANCE-CUBE-FUNCTIONS"></a>

### 表 F.4. 以 Cube 為基礎的 Earthdistance 函式 [#](#earthdistance-cube-functions) <a href="#earthdistance-cube-functions" id="earthdistance-cube-functions"></a>

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

[返回 F.14. earthdistance — 計算大圓距離](../earthdistance.md#earthdistance)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/earthdistance.html)
