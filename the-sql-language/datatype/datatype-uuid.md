<a id="DATATYPE-UUID"></a>

## 8.12. UUID 型別 [#](#DATATYPE-UUID)

<a id="id-1.5.7.20.2"></a>

資料型別 `uuid` 用來儲存由 [RFC 9562](https://datatracker.ietf.org/doc/html/rfc9562)、ISO/IEC 9834-8:2005 以及相關標準所定義的通用唯一識別碼（Universally Unique Identifiers，UUID）。（有些系統改稱這個資料型別為全域唯一識別碼，或稱 GUID。<a id="id-1.5.7.20.3.3"></a>）這個識別碼是一個 128 位元的數值，由一套演算法產生，該演算法的選擇使得在已知的宇宙中，其他任何人使用相同演算法產生出相同識別碼的機率極低。因此對於分散式系統而言，這些識別碼提供的唯一性保證優於序列（sequence）產生器，因為後者只在單一資料庫內具有唯一性。

RFC 9562 定義了 8 種不同的 UUID 版本。每個版本對於產生新的 UUID 值都有特定的要求，而且各有其優缺點。PostgreSQL 原生支援使用 UUIDv4 與 UUIDv7 演算法產生 UUID。此外，UUID 值也可以在資料庫外部以任何演算法產生。資料型別 `uuid` 可用來儲存任何 UUID，不論其來源與 UUID 版本為何。

UUID 寫成一串小寫的十六進位數字，分成數個以連字號分隔的群組，具體來說是一組 8 位數字，後面接著三組 4 位數字，最後再接一組 12 位數字，總共 32 位數字來表示這 128 個位元。以這種標準形式表示的 UUID 範例如下：

```

a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
```

PostgreSQL 在輸入時也接受下列替代形式：使用大寫的十六進位數字、標準格式外面加上大括號、省略部分或全部的連字號、在任何一組四位數字之後加上連字號。範例如下：

```

A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11
{a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11}
a0eebc999c0b4ef8bb6d6bb9bd380a11
a0ee-bc99-9c0b-4ef8-bb6d-6bb9-bd38-0a11
{a0eebc99-9c0b4ef8-bb6d6bb9-bd380a11}
```

輸出一律採用標準形式。

關於如何在 PostgreSQL 中產生 UUID，請參閱[第 9.14 節](../functions/functions-uuid.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-uuid.html)（原文版本：18.6；核對日期：2026-09-13）
