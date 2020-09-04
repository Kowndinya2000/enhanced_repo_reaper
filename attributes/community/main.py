import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
from subprocess import Popen, PIPE

QUERY = '''
SELECT name FROM projects WHERE id={0}
'''

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: COMMUNITY -----")
    num_core_contributors = 0
    num_commits = 0
    commitList = []
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd()
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            stream = inner_os.popen(r'git log --pretty="%ae" | sort').read().split()
            unique_names = set(stream)
            for names in unique_names:
                stream.count(names)
                commitList.append(int(stream.count(names)))
                num_commits += int(stream.count(names))
            break
    commitList.sort(reverse=True)
    cutoff = 0.8
    aggregate = 0
    for v in commitList:
        num_core_contributors += 1
        aggregate += v
        if (aggregate / num_commits) >= cutoff:
            break
    print('# of Core Contributors: ',num_core_contributors)
    threshold = options['threshold']
    num_core_contributors >= threshold, num_core_contributors
    return (num_core_contributors >= threshold, num_core_contributors)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
