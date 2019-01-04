#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2019/1/2 20:16
# @Author  : Zhanhui
# @File    : my_git.py


"""
    Git package : gitpython
"""


import os

from git import diff, exc, Repo


class MyRepo(object):
    def __init__(self, repo_path):
        self.repo = None
        self.err = None
        self.repo_path = None

        self._default_branch = "master"

        # init repo obj by repo_path.
        self.__init_repo_obj(repo_path)

    def __init_repo_obj(self, repo_path):
        """
        Init repo obj by repo_path.
        :param repo_path:
        :return:
        """

        if repo_path:
            if os.path.isdir(os.path.realpath(repo_path)):
                try:
                    self.repo = Repo(repo_path)
                    self.repo_path = repo_path
                except exc.NoSuchPathError:
                    pass
                except Exception as e:
                    self.err = e
            else:
                self.err = "Repo path is not a folder"
        else:
            self.err = "No repo path"

    @property
    def commit_diff_files(self):
        """
        Get repo commit diff file list.
        :return:
        """

        commit_diff_file_list = list()

        if not self.err:
            commit_diff_obj_list = self.repo.index.diff(self.repo.head.commit)
            commit_diff_file_list = self.__get_attr_list_from_diff_obj_list(commit_diff_obj_list)

        return commit_diff_file_list

    @property
    def modify_diff_files(self):
        """
        Get repo modify diff file list.
        :return:
        """

        modify_diff_file_list = list()

        if not self.err:
            modify_diff_obj_list = self.repo.index.diff(None)
            modify_diff_file_list = self.__get_attr_list_from_diff_obj_list(modify_diff_obj_list)

        return modify_diff_file_list

    @property
    def untracked_files(self):
        """
        Get repo untracked file list.
        :return:
        """

        untracked_file_list = list()

        if not self.err:
            untracked_file_list = self.repo.untracked_files

        return untracked_file_list

    @staticmethod
    def __get_attr_list_from_diff_obj_list(diff_obj_list, attr="a_path"):
        """
        Get path from diff obj list.
        :param diff_obj_list: repo diff obj list.
        :param attr: the attr need get from diff obj.
        :return:
        """

        value_list = list()

        if isinstance(diff_obj_list, list) and diff_obj_list:
            for diff_obj in diff_obj_list:
                if isinstance(diff_obj, diff.Diff):
                    value = getattr(diff_obj, attr)

                    if value:
                        value_list.append(value)

        return value_list

    @property
    def is_dirty(self):
        """
        Return is the current workspace clean.
        :return:
        """

        clean = True

        if not self.err:
            clean = self.repo.is_dirty()

        return clean

    @property
    def active_branch(self):
        """
        Return current branch.
        :return:
        """

        current_branch = None

        if not self.err:
            current_branch = self.repo.active_branch

        return current_branch

    def pull(self, branch_name=None):
        """
        Retrieving current branch from remote.
        :param branch_name: pull branch. We will check if the branch eq current branch.
        :return: result : boolean value, pull success or not.
        """

        result = False

        if not self.err:
            if branch_name is None:
                branch_name = self._default_branch

            # check and checkout branch
            if self.__sync_branch(branch_name):
                try:
                    self.repo.remote().pull()
                except Exception as e:
                    self.err = e
                else:
                    result = True

        return result

    def push(self, branch_name=None):
        """
        Push local branch to remote.
        :param branch_name: pull branch. We will check if the branch eq current branch.
        :return: result : boolean value, push success or not.
        """

        result = False

        if not self.err:
            if branch_name is None:
                branch_name = self._default_branch

            # Check and checkout branch.
            if self.__sync_branch(branch_name):
                try:
                    self.repo.remote().push()
                except Exception as e:
                    self.err = e
                else:
                    result = True

        return result

    def __sync_branch(self, branch_name=None):
        """
        Check and checkout branch.
        :param branch_name: branch name that want to sync.
        :return: check : boolean value of check and checkout branch result.
        """

        check = False

        if not self.err:
            if branch_name is None:
                branch_name = self._default_branch

            if self.active_branch == branch_name:
                check = True
            else:
                if self.checkout_branch(branch_name):
                    check = True

        return check

    def checkout_branch(self, branch_name=None):
        """
        Checkout to branch_name
        :param branch_name: the branch name need checkout to.
        :return: checkout : boolean value, the result of checkout operation.
        """

        checkout = False

        if not self.err:
            if branch_name is None:
                branch_name = self._default_branch

            # Get branch_name obj
            try:
                branch_obj = getattr(self.repo.heads, branch_name)
            except AttributeError:
                self.err = "No branch : %s" % branch_name
            else:
                branch_obj.checkout()
                checkout = True

        return checkout

    def reset(self, reset_file_list=None):
        """
        Reset
        :return:
        """

    def checkout(self, checkout_file_list=None):
        """
        Check out modify files.
        :param checkout_file_list:
        :return:
        """

        result = False

        if not self.err:
            if not isinstance(checkout_file_list, list):
                checkout_file_list = self.modify_diff_files

            if checkout_file_list:
                pass

        result = True


if __name__ == "__main__":
    # test_repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    test_repo_path = r"M:\10.code\glib"
    repo_obj = MyRepo(test_repo_path)

    # print(repo_obj.commit_diff_files)
    # print(repo_obj.modify_diff_files)
    # print(repo_obj.untracked_files)
    #
    # print(repo_obj.is_dirty)
    # print(repo_obj.active_branch)

    print(repo_obj.active_branch)
    repo_obj.checkout_branch("master")

    print(repo_obj.err)
