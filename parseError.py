import sys
import argparse


def parse_node(node):
    return node.split('created at http')[1].split('/node/')[1].strip('.\n')


def parse_media(media):
    return media.split('Media for')[1].split(" not created")[0]


parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Output from error file.')
parser.add_argument('--secondary', required=False, help='Output from error file after running remediation script.')
args = parser.parse_args()

if args.secondary:
    with open(args.secondary) as f:
        success = []
        lines = f.readlines()
        for line in lines:
            if "INFO" in line:
                words = line.split()
                pid = line.split('/node/')[1].strip('.\n')
                success.append(words[7])

with open(args.input) as f:
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
            if len(line) > 1:
                pair.append(line)
    for candidate in pairs:

        node = parse_node(candidate.pop(0))
        # if len(success) > 0:
        #     if node in success:
        #         continue
        for item in candidate:
            if 'Media' in item:
                media = parse_media(item).strip()
                if len(success) > 0:
                    if media in success:
                        continue
                media_use = ''
                if 'OBJ' in media or 'PDF' in media:
                    media_use = 'http://pcdm.org/use#OriginalFile'
                if 'OCR' in media:
                    media_use = 'http://pcdm.org/use#ExtractedText'
                if 'TN' in media:
                    media_use = 'http://pcdm.org/use#ThumbnailImage'
                output += f"{node}, {media}, {media_use}\n"

print(output)
text_file = open("mediation.csv", "wt")
n = text_file.write(output)
text_file.close()
