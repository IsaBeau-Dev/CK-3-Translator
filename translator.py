# To make it run do:
# right click on folder of this file-> open in terminal
# type python main.py "path"
# example python main.py D:\Downloads\CK3_LocalizationChanger-main\db\
# https://github.com/CyberNord/CK3_LocalizationChanger
# Usage
# Below you can see the general Syntax
#
# python main.py [-h] [-l1 L1] [-l2 L2] [-trans TRANS] path
# The following parts are mandatory
#
# python main.py    call of the programm
# path                       path to the folder to be translated
# Optional information
#
# [-h]                      no function for now
# [-l1 L1]                given input language (default = en)
# [-l2 L2]                desired output language (default = de)
# [-trans TRANS]  (default = 1) If this value is set to 0 there will be no translation. The Programm wil only convert the files to the disired output language so that it is supported by the game (e.g. results in english text in german localisation)
# Supported languages
# The list is limited by the possible localisations supported in CK3.
#
# 'en' english
# 'de' german
# 'fr' french
# 'es' spanish
# 'zh-cn' simplified chinese
# 'ko' korean
# More examples
# this will translate from english (default) to french
#
# python main.py -l2 fr D:\the\path\to\english\loc\folder
# this will translate from french to german (default)
#
# python main.py -l1 fr D:\the\path\to\english\loc\folder
# this will just alter the first line and filename so that the localisation is detected by the game
#
# python main.py -trans 0 D:\the\path\to\english\loc\folder


import time
import argparse
from pathlib import Path
import os
import re
from googletrans import Translator
import argostranslate.package
import argostranslate.translate as at
# import PyYAML

# ---------------------------------------------------
DEBUG = False
INFO = False
translator = Translator()
RE_PATTERN = re.compile(r'\[[^"\]]*]|\$[^$]+\$|#[^$]+#|\\n')
REPLACER = '{@}'
# ---------------------------------------------------


def get_loc_code(from_l: bool, pars_arg: str):
    locale_codes = {
        'en': 'english',
        'de': 'german',
        'fr': 'french',
        'es': 'spanish',
        'ru': 'russian',
        'zh-cn': 'simp_chinese',
        'ko': 'korean'
    }
    locale = locale_codes.get(pars_arg)
    if not locale:
        locale = 'english' if from_l else 'german'
    return locale


# def parseargs():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-l1", type=str, default="en")
#     parser.add_argument("-l2", type=str, default="de")
#     parser.add_argument("-trans", type=int, default=1)
#     parser.add_argument("path")
#
#     args = parser.parse_args()
#     from_language = args.l1
#     to_language = args.l2
#     from_naming = get_loc_code(True, from_language)
#     to_naming = get_loc_code(False, to_language)
#
#     if args.trans == 1:
#         do_translation = True
#     else:
#         do_translation = False
#     # target_dir = "D:\Downloads\CK3_LocalizationChanger-main\db\Testing\Testcases_english.yml"
#     target_dir = Path(args.path)
#
#     if not target_dir.exists():
#         print("The target directory doesn't exist")
#         raise SystemExit(1)
#     init(target_dir, do_translation, from_language, to_language, from_naming, to_naming)

def call(l1:str,l2:str,trans:int,path):
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-l1", type=str, default="en")
    # parser.add_argument("-l2", type=str, default="de")
    # parser.add_argument("-trans", type=int, default=1)
    # parser.add_argument("path")

    # args = parser.parse_args()
    from_language = l1
    to_language = l2
    from_naming = get_loc_code(True, from_language)
    to_naming = get_loc_code(False, to_language)

    if trans == 1:
        do_translation = True
    else:
        do_translation = False
    # target_dir = "D:\Downloads\CK3_LocalizationChanger-main\db\Testing\Testcases_english.yml"
    target_dir = Path(path)

    if not target_dir.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)
    init(target_dir, do_translation, from_language, to_language, from_naming, to_naming)


def init(target_dir, do_translation, from_language, to_language, from_naming, to_naming):
    INPUT_DIR = target_dir
    print("INPUT_DIR " + INPUT_DIR.__str__())

    totalCount = 0

    file: Path
    for file in list(INPUT_DIR.rglob("*.yml*")):
        filepath = os.path.dirname(os.path.abspath(file))
        filename = file.name.split('/')[0]
        newfileName = filename.replace(from_naming, to_naming)

        # replace text in file
        with open(file, 'r', encoding="utf-8") as f_r:
            print('----------------------------------------------')
            print("current File: " + file.name)
            file_data = f_r.readlines()
            file_data[0] = file_data[0].replace(from_naming, to_naming)
            if do_translation:
                translate(file_data, totalCount, from_language, to_language)
            tofile(filepath, filename, file_data, from_naming, to_naming)


def tofile(filepath, filename, file_data, from_naming, to_naming):
    old_file = os.path.join(filepath, filename)
    newfileName = filename.replace(from_naming, to_naming, 1)
    new_filepath = filepath.replace(from_naming, to_naming, 1)
    new_file = os.path.join(new_filepath, newfileName)

    new_path = Path(new_file)
    if not os.path.exists(new_filepath):
        os.makedirs(new_filepath)

    with open(new_path, 'w', encoding="utf-8") as f_r:
        f_r.writelines(file_data)


def translate(file_data, totalCount, from_language, to_language):
    #  basic Translator in work
    for i, lines in enumerate(file_data[1:]):
        matches = re.findall('"([^"]*)"', lines)
        # matches = re.findall(r'"(.*?)"', lines)
        if len(matches) == 1 and matches is not None:
            tokens = re.findall(RE_PATTERN, matches[0])

            match = matches[0]
            matches[0] = re.sub(RE_PATTERN, REPLACER, matches[0])

            #remove timeout
            # # timeout is needed otherwise api will block usage
            # if DEBUG:
            #     print("Timeout API.")
            #     for j in range(2, 0, -1):
            #         print(j, end="...")
            #         time.sleep(0.1)
            #         # time.sleep(2)
            #     print("resuming")
            # else:
            #     # time.sleep(2)
            #     time.sleep(0.1)
            # translate
            try:
                # translation = translator.translate(matches[0], dest=to_language, src=from_language)
                translation = at.translate(matches[0], to_code=to_language, from_code=from_language)
                padded_translation = translation
            except TypeError:
                translation = matches[0]
                padded_translation = matches[0]
                print('Error (TypeError) Skipped in: ' + matches[0])
            except TimeoutError:
                translation = matches[0]
                padded_translation = matches[0]
                print('Error (TimeOut) Skipped in: ' + matches[0])
            except:
                translation = matches[0]
                padded_translation = matches[0]
                print('Unknown Exception - Skipped in' + matches[0])
            totalCount += 1

            if DEBUG:
                print(padded_translation)

            for t in tokens:
                padded_translation = padded_translation.replace(REPLACER, t, 1)

            if DEBUG:
                print(padded_translation)

            file_data[i + 1] = lines.replace("\"" + match + "\"", "\"" + padded_translation + "\"", 1)
            if INFO:
                print(match + " <- " + padded_translation)
            print("line no. #" + str(totalCount), end="")
        print()