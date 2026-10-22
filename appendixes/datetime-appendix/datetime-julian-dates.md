<a id="DATETIME-JULIAN-DATES"></a>

## B.7. 儒略日期 [#](#DATETIME-JULIAN-DATES)

<a id="id-1.11.3.10.2"></a>

*儒略日期*（Julian Date）系統是一種
為日子編號的方法。它
與儒略曆無關，雖然它的名稱容易令人混淆，
與該曆法相似。
儒略日期系統由法國學者
約瑟夫·尤斯圖斯·斯卡利傑（Joseph Justus Scaliger，1540–1609）
發明，其名稱可能取自斯卡利傑的父親，
義大利學者尤利烏斯·凱撒·斯卡利傑（Julius Caesar Scaliger，1484–1558）。

在儒略日期系統中，每一天都有一個連續的編號，從
JD 0 開始（JD 0 有時被稱為*那個*儒略日期）。
JD 0 對應儒略曆的西元前 4713 年 1 月 1 日，或
格里曆的西元前 4714 年 11 月 24 日。儒略日期計數
最常由天文學家用來標記夜間觀測，
因此一個日期是從 UTC 正午持續到下一個 UTC 正午，而不是
從午夜到午夜：JD 0 表示從西元前 4714 年 11 月 24 日
UTC 正午到西元前 4714 年 11 月 25 日 UTC 正午的 24 小時。

雖然 PostgreSQL 支援以儒略日期表示法
輸入與輸出日期（而且在某些內部
日期時間計算中也使用儒略日期），但它並未遵循
日期從正午到正午這項細節。PostgreSQL 將儒略日期
視為從當地午夜持續到當地午夜，與一般
日期相同。

不過，當你需要天文學上的定義時，此定義也提供了
取得的方法：在時區 `UTC+12` 中進行
運算。例如：

```

=> SELECT extract(julian from '2021-06-23 7:00:00-04'::timestamptz at time zone 'UTC+12');
           extract
------------------------------
 2459388.95833333333333333333
(1 row)
=> SELECT extract(julian from '2021-06-23 8:00:00-04'::timestamptz at time zone 'UTC+12');
               extract
--------------------------------------
 2459389.0000000000000000000000000000
(1 row)
=> SELECT extract(julian from date '2021-06-23');
 extract
---------
 2459389
(1 row)
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datetime-julian-dates.html)（原文版本：18.6；核對日期：2026-10-22）
