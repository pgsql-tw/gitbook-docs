# Table of contents

* [簡介](README.md)
* [前言](preface/README.md)
  * [1. 什麼是PostgreSQL？](preface/intro-whatis.md)
  * [2. PostgreSQL沿革](preface/history.md)
  * [3. 慣例](preface/notation.md)
  * [4. 其他參考資訊](preface/resources.md)
  * [5. 問題回報指南](preface/bug-reporting.md)
* [I. 新手教學](tutorial/README.md)
  * [1. 入門指南](tutorial/start/README.md)
    * [1.1. 安裝](tutorial/start/installation.md)
    * [1.2. 基礎架構](tutorial/start/architecture.md)
    * [1.3. 建立一個資料庫](tutorial/start/createdb.md)
    * [1.4. 存取一個資料庫](tutorial/start/accessdb.md)
  * [2. SQL查詢語言](tutorial/sql/README.md)
    * [2.1. 簡介](tutorial/sql/intro.md)
    * [2.2. 概念](tutorial/sql/concepts.md)
    * [2.3. 創建一個新的資料表](tutorial/sql/table.md)
    * [2.4. 資料列是資料表的組成單位](tutorial/sql/populate.md)
    * [2.5. 資料表的查詢](tutorial/sql/select.md)
    * [2.6. 交叉查詢](tutorial/sql/join.md)
    * [2.7. 彙總查詢](tutorial/sql/agg.md)
    * [2.8. 更新資料](tutorial/sql/update.md)
    * [2.9. 刪除資料](tutorial/sql/delete.md)
  * [3. 先進功能](tutorial/advanced/README.md)
    * [3.1. 簡介](tutorial/advanced/advanced-intro.md)
    * [3.2. 檢視表（View）](tutorial/advanced/views.md)
    * [3.3. 外部索引鍵](tutorial/advanced/fk.md)
    * [3.4. 交易安全](tutorial/advanced/transaction.md)
    * [3.5. 窗函數](tutorial/advanced/window-function.md)
    * [3.6. 繼承](tutorial/advanced/inheritance.md)
    * [3.7. 結論](tutorial/advanced/conclusion.md)
* [II. SQL查詢語言](sql/README.md)
  * [4. SQL語法](sql/syntax/README.md)
    * [4.1. 語法結構](sql/syntax/lexical.md)
    * [4.2. 參數表示式](sql/syntax/value-expressions.md)
    * [4.3. 函數呼叫](sql/syntax/calling-funcs.md)
  * [5. 定義資料結構](sql/ddl/README.md)
    * [5.1. 認識資料表](sql/ddl/5.1.-ren-shi-zi-liao-biao.md)
    * [5.2. 預設值](sql/ddl/5.2.-yu-she-zhi.md)
    * [5.3. 限制條件](sql/ddl/5.3.-xian-zhi-tiao-jian.md)
    * [5.4. 系統欄位](sql/ddl/system-columns.md)
    * [5.5. 表格變更](sql/ddl/5.5.-biao-ge-bian-geng.md)
    * [5.6. 權限](sql/ddl/priv.md)
    * [5.7. 資料列安全原則](sql/ddl/rowsecurity.md)
    * [5.8. Schemas](sql/ddl/5.8.-schemas.md)
    * [5.9. 繼承](sql/ddl/5.9.-ji-cheng.md)
    * [5.10. 分割資料表](sql/ddl/partition-table.md)
    * [5.11. 外部資料](sql/ddl/5.11.-wai-bu-zi-liao.md)
    * [5.12. 其他資料庫物件](sql/ddl/5.12.-qi-ta-zi-liao-ku-wu-jian.md)
    * [5.13. 相依性追蹤](sql/ddl/dependency-tracking.md)
  * [6. 資料處理](sql/6.-zi-liao-chu-li/README.md)
    * [6.1. 新增資料](sql/6.-zi-liao-chu-li/6.1.-xin-zeng-zi-liao.md)
    * [6.2. 更新資料](sql/6.-zi-liao-chu-li/6.2.-geng-xin-zi-liao.md)
    * [6.3. 刪除資料](sql/6.-zi-liao-chu-li/6.3.-shan-chu-zi-liao.md)
    * [6.4. 修改並回傳資料](sql/6.-zi-liao-chu-li/6.4.-xiu-gai-bing-hui-chuan-zi-liao.md)
  * [7. 資料查詢](sql/7.-zi-liao-cha-xun/README.md)
    * [7.1. 概觀](sql/7.-zi-liao-cha-xun/7.1.-gai-guan.md)
    * [7.2. 資料表表示式](sql/7.-zi-liao-cha-xun/table-expressions.md)
    * [7.3. 取得資料列表](sql/7.-zi-liao-cha-xun/7.3.-qu-de-zi-liao-lie-biao.md)
    * [7.4. 合併查詢結果](sql/7.-zi-liao-cha-xun/7.4.-he-bing-cha-xun-jie-guo.md)
    * [7.5. 資料排序](sql/7.-zi-liao-cha-xun/7.5.-zi-liao-pai-xu.md)
    * [7.6. 指定資料範圍](sql/7.-zi-liao-cha-xun/7.6.-zhi-ding-zi-liao-fan-wei.md)
    * [7.7. 列舉資料](sql/7.-zi-liao-cha-xun/7.7.-lie-ju-zi-liao.md)
    * [7.8. 遞迴查詢](sql/7.-zi-liao-cha-xun/7.8.-di-hui-cha-xun.md)
  * [8. 資料型別](sql/datatype/README.md)
    * [8.1. 數字型別](sql/datatype/8.1.-shu-zi-xing-bie.md)
    * [8.2. 貨幣型別](sql/datatype/8.2.-huo-bi-xing-bie.md)
    * [8.3. 文字型別](sql/datatype/8.3.-wen-zi-xing-bie.md)
    * [8.4. 位元組型別](sql/datatype/datatype-binary.md)
    * [8.5. 日期時間型別](sql/datatype/datetime.md)
    * [8.6. 布林型別](sql/datatype/8.6.-bu-lin-xing-bie.md)
    * [8.7. 列舉型別](sql/datatype/8.7.-lie-ju-xing-bie.md)
    * [8.8. 地理資訊型別](sql/datatype/geometric.md)
    * [8.9. 網路資訊型別](sql/datatype/8.9.-wang-lu-zi-xun-xing-bie.md)
    * [8.10. 位元字串型別](sql/datatype/8.10.-wei-yuan-zi-chuan-xing-bie.md)
    * [8.11. 全文檢索型別](sql/datatype/8.11.-quan-wen-jian-suo-xing-bie.md)
    * [8.12. UUID型別](sql/datatype/8.12.-uuid-xing-bie.md)
    * [8.13. XML型別](sql/datatype/8.13.-xml-xing-bie.md)
    * [8.14. JSON型別](sql/datatype/8.14.-json-xing-bie.md)
    * [8.15. 陣列](sql/datatype/8.15.-zhen-lie.md)
    * [8.16. 複合型別](sql/datatype/8.16.-fu-he-xing-bie.md)
    * [8.17. 範圍型別](sql/datatype/8.17.-fan-wei-xing-bie.md)
    * [8.18. 指標型別](sql/datatype/8.18.-zhi-biao-xing-bie.md)
    * [8.19. pg\_lsn型別](sql/datatype/8.19.-pglsn-xing-bie.md)
    * [8.20. 概念型別](sql/datatype/8.20.-gai-nian-xing-bie.md)
  * [9. 函式及運算子](sql/functions/README.md)
    * [9.1. 邏輯運算子](sql/functions/9.1.-luo-ji-yun-suan-zi.md)
    * [9.2. 比較函式及運算子](sql/functions/9.2.-bi-jiao-han-shi-ji-yun-suan-zi.md)
    * [9.3. 數學函式及運算子](sql/functions/9.3.-shu-xue-han-shi-ji-yun-suan-zi.md)
    * 9.4. 字串函式及運算子
    * [9.5. 位元字串函式及運算子](sql/functions/9.5.-wei-yuan-zi-chuan-han-shi-ji-yun-suan-zi.md)
    * [9.6. 二元字串函式及運算子](sql/functions/9.6.-er-yuan-zi-chuan-han-shi-ji-yun-suan-zi.md)
    * [9.7. 特徵比對](sql/functions/functions-matching.md)
    * [9.8. 型別轉換函式](sql/functions/9.8.-xing-bie-zhuan-huan-han-shi.md)
    * [9.9 日期時間函式及運算子](sql/functions/datetime.md)
    * [9.10. 列舉型別函式](sql/functions/9.10.-lie-ju-xing-bie-han-shi.md)
    * [9.11. 地理資訊函式及運算子](sql/functions/9.11.-di-li-zi-xun-han-shi-ji-yun-suan-zi.md)
    * [9.12. 網路位址函式及運算子](sql/functions/9.12.-wang-lu-wei-zhi-han-shi-ji-yun-suan-zi.md)
    * [9.13. 文字檢索函式及運算子](sql/functions/9.13.-wen-zi-jian-suo-han-shi-ji-yun-suan-zi.md)
    * [9.14. XML函式](sql/functions/functions-xml.md)
    * [9.15. JSON函式及運算子](sql/functions/9.15.-json-han-shi-ji-yun-suan-zi.md)
    * [9.16. 序列函式](sql/functions/9.16.-xu-lie-han-shi.md)
    * [9.17. 條件表示式](sql/functions/functions-conditional.md)
    * [9.18. 陣列函式及運算子](sql/functions/9.18.-zhen-lie-han-shi-ji-yun-suan-zi.md)
    * [9.19. 範圍函式及運算子](sql/functions/9.19.-fan-wei-han-shi-ji-yun-suan-zi.md)
    * [9.20. 彙總函式](sql/functions/9.20.-hui-zong-han-shi.md)
    * [9.21. Window函式](sql/functions/9.21.-window-han-shi.md)
    * [9.22. 子查詢](sql/functions/9.22.-zi-cha-xun.md)
    * [9.23. 資料列與陣列的比較運算](sql/functions/functions-comparisons.md)
    * [9.24. 集合回傳函式](sql/functions/9.24.-ji-he-hui-chuan-han-shi.md)
    * [9.25. 系統資訊函數](sql/functions/info.md)
    * [9.26. 系統管理函式](sql/functions/functions-admin.md)
    * [9.27. 觸發函式](sql/functions/9.27.-chu-fa-han-shi.md)
    * [9.28. 事件觸發函式](sql/functions/9.28.-shi-jian-chu-fa-han-shi.md)
  * [10. 型別轉換](sql/typeconv/README.md)
    * [10.1. 概觀](sql/typeconv/10.1.-gai-guan.md)
    * [10.2. 運算子](sql/typeconv/10.2.-yun-suan-zi.md)
    * [10.3. 函式](sql/typeconv/10.3.-han-shi.md)
    * [10.4. 儲存轉換規則](sql/typeconv/10.4.-chu-cun-zhuan-huan-gui-ze.md)
    * [10.5. UNION、CASE等相關操作](sql/typeconv/union-case.md)
    * [10.6. SELECT輸出規則](sql/typeconv/10.6.-select-shu-chu-gui-ze.md)
  * [11. 索引](sql/index/README.md)
    * [11.1. 簡介](sql/index/11.1.-jian-jie.md)
    * [11.2. 索引型別](sql/index/11.2.-suo-yin-xing-bie.md)
    * [11.3. 多欄位索引](sql/index/11.3.-duo-lan-wei-suo-yin.md)
    * [11.4. 索引與ORDER BY](sql/index/11.4.-suo-yin-yu-order-by.md)
    * [11.5. 善用多個索引](sql/index/11.5.-shan-yong-duo-ge-suo-yin.md)
    * [11.6. 唯一值索引](sql/index/11.6.-wei-yi-zhi-suo-yin.md)
    * [11.7. 表示式索引](sql/index/11.7.-biao-shi-shi-suo-yin.md)
    * [11.8. 部份索引](sql/index/11.8.-bu-fen-suo-yin.md)
    * [11.9. 運算子物件及家族](sql/index/11.9.-yun-suan-zi-wu-jian-ji-jia-zu.md)
    * [11.10. Indexes and Collations](sql/index/11.10.-indexes-and-collations.md)
    * [11.11. 索引限定查詢](sql/index/index-only-scans.md)
    * [11.12. 檢查索引運用](sql/index/11.12.-jian-cha-suo-yin-yun-yong.md)
  * [12. 全文檢索](sql/textsearch/README.md)
    * [12.1. 簡介](sql/textsearch/12.1.-jian-jie.md)
    * [12.2. 查詢與索引](sql/textsearch/12.2.-cha-xun-yu-suo-yin.md)
    * [12.3. 細部控制](sql/textsearch/12.3.-xi-bu-kong-zhi.md)
    * [12.4. 延伸功能](sql/textsearch/12.4.-yan-shen-gong-neng.md)
    * [12.5. 斷詞](sql/textsearch/12.5.-duan-ci.md)
    * [12.6. 字典](sql/textsearch/12.6.-zi-dian.md)
    * [12.7. 組態範例](sql/textsearch/12.7.-zu-tai-fan-li.md)
    * [12.8. 測試與除錯](sql/textsearch/12.8.-ce-shi-yu-chu-cuo.md)
    * [12.9. GIN及GiST索引型別](sql/textsearch/12.9.-gin-ji-gist-suo-yin-xing-bie.md)
    * [12.10. psql支援](sql/textsearch/12.10.-psql-zhi-yuan.md)
    * [12.11. 功能限制](sql/textsearch/12.11.-gong-neng-xian-zhi.md)
  * [13. 一致性管理\(MVCC\)](sql/mvcc/README.md)
    * [13.1. 簡介](sql/mvcc/13.1.-jian-jie.md)
    * [13.2. 交易隔離](sql/mvcc/13.2.-jiao-yi-ge-li.md)
    * [13.3. 鎖定模式](sql/mvcc/13.3.-suo-ding-mo-shi.md)
    * [13.4. 在應用端檢視資料一致性](sql/mvcc/13.4.-zai-ying-yong-duan-jian-shi-zi-liao-yi-zhi-xing.md)
    * [13.5. 特別注意](sql/mvcc/caveats.md)
    * [13.6. 鎖定與索引](sql/mvcc/13.6.-suo-ding-yu-suo-yin.md)
  * [14. 效能技巧](sql/performance-tips/README.md)
    * [14.1. 善用EXPLAIN](sql/performance-tips/14.1.-shan-yong-explain.md)
    * [14.2. 統計資訊](sql/performance-tips/planner-stats.md)
    * [14.3. 使用確切的JOIN方式](sql/performance-tips/14.3.-shi-yong-que-qie-de-join-fang-shi.md)
    * [14.4. 快速建立資料庫內容](sql/performance-tips/14.4.-kuai-su-jian-li-zi-liao-ku-nei-rong.md)
    * [14.5. 彈性設定](sql/performance-tips/14.5.-dan-xing-she-ding.md)
  * [15. 平行查詢](sql/15.-ping-hang-cha-xun/README.md)
    * [15.1. 如何運作？](sql/15.-ping-hang-cha-xun/15.1.-ru-he-yun-zuo.md)
    * [15.2. 啓用時機？](sql/15.-ping-hang-cha-xun/15.2.-qi-yong-shi-ji.md)
    * [15.3. 平行查詢計畫](sql/15.-ping-hang-cha-xun/15.3.-ping-hang-cha-xun-ji-hua.md)
    * [15.4. 平行查詢的安全性](sql/15.-ping-hang-cha-xun/15.4.-ping-hang-cha-xun-de-an-quan-xing.md)
* [III. 系統管理](server-administration/README.md)
  * [16. 用原始碼安裝](server-administration/installation-from-source-code/README.md)
    * 16.1. Short Version
    * 16.2. Requirements
    * 16.3. Getting The Source
    * 16.4. Installation Procedure
    * 16.5. Post-Installation Setup
    * 16.6. Supported Platforms
    * [16.7. 平台相關的注意事項](server-administration/installation-from-source-code/platform-specific-notes.md)
  * [17. 用原始碼在 Windows 上安裝](server-administration/installation-from-source-code-on-windows/README.md)
    * 17.1. Building with Visual C++ or the Microsoft Windows SDK
  * [18. 服務配置與維運](server-administration/18.-fu-wu-pei-zhi-yu-wei-yun/README.md)
    * [18.1. The PostgreSQL User Account](server-administration/18.-fu-wu-pei-zhi-yu-wei-yun/18.1.-the-postgresql-user-account.md)
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
  * [19. 服務組態設定](server-administration/runtime-config/README.md)
    * 19.1. Setting Parameters
    * [19.2. File Locations](server-administration/runtime-config/file-locations.md)
    * 19.3. Connections and Authentication
    * [19.4. Resource Consumption](server-administration/runtime-config/resource-consumption.md)
    * 19.5. Write Ahead Log
    * [19.6. Replication](server-administration/runtime-config/replication.md)
    * [19.7. 查詢規畫](server-administration/runtime-config/query-planning.md)
    * [19.8. 錯誤回報與日誌記錄](server-administration/runtime-config/logging.md)
    * [19.9. Run-time Statistics](server-administration/runtime-config/run-time-statistics.md)
    * [19.10. 自動資料庫清理](server-administration/runtime-config/autovacuum.md)
    * [19.11. 用戶端連線預設參數](server-administration/runtime-config/runtime-config-client.md)
    * 19.12. Lock Management
    * [19.13. 版本與平台的相容性](server-administration/runtime-config/19.13.-ban-ben-yu-ping-tai-de-xiang-rong-xing.md)
    * 19.14. Error Handling
    * [19.15. 預先配置的參數](server-administration/runtime-config/preset.md)
    * 19.16. Customized Options
    * 19.17. Developer Options
    * 19.18. Short Options
  * [20. 使用者認證](server-administration/client-authentication/README.md)
    * [20.1. 設定檔：pg\_hba.conf](server-administration/client-authentication/auth-pg-hba-conf.md)
    * 20.2. User Name Maps
    * 20.3. Authentication Methods
    * 20.4. Authentication Problems
  * [21. 資料庫角色](server-administration/user-manag/README.md)
    * [21.1. Database Roles](server-administration/user-manag/database-roles.md)
    * [21.2. Role Attributes](server-administration/user-manag/role-attributes.md)
    * [21.3. Role Membership](server-administration/user-manag/role-membership.md)
    * [21.4. Dropping Roles](server-administration/user-manag/dropping-roles.md)
    * [21.5. Default Roles](server-administration/user-manag/default-roles.md)
    * [21.6. Function Security](server-administration/user-manag/function-security.md)
  * [22. Managing Databases](server-administration/managing-databases/README.md)
    * 22.1. Overview
    * 22.2. Creating a Database
    * 22.3. Template Databases
    * 22.4. Database Configuration
    * 22.5. Destroying a Database
    * [22.6. Tablespaces](server-administration/managing-databases/manage-ag-tablespaces.md)
  * [23. 語系](server-administration/charset/README.md)
    * [23.1. 語系支援](server-administration/charset/locale.md)
    * [23.2. Collation Support](server-administration/charset/collation-support.md)
    * [23.3. Character Set Support](server-administration/charset/multibyte.md)
  * [24. 例行性資料庫維護工作](server-administration/maintenance/README.md)
    * [24.1. 例行性資料清理](server-administration/maintenance/routine-vacuuming.md)
    * 24.2. Routine Reindexing
    * [24.3. Log File Maintenance](server-administration/maintenance/log-file-maintenance.md)
  * [25. 備份及還原](server-administration/backup-and-restore/README.md)
    * [25.1. SQL Dump](server-administration/backup-and-restore/sql-dump.md)
    * [25.2. File System Level Backup](server-administration/backup-and-restore/file-system-level-backup.md)
    * [25.3. Continuous Archiving and Point-in-Time Recovery \(PITR\)](server-administration/backup-and-restore/continuous-archiving-and-point-in-time-recovery-pitr.md)
  * High Availability, Load Balancing, and Replication
    * 26.1. Comparison of Different Solutions
    * 26.2. Log-Shipping Standby Servers
    * 26.3. Failover
    * 26.4. Alternative Method for Log Shipping
    * [26.5. Hot Standby](server-administration/high-availability-load-balancing-and-replication/hot-standby.md)
  * Recovery Configuration
    * 27.1. Archive Recovery Settings
    * 27.2. Recovery Target Settings
    * 27.3. Standby Server Settings
  * [28. 監控資料庫活動](server-administration/monitoring/README.md)
    * 28.1. Standard Unix Tools
    * [28.2. 統計資訊收集器](server-administration/monitoring/stats.md)
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
* [IV. 用戶端介面](client-interfaces/README.md)
  * [33. libpq - C Library](client-interfaces/libpq-c-library/README.md)
    * 33.1. Database Connection Control Functions
    * [33.2. 連線狀態函數](client-interfaces/libpq-c-library/libpq-status.md)
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
    * [33.15. 密碼檔](client-interfaces/libpq-c-library/password-file.md)
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
* [V. 資料庫程式設計](server-programming/README.md)
  * [37. Extending SQL](server-programming/extending-sql/README.md)
    * 37.1. How Extensibility Works
    * 37.2. The PostgreSQL Type System
    * [37.3. 使用者自訂函數](server-programming/extending-sql/user-defined-functions.md)
    * [37.4. SQL 語言函數](server-programming/extending-sql/xfunc-sql.md)
    * 37.5. Function Overloading
    * [37.6. Function Volatility Categories](server-programming/extending-sql/function-volatility-categories.md)
    * [37.7. Procedural Language Functions](server-programming/extending-sql/xfunc-pl.md)
    * [37.8. Internal Functions](server-programming/extending-sql/xfunc-internal.md)
    * [37.9. C-Language Functions](server-programming/extending-sql/c-language-functions.md)
    * 37.10. User-defined Aggregates
    * 37.11. User-defined Types
    * 37.12. User-defined Operators
    * 37.13. Operator Optimization Information
    * 37.14. Interfacing Extensions To Indexes
    * 37.15. Packaging Related Objects into an Extension
    * 37.16. Extension Building Infrastructure
  * [40. 規則系統](server-programming/the-rule-system/README.md)
    * [40.5. Rules and Privileges](server-programming/the-rule-system/rules-and-privileges.md)
* [VI. 參考資訊](reference/README.md)
  * [I. SQL 指令](reference/sql-commands/README.md)
    * [ALTER FUNCTION](reference/sql-commands/alter-function.md)
    * [ALTER MATERIALIZED VIEW](reference/sql-commands/alter-materialized-view.md)
    * [ALTER POLICY](reference/sql-commands/alter-policy.md)
    * [ALTER ROLE](reference/sql-commands/alter-role.md)
    * [ALTER SEQUENCE](reference/sql-commands/alter-sequence.md)
    * [ALTER TABLE](reference/sql-commands/alter-table.md)
    * [ALTER TABLESPACE](reference/sql-commands/alter-tablespace.md)
    * [ANALYZE](reference/sql-commands/analyze.md)
    * [CLUSTER](reference/sql-commands/cluster.md)
    * [COMMENT](reference/sql-commands/comment.md)
    * [COPY](reference/sql-commands/copy.md)
    * [CREATE DATABASE](reference/sql-commands/create-database.md)
    * [CREATE FOREIGN TABLE](reference/sql-commands/create-foreign-table.md)
    * [CREATE FOREIGN DATA WRAPPER](reference/sql-commands/create-foreign-data-wrapper.md)
    * [CREATE FUNCTION](reference/sql-commands/create-function.md)
    * [CREATE INDEX](reference/sql-commands/create-index.md)
    * [CREATE MATERIALIZED VIEW](reference/sql-commands/create-materialized-view.md)
    * [CREATE POLICY](reference/sql-commands/create-policy.md)
    * [CREATE ROLE](reference/sql-commands/create-role.md)
    * [CREATE SCHEMA](reference/sql-commands/create-schema.md)
    * [CREATE SERVER](reference/sql-commands/create-server.md)
    * [CREATE TABLE](reference/sql-commands/create-table.md)
    * [CREATE TABLE AS](reference/sql-commands/create-table-as.md)
    * [CREATE TABLESPACE](reference/sql-commands/create-tablespace.md)
    * [CREATE TRANSFORM](reference/sql-commands/create-transform.md)
    * [CREATE TYPE](reference/sql-commands/create-type.md)
    * [CREATE USER](reference/sql-commands/create-user.md)
    * [CREATE USER MAPPING](reference/sql-commands/create-user-mapping.md)
    * [CREATE VIEW](reference/sql-commands/create-view.md)
    * [DELETE](reference/sql-commands/delete.md)
    * [DROP FUNCTION](reference/sql-commands/drop-function.md)
    * [DROP MATERIALIZED VIEW](reference/sql-commands/drop-materialized-view.md)
    * [DROP OWNED](reference/sql-commands/drop-owned.md)
    * [DROP POLICY](reference/sql-commands/drop-policy.md)
    * [DROP ROLE](reference/sql-commands/drop-role.md)
    * [DROP TABLE](reference/sql-commands/drop-table.md)
    * [DROP TABLESPACE](reference/sql-commands/drop-tablespace.md)
    * [EXPLAIN](reference/sql-commands/explain.md)
    * [GRANT](reference/sql-commands/grant.md)
    * [IMPORT FOREIGN SCHEMA](reference/sql-commands/import-foreign-schema.md)
    * [INSERT](reference/sql-commands/insert.md)
    * [LISTEN](reference/sql-commands/listen.md)
    * [LOAD](reference/sql-commands/load.md)
    * [NOTIFY](reference/sql-commands/notify.md)
    * [REASSIGN OWNED](reference/sql-commands/reassign-owned.md)
    * [REFRESH MATERIALIZED VIEW](reference/sql-commands/refresh-materialized-view.md)
    * [RESET](reference/sql-commands/reset.md)
    * [REVOKE](reference/sql-commands/revoke.md)
    * [SELECT](reference/sql-commands/select.md)
    * [SET](reference/sql-commands/set.md)
    * [SET ROLE](reference/sql-commands/set-role.md)
    * [SET SESSION AUTHORIZATION](reference/sql-commands/set-session-authorization.md)
    * [SET TRANSACTION](reference/sql-commands/set-transaction.md)
    * [SHOW](reference/sql-commands/show.md)
    * [TRUNCATE](reference/sql-commands/truncate.md)
    * [UPDATE](reference/sql-commands/update.md)
    * [VACUUM](reference/sql-commands/vacuum.md)
    * [VALUES](reference/sql-commands/values.md)
  * [II. PostgreSQL 用戶端工具](reference/client/README.md)
    * [createdb](reference/client/createdb.md)
    * [createuser](reference/client/createuser.md)
    * [dropdb](reference/client/dropdb.md)
    * [dropuser](reference/client/dropuser.md)
    * [pgbench](reference/client/pgbench.md)
    * [psql](reference/client/psql.md)
    * [vacuumdb](reference/client/vacuumdb.md)
  * III. PostgreSQL Server Applications
* [VII. 資料庫進階](internals/README.md)
  * [51. 系統目錄](internals/system-catalogs/README.md)
    * [51.8. pg\_authid](internals/system-catalogs/pg_authid.md)
    * [51.11 pg\_class](internals/system-catalogs/pg_class.md)
    * [51.15 pg\_database](internals/system-catalogs/pg_database.md)
    * [51.26 pg\_index](internals/system-catalogs/pg_index.md)
    * [51.54. pg\_tablespace](internals/system-catalogs/pg_tablespace.md)
    * [51.81 pg\_roles](internals/system-catalogs/pg_roles.md)
  * [52. Frontend/Backend Protocol](internals/52.-frontend-backend-protocol/README.md)
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
  * 64. GIN 索引
    * [64.1. 簡介](internals/gin-indexes/introduction.md)
    * [64.2. Built-in Operator Classes](internals/gin-indexes/built-in-operator-classes.md)
    * [64.3. Extensibility](internals/gin-indexes/extensibility.md)
    * [64.4. Implementation](internals/gin-indexes/implementation.md)
    * [64.5. GIN Tips and Tricks](internals/gin-indexes/gin-tips-and-tricks.md)
    * [64.6. Limitations](internals/gin-indexes/limitations.md)
    * [64.7. Examples](internals/gin-indexes/examples.md)
  * [66. 資料庫實體儲存格式](internals/database-physical-storage/README.md)
    * [66.2. TOAST](internals/database-physical-storage/toast.md)
* [VIII. 附錄](appendix/README.md)
  * [A. PostgreSQL錯誤代碼](appendix/errcodes.md)
  * [B. 日期時間格式支援](appendix/datetime-appendix/README.md)
    * [B.1. 日期時間解譯流程](appendix/datetime-appendix/datetime-input-rules.md)
    * [B.2. 日期時間慣用字](appendix/datetime-appendix/datetime-keywords.md)
    * [B.3. 日期時間設定檔](appendix/datetime-appendix/datetime-config-files.md)
    * [B.4. 日期時間的沿革](appendix/datetime-appendix/datetime-units-history.md)
  * [C. SQL 關鍵字](appendix/sql-keywords.md)
  * [D. SQL 相容性](appendix/sql-conformance.md)
  * [E. 版本資訊](appendix/release-notes.md)
  * [F. 延伸支援模組](appendix/contrib/README.md)
    * [F.4. auto\_explain](appendix/contrib/auto_explain.md)
    * [F.11. dblink](appendix/contrib/f.11.-dblink/README.md)
      * [dblink](appendix/contrib/f.11.-dblink/dblink.md)
  * [G. Additional Supplied Programs](appendix/additional-supplied-programs/README.md)
    * [G.1. Client Applications](appendix/additional-supplied-programs/g.1.-client-applications/README.md)
      * [oid2name](appendix/additional-supplied-programs/g.1.-client-applications/oid2name.md)
      * [vacuumlo](appendix/additional-supplied-programs/g.1.-client-applications/untitled.md)
    * [G.2. Server Applications](appendix/additional-supplied-programs/g.2.-server-applications/README.md)
      * [pg\_standby](appendix/additional-supplied-programs/g.2.-server-applications/pg_standby.md)
  * [H. 外部專案](appendix/external-projects/README.md)
    * [H.1. 用戶端介面](appendix/external-projects/client-interface.md)
    * [H.2. Administration Tools](appendix/external-projects/h.2.-administration-tools.md)
    * [H.3. Procedural Languages](appendix/external-projects/untitled.md)
    * [H.4. Extensions](appendix/external-projects/h.4.-extensions.md)
  * [I. The Source Code Repository](appendix/the-source-code-repository/README.md)
    * [I.1. Getting The Source via Git](appendix/the-source-code-repository/i.1.-getting-the-source-via-git.md)
  * [J. 文件取得](appendix/docguide.md)
  * [K. 縮寫字](appendix/acronyms.md)
* [參考書目](biblio.md)

