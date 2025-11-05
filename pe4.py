from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import wikipedia

def timer(func):
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        func(*args, **kwargs)
        t1 = perf_counter()
        return t1-t0
    wrapper.__name__ = func.__name__
    return wrapper

def wiki_dl_and_save(topic):
  page = wikipedia.page(topic, auto_suggest=False)
  title = page.title
  references = page.references
  with open(f"{title}.txt", 'w', encoding='utf-8') as f:
    f.write('\n'.join(references))

@timer
def wiki_dl_series(search_term):
   search_results = wikipedia.search(search_term)
   for result in search_results:
      wiki_dl_and_save(result)

@timer
def wiki_dl_parallel(search_term):
   search_results = wikipedia.search(search_term)
   with ThreadPoolExecutor() as executor:
      executor.map(wiki_dl_and_save, search_results)


if __name__ == '__main__':
   term = 'generative artificial intelligence'
   print(f'[series] Downloading Wikipedia content for "{term}"...')
   t_series = wiki_dl_series(term)
   print(f'[series] Download complete: {t_series}s')
   print(f'[parallel] Downloading Wikipedia content for "{term}"...')
   t_parallel = wiki_dl_parallel(term)
   print(f'[parallel] Download complete: {t_parallel}s')