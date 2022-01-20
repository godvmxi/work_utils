#!/usr/bin/env python3

import sys
import argparse
cmd_args =  None
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-c', '--cfg', dest= "cfg", type=str, help='Runtime config json file')
parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help='Show current config')
parser.add_argument('--base_on_library', dest='base_on_library', action="store_true", help='All test based on so library test')
parser.add_argument('--email_send_test', dest='email_send_test', action="store", help='Send A test email to some one')

if __name__ == "__main__":
    cmd_args = parser.parse_args()

    if cmd_args.base_on_library:
        from lib.email_utils import MailUtils
        pass
    else:
        from email_utils import MailUtils
    if cmd_args.email_send_test:
        mail= MailUtils()
        mail.SendEmail(cmd_args.email_send_test.split(","),"test_title", "test body", [])
        sys.exit(0)


