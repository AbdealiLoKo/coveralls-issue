# coveralls-issue
Repo to reproduce issues in coveralls

```bash
$ python -m venv venv
$ venv/bin/pip install -r requirements.txt -e .
$ venv/bin/pytest --cov --cov-report=html
```