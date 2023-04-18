import string
import pyperclip
import io
import argparse

def parser_hook(text):
    parsed_text = []
    for line in text:
        if '$include="' in line:
            parsed_text.append(include(line))

        if not ("#" in line):
                parsed_text.append(line)

    return ''.join(parsed_text)


def include(line):
    parts = line.split('"')
    file = parts[1]
    print(file)
    file_text = open_file_template(file)
    newLine = line.replace(file_text)
    return newLine


def outfile(file, text):
    f = open(file, 'w')
    f.write(text)
    f.close()


def open_file_list(fname):
    with open(fname, 'r') as f:
        lines = []
        for line in f:
            line = line.strip()
            lines.append(line)
    f.close()
    return lines


def clip_to_list():
    lines = []
    for line in io.StringIO(pyperclip.paste()):
        line = line.strip()
        lines.append(line)
    return lines


def open_file_template(fname):
    f = open(fname, 'r')
    text = f.read()
    f.close()
    return text


def gen_num(numlist, data, inc):
    newdata = data
    for i in range(len(numlist)):
        x = numlist[i]
        xstr = str(x)
        x += inc
        numlist[i] = x
        rep = '$n' + str(i + 1)

        newdata = newdata.replace(rep, xstr)
    return newdata


def gen_number(numlist, data, loop, inc):
    newlist = ""
    for i in range(loop):
        getline = gen_num(numlist, data, inc)
        newlist += getline + "\n"

    return newlist


def multi_data(data, list):
    lines = list.split("|")
    i = 1
    curData = data
    for ln in lines:
        rep = '$data' + str(i)
        repData = curData.replace(rep, ln)
        curData = repData
        i += 1
    return curData


def single_data(data, line):
    newdata = data.replace('$data.end', get_end_data(line))
    newdata = newdata.replace('$data', line)
    return newdata


def get_data_path(line):
    splitLines = line.split("/")
    filename = splitLines[len(splitLines) - 1]

    i = 1
    path = ""
    for l in splitLines:
        if i > 3:
            path += l
            if i != len(splitLines):
                path += '/'
        i += 1
    return path


def get_end_data(line):
    path = get_data_path(line)
    splitPath = path.split('/')
    fileName = splitPath[len(splitPath) - 1]
    name = fileName.split(".")[0]
    return name


def gen_File_Arg(args):
    listfile = args.file
    exclude_file = args.exclude
    datasource = args.source
    multi = args.multi
    numbers = args.number
    pData = args.data
    add_line = args.line
    new_line = "\n"
    out = args.out
    onlynum = args.onlynum
    inc = args.inc
    seperate = args.seperate

    if not inc:
        inc = 1
        print("inc default:")

    data = open_file_template(datasource)
    data = parser_hook(data)
    newdata = data
    newlines = ""
    numlist = numbers
    if (add_line):
        new_line += "\n"



    if not onlynum:
        if listfile:
            getlines = open_file_list(listfile)
            print("Open File")

        else:
            getlines = clip_to_list()
            print("Open from Clipboard")

        for line in getlines:
            # verify it isnt blank or contains a comment
            if (line and line.strip()) and not("#" in line):

                if exclude_file:
                    exclude_lines = open_file_list(exclude_file)
                    adjustedLine = line.split('/')
                    if adjustedLine[len(adjustedLine)-1] in exclude_lines:
                        continue

                if multi:
                    newdata = multi_data(data, line)

                else:
                    newdata = single_data(data, line)


                if pData:
                    i = 1
                    for p in pData:
                        rep = '$p' + str(i)
                        repData = newdata.replace(rep, p)
                        newdata = repData

                if numbers:
                    newdata = gen_num(numlist, newdata, inc)

                if seperate:
                    path = get_data_path(line)
                    filepath = out + path
                    outfile(filepath, newdata)
                newlines += newdata + new_line

    else:
        # for x in range(int(onlynum)):
        newdata = gen_number(numbers, data, onlynum, inc)
        newlines += newdata
    if listfile:
        fileout = listfile + ".out"
        if out:
            fileout = out
        if not seperate:
            outfile(fileout, newlines)
    else:
        pyperclip.copy(newlines)


if __name__ == '__main__':
    # total arguments
    parser = argparse.ArgumentParser("Code Generator")
    parser.add_argument("source", help="File containing data to surround your text list")
    parser.add_argument("-f", "--file", help="gets input from a file then outputs to a file")
    parser.add_argument("-e", "--exclude", help="gets a list from file to exclude items from the first list/clipboard")
    parser.add_argument("-m", "--multi", help="Splits input list into multiple delimitated items", action="store_true")
    parser.add_argument("-s", "--seperate", help="output into seperate files  expects $data1 to be path",
                        action="store_true")
    parser.add_argument("-o", "--out", help="sets the name of the output file")
    parser.add_argument("-n", "--number", nargs="*", type=int, help="Increments number, with $n1, $n2 starting num",
                        default=0)
    parser.add_argument("-d", "--data", nargs="*", type=str, help="Additional data: $p1, $p2 ...")
    parser.add_argument("-i", "--inc", type=int, help="Custom increment for numbers default is 1:", default=1)
    parser.add_argument("--onlynum", type=int, help="uses no source, instead only increments numbers")
    parser.add_argument("-l", "--line", help="Adds a new line after every item.", action="store_true")
    args = parser.parse_args()

    if args.file:
        print("Using your file: {} , source is {}, numbers are {}".format(args.file, args.source, args.number))
    if args.line:
        print("Adding new line after each item.")
    if args.multi:
        print("Splitting input into deliminated items.")

    elif not args.file:
        print("Using clipboard")

    gen_File_Arg(args)