# 5.2. 預設值

欄位可以指定一個預設值。當新的列被插入，某些欄位卻沒有指定其值時，這些欄位將會被填入相對應的預設值。資料處理的過程中，當有欄位的值不確定時，也會被設定為其預設值。（關於資料處理的詳細內容，請參閱[第 6 章](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/data-manipulation.md)。）

如果預設值並沒有明確被指定時，預設值就會是 null。一般來說空值是可接受的情況，因為空值可以表示「未知的資料」的意義。

在表格定義時，預設值接在資料型別後宣告，如下所示：

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric 
DEFAULT 9.99
);
```

預設值也可以是運算表示式，會在資料插入的同時進行運算（不是在表格建立時）。常見的例子是 timestamp 欄位，會設定一個 CURRENT\_TIMESTAMP 的預設值，使其在資料插入時設定為當下的時間。另一個例子是產生「序列數」，這在 PostgreSQL 中，通常以下列語法來表現：

```
CREATE TABLE products (
    product_no integer 
DEFAULT nextval('products_product_no_seq')
,
    ...
);
```

這裡的 nextval() 函數會從序列物件取得下一個數字（參閱 [9.16 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/functions-and-operators/916-sequence-manipulation-functions.md)）。這個例子也常簡化為：

```
CREATE TABLE products (
    product_no 
SERIAL
,
    ...
);
```

有關 SERIAL 的簡寫方式，將在 [8.1.4 節](https://github.com/pgsql-tw/documents/tree/a096b206440e1ac8cdee57e1ae7a74730f0ee146/ii-the-sql-language/data-types/81-numeric-types.md)中說明。
