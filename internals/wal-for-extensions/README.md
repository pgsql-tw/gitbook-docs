## Chapter 64. Write Ahead Logging for Extensions

**Table of Contents**

[64.1. Generic WAL Records](generic-wal.md)

[64.2. Custom WAL Resource Managers](custom-rmgr.md)

Certain extensions, principally extensions that implement custom access
methods, may need to perform write-ahead logging in order to ensure
crash-safety. PostgreSQL provides two ways
for extensions to achieve this goal.

First, extensions can choose to use [generic
WAL](generic-wal.md), a special type of WAL record which describes changes to pages
in a generic way. This method is simple to implement and does not require
that an extension library be loaded in order to apply the records. However,
generic WAL records will be ignored when performing logical decoding.

Second, extensions can choose to use a [custom
resource manager](custom-rmgr.md). This method is more flexible, supports logical
decoding, and can sometimes generate much smaller write-ahead log records
than would be possible with generic WAL. However, it is more complex for an
extension to implement.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/wal-for-extensions.html)（英文原文，待翻譯）
