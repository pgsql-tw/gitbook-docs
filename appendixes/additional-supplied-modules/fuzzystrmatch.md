<a id="FUZZYSTRMATCH"></a>

# F.17. fuzzystrmatch

[F.17.1. Soundex](#id-1.11.7.26.6)

[F.17.2. Levenshtein](#id-1.11.7.26.7)

[F.17.3. Metaphone](#id-1.11.7.26.8)

[F.17.4. Double Metaphone](#id-1.11.7.26.9)

<a id="id-1.11.7.26.2"></a>

The `fuzzystrmatch` module provides several functions to determine similarities and distance between strings.

## Caution

At present, the `soundex`, `metaphone`, `dmetaphone`, and `dmetaphone_alt` functions do not work well with multibyte encodings (such as UTF-8).

This module is considered “trusted”, that is, it can be installed by non-superusers who have `CREATE` privilege on the current database.

<a id="id-1.11.7.26.6"></a>

## F.17.1. Soundex

The Soundex system is a method of matching similar-sounding names by converting them to the same code. It was initially used by the United States Census in 1880, 1900, and 1910. Note that Soundex is not very useful for non-English names.

The `fuzzystrmatch` module provides two functions for working with Soundex codes:

<a id="id-1.11.7.26.6.4"></a><a id="id-1.11.7.26.6.5"></a>

```

soundex(text) returns text
difference(text, text) returns int
```

The `soundex` function converts a string to its Soundex code. The `difference` function converts two strings to their Soundex codes and then reports the number of matching code positions. Since Soundex codes have four characters, the result ranges from zero to four, with zero being no match and four being an exact match. (Thus, the function is misnamed — `similarity` would have been a better name.)

Here are some usage examples:

```

SELECT soundex('hello world!');

SELECT soundex('Anne'), soundex('Ann'), difference('Anne', 'Ann');
SELECT soundex('Anne'), soundex('Andrew'), difference('Anne', 'Andrew');
SELECT soundex('Anne'), soundex('Margaret'), difference('Anne', 'Margaret');

CREATE TABLE s (nm text);

INSERT INTO s VALUES ('john');
INSERT INTO s VALUES ('joan');
INSERT INTO s VALUES ('wobbly');
INSERT INTO s VALUES ('jack');

SELECT * FROM s WHERE soundex(nm) = soundex('john');

SELECT * FROM s WHERE difference(s.nm, 'john') > 2;
```

<a id="id-1.11.7.26.7"></a>

## F.17.2. Levenshtein

This function calculates the Levenshtein distance between two strings:

<a id="id-1.11.7.26.7.3"></a><a id="id-1.11.7.26.7.4"></a>

```

levenshtein(text source, text target, int ins_cost, int del_cost, int sub_cost) returns int
levenshtein(text source, text target) returns int
levenshtein_less_equal(text source, text target, int ins_cost, int del_cost, int sub_cost, int max_d) returns int
levenshtein_less_equal(text source, text target, int max_d) returns int
```

Both `source` and `target` can be any non-null string, with a maximum of 255 characters. The cost parameters specify how much to charge for a character insertion, deletion, or substitution, respectively. You can omit the cost parameters, as in the second version of the function; in that case they all default to 1.

`levenshtein_less_equal` is an accelerated version of the Levenshtein function for use when only small distances are of interest. If the actual distance is less than or equal to `max_d`, then `levenshtein_less_equal` returns the correct distance; otherwise it returns some value greater than `max_d`. If `max_d` is negative then the behavior is the same as `levenshtein`.

Examples:

```

test=# SELECT levenshtein('GUMBO', 'GAMBOL');
 levenshtein
-------------
           2
(1 row)

test=# SELECT levenshtein('GUMBO', 'GAMBOL', 2, 1, 1);
 levenshtein
-------------
           3
(1 row)

test=# SELECT levenshtein_less_equal('extensive', 'exhaustive', 2);
 levenshtein_less_equal
------------------------
                      3
(1 row)

test=# SELECT levenshtein_less_equal('extensive', 'exhaustive', 4);
 levenshtein_less_equal
------------------------
                      4
(1 row)
```

<a id="id-1.11.7.26.8"></a>

## F.17.3. Metaphone

Metaphone, like Soundex, is based on the idea of constructing a representative code for an input string. Two strings are then deemed similar if they have the same codes.

This function calculates the metaphone code of an input string:

<a id="id-1.11.7.26.8.4"></a>

```

metaphone(text source, int max_output_length) returns text
```

`source` has to be a non-null string with a maximum of 255 characters. `max_output_length` sets the maximum length of the output metaphone code; if longer, the output is truncated to this length.

Example:

```

test=# SELECT metaphone('GUMBO', 4);
 metaphone
-----------
 KM
(1 row)
```

<a id="id-1.11.7.26.9"></a>

## F.17.4. Double Metaphone

The Double Metaphone system computes two “sounds like” strings for a given input string — a “primary” and an “alternate”. In most cases they are the same, but for non-English names especially they can be a bit different, depending on pronunciation. These functions compute the primary and alternate codes:

<a id="id-1.11.7.26.9.3"></a><a id="id-1.11.7.26.9.4"></a>

```

dmetaphone(text source) returns text
dmetaphone_alt(text source) returns text
```

There is no length limit on the input strings.

Example:

```

test=# SELECT dmetaphone('gumbo');
 dmetaphone
------------
 KMP
(1 row)
```

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/fuzzystrmatch.html)（英文原文，待翻譯）
