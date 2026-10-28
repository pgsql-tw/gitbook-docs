<a id="SQL-ALTEROPFAMILY"></a><a id="id-1.9.3.22.1"></a>

## ALTER OPERATOR FAMILY

ALTER OPERATOR FAMILY — 變更運算子家族的定義

<a id="id-1.9.3.22.4"></a>

## 語法

```

ALTER OPERATOR FAMILY name USING index_method ADD
  {  OPERATOR strategy_number operator_name ( op_type, op_type )
              [ FOR SEARCH | FOR ORDER BY sort_family_name ]
   | FUNCTION support_number [ ( op_type [ , op_type ] ) ]
              function_name [ ( argument_type [, ...] ) ]
  } [, ... ]

ALTER OPERATOR FAMILY name USING index_method DROP
  {  OPERATOR strategy_number ( op_type [ , op_type ] )
   | FUNCTION support_number ( op_type [ , op_type ] )
  } [, ... ]

ALTER OPERATOR FAMILY name USING index_method
    RENAME TO new_name

ALTER OPERATOR FAMILY name USING index_method
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR FAMILY name USING index_method
    SET SCHEMA new_schema
```

<a id="id-1.9.3.22.5"></a>

## 說明

`ALTER OPERATOR FAMILY` 會變更運算子家族的定義。你可以將運算子與支援函式加入家族、從家族中移除它們，或變更家族的名稱或擁有者。

以 `ALTER OPERATOR FAMILY` 將運算子與支援函式加入家族時，它們不屬於家族內任何特定的運算子類別，而只是在家族內「鬆散」存在。這表示這些運算子與函式和該家族的語意相容，但並非任何特定索引正確運作所必需。（確實為此所必需的運算子與函式，應該改為宣告為運算子類別的一部分；請參閱 [CREATE OPERATOR CLASS](sql-createopclass.md)。）PostgreSQL 允許隨時從家族中移除家族的鬆散成員，但若不移除整個類別以及相依於它的所有索引，就無法移除運算子類別的成員。通常，單一資料型別的運算子與函式屬於運算子類別，因為需要它們來支援該特定資料型別上的索引；而跨資料型別的運算子與函式則會成為家族的鬆散成員。

你必須是超級使用者才能使用 `ALTER OPERATOR FAMILY`。（之所以有此限制，是因為錯誤的運算子家族定義可能使伺服器混亂，甚至當機。）

`ALTER OPERATOR FAMILY` 目前既不檢查運算子家族定義是否包含索引方法所需的所有運算子與函式，也不檢查這些運算子與函式是否構成自我一致的集合。定義有效的運算子家族是使用者的責任。

更多資訊請參閱[第 36.16 節](../../server-programming/extend/xindex.md)。

<a id="id-1.9.3.22.6"></a>

## 參數

*`name`*
:   現有運算子家族的名稱（可選擇以綱要限定）。

*`index_method`*
:   此運算子家族所適用之索引方法的名稱。

*`strategy_number`*
:   索引方法中與該運算子家族相關聯之運算子的策略編號。

*`operator_name`*
:   與該運算子家族相關聯之運算子的名稱（可選擇以綱要限定）。

*`op_type`*

在 `OPERATOR` 子句中，為運算子的運算元資料型別，或以 `NONE` 表示前綴運算子。與 `CREATE OPERATOR CLASS` 中的類似語法不同，運算元資料型別必須一律指定。

在 `ADD FUNCTION` 子句中，為該函式要支援的運算元資料型別（若與函式的輸入資料型別不同）。對於 B-tree 比較函式與雜湊函式，不需要指定 *`op_type`*，因為函式的輸入資料型別一律就是應使用的正確型別。對於 B-tree 排序支援函式、B-Tree equal image 函式，以及 GiST、SP-GiST 與 GIN 運算子類別中的所有函式，則必須指定該函式要搭配使用的運算元資料型別。

在 `DROP FUNCTION` 子句中，必須指定該函式要支援的運算元資料型別。

*`sort_family_name`*

現有 `btree` 運算子家族的名稱（可選擇以綱要限定），該家族描述與排序運算子相關聯的排序順序。

若既未指定 `FOR SEARCH`，也未指定 `FOR ORDER BY`，則預設為 `FOR SEARCH`。

*`support_number`*
:   索引方法中與該運算子家族相關聯之函式的支援函式編號。

*`function_name`*
:   作為該運算子家族索引方法支援函式之函式的名稱（可選擇以綱要限定）。若未指定引數清單，該名稱在其綱要中必須是唯一的。

*`argument_type`*
:   函式的參數資料型別。

*`new_name`*
:   運算子家族的新名稱。

*`new_owner`*
:   運算子家族的新擁有者。

*`new_schema`*
:   運算子家族的新綱要。

`OPERATOR` 與 `FUNCTION` 子句可以任意順序出現。

<a id="id-1.9.3.22.7"></a>

## 注意事項

請注意，`DROP` 語法只透過策略編號或支援編號以及輸入資料型別，來指定運算子家族中的「槽位」，並不提及佔用該槽位之運算子或函式的名稱。此外，對於 `DROP FUNCTION`，要指定的型別是該函式要支援的輸入資料型別；對於 GiST、SP-GiST 與 GIN 索引，這可能與函式實際的輸入引數型別毫無關係。

由於索引機制在使用函式前不會檢查函式的存取權限，將函式或運算子納入運算子家族，等同於授予它公開的執行權限。對於在運算子家族中有用的那類函式而言，這通常不是問題。

運算子不應該由 SQL 函式定義。SQL 函式很可能會被內嵌到呼叫它的查詢中，這會使最佳化器無法辨識該查詢符合某個索引。

<a id="id-1.9.3.22.8"></a>

## 範例

以下範例命令將跨資料型別的運算子與支援函式，加入一個已包含資料型別 `int4` 與 `int2` 之 B-tree 運算子類別的運算子家族。

```

ALTER OPERATOR FAMILY integer_ops USING btree ADD

  -- int4 vs int2
  OPERATOR 1 < (int4, int2) ,
  OPERATOR 2 <= (int4, int2) ,
  OPERATOR 3 = (int4, int2) ,
  OPERATOR 4 >= (int4, int2) ,
  OPERATOR 5 > (int4, int2) ,
  FUNCTION 1 btint42cmp(int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 < (int2, int4) ,
  OPERATOR 2 <= (int2, int4) ,
  OPERATOR 3 = (int2, int4) ,
  OPERATOR 4 >= (int2, int4) ,
  OPERATOR 5 > (int2, int4) ,
  FUNCTION 1 btint24cmp(int2, int4) ;
```

若要再次移除這些項目：

```

ALTER OPERATOR FAMILY integer_ops USING btree DROP

  -- int4 vs int2
  OPERATOR 1 (int4, int2) ,
  OPERATOR 2 (int4, int2) ,
  OPERATOR 3 (int4, int2) ,
  OPERATOR 4 (int4, int2) ,
  OPERATOR 5 (int4, int2) ,
  FUNCTION 1 (int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 (int2, int4) ,
  OPERATOR 2 (int2, int4) ,
  OPERATOR 3 (int2, int4) ,
  OPERATOR 4 (int2, int4) ,
  OPERATOR 5 (int2, int4) ,
  FUNCTION 1 (int2, int4) ;
```

<a id="id-1.9.3.22.9"></a>

## 相容性

SQL 標準中沒有 `ALTER OPERATOR FAMILY` 陳述式。

<a id="id-1.9.3.22.10"></a>

## 另請參閱

[CREATE OPERATOR FAMILY](sql-createopfamily.md), [DROP OPERATOR FAMILY](sql-dropopfamily.md), [CREATE OPERATOR CLASS](sql-createopclass.md), [ALTER OPERATOR CLASS](sql-alteropclass.md), [DROP OPERATOR CLASS](sql-dropopclass.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-alteropfamily.html)（原文版本：18.6；核對日期：2026-10-09）
