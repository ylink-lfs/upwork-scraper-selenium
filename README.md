# upwork Scraper

An upwork website scraper powered by selenium and bs4 library written in Python.

## Depedency

### Python related

```bash
python -m pip install -r requirements.txt
```

### Selenium releated

Place chromedriver with suitable version into assets path, then change webdriver path specification under settings subsequently.

## Usage

### Windows x headful

```bash
# assume below commands are executed under Windows powershell
$env:ENV = 'dev'
python -m pip install -r requirements.txt
python main.py --main_category 'Web, Mobile & Software Dev' --sub_category 'All' --output out.json
```

## Platform Supporting Plan

- [x] Windows x headful
- [ ] Windows x headless
- [ ] Linux x headless
