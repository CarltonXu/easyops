#!/usr/bin/env python
# coding:utf8
"""
A Python wrapper for rclone.
"""

import logging
import subprocess
import tempfile

class RClone:
    """
    Wrapper class for rclone.
    """

    def __init__(self, cfg):
        if not cfg:
            self.cfg = ""
        else:
            self.cfg = cfg.replace("\\n", "\n")
        self.log = logging.getLogger("RClone")

    def _execute(self, command_with_args):
        """
        Execute the given `command_with_args` using Popen
        Args:
            - command_with_args (list) : An array with the command to execute,
                                         and its arguments. Each argument is given
                                         as a new element in the list.
        """
        self.log.debug("Invoking : %s", " ".join(command_with_args))
        try:
            proc = subprocess.Popen(
                    command_with_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            (out, err) = proc.communicate()

            #out = proc.stdout.read()
            #err = proc.stderr.read()

            self.log.debug(out)
            if err:
                self.log.warning(err.decode("utf-8").replace("\\n", "\n"))

            return {
                "code": proc.returncode,
                "out": out,
                "error": err
            }
        except FileNotFoundError as not_found_e:
            self.log.error("Executable not found. %s", not_found_e)
            return {
                "code": -20,
                "error": not_found_e
            }
        except Exception as generic_e:
            self.log.exception("Error running command. Reason: %s", generic_e)
            return {
                "code": -30,
                "error": generic_e
            }

    def run_cmd(self, command, extra_args=[]):
        """
        Execute rclone command
        Args:
            - command (string): the rclone command to execute.
            - extra_args (list): extra arguments to be passed to the rclone command
        """
        # save the configuration in a temporary file
        with tempfile.NamedTemporaryFile(mode='wt', delete=True) as cfg_file:
            # cfg_file is automatically cleaned up by python
            self.log.debug("rclone config: ~%s~", self.cfg)
            cfg_file.write(self.cfg)
            cfg_file.flush()

            command_with_args = ["rclone", command, "--config", cfg_file.name]
            command_with_args += extra_args
            command_result = self._execute(command_with_args)
            cfg_file.close()
            return command_result

    def copy(self, source, dest, flags=[]):
        """
        Executes: rclone copy source:path dest:path [flags]
        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone copy --help` flags.
        """
        return self.run_cmd(command="copy", extra_args=[source] + [dest] + flags)

    def sync(self, source, dest, flags=[]):
        """
        Executes: rclone sync source:path dest:path [flags]
        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone sync --help` flags.
        """
        return self.run_cmd(command="sync", extra_args=[source] + [dest] + flags)

    def listremotes(self, flags=[]):
        """
        Executes: rclone listremotes [flags]
        Args:
        - flags (list): Extra flags as per `rclone listremotes --help` flags.
        """
        return self.run_cmd(command="listremotes", extra_args=flags)

    def ls(self, dest, flags=[]):
        """
        Executes: rclone ls remote:path [flags]
        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        return self.run_cmd(command="ls", extra_args=[dest] + flags)

    def lsf(self, dest, flags=[]):
        """
        Executes: rclone lsf remote:path [flags]
        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        return self.run_cmd(command="lsf", extra_args=[dest] + flags)

    def lsjson(self, dest, flags=[]):
        """
        Executes: rclone lsjson remote:path [flags]
        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        return self.run_cmd(command="lsjson", extra_args=[dest] + flags)

    def delete(self, dest, flags=[]):
        """
        Executes: rclone delete remote:path
        Args:
        - dest (string): A string "remote:path" representing the location to delete.
        """
        return self.run_cmd(command="delete", extra_args=[dest] + flags)

    def rmdir(self, dest, flags=[]):
        """
        Executes: rclone rmdir remote:path
        Args:
        - dest (string): A empty directory "remote:path" representing the location to delete.
        """
        return self.run_cmd(command="rmdir", extra_args=[dest] + flags)


def with_config(cfg):
    """
    Configure a new RClone instance.
    """
    inst = RClone(cfg=cfg)
    return inst