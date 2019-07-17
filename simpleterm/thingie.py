#!/usr/bin/env python

import cmd
import readline
import sys


class Command(cmd.Cmd):
    prompt = "]> "

    def do_EOF(self, txt):
        print("See ya!")
        sys.exit(0)

    def do_hi(self, txt):
        print("Hello there!")

Command.do_bye = Command.do_EOF

if __name__ == "__main__":
    c = Command()
    c.cmdloop()
