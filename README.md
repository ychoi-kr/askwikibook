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
