# 9.1. 邏輯運算子

常見可用的邏輯運算子：

| `AND` |
| ----- |
| `OR`  |
| `NOT` |

SQL 使用具有 true、false 和 null 的三值邏輯系統，其中 null 表示“未知”。請參閱以下真值表：

| _`a`_ | _`b`_ | _`a`_ AND _`b`_ | _`a`_ OR _`b`_ |
| ----- | ----- | --------------- | -------------- |
| TRUE  | TRUE  | TRUE            | TRUE           |
| TRUE  | FALSE | FALSE           | TRUE           |
| TRUE  | NULL  | NULL            | TRUE           |
| FALSE | FALSE | FALSE           | FALSE          |
| FALSE | NULL  | FALSE           | NULL           |
| NULL  | NULL  | NULL            | NULL           |

| _`a`_ | NOT _`a`_ |
| ----- | --------- |
| TRUE  | FALSE     |
| FALSE | TRUE      |
| NULL  | NULL      |

運算子 AND 和 OR 是可交換的，也就是說，您可以在不影響結果的情況下交換左右運算元。有關子表示式求值順序的更多資訊，請參閱[第 4.2.14 節](../sql-syntax/value-expressions.md#4-2-14-biao-shi-shi-yun-suan-gui-ze)。
