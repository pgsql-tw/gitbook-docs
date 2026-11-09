<a id="EXTEND-TYPE-SYSTEM"></a>
## 36.2. PostgreSQL 型別系統 [#](#extend-type-system) <a href="#extend-type-system" id="extend-type-system"></a>

[36.2.1. 基礎型別](extend-type-system.md#extend-type-system-base)

[36.2.2. 容器型別](extend-type-system.md#extend-type-system-container)

[36.2.3. 網域](extend-type-system.md#extend-type-system-domains)

[36.2.4. 虛擬型別](extend-type-system.md#extend-type-system-pseudo)

[36.2.5. 多型型別](extend-type-system/extend-types-polymorphic.md#extend-types-polymorphic)

<a id="id-1.8.3.5.2"></a><a id="id-1.8.3.5.3"></a><a id="id-1.8.3.5.4"></a><a id="id-1.8.3.5.5"></a><a id="id-1.8.3.5.6"></a><a id="id-1.8.3.5.7"></a>

PostgreSQL 的資料型別可以分為基礎
型別、容器型別、網域與虛擬型別。

<a id="EXTEND-TYPE-SYSTEM-BASE"></a>

### 36.2.1. 基礎型別 [#](#extend-type-system-base) <a href="#extend-type-system-base" id="extend-type-system-base"></a>

基礎型別是指像 `integer` 這樣，在
SQL 語言層級之下實作的型別
（通常以 C 之類的低階語言撰寫）。它們大致對應於一般所稱的抽象資料型別。
PostgreSQL 只能透過使用者所提供的函式來操作這類
型別，並且僅在使用者已對其行為做出描述的範圍內，才能理解這類型別的行為。
內建的基礎型別說明於[第 8 章](../../the-sql-language/datatype/README.md)。

列舉（enum）型別可視為基礎型別的一個子類別。主要
差異在於，它們可以只用 SQL 命令建立，而不需要任何低階程式設計。
詳情請參閱[8.7 節](../../the-sql-language/datatype/datatype-enum.md)。

<a id="EXTEND-TYPE-SYSTEM-CONTAINER"></a>

### 36.2.2. 容器型別 [#](#extend-type-system-container) <a href="#extend-type-system-container" id="extend-type-system-container"></a>

PostgreSQL 有三種「容器」
型別，也就是包含其他型別多個值的型別。這三種分別是陣列、複合型別與範圍型別。

陣列可以保存多個值，這些值都屬於同一種型別。系統會為每一種基礎型別、複合
型別、範圍型別與網域型別自動建立對應的陣列型別。但並不存在陣列的陣列。就
型別系統而言，多維陣列與一維陣列並無不同。詳情請參閱[8.15 節](../../the-sql-language/datatype/arrays.md)。

複合型別（或稱資料列型別），會在使用者
建立資料表時一併建立。也可以使用 [CREATE TYPE](../../reference/sql-commands/sql-createtype.md)
來定義一個沒有關聯資料表的「獨立」複合型別。複合型別
就是一份帶有相應欄位名稱的型別清單。複合型別的值，即為一組欄位值所組成的資料列或
紀錄。詳情請參閱[8.16 節](../../the-sql-language/datatype/rowtypes.md)。

範圍型別可以保存兩個相同型別的值，分別是該範圍的下界
與上界。範圍型別是由使用者建立的，不過也存在少數幾種內建的範圍型別。詳情請參閱[8.17 節](../../the-sql-language/datatype/rangetypes.md)。

<a id="EXTEND-TYPE-SYSTEM-DOMAINS"></a>

### 36.2.3. 網域 [#](#extend-type-system-domains) <a href="#extend-type-system-domains" id="extend-type-system-domains"></a>

網域是以某個特定的底層型別為基礎，並且在許多用途上，都可以與其底層型別
互換使用。不過，網域可以帶有限制條件，將其有效值限縮為底層
型別所允許範圍的一個子集。網域是使用
SQL 命令 [CREATE DOMAIN](../../reference/sql-commands/sql-createdomain.md) 建立的。
詳情請參閱[8.18 節](../../the-sql-language/datatype/domains.md)。

<a id="EXTEND-TYPE-SYSTEM-PSEUDO"></a>

### 36.2.4. 虛擬型別 [#](#extend-type-system-pseudo) <a href="#extend-type-system-pseudo" id="extend-type-system-pseudo"></a>

有少數幾種特殊用途的「虛擬型別」。
虛擬型別不能作為資料表的欄位，或容器型別的組成部分，但可以用來宣告函式的
引數與結果型別。這在型別系統中提供了一種機制，用以識別特殊
類別的函式。[表 8.27](../../the-sql-language/datatype/datatype-pseudo.md#datatype-pseudo-table) 列出了現有的
虛擬型別。

### 36.2.5. 多型型別 [#](#extend-types-polymorphic) <a href="#extend-types-polymorphic" id="extend-types-polymorphic"></a>

完整內容請見 [36.2.5. 多型型別](extend-type-system/extend-types-polymorphic.md#extend-types-polymorphic)。


---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/extend-type-system.html)（原文版本：18.6；核對日期：2026-09-16）
