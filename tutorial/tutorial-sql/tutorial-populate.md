<a id="TUTORIAL-POPULATE"></a>

## 2.4. 將資料列加入資料表 [#](#TUTORIAL-POPULATE)

<a id="id-1.4.4.5.2"></a>

`INSERT` 陳述式用來將資料列新增到資料表中：

```

INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');
```

請注意，所有資料型別都使用相當直觀的輸入格式。不是單純數值的常數通常必須以單引號（`'`）括住，如範例所示。`date` 型別實際上能接受相當多樣的格式，但在本教學中，我們會使用這裡所示、不會產生歧義的格式。

`point` 型別需要以一組座標作為輸入，如下所示：

```

INSERT INTO cities VALUES ('San Francisco', '(-194.0, 53.0)');
```

目前使用的語法要求你記住欄位的順序。另一種語法可以讓你明確列出欄位：

```

INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
    VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');
```

如果你願意，可以用不同的順序列出欄位，甚至省略部分欄位，例如降雨量未知時：

```

INSERT INTO weather (date, city, temp_hi, temp_lo)
    VALUES ('1994-11-29', 'Hayward', 54, 37);
```

許多開發人員認為，明確列出欄位是比依賴隱含順序更好的寫法。

請輸入上面列出的所有指令，讓後續各節有資料可以使用。

<a id="id-1.4.4.5.7.1"></a>
你也可以使用 `COPY` 從純文字檔載入大量資料。這通常比較快，因為 `COPY` 指令是針對這種用途最佳化的，但彈性不如 `INSERT`。範例如下：

```

COPY weather FROM '/home/user/weather.txt';
```

其中來源檔案的檔名必須在執行後端程序的機器上可以存取，而不是在用戶端上，因為檔案是由後端程序直接讀取。上面插入 weather 資料表的資料，也可以從包含下列內容的檔案匯入（各值以定位字元分隔）：

```

San Francisco    46    50    0.25    1994-11-27
San Francisco    43    57    0.0    1994-11-29
Hayward    37    54    \N    1994-11-29
```

你可以在 [COPY](../../reference/sql-commands/sql-copy.md) 中進一步瞭解 `COPY` 指令。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-populate.html)（原文版本：18.6；核對日期：2026-09-11）
