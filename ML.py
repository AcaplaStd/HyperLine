# ULTRA MARKUP LANGUAGE
# better than html

# Этому коду надо:
# - научиться разделять теги в head от тегов в body, а то ему грустно
# - научиться иметь строку внутри команду (в  div class='main-div' 'hi'  не надо определять 'hi' как аргумент для тега)

from sys import stdin
import re


code = list(map(lambda x: x[:-1], stdin))
html = ''  # В эту переменную записывается получающийся хтмлькод
single_tags = ['area', 'base', 'basefont', 'bgsound', 'br', 'col', 'command', 'embed', 'hr', 'img',
               'input', 'isindex', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']  # Незакрывающиеся теги
h_sep = '\t'  # Разделитель иерархии


tags = []
pag = -1
for el in code:
    line = el.lstrip(h_sep).strip()  # сама строка
    lvl = (len(el) - len(line)) // len(h_sep)  # уровень вложенности
    if lvl > pag:
        pag += 1
    else:
        for i in range(pag - lvl + 1):
            if tags[-1] not in single_tags:
                html += '</'+tags.pop()+'>'
        pag += lvl - pag

    html += '<'+line+'>'
    tags.append(line.split()[0])

html += ''.join(list(map(lambda x: '</'+x+'>', reversed(tags))))


print(html)