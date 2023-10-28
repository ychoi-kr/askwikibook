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
pip install -r requirements
```

# How to Run

1. Start server.

```
python mysite/flask_app.py
```

2. Open <http://127.0.0.1:5000> in a web browser.

