#!/usr/bin/env python3

from huggingface_hub import scan_cache_dir

# Check the structure of the cache
cache_dir = scan_cache_dir()
print("Cache dir type:", type(cache_dir))
print("Cache dir attributes:", [attr for attr in dir(cache_dir) if not attr.startswith('_')])

# Check repos
print("\nRepos type:", type(cache_dir.repos))
print("Repos length:", len(cache_dir.repos))

if cache_dir.repos:
    # Convert frozenset to list to access elements
    repos_list = list(cache_dir.repos)
    repo = repos_list[0]
    print("\nFirst repo type:", type(repo))
    print("First repo attributes:", [attr for attr in dir(repo) if not attr.startswith('_')])
    
    # Check revisions
    print("\nRevisions type:", type(repo.revisions))
    print("Revisions length:", len(repo.revisions))
    
    # Check if revisions is a frozenset and convert it
    if hasattr(repo.revisions, '__iter__'):
        revisions_list = list(repo.revisions)
        if revisions_list:
            revision = revisions_list[0]
            print("Revision type:", type(revision))
            print("Revision attributes:", [attr for attr in dir(revision) if not attr.startswith('_')])
            
            # Check if files attribute exists in revision
            if hasattr(revision, 'files'):
                print("Files attribute exists in revision")
                print("Files type:", type(revision.files))
                print("Files length:", len(revision.files))
                if revision.files:
                    # Convert frozenset to list to access elements
                    files_list = list(revision.files)
                    file = files_list[0]
                    print("First file type:", type(file))
                    print("First file attributes:", [attr for attr in dir(file) if not attr.startswith('_')])
            else:
                print("Files attribute does NOT exist in revision")