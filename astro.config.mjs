import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://zealedfujoshi.xyz',
  trailingSlash: 'ignore',
  build: {
    format: 'file',
  },
});
