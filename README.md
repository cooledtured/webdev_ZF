
# Zealed Fujoshi 

Website for Zealed Fujoshi 

---


## Build and develop

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs to ./dist
npm run preview  # serves the built site locally
```

---

## Project layout

```
.
├── astro.config.mjs
├── package.json
├── tailwind.config.mjs
├── tsconfig.json
├── public/               # Static assets
└── src/
    ├── assets/            # Global images and media
    ├── components/       # UI Components
    │   ├── layout/       # Global architectural elements (Nav, Footer)
    │   └── features/     # Feature-specific modules (Hero, Marquee)
    ├── content/          # Content Collections
    │   └── config.ts     # Schema for press/posts
    ├── layouts/          # Page wrappers (BaseLayout, PostLayout)
    ├── pages/            # File-based routing
    │   ├── index.astro    # Homepage
    │   ├── contact.astro # Contact page
    │   ├── podcasts/      # Podcast index and dynamic pages
    │   └── posts/        # Paginated blog index and dynamic pages
    ├── styles/           # Global CSS & Themes
    └── utils/            # Shared utilities (URL resolution)
```

---


