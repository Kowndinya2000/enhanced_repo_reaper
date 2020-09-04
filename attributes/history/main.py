import sys
import os
import os as inner_os
from dateutil import relativedelta
import urllib.request
from time import strptime
from datetime import datetime
import mysql.connector
import arrow
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: HISTORY -----")
    avg_commits = 0
    num_commits = 0
    commitList = []
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd() 
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
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
                if(numberOfMonths != 0):
                    avg_commits = float(num_commits)/(float(numberOfMonths)*1.0)
                    print('Average Commits: ',avg_commits)
                    threshold = options['threshold']
                    return avg_commits >= threshold, avg_commits
                else:
                    return False, avg_commits
            else:
                return False, avg_commits
            break

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
