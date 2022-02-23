import argparse
from ast import parse
import os

from shazamLyric import *
from typing import List


FormatterType_MD = 'md'
FormatterType_TXT = 'txt'
FormatterType_CLI = 'cli'


class Song:
    def __init__(self, title: str, artist: str, lyrics: str) -> None:
        self.title = title
        self.artist = artist
        self.lyrics = lyrics
        pass


class Formatter:
    _file = None
    _file_name: str = None

    def __init__(self, file_name: str) -> None:
        self.open(file_name)
        pass

    def __del__(self):
        if self.file is None:
            return
        if self.file.closed == False:
            self.close()

    def write(self, song_title: str, song_artist: str, song_lyrics: List[str]) -> None:
        pass

    def open(self, file_name: str) -> None:
        self.file_name = file_name
        self.file = open(file_name, 'w', encoding='utf-8')
        pass

    def close(self) -> None:
        self.file.close()
        pass

    def get_file_name(self) -> str:
        return self.file_name


class MDFormatter(Formatter):
    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    def write(self, song_title: str, song_artist: str, song_lyrics: List[str]) -> None:
        self.file.write('## ' + song_title)
        self.file.write('\n')
        self.file.write('### ' + song_artist)
        self.file.write('\n')
        self.file.write('---')
        self.file.write('\n')
        for line in song_lyrics[:-1]:
            self.file.write(line)
            self.file.write('\\')
            self.file.write('\n')
        self.file.write(song_lyrics[-1])
        self.file.write('\n')


class CLIFormatter(Formatter):
    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    def __del__(self) -> None:
        super().__del__()
        os.remove(self.get_file_name())
        return

    def write(self, song_title: str, song_artist: str, song_lyrics: List[str]) -> None:
        print(song_title)
        print(song_artist)
        print()
        for line in song_lyrics:
            print(line)


class TXTFormatter(Formatter):
    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    def write(self, song_title: str, song_artist: str, song_lyrics: List[str]) -> None:
        self.file.write(song_title)
        self.file.write('\n')
        self.file.write(song_artist)
        self.file.write('\n')
        self.file.write('\n')
        for line in song_lyrics:
            self.file.write(line)
            self.file.write('\n')


class Shazam:
    def __init__(self) -> None:
        pass

    def get_song_info(self, search_str, lang) -> Song:
        app = shazamLyric(search_str, 1, 0, lang)

        title = app.title()
        artist = app.subtitle()
        lyrics = app.lyrics()

        if 'No lyric' in lyrics[0]:
            raise Exception(
                'No song lyrics were found for {} - {}'.format(artist[0], title[0]))

        return Song(title[0], artist[0], lyrics[0])


class Builder:
    def __init__(self) -> None:
        pass

    def get_formatter(self, info: Song, type: str, dest: str) -> Formatter:
        if not os.path.exists(dest):
            os.makedirs(dest)

        file_name = dest + '/' + info.artist + ' - ' + info.title

        if (type == FormatterType_MD):
            return MDFormatter(file_name+'.md')
        elif (type == FormatterType_TXT):
            return TXTFormatter(file_name+'.txt')
        elif (type == FormatterType_CLI):
            return CLIFormatter(file_name)

        raise Exception('Unknown option for formatter')


def do(song: Song, type: str, output: str):
    builder = Builder()
    formatter = builder.get_formatter(song, type, output)

    formatter.write(song.title, song.artist, song.lyrics)
    pass


def handle(args) -> None:
    try:
        _t = args.type
        _o = args.output
        _l = args.lang

        _i = args.input
        _q = args.query

        _c = args.collection

        shazam = Shazam()
        song = None

        if _i is not None:
            file_input = open(_i, 'r')
            lines = file_input.readlines()

            for line in lines:
                try:
                    song = shazam.get_song_info(line, _l)
                    do(song, _t, _o)
                except Exception as e:
                    print(e)

            file_input.close()
            return

        if _q is not None:
            try:
                song = shazam.get_song_info(_q, _l)
                do(song, _t, _o)
            except Exception as e:
                print(e)
            return

        if _c is not None:
            file_location = os.getcwd() + "\\collection.txt"
            output_file = open(file_location, 'w')

            for (root, dirs, files) in os.walk(_c):
                for file in files:
                    filename = file.split('.')[0]
                    output_file.write(filename)
                    output_file.write('\n')

            output_file.close()
            print('Result is on parh {}'.format(file_location))
            return

    except Exception as e:
        print(e)


def set_up() -> str:

    parser = argparse.ArgumentParser(
        description='CLI tool alowing you to get song lyrics fast and easy')

    parser.add_argument('-t', '--type', dest='type', type=str, default=FormatterType_CLI,
                        choices=[FormatterType_MD,
                                 FormatterType_TXT, FormatterType_CLI],
                        help='Type of output file you want')

    parser.add_argument('-s', '--search', dest='query', type=str, metavar='query',
                        help='Search string')

    parser.add_argument('-l', '--lang', dest='lang', type=str, default='en-US', metavar='language',
                        help='Language of lyrics')

    parser.add_argument('-in', '--input', dest='input', type=str, metavar='file',
                        help='File with list of songs/search strings (each line, one search)')

    parser.add_argument('-o', '--output', dest='output', metavar='file',
                        type=str, help='Output directory', default='lyrics')

    parser.add_argument('-c', '--collect', dest='collection', metavar='root',
                        type=str, help='Root directory for collectiong song names and/or artists')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = set_up()
    handle(args)
