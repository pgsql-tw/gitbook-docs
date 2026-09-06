<a id="SPI-SPI-FNUMBER"></a><a id="id-1.8.12.9.5.1"></a>

# SPI_fnumber

SPI_fnumber — determine the column number for the specified column name

## Synopsis

```

int SPI_fnumber(TupleDesc rowdesc, const char * colname)
```

<a id="id-1.8.12.9.5.5"></a>

## Description

`SPI_fnumber` returns the column number for the column with the specified name.

If <em class="parameter"><code>colname</code></em> refers to a system column (e.g., `ctid`) then the appropriate negative column number will be returned. The caller should be careful to test the return value for exact equality to `SPI_ERROR_NOATTRIBUTE` to detect an error; testing the result for less than or equal to 0 is not correct unless system columns should be rejected.

<a id="id-1.8.12.9.5.6"></a>

## Arguments

<code class="literal">TupleDesc <em class="parameter"><code>rowdesc</code></em></code>

input row description

<code class="literal">const char &#42; <em class="parameter"><code>colname</code></em></code>

column name

<a id="id-1.8.12.9.5.7"></a>

## Return Value

Column number (count starts at 1 for user-defined columns), or `SPI_ERROR_NOATTRIBUTE` if the named column was not found.

---

原文：[PostgreSQL 15.19 Documentation](spi-spi-fnumber.md)（英文原文，待翻譯）
