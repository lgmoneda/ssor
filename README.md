# Semantic Search for Org Roam

Original post: http://lgmoneda.github.io/2023/04/08/semantic-search-for-org-roam.html

Steps:

1. Go to `config.py` file and provide the correct paths for your use case and the OpenAI API Key.

2. Run `python setup.py install`

3. Run `python ssor/org_roam_vectordb.py` to build the knowledge base

4. Run `python ssor/server.py` to serve the application under the 8800 port
