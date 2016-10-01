#!/usr/bin/env python3
import os
import argparse
import string


def treeify(path):
    print(path)
    nDir, nFil = treeify_helper(path, 0, [], 0, 0)
    sDir = "directory" if nDir == 1 else "directories"
    sFil = "file" if nDir == 1 else "files"

    print("\n{} {}, {} {}".format(nDir, sDir, nFil, sFil))


def treeify_helper(path, depth, colContinues, nDir, nFil, no_hidden=True):
    # our printy blocks
    vertLine = "│   "
    contBranch = "├── "
    endBranch = "└── "
    blockSpace = "    "

    # determine which lines we need
    leftSpace = ""
    for col in colContinues:
        leftSpace += vertLine if col else blockSpace

    if depth > 0:
        branch = contBranch if True else endBranch

    # get contents
    dirContents = os.listdir(path)
    stdStrs = []

    # remove hidden files
    if no_hidden:
        dirTmp = list(dirContents)
        dirContents = []
        for key, thing in enumerate(dirTmp):
            if not os.path.basename(thing).startswith('.'):
                dirContents.append(thing)

    # http://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
    translation_table = dict.fromkeys(map(ord, string.punctuation), None)
    for i in dirContents:
        stdStrs.append(i.translate(translation_table).lower())

    stdStrs, dirContents = (list(t) for t in zip(*sorted(zip(stdStrs, dirContents))))
    # http://stackoverflow.com/questions/9764298/is-it-possible-to-sort-two-listswhich-reference-each-other-in-the-exact-same-w

    # recurse and print
    for key, thing in enumerate(dirContents):
        branch = contBranch if key < (len(dirContents)-1) else endBranch

        if os.path.isdir(os.path.join(path, thing)):
            cC = list(colContinues)
            if key < (len(dirContents) - 1):
                cC.append(True)
            else:
                cC.append(False)

            print( leftSpace + branch + os.path.basename(thing))
            d, f = treeify_helper(os.path.join(path, thing), depth + 1, cC, 1, 0)
            nDir += d
            nFil += f
        else:
            nFil += 1
            print(leftSpace + branch + thing)

    return nDir, nFil


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='path to directory of interest', nargs='?', default='.')
    args = parser.parse_args()

    treeify(args.directory)
# http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
