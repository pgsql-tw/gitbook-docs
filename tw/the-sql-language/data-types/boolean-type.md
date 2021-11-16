# 8.6. 布林型別

PostgreSQL 支援標準 SQL 的布林型別，如 [Table 8-19](boolean-type.md#table-8-19-bu-lin-xing-bie-de-zi-liao-xing-tai-miao-shu) 所示。布林型別有幾種狀態: "true"、"false"，和第三種狀態 "unknown"，"unknown" 會用 SQL 的 null 值表示。

#### Table 8-19. 布林型別的資料型態描述

| Name    | Storage Size | Description            |
| ------- | ------------ | ---------------------- |
| boolean | 1 byte       | state of true or false |

以下的字詞都可以代表 "true" 狀態:

| TRUE   |
| ------ |
| 't'    |
| 'true' |
| 'y'    |
| 'yes'  |
| 'on'   |
| '1'    |

"false" 狀態則可以用以下的字詞表示:

| FALSE   |
| ------- |
| 'f'     |
| 'false' |
| 'n'     |
| 'no'    |
| 'off'   |
| '0'     |

開頭和結尾的空白都會被忽略，也不分大小寫。 為了符合 SQL 用法，建議使用關鍵字 "TRUE" 和 "FALSE"。

[Example 8-2](boolean-type.md#example-8-2-shi-yong-bu-lin-xing-bie) 使用字母 t 和 f，來顯示布林型別的輸出。

#### [ ](boolean-type.md#DATATYPE-BOOLEAN-EXAMPLE)Example 8-2. 使用布林型別

```
CREATE TABLE test1 (a boolean, b text);
INSERT INTO test1 VALUES (TRUE, 'sic est');
INSERT INTO test1 VALUES (FALSE, 'non est');
SELECT * FROM test1;
 a |    b
---+---------
 t | sic est
 f | non est

SELECT * FROM test1 WHERE a;
 a |    b
---+---------
 t | sic est
```
