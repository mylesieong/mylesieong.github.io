# Vancouver Field Notes

A sub-page of mylesieong.github.io. Plain HTML/CSS/JS — no build step, no
dependencies, works as-is on GitHub Pages.

| File | Role |
| --- | --- |
| `index.html` | Page shell and the prose sections (hero, philosophy) |
| `styles.css` | All styling, light + dark theme |
| `data.js` | **All content.** The single source of truth |
| `app.js` | Renders every section from `data.js` |

## Adding a place

Append an object to `window.FIELD_NOTES.places` in `data.js`. Everything else
updates automatically: the counts in the hero, the champions grid, the timeline,
the filters, and the search index.

```js
{
  id: "prototype",              // unique; used for the #place-prototype anchor
  name: "Prototype Coffee",
  location: "Chinatown",
  category: "Specialty Coffee",
  kind: "coffee",               // "coffee" | "drinks" — drives the filter chips
  status: "visited",            // "visited" | "wishlist"

  // Optional: puts it on the timeline at this position.
  step: 6,
  stepNote: "One line on what this stop taught us.",

  // Optional: promotes it to the Current Champions grid.
  award: {
    emoji: "🧪",
    category: "Most Experimental",   // plain label, shown small above the title
    title: "The One That Surprised Us", // the award name itself
    subject: "Kenya AA",             // optional — a specific drink
    why: "One sentence on why it holds the title.",
    highlights: ["Point one", "Point two"]
  },

  sections: [
    {
      h: "Coffee Notes",
      blocks: [
        { p: "A paragraph." },
        { label: "A small bold sub-heading" },
        { ul: ["Bullet one", "Bullet two"] },
        { note: "A highlighted aside — good for surprises or corrections." },
        { link: { href: "#neighborhoods", text: "Cross-reference" } }
      ]
    }
  ],

  impression: "The pull-quote shown on the collapsed card.",
  tags: ["🧪 Experimental", "☕ Specialty"]
}
```

Only `id`, `name`, and `status` are strictly required. Omit any optional field
and its UI simply doesn't render.

## Changing a champion

Move the `award` object from one place to another, or delete it to retire a
title. The champions grid and the hero count are both derived, so nothing else
needs editing. The grid is laid out for four — adding a fifth still works, it
just wraps.

## Wishlist, neighborhoods, future features

Edit `wishlist`, `neighborhoods`, and `future` in `data.js` — same idea.

## Preview locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000/field-notes/
```
