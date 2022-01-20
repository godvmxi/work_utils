from email_utils import MailUtils,CryptUtils
import argparse
cmd_args =  None
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-c', '--cfg', dest= "cfg", type=str, help='Runtime config json file')
parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help='Show current config')
parser.add_argument('--encode', dest='encode', action="store_true", help='Cleanup old tests')
parser.add_argument('--decode', dest='decode', action="store_true", help='Cleanup old tests')
parser.add_argument('--json_dir', '--json_dir', dest= "json_dir", type=str, help='Json file list')
parser.add_argument( '--plain_script', dest= "plain_script", type=str, help='Plain Python file')
parser.add_argument( '--crypto_output', dest= "crypto_output", default="crypto_output.py", type=str, help='Crypto Output Python library')
parser.add_argument('--check_new_deploy', dest='check_new_deploy', action="store_true", help='Check the latest deploy test')

if __name__ == "__main__":
    cmd_args = parser.parse_args()
    print(cmd_args)
    if cmd_args.encode :
        crypto = CryptUtils()
        crypto.load_data()
    if cmd_args.decode :
        crypto = CryptUtils()
        crypto.load_data()