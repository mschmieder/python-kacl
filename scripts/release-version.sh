#/bin/bash

set -e

VERSION_INCREMENT_SECTION=$1
VERSION_INCREMENT_SECTION=${VERSION_INCREMENT_SECTION:-"patch"}

current_version=$(cat VERSION)

bumpversion --allow-dirty ${VERSION_INCREMENT_SECTION}

new_version=$(cat VERSION)

python3 kacl/kacl_cli.py release $(cat VERSION) --modify
git add CHANGELOG.md kacl/__init__.py VERSION .bumpversion.cfg
git commit -m "Version update ${current_version} --> ${new_version}"
git tag v${new_version}
git push origin --tags