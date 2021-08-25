import sys


def parse_node(node):
    checker = node.split('created at http')
    return node.split('created at http')[1].split('/node/')[1].strip('.\n')


def parse_media(media):
    return media.split('Media for')[1].split(" not created")[0]


if len(sys.argv) > 2:
    with open(sys.argv[2]) as f:
        success = []
        lines = f.readlines()
        for line in lines:
            if "INFO" in line:
                pid = line.split('/node/')[1].strip('.\n')
                success.append(pid)

with open(sys.argv[1]) as f:
    lines = f.readlines()
    pairs = []
    pair = []
    output = 'node_id, file, media_use_tid\n'
    breaker = '--\n'
    if lines[-1] != breaker:
        lines.append(breaker)

    for line in lines:
        if line == breaker:

            if len(pair) > 0:
                pairs.append(pair.copy())
            pair.clear()
        else:
            pair.append(line)
    for candidate in pairs:

        node = parse_node(candidate.pop(0))
        for item in candidate:
            if 'Media' in item:
                media = parse_media(item)
                media_use = ''
                if 'OBJ' in media or 'PDF' in media:
                    media_use = 'http://pcdm.org/use#OriginalFile'
                if 'OCR' in media:
                    media_use = 'http://pcdm.org/use#ExtractedText'
                if 'TN' in media:
                    media_use = 'http://pcdm.org/use#ThumbnailImage'
                output += node + ", " + media + ", " + media_use + '\n'

print(output)
text_file = open("mediation.csv", "wt")
n = text_file.write(output)
text_file.close()

