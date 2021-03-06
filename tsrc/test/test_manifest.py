import os.path

import tsrc.manifest
from tsrc.repo import Repo

import pytest


def test_load():
    contents = """
gitlab:
  url: http://gitlab.example.com
repos:
  - src: foo
    url: git@example.com:foo.git
    branch: next

  - src: master
    url: git@example.com:master.git
    copy:
      - src: top.cmake
        dest: CMakeLists.txt
"""
    manifest = tsrc.manifest.Manifest()
    manifest.load(contents)
    assert manifest.gitlab["url"] == "http://gitlab.example.com"
    assert manifest.repos == [
        tsrc.Repo(src="foo", url="git@example.com:foo.git", branch="next"),
        tsrc.Repo(src="master", url="git@example.com:master.git", branch="master")
    ]
    assert manifest.copyfiles == [
        (os.path.join("master", "top.cmake"), "CMakeLists.txt")
    ]


def test_find():
    contents = """
repos:
  - src: foo
    url: git@example.com:proj_one/foo

  - src: bar
    url: git@example.com:proj_two/bar
"""
    manifest = tsrc.manifest.Manifest()
    manifest.load(contents)
    assert manifest.get_url("foo") == "git@example.com:proj_one/foo"
    assert manifest.get_url("bar") == "git@example.com:proj_two/bar"
    with pytest.raises(tsrc.manifest.RepoNotFound) as e:
        manifest.get_url("no/such")
        assert "no/such" in e.value.message
