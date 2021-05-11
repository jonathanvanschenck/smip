"""
What do I need to do?

1) take a non-standard string and form a standard string reference
2) take a range and create a standard string reference
3) take either lookup or query a range via BSW
"""





import biblescrapeway as bsw

class Parser:
    def __init__(self, string):
        self.range_litwst = string
        (\[)[a-z]+(\])


def get_reference_text(string, index_file = None, version = "ESV"):
#     # if "'" in string or '"' in string:
#     #     return string
#     # print(string)
#     if '`' in string:
#         return string
#     
#     m = re.search("[ ]*\(([A-Z]+)\)[ ]*", string)
#     if not m is None:
#         version = m.group(1)
#         string = string[:m.start(0)] + string[m.end(0):]
#     try:
#         ref_list = bsw.reference.parse_reference_string(string)
#     except:
#         return "Error parsing: '{}'".format(string)
   
    ref_list = bsw.reference.parse_reference_string(string)
    string_list = []
    for r in ref_list:
        # TODO : add lookup in index file
        
        if r.start.equals(r.end) and not r.start.verse is None:
            verse = bsw.scrap(r.start, version)
            sub = verse.text
        else:
            verses = []
            for chap in range(r.start.chapter,r.end.chapter+1):
                verses += bsw.scrap(bsw.reference.Reference(r.start.book,chap,None),version)
            sub = " ".join([v.text for v in verses if r.contains(v)])
        
        string_list.append(sub)

        # TODO : save queries in index file

    return '{} : \`'.format(get_reference_only(string)) + " ... ".join(string_list) + '\`' + " ({})".format(version)

# def get_block_reference(string, index_file = None):
#     # TODO
#     return string

def get_reference_only(string):
    """Get a normalized reference string for a list of references"""
    try:
        ref_list = bsw.reference.parse_reference_string(string)
    except:
        return "Error parsing: '{}'".format(string)

    previous_book, previous_chapter, previous_verse = None, None, None
    string_list = []

    for r in ref_list:
        sub = ""
        # Handle single verse reference
        #  HACK : .is_single is broken for chapters
        if (r.start.equals(r.end)):
            full_string = r.start.to_string().strip(" ")
            if previous_book != r.start.book:
                sub = full_string
            elif (
                # get C:V if previous is different
                #  chapter, or previous is an
                #  entire chapter
                previous_chapter != r.start.chapter\
                or previous_verse is None
            ):
                sub = full_string.split(" ")[-1]
            else:
                sub = full_string.split(":")[-1]
        # Handle range reference
        else:
            if previous_book != r.start.book:
                sub = "{} ".format(r.start.book)
            if (
                previous_chapter != r.start.chapter\
                or previous_verse is None
            ):
                sub = sub + str(r.start.chapter)
            if not r.start.verse is None:
                sub = sub + ":{}-".format(r.start.verse)
            else:
                sub = sub + "-"
            if (
                r.start.chapter != r.end.chapter\
                or r.start.verse is None
            ):
                sub = sub + str(r.end.chapter)
                if not r.end.verse is None:
                    sub = sub + ":{}".format(r.end.verse)
            else:
                sub = sub + str(r.end.verse)

        # Prepare next loop
        previous_book, previous_chapter, previous_verse = r.end.book, r.end.chapter, r.end.verse
        string_list.append(sub)
    return ", ".join(string_list)
        
