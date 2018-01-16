# 8.2. 貨幣型別[^1]

貨幣型別儲存具有固定小數精確度的貨幣數量；詳見表 8.3。 小數精確度視資料庫的 [lc\_monetary](/iii-server-administration/server-configuration/1911-client-connection-defaults.md) 設定而定。表中顯示的範圍假設有兩個小數位。有許多可以接受的格式，包括整數和浮點數字，以及典型的貨幣格式，例如如「$1,000.00」。 輸出時通常採用後者的形式，但取決於語言環境（locale）。

**Table 8.3. Monetary Types**

| Name | Storage Size | Description | Range |
| :--- | :--- | :--- | :--- |
| `money` | 8 bytes | currency amount | -92233720368547758.08 to +92233720368547758.07 |

由於此資料型別的輸出是與區域設定有關的，因此可能無法將貨幣資料載入到不同 lc\_monetary 設定的資料庫中。為避免出現問題，在將轉換恢復到新的資料庫之前，請確保 lc\_monetary 與轉換的資料庫中的設定值相容。

numberic、int 和 bigint 資料型別的值可以轉換為 money。從 real 和 double precision 資料型別轉換會先轉為 numeric 來完成，例如：

```
SELECT '12.34'::float8::numeric::money;
```

但是，並不推薦這樣做。由於四捨五入誤差的可能性，不應該使用浮點數來處理貨幣。

money 型別的數值可以轉換為 numeric 而不會損失精確度。轉換為其他型別可能會失去精確性，而且還必須分兩步驟完成：

```
SELECT '52093.89'::money::numeric::float8;
```

當貨幣數值除以另一貨幣數值時，結果會是 double precision（即純數，而不是貨幣）；貨幣單位會相互抵消。

---

[^1]: [PostgreSQL: Documentation: 10: 8.2. Monetary Types](https://www.postgresql.org/docs/10/static/datatype-money.html)

