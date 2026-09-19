## 🛠 Development Setup

1. **Fork the repository** and create your branch from `main`.
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Build and Run**:
   ```bash
   npm run build
   npm run preview
   ```

## 🎨 Design Guidelines

The project uses a **Glassmorphic Design System**. When adding new components:
- **Translucency**: Use `backdrop-blur` and semi-transparent backgrounds (e.g., `bg-white/10`).
- **Borders**: Use thin, light borders (`border-white/10`) to define edges.
- **Colors**: Stick to the defined Tailwind theme (e.g., `text-porcelain`, `text-razzmatazz`).
- **Animations**: Prefer GSAP for complex timelines and Framer Motion for simple interactive transitions.

## Architecture

- **Component Tiering**:
  - `src/components/layout/`: For global elements used across most pages (Navigation, Footer).
  - `src/components/features/`: For complex, standalone feature modules (Hero, VideoSpotlight).
- **URL Resolution**: Always use the `resolvePath` utility from `src/utils/url.ts` for paths that need to be relative to the base deployment URL.

## 🚀 Submission Process

1. **Lint & Build**: Ensure your changes don't break the build:
   ```bash
   npm run build
   ```
2. **Pull Request**: Open a PR with a clear description of the changes.
3. **Review**: Be prepared to iterate on the visual polish during the review process.





