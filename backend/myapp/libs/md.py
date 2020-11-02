# -*- coding: utf-8 -*-
'''
将 markdown 文档转为 html，同时生成目录
'''

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class TocMixin:
    """TOC mixin for Renderer, mix this with Renderer::
        class TocRenderer(TocMixin, Renderer):
            pass
        toc = TocRenderer()
        md = mistune.Markdown(renderer=toc)
        # required in this order
        toc.reset_toc()          # initial the status
        md.parse(text)           # parse for headers
        toc.render_toc(level=3)  # render TOC HTML
    """

    def reset_toc(self):
        self.toc_tree = []
        self.toc_count = 0

    def header(self, text, level, raw=None):
        rv = '<h%d id="toc-%d">%s</h%d>\n' % (
            level, self.toc_count, text, level
        )
        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv

    def render_toc(self, level=3):
        """Render TOC to HTML.
        :param level: render toc to the given level
        """
        return ''.join(self._iter_toc(level))

    def _iter_toc(self, level):
        first_level = 0
        last_level = 0

        yield '<div id="toc" class="toc-article"><strong class="toc-title">目录</strong><ol class="toc">\n'  # noqa

        for toc in self.toc_tree:
            index, text, l, raw = toc
            title = text.replace(' ', '')

            if l > level:
                # ignore this level
                continue

            if first_level == 0:
                # based on first level
                first_level = l
                last_level = l
                yield f'<li class="toc-item toc-level-{l - 1}"><a class="toc-link" href="#{title}"><span class="toc-text">{text}</span></a>'  # noqa
            elif last_level == l:
                yield f'</li>\n<li class="toc-item toc-level-{l - 1}"><a class="toc-link" href="#{title}"><span class="toc-text">{text}</span></a>'  # noqa
            elif last_level == l - 1:
                last_level = l
                yield f'<ol class="toc-child">\n<li class="toc-item toc-level-{l - 1}"><a class="toc-link" href="#{title}"><span class="toc-text">{text}</span></a>'  # noqa
            elif last_level > l:
                yield '</li>'
                while last_level > l:
                    yield '</ol>\n</li>\n'
                    last_level -= 1
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)

        # close tags
        yield '</li>\n'
        while last_level > first_level:
            yield '</ul>\n</li>\n'
            last_level -= 1

        yield '</ul></div>\n'


class BlogHtmlFormatter(HtmlFormatter):

    def __init__(self, **options):
        super().__init__(**options)
        self.lang = options.get('lang', '')

    def _wrap_div(self, inner):
        style = []
        if (self.noclasses and not self.nobackground and
                self.style.background_color is not None):
            style.append('background: %s' % (self.style.background_color,))
        if self.cssstyles:
            style.append(self.cssstyles)
        style = '; '.join(style)

        yield 0, ('<figure' + (self.cssclass and ' class="%s"' % self.cssclass) +  # noqa
                  (style and (' style="%s"' % style)) +
                  (self.lang and ' data-lang="%s"' % self.lang) +
                  '><table><tbody><tr><td class="code">')
        for tup in inner:
            yield tup
        yield 0, '</table></figure>\n'

    def _wrap_pre(self, inner):
        style = []
        if self.prestyles:
            style.append(self.prestyles)
        if self.noclasses:
            style.append('line-height: 125%')
        style = '; '.join(style)

        if self.filename:
            yield 0, ('<span class="filename">' + self.filename + '</span>')

        # the empty span here is to keep leading empty lines from being
        # ignored by HTML parsers
        yield 0, ('<pre' + (style and ' style="%s"' % style) + (
            self.lang and f' class="hljs {self.lang}"') + '><span></span>')
        for tup in inner:
            yield tup
        yield 0, '</pre>'


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return '<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = BlogHtmlFormatter(
            noclasses=inlinestyles, linenos=linenos,
            cssclass='highlight %s' % lang, lang=lang
        )
        code = highlight(text, lexer, formatter)
        return code
    except Exception:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


class TocRenderer(TocMixin, mistune.Renderer):
    pass


class BlogRenderer(mistune.Renderer):

    def header(self, text, level, raw=None):
        hid = text.replace(' ', '')
        return f'<h{level} id="{hid}">{text}</h{level}>\n'

    def block_code(self, text, lang):
        inlinestyles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')
        return block_code(text, lang, inlinestyles, linenos)


renderer = BlogRenderer()
toc = TocRenderer()
markdown = mistune.Markdown(renderer=renderer)
toc_md = mistune.Markdown(renderer=toc)
