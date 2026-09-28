# Puspamitra Mishra — Enterprise Solutions Architect

A responsive, static portfolio with four dedicated enterprise AI case studies. Designed for free GitHub Pages hosting. No framework, paid service, build dependency, or backend is needed to serve the site.

## Preview

Run `node scripts/preview.mjs` from this directory, then visit **http://127.0.0.1:4173**. You can also open `site/index.html` directly in a browser.

## Publish on GitHub Pages

This repository is published at **https://myprofile.puspamitramishra.fyi/**.
Pages must use **GitHub Actions**, not **Deploy from a branch**. Publishing the
repository root shows this README instead of the portfolio in `site/`.
The existing workflow uploads `site/` as the website root.

For future updates, commit and push to `main`; the workflow publishes automatically.
If you edit `scripts/build.py`, first run `python scripts/build.py` and commit the
generated HTML too. Check the repository's Actions tab for deployment status.

1. Create a **public** GitHub repository. Use `YOUR-USERNAME.github.io` for your main profile site, or any repository name for a project site.
2. Upload `site/`, `.github/`, `scripts/`, `.gitignore`, and this README. Preserve their directory structure. The original Word documents are not needed for hosting.
3. In the repository, open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Push to `main`, or run **Actions → Publish portfolio to GitHub Pages → Run workflow**.
5. The deployment publishes only the contents of `site/`. The resulting URL appears in **Settings → Pages** and the deployment run.

GitHub Free supports Pages from public repositories. Instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

If GitHub CLI authentication expires, run `gh auth login -h github.com` in your own terminal. Do not place access tokens in this repository.

## Edit the site

- **Profile and case-study copy:** edit `scripts/build.py`, then run `python scripts/build.py`. Commit the generated HTML under `site/`.
- **Design and responsive layout:** `site/styles.css`.
- **Mobile menu:** `site/script.js`.
- **Portrait, badges, downloadable profile, and photographs:** `site/assets/`.
- **Hosting:** `.github/workflows/pages.yml`.

The site uses relative links and works both at a domain root and under a repository path. Content is server-rendered static HTML and remains readable without JavaScript. Only the mobile menu uses JavaScript. Google Fonts are optional; local system font fallbacks are provided.

## Content notes

Profile and career details come from the supplied professional profile; AI project descriptions and metrics come from `Project_Highlights_Summary.docx`. No client identities have been inferred for the four AI projects. Career dates are preserved, including the overlapping 2017 roles. Conceptual workflow graphics illustrate the supplied descriptions rather than asserting implementation details not in the source. Confirm any changes to current-role dates and reported outcomes before future updates.

The downloadable profile is a designed, three-page PDF with a portrait, career summary, certification badges, education and credentials, and four illustrated AI project summaries with conceptual workflows. Both profile links download `Puspamitra-Mishra-Profile.pdf`. Contact details and credentials are drawn from the supplied professional profile; no additional licenses are asserted.

### Rebuild the downloadable profile

Install the optional authoring dependencies once: `python -m pip install -r scripts/requirements-pdf.txt`.
Run `python scripts/build-profile.py` to rebuild the website and PDF. It writes a review copy to `output/pdf/` and the publishable file to `site/assets/puspamitra-mishra-profile.pdf`. Commit the generated HTML and the asset PDF; hosting needs no Python packages. Project titles, metrics, and workflows are shared with `scripts/build.py`; the condensed career and project narrative copy is maintained in `scripts/build-profile.py`.

For PDF verification, install `pypdf` and `pymupdf`, then run `python scripts/check-profile.py`. It checks content, images, page count, and links, and renders all pages into `qa/pdf/` for visual review. With the preview server and optional Playwright dependency available, run `node scripts/check-profile-download.cjs` to verify both downloads at desktop and mobile widths.

## Photography

Locally stored illustrative photos from Unsplash, used under https://unsplash.com/license. They do not depict the actual project teams, clients, or deployments.

| Asset | Source |
| --- | --- |
| Clinical | https://images.unsplash.com/photo-1576091160399-112ba8d25d1d |
| Pharmaceuticals | https://images.unsplash.com/photo-1584308666744-24d5c474f2ae |
| Claims | https://images.unsplash.com/photo-1450101499163-c8848c66ca85 |
| Mortgage | https://images.unsplash.com/photo-1560518883-ce09059eeffa |

Your portrait and certification badge files are reproduced as supplied.

## Browser checks

With the preview server running, install the optional local QA dependency using `npm install --prefix .tools playwright`, then run `node scripts/check-site.cjs`. It uses installed Google Chrome to check all five pages at desktop and mobile widths, images, horizontal overflow, and navigation. Screenshots are saved under the ignored `qa/` folder.
