import json

data = json.load(open('./tmp/cvpr13-23.json'))

print(len(data))
cnt = 0
for paper in data:
    title = paper['title']
    if 'backdoor' in title.lower():
        cnt += 1
        print(cnt, title)

print(cnt)