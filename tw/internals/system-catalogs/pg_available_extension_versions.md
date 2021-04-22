# 51.67. pg\_available\_extension\_versions

pg\_available\_extension\_versions 檢視圖列出可用於安裝的特定延伸功能版本。另請參閱 [pg\_extension](pg_extension.md) 目錄，該目錄列出了目前已安裝的延伸功能。

## **Table 51.68. `pg_available_extension_versions` Columns**

| Name | Type | Description |
| :--- | :--- | :--- |
| `name` | `name` | 延伸功能名稱 |
| `version` | `text` | 版本名稱 |
| `installed` | `bool` | 如果目前已安裝此延伸功能的此版本，則為 True |
| `superuser` | `bool` | 如果僅允許超級使用者安裝此延伸功能，則為 True |
| `relocatable` | `bool` | 如果延伸功能可以接受重新定位到另一個綱要，則為 True |
| `schema` | `name` | 延伸功能必須安裝到的綱要名稱，如果可部分或完全重新定位，則為 NULL |
| `requires` | `name[]` | 必須預先安裝的延伸功能名稱，如果沒有則為 NULL |
| `comment` | `text` | 延伸功能控制檔案中的註解文字內容 |

pg\_available\_extension\_versions 檢視表是唯讀的。

