from shazamLyric import *
app = shazamLyric('iron maden - fear of the dark', 1, 0, 'en-US')

title = app.title()
# print(title)
subtitle = app.subtitle()
# print(subtitle)
lyrics = app.lyrics()
# print(lyrics)


f = open('./lyrics/'+title[0]+' - '+subtitle[0]+'.md', 'w')

f.write('## '+title[0]+'\n')
f.write('### ' + subtitle[0]+'\n')
f.write('---\n')
lyric = lyrics[0]
for i in range(len(lyric)):
    f.write(lyric[i])
    if i != len(lyric)-1:
        f.write('\\')
    else:
        print('h')
    f.write('\n')

f.close()
