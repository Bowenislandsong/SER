# Release Guide for SER

This document describes how to release new versions of the SER library across different platforms.

## Prerequisites

Before releasing, ensure:
1. All tests pass locally and in CI
2. Documentation is up to date
3. CHANGELOG is updated with new version notes
4. Version number is updated in `pyproject.toml` and `ser/__init__.py`

## Release Checklist

- [ ] Update version number in `pyproject.toml`
- [ ] Update version number in `ser/__init__.py`
- [ ] Update version number in `conda/meta.yaml`
- [ ] Update CHANGELOG.md with release notes
- [ ] Commit all changes
- [ ] Create and push a git tag
- [ ] Wait for automated workflows to complete

## PyPI Release (Automated)

The library is automatically published to PyPI when a new release is created on GitHub.

### Steps:

1. **Update version numbers** in the files mentioned above
2. **Commit changes**:
   ```bash
   git add pyproject.toml ser/__init__.py conda/meta.yaml
   git commit -m "Bump version to X.Y.Z"
   git push origin main
   ```

3. **Create a git tag**:
   ```bash
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin vX.Y.Z
   ```

4. **Create a GitHub Release**:
   - Go to https://github.com/Bowenislandsong/SER/releases/new
   - Select the tag you just created
   - Add release notes
   - Publish the release

5. **Automated publishing**:
   - The GitHub Action will automatically build and publish to PyPI
   - Check the Actions tab to monitor progress
   - Verify on PyPI: https://pypi.org/project/ser-algorithms/

### Manual PyPI Release (if needed)

If automated release fails, you can publish manually:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI
twine upload dist/*
```

**Note**: You need a PyPI API token saved as `PYPI_API_TOKEN` in repository secrets.

## Conda Release

The conda package is built from the PyPI release.

### Steps:

1. **Wait for PyPI release to complete**

2. **Update conda-forge feedstock**:
   - Fork https://github.com/conda-forge/ser-algorithms-feedstock
   - Update the recipe with new version and SHA256
   - Create a pull request

3. **Automated build**:
   - conda-forge bots will automatically test and merge
   - Package will be available on conda-forge channel

### Manual Conda Build (for testing)

```bash
# Install conda-build
conda install conda-build

# Build the package
conda build conda/

# Upload to your channel (optional)
anaconda upload /path/to/package.tar.bz2
```

## Docker Release (Automated)

Docker images are automatically built and published to GitHub Container Registry when a release is created.

### Steps:

1. **Automated building**: When you create a GitHub release, the Docker workflow runs automatically

2. **Check the image**:
   - Go to https://github.com/Bowenislandsong/SER/pkgs/container/ser
   - Verify the new image is available

3. **Pull and test**:
   ```bash
   docker pull ghcr.io/bowenislandsong/ser:latest
   docker pull ghcr.io/bowenislandsong/ser:vX.Y.Z
   docker run -it ghcr.io/bowenislandsong/ser:latest python
   ```

### Manual Docker Build and Push

```bash
# Build the image
docker build -t ghcr.io/bowenislandsong/ser:vX.Y.Z .
docker tag ghcr.io/bowenislandsong/ser:vX.Y.Z ghcr.io/bowenislandsong/ser:latest

# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push the images
docker push ghcr.io/bowenislandsong/ser:vX.Y.Z
docker push ghcr.io/bowenislandsong/ser:latest
```

## GitHub Pages (Automated)

The documentation website is automatically deployed to GitHub Pages when changes are pushed to main.

### Steps:

1. **Update documentation** in the `docs/` directory

2. **Commit and push**:
   ```bash
   git add docs/
   git commit -m "Update documentation"
   git push origin main
   ```

3. **Automated deployment**:
   - GitHub Action will automatically deploy to Pages
   - Check https://bowenislandsong.github.io/SER/

### Manual Deployment (if needed)

The site is a static HTML site, so you can test it locally:

```bash
cd docs/
python -m http.server 8000
# Visit http://localhost:8000
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards compatible)
- **PATCH** version for backwards compatible bug fixes

Example: `0.1.0` → `0.2.0` (new feature) → `0.2.1` (bug fix) → `1.0.0` (stable API)

## Rollback

If a release has issues:

1. **PyPI**: You cannot delete releases, but you can yank them:
   ```bash
   twine upload --skip-existing dist/*  # Upload a fixed version
   ```

2. **Docker**: Delete the tag from GitHub Container Registry

3. **Git**: Create a new release with a patch version

## Troubleshooting

### PyPI Upload Fails
- Check that `PYPI_API_TOKEN` secret is set correctly
- Verify version number is not already used
- Check build logs in GitHub Actions

### Docker Build Fails
- Test the Dockerfile locally first
- Check that all dependencies are available
- Verify GitHub Container Registry permissions

### Conda Build Fails
- Ensure PyPI release is successful first
- Check SHA256 hash matches
- Review conda-forge feedstock CI logs

## Support

For issues with releases, open an issue on GitHub:
https://github.com/Bowenislandsong/SER/issues
