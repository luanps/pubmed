# Download and format Pubmed metadata

You need to install [EDirect](https://dataguide.nlm.nih.gov/edirect/install.html)
lib to download and extract Pubmed metadata.

### How-To:

01. Search articles on Pubmed using a boolean query. It get articles published from 2015 up to now. The output is stored in
    `raw/$query_string` folder. Run: <br>
```./search.sh "query string"```

02. Format data to TREC standard. Run: <br>
```python3 format_to_trec.py```

