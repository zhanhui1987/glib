#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2019/1/2 20:16
# @Author  : Zhanhui
# @File    : my_git.py


"""
    Git package : gitpython
"""


import os

from git import diff, exc, Repo, refs


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

    # ==== class external func START ==== #

    def pull(self, branch_name=None):
        """
        Retrieving current branch from remote.
        :param branch_name: pull branch. We will check if the branch eq current branch.
        :return: result : boolean value, pull success or not.
        """

        result = False

        if self.err is None:
            if branch_name is None:
                branch_name = self._default_branch

            # check and checkout branch
            branch_obj = self.__sync_branch(branch_name)
            if self.__check_branch_obj(branch_obj):
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

        if self.err is None:
            if branch_name is None:
                branch_name = self._default_branch

            # Check and checkout branch.
            branch_obj = self.__sync_branch(branch_name)
            if self.__check_branch_obj(branch_obj):
                try:
                    self.repo.remote().push()
                except Exception as e:
                    self.err = e
                else:
                    result = True

        return result

    def checkout_branch(self, branch_name=None):
        """
        Checkout to branch_name
        :param branch_name: the branch name need checkout to.
        :return: checkout : boolean value, the result of checkout operation.
        """

        checkout = False

        if self.err is None:
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

    def reset(self, reset_file_list=None, branch_name=None):
        """
        Reset to be committed files.
        :return:
        """

        result = False

        if self.err is None:
            # checkout to branch
            branch_obj = self.__sync_branch(branch_name)
            if self.__check_branch_obj(branch_obj):
                # get commit diff files
                commit_diff_file_list = self.commit_diff_files

                # check reset_file_list
                if reset_file_list is None:
                    reset_file_list = commit_diff_file_list
                else:
                    if isinstance(reset_file_list, list):
                        # check reset files are all in commit_diff_files or not.
                        error_reset_file_list = list()
                        for reset_file in reset_file_list:
                            if reset_file not in commit_diff_file_list:
                                error_reset_file_list.append(reset_file)

                        if error_reset_file_list:
                            self.err = "Reset files not in commit diff files : %s" \
                                       % ", ".join(error_reset_file_list)
                    else:
                        self.err = "Reset files must be a list"

                if self.err is None:
                    if reset_file_list:
                        reset_success_count = 0
                        git_obj = self.repo.git

                        for reset_file in reset_file_list:
                            # reset reset_file
                            try:
                                git_obj.reset(reset_file)
                            except Exception as e:
                                self.err = e
                                break
                            else:
                                reset_success_count += 1

                        if reset_success_count == len(reset_file_list):
                            result = True
                    elif len(commit_diff_file_list) == len(reset_file_list) == 0:
                            result = True

        return result

    def checkout_file(self, checkout_file_list=None, branch_name=None):
        """
        Check out modify files.
        :param checkout_file_list: need checkout file list
        :param branch_name: branch of need checkout files belong to
        :return:
        """

        result = False

        if self.err is None:
            # checkout to branch
            branch_obj = self.__sync_branch(branch_name)
            if self.__check_branch_obj(branch_obj):
                # get modify file list
                modify_file_list = self.modify_diff_files

                # check checkout_file_list
                if checkout_file_list is None:
                    checkout_file_list = modify_file_list
                else:
                    if isinstance(checkout_file_list, list):
                        # check checkout files are all in modify_file_list or not.
                        error_checkout_file_list = list(set(checkout_file_list).difference(set(modify_file_list)))
                        if error_checkout_file_list:
                            self.err = "Checkout files not in modify files : %s" \
                                       % ", ".join(error_checkout_file_list)
                    else:
                        self.err = "Checkout files must be a list"

                if self.err is None:
                    if checkout_file_list:
                        checkout_success_count = 0
                        git_obj = self.repo.git

                        for checkout_file in checkout_file_list:
                            # checkout file
                            try:
                                git_obj.checkout(checkout_file)
                            except Exception as e:
                                self.err = e
                                break
                            else:
                                checkout_success_count += 1

                        if checkout_success_count == len(checkout_file_list):
                            result = True
                    elif len(checkout_file_list) == len(modify_file_list) == 0:
                        result = True

        return result

    def add(self, add_file_list=None, branch_name=None):
        """
        Git add untracked files.
        :param add_file_list: file list which need to add.
        :param branch_name: branch name.
        :return:
        """

        result = False

        print(add_file_list)

        if self.err is None:
            # checkout to branch
            branch_obj = self.__sync_branch(branch_name)
            if self.__check_branch_obj(branch_obj):
                # get can add file list
                can_add_file_list = list(set(self.untracked_files).union(set(self.modify_diff_files)))

                # check add_file_list
                add_file_list = self.__check_file_list(add_file_list, can_add_file_list, "Add", "untracked / modify")

                if self.err is None:
                    if add_file_list:
                        # execute git cmd for each file in file_list
                        if self.__execute_git_cmd(self.repo.git.add, add_file_list):
                            result = True
                    elif len(add_file_list) == len(can_add_file_list) == 0:
                        result = True

        return result

    def clean(self, branch_name=None, rm_untracked_file=False):
        """
        Reset all commit diff files and modify diff files.
        :return:
        """

        result = False

        if self.err is None:
            self.reset(branch_name=branch_name)
            self.checkout_file(branch_name=branch_name)

            # check whether need rm untracked files or not.
            if rm_untracked_file:
                if self.untracked_files:
                    for file in self.untracked_files:
                        file_path = os.path.realpath(os.path.join(self.repo_path, file))
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            self.err = e
                            break

            # check clean result
            if not self.commit_diff_files and not self.modify_diff_files:
                if rm_untracked_file:
                    if not self.untracked_files:
                        result = True
                else:
                    result = True

        return result

    def commit(self, commit_msg="", file_list=None, branch_name=None, commit_all=False):
        """
        Commit the commit files.
        :param commit_msg: commit msg.
        :param file_list: the file list which need to commit. If it is empty, commit the commit_file_list; if not, check
         untracked files and modify files, git add those files which are both in file_list and untracked_files and
         modify_files, then commit.
        :param branch_name: the branch name which need to commit.
        :param commit_all: commit all option. If it is True, we will git add all untracked files and modify files before
        commit; if it is False, only commit the commit_diff_files.
        :return:
        """

        result = False

        if self.err is None:
            # checkout to branch
            branch_obj = self.__sync_branch(branch_name)
            if self.__check_branch_obj(branch_obj):
                # add files in file_list which are also in modify_file_list or untracked_file_list
                self.__add_file_list(file_list, branch_name=branch_name)

                # check commit_all. If it is True, need git add untracked_diff_files and modify_diff_files.
                if commit_all:
                    self.__add_file_list(self.untracked_files, branch_name=branch_name)
                    self.__add_file_list(self.modify_diff_files, branch_name=branch_name)

                if self.err is None:
                    processed_file_list = self.__check_commit_file_list(file_list, branch_name=branch_name)

                    if self.err is None:
                        if processed_file_list:
                            git_obj = self.repo.git
                            git_obj.commit("-m", "%s" % commit_msg)
                            result = True
                        else:
                            self.err = "No files remainder after check file_list"

        return result

    # ==== class external func END ==== #

    # ==== class internal func START ==== #

    def __sync_branch(self, branch_name=None):
        """
        Check and checkout branch.
        :param branch_name: branch name that want to sync.
        :return: check : boolean value of check and checkout branch result.
        """

        branch_obj = None

        if self.err is None:
            if branch_name is None:
                branch_name = self._default_branch

            if self.active_branch == branch_name:
                branch_obj = getattr(self.repo.heads, branch_name)
            else:
                if self.checkout_branch(branch_name):
                    branch_obj = getattr(self.repo.heads, branch_name)

        return branch_obj

    def __check_file_list(self, origin_file_list, target_file_list, file_type="", error_detail=""):
        """
        Check files in origin_file_list are all in target_file_list or not.
        :param origin_file_list: origin file list
        :param target_file_list: target file list
        :param error_detail: error detail
        :return: origin_file_list: file list after check
        """

        if isinstance(target_file_list, list):
            if origin_file_list is None:
                origin_file_list = target_file_list
            elif isinstance(origin_file_list, list):
                # check files are all in target_file_list or not.
                error_file_list = list()
                for file in origin_file_list:
                    if file not in target_file_list:
                        error_file_list.append(file)

                if error_file_list:
                    self.err = "%s files not in %s files : %s" % (file_type, error_detail, ", ".join(error_file_list))
            else:
                self.err = "%s files must be a list" % file_type

        return origin_file_list

    def __execute_git_cmd(self, func, file_list):
        """
        Execute git func for each file in file_list and return execute result.
        :param func:
        :param file_list:
        :return: result : execute result
        """

        result = False

        if isinstance(file_list, list):
            # record execute success count
            success_count = 0

            for file in file_list:
                try:
                    func(file)
                except Exception as e:
                    self.err = e
                    break
                else:
                    success_count += 1

            if success_count == len(file_list):
                result = True

        return result

    def __get_list_diff(self, list_1, list_2):
        """
        Get diff str in list_1 and list_2.
        :param list_1:
        :param list_2:
        :return:
        """

        only_in_1_list = list(set(list_1).difference(set(list_2)))
        only_in_2_list = list(set(list_2).difference(set(list_1)))

        return only_in_1_list, only_in_2_list

    def __add_file_list(self, file_list, branch_name=None):
        """
        Add files in file_list which are also in modify_file_list or untracked_file_list.
        :param file_list:
        :return:
        """

        if self.err is None:
            if isinstance(file_list, list) and file_list:
                both_in_untracked_file_list = list(set(file_list).intersection(set(self.untracked_files)))
                both_in_modify_file_list = list(set(file_list).intersection(set(self.modify_diff_files)))

                both_file_list = list(set(both_in_untracked_file_list).union(set(both_in_modify_file_list)))

                if both_file_list:
                    self.add(both_file_list, branch_name=branch_name)

    def __check_commit_file_list(self, file_list, branch_name=None):
        """
        Check commit file_list and process it.
        :param file_list:
        :return:
        """

        processed_file_list = list()

        commit_file_list = self.commit_diff_files
        if commit_file_list:
            # check file list and process it.
            if file_list is None:
                processed_file_list = commit_file_list
            else:
                if isinstance(file_list, list):
                    if file_list:
                        # check if file in file_list are all both in commit_file_list
                        not_in_commit_list, only_in_commit_list = self.__get_list_diff(file_list, commit_file_list)

                        if not_in_commit_list:
                            # Those files are error files.
                            self.err = "Find files not in commit file list : %s" % ", ".join(not_in_commit_list)
                        elif only_in_commit_list:
                            # Those files need to be reset.
                            self.reset(only_in_commit_list, branch_name=branch_name)

                        if self.err is None and self.commit_diff_files:
                            processed_file_list = self.commit_diff_files
                    else:
                        self.err = "File list which need to commit can not be empty"
                else:
                    self.err = "Files which need to commit must be a list"

        if not processed_file_list and self.err is None:
            self.err = "No commit files"

        return processed_file_list

    # ==== class internal func END ==== #

    # ==== class property func START ==== #

    @property
    def commit_diff_files(self):
        """
        Get repo commit diff file list.
        :return:
        """

        commit_diff_file_list = list()

        if self.err is None:
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

        if self.err is None:
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

        if self.err is None:
            untracked_file_list = self.repo.untracked_files

        return untracked_file_list

    @property
    def is_dirty(self):
        """
        Return is the current workspace clean or not.
        :return:
        """

        dirty = False

        if self.err is None:
            dirty = self.repo.is_dirty()

        return dirty

    @property
    def active_branch(self):
        """
        Return current branch.
        :return:
        """

        current_branch = None

        if self.err is None:
            current_branch = self.repo.active_branch

        return current_branch

    # ==== class property func END ==== #

    # ==== class staticmethod func START ==== #

    @staticmethod
    def __get_attr_list_from_diff_obj_list(diff_obj_list, attr="a_path"):
        """
        Get path from diff obj list.
        :param diff_obj_list: repo diff obj list.
        :param attr: the attr need get from diff obj.
        :return:
        """

        value_list = list()

        if attr is not None and isinstance(diff_obj_list, list) and diff_obj_list:
            for diff_obj in diff_obj_list:
                if isinstance(diff_obj, diff.Diff):
                    value = getattr(diff_obj, attr)

                    if value:
                        value_list.append(value)

        return value_list

    @staticmethod
    def __check_branch_obj(branch_obj):
        """
        Check branch obj is correct branch obj or not.
        :param branch_obj:
        :return:
        """

        check = False

        if isinstance(branch_obj, refs.head.Head):
            check = True

        return check

    # ==== class staticmethod func END ==== #


if __name__ == "__main__":
    # test_repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    test_repo_path = r"M:\10.code\glib"
    repo_obj = MyRepo(test_repo_path)

    # print(repo_obj.commit_diff_files)
    # print(repo_obj.modify_diff_files)
    # print(repo_obj.untracked_files)

    # reset commit files
    # print(repo_obj.commit_diff_files)
    # print(repo_obj.reset())
    # print(repo_obj.commit_diff_files)

    # add untracked files
    # print(repo_obj.untracked_files)
    # print(repo_obj.add())
    # print(repo_obj.untracked_files)

    # checkout -- modify files
    # print(repo_obj.modify_diff_files)
    # print(repo_obj.checkout_file())
    # print(repo_obj.modify_diff_files)

    # print(repo_obj.commit("Commit my_modify file", commit_all=True))

    # print(repo_obj.push())

    print(repo_obj.err)
