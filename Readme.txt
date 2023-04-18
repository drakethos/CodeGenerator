----------READ ME -----------
CodeGen.py
Created by Derrick Kamphaus

This script automates making repetitive code. It takes a source file / clipboard list, which is a line by line list
that has the data which you need to wrap code around. Supply a template file to format around the code.

Parameters / arguments:
    source: Required baseline argument. This is the name of the file that will be used as the template
--file -f : Specifies an input file to use as source for list. will output the same name but out
    IE: CodeGen.py "myTemplate.txt" --f "Mylist.txt"
    will pull "Mylist.txt" and use each line to wrap the template text from "myTemplate.txt" and output as Mylist.txt.out
    not supplying file with this flag will default to clipboard as source and destination.

--multi -m : Allows a supplied list to have multiple items per line delineated by | each line will be parsed by the
    template as $data1, $data2, ... $dataN , when not supplied template will be interpreted as $data

--out -o : sets a specific name for output file, otherwise will use the name of the inputfile + .out

--number -n : (any number of args)  Increments numbers in template $n1, $n2 ... $nX where n is the number at which it
starts. --n "1 2 3" would increment 1 2 3 -> 2 3 4 -> 3 4 5 for each line in the source.

--line -l : Adds a new line after each chunk iteration of the code wrap.

--onlynum : increments numbers only and does not use a list source. Supply number of loops, and generates that many number
of template based items with the supplied -n number list


to use clipboard as the source of list and output of template: just supply the source and don't use --f
CodeGen.py "template.txt"
or other arguments: CodeGen.py "template.txt" -l -n "1 3 4"


Example uses: XML-, when you need to create multiple items in a large XML1 where the only variance is the sku, name, and document number
Test Automation- when you have several files to make into includes: have a list of file1, file2 ,file3 ... simply write the list in the .test where you want it.
supply source file with: <include path="$data"/>
copy run CodeGen and paste a list of <include path="file1"/> .. <include path="fileX"/>


Creating Template: create a file that has the text that will wrap around each data item supplied from the source list.
variables: $data - whatever data from list source either file or clipboard will supply each line and replace with data
$data1, $data2 .. $dataN see --multi flag

$n1, $n2, $n3 ... - when --numbers is set, allows incrementing numbers to be replaced. Good for xml1s where multiple
numbers may increment. each number can start from a different number.

$break$
requires at the start and end of the section at minimum a file should have 2 breaks. A break will treat a section as a new file and restart the list, and
numbering. This allows repetitive but slightly different changes

<$header> ... </$header>
text between this will be parsed once and only once this allows for parts that will not be looped

<$footer> ... </$footer>
text between this is parsed only once to be at end of file. Does not get looped.

EX Template:
my.tmpl

<text>
    <foo="$data"/>
    <num="$n1">
    <otherNum="$n2">
</text>

supplying the list of :
thing1
thing2
thing3

--numbers 1 4

output would be:

<text>
    <foo="thing1"/>
    <num="1">
    <otherNum="4">
</text>
<text>
    <foo="thing2"/>
    <num="2">
    <otherNum="5">
</text>
<text>
    <foo="thing3"/>
    <num="3">
    <otherNum="6">
</text>