# python-myPackage
my python package

Terminology
* { Remote name } : Nick name of this used in the parent
* { Child repo } : URL of this repo
* { Child path } : path and folder name below the parrent location
* { Child branch } : Branch name of this in this repo

Initialization    
1. git remote add { Remote name } { Child repo }
    * git remote -v : to check push/pull target information
1. git subtree add --prefix { Child path } { Remote name } { Child branch }
    * { Child path } must not exist before.
    * check the { Child path } is created.

Pus & Pull change of this in the parent directory,
* Push : git subtree push --prefix { Child path } { Remote name } { Child branch }
* Pull : git subtree pull --prefix { Child path } { Remote name } { Child branch }
