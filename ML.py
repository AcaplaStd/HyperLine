# ULTRA MARKUP LANGUAGE
# better than html

# Этому коду надо:
# - научиться разделять теги в head от тегов в body, а то ему грустно
# - научиться иметь строку внутри команду (в  div class='main-div' 'hi'  не надо определять 'hi' как аргумент для тега)

from sys import stdin
import re


def is_word(s):
    return True if s[0].isalpha() and s[1:].isalnum() else False


def ERROR(code: int, s: str):
    print(f'\nERROR {code}: {s}\n')
    exit(code)


def is_attr_needed():
    if attr:
        ERROR(201, 'Attribute value expected')


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.val = value

    def to_string(self):
        if self.val is None:
            return self.type
        return self.type + ': ' + str(self.val)


tokens = []
single_tags = ['area', 'base', 'basefont', 'bgsound', 'br', 'col', 'command', 'embed', 'hr', 'img',
               'input', 'isindex', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']  # Незакрывающиеся теги
paired_tags = ['!DOCTYPE', 'a', 'abbr', 'address', 'article', 'aside', 'audio', 'b', 'bdi', 'bdo', 'blockquote',
        'body', 'button', 'canvas', 'caption', 'cite', 'code', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details',
        'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2',
        'h3', 'h4', 'h5', 'h6', 'head', 'header', 'html', 'i', 'iframe', 'ins', 'kbd', 'label', 'legend', 'li', 'main',
        'map', 'mark', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'picture',
        'pre', 'progress', 'q', 'ruby', 'rb', 'rt', 'rtc', 'rp', 's', 'samp', 'script', 'section', 'select', 'small',
        'span', 'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot',
        'th', 'thead', 'time', 'title', 'tr', 'u', 'ul', 'var', 'video']
quotes = "'" + '"'
h_sep = '\t'  # Разделитель иерархии
spaces = ' \t\n\r\x0b\x0c'
attr = False


def check(text):
    global tokens
    global attr

    if text:
        if text in paired_tags:
            is_attr_needed()
            tokens.append(Token(text, True))
        elif text in single_tags:
            is_attr_needed()
            tokens.append(Token(text, False))
        elif text[-1] == '=':
            if is_word(text[:-1]):
                tokens.append(Token('attr_name', text[:-1]))
                attr = True
            else:
                ERROR(102, 'Illegal attribute: ' + text)


def tokenize_text(text):
    global attr
    global tokens
    if attr:
        tokens.append(Token('attr_val', text))
        attr = False
    else:
        tokens.append(Token('TEXT', text))


def lexer(code):
    global tokens
    pag = -1
    for el in code:
        line = el.lstrip(h_sep).strip()  # сама строка
        lvl = (len(el) - len(line)) // len(h_sep)  # уровень вложенности
        if lvl > pag:
            pag += 1
        else:
            is_attr_needed()
            tokens += [Token('EOT')] * (pag - lvl + 1)  # End of tag

        string = False
        quote = ""
        buffer = ''
        i = 0
        while i < len(line):
            if string:
                if line[i] == quote:
                    string = False
                    tokenize_text(buffer)
                    buffer = ''
                elif line[i] == '\\':
                        i += 1
                        c = line[i]
                        if c == 'n':
                            c = '<br>'
                        buffer += c
                else:
                    buffer += line[i]
            elif line[i] in quotes:
                    string = True
                    quote = line[i]
                    check(buffer)
                    buffer = ''
            elif line[i] in spaces:
                while i < len(line) and line[i+1] in spaces:
                    i += 1
                check(buffer)
                buffer = ''
            elif line[i] == '=':
                buffer += '='
                check(buffer)
                buffer = ''
            else:
                buffer += line[i]
            i += 1


if __name__ == '__main__':
    # code = list(map(lambda x: x[:-1], stdin))
    code = ['@']
    while code[-1] != '':
        code.append(input())
    code = code[1:-1]

    html = ''  # В эту переменную записывается получающийся хтмлькод
    lexer(code)
    print(*[i.to_string() for i in tokens], sep='\n')
