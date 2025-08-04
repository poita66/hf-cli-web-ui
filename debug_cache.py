#!/usr/bin/env python3

from huggingface_hub import scan_cache_dir

# Check the structure of the cache
cache_dir = scan_cache_dir()
print("Cache dir attributes:", [attr for attr in dir(cache_dir) if not attr.startswith('_')])
print("\nCache dir type:", type(cache_dir))

# Print the structure of repos
print("\nRepos:")
for i, repo in enumerate(cache_dir.repos):
    print(f"Repo {i}:")
    print("  Attributes:", [attr for attr in dir(repo) if not attr.startswith('_')])
    print("  Repo path:", repo.repo_path)
    print("  Size on disk:", repo.size_on_disk)
    print("  Number of files:", repo.nb_files)
    break  # Just show first repo for now
