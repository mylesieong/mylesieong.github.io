# mylesieong.github.io

This is my personal website hosted on GitHub Pages. The site is built using static HTML and CSS for simplicity and ease of maintenance.

## Structure

- `index.html` - Homepage
- `products/` - Product pages and listings
- `case-studies/` - Case study pages
- `partners/` - Partnership pages
- `assets/` - CSS, images, and other static assets
- `README.md` - This file

## Preview

To preview this site locally, you have several options:

### Option 1: Open Directly in Browser (Simplest)

Simply open `index.html` in your web browser. This works for basic previewing, but using a local server (options below) is recommended because:
- It ensures all relative paths and assets load correctly
- It more closely mimics how the site works when deployed
- Some browser features work better over HTTP than file:// protocol

### Option 2: Python HTTP Server (Recommended)

```bash
# Python 3
python3 -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Then visit: `http://localhost:8000`

## Customization

Edit the HTML files to customize the content for your needs. The site uses custom CSS styling located in `assets/css/style.css`.

## Contact

- GitHub: [@mylesieong](https://github.com/mylesieong)
