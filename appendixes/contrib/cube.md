<a id="CUBE"></a>

## F.10. cube — 多維 cube 資料型別 [#](#cube) <a href="#cube" id="cube"></a>

[F.10.1. 語法](cube/cube-syntax.md#cube-syntax)

[F.10.2. 精確度](cube.md#cube-precision)

[F.10.3. 用法](cube/cube-usage.md#cube-usage)

[F.10.4. 預設值](cube.md#cube-defaults)

[F.10.5. 注意事項](cube.md#cube-notes)

[F.10.6. 致謝](cube.md#cube-credits)

<a id="id-1.11.7.20.2"></a>

此模組實作 `cube` 資料型別，用來表示多維 cube。

此模組視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非 superuser 也可
安裝它。

### F.10.1. 語法 [#](#cube-syntax) <a href="#cube-syntax" id="cube-syntax"></a>

完整內容請見 [F.10.1. 語法](cube/cube-syntax.md#cube-syntax)。

<a id="CUBE-PRECISION"></a>

### F.10.2. 精確度 [#](#cube-precision) <a href="#cube-precision" id="cube-precision"></a>

值在內部以 64 位元浮點數儲存。因此，具有超過約 16 位有效數字的數值會被截斷。

### F.10.3. 用法 [#](#cube-usage) <a href="#cube-usage" id="cube-usage"></a>

完整內容請見 [F.10.3. 用法](cube/cube-usage.md#cube-usage)。

<a id="CUBE-DEFAULTS"></a>

### F.10.4. 預設值 [#](#cube-defaults) <a href="#cube-defaults" id="cube-defaults"></a>

下列聯集：

```

select cube_union('(0,5,2),(2,3,1)', '0');
cube_union
-------------------
(0, 0, 0),(2, 5, 2)
(1 row)
```

符合直覺；下列交集也同樣如此：

```

select cube_inter('(0,-1),(1,1)', '(-2),(2)');
cube_inter
-------------
(0, 0),(1, 0)
(1 row)
```

對於維度不同的 cube 執行所有二元運算時，會將維度較低者視為笛卡兒投影，
亦即字串表示法中省略的座標位置為零。以上範例等同於：

```

cube_union('(0,5,2),(2,3,1)','(0,0,0),(0,0,0)');
cube_inter('(0,-1),(1,1)','(-2,0),(2,0)');
```

下列包含述詞使用點的語法，而第二個引數實際上在內部表示為方框。此語法使得
無須為 (box, point) 述詞另行定義點型別與函式。

```

select cube_contains('(0,0),(1,1)', '0.5,0.5');
cube_contains
--------------
t
(1 row)
```

<a id="CUBE-NOTES"></a>

### F.10.5. 注意事項 [#](#cube-notes) <a href="#cube-notes" id="cube-notes"></a>

用法範例請參閱回歸測試 `sql/cube.sql`。

為了降低不慎破壞的可能性，cube 的維度數上限為 100。若需要更大的上限，可在
`cubedata.h` 設定。

<a id="CUBE-CREDITS"></a>

### F.10.6. 致謝 [#](#cube-credits) <a href="#cube-credits" id="cube-credits"></a>

原作者：Gene Selkov, Jr. `<selkovjr@mcs.anl.gov>`，Argonne National Laboratory
數學與電腦科學部門。

我主要感謝 Joe Hellerstein 教授（<https://dsf.berkeley.edu/jmh/>）闡明 GiST
（<http://gist.cs.berkeley.edu/>）的要旨，以及其前學生 Andy Dong 為 Illustra
撰寫的範例。我也感謝所有現任及過去的 Postgres 開發者，讓我得以創造並安居
於自己的世界。並感謝 Argonne Lab 與 U.S. Department of Energy 多年來對我
資料庫研究的持續支持。

Bruno Wolff III `<bruno@wolff.to>` 在 2002 年 8／9 月對此套件進行小幅更新，
包括將精確度從單精度改為雙精度，並新增一些函式。

Joshua Reich `<josh@root.net>` 在 2006 年 7 月進行額外更新，包括
`cube(float8[], float8[])`，以及清理程式碼以改用 V1 呼叫協定，而非已棄用的
V0 協定。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/cube.html)
