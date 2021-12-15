Download and format Pubmed metadata

First you need to install [EDirect](https://dataguide.nlm.nih.gov/edirect/install.html)
lib.

#How-To:

01. Search articles on Pubmed using a boolean query. By default, it get
    articles published from 2015 up to now. The output is stored in
    `raw/$query_string` folder. Run: <\br>
```./search.sh "query string"```

02. Format data to TREC standard. Run: <\br>
```python3 format_to_trec.py```

