/**
 * Resolves local asset and page paths against Astro's configured BASE_URL.
 * Works seamlessly across local dev, GitHub Pages subpaths, and custom apex domains.
 */
export const getBaseUrl = (): string => {
  const base = import.meta.env.BASE_URL || "/";
  return base.endsWith("/") && base.length > 1 ? base.slice(0, -1) : base === "/" ? "" : base;
};

export const resolvePath = (path: string): string => {
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `${getBaseUrl()}${cleanPath}`;
};
