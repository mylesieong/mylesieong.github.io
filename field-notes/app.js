/*
 * Vancouver Field Notes — renders every section from data.js.
 * No build step, no dependencies. Plain DOM APIs so it runs anywhere.
 */
(function () {
  "use strict";

  var DATA = window.FIELD_NOTES;
  if (!DATA) return;

  var PLACES = DATA.places;

  /* ── tiny DOM helpers ───────────────────────────────────────── */

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function list(items, className) {
    var ul = el("ul", className);
    items.forEach(function (item) {
      ul.appendChild(el("li", null, item));
    });
    return ul;
  }

  function mount(id) {
    return document.getElementById(id);
  }

  /* ── Stats ──────────────────────────────────────────────────── */

  function renderStats() {
    var visited = PLACES.filter(isVisited).length;
    var champions = PLACES.filter(hasAward).length;
    var wishCount = DATA.wishlist.reduce(function (sum, group) {
      return sum + group.items.length;
    }, 0);
    var neighborhoods = unique(
      PLACES.filter(isVisited).map(function (p) {
        return p.location;
      })
    ).length;

    var stats = [
      ["Places visited", visited],
      ["Champions", champions],
      ["Areas explored", neighborhoods],
      ["On the wishlist", wishCount],
    ];

    var target = mount("stats");
    stats.forEach(function (pair) {
      var wrap = el("div", "fn-stat");
      wrap.appendChild(el("dt", null, pair[0]));
      wrap.appendChild(el("dd", null, String(pair[1])));
      target.appendChild(wrap);
    });
  }

  function isVisited(p) {
    return p.status === "visited";
  }

  function hasAward(p) {
    return Boolean(p.award);
  }

  function unique(arr) {
    return arr.filter(function (v, i) {
      return arr.indexOf(v) === i;
    });
  }

  /* ── Legend ─────────────────────────────────────────────────── */

  function renderLegend() {
    var target = mount("legend");
    DATA.legend.forEach(function (entry) {
      target.appendChild(el("li", null, entry.symbol + " " + entry.label));
    });
  }

  /* ── Champions ──────────────────────────────────────────────── */

  function renderChampions() {
    var target = mount("champions-grid");

    PLACES.filter(hasAward).forEach(function (place) {
      var award = place.award;
      var card = el("article", "fn-champ");

      var head = el("p", "fn-champ-award");
      head.appendChild(el("span", null, award.emoji));
      head.appendChild(el("span", null, award.category || award.title));
      card.appendChild(head);

      card.appendChild(el("h3", null, award.title));
      card.appendChild(el("p", "fn-champ-place", place.name));

      var where = place.location;
      if (award.subject) where += " · " + award.subject;
      card.appendChild(el("p", "fn-champ-where", where));

      card.appendChild(el("p", "fn-champ-why", award.why));

      if (award.highlights && award.highlights.length) {
        card.appendChild(list(award.highlights, "fn-champ-highlights"));
      }

      var link = el("a", "fn-champ-link", "Read the full note →");
      link.href = "#place-" + place.id;
      link.addEventListener("click", function () {
        openPlace(place.id);
      });
      card.appendChild(link);

      target.appendChild(card);
    });
  }

  /* ── Timeline ───────────────────────────────────────────────── */

  function renderTimeline() {
    var target = mount("timeline-list");

    PLACES.filter(function (p) {
      return typeof p.step === "number";
    })
      .sort(function (a, b) {
        return a.step - b.step;
      })
      .forEach(function (place) {
        var item = el("li", "fn-tl-item");

        item.appendChild(
          el("span", "fn-tl-dot", pad(place.step))
        );

        var heading = el("h3");
        var link = el("a", null, place.name);
        link.href = "#place-" + place.id;
        link.addEventListener("click", function () {
          openPlace(place.id);
        });
        heading.appendChild(link);
        item.appendChild(heading);

        if (place.stepNote) {
          item.appendChild(el("p", "fn-tl-note", place.stepNote));
        }

        target.appendChild(item);
      });

    var end = el("li", "fn-tl-item fn-tl-end");
    end.appendChild(el("span", "fn-tl-dot", "…"));
    end.appendChild(el("p", null, "More discoveries continue…"));
    target.appendChild(end);
  }

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  /* ── Place cards ────────────────────────────────────────────── */

  var STATUS_SYMBOL = { visited: "🟢", wishlist: "🟡" };

  function renderPlaces() {
    var target = mount("notes-grid");

    PLACES.forEach(function (place) {
      var card = el("article", "fn-place");
      card.id = "place-" + place.id;
      card.dataset.kind = place.kind;
      card.dataset.award = String(hasAward(place));
      card.dataset.haystack = haystack(place);

      /* Left column: identity. */
      var main = el("div", "fn-place-main");

      var head = el("div", "fn-place-head");
      var status = el(
        "span",
        "fn-place-status",
        STATUS_SYMBOL[place.status] || ""
      );
      status.title = place.status === "visited" ? "Visited" : "Wishlist";
      head.appendChild(status);
      head.appendChild(el("h3", null, place.name));
      main.appendChild(head);

      var meta = el("div", "fn-place-meta");
      if (place.location) meta.appendChild(el("span", null, place.location));
      if (place.category) meta.appendChild(el("span", null, place.category));
      main.appendChild(meta);

      if (place.award) {
        main.appendChild(
          el(
            "div",
            "fn-place-badge",
            place.award.emoji + "  " + place.award.title
          )
        );
      }

      card.appendChild(main);

      /* Right column: what we thought. */
      var body = el("div", "fn-place-body");

      if (place.impression) {
        body.appendChild(el("p", "fn-impression", place.impression));
      }

      if (place.tags && place.tags.length) {
        var tags = el("div", "fn-tags");
        place.tags.forEach(function (tag) {
          tags.appendChild(el("span", "fn-tag", tag));
        });
        body.appendChild(tags);
      }

      if (place.sections && place.sections.length) {
        body.appendChild(renderSections(place.sections));
      }

      card.appendChild(body);

      target.appendChild(card);
    });
  }

  function renderSections(sections) {
    var details = el("details", "fn-details");
    details.appendChild(el("summary", null, "Read the notes"));

    sections.forEach(function (section) {
      var wrap = el("div", "fn-note-section");
      wrap.appendChild(el("h4", null, section.h));

      section.blocks.forEach(function (block) {
        if (block.p) {
          wrap.appendChild(el("p", null, block.p));
        } else if (block.label) {
          wrap.appendChild(el("p", "fn-note-label", block.label));
        } else if (block.note) {
          wrap.appendChild(el("p", "fn-note-aside", block.note));
        } else if (block.ul) {
          wrap.appendChild(list(block.ul));
        } else if (block.link) {
          var p = el("p");
          var a = el("a", null, block.link.text);
          a.href = block.link.href;
          p.appendChild(a);
          wrap.appendChild(p);
        }
      });

      details.appendChild(wrap);
    });

    return details;
  }

  /* Flattened searchable text for each place. */
  function haystack(place) {
    var parts = [place.name, place.location, place.category, place.impression];

    (place.tags || []).forEach(function (t) {
      parts.push(t);
    });

    if (place.award) {
      parts.push(place.award.title, place.award.why);
      (place.award.highlights || []).forEach(function (h) {
        parts.push(h);
      });
    }

    (place.sections || []).forEach(function (section) {
      parts.push(section.h);
      section.blocks.forEach(function (block) {
        if (block.p) parts.push(block.p);
        if (block.label) parts.push(block.label);
        if (block.note) parts.push(block.note);
        if (block.ul) parts.push(block.ul.join(" "));
      });
    });

    return parts
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
  }

  /* ── Filtering ──────────────────────────────────────────────── */

  var FILTERS = [
    { id: "all", label: "All places" },
    { id: "coffee", label: "☕ Coffee" },
    { id: "drinks", label: "🍺 Bars & Breweries" },
    { id: "champions", label: "🏆 Champions" },
  ];

  var activeFilter = "all";

  function renderFilters() {
    var target = mount("filters");

    FILTERS.forEach(function (filter) {
      var btn = el("button", "fn-chip", filter.label);
      btn.type = "button";
      btn.dataset.filter = filter.id;
      btn.setAttribute("aria-pressed", String(filter.id === activeFilter));

      btn.addEventListener("click", function () {
        activeFilter = filter.id;
        target.querySelectorAll(".fn-chip").forEach(function (chip) {
          chip.setAttribute(
            "aria-pressed",
            String(chip.dataset.filter === activeFilter)
          );
        });
        applyFilters();
      });

      target.appendChild(btn);
    });
  }

  function matchesFilter(card) {
    if (activeFilter === "all") return true;
    if (activeFilter === "champions") return card.dataset.award === "true";
    return card.dataset.kind === activeFilter;
  }

  function applyFilters() {
    var query = (mount("search").value || "").trim().toLowerCase();
    var cards = document.querySelectorAll(".fn-place");
    var shown = 0;

    cards.forEach(function (card) {
      var visible =
        matchesFilter(card) &&
        (!query || card.dataset.haystack.indexOf(query) !== -1);
      card.hidden = !visible;
      if (visible) shown += 1;
    });

    mount("notes-empty").hidden = shown !== 0;
    mount("result-count").textContent =
      shown === cards.length
        ? shown + " places"
        : "Showing " + shown + " of " + cards.length + " places";
  }

  /* ── Neighborhoods ──────────────────────────────────────────── */

  function renderNeighborhoods() {
    var hood = DATA.neighborhoods;
    mount("hood-intro").textContent = hood.intro;
    mount("hood-outro").textContent = hood.outro;

    var target = mount("hood-grid");
    hood.columns.forEach(function (column) {
      var card = el("article", "fn-hood");
      card.appendChild(el("span", "fn-hood-emoji", column.emoji));
      card.appendChild(el("h3", null, column.name));
      card.appendChild(list(column.traits));
      target.appendChild(card);
    });
  }

  /* ── Wishlist ───────────────────────────────────────────────── */

  function renderWishlist() {
    var target = mount("wishlist-groups");

    DATA.wishlist.forEach(function (group) {
      var section = el("div", "fn-wish-group");
      section.appendChild(
        el("h3", null, group.emoji + "  " + group.group)
      );

      var grid = el("div", "fn-wish-grid");
      group.items.forEach(function (item) {
        var card = el("article", "fn-wish");
        card.appendChild(el("h4", null, item.name));
        if (item.note) card.appendChild(el("p", "fn-wish-note", item.note));

        if (item.tags && item.tags.length) {
          var tags = el("div", "fn-tags");
          item.tags.forEach(function (tag) {
            tags.appendChild(el("span", "fn-tag", tag));
          });
          card.appendChild(tags);
        }

        grid.appendChild(card);
      });

      section.appendChild(grid);
      target.appendChild(section);
    });
  }

  /* ── Future features ────────────────────────────────────────── */

  function renderFuture() {
    var target = mount("future-grid");

    DATA.future.forEach(function (entry) {
      var card = el("article", "fn-future");
      card.appendChild(el("h3", null, entry.title));
      card.appendChild(el("p", null, entry.body));

      if (entry.examples && entry.examples.length) {
        var tags = el("div", "fn-tags");
        entry.examples.forEach(function (example) {
          tags.appendChild(el("span", "fn-tag", example));
        });
        card.appendChild(tags);
      }

      target.appendChild(card);
    });
  }

  /* ── Cross-links: reset filters so the target is always visible ── */

  function openPlace(id) {
    activeFilter = "all";
    mount("search").value = "";
    document.querySelectorAll("#filters .fn-chip").forEach(function (chip) {
      chip.setAttribute("aria-pressed", String(chip.dataset.filter === "all"));
    });
    applyFilters();

    var card = document.getElementById("place-" + id);
    if (!card) return;
    var details = card.querySelector(".fn-details");
    if (details) details.open = true;
  }

  /* ── Init ───────────────────────────────────────────────────── */

  renderStats();
  renderLegend();
  renderChampions();
  renderTimeline();
  renderFilters();
  renderPlaces();
  renderNeighborhoods();
  renderWishlist();
  renderFuture();
  applyFilters();

  mount("search").addEventListener("input", applyFilters);

  /* Deep link support: /field-notes/#place-nemesis */
  if (location.hash.indexOf("#place-") === 0) {
    openPlace(location.hash.slice("#place-".length));
  }
})();
