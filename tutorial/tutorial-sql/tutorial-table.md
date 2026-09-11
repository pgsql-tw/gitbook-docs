<a id="TUTORIAL-TABLE"></a>

## 2.3. 建立新資料表 [#](#TUTORIAL-TABLE)

<a id="id-1.4.4.4.2"></a>

你可以指定資料表名稱以及所有欄位的名稱與型別，來建立新的資料表：

```

CREATE TABLE weather (
    city            varchar(80),
    temp_lo         int,           -- low temperature
    temp_hi         int,           -- high temperature
    prcp            real,          -- precipitation
    date            date
);
```

你可以把這段指令連同換行一起輸入到 `psql` 中。`psql` 會辨識出指令要到分號才結束。

SQL 指令中可以自由使用空白字元（也就是空格、定位字元與換行）。這表示你可以用與上面不同的方式對齊指令，甚至全部寫在同一行。兩個連字號（「`--`」）表示註解的開始，其後直到行尾的內容都會被忽略。SQL 的關鍵字與識別字不區分大小寫，除非識別字以雙引號括住以保留大小寫（上例並未如此）。

`varchar(80)` 指定一種資料型別，可儲存長度最多 80 個字元的任意字串。`int` 是一般的整數型別。`real` 是用來儲存單精度浮點數的型別。`date` 的意思應該不言自明。（沒錯，型別為 `date` 的欄位也命名為 `date`。這可能很方便，也可能令人混淆，由你決定。）

PostgreSQL 支援標準 SQL 型別 `int`, `smallint`, `real`, `double
precision`, `char(N)`,
`varchar(N)`, `date`, `time`, `timestamp` 與 `interval`，以及其他通用型別和豐富的幾何型別。PostgreSQL 可以依需要加入任意數量的使用者自訂資料型別。因此，除了為支援 SQL 標準中的特殊情況而必要之處以外，型別名稱在語法中都不是關鍵字。

第二個範例會儲存城市及其對應的地理位置：

```

CREATE TABLE cities (
    name            varchar(80),
    location        point
);
```

`point` 型別是 PostgreSQL 特有資料型別的一個例子。

<a id="id-1.4.4.4.8.1"></a>
最後要提的是，如果你不再需要某個資料表，或想以不同方式重新建立它，可以使用下列指令將它移除：

```

DROP TABLE tablename;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-table.html)（原文版本：18.6；核對日期：2026-09-11）
