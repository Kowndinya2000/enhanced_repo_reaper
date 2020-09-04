import sys
import requests
from lib import utilities


def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: STARS -----")
    threshold = options.get('threshold', 0)
    cursor.execute('SELECT url FROM projects WHERE id = {}'.format(project_id))
    record = cursor.fetchone()
    full_url = record[0]
    git_tokens = options['tokens']
    token_avail = False
    for user_name in git_tokens:
        if(token_avail == True):
            break
        else:
            try: 
                page = requests.get(full_url,auth=(user_name,git_tokens[user_name])).json()["stargazers_count"]
                token_avail = True
            except:
                continue
    if(token_avail == False):
        try:
            print("[Reg: Stargazers Count]Tokens didn't work! Trying out without token...")
            page = requests.get(full_url).json()["stargazers_count"]
            print('Fetch Successful')
        except:
            print("[Reg: Stargazers Count]Couldn't fetch data..")
            page = None
    rresult = page
    bresult = True if rresult is not None and rresult >= threshold else False
    print('stars: ',rresult)
    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
