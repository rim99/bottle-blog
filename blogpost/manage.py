#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

'''
extension_map = {
    'tables': EXT_TABLES,
    'autolink': EXT_AUTOLINK,
    'fenced-code': EXT_FENCED_CODE,
    'strikethrough': EXT_STRIKETHROUGH,
    'disable-indented-code': EXT_DISABLE_INDENTED_CODE,

--- 'underline': EXT_UNDERLINE,

    EXAMPLE:
        _That's some text with a footnote._
      into:
        <u>That's some text with a footnote._</u>
      and
        __REMAIN STRONG__


--- 'footnotes': EXT_FOOTNOTES,

    EXAMPLE:
        That's some text with a footnote.[^1]
        [^1]: And that's the footnote.
            That's the second paragraph.


--- 'highlight': EXT_HIGHLIGHT,
        Enables ==marking== text.


--- 'quote': EXT_QUOTE,
        “Quotes” are translated into <q> tags.

    EXAMPLE:
        “Quotes” are translated into <q> tags.
        <p>Luke continued, <q>And then she called him a <q>scruffy-looking nerf-herder</q>!
        I think I’ve got a chance!</q> The poor naive fool…</p>
      into:
        Luke continued, "And then she called him a 'scruffy-looking nerf-herder'!
        I think I’ve got a chance!" The poor naive fool…


--- 'superscript': EXT_SUPERSCRIPT,
        Enables super^script. Still use the <sub></sub> tag.

    EXAMPLE:
        Function(X^2 *10)
      into:
        <p>Function(X<sup>2</sup> *10)</p>


--- 'math': EXT_MATH,
        Search 'MathJax' for detail.


--- 'no-intra-emphasis': EXT_NO_INTRA_EMPHASIS,
        Disables emphasis_between_words.


--- 'space-headers': EXT_SPACE_HEADERS,
        ATX style headers require a space after the opening number sign(s).


--- 'math-explicit': EXT_MATH_EXPLICIT,
        Unknown
}
'''

from pathlib import PurePosixPath
from misaka import Markdown, HtmlRenderer
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from blogpost.models import BlogPost
import houdini

MARKDOWN_EXTENSIONS = (
    'autolink',
    'strikethrough',
    'underline',
    'tables',
    'fenced-code',
    'footnotes',
    'highlight',
    'quote',
    'superscript',
    'math',
    'space-headers',
    'math-explicit',
    'disable-indented-code'
)  # remove 'no-intra-emphasis'

class HighlighterRenderer(HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(
                houdini.escape_html(text.strip()))
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

def saveFile(file, category=''):
    if category == '':
        print('No tag! Abort.')
        return
    rndr = HighlighterRenderer()
    md = Markdown(rndr, MARKDOWN_EXTENSIONS)
    with open(file, 'r', encoding='utf-8') as f:
        title = ''
        for line in f:
            title = line[1:]
            break
        content_html = (md(f.read()))
    blog_id = PurePosixPath(file).stem  # use the filename without the extension as the blog_id
    new_blog = BlogPost(title, category, content_html, blog_id)
    old = BlogPost.query(blog_id)
    if isinstance(old, BlogPost):
        print("The same blog id already exists. \nOverwriting......")
        old.delete()
    else:
        print("New blog. Posting...")
    new_blog.save()
    return

def list_all():
    try:
        blog_posts = BlogPost.getAll()
        for blog in blog_posts:
            print(blog_posts.index(blog))
            blog.print()
    except:
        print('Error when list all files!')

def list_by_tag(tag):
    blog_posts = BlogPost.queryByTag(tag)
    if len(blog_posts) == 0:
        print('No file was found by tag: %s!' % tag)
    for blog in blog_posts:
        print(blog_posts.index(blog))
        blog.print()

def deleteFile(blog_id=''):
    if blog_id == '':
        blog_posts = BlogPost.getAll()
        last_blog = blog_posts[-1]
        blog_id = last_blog.blog_id
    try:
        BlogPost.delete_by_id(blog_id)
    except:
        print("Error!")
    return
