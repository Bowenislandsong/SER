# SER Documentation

This directory contains the GitHub Pages documentation for the SER project.

## Files

- **index.html**: Main documentation page with features, installation, quick start, API reference
- **SETUP.md**: Instructions for enabling GitHub Pages

## Viewing Locally

To preview the documentation locally:

```bash
cd docs/
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Live Site

Once GitHub Pages is enabled, the documentation will be available at:
**https://bowenislandsong.github.io/SER/**

## Updating Documentation

1. Edit `index.html` or add new HTML files
2. Test locally using the command above
3. Commit and push changes
4. GitHub Actions will automatically deploy updates

## Automatic Deployment

The `.github/workflows/github-pages.yml` workflow automatically deploys the docs to GitHub Pages on every push to the main branch.
