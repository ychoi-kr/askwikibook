import re
from string_utils import contains_any

def get_more_hints(natural_query):
    hint = []
    if 1 < len(natural_query.split()) < 4 and contains_any(natural_query, ["도서", "서적", "책"]):
        hint.append("If search keyword has two or more words, consider to split it into multiple keywords.")

    if contains_any(natural_query, ["비싼", "재미있는", "재밌는", "저렴한", "좋은"]):
        hint.append("Words that describe the character of a book may not be keywords.")

    if re.search(r"\b신간\b", natural_query):
        hint.append('In Korean, the word "신간" means "new book", so it probably won\'t be included in the title or intro_book.')

    else:
        if not contains_any(natural_query, ["구간", "부터", "순서", "순으로", "옛날", "오래된", "정렬"]):
            hint.append("Unless otherwise specified, it sorts in reverse order of pubdate.")
    
        if not contains_any(natural_query, [" 다 ", "다알려줘", "다찾아", "모두", "모든", "싹다", "싹 다", "전부", "하나도 빼놓지 말고"]):
            hint.append("Unless otherwise specified, it limits to 10.")

    if contains_any(natural_query, ["자바", "Java", "java"]) and not contains_any(natural_query, ["자바스크립트", "JavaScript", "javascript"]):
        hint.append("When using Java as a keyword, it's a good idea to exclude JavaScript.")

    if "c++" in natural_query:
        hint.append('You can also get good results by searching for "C++" as well as "c++".')

    if "Java" in natural_query:
        hint.append('You can also get good results by searching for "자바" or "java" as well as "Java".')

    if contains_any(natural_query, ["교수", "근무", "대학교", "박사", "석사", "재직", "졸업", "출신"]) or re.search(r"대\b", natural_query):
        hint.append("Organization name can also be found in intro_author.")

    return '\n'.join(hint) 
