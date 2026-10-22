# How to open the portfolio as a real website

## Working alternatives that do not require Pages

**Read case studies directly in GitHub:** [Six readable Markdown case studies](../projects/CASE_STUDIES.md). These work now.

**Open the fully designed site locally:** From the [successful Actions workflow](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions), download the `cybersecurity-portfolio-site` artifact, extract its ZIP, and open `index.html` in your browser. The archive includes CSS, illustrations and case-study pages; it does **not** create a public website.

## Enable real online hosting

GitHub's **Code** view displays `.html` files as source code. To render the designed portfolio site at its public `github.io` address, GitHub Pages must be enabled separately. Passing the code-test GitHub Actions workflow does **not** enable Pages.

## One-time activation

1. Sign in to GitHub and open [Cybersecurity_Portfolio → Settings → Pages](https://github.com/IXI-2773/Cybersecurity_Portfolio/settings/pages).
2. Under **Build and deployment → Source**, select **Deploy from a branch**.
3. Select **main** and **/(root)**, then **Save**.
4. Check the Pages publishing/deployment status. If it fails, inspect the Pages workflow in the repository's Actions tab.

Once publishing succeeds, these are the rendered URLs:

- [Portfolio homepage](https://ixi-2773.github.io/Cybersecurity_Portfolio/)
- [Celestial Resonance — rendered case study](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/celestial-resonance.html)
- [Research AI Infrastructure — rendered case study](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/research-ai-infrastructure.html)
- [Vulnerability remediation — rendered case study](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/vulnerability-remediation.html)

These addresses may not work until Pages is enabled and successfully deployed.

**Do not use** `github.com/IXI-2773/Cybersecurity_Portfolio/blob/main/projects/celestial-resonance.html` to view the designed page: that URL is specifically GitHub's source-file viewer.

If you see a 404, check Pages Settings, deployment status, the `main` branch and `/(root)` directory. The root `index.html` and `.nojekyll` are already present. CR and RAI source code remains private; the public website contains only high-level case studies.
