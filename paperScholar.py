#%%
from scholarly import scholarly
#%%
author = scholarly.search_author_id('Smr99uEAAAAJ')
scholarly.fill(author,sections=['publications'])
# %%
titles=[author['publications'][i]['bib']['title'] for i in range(0,len(author['publications']))]

# %%
