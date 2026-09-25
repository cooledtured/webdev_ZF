import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  trailingSlash: "ignore",

  integrations: [react(), tailwind()],

  vite: {
    ssr: {
      noExternal: ["lucide-react", "framer-motion", "gsap"],
    },
    build: {
      cssCodeSplit: false,
    },
  },

  build: {
    format: "directory",
    inlineStylesheets: "always",
  },
});