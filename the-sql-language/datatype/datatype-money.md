<a id="DATATYPE-MONEY"></a>

## 8.2. 貨幣型別 [#](#DATATYPE-MONEY)

`money` 型別以固定的小數精度儲存貨幣金額；請參閱[表 8.3](datatype-money.md#DATATYPE-MONEY-TABLE)。小數精度由資料庫的 [lc_monetary](../../server-administration/runtime-config/runtime-config-client.md#GUC-LC-MONETARY) 設定決定。表中所列的範圍假設有兩位小數。輸入時可接受多種格式，包括整數與浮點數常數，以及典型的貨幣格式，例如 `'$1,000.00'`。輸出通常採用後者的形式，但取決於語系。

<a id="DATATYPE-MONEY-TABLE"></a>

**表 8.3. 貨幣型別**

<table border="1" class="table" summary="貨幣型別"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/></colgroup><thead><tr><th>名稱</th><th>儲存空間大小</th><th>說明</th><th>範圍</th></tr></thead><tbody><tr><td><code class="type">money</code></td><td>8 個位元組</td><td>貨幣金額</td><td>-92233720368547758.08 至 +92233720368547758.07</td></tr></tbody></table>

<br>

由於這個資料型別的輸出會受語系影響，將 `money` 資料載入到 `lc_monetary` 設定不同的資料庫中可能無法正常運作。為避免問題，在把備份傾印還原到新資料庫之前，請確認 `lc_monetary` 與被傾印的資料庫具有相同或等效的值。

`numeric`、`int` 與 `bigint` 資料型別的值可以轉換為 `money`。從 `real` 與 `double precision` 資料型別轉換時，可以先轉換為 `numeric` 來完成，例如：

```

SELECT '12.34'::float8::numeric::money;
```

不過並不建議這麼做。由於可能產生捨入誤差，浮點數不應該用來處理金錢。

`money` 值可以在不損失精度的情況下轉換為 `numeric`。轉換為其他型別則可能會損失精度，而且同樣必須分兩個階段進行：

```

SELECT '52093.89'::money::numeric::float8;
```

`money` 值除以整數值時，小數部分會朝零的方向被截斷。若要取得四捨五入的結果，請除以浮點數值，或是在相除之前先將 `money` 值轉換為 `numeric`，之後再轉換回 `money`。（為了避免損失精度的風險，後者較為可取。）當 `money` 值除以另一個 `money` 值時，結果會是 `double precision`（也就是純粹的數字，而非金額）；相除時貨幣單位會互相抵消。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-money.html)（原文版本：18.6；核對日期：2026-09-13）
