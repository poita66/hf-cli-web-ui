#!/bin/bash

# Script to update version across the project

NEW_VERSION="$1"

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new_version>"
    exit 1
fi

echo "Updating version to $NEW_VERSION"

# Update backend version
sed -i "s/version = .*/version = \"$NEW_VERSION\"/" backend/pyproject.toml

# Update frontend version
sed -i "s/\"version\": .*/\"version\": \"$NEW_VERSION\",/" frontend/package.json

# Update main VERSION file
echo "$NEW_VERSION" > VERSION

echo "Version updated to $NEW_VERSION in all files"

git add .
git commit -m "Update to version v$NEW_VERSION"

# Create and push git tag if we're on the main branch
if git branch --show-current | grep -q "main"; then
    echo "Creating git tag v$NEW_VERSION"

    git tag -a "v$NEW_VERSION" -m "Version $NEW_VERSION release"
    echo "Tag v$NEW_VERSION created. Push with: git push origin v$NEW_VERSION"
fi

