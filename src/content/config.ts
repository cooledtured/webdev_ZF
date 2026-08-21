import { defineCollection, z } from 'astro:content';

const postsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    category: z.enum(['REVIEWS', 'INTERVIEWS', 'PODCAST']),
    summary: z.string(),
  }),
});

export const collections = {
  posts: postsCollection,
};
