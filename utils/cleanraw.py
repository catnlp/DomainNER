# encoding:utf-8
'''
@Author: catnlp
@Email: wk_nlp@163.com
@Time: 2018/5/25 12:39
'''
import os
class CleanRaw:
    def __init__(self, path):
        if os.path.exists(path):
            if path[-1] != '/':
                path += '/'
            self.path = path
        else:
            print('Folder does not exists!')
            exit(1)
        self.raw_path = path

    def clean(self, raw_name='raw.txt', save_name='clean.txt'):
        raw_path = self.path + raw_name
        print('Raw path: %s', raw_path)
        if not os.path.exists(raw_path):
            print('Raw does not exists!')
            exit(1)
        save_path = self.path + save_name
        with open(raw_path) as raw, open(save_path, 'w') as clean:
            content = raw.read()
            content = content.replace('。。', '#catnlp1#')
            content = content.replace('。。。', '#catnlp2#')
            content = content.replace('？？', '#catnlp3#')
            content = content.replace('？？？', '#catnlp4#')
            content = content.replace('？！', '#catnlp5#')
            content = content.replace('。"', '#catnlp6#')
            content = content.replace('。', '。\n')
            content = content.replace('？', '？\n')
            content = content.replace('\n\n', '\n')
            content = content.replace(' ', '') # catnlp
            content = content.replace(' ', '') # catnlp
            content = content.replace('　', '') # catnlp
            content = content.replace('#catnlp1#', '。。')
            content = content.replace('#catnlp2#', '。。。')
            content = content.replace('#catnlp3#', '？？')
            content = content.replace('#catnlp4#', '？？？')
            content = content.replace('#catnlp5#', '？！')
            content = content.replace('#catnlp6#', '。"')
            clean.write(content)

if __name__ == '__main__':
    cleanRaw = CleanRaw('../data/raw')
    cleanRaw.clean('raw.txt')