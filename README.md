# python-myPackage
my python package

---
* git subtree pull/push --prefix myPkgBasic myPkgBasic main
---

<H3> Terminology </H3>

* { Remote name } : Nick name of this used in the parent
* { Child repo } : URL of this repo
* { Child path } : path and folder name below the parrent location
* { Child branch } : Branch name of this in this repo

<H3> Initialization </H3>

1. git remote add { Remote name } { Child repo }
    * <i> git remote add myPkgBasic https://github.com/qocop77/python-myBasicPack.git </i>
    * git remote -v : to check push/pull target information
1. git subtree add --prefix { Child path } { Remote name } { Child branch }
    * <i> git subtree add --prefix myPkgBasic myPkgBasic main </i>
    * { Child path } must not exist before.
    * check the { Child path } is created.

<H3> Push & Pull change of this in the parent directory </H3>

* Push : git subtree push --prefix { Child path } { Remote name } { Child branch }
* Pull : git subtree pull --prefix { Child path } { Remote name } { Child branch }
