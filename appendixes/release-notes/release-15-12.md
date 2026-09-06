<a id="RELEASE-15-12"></a>

# E.8. Release 15.12

[E.8.1. Migration to Version 15.12](#id-1.11.6.13.4)

[E.8.2. Changes](#id-1.11.6.13.5)

<strong>Release date: </strong>2025-02-20

This release contains a few fixes from 15.11. For information about new features in major release 15, see [Section E.20](e.3.-release-15.md).

<a id="id-1.11.6.13.4"></a>

## E.8.1. Migration to Version 15.12

A dump/restore is not required for those running 15.X.

However, if you are upgrading from a version earlier than 15.9, see [Section E.11](release-15-9.md).

<a id="id-1.11.6.13.5"></a>

## E.8.2. Changes

* Improve behavior of libpq's quoting functions (Andres Freund, Tom Lane) [§](https://postgr.es/c/22ffbbf24) [§](https://postgr.es/c/e782a63cc) [§](https://postgr.es/c/2226a2e26)

  The changes made for CVE-2025-1094 had one serious oversight: `PQescapeLiteral()` and `PQescapeIdentifier()` failed to honor their string length parameter, instead always reading to the input string's trailing null. This resulted in including unwanted text in the output, if the caller intended to truncate the string via the length parameter. With very bad luck it could cause a crash due to reading off the end of memory.

  In addition, modify all these quoting functions so that when invalid encoding is detected, an invalid sequence is substituted for just the first byte of the presumed character, not all of it. This reduces the risk of problems if a calling application performs additional processing on the quoted string.

---

原文：[PostgreSQL 15.19 Documentation](release-15-12.md)（英文原文，待翻譯）
