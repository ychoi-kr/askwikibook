import re
from datetime import date

from string_utils import contains_any

INCLUDE_KEYWORDS_HINTS = {
    ("ChatGPT", "IoT", "NFT", "PyTorch", "pytorch", "메타버스", "블록체인", "비트코인", "솔리디티", "스마트 컨트랙트", "스프링", "웹3.0", "이더리움", "챗GPT", "챗gpt", "카프카", "파이썬", "파이토치", "포토샵", "포토숍", "프론트엔드"): "A good place to look for a product or service name is in the title, subtitle, toc or book_intro.",
    ("신간",): 'In Korean, the word "신간" means "new book", it\'s better to leave it out of the keywords and search for a date range for the pubdate, such as within three months.',
    ("국내서",): 'You can find 국내서 by using `translator = ""` in WHERE clause.',
    ("비싼", "재미있는", "재밌는", "저렴한", "좋은"): "Words that describe the character of a book may not be keywords.",
    ("c++",): 'You can also get good results by searching for "C++" as well as "c++".',
    ("파이선",): 'Respect the user\'s input and search for "파이선", but also search for "파이썬" to account for the widespread Korean notation. Looking for it in the title, subtitle and intro_book should yield good results.',
    ("파이싼",): 'Respect the user\'s input and search for "파이싼", but also search for "파이썬" to account for the widespread Korean notation. Looking for it in the title, subtitle and intro_book should yield good results.',
    ("퓌톤",): 'Respect the user\'s input and search for "퓌톤", but also search for "파이썬" to account for the widespread Korean notation. Looking for it in the title, subtitle and intro_book should yield good results.',
    ("프로그래밍",): 'If the user didn\'t specify that they wanted to search for the string "프로그래밍", you might want to try searching for "개발" as well.',
    ("앱개발",): 'You might want to search for the keywords "앱" and "개발" to account for the missing spaces.',
    ("웹개발",): 'You might want to search for the keywords "웹" and "개발" to account for the missing spaces.',
    ("주식거래",): 'You might want to search for the keywords "주식" and "거래" to account for the missing spaces.',
    ("프론트엔드",): 'Respect your users\' needs and search for "프론트엔드" (using the Hangul letter "론"), but also search for the keyword "프런트엔드" (using the Hangul letter "런") to account for Hangul notation.',
    ("관련 책", "시리즈"): 'When searching for a series, we recommend using a LIKE search.',
    ("시리즈"): 'The word "시리즈" is unlikely to be in title or series, so it\'s a good idea to leave it out as a keyword.',
    ("Unity", "unity"): 'You can also get good results by searching for "유니티" as well as "Unity".',
    ("알고리듬",): 'Respect the user\'s input and search for "알고리듬", but also search for "알고리즘" to account for the widespread Korean notation. Looking for it in the title, subtitle and intro_book should yield good results.',
    ("인공지능", "AI"): 'When searching for artificial intelligence, use "머신러닝", "딥러닝" and "강화학습" as keywords.',
    ("기계학습",): 'You can also get good results by searching for "머신러닝" as well as "기계학습".',
    ("심층학습",): 'You can also get good results by searching for "딥러닝" as well as "심층학습".',
    ("컴퓨터비전",): 'You can also get good results by searching for "컴퓨터 비전" as well as "컴퓨터비전".',
    ("ChatGPT", "chatgpt",): 'You can also get good results by searching for "챗GPT" as well as "ChatGPT".',
    ("챗지피티",): 'You can also get good results by searching for "챗GPT" as well as "챗지피티".',
    ("트랜스메이트",): 'To find "트랜스메이트", search for translator.',
    ("봄", "여름", "가을", "겨울", "올해", "작년", "내년", "후년", "오늘", "어제", "엊그제", "내일", "이번", "지난",): 'For queries about timing, search by date range. Today is ' + str(date.today()),
    ("nft",): 'You might want to search for "NFT" in all caps in the title, subtitle, toc, and intro_books.',
    ("JavaScript", "자바스크립트",): 'If the user didn\'t specify to search in the title, you can also search for "자바스크립트" in subtitle and intro_book.',
}

EXCLUDE_KEYWORDS_HINTS = {
    ("구간", "년 초", "년초", "부터", "순서", "순으로", "연초", "옛날", "오래된", "정렬", "처음"): "Unless otherwise specified, it sorts in reverse order of pubdate.",
    (" 다 ", "다알려줘", "다찾아", "모두", "모든", "싹다", "싹 다", "전부", "처음", "하나도 빼놓지 말고"): "Unless otherwise specified, it limits to 10.",
}

def get_hints(natural_query):
    hints = []

    hints.append("If the query is about an individual book and the user hasn't specified which fields to show, consider include title, subtitle, url, author, translator, price, pubdate and intro_book in SQL query.")

    for keywords, message in INCLUDE_KEYWORDS_HINTS.items():
        if contains_any(natural_query, keywords):
            hints.append(message)
    
    for keywords, message in EXCLUDE_KEYWORDS_HINTS.items():
        if not contains_any(natural_query, keywords):
            hints.append(message)

    if 1 < len(natural_query.split()) < 4 and contains_any(natural_query, ["도서", "서적", "책"]):
        hints.append("If search keyword has two or more words, consider to split it into multiple keywords.")

    if contains_any(natural_query, ["교수", "근무", "대학교", "박사", "석사", "재직", "졸업", "출신"]) or re.search(r"대\b", natural_query):
        hints.append("Organization name can also be found in intro_author.")

    if contains_any(natural_query, ["자바", "java"]) and not contains_any(natural_query, ["스크립트", "Script", "script"]):
        hints.append('When using "자바" as a keyword, it\'s a good idea to exclude "자바스크립트".')

    if contains_any(natural_query, ["Java"]) and not contains_any(natural_query, ["스크립트", "Script", "script"]):
        hints.append('When using "Java" as a keyword, it\'s a good idea to exclude "자바스크립트". You can also get good results by searching for "자바" or "java" as well as "Java".')

    return '\n'.join(hints) 
