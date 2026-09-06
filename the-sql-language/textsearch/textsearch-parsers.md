## 12.5. Parsers [#](#TEXTSEARCH-PARSERS)

Text search parsers are responsible for splitting raw document text
into *tokens* and identifying each token's type, where
the set of possible types is defined by the parser itself.
Note that a parser does not modify the text at all — it simply
identifies plausible word boundaries. Because of this limited scope,
there is less need for application-specific custom parsers than there is
for custom dictionaries. At present PostgreSQL
provides just one built-in parser, which has been found to be useful for a
wide range of applications.

The built-in parser is named `pg_catalog.default`.
It recognizes 23 token types, shown in [Table 12.1](textsearch-parsers.md#TEXTSEARCH-DEFAULT-PARSER).

<a id="TEXTSEARCH-DEFAULT-PARSER"></a>

**Table 12.1. Default Parser's Token Types**

<table border="1" class="table" summary="Default Parser's Token Types"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>Alias</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td><code class="literal">asciiword</code></td><td>Word, all ASCII letters</td><td><code class="literal">elephant</code></td></tr><tr><td><code class="literal">word</code></td><td>Word, all letters</td><td><code class="literal">mañana</code></td></tr><tr><td><code class="literal">numword</code></td><td>Word, letters and digits</td><td><code class="literal">beta1</code></td></tr><tr><td><code class="literal">asciihword</code></td><td>Hyphenated word, all ASCII</td><td><code class="literal">up-to-date</code></td></tr><tr><td><code class="literal">hword</code></td><td>Hyphenated word, all letters</td><td><code class="literal">lógico-matemática</code></td></tr><tr><td><code class="literal">numhword</code></td><td>Hyphenated word, letters and digits</td><td><code class="literal">postgresql-beta1</code></td></tr><tr><td><code class="literal">hword_asciipart</code></td><td>Hyphenated word part, all ASCII</td><td><code class="literal">postgresql</code> in the context <code class="literal">postgresql-beta1</code></td></tr><tr><td><code class="literal">hword_part</code></td><td>Hyphenated word part, all letters</td><td><code class="literal">lógico</code> or <code class="literal">matemática</code>
       in the context <code class="literal">lógico-matemática</code></td></tr><tr><td><code class="literal">hword_numpart</code></td><td>Hyphenated word part, letters and digits</td><td><code class="literal">beta1</code> in the context
       <code class="literal">postgresql-beta1</code></td></tr><tr><td><code class="literal">email</code></td><td>Email address</td><td><code class="literal">foo@example.com</code></td></tr><tr><td><code class="literal">protocol</code></td><td>Protocol head</td><td><code class="literal">http://</code></td></tr><tr><td><code class="literal">url</code></td><td>URL</td><td><code class="literal">example.com/stuff/index.html</code></td></tr><tr><td><code class="literal">host</code></td><td>Host</td><td><code class="literal">example.com</code></td></tr><tr><td><code class="literal">url_path</code></td><td>URL path</td><td><code class="literal">/stuff/index.html</code>, in the context of a URL</td></tr><tr><td><code class="literal">file</code></td><td>File or path name</td><td><code class="literal">/usr/local/foo.txt</code>, if not within a URL</td></tr><tr><td><code class="literal">sfloat</code></td><td>Scientific notation</td><td><code class="literal">-1.234e56</code></td></tr><tr><td><code class="literal">float</code></td><td>Decimal notation</td><td><code class="literal">-1.234</code></td></tr><tr><td><code class="literal">int</code></td><td>Signed integer</td><td><code class="literal">-1234</code></td></tr><tr><td><code class="literal">uint</code></td><td>Unsigned integer</td><td><code class="literal">1234</code></td></tr><tr><td><code class="literal">version</code></td><td>Version number</td><td><code class="literal">8.3.0</code></td></tr><tr><td><code class="literal">tag</code></td><td>XML tag</td><td><code class="literal">&lt;a href="dictionaries.html"&gt;</code></td></tr><tr><td><code class="literal">entity</code></td><td>XML entity</td><td><code class="literal">&amp;amp;</code></td></tr><tr><td><code class="literal">blank</code></td><td>Space symbols</td><td>(any whitespace or punctuation not otherwise recognized)</td></tr></tbody></table>

<br>

### Note

The parser's notion of a “letter” is determined by the database's
locale setting, specifically `lc_ctype`. Words containing
only the basic ASCII letters are reported as a separate token type,
since it is sometimes useful to distinguish them. In most European
languages, token types `word` and `asciiword`
should be treated alike.

`email` does not support all valid email characters as
defined by [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322).
Specifically, the only non-alphanumeric characters supported for
email user names are period, dash, and underscore.

`tag` does not support all valid tag names as defined by
[W3C Recommendation, XML](https://www.w3.org/TR/xml/).
Specifically, the only tag names supported are those starting with an
ASCII letter, underscore, or colon, and containing only letters, digits,
hyphens, underscores, periods, and colons. `tag` also
includes XML comments starting with `<!--` and ending
with `-->`, and XML declarations (but note that this
includes anything starting with `<?x` and ending with
`>`).

It is possible for the parser to produce overlapping tokens from the same
piece of text. As an example, a hyphenated word will be reported both
as the entire word and as each component:

```

SELECT alias, description, token FROM ts_debug('foo-bar-beta1');
      alias      |               description                |     token
-----------------+------------------------------------------+---------------
 numhword        | Hyphenated word, letters and digits      | foo-bar-beta1
 hword_asciipart | Hyphenated word part, all ASCII          | foo
 blank           | Space symbols                            | -
 hword_asciipart | Hyphenated word part, all ASCII          | bar
 blank           | Space symbols                            | -
 hword_numpart   | Hyphenated word part, letters and digits | beta1
```

This behavior is desirable since it allows searches to work for both
the whole compound word and for components. Here is another
instructive example:

```

SELECT alias, description, token FROM ts_debug('http://example.com/stuff/index.html');
  alias   |  description  |            token
----------+---------------+------------------------------
 protocol | Protocol head | http://
 url      | URL           | example.com/stuff/index.html
 host     | Host          | example.com
 url_path | URL path      | /stuff/index.html
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/textsearch-parsers.html)（英文原文，待翻譯）
