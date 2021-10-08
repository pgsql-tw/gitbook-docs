# 51.66. pg\_available\_extensions

pg\_available\_extensions 檢視表列出可以安裝的延伸功能。另請參閱 [pg\_extension](pg_extension.md) 系統目錄，該目錄顯示了目前已安裝的延伸功能。

## **Table 51.67. `pg_available_extensions` Columns**

| Name | Type | Description |
| :--- | :--- | :--- |
| `name` | `name` | Extension name |
| `default_version` | `text` | 預設版本的名稱；如果未指定，則為 NULL |
| `installed_version` | `text` | 目前安裝的延伸功能版本，如果未安裝，則為 NULL |
| `comment` | `text` | 延伸功能的控制檔案中的註解文字內容 |

pg\_available\_extensions 檢視表是唯讀的。

