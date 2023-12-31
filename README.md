This Flask app allows users to query Wikibooks(https://wikibook.co.kr/)' book information in natural language, which is then converted to SQL to query and display the results. 

![screenshot](screenshot.png)

# How to Setup

1. Clone repository.

```
git clone https://github.com/ychoi-kr/askwikibook.git
```

2. Make folders.

```
cd askwikibook
mkdir databases settings
```

3. Download database

```
./scripts/download_db.sh
```

4. Set OpenAI API Key

```
cat > ./settings/OPENAI_API_KEY
<your key>
^D
```

5. Install dependencies.

```
pip install -r requirements.txt
```

# How to Run

1. Start server.

```
python mysite/flask_app.py
```

2. Open <http://127.0.0.1:5000> in a web browser.

