import json

files_names = [
    './tmp/cvpr13-23.json',
    './tmp/cvpr_24.json',
    './tmp/eccv.json',
    './tmp/iccv.json',
    './tmp/wacv.json',
]
data = []
cnt = 0
for fn in files_names:
    data_file = json.load(open(fn))
    cfs_name = fn.split('/')[-1][:4]
    data.extend(data_file)
    print(len(data), len(data_file))

    for paper in data_file:
        title = paper['title']
        if 'backdoor' in title.lower():
            cnt += 1
            print(cnt, cfs_name, title, paper.get('pdf', ''))

# print(len(data))
# cnt = 0
# for paper in data:
#     title = paper['title']
#     if 'backdoor' in title.lower():
#         cnt += 1
#         print(cnt, title)

# print(cnt)