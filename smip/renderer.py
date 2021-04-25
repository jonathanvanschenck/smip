import re

import xml.etree.ElementTree as etree
from markdown import Markdown
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension


class NoRender(Preprocessor):
    """Skip lines starting with a `.`"""
    def run(self, lines):
        _lines = []

        for line in lines:
            if not line.strip()[:1] == ".":
                _lines.append(line)

        return _lines


class DropComments(InlineProcessor):
    """Drop all comments

    Comment Types:
    //     = comment to EOL

    /*  */ = comment inline

    /*
     *     = comment block
     */
    """
    def __init__(self,*args,**kwargs):
        super().__init__(r"/", *args, **kwargs)


    def handleMatch(self, m, data):
        el, start, end = None, None, None
        offset = m.start(0) + 1
        substring = data[m.start(0)+1:]
        if substring[:1] == "/":
            # Handle EOL comment
            try:
                end = substring.index('\n') + offset + 1
            except ValueError:
                # No CR, so grab the whole substring
                end = len(substring) + offset + 1
            if not end is None:
                el = ""
                start = m.start(0)

        elif substring[:1] == '*':
            # Handle inline and block
            try:
                end = substring.index('*/') + offset + 2
            except:
                pass
            if not end is None:
                el = ""
                start = m.start(0)
                # Capture CR for block comments
                if "\n" in substring[start:end] and substring[end:end+1] == "\n":
                    end += 1
        else:
            pass

        return (el, start, end)

class ClassedTagInline(InlineProcessor):
    """Wraps m.group(1) in a tag with classes"""

    def __init__(self, md, regex, tag, classes=[], string_parser=lambda x:x):
        super().__init__(regex,md)
        self.tag = tag
        self.classes = " ".join(classes)
        self.parser = string_parser

    def handleMatch(self, m, data):
        el = etree.Element(self.tag)
        el.text = self.parser(m.group(1))
        el.set("class", self.classes)
        el.set("style", "color: red;")
        return el, m.start(0), m.end(0)

class UnescapeCharacter(InlineProcessor):
    """Removes all preceeding backslashes (\) from a character"""
    def __init__(self, md, char):
        super().__init__("\\\\" + re.escape(char), md)
        self.char = char

    def handleMatch(self, m, data):
        return self.char, m.start(0), m.end(0)


def get_inline_reference(string, index_file = None):
    # TODO
    return string

def get_block_reference(string, index_file = None):
    # TODO
    return string

def get_reference_only(string):
    # TODO
    return 2*string

class ScriptureExtension(Extension):
    def __init__(self, **kwargs):
        self.config = dict(
            index_file = [None, 'file path to the scripture index']
        )
        super(ScriptureExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        # Comments
        md.inlinePatterns.register(DropComments(md), 'drop_comments', 104)

        # Block scripture references
        md.inlinePatterns.register(
            ClassedTagInline(
                md, 
                r"(?<!\\)\$\$\$([^$]+)\$\$\$", 
                "div", 
                ["reference", "reference-block"],
                lambda string : get_block_reference(string, self.config["index_file"])
            ),
            'reference_block',
            103
        )

        # Scripture references
        md.inlinePatterns.register(
            ClassedTagInline(
                md, 
                r"(?<!\\)\$\$([^$]+)\$\$", 
                "span", 
                ["reference", "reference-inline"],
                get_reference_only
            ),
            'reference_inline',
            102
        )

        # Scripture quotations inline
        md.inlinePatterns.register(
            ClassedTagInline(
                md, 
                r"(?<!\\)\$([^$]+)\$", 
                "span", 
                ["scripture", "scripture-inline"],
                lambda string : get_inline_reference(string, self.config["index_file"])
            ),
            'scripture_inline',
            101
        )

        # Remove the escape character from $
        md.inlinePatterns.register(UnescapeCharacter(md, "$"), 'unescape_$', 0)


md = Markdown(
    extensions=[
        ScriptureExtension(index_file = None)
    ]
)
