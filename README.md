# Zealed Fujoshi 

Built with Astro!

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
├── tsconfig.json
└── src/
    ├── components/
    │   ├── Navigation.astro
    │   ├── PopularPosts.astro
    │   ├── SidebarAds.astro
    │   ├── SiteHeader.astro
    ├── content/
    │   ├── config.ts          # schema for posts
    │   └── posts/             # drop .md files here
    │       ├── example.md     # an example markdown file
    ├── layouts/
    │   └── BaseLayout.astro   # shell
    └── pages/
        ├── index.astro        # homepage feed
        └── posts/
            └── [...slug].astro # dynamic post pages
```

---
