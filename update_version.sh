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
