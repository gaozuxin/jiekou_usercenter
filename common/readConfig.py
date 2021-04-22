# -*- coding: utf-8 -*-
import configparser


def read_config(cfg_file):
    cfg = configparser.ConfigParser()
    cfg.read(cfg_file)
    return cfg


# cfg = read_config(os.path.dirname(os.path.dirname(__file__)) + '/cfg/config.ini')

# if __name__ == "__main__":
#     cfg = read_config(os.path.dirname(os.path.dirname(__file__)) + '/cfg/config.ini')
#     print(cfg.get('base_para', 'base_url'))
