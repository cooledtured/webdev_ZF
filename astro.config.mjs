import { defineConfig } from "astro/config";

import react from "@astrojs/react";

import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  site: "https://zealedfujoshi.xyz",
  trailingSlash: "ignore",

  integrations: [react(), tailwind()],

  vite: {
    ssr: {
      noExternal: ["lucide-react"],
    },
    build: {
      // Prevents micro-chunking that creates deep import dependency trees
      cssCodeSplit: false,
      rollupOptions: {
        output: {
          // Flatten module structure into cohesive bundles
          manualChunks(id) {
            if (
              id.includes("node_modules/react") ||
              id.includes("node_modules/react-dom")
            ) {
              return "vendor-react";
            }
            if (id.includes("node_modules/framer-motion")) {
              return "vendor-motion";
            }
          },
        },
      },
    },
  },

  build: {
    format: "file",

    inlineStylesheets: "always",
  },

  integrations: [react(), tailwind()],
});
