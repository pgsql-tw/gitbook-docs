# 65.2. Built-in Operator Classes

The core PostgreSQL distribution includes the SP-GiST operator classes shown in [Table 63.1](https://www.postgresql.org/docs/10/static/spgist-builtin-opclasses.html#SPGIST-BUILTIN-OPCLASSES-TABLE).

## **Table 63.1. Built-in SP-GiST Operator Classes**

| Name | Indexed Data Type | Indexable Operators |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `kd_point_ops` | `point` | `<<` `<@` `<^` `>>` `>^` `~=` |  |  |  |  |
| `quad_point_ops` | `point` | `<<` `<@` `<^` `>>` `>^` `~=` |  |  |  |  |
| `range_ops` | any range type | `&&` `&<` `&>` \`- | -```<<`` `<@` `=` `>>` `@>` |  |  |  |
| `box_ops` | `box` | `<<` `&<` `&&` `&>` `>>` `~=` `@>` `<@` \`&&lt; | \`\`&lt;&lt; |  | &gt;&gt; \`\` | &&gt;\` |
| `text_ops` | `text` | `<` `<=` `=` `>` `>=` `~<=~` `~<~` `~>=~` `~>~` |  |  |  |  |
| `inet_ops` | `inet`, `cidr` | `&&` `>>` `>>=` `>` `>=` `<>` `<<` `<<=` `<` `<=` `=` |  |  |  |  |

Of the two operator classes for type `point`, `quad_point_ops` is the default. `kd_point_ops` supports the same operators but uses a different index data structure which may offer better performance in some applications.

