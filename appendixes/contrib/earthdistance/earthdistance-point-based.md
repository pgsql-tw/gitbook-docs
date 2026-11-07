# F.14.2. 以 Point 為基礎的地球距離

<a id="EARTHDISTANCE-POINT-BASED"></a>

## F.14.2. 以 Point 為基礎的地球距離 [#](#earthdistance-point-based) <a href="#earthdistance-point-based" id="earthdistance-point-based"></a>

模組的第二部分將地球位置表示為 `point` 型別的值，其中第一個分量表示度數的
經度，第二個分量表示度數的緯度。點採用 (經度, 緯度)，而非相反順序，因為
經度較接近 x 軸、緯度較接近 y 軸的直觀概念。

提供一個運算子，如[表 F.5](#earthdistance-point-operators) 所示。

<a id="EARTHDISTANCE-POINT-OPERATORS"></a>

### 表 F.5. 以 Point 為基礎的 Earthdistance 運算子 [#](#earthdistance-point-operators) <a href="#earthdistance-point-operators" id="earthdistance-point-operators"></a>

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
[返回 F.14. earthdistance — 計算大圓距離](../earthdistance.md#earthdistance)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/earthdistance.html)
