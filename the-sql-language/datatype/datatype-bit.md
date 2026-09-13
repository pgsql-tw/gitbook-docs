<a id="DATATYPE-BIT"></a>

## 8.10. 位元字串型別 [#](#DATATYPE-BIT)

<a id="id-1.5.7.18.2"></a>

位元字串是由 1 與 0 所組成的字串。它們可以用來儲存或呈現位元遮罩。SQL 有兩種位元型別：`bit(n)` 與 `bit varying(n)`，其中 *`n`* 是正整數。

`bit` 型別的資料長度必須正好符合 *`n`*；嘗試儲存較短或較長的位元字串都會發生錯誤。`bit varying` 的資料則是可變長度，最長為 *`n`*；超過長度的字串會被拒絕。撰寫 `bit` 而不指定長度等同於 `bit(1)`，而 `bit varying` 不指定長度則表示長度不受限制。

### 注意

如果明確地將位元字串值轉換為 `bit(n)`，它會在右邊被截斷或補零，使其正好為 *`n`* 個位元，而不會引發錯誤。同樣地，如果明確地將位元字串值轉換為 `bit varying(n)`，當它超過 *`n`* 個位元時會在右邊被截斷。

關於位元字串常數的語法資訊，請參閱[第 4.1.2.5 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-BIT-STRINGS)。位元邏輯運算子與字串操作函式都可以使用；請參閱[第 9.6 節](../functions/functions-bitstring.md)。

<a id="id-1.5.7.18.7"></a>

**範例 8.3. 使用位元字串型別**

```

CREATE TABLE test (a BIT(3), b BIT VARYING(5));
INSERT INTO test VALUES (B'101', B'00');
INSERT INTO test VALUES (B'10', B'101');

ERROR:  bit string length 2 does not match type bit(3)

INSERT INTO test VALUES (B'10'::bit(3), B'101');
SELECT * FROM test;

  a  |  b
-----+-----
 101 | 00
 100 | 101
```

<br>

位元字串值每 8 個位元需要 1 個位元組，另外再加上 5 或 8 個位元組的額外開銷，視字串長度而定（但過長的值可能會被壓縮或移到行外儲存，如同[第 8.3 節](datatype-character.md)中針對字元字串所說明的）。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-bit.html)（原文版本：18.6；核對日期：2026-09-13）
