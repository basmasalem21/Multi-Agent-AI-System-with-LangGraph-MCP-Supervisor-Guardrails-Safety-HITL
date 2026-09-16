from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client=TavilyClient(

    api_key=os.getenv("TAVILY_API_KEY")
)

def tavily_search(query):

    response=client.search(

        query=query,
        max_results=5
    )

    results=[]

    for index,result in enumerate(response['results']):
        url=result['url']
        title=result['title']
        #Get first 2 statements
        if len(result['content'].split("."))>=2:
            content="".join(result['content'].split(".")[:2])

        results.append(f'{index+1}: \n ***{title}*** \n {url} \n {content}')
     
    return results

#print(tavily_search("best hotels in cairo"))

