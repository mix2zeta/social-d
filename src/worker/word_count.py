
import asyncio
from datetime import datetime

from pythainlp import word_tokenize


async def get_count_by_list(data:list, return_value:str='wordcount') -> dict:
    wordcount = {}
    hashtag = {}
    mention = {}
    for row in data:
        word_list = word_tokenize(row['message'], keep_whitespace=False)

        for word in get_word_or_hashtag(word_list):
            if word[0] == '@' and return_value == 'mention':
                if word in mention.keys():
                    mention[word] += 1
                else :
                    mention[word] = 1
            elif word[0] == '#' and return_value == 'hashtag':
                if word in hashtag.keys():
                    hashtag[word] += 1
                else :
                    hashtag[word] = 1
            else:
                if word in wordcount.keys():
                    wordcount[word] += 1
                else :
                    wordcount[word] = 1

    if return_value == 'mention':
        return mention
    if return_value == 'hashtag':
        return hashtag
    return wordcount


def get_word_or_hashtag(word_list:list) -> str:
    result = ''
    for word in word_list:
        if word == '@':
            result += '@'
            continue
        if word == '#':
            result += '#'
            continue
        result += word
        yield result
        result = ''