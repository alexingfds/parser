from github import Github
ACCESS_TOKEN = 'da92ec3fca51bc602d252f67ed15a94ca5d519ed '
g = Github(ACCESS_TOKEN)
# g.get_user('dguenms').get_repo('Dawn-of-Civilization')
# print(g.get_user().get_repos())


repos= g.get_user('dguenms').get_repos()


for repo in repos:
 for name in repo.filename:
    print(files.name)
# def search_github(keyword):
#     rate_limit = g.get_rate_limit()
#     rate = rate_limit.search
#     if rate.remaining == 0:
#         print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
#         return
#     else:
#         print(f'You have {rate.remaining}/{rate.limit} API calls remaining')

#     query = f'"{keyword} english" in:repo  extension:xml'
#     result = g.search_code(query, order='desc')
 
#     max_size = 100
#     print(f'Found {result.totalCount} file(s)')
#     if result.totalCount > max_size:
#         result = result[:max_size]
 
#     for file in result:
#         print(f'{file.download_url}')


query =''

