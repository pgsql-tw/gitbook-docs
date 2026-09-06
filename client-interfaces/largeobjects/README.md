## Chapter 33. Large Objects

**Table of Contents**

[33.1. Introduction](lo-intro.md)

[33.2. Implementation Features](lo-implementation.md)

[33.3. Client Interfaces](lo-interfaces.md)
:   [33.3.1. Creating a Large Object](lo-interfaces.md#LO-CREATE)

    [33.3.2. Importing a Large Object](lo-interfaces.md#LO-IMPORT)

    [33.3.3. Exporting a Large Object](lo-interfaces.md#LO-EXPORT)

    [33.3.4. Opening an Existing Large Object](lo-interfaces.md#LO-OPEN)

    [33.3.5. Writing Data to a Large Object](lo-interfaces.md#LO-WRITE)

    [33.3.6. Reading Data from a Large Object](lo-interfaces.md#LO-READ)

    [33.3.7. Seeking in a Large Object](lo-interfaces.md#LO-SEEK)

    [33.3.8. Obtaining the Seek Position of a Large Object](lo-interfaces.md#LO-TELL)

    [33.3.9. Truncating a Large Object](lo-interfaces.md#LO-TRUNCATE)

    [33.3.10. Closing a Large Object Descriptor](lo-interfaces.md#LO-CLOSE)

    [33.3.11. Removing a Large Object](lo-interfaces.md#LO-UNLINK)

[33.4. Server-Side Functions](lo-funcs.md)

[33.5. Example Program](lo-examplesect.md)

<a id="id-1.7.4.2"></a><a id="id-1.7.4.3"></a>

PostgreSQL has a *large object*
facility, which provides stream-style access to user data that is stored
in a special large-object structure. Streaming access is useful
when working with data values that are too large to manipulate
conveniently as a whole.

This chapter describes the implementation and the programming and
query language interfaces to PostgreSQL
large object data. We use the libpq C
library for the examples in this chapter, but most programming
interfaces native to PostgreSQL support
equivalent functionality. Other interfaces might use the large
object interface internally to provide generic support for large
values. This is not described here.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/largeobjects.html)（英文原文，待翻譯）
