# Project Versioning

This project follows semantic versioning. The version is maintained in multiple places to ensure consistency across the application.

## Version Files

The version is stored in three main locations:
1. `VERSION` - Main version file
2. `backend/pyproject.toml` - Backend version
3. `frontend/package.json` - Frontend version

## Version Update Process

To update the version across all files:
1. Run the `update_version.sh` script with the new version as an argument:
   ```bash
   ./update_version.sh 0.1.0
   ```

2. Alternatively, manually update each file:
   - Update the VERSION file with the new version
   - Update the version in `backend/pyproject.toml`
   - Update the version in `frontend/package.json`

## Release Process

Releases are created using Git tags. To create a new release:

1. Ensure all changes are committed
2. Run `./update_version.sh <new_version>`
3. Create and push a tag:
   ```bash
   git tag -a v0.1.0 -m "Version 0.1.0 release"
   git push origin v0.1.0
   ```

The GitHub Actions workflow will automatically create a release from the tag.