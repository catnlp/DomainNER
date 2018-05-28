# encoding:utf-8
'''
@Author: catnlp
@Email: wk_nlp@163.com
@Time: 2018/5/25 14:40
'''
import os
import re
import json

class GenerateData:
    def __init__(self, path):
        if os.path.exists(path):
            if path[-1] != '/':
                path += '/'
            self.path = path
        else:
            print('Folder does not exists!')
            exit(1)
        self.path = path

    def generateTrain(self, clean_name='clean.txt', dict_name='dict.txt', train_name='train.bmes'):
        clean_path = self.path + clean_name
        print('Clean path: %s', clean_path)
        if not os.path.exists(clean_path):
            print('Clean does not exists!')
            exit(1)
        train_path = self.path + train_name

        rule = ''
        dict_tag = {}
        dict_path = self.path + dict_name
        with open(dict_path) as dict:
            lines = dict.readlines()
            for line in lines:
                line = line.replace('\n', '')
                word = line.split('\t')
                rule += word[0] + '|'
                dict_tag[word[0]] = word[1]
            if rule[-1] == '|':
                rule = rule[:-1]

        with open(clean_path) as clean, open(train_path, 'w') as train:
            lines = clean.readlines()
            str = ''
            for line in lines:
                line = line.replace('\n', '')
                if line == '':
                    continue
                s = re.compile(rule)
                tmp = 0
                answers = s.finditer(line)
                if answers:
                    for i in answers:
                        for j in range(tmp, i.start()):
                            str += line[j] + '\tO\n'
                        tag = dict_tag[i.group()]
                        if i.start() + 1 == i.end():
                            str += line[i.start()] + '\tS-' + tag + '\n'
                        else:
                            str += line[i.start()] + '\tB-' + tag + '\n'
                            for j in range(i.start()+1, i.end()-1):
                                str += line[j] + '\tM-' + tag + '\n'
                            str += line[i.end()-1] + '\tE-' + tag + '\n'
                        tmp = i.end()
                    for j in range(tmp, len(line)):
                        str += line[j] + '\tO\n'
                else:
                    for i in range(len(line)):
                        str += line[i] + '\tO\n'
                str += '\n'
            train.write(str[: -1])

    def generateTest(self, origin_path, test_name='test.bmes'):
        test_path = self.path + test_name

        with open(origin_path) as origin, open(test_path, 'w') as test:
            lines = origin.readlines()
            str = ''
            for line in lines:
                line = json.loads(line)
                if line['answer'] == 'reject':
                    continue

                tag = line.get('spans')
                content = line['text']
                current = 0
                if tag:
                    entityList = line['spans']
                    for entity in entityList:
                        for i in range(current, entity['start']):
                            if content[i] == ' ' or content[i] == ' ' or content[i] == '　':
                                continue
                            str += content[i] + '\tO\n'
                            if content[i] == '。' or content[i] == '？':
                                str += '\n'
                        tag = entity['label']
                        if entity['start'] + 1 == entity['end']:
                            str += content[entity['start']] + '\tS-' + tag + '\n'
                        else:
                            str += content[entity['start']] + '\tB-' + tag + '\n'
                            for i in range(entity['start']+1, entity['end']-1):
                                str += content[i] + '\tM-' + tag + '\n'
                            str += content[entity['end']-1] + '\tE-' + tag + '\n'
                        current = entity['end']
                    for i in range(current, len(content)):
                        if content[i] == ' ' or content[i] == ' ' or content[i] == '　':
                            continue
                        str += content[i] + '\tO\n'
                        if content[i] == '。' or content[i] == '？':
                            str += '\n'

                else:
                    for i in range(len(content)):
                        if content[i] == ' ' or content[i] == ' ' or content[i] == '　':
                            continue
                        str += content[i] + '\tO\n'
                        if content[i] == '。' or content[i] == '？':
                            str += '\n'
                str += '\n'
            # clean data
            str = str.replace('。\tO\n\n。\tO\n', '。\tO\n。\tO\n')
            str = str.replace('？\tO\n\n？\tO\n', '？\tO\n？\tO\n')
            str = str.replace('？\tO\n\n！\tO\n', '？\tO\n！\tO\n')
            str = str.replace('\n\n\n', '\n\n')
            str = str.replace('。\tO\n\n。\tO\n', '。\tO\n。\tO\n')
            str = str.replace('？\tO\n\n？\tO\n', '？\tO\n？\tO\n')
            str = str.replace('？\tO\n\n！\tO\n', '？\tO\n！\tO\n')

            test.write(str)

if __name__ == '__main__':
    generate = GenerateData('../data/raw')
    generate.generateTrain('clean.txt', 'dict.txt', 'train.bmes')
    generate.generateTest('../data/origin/Anti-fraud Product Data/Intel-05-17.jsonl', 'test.bmes')