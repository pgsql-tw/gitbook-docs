<a id="id-1.9.3.103.1"></a>

## DROP ACCESS METHOD

DROP ACCESS METHOD — 移除存取方法

## 語法

```

DROP ACCESS METHOD [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

<a id="id-1.9.3.103.5"></a>

## 說明

`DROP ACCESS METHOD` 移除既有存取方法。只有超級使用者可移除存取方法。

<a id="id-1.9.3.103.6"></a>

## 參數

`IF EXISTS`
:   存取方法不存在時不發生錯誤，並發出 notice。

*`name`*
:   既有存取方法的名稱。

`CASCADE`
:   自動移除依賴該存取方法的物件（例如運算子類別、運算子家族和索引），以及依賴這些物件的所有物件（請參閱[第 5.15 節](../../the-sql-language/ddl/ddl-depend.md)）。

`RESTRICT`
:   若有任何物件依賴該存取方法，拒絕移除。這是預設行為。

<a id="id-1.9.3.103.7"></a>

## 範例

移除存取方法 `heptree`：

```

DROP ACCESS METHOD heptree;
```

<a id="id-1.9.3.103.8"></a>

## 相容性

`DROP ACCESS METHOD` 是 PostgreSQL 擴充功能。

<a id="id-1.9.3.103.9"></a>

## 參閱

[CREATE ACCESS METHOD](sql-create-access-method.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-drop-access-method.html)（原文版本：18.6；核對日期：2026-09-06）
