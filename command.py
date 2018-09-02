from __future__ import unicode_literals, absolute_import

TYPE_SINGLE_CMD = 1         # /pin
TYPE_PARAM = 2              # /delsell 4
TYPE_SEMICOLON = 3          # /msg : Hello
TYPE_PARAM_SEMICOLON = 4    # /msg 123: Hello, 123

class Command():

    def __init__(self, text):
        """
        prepares:
            self.cmd
            self.param
            self.value
            self.type
        """
        stripped = text.strip()
        splitted = stripped.split(':', 1)

        # Process left part
        cmd_par = splitted[0].strip().split(' ', 1)
        self.cmd = cmd_par[0].strip()
        
        if len(cmd_par) == 2:
            self.param = cmd_par[1].strip()
            self.type = TYPE_PARAM
        else:
            self.param = None
            self.type = TYPE_SINGLE_CMD

        # Process right part
        if len(splitted) == 2:
            self.value = splitted[1].strip()
            if self.type == TYPE_SINGLE_CMD:
                self.type = TYPE_SEMICOLON
            else:
                self.type = TYPE_PARAM_SEMICOLON
        else:
            self.value = None

        return

    def is_single_cmd(self):
        return self.type == TYPE_SINGLE_CMD

    def is_param(self):
        return self.type == TYPE_PARAM

    def is_semicolon(self):
        return self.type == TYPE_SEMICOLON

    def is_param_semicolon(self):
        return self.type == TYPE_PARAM_SEMICOLON

    def is_cmd_eq(self, cmd):
        return self.cmd in [cmd, '{}@CombatDetectorBot'.format(cmd)]
        