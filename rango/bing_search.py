import json
import requests
#add your mocrosoft account key to a file called bing.key
def read_bing_key():
    '''read the bing api key from a file called bing.key
    returns a string which is either None or a key
    remember to put bing.key in your .gitignore file to avoid commiting it
    see python anti-patterns -it is an awesome resource to improve your python code
    here we using "with" when opening documents
    http://bit.ly/twd-antipattern-open-files
    '''
    bing_api_key=None
    try:
        with open('bing.key','r') as f:
            bing_api_key=f.readline().strip()
    except:
        try:
            with open('../bing.key') as f:
                bing_api_key=f.readline().strip()
        except:
            raise IOError('bing.key file not found')
    if not bing_api_key:
        raise KeyError('bing key not found')
    return bing_api_key

def run_query(search_terms):
    '''
    see the microsoft's documentation on other parameters that you can set.
    http://bit.ly/twd-bing-apy
    '''
    bing_key=read_bing_key()
    #print('key:',bing_key)
    search_url='https://api.cognitive.microsoft.com/bing/v7.0/search'
    #search_url='https://rango.cognitiveservices.azure.com/bing/v7.0'
    headers={'Ocp-Apim-Subscription-Key':bing_key}
    params={'q':search_terms,'textDecorations':True,'textFormat':'HTML'}
    #issue the request,given the details above
    response=requests.get(search_url,headers=headers,params=params)
    response.raise_for_status()
    search_results=response.json()
    #with the response now in play,build uo a Python list
    results=[]
    for result in search_results['webPages']['value']:
        results.append({'title':result['name'],'link':result['url'],'summary':result['snippet']})
    return results
def main():
    print("Bing search")
    query_str = input("Enter a query to search for: ")
    results = run_query(query_str)
    
    for result in results:
        print(result['title'])

if __name__ == '__main__':
    main()

# def run_query(search_terms):
#     bing_key = read_bing_key()
#     search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
#     headers = {'Ocp-Apim-Subscription-Key': bing_key}
#     params = {'q': search_terms, 'textDecorations': True, 'textFormat': 'HTML'}
    
#     response = requests.get(search_url, headers=headers, params=params)
#     response.raise_for_status()
#     search_results = response.json()
    
#     results = []
#     for result in search_results['webPages']['value']:
#         results.append({
#             'title': result['name'],
#             'link': result['url'],
#             'summary': result['snippet'],
#         })
    
#     return results

# def main():
#     print("Bing search")
#     query_str = input("Enter a query to search for: ")
#     results = run_query(query_str)
    
#     for result in results:
#         print(result['title'])

# if __name__ == '__main__':
#     main()