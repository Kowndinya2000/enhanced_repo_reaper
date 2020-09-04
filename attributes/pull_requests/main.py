import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
import urllib.request

QUERY = '''
SELECT name FROM projects WHERE id={0}
'''

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: PULL REQUESTS -----")
    pr_rate = 0
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd()
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            try:
                cpr = len(inner_os.popen(r'hub pr list -s closed').read().split("\n")) - 1
            except:
                print("[Reg: Closed Pull Requests]Couldn't fetch data from command..")
                cpr = 0
            try:
                opr = len(inner_os.popen(r'hub pr list -s open').read().split("\n")) - 1
            except:
                print("[Reg: Open Pull Requests]Couldn't fetch data from command..")
                opr = 0
            try:
                mpr = len(inner_os.popen(r'hub pr list -s merged').read().split("\n")) - 1
            except:
                print("[Reg: Merged Pull Requests]Couldn't fetch data from command..")
                mpr = 0
            break
    pr = mpr+cpr+opr
    if(pr > 0):
        pr_rate = float(mpr+cpr)/float(pr*1.0)    
    pr = mpr+cpr+opr
    if(pr > 0):
        pr_rate = float(mpr+cpr)/float(pr*1.0)
    threshold = options['threshold']
    pr_rate >= threshold, pr_rate
    print("PR Rate: ",pr_rate)
    return (pr_rate >= threshold, pr_rate)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
