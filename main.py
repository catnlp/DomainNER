# encoding:utf-8
'''
@Author: catnlp
@Email: wk_nlp@163.com
@Time: 2018/5/26 11:02
'''
import argparse
from utils.data import Data
from utils.helper import *

seed_num = 42
random.seed(seed_num)
torch.manual_seed(seed_num)
np.random.seed(seed_num)

import os
os.environ["CUDA_VISIBLE_DEVICES"] = '3'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tuning with NCRF++')
    parser.add_argument('--config', help='Configuration File', default='train.config')
    args = parser.parse_args()

    data = Data()
    data.read_config(args.config)
    status = data.status.lower()
    data.HP_gpu = data.HP_gpu and torch.cuda.is_available()
    print("Seed num:", seed_num)

    if status == 'train':
        print("MODEL: train")
        data_initialization(data)
        data.generate_instance('train')
        # data.generate_instance('dev')
        data.generate_instance('test')
        data.build_pretrain_emb()
        name = 'domain-cws'
        train(data, name)
    elif status == 'decode':
        print("MODEL: decode")
        data.load(data.dset_dir)
        data.read_config(args.config)
        print(data.raw_dir)
        # exit(0)
        data.show_data_summary()
        data.generate_instance('raw')
        print("nbest: %s" % (data.nbest))
        decode_results, pred_scores = load_model_decode(data, 'raw')
        if data.nbest:
            data.write_nbest_decoded_results(decode_results, pred_scores, 'raw')
        else:
            data.write_decoded_results(decode_results, 'raw')
    else:
        print("Invalid argument! Please use valid arguments! (train/test/decode)")
