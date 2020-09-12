import sys
import requests
from lib.utilities import url_to_json

QUERY = '''
SELECT url FROM projects WHERE id = {0}
'''
def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: STARS -----")
    threshold = options.get('threshold', 0)
    cursor.execute(QUERY.format(project_id))
    full_url = cursor.fetchone()[0]
    git_tokens = options['tokens']
    token_avail = False
    # Making a github api request with the tokens provided 
    for token in git_tokens:
        try: 
            rresult = url_to_json(full_url,authentication=[git_tokens[token],token])["stargazers_count"]
            token_avail = True
            break
        except:
            continue
    # Making api request without token, in the case all OAuth tokens got expired or incorrect tokens provided  
    if(token_avail == False):
        try:
            print('without token - stargazers - fetch ok')
            rresult = url_to_json(full_url)["stargazers_count"]
            print('Fetch Successful')
        except Exception as ex:
            print(ex)
            rresult = None
    bresult = True if rresult is not None and rresult >= threshold else False
    print('stars: ',rresult)
    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
