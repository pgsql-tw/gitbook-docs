# Summary

* [PostgreSQL台灣使用者社群](https://postgresql.tw)
* [簡介](README.md)
* [前言](preface.md)
  * [1. 什麼是PostgreSQL？](what-is-postgresql.md)
  * [2. PostgreSQL沿革](a-brief-history-of-postgresql.md)
  * [3. 慣例](conventions.md)
  * [4. 其他參考資訊](further-information.md)
  * [5. 問題回報指南](bug-reporting-guidelines.md)
* [I. 新手教學](i-tutorial.md)
  * [1. 入門指南](getting-started.md)
    * [1.1. 安裝](getting-started/11-installation.md)
    * [1.2. 基礎架構](getting-started/12-architectural-fundamentals.md)
    * [1.3. 建立一個資料庫](getting-started/13-creating-a-database.md)
    * [1.4. 存取一個資料庫](getting-started/14-accessing-a-database.md)
  * [2. SQL查詢語言](the-sql-language.md)
    * [2.1. 簡介](the-sql-language/21-introduction.md)
    * [2.2. 概念](the-sql-language/22-concepts.md)
    * [2.3. 創建一個新的表格](the-sql-language/23-creating-a-new-table.md)
    * [2.4. 列是表格的組成單位](the-sql-language/24-populating-a-table-with-rows.md)
    * [2.5. 表格的查詢](the-sql-language/25-querying-a-table.md)
    * [2.6. 交叉查詢](the-sql-language/26-joins-between-tables.md)
    * [2.7. 彙總查詢](the-sql-language/27-aggregate-functions.md)
    * [2.8. 更新資料](the-sql-language/28-updates.md)
    * [2.9. 刪除資料](the-sql-language/29-deletions.md)
  * [3. 先進功能](advanced-features.md)
    * [3.1. 簡介](advanced-features/31-introduction.md)
    * [3.2. Views](advanced-features/32-views.md)
    * [3.3. 外部索引鍵](advanced-features/33-foreign-keys.md)
    * [3.4. 交易安全](advanced-features/34-transactions.md)
    * [3.5. 窗函數](advanced-features/35-window-functions.md)
    * [3.6. 繼承](advanced-features/36-inheritance.md)
    * [3.7. 結論](advanced-features/37-conclusion.md)
* [II. SQL查詢語言](ii-the-sql-language.md)
  * [4. SQL語法](ii-the-sql-language/sql-syntax.md)
    * [4.1. 語法結構](ii-the-sql-language/sql-syntax/41-lexical-structure.md)
    * [4.2. 參數表示式](ii-the-sql-language/sql-syntax/42-value-expressions.md)
    * [4.3. 函數呼叫](ii-the-sql-language/sql-syntax/43-calling-functions.md)
  * [5. 定義資料結構](ii-the-sql-language/data-definition.md)
    * [5.1. 認識表格](ii-the-sql-language/data-definition/51-table-basics.md)
    * [5.2. 預設值](ii-the-sql-language/data-definition/52-default-values.md)
    * [5.3. 限制條件](ii-the-sql-language/data-definition/53-constraints.md)
    * [5.4. 系統欄位](ii-the-sql-language/data-definition/54-system-columns.md)
    * [5.5. 表格變更](ii-the-sql-language/data-definition/55-modifying-tables.md)
    * [5.6. 權限](ii-the-sql-language/data-definition/56-privileges.md)
    * [5.7. 資料列安全原則](ii-the-sql-language/data-definition/57-row-security-policies.md)
    * [5.8. Schemas](ii-the-sql-language/data-definition/58-schemas.md)
    * [5.9. 繼承](ii-the-sql-language/data-definition/59-inheritance.md)
    * [5.10. 分割資料表](ii-the-sql-language/data-definition/510-table-partitioning.md)
    * [5.11. 外部資料](ii-the-sql-language/data-definition/511-foreign-data.md)
    * [5.12. 其他資料庫物件](ii-the-sql-language/data-definition/512-other-database-objects.md)
    * [5.13. 相依性追蹤](ii-the-sql-language/data-definition/513-dependency-tracking.md)
  * [6. 資料處理](ii-the-sql-language/data-manipulation.md)
    * [6.1. 新增資料](ii-the-sql-language/data-manipulation/61-inserting-data.md)
    * [6.2. 更新資料](ii-the-sql-language/data-manipulation/62-updating-data.md)
    * [6.3. 刪除資料](ii-the-sql-language/data-manipulation/63-deleting-data.md)
    * [6.4. 修改並回傳資料](ii-the-sql-language/data-manipulation/64-returning-data-from-modified-rows.md)
  * [7. 資料查詢](ii-the-sql-language/queries.md)
    * [7.1. 概觀](ii-the-sql-language/queries/71-overview.md)
    * [7.2. 資料表表示式](ii-the-sql-language/queries/72-table-expressions.md)
    * [7.3. 取得資料列表](ii-the-sql-language/queries/73-select-lists.md)
    * [7.4. 合併查詢結果](ii-the-sql-language/queries/74-combining-queries.md)
    * [7.5. 資料排序](ii-the-sql-language/queries/75-sorting-rows.md)
    * [7.6. 指定資料範圍](ii-the-sql-language/queries/76-limit-and-offset.md)
    * [7.7. 列舉資料](ii-the-sql-language/queries/77-values-lists.md)
    * [7.8. 遞迴查詢](ii-the-sql-language/queries/78-with-queries-common-table-expressions.md)
  * [8. 資料型別](ii-the-sql-language/data-types.md)
    * [8.1. 數字型別](ii-the-sql-language/data-types/81-numeric-types.md)
    * [8.2. 貨幣型別](ii-the-sql-language/data-types/82-monetary-types.md)
    * [8.3. 文字型別](ii-the-sql-language/data-types/83-character-types.md)
    * [8.4. 位元組型別](ii-the-sql-language/data-types/84-binary-data-types.md)
    * [8.5. 日期時間型別](ii-the-sql-language/data-types/85-datetime-types.md)
    * [8.6. 布林型別](ii-the-sql-language/data-types/86-boolean-type.md)
    * [8.7. 列舉型別](ii-the-sql-language/data-types/87-enumerated-types.md)
    * [8.8. 地理資訊型別](ii-the-sql-language/data-types/88-geometric-types.md)
    * [8.9. 網路資訊型別](ii-the-sql-language/data-types/89-network-address-types.md)
    * [8.10. 位元字串型別](ii-the-sql-language/data-types/810-bit-string-types.md)
    * [8.11. 全文檢索型別](ii-the-sql-language/data-types/811-text-search-types.md)
    * [8.12. UUID型別](ii-the-sql-language/data-types/812-uuid-type.md)
    * [8.13. XML型別](ii-the-sql-language/data-types/813-xml-type.md)
    * [8.14. JSON型別](ii-the-sql-language/data-types/814-json-types.md)
    * [8.15. 陣列](ii-the-sql-language/data-types/815-arrays.md)
    * [8.16. 複合型別](ii-the-sql-language/data-types/816-composite-types.md)
    * [8.17. 範圍型別](ii-the-sql-language/data-types/817-range-types.md)
    * [8.18. 指標型別](ii-the-sql-language/data-types/818-object-identifier-types.md)
    * [8.19. pg\_lsn型別](ii-the-sql-language/data-types/819-pglsn-type.md)
    * [8.20. 概念型別](ii-the-sql-language/data-types/820-pseudo-types.md)
  * [9. 函式及運算子](ii-the-sql-language/functions-and-operators.md)
    * [9.1. 邏輯運算子](ii-the-sql-language/functions-and-operators/91-logical-operators.md)
    * [9.2. 比較函式及運算子](ii-the-sql-language/functions-and-operators/92-comparison-functions-and-operators.md)
    * [9.3. 數學函式及運算子](ii-the-sql-language/functions-and-operators/93-mathematical-functions-and-operators.md)
    * [9.4. 字串函式及運算子](ii-the-sql-language/functions-and-operators/94-string-functions-and-operators.md)
    * [9.5. 位元字串函式及運算子](ii-the-sql-language/functions-and-operators/95-binary-string-functions-and-operators.md)
    * [9.6. 二元字串函式及運算子](ii-the-sql-language/functions-and-operators/96-bit-string-functions-and-operators.md)
    * [9.7. 特徵比對](ii-the-sql-language/functions-and-operators/97-pattern-matching.md)
    * [9.8. 型別轉換函式](ii-the-sql-language/functions-and-operators/98-data-type-formatting-functions.md)
    * [9.9 日期時間函式及運算子](ii-the-sql-language/functions-and-operators/99-datetime-functions-and-operators.md)
    * [9.10. 列舉型別函式](ii-the-sql-language/functions-and-operators/910-enum-support-functions.md)
    * [9.11. 地理資訊函式及運算子](ii-the-sql-language/functions-and-operators/911-geometric-functions-and-operators.md)
    * [9.12. 網路位址函式及運算子](ii-the-sql-language/functions-and-operators/912-network-address-functions-and-operators.md)
    * [9.13. 文字檢索函式及運算子](ii-the-sql-language/functions-and-operators/913-text-search-functions-and-operators.md)
    * [9.14. XML函式](ii-the-sql-language/functions-and-operators/914-xml-functions.md)
    * [9.15. JSON函式及運算子](ii-the-sql-language/functions-and-operators/915-json-functions-and-operators.md)
    * [9.16. 序列函式](ii-the-sql-language/functions-and-operators/916-sequence-manipulation-functions.md)
    * [9.17. 條件表示式](ii-the-sql-language/functions-and-operators/917-conditional-expressions.md)
    * [9.18. 陣列函式及運算子](ii-the-sql-language/functions-and-operators/918-array-functions-and-operators.md)
    * [9.19. 範圍函式及運算子](ii-the-sql-language/functions-and-operators/919-range-functions-and-operators.md)
    * [9.20. 彙總函式](ii-the-sql-language/functions-and-operators/920-aggregate-functions.md)
    * [9.21. Window函式](ii-the-sql-language/functions-and-operators/921-window-functions.md)
    * [9.22. 子查詢](ii-the-sql-language/functions-and-operators/922-subquery-expressions.md)
    * [9.23. 列與陣列的差異](ii-the-sql-language/functions-and-operators/923-row-and-array-comparisons.md)
    * [9.24. 集合回傳函式](ii-the-sql-language/functions-and-operators/924-set-returning-functions.md)
    * [9.25. 系統資訊函式](ii-the-sql-language/functions-and-operators/925-system-information-functions.md)
    * [9.26. 系統管理函式](ii-the-sql-language/functions-and-operators/926-system-administration-functions.md)
    * [9.27. 觸發函式](ii-the-sql-language/functions-and-operators/927-trigger-functions.md)
    * [9.28. 事件觸發函式](ii-the-sql-language/functions-and-operators/928-event-trigger-function.md)
  * [10. 型別轉換](ii-the-sql-language/type-conversion.md)
    * [10.1. 概觀](ii-the-sql-language/type-conversion/101-overview.md)
    * [10.2. 運算子](ii-the-sql-language/type-conversion/102-operators.md)
    * [10.3. 函式](ii-the-sql-language/type-conversion/103-functions.md)
    * [10.4. 儲存轉換規則](ii-the-sql-language/type-conversion/104-value-storage.md)
    * [10.5. UNION、CASE等相關操作](ii-the-sql-language/type-conversion/105-union-case-and-related-constructs.md)
    * [10.6. SELECT輸出規則](ii-the-sql-language/type-conversion/106-select-output-columns.md)
  * [11. 索引](ii-the-sql-language/indexes.md)
    * [11.1. 簡介](ii-the-sql-language/indexes/111-introduction.md)
    * [11.2. 索引型別](ii-the-sql-language/indexes/112-index-types.md)
    * [11.3. 多欄位索引](ii-the-sql-language/indexes/113-multicolumn-indexes.md)
    * [11.4. 索引與ORDER BY](ii-the-sql-language/indexes/114-indexes-and-order-by.md)
    * [11.5. 善用多個索引](ii-the-sql-language/indexes/115-combining-multiple-indexes.md)
    * [11.6. 唯一值索引](ii-the-sql-language/indexes/116-unique-indexes.md)
    * [11.7. 表示式索引](ii-the-sql-language/indexes/117-indexes-on-expressions.md)
    * [11.8. 部份索引](ii-the-sql-language/indexes/118-partial-indexes.md)
    * [11.9. 運算子物件及家族](ii-the-sql-language/indexes/119-operator-classes-and-operator-families.md)
    * [11.10. Indexes and Collations](ii-the-sql-language/indexes/1110-indexes-and-collations.md)
    * [11.11. 限用索引查詢](ii-the-sql-language/indexes/1111-index-only-scans.md)
    * [11.12. 檢查索引運用](ii-the-sql-language/indexes/1112-examining-index-usage.md)
  * [12. 全文檢索](ii-the-sql-language/full-text-search.md)
    * [12.1. 簡介](ii-the-sql-language/full-text-search/121-introduction.md)
    * [12.2. 查詢與索引](ii-the-sql-language/full-text-search/122-tables-and-indexes.md)
    * [12.3. 細部控制](ii-the-sql-language/full-text-search/123-controlling-text-search.md)
    * [12.4. 延伸功能](ii-the-sql-language/full-text-search/124-additional-features.md)
    * [12.5. 斷詞](ii-the-sql-language/full-text-search/125-parsers.md)
    * [12.6. 字典](ii-the-sql-language/full-text-search/126-dictionaries.md)
    * [12.7. 組態範例](ii-the-sql-language/full-text-search/127-configuration-example.md)
    * [12.8. 測試與除錯](ii-the-sql-language/full-text-search/128-testing-and-debugging-text-search.md)
    * [12.9. GIN及GiST索引型別](ii-the-sql-language/full-text-search/129-gin-and-gist-index-types.md)
    * [12.10. psql支援](ii-the-sql-language/full-text-search/1210-psql-support.md)
    * [12.11. 功能限制](ii-the-sql-language/full-text-search/1211-limitations.md)
  * [13. 一致性管理](ii-the-sql-language/concurrency-control.md)
    * [13.1. 簡介](ii-the-sql-language/concurrency-control/131-introduction.md)
    * [13.2. 交易隔離](ii-the-sql-language/concurrency-control/132-transaction-isolation.md)
    * [13.3. 鎖定模式](ii-the-sql-language/concurrency-control/133-explicit-locking.md)
    * [13.4. 在應用端檢視資料一致性](ii-the-sql-language/concurrency-control/134-data-consistency-checks-at-the-application-level.md)
    * [13.5. 特別注意](ii-the-sql-language/concurrency-control/135-caveats.md)
    * [13.6. 鎖定與索引](ii-the-sql-language/concurrency-control/136-locking-and-indexes.md)
  * [14. 效率技巧](ii-the-sql-language/performance-tips.md)
    * [14.1. 善用EXPLAIN](ii-the-sql-language/performance-tips/141-using-explain.md)
    * [14.2. 統計資訊](ii-the-sql-language/performance-tips/142-statistics-used-by-the-planner.md)
    * [14.3. 使用確切的JOIN方式](ii-the-sql-language/performance-tips/143-controlling-the-planner-with-explicit-join-clauses.md)
    * [14.4. 快速建立資料庫內容](ii-the-sql-language/performance-tips/144-populating-a-database.md)
    * [14.5. 彈性設定](ii-the-sql-language/performance-tips/145-non-durable-settings.md)
  * [15. 平行查詢](ii-the-sql-language/parallel-query.md)
    * [15.1. 如何運作？](ii-the-sql-language/parallel-query/151-how-parallel-query-works.md)
    * [15.2. 啓用時機？](ii-the-sql-language/parallel-query/152-when-can-parallel-query-be-used.md)
    * [15.3. 平行查詢計畫](ii-the-sql-language/parallel-query/153-parallel-plans.md)
    * [15.4. 平行查詢的安全性](ii-the-sql-language/parallel-query/154-parallel-safety.md)
* [III. 系統管理](iii-server-administration.md)
  * Installation from Source Code
    * 16.1. Short Version
    * 16.2. Requirements
    * 16.3. Getting The Source
    * 16.4. Installation Procedure
    * 16.5. Post-Installation Setup
    * 16.6. Supported Platforms
    * 16.7. Platform-specific Notes
  * Installation from Source Code on Windows
    * 17.1. Building with Visual C++ or the Microsoft Windows SDK
  * [18. 服務配置與維運](iii-server-administration/server-setup-and-operation.md)
    * [18.1. The PostgreSQL User Account](iii-server-administration/server-setup-and-operation/181-the-postgresql-user-account.md)
    * 18.2. Creating a Database Cluster
    * 18.3. Starting the Database Server
    * 18.4. Managing Kernel Resources
    * 18.5. Shutting Down the Server
    * 18.6. Upgrading a PostgreSQL Cluster
    * 18.7. Preventing Server Spoofing
    * 18.8. Encryption Options
    * 18.9. Secure TCP/IP Connections with SSL
    * 18.10. Secure TCP/IP Connections with SSH Tunnels
    * 18.11. Registering Event Log on Windows
  * [19. 服務組態設定](iii-server-administration/server-configuration.md)
    * 19.1. Setting Parameters
    * 19.2. File Locations
    * 19.3. Connections and Authentication
    * 19.4. Resource Consumption
    * 19.5. Write Ahead Log
    * 19.6. Replication
    * [19.7. 查詢規畫](iii-server-administration/server-configuration/197-query-planning.md)
    * 19.8. Error Reporting and Logging
    * 19.9. Run-time Statistics
    * 19.10. Automatic Vacuuming
    * [19.11. 用戶端連線預設參數](iii-server-administration/server-configuration/1911-client-connection-defaults.md)
    * 19.12. Lock Management
    * [19.13. 版本與平台的相容性](iii-server-administration/server-configuration/1913-version-and-platform-compatibility.md)
    * 19.14. Error Handling
    * 19.15. Preset Options
    * 19.16. Customized Options
    * 19.17. Developer Options
    * 19.18. Short Options
  * Client Authentication
    * 20.1. The pg\_hba.conf File
    * 20.2. User Name Maps
    * 20.3. Authentication Methods
    * 20.4. Authentication Problems
  * [21. 資料庫角色](iii-server-administration/database-roles.md)
    * 21.1. Database Roles
    * 21.2. Role Attributes
    * 21.3. Role Membership
    * 21.4. Dropping Roles
    * 21.5. Default Roles
    * 21.6. Function and Trigger Security
  * Managing Databases
    * 22.1. Overview
    * 22.2. Creating a Database
    * 22.3. Template Databases
    * 22.4. Database Configuration
    * 22.5. Destroying a Database
    * [22.6. Tablespaces](iii-server-administration/226-tablespaces.md)
  * Localization
    * 23.1. Locale Support
    * 23.2. Collation Support
    * 23.3. Character Set Support
  * [24. 例行性資料庫維護工作](iii-server-administration/routine-database-maintenance-tasks.md)
    * [24.1. 例行性資料清理](iii-server-administration/routine-database-maintenance-tasks/241-routine-vacuuming.md)
    * 24.2. Routine Reindexing
    * 24.3. Log File Maintenance
  * Backup and Restore
    * 25.1. SQL Dump
    * 25.2. File System Level Backup
    * 25.3. Continuous Archiving and Point-in-Time Recovery \(PITR\)
  * High Availability, Load Balancing, and Replication
    * 26.1. Comparison of Different Solutions
    * 26.2. Log-Shipping Standby Servers
    * 26.3. Failover
    * 26.4. Alternative Method for Log Shipping
    * 26.5. Hot Standby
  * Recovery Configuration
    * 27.1. Archive Recovery Settings
    * 27.2. Recovery Target Settings
    * 27.3. Standby Server Settings
  * Monitoring Database Activity
    * 28.1. Standard Unix Tools
    * 28.2. The Statistics Collector
    * 28.3. Viewing Locks
    * 28.4. Progress Reporting
    * 28.5. Dynamic Tracing
  * Monitoring Disk Usage
    * 29.1. Determining Disk Usage
    * 29.2. Disk Full Failure
  * Reliability and the Write-Ahead Log
    * 30.1. Reliability
    * 30.2. Write-Ahead Logging \(WAL\)
    * 30.3. Asynchronous Commit
    * 30.4. WAL Configuration
    * 30.5. WAL Internals
  * Logical Replication
    * 31.1. Publication
    * 31.2. Subscription
    * 31.3. Conflicts
    * 31.4. Architecture
    * 31.5. Monitoring
    * 31.6. Security
    * 31.7. Configuration Settings
    * 31.8. Quick Setup
  * Regression Tests
    * 32.1. Running the Tests
    * 32.2. Test Evaluation
    * 32.3. Variant Comparison Files
    * 32.4. TAP Tests
    * 32.5. Test Coverage Examination
* [IV. Client Interfaces](iv-client-interfaces.md)
  * libpq - C Library
    * 33.1. Database Connection Control Functions
    * 33.2. Connection Status Functions
    * 33.3. Command Execution Functions
    * 33.4. Asynchronous Command Processing
    * 33.5. Retrieving Query Results Row-By-Row
    * 33.6. Canceling Queries in Progress
    * 33.7. The Fast-Path Interface
    * 33.8. Asynchronous Notification
    * 33.9. Functions Associated with the COPY Command
    * 33.10. Control Functions
    * 33.11. Miscellaneous Functions
    * 33.12. Notice Processing
    * 33.13. Event System
    * 33.14. Environment Variables
    * 33.15. The Password File
    * 33.16. The Connection Service File
    * 33.17. LDAP Lookup of Connection Parameters
    * 33.18. SSL Support
    * 33.19. Behavior in Threaded Programs
    * 33.20. Building libpq Programs
    * 33.21. Example Programs
  * Large Objects
    * 34.1. Introduction
    * 34.2. Implementation Features
    * 34.3. Client Interfaces
    * 34.4. Server-side Functions
    * 34.5. Example Program
  * ECPG - Embedded SQL in C
    * 35.1. The Concept
    * 35.2. Managing Database Connections
    * 35.3. Running SQL Commands
    * 35.4. Using Host Variables
    * 35.5. Dynamic SQL
    * 35.6. pgtypes Library
    * 35.7. Using Descriptor Areas
    * 35.8. Error Handling
    * 35.9. Preprocessor Directives
    * 35.10. Processing Embedded SQL Programs
    * 35.11. Library Functions
    * 35.12. Large Objects
    * 35.13. C++ Applications
    * 35.14. Embedded SQL Commands
    * 35.15. Informix Compatibility Mode
    * 35.16. Internals
  * The Information Schema
    * 36.1. The Schema
    * 36.2. Data Types
    * 36.3. information\_schema\_catalog\_name
    * 36.4. administrable\_role\_authorizations
    * 36.5. applicable\_roles
    * 36.6. attributes
    * 36.7. character\_sets
    * 36.8. check\_constraint\_routine\_usage
    * 36.9. check\_constraints
    * 36.10. collations
    * 36.11. collation\_character\_set\_applicability
    * 36.12. column\_domain\_usage
    * 36.13. column\_options
    * 36.14. column\_privileges
    * 36.15. column\_udt\_usage
    * 36.16. columns
    * 36.17. constraint\_column\_usage
    * 36.18. constraint\_table\_usage
    * 36.19. data\_type\_privileges
    * 36.20. domain\_constraints
    * 36.21. domain\_udt\_usage
    * 36.22. domains
    * 36.23. element\_types
    * 36.24. enabled\_roles
    * 36.25. foreign\_data\_wrapper\_options
    * 36.26. foreign\_data\_wrappers
    * 36.27. foreign\_server\_options
    * 36.28. foreign\_servers
    * 36.29. foreign\_table\_options
    * 36.30. foreign\_tables
    * 36.31. key\_column\_usage
    * 36.32. parameters
    * 36.33. referential\_constraints
    * 36.34. role\_column\_grants
    * 36.35. role\_routine\_grants
    * 36.36. role\_table\_grants
    * 36.37. role\_udt\_grants
    * 36.38. role\_usage\_grants
    * 36.39. routine\_privileges
    * 36.40. routines
    * 36.41. schemata
    * 36.42. sequences
    * 36.43. sql\_features
    * 36.44. sql\_implementation\_info
    * 36.45. sql\_languages
    * 36.46. sql\_packages
    * 36.47. sql\_parts
    * 36.48. sql\_sizing
    * 36.49. sql\_sizing\_profiles
    * 36.50. table\_constraints
    * 36.51. table\_privileges
    * 36.52. tables
    * 36.53. transforms
    * 36.54. triggered\_update\_columns
    * 36.55. triggers
    * 36.56. udt\_privileges
    * 36.57. usage\_privileges
    * 36.58. user\_defined\_types
    * 36.59. user\_mapping\_options
    * 36.60. user\_mappings
    * 36.61. view\_column\_usage
    * 36.62. view\_routine\_usage
    * 36.63. view\_table\_usage
    * 36.64. views
* [V. Server Programming](v-server-programming.md)
  * [37. Extending SQL](v-server-programming/extending-sql.md)
    * 37.1. How Extensibility Works
    * 37.2. The PostgreSQL Type System
    * 37.3. User-defined Functions
    * [37.4. SQL 語言函數](v-server-programming/extending-sql/374-query-language-sql-functions.md)
    * 37.5. Function Overloading
    * 37.6. Function Volatility Categories
    * 37.7. Procedural Language Functions
    * 37.8. Internal Functions
    * 37.9. C-Language Functions
    * 37.10. User-defined Aggregates
    * 37.11. User-defined Types
    * 37.12. User-defined Operators
    * 37.13. Operator Optimization Information
    * 37.14. Interfacing Extensions To Indexes
    * 37.15. Packaging Related Objects into an Extension
    * 37.16. Extension Building Infrastructure
  * [40. The Rule System](v-server-programming/the-rule-system.md)
* [VI. Reference](vi-reference.md)
  * [I. SQL 指令](vi-reference/i-sql-commands.md)
    * [ALTER POLICY](vi-reference/i-sql-commands/alter-policy.md)
    * [ALTER TABLE](vi-reference/i-sql-commands/alter-table.md)
    * [COPY](vi-reference/i-sql-commands/copy.md)
    * [CREATE FOREIGN TABLE](vi-reference/i-sql-commands/create-foreign-table.md)
    * [CREATE FOREIGN DATA WRAPPER](vi-reference/i-sql-commands/create-foreign-data-wrapper.md)
    * [CREATE FUNCTION](vi-reference/i-sql-commands/create-function.md)
    * [CREATE POLICY](vi-reference/i-sql-commands/create-policy.md)
    * [CREATE SCHEMA](vi-reference/i-sql-commands/create-schema.md)
    * [CREATE SERVER](vi-reference/i-sql-commands/create-server.md)
    * [CREATE TABLE](vi-reference/i-sql-commands/create-table.md)
    * [CREATE TYPE](vi-reference/i-sql-commands/create-type.md)
    * [CREATE USER MAPPING](vi-reference/i-sql-commands/create-user-mapping.md)
    * [DELETE](vi-reference/i-sql-commands/delete.md)
    * [DROP POLICY](vi-reference/i-sql-commands/drop-policy.md)
    * [DROP TABLE](vi-reference/i-sql-commands/drop-table.md)
    * [GRANT](vi-reference/i-sql-commands/grant.md)
    * [IMPORT FOREIGN SCHEMA](vi-reference/i-sql-commands/import-foreign-schema.md)
    * [INSERT](vi-reference/i-sql-commands/insert.md)
    * [REVOKE](vi-reference/i-sql-commands/revoke.md)
    * [SELECT](vi-reference/i-sql-commands/select.md)
    * [SET TRANSACTION](vi-reference/i-sql-commands/set-transaction.md)
    * [UPDATE](vi-reference/i-sql-commands/update.md)
    * [VALUES](vi-reference/i-sql-commands/values.md)
  * [II. PostgreSQL 用戶端工具](vi-reference/ii-postgresql-client-applications.md)
    * [createdb](vi-reference/ii-postgresql-client-applications/createdb.md)
    * [dropdb](vi-reference/ii-postgresql-client-applications/dropdb.md)
    * [pgbench](vi-reference/ii-postgresql-client-applications/pgbench.md)
    * [psql](vi-reference/ii-postgresql-client-applications/psql.md)
  * III. PostgreSQL Server Applications
* [VII. Internals](vii-internals.md)
  * [52. Frontend/Backend Protocol](vii-internals/frontendbackend-protocol.md)
    * 52.1. Overview
    * 52.2. Message Flow
    * 52.3. SASL Authentication
    * 52.4. Streaming Replication Protocol
    * 52.5. Logical Streaming Replication Protocol
    * 52.6. Message Data Types
    * 52.7. Message Formats
    * 52.8. Error and Notice Message Fields
    * 52.9. Logical Replication Message Formats
    * 52.10. Summary of Changes since Protocol 2.0
* [VIII. 附錄](viii-appendixes.md)
  * [A. PostgreSQL錯誤代碼](viii-appendixes/postgresql-error-codes.md)
  * [B. 日期時間格式支援](viii-appendixes/datetime-support.md)
    * [B.1. 日期時間解譯流程](viii-appendixes/datetime-support/b1-datetime-input-interpretation.md)
    * [B.2. 日期時間慣用字](viii-appendixes/datetime-support/b2-datetime-key-words.md)
    * [B.3. 日期時間設定檔](viii-appendixes/datetime-support/b3-datetime-configuration-files.md)
    * [B.4. 日期時間的沿革](viii-appendixes/datetime-support/b4-history-of-units.md)
  * [C. SQL 關鍵字](viii-appendixes/sql-key-words.md)
  * SQL Conformance
  * Release Notes
  * [F. 延伸支援模組](viii-appendixes/additional-supplied-modules.md)
    * [F.11. dblink](viii-appendixes/additional-supplied-modules/f11-dblink.md)
      * [dblink](viii-appendixes/additional-supplied-modules/f11-dblink/dblink.md)
  * Additional Supplied Programs
  * External Projects
  * The Source Code Repository
  * [J. 文件取得](viii-appendixes/documentation.md)
  * [K. 縮寫字](viii-appendixes/acronyms.md)
* [參考書目](bibliography.md)

