# coding='utf8'
import bidi.algorithm as bidi
import six


def print_storage_chars(storage):
    string=''
    dir_list = []
    ws_list = []
    for i in storage['chars']:
        dir_list.append(i['type'])
        ws_list.append(i['orig'])
        string=string+i['ch']

    char_types = tuple(zip(dir_list, ws_list))

    markers=[0]
    # set markers where wb seperates direction:
    for i in range(1, len(char_types)):
        if (
            char_types[i][1] == 'WS' and
            char_types[i-1][0] != char_types[i+1][0]
            ):
            markers.append(i)
    markers.append(len(char_types))
    
    return_list=[]
    for i in range(1,len(markers)):
        substring=string[markers[i-1]:markers[i]]

        if substring.startswith(' '):
            substring=substring[1:]
        return_list.append(bidi.get_display(substring))

    return ' '.join(return_list)


def get_display_mod(unicode_or_str, encoding='utf-8', upper_is_rtl=False,
                    base_dir=None, debug=False):
    """Accepts unicode or string. In case it's a string, `encoding`
    is needed as it works on unicode ones (default:"utf-8").
    Set `upper_is_rtl` to True to treat upper case chars as strong 'R'
    for debugging (default: False).
    Set `base_dir` to 'L' or 'R' to override the calculated base_level.
    Set `debug` to True to display (using sys.stderr) the steps taken with the
    algorithm.
    Returns the display layout, either as unicode or `encoding` encoded
    string.
    """
    storage = bidi.get_empty_storage()

    # utf-8 ? we need unicode
    if isinstance(unicode_or_str, six.text_type):
        text = unicode_or_str
        decoded = False
    else:
        text = unicode_or_str.decode(encoding)
        decoded = True

    if base_dir is None:
        base_level = bidi.get_base_level(text, upper_is_rtl)
    else:
        base_level = bidi.PARAGRAPH_LEVELS[base_dir]

    storage['base_level'] = base_level
    storage['base_dir'] = ('L', 'R')[base_level]

    bidi.get_embedding_levels(text, storage, upper_is_rtl, debug)
    bidi.explicit_embed_and_overrides(storage, debug)
    bidi.resolve_weak_types(storage, debug)
    bidi.resolve_neutral_types(storage, debug)
    bidi.resolve_implicit_levels(storage, debug)
    bidi.reorder_resolved_levels(storage, debug)
    #Commented out from original code:
    # bidi.apply_mirroring(storage, debug)
    # print_storage_chars(storage)
    # chars = storage['chars']
    # display = u''.join([_ch['ch'] for _ch in chars])
    display = print_storage_chars(storage)

    if decoded:
        return display.encode(encoding)
    else:
        return display

test_string="טקסט שבמרכזו יש מילה ב ENGLISH אך הוא מתחיל בעברית"