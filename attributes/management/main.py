import sys
import urllib.request
from time import strptime
from datetime import datetime
import mysql.connector
import arrow
import os
import os as inner_os
import requests
import json
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: ISSUES -----")
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd()
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            try:
                cs = len(inner_os.popen(r'hub issue -s closed').read().split("\n")) - 1
            except:
                print("[Reg: Closed Issues]Couldn't fetch data from command..")
                cs = 0
            try:
                ops = len(inner_os.popen(r'hub issue -s open').read().split("\n")) - 1
            except:
                print("[Reg: Open Issues]Couldn't fetch data from command..")
                ops = 0
            totalNoOfIssues = ops + cs
            stream = inner_os.popen('git log --pretty=format:"%cd"').read().split("\n")
            num_commits = len(stream)
            numberOfMonths = -1
            if(num_commits > 1):
                prev = stream[num_commits-1].split(" ")
                Y1 = int(prev[4])
                M1 = int(strptime(prev[1],'%b').tm_mon)
                D1 = int(prev[2])
                start = datetime(Y1,M1,D1)
                prev = stream[0].split(" ")
                Y1 = int(prev[4])
                M1 = int(strptime(prev[1],'%b').tm_mon)
                D1 = int(prev[2])
                end = datetime(Y1,M1,D1)
                for d in arrow.Arrow.range('month', start, end):
                    numberOfMonths += 1
            issueFrequency = 0
            break
    if numberOfMonths >= 1:
        avg_issues = totalNoOfIssues / numberOfMonths*1.0
        print('Issue Frequency: ',avg_issues)
    if numberOfMonths >= options.get('minimumDurationInMonths', 1):
        avg_issues = totalNoOfIssues / numberOfMonths 
    else:
        return False, avg_issues
    threshold = options['threshold']
    return avg_issues >= threshold, avg_issues
        
if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
