# Personal Website

A minimal, brutalist-style personal website built with Hugo and deployed to GitHub Pages
at **[maxdavy.com](https://maxdavy.com/)**.

The old address, `daxmavy.github.io`, now serves only a redirect stub (see the
`daxmavy/daxmavy.github.io` repository).

## Features

- 🎨 Minimal brutalist design with clean typography
- 📝 Blog with markdown support
- 📚 Footnotes with hover preview
- 📖 Bibliography and citation system
- 📧 Newsletter subscription (Buttondown)
- 🚀 Automatic deployment via GitHub Actions

## Local Development

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (v0.155.3 or later)

### Running Locally

```bash
# Clone the repository
git clone https://github.com/daxmavy/maxdavy.com.git
cd maxdavy.com

# Start the Hugo development server
hugo server -D

# Visit http://localhost:1313
```

## Content Management

### Creating a New Blog Post

```bash
# Create a new post using the archetype template
hugo new blog/posts/my-new-post.md

# Edit the file in content/blog/posts/my-new-post.md
# Set draft: false when ready to publish
# Commit and push to deploy
```

### Using Footnotes

```markdown
This is text with a footnote.[^1]

[^1]: This is the footnote content.
```

Footnotes will automatically show in a popup when you hover over them!

### Using Citations

Add citations to your bibliography in `data/bibliography.json`:

```json
{
  "author2025": {
    "author": "Author Name",
    "year": "2025",
    "title": "Paper Title",
    "journal": "Journal Name",
    "doi": "10.1234/example"
  }
}
```

Then cite in your posts:

```markdown
As noted by {{< cite "author2025" >}}, or with a page: {{< cite "author2025" "p. 45" >}}.

At the end of your post:

{{< bibliography >}}
```

## Deployment

The site automatically deploys to GitHub Pages when you push to the `main` branch.

### How the custom domain is wired

- `static/CNAME` claims `maxdavy.com` for this repository.
- Pages source is set to **GitHub Actions**; `.github/workflows/deploy.yml` builds
  with Hugo and deploys on every push to `main`.
- DNS lives in Cloudflare: apex `A`/`AAAA` records for `maxdavy.com` point at the
  GitHub Pages anycast addresses, and `www` is a `CNAME` to `daxmavy.github.io`.
  Manage them with `~/.claude/skills/maxdavy-site/scripts/maxdavy.sh dns list`.

## Configuration

Edit `hugo.toml` to customize:

- `baseURL`: Your site URL
- `title`: Your site title
- `params.author`: Your name
- `params.description`: Site description

### Newsletter Setup

1. Sign up at [Buttondown](https://buttondown.email)
2. Get your username
3. Edit `layouts/partials/newsletter.html`
4. Replace `[your-username]` with your Buttondown username

## File Structure

```
.
├── .github/workflows/    # GitHub Actions deployment
├── archetypes/          # Content templates
├── content/             # All site content (markdown)
│   ├── bio/
│   ├── blog/            # kept, but deliberately unlinked from the main nav
│   ├── maximalism/
│   └── research/
├── data/                # Bibliography and data files
├── layouts/             # HTML templates
│   ├── _default/
│   ├── partials/
│   └── shortcodes/
├── static/              # Static files (CSS, JS)
│   ├── css/
│   └── js/
└── hugo.toml            # Hugo configuration
```

## Customization

### Design

Edit `static/css/style.css` to customize the brutalist design. The design principles:

- System fonts (Georgia for body, Courier for code)
- Black and white color scheme
- Clean borders and simple shapes
- Maximum readability

### Content

- **Homepage**: `content/_index.md`
- **Bio**: `content/bio/index.md`
- **Research**: `content/research/index.md`
- **Blog posts**: `content/blog/posts/`

### Two deliberate bits of hiding

- **The blog is unlisted.** It still builds and lives at `/blog/`, but the only
  link to it is a small one in the site footer — it is not in the header nav.
- **The homepage news block is off.** The `news:` entries are still in
  `content/_index.md`; set `show_news: true` there to render them again.

## License

[Your chosen license]

## Contact

[Your contact information]
