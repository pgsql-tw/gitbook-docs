# 11.10. 索引與排序規則

每個索引欄位只能支援一個排序規則（Collation）。 如果感興趣多個排序規則，則可能需要多個索引。

看看以下語法：

```text
CREATE TABLE test1c (
    id integer,
    content varchar COLLATE "x"
);

CREATE INDEX test1c_content_index ON test1c (content);
```

索引自動使用基礎欄位的排序規則。所以這樣的查詢形式

```text
SELECT * FROM test1c WHERE content > constant;
```

會使用這個索引，因為預設情況下比較將使用欄位的排序規則。但是，此索引無法加速涉及其他一些排序規則的查詢。所以，如果是像這樣的查詢，比方說，

```text
SELECT * FROM test1c WHERE content > constant COLLATE "y";
```

也是有意義的，可以建立一個支援「y」排序規則的附加索引，如下所示：

```text
CREATE INDEX test1c_content_y_index ON test1c (content COLLATE "y");
```

