<a id="EARTHDISTANCE"></a>

## F.14. earthdistance — 計算大圓距離 [#](#earthdistance) <a href="#earthdistance" id="earthdistance"></a>

[F.14.1. 以 Cube 為基礎的地球距離](earthdistance/earthdistance-cube-based.md#earthdistance-cube-based)

[F.14.2. 以 Point 為基礎的地球距離](earthdistance/earthdistance-point-based.md#earthdistance-point-based)

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

### F.14.1. 以 Cube 為基礎的地球距離 [#](#earthdistance-cube-based) <a href="#earthdistance-cube-based" id="earthdistance-cube-based"></a>

完整內容請見 [F.14.1. 以 Cube 為基礎的地球距離](earthdistance/earthdistance-cube-based.md#earthdistance-cube-based)。

### F.14.2. 以 Point 為基礎的地球距離 [#](#earthdistance-point-based) <a href="#earthdistance-point-based" id="earthdistance-point-based"></a>

完整內容請見 [F.14.2. 以 Point 為基礎的地球距離](earthdistance/earthdistance-point-based.md#earthdistance-point-based)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/earthdistance.html)
