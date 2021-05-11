
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension



class CCommentInline(InlineProcessor):
    """Drop all c-style comments
    
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


class CCommentExtension(Extension):
    def extendMarkdown(self, md):
        # Comments
        md.inlinePatterns.register(CCommentInline(md), 'c_comments', 1040)
