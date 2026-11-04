"""Собирает веб-версию для Claude (артефакт) из index.html Android-приложения: один исходник на обе версии.
Запуск из корня репозитория:  python3 tools/build_web.py life-rpg.html
Что делает: убирает встроенные шрифты (в вебе они грузятся с Google Fonts), снимает обёртку <html>/<head>/<body>
(её добавляет хостинг артефакта) и подключает JSZip с cdnjs для резервной копии в ZIP."""
import re,sys,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=open(os.path.join(root,'app/src/main/assets/www/index.html'),encoding='utf-8').read()
out=sys.argv[1] if len(sys.argv)>1 else 'life-rpg.html'
m=re.search(r'<!doctype html>\s*<html lang="ru">\s*<head>\s*<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*',src)
assert m; s=src[m.end():]
s=s.replace('<title>Уровень жизни</title>','<title>Уровень жизни</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=IBM+Plex+Mono:wght@400;500;600&display=swap">',1)
n=len(re.findall(r"@font-face\{[^}]*\}\n",s)); s=re.sub(r"@font-face\{[^}]*\}\n","",s); assert n==4,n
for a in ['</style>\n</head>\n<body>\n','</body>\n</html>\n']: assert a in s,a
s=s.replace('</style>\n</head>\n<body>\n','</style>\n').replace('</body>\n</html>\n','')
tag='<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>\n'
i=s.index('<script>\n(function(){');s=s[:i]+tag+s[i:]
open(out,'w',encoding='utf-8').write(s);print('web build ok',len(s))
