<a id="DOMAINS"></a>

## 8.18. 網域型別 [#](#DOMAINS)

<a id="id-1.5.7.26.2"></a><a id="id-1.5.7.26.3"></a>

*網域*（domain）是一種以另一個*基礎型別*（underlying type）為基礎的使用者定義資料型別。它還可以選擇性地帶有限制條件，把它的有效值限定在基礎型別所允許範圍的一個子集合中。除此之外，它的行為就跟基礎型別一樣 — 舉例來說，任何可以套用在基礎型別上的運算子或函式，都可以在這個網域型別上運作。基礎型別可以是任何內建或使用者定義的基本型別、列舉型別、陣列型別、複合型別、範圍型別，或是另一個網域。

例如，我們可以在整數之上建立一個只接受正整數的網域：

```

CREATE DOMAIN posint AS integer CHECK (VALUE > 0);
CREATE TABLE mytable (id posint);
INSERT INTO mytable VALUES(1);   -- works
INSERT INTO mytable VALUES(-1);  -- fails
```

當基礎型別的運算子或函式被套用到網域值時，這個網域會自動向下轉型（down-cast）為基礎型別。因此，舉例來說，`mytable.id - 1` 的結果會被視為 `integer` 型別，而不是 `posint`。我們可以寫成 `(mytable.id - 1)::posint`，把結果轉換回 `posint`，這會使得網域的限制條件被重新檢查。在這個例子中，如果這個運算式是套用在值為 1 的 `id` 上，就會產生錯誤。將基礎型別的值指派給網域型別的欄位或變數時，不需要寫明確的型別轉換，但網域的限制條件仍會被檢查。

更多資訊請參閱 [CREATE DOMAIN](../../reference/sql-commands/sql-createdomain.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/domains.html)（原文版本：18.6；核對日期：2026-09-13）
