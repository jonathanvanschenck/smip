import re
import biblescrapeway as bsw

import xml.etree.ElementTree as etree
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension


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
        return el, m.start(0), m.end(0)

class UnescapeCharacter(InlineProcessor):
    """Removes all preceeding backslashes (\) from a character"""
    def __init__(self, md, char):
        super().__init__("\\\\" + re.escape(char), md)
        self.char = char

    def handleMatch(self, m, data):
        return self.char, m.start(0), m.end(0)


def get_reference_text(string, cache = True, cache_fp = None, version = "ESV"):
    # if there is a "`" in the string, render literally.
    if '`' in string:
        return string
    
    # discover the version, if any specified
    m = re.search("[ ]*\(([A-Z]+)\)[ ]*", string)
    if not m is None:
        version = m.group(1)
        string = string[:m.start(0)] + string[m.end(0):]
    
    try:
        verse_list = bsw.query(string, cache = cache, cache_fp = cache_fp, version = version)
    except bsw.errors.ReferenceError:
        return "Error parsing: '{}'".format(string)
    
    # FIXME : be intellegent about if it should be a space or not that delimits verses
    verse_string = " ".join([ v.text for v in verse_list ])
    return '{} : \`'.format(get_reference_only(string)) + verse_string + '\`' + " ({})".format(version)

def get_reference_only(string):
    """Get a normalized reference string for a list of references"""
    try:
        string = bsw.reference.shorten_reference_string(string)
    except bsw.errors.ReferenceError:
        return "Error parsing: '{}'".format(string)

    return string
        

class ScriptureExtension(Extension):
    def __init__(self, **kwargs):
        self.config = dict(
            cache_fp = None, #[None, 'File path for scripture cache, default is ~/.bsw_cache.json'],
            cache = True, #[True, 'Boolean to decide if biblescrapeway should cache bible verse. Default is True'],
            version_default = "ESV" # ["ESV", "Default bible version to use, unless specified in the markdown document"]
        )
        super(ScriptureExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        # Block scripture references
        md.inlinePatterns.register(
            ClassedTagInline(
                md, 
                r"(?<!\\)\$\$\$([^$]+)\$\$\$", 
                "div", 
                ["reference", "reference-block"],
                lambda string : get_reference_text(string, cache_fp = self.config["cache_fp"], cache = self.config["cache"], version = self.config["version_default"])
            ),
            'reference_block',
            1030
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
            1020
        )

        # Scripture quotations inline
        md.inlinePatterns.register(
            ClassedTagInline(
                md, 
                r"(?<!\\)\$([^$]+)\$", 
                "span", 
                ["scripture", "scripture-inline"],
                lambda string : get_reference_text(string, cache_fp = self.config["cache_fp"], cache = self.config["cache"], version = self.config["version_default"])
            ),
            'scripture_inline',
            1010
        )

        # Remove the escape character from $
        md.inlinePatterns.register(UnescapeCharacter(md, "$"), 'unescape_$', 0)
