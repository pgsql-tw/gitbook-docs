<a id="ECPG-DESCRIPTORS"></a>

## 34.7. 使用描述區 [#](#ecpg-descriptors) <a href="#ecpg-descriptors" id="ecpg-descriptors"></a>

[34.7.1. 具名 SQL 描述區](ecpg-named-descriptors.md#ecpg-named-descriptors)

[34.7.2. SQLDA 描述區](ecpg-sqlda-descriptors.md#ecpg-sqlda-descriptors)

SQL 描述區是處理 `SELECT`、`FETCH` 或 `DESCRIBE` 陳述式結果的一種較進階的方法。SQL 描述區會把一個資料列的資料連同中繼資料項目，一起歸入同一個資料結構中。執行動態 SQL 陳述式時，結果欄位的性質可能無法事先得知，因此中繼資料特別有用。PostgreSQL 提供兩種使用描述區的方式：具名 SQL 描述區，以及 C 結構形式的 SQLDA。

<a id="ECPG-NAMED-DESCRIPTORS"></a>

### 34.7.1. 具名 SQL 描述區 [#](#ecpg-named-descriptors) <a href="#ecpg-named-descriptors" id="ecpg-named-descriptors"></a>

本節內容請參閱[34.7.1. 具名 SQL 描述區](ecpg-named-descriptors.md#ecpg-named-descriptors)。

<a id="ECPG-SQLDA-DESCRIPTORS"></a>

### 34.7.2. SQLDA 描述區 [#](#ecpg-sqlda-descriptors) <a href="#ecpg-sqlda-descriptors" id="ecpg-sqlda-descriptors"></a>

本節內容請參閱[34.7.2. SQLDA 描述區](ecpg-sqlda-descriptors.md#ecpg-sqlda-descriptors)。

<a id="ECPG-SQLDA-DESCRIPTORS-SQLDA"></a>

### 34.7.2.1. SQLDA 資料結構 [#](#ecpg-sqlda-descriptors-sqlda) <a href="#ecpg-sqlda-descriptors-sqlda" id="ecpg-sqlda-descriptors-sqlda"></a>

本節內容請參閱[34.7.2.1. SQLDA 資料結構](ecpg-sqlda-data-structures.md#ecpg-sqlda-descriptors-sqlda)。

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-descriptors.html)（原文版本：18.6；核對日期：2026-10-23）
