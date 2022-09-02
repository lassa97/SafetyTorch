import json
import subprocess

class Worker:
    @staticmethod
    def get_lists(sources='../lists.txt'):
        subprocess.call("mkdir -p lists/filtered", shell=True)
        subprocess.call("cd lists && wget -i {SOURCES} -N".format(SOURCES=sources), shell=True)

    @staticmethod
    def filter_lists(categories=None):
        subprocess.call("cd lists && rename -f 'y/A-Z/a-z/' *", shell=True)
        for category in categories:
            subprocess.call("cd lists && find . -maxdepth 1 -name '*{CATEGORY}*' -exec grep -v '^#' {{}} > filtered/{CATEGORY}.txt \;".format(CATEGORY=category), shell=True)

    @staticmethod
    def categorise_lists(categories=None):
        output = {}
        for category in categories:
            with open('lists/filtered/{CATEGORY}.txt'.format(CATEGORY=category), 'r') as infile:
                for line in infile:
                    if len(line) == 1:
                        continue
                    output[line[:-1]] = category

        with open('blocklist.json', 'w') as outfile:
            outfile.write(json.dumps(output, separators=(',', ':')))