# GitHub Pages Setup Instructions

After merging this PR, follow these steps to enable GitHub Pages for your repository:

## Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/Bowenislandsong/SER
2. Click on **Settings** (top right)
3. Scroll down to the **Pages** section in the left sidebar
4. Under **Source**, select:
   - Source: **Deploy from a branch** (or **GitHub Actions** if you prefer)
   - If using branch: Select branch **main** and folder **/docs**
5. Click **Save**

## Step 2: Wait for Deployment

The first deployment may take a few minutes. You can check the progress:
1. Go to the **Actions** tab
2. Look for the "Deploy GitHub Pages" workflow
3. Wait for it to complete (green checkmark)

## Step 3: Verify Your Site

Once deployed, your site will be available at:
**https://bowenislandsong.github.io/SER/**

## Alternative: Use GitHub Actions Workflow (Recommended)

The repository already includes a GitHub Pages workflow (`.github/workflows/github-pages.yml`).

To use it:
1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow will automatically deploy on every push to main

This is the recommended approach as it's more flexible and automated.

## Troubleshooting

### Site not loading
- Check that the workflow completed successfully in the Actions tab
- Verify GitHub Pages is enabled in Settings
- Wait a few minutes for DNS propagation

### 404 Error
- Make sure the `docs/index.html` file exists in the main branch
- Check that the branch and folder are correctly configured

### Workflow fails
- Check the workflow logs in the Actions tab
- Ensure GitHub Pages permissions are enabled in repository settings
- Under Settings → Actions → General → Workflow permissions:
  - Select "Read and write permissions"
  - Check "Allow GitHub Actions to create and approve pull requests"

## Testing Locally

You can test the GitHub Pages site locally before deployment:

```bash
cd docs/
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Customizing the Site

The site is a static HTML page located at `docs/index.html`. To customize:
1. Edit `docs/index.html`
2. Commit and push changes
3. The workflow will automatically redeploy

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
