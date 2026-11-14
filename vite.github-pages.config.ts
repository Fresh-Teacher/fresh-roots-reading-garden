// External hosting only; the normal Lovable runtime remains unchanged.
import { defineConfig } from '@lovable.dev/vite-tanstack-config';
import { githubPagesPaths } from './scripts/github-pages-config';

export default defineConfig({
  nitro: false,
  tanstackStart: {
    server: { entry: 'server' },
    pages: githubPagesPaths().map(path => ({ path })),
    prerender: { enabled: true, autoStaticPathsDiscovery: false, crawlLinks: false, failOnError: true, concurrency: 4 },
    spa: { enabled: true },
  },
});