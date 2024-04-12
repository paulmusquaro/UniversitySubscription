from typing import List, Any, Optional
import redis
from redis_lru import RedisLRU
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_name(tag: str) -> List[Optional[str]]:
    print(f"Find by name {tag}")
    authors = Author.objects(fullname__iregex=tag)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tag: str) -> List[Optional[str]]:
    print(f"Find by tags: {tag}")
    tags = tag.split(",")
    result = None
    if len(tags) == 1:
        quotes = Quote.objects(tags__iregex=tags[0])
        result = [q.quote for q in quotes]
    if len(tags) > 1:
        quotes = Quote.objects(tags__all=tags)
        result, *_ = [q.quote for q in quotes]
    return result


commands = {
    "name": find_by_name,
    "tag": find_by_tags,

}

if __name__ == '__main__':
    while True:
        command = input("Enter the command: ")
        if command == "exit":
            break
        try:
            action, argument = command.split(":")
            if action in commands.keys():
                print(commands.get(action)(argument))
        except ValueError:
            print("Wrong command. Example: 'command:value'")
