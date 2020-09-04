import sys
from datetime import datetime
import urllib.request
from time import strptime
import attributes
import requests
from lib import utilities
import os
import os as inner_os
import mysql.connector
from lib import dateutil
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def getLastCommitDate(project_id,cursor):   
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd() 
    page = ""
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            stream = inner_os.popen('git log --pretty=format:%cd').read().split("\n")
            dat = stream[0].split(" ")
            page += dat[4] + "-" + str(strptime(dat[1],'%b').tm_mon) + "-" + dat[2]     
            break
    return page

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: STATE -----")
    bresult = False
    rresult = 'dormant'
    last_commit_date = getLastCommitDate(project_id,cursor)
    if last_commit_date is not None:
        today = options.get('today', datetime.today().date())
        if isinstance(today, str):
            today = datetime.strptime(today, '%Y-%m-%d')
        last_commit_date_formatted = tuple(map(int,last_commit_date.split("-")))
        delta = dateutil.relativedelta(today, datetime(*last_commit_date_formatted))
        threshold = utilities.parse_datetime_delta(options['threshold'])
        bresult = delta <= threshold
        if bresult:
            rresult = 'active'
    print('State: ',rresult)
    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
