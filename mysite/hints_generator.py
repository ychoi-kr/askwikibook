import re
from string_utils import contains_any

INCLUDE_KEYWORDS_HINTS = {
    ("신간",): 'In Korean, the word "신간" means "new book", so it probably won\'t be included in the title or intro_book.',
    ("비싼", "재미있는", "재밌는", "저렴한", "좋은"): "Words that describe the character of a book may not be keywords.",
    ("자바", "Java", "java"): "When using Java as a keyword, it's a good idea to exclude JavaScript.",
    ("c++",): 'You can also get good results by searching for "C++" as well as "c++".',
    ("Java",): 'You can also get good results by searching for "자바" or "java" as well as "Java".',
    ("파이선",): 'You can also get good results by searching for "파이썬" as well as "파이선".',
    ("프로그래밍",): 'If the user didn\'t specify that they wanted to search for the string "프로그래밍", you might want to try searching for "개발" as well.',
    ("앱개발",): 'You might want to search for the keywords "앱" and "개발" to account for the missing spaces.',
    ("웹개발",): 'You might want to search for the keywords "웹" and "개발" to account for the missing spaces.',
    ("주식거래",): 'You might want to search for the keywords "주식" and "거래" to account for the missing spaces.',
    ("프론트엔드",): 'Respect your users\' needs and search for "프론트엔드" (using the Hangul letter "론"), but also search for the keyword "프런트엔드" (using the Hangul letter "런") to account for Hangul notation.',
}

EXCLUDE_KEYWORDS_HINTS = {
    ("제목", "URL", "가격", "출간일"): "If not specified, consider include title, url, price, and pubdate in SQL query.",
    ("구간", "부터", "순서", "순으로", "옛날", "오래된", "정렬"): "Unless otherwise specified, it sorts in reverse order of pubdate.",
    (" 다 ", "다알려줘", "다찾아", "모두", "모든", "싹다", "싹 다", "전부", "하나도 빼놓지 말고"): "Unless otherwise specified, it limits to 10.",
}

def get_more_hints(natural_query):
    hints = []

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

    return '\n'.join(hints) 
