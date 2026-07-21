/*
 * Vancouver Field Notes — content source of truth.
 *
 * Everything on the page (champions, timeline, cards, filters, counts) is
 * derived from this file. To add a place, append an object to PLACES.
 * See README.md in this folder for the field reference.
 */

window.FIELD_NOTES = {
  meta: {
    title: "Vancouver Field Notes",
    authors: "Sai × Jay",
    tagline:
      "Two friends exploring Vancouver through coffee, food, drinks, and neighborhoods.",
  },

  /* Legend used by the map/status chips. */
  legend: [
    { symbol: "🟢", label: "Visited" },
    { symbol: "🟡", label: "Wishlist" },
    { symbol: "🏆", label: "Current Champion" },
  ],

  places: [
    {
      id: "small-factory",
      name: "Small Factory",
      location: "South Granville",
      category: "Coffee Shop",
      kind: "coffee",
      status: "visited",
      step: 1,
      stepNote: "The beginning of the journey.",
      sections: [
        {
          h: "Why We Went",
          blocks: [{ p: "The first café we explored together." }],
        },
        {
          h: "Experience",
          blocks: [
            { p: "A large café with plenty of seating." },
            { ul: ["Clean", "Spacious", "Comfortable"] },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { p: "The coffee was standard." },
            { p: "Nothing particularly memorable about the coffee itself." },
          ],
        },
        {
          h: "Food Notes",
          blocks: [{ ul: ["Coffee", "Pistachio savory snack"] }],
        },
      ],
      impression:
        "Not remembered for the coffee, but important because it was the starting point of our café exploration journey.",
      tags: ["🚩 First Stop", "🌱 Beginning of Exploration"],
    },

    {
      id: "bean-around-the-world",
      name: "Bean Around the World",
      location: "South Granville",
      category: "Coffee Shop",
      kind: "coffee",
      status: "visited",
      step: 2,
      stepNote: "Discovering what balanced coffee feels like.",
      award: {
        emoji: "⚖️",
        category: "Most Drinkable",
        title: "The Everyday Cup",
        why: "The coffee was excellent. Not necessarily the most unusual coffee, but one of the best balanced cups.",
        highlights: ["Balanced", "Easy to drink", "Consistently enjoyable"],
      },
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "A small café." },
            { p: "We sat next to the window." },
            { p: "It was a very hot day." },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { p: "Both of us agreed: the coffee was excellent." },
            { ul: ["Balanced", "Drinkable", "One of the best coffees we had"] },
          ],
        },
      ],
      impression: "A coffee that does not need to be unusual to be excellent.",
      tags: ["⚖️ Most Drinkable", "☕ Balanced Coffee"],
    },

    {
      id: "nemesis",
      name: "Nemesis Coffee",
      location: "Outside Emily Carr University",
      category: "Specialty Coffee",
      kind: "coffee",
      status: "visited",
      step: 3,
      stepNote: "Finding exceptional specialty coffee.",
      award: {
        emoji: "☕",
        category: "Best Coffee Overall",
        title: "The Best Cup in the City",
        why: "The best coffee we had around the past month.",
        highlights: [
          "Very balanced",
          "Very drinkable",
          "Multiple tasting profiles",
          "Complex but still enjoyable",
        ],
      },
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "The place was stunning." },
            { p: "The environment felt carefully designed." },
            {
              note: "You even need a reservation to sit at some tables.",
            },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { p: "In Sai's opinion: the best coffee we had around the past month." },
            {
              ul: [
                "Very balanced",
                "Very drinkable",
                "Many different tasting profiles",
                "Complex but enjoyable",
              ],
            },
          ],
        },
      ],
      impression:
        "A complete experience: great coffee, beautiful space, strong attention to detail.",
      tags: ["🏆 Best Coffee", "🍓 Complex Flavor", "🎨 Beautiful Space"],
    },

    {
      id: "49th-parallel",
      name: "49th Parallel",
      location: "Kitsilano",
      category: "Coffee Shop",
      kind: "coffee",
      status: "visited",
      step: 4,
      stepNote: "Realizing atmosphere matters as much as coffee.",
      award: {
        emoji: "👀",
        category: "Best People Watching",
        title: "The Best Seat in the House",
        why: "The environment was part of the experience.",
        highlights: [
          "Outdoor seating",
          "Busy neighborhood feeling",
          "Interesting people passing by",
        ],
      },
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "We sat outside. The view was excellent." },
            { p: "The atmosphere was a big part of the experience." },
            { label: "Compared with quieter cafés" },
            {
              ul: [
                "More street activity",
                "More people passing by",
                "More things happening around us",
              ],
            },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { p: "The coffee was good. However:" },
            {
              ul: [
                "Flavor was a little too strong",
                "Sai personally added water to make it more balanced",
              ],
            },
          ],
        },
      ],
      impression:
        "The coffee was good, but the overall experience was elevated by the environment.",
      tags: ["👀 People Watching", "🌞 Outdoor Café", "🚶 Street Atmosphere"],
    },

    {
      id: "elysian",
      name: "Elysian",
      location: "Kitsilano",
      category: "Coffee Shop",
      kind: "coffee",
      status: "visited",
      step: 5,
      stepNote: "Exploring different flavor profiles.",
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "A smaller café. We sat outside." },
            {
              note: "The downside: the location was not on a busy main street.",
            },
            { label: "Compared with 49th Parallel" },
            { ul: ["Less street activity", "Less to watch around us"] },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { label: "Ethiopia Blend — Sai" },
            { p: "When hot:" },
            { ul: ["Peach flavor", "Fruity", "Enjoyable"] },
            { p: "When colder:" },
            { ul: ["Too sour", "Less balanced"] },
            {
              p: "Overall: the coffee had interesting characteristics, but the drinkability was not as high.",
            },
          ],
        },
      ],
      impression: "Interesting coffee, but not an easy everyday cup.",
      tags: ["🍑 Interesting Flavor", "⚖️ Balance Challenge"],
    },

    {
      id: "turks",
      name: "Turks Coffee",
      location: "Commercial Drive",
      category: "Coffee Shop",
      kind: "coffee",
      status: "visited",
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "A café with strong personality." },
            {
              ul: [
                "Outdoor patio",
                "Large working table",
                "Artwork",
                "Decorations",
                "Unique style",
              ],
            },
            { p: "Sai personally loved the atmosphere." },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { p: "We ordered drip coffee. Dark roast." },
            { label: "Sai's impression" },
            {
              ul: [
                "Strong roasted flavor",
                "Nutty flavor",
                "Strong taste but not heavy body",
              ],
            },
            {
              note: "Initially the burnt flavor seemed like a mistake. Later we realized it was an intentional roasted flavor profile.",
            },
          ],
        },
        {
          h: "Jay's Opinion",
          blocks: [{ p: "Jay did not enjoy the coffee as much." }],
        },
      ],
      impression: "A café where personality matters as much as coffee.",
      tags: ["🌰 Best Dark Roast", "🎨 Unique Atmosphere"],
    },

    {
      id: "cafe-calabria",
      name: "Cafe Calabria",
      location: "Commercial Drive",
      category: "Italian-style Café",
      kind: "coffee",
      status: "visited",
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "A very unique place." },
            { label: "Inside" },
            { ul: ["Very dark", "Strong personality"] },
            {
              p: "Although Italian-style, the feeling was closer to a Greek-style café.",
            },
            { p: "We sat outside." },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [{ ul: ["Sai — Long Black", "Jay — Espresso"] }],
        },
        {
          h: "Neighborhood Notes",
          blocks: [
            {
              p: "Commercial Drive and Kitsilano are both enjoyable but very different.",
            },
            { link: { href: "#neighborhoods", text: "Read the comparison" } },
          ],
        },
      ],
      tags: ["🚶 Best Street Experience", "🌆 Neighborhood Character"],
    },

    {
      id: "pallet",
      name: "Pallet Coffee",
      location: "Oak Street",
      category: "Coffee Shop",
      kind: "coffee",
      status: "visited",
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "A quiet neighborhood café." },
            { label: "The street itself" },
            { ul: ["Busy road", "Not much pedestrian activity"] },
            { p: "But the surrounding neighborhood was beautiful. Driving around:" },
            { ul: ["Green trees", "Beautiful homes", "Decorated yards"] },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { p: "The coffee was good." },
            { p: "Jay likes it a lot and often mentions it. Sai also enjoyed it." },
            { label: "Signature" },
            { ul: ["Roasted flavor", "Sometimes strong burnt flavor"] },
            {
              note: "At first we thought it was a mistake. Later we realized it was intentional dark roasting.",
            },
          ],
        },
      ],
      impression: "Very good drinkability.",
      tags: ["🌳 Best Neighborhood Experience", "⚖️ Reliable Coffee"],
    },

    {
      id: "wicked",
      name: "Wicked Café",
      location: "Fairview",
      category: "Coffee Shop",
      kind: "coffee",
      status: "visited",
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "A very warm café." },
            {
              ul: [
                "Cozy decoration",
                "Family-like feeling",
                "Comfortable atmosphere",
              ],
            },
          ],
        },
        {
          h: "Coffee Notes",
          blocks: [
            { p: "The coffee was regular. Nothing special." },
            { p: "But the place itself was memorable." },
          ],
        },
      ],
      impression:
        "Some cafés are remembered because of atmosphere, not coffee.",
      tags: ["🏡 Coziest Café", "🏡 Warm Atmosphere"],
    },

    {
      id: "batch",
      name: "Batch",
      location: "Kitsilano",
      category: "Bar",
      kind: "drinks",
      status: "visited",
      award: {
        emoji: "🌊",
        category: "Best Atmosphere",
        title: "The Afternoon We Remember",
        why: "The view and atmosphere created a memorable afternoon.",
        highlights: [
          "Great view",
          "Outdoor seating",
          "Summer feeling",
          "People watching",
        ],
      },
      sections: [
        {
          h: "Experience",
          blocks: [
            { p: "Located next to Kitsilano Pool." },
            { ul: ["Great view", "Outdoor seating", "Beautiful day"] },
          ],
        },
        {
          h: "Food & Drinks",
          blocks: [{ ul: ["Beer", "Fries"] }],
        },
        {
          h: "The Moment",
          blocks: [
            { p: "We sat next to a group of girls." },
            { p: "We tried guessing where they were from." },
            {
              p: "We guessed places like Colombia because one person looked very exotic.",
            },
            { p: "Turns out: she was from Iran." },
            {
              note: "The funny part — Jay is from Iran and he could not recognize it.",
            },
          ],
        },
      ],
      impression:
        "A memorable place because of the moment, atmosphere, and people around us.",
      tags: ["🌊 Best View", "🍺 Summer Afternoon", "💬 Memorable Moment"],
    },

    {
      id: "stanley-park-brewery",
      name: "Stanley Park Brewery",
      location: "Stanley Park",
      category: "Brewery",
      kind: "drinks",
      status: "visited",
      sections: [
        {
          h: "Experience",
          blocks: [{ p: "We tried a beer flight." }],
        },
        {
          h: "Beer Notes",
          blocks: [
            { p: "The highlight: their signature beer." },
            { p: "A wheat beer with:" },
            { ul: ["Peach flavor", "Fruity character", "Refreshing profile"] },
            { p: "Both of us were impressed." },
          ],
        },
      ],
      impression: "A good place for exploring beer styles.",
      tags: ["🍺 Beer Discovery", "🍑 Peach Beer"],
    },
  ],

  /* Pulled out of the Cafe Calabria entry — it stands on its own. */
  neighborhoods: {
    intro:
      "Two neighborhoods, two completely different ways of spending an afternoon.",
    columns: [
      {
        name: "Commercial Drive",
        emoji: "🌆",
        traits: ["More vivid", "More lively", "More diverse", "More unexpected"],
      },
      {
        name: "Kitsilano",
        emoji: "🌊",
        traits: ["More polished", "Beach lifestyle", "People dressing nicely"],
      },
    ],
    outro: "Both neighborhoods are enjoyable but very different.",
  },

  wishlist: [
    {
      group: "Coffee",
      emoji: "☕",
      items: [
        {
          name: "Prototype Coffee",
          note: "Potential challenge: can it compete with Nemesis?",
          tags: ["Best Specialty Coffee", "Most Experimental"],
        },
        {
          name: "Revolver",
          note: "A coffee comparison experience.",
          tags: ["Best Coffee Selection", "Best Comparison Experience"],
        },
        {
          name: "Timbertrain",
          note: "Coffee + Gastown atmosphere.",
          tags: ["Best Neighborhood Coffee", "Best Café Design"],
        },
        {
          name: "Modus",
          note: "Specialty coffee in Mount Pleasant.",
          tags: ["Hidden Gem", "Balanced Specialty Coffee"],
        },
        {
          name: "Analog Coffee",
          note: "Potential comparison: Nemesis, Bean Around the World, 49th Parallel.",
          tags: [],
        },
        { name: "Trees Organic", note: "", tags: ["Classic Vancouver Coffee"] },
        {
          name: "JJ Bean",
          note: "",
          tags: ["Everyday Champion", "Vancouver Classic"],
        },
        { name: "Guffo Café", note: "", tags: ["Cozy Café", "Coffee + Pastry"] },
        {
          name: "Breka",
          note: "",
          tags: ["Late Night Café", "Bakery Experience"],
        },
      ],
    },
    {
      group: "Food & Drinks",
      emoji: "🍽️",
      items: [
        {
          name: "Social",
          note: "Second-floor patio. Summer lunch destination.",
          tags: [],
        },
        {
          name: "Blaze Gourmet Burgers",
          note: "Mission: find Vancouver's memorable burger.",
          tags: ["Best Burger"],
        },
        {
          name: "The Peri Peri Shack",
          note: "Mission: explore peri-peri chicken.",
          tags: [],
        },
        {
          name: "House of Dosas",
          note: "Kingsway. Mission: explore South Indian food.",
          tags: [],
        },
        {
          name: "Chinese Restaurants",
          note: "A future category rather than a single place.",
          tags: ["Best Dumplings", "Best Noodles", "Best Wok Hei", "Hidden Gem"],
        },
      ],
    },
  ],

  future: [
    {
      title: "Places We Return To",
      body: "For places visited multiple times.",
    },
    {
      title: "Personal Awards",
      body: "Not ratings. Only memorable categories.",
      examples: [
        "Best Coffee",
        "Most Drinkable",
        "Most Interesting Flavor",
        "Best View",
        "Best Neighborhood",
        "Coziest Café",
        "Best Street Atmosphere",
        "Best Conversation Spot",
        "Hidden Gem",
      ],
    },
  ],
};
