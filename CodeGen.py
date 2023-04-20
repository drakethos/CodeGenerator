import copy
import string
import pyperclip
import io
import argparse
import configparser

listfile = "list.txt"
exclude_file = ""
datasource = ""
numbers = "1"
pData = ""
add_line = ""
new_line = ""
out = ""
onlynum = ""
inc = ""
seperate = ""
header = []
footer = []


def initializeGlobals(args):
    global listfile
    global exclude_file
    global datasource
    global numbers
    global pData
    global add_line
    global new_line
    global out
    global onlynum
    global inc
    global seperate
    global header
    global footer
    global ext
    global delim

    # get configs, we will set values from either args or config
    cfg = read_ini("config.ini", args.cfg)

    listfile = args.file
    exclude_file = args.exclude
    datasource = args.source
    #nm = []
    #nm.append(cfg.getint("start_num"))
    nm = stringToIntList(cfg.get("start_num"))
    numbers = getCfg(args.number, nm)
    print(numbers)
    pData = args.data
    add_line = getCfg(args.line, cfg.getboolean("addline"))
    new_line = "\n" if add_line else ""
    ext = cfg.get("DefaultExt")
    out = getCfg(args.out, cfg.get("defaultname") + ext)
    onlynum = args.onlynum
    inc = getCfg(args.inc, cfg.getint("numinc"))
    seperate = args.seperate
    delim = cfg.get("data_delim")
    # Get defaults from config, if values are not set we will use these:
    inc = getCfg(inc, int(cfg.get("numinc")))


def stringToIntList(text):
    return text.split(',')


def read_ini(file, section):
    config = configparser.ConfigParser()
    config.read(file)
    # for section in config.sections():
    # print(section)
    #   for key in config[section]:
    # print((key, config[section][key]))
    #return config.defaults()
    return config[section]


def getCfg(value, config):
    if value:
        return value
    return config


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
        x = int(numlist[i])
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
        newlist += getline + "new_line"

    return newlist


def multi_data(data, list):
    lines = list.split(delim)
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


def getHeader(text):
    global header
    # open and close for the header
    hdrO = '<$header>'
    hdrC = '</$header>'
    # The indexes of the start and end of header tags
    startF = text.find(hdrO)
    endF = text.find(hdrC)
    startL = startF + len(hdrO)
    endL = endF + len(hdrC)
    nl = 0
    # The entire text including opening and closing tags
    if '\n' in text[endL:endL + 1]:
        nl = 1

    hdr = text[startF:endL + nl]
    # Set the header to the actual text between tags

    nl = 0

    if '\n' in text[startL:endF]:
        nl = 1

    header = text[startL + nl:endF]

    # Remove header text
    return text.replace(hdr, '')


def getFooter(text):
    global footer
    # open and close for the Footer
    ftrO = '<$footer>'
    ftrC = '</$footer>'
    # indexes of start and end of footer tags
    startF = text.find(ftrO)
    endF = text.find(ftrC)
    startL = startF + len(ftrO)
    endL = endF + len(ftrC)

    nl = 0
    # The entire text including opening and closing tags
    if '\n' in text[endL:endL + 1]:
        nl = 1

    ftr = text[startF:endL + nl]
    # Set the footer to the actual text between tags

    nl = 0

    if '\n' in text[startL:endF]:
        nl = 1
    footer = text[startL + nl:endF]

    # Remove footer text
    return text.replace(ftr, '')


def createCode(getlines, data):
    # make a single deep copy of numbers to prevent reference
    tempNumList = copy.copy(numbers)
    multi = ""
    newlines = ""

    if delim in getlines[0]:
        multi = "true"

    for line in getlines:
        # verify it isn't blank or contains a comment
        if (line and line.strip()) and not ("#" in line):

            if exclude_file:
                exclude_lines = open_file_list(exclude_file)
                adjustedLine = line.split('/')
                if adjustedLine[len(adjustedLine) - 1] in exclude_lines:
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

            if tempNumList:
                newdata = gen_num(tempNumList, newdata, inc)

            if seperate:
                path = get_data_path(line)
                filepath = out + path
                outfile(filepath, newdata)
            newlines += newdata + new_line
    return newlines


def generateCode(data):
    newlines = ""

    if not onlynum:
        if listfile:
            getlines = open_file_list(listfile)

        else:
            getlines = clip_to_list()

        newlines = createCode(getlines, data)

    else:
        # for x in range(int(onlynum)):
        newdata = gen_number(numbers, data, onlynum, inc)
        newlines += newdata

    return newlines


def parseBreak(data):
    lines = ""
    # We will keep updating data until there are no more breaks
    dataToParse = data
    breakSection = ""
    brk = "$break$"

    while brk in dataToParse:

        # find the start and stop of break
        brkF = dataToParse.find(brk)
        brkL = brkF + len(brk)
        # define the current break section, all text up to start of break
        breakSection = dataToParse[0:brkF]

        # update our list to include the breaksection (without tags)
        lines += generateCode(breakSection)

        # data will be updated to hold what needs to be still parsed
        nl = 0

        if '\n' in dataToParse[brkL:brkL + 1]:
            nl = 1
        dataToParse = dataToParse[brkL + nl:len(dataToParse)]

    return lines


def gen_File_Arg(args):
    initializeGlobals(args)

    data = open_file_template(datasource)
    data = parser_hook(data)
    data = getHeader(data)
    data = getFooter(data)
    if "$break$" in data:
        # loop for each time and keep generating
        newlines = parseBreak(data)

    else:
        newlines = generateCode(data)

    fulltext = header + str(newlines) + footer

    newlines = fulltext

    if listfile:
        fileout = listfile + ext
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
    parser.add_argument("-s", "--seperate", help="output into seperate files  expects $data1 to be path",
                        action="store_true")
    parser.add_argument("-o", "--out", help="sets the name of the output file")
    parser.add_argument("-n", "--number", nargs="*", type=int, help="Increments number, with $n1, $n2 starting num")
    parser.add_argument("-d", "--data", nargs="*", type=str, help="Additional data: $p1, $p2 ...")
    parser.add_argument("-i", "--inc", type=int, help="Custom increment for numbers default is 1:")
    parser.add_argument("--onlynum", type=int, help="uses no source, instead only increments numbers")
    parser.add_argument("-l", "--line", help="Adds a new line after every item.", action="store_true")
    parser.add_argument("-c", "--cfg", help="Specifies a section to use in cfg for defaults, default is main. others "
                                            "av xml", default="main")
    args = parser.parse_args()

    if args.file:
        print("Using your file: {} , source is {}, numbers are {}".format(args.file, args.source, args.number))
    if args.line:
        print("Adding new line after each item.")

    elif not args.file:
        print("Using clipboard")

    gen_File_Arg(args)
