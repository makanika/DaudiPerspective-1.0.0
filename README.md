# Daudi's Perspective Blog

A modern blog application built with Next.js 16, featuring a clean design with Lora and Lato fonts, warm color scheme, and responsive layout.

## Features

- **Modern Stack**: Built with Next.js 16, React 19, and TypeScript
- **Preserved Design**: Maintains warm color scheme with Lora and Lato fonts
- **Static Site Generation**: Optimized for performance and SEO
- **Dynamic Content**: Articles stored in JSON format for easy management
- **Individual Article Pages**: Each article has its own URL
- **Category Pages**: Browse articles by category
- **Responsive Design**: Works on all device sizes
- **SEO Friendly**: Proper meta tags and semantic HTML
- **Cloudflare Ready**: Configured for Cloudflare Pages deployment

## Project Structure

\`\`\`
daudis-perspective/
├── app/
│   ├── layout.tsx           # Root layout with fonts
│   ├── page.tsx             # Home page
│   ├── article/[id]/        # Individual article pages
│   └── category/[category]/ # Category pages
├── components/
│   ├── header.tsx           # Site header
│   └── ui/                  # shadcn/ui components
├── lib/
│   ├── articles.ts          # Article data functions
│   └── utils.ts             # Utility functions
├── data/
│   └── articles.json        # Article content and metadata
├── public/
│   └── images/              # Article images
├── next.config.mjs          # Next.js configuration
├── wrangler.toml            # Cloudflare configuration
└── CLOUDFLARE_DEPLOYMENT.md # Deployment guide
\`\`\`

## Quick Start

### Local Development

1. **Install Dependencies**
   \`\`\`bash
   # Using pnpm (recommended)
   pnpm install
   
   # Or using npm
   npm install
   \`\`\`

2. **Run Development Server**
   \`\`\`bash
   pnpm dev
   # or
   npm run dev
   \`\`\`

3. **Visit** http://localhost:3000

### Production Build

\`\`\`bash
# Build for production
pnpm build

# Preview production build
pnpm start
\`\`\`

## Deployment Options

### Option 1: Cloudflare Pages (Recommended)

Cloudflare Pages provides global CDN, automatic deployments, and unlimited bandwidth on the free tier.

**Quick Deploy:**
1. Push your code to GitHub
2. Connect repository to Cloudflare Pages
3. Configure build settings:
   - Build command: `pnpm build`
   - Build output: `out`
   - Framework: Next.js

See [CLOUDFLARE_DEPLOYMENT.md](./CLOUDFLARE_DEPLOYMENT.md) for detailed instructions.

### Option 2: Vercel

\`\`\`bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
\`\`\`

### Option 3: Traditional Hosting (Flask Version)

The repository also includes a Flask version for traditional server deployment.

See [DEPLOYMENT.md](./DEPLOYMENT.md) for Digital Ocean deployment instructions.

## Article Management

### Current Articles

1. **Networks**: "The Internet in Africa is Just a Connection to Europe"
2. **Automotive**: "The Soul of the Machine" 
3. **Aviation**: "The Simple Genius of the Turbofan"
4. **Linux**: "My Operating System is a Land Cruiser"
5. **Python**: "The Language That Speaks to Machines"
6. **Embedded**: "The Hidden Genius All Around Us"

### Adding New Articles

1. **Edit articles.json**
   \`\`\`bash
   # Open the data file
   nano data/articles.json
   \`\`\`

2. **Add Article Entry**
   \`\`\`json
   {
     "id": "unique-article-slug",
     "title": "Your Article Title",
     "category": "Engineering",
     "date": "January 30, 2025",
     "image": "article-image.jpg",
     "content": [
       "First paragraph of your article...",
       "Second paragraph...",
       "Continue with more paragraphs..."
     ]
   }
   \`\`\`

3. **Add Article Image**
   \`\`\`bash
   # Add image to public/images/
   cp ~/Downloads/article-image.jpg public/images/
   \`\`\`

4. **Deploy Changes**
   
   **For Cloudflare Pages:**
   \`\`\`bash
   git add data/articles.json public/images/article-image.jpg
   git commit -m "Add new article: Your Article Title"
   git push origin main
   # Automatic deployment in 2-5 minutes
   \`\`\`
   
   **For local testing:**
   \`\`\`bash
   pnpm dev
   # Visit http://localhost:3000
   \`\`\`

### Article JSON Format

\`\`\`json
{
  "articles": [
    {
      "id": "unique-slug",
      "title": "Article Title",
      "category": "Category Name",
      "date": "Month Day, Year",
      "image": "image-filename.jpg",
      "content": [
        "Paragraph 1...",
        "Paragraph 2...",
        "Paragraph 3..."
      ]
    }
  ]
}
\`\`\`

## Image Management

### Image Guidelines

- **Size**: 1200x600 pixels (2:1 aspect ratio)
- **Format**: JPEG or WebP
- **Quality**: 80-90% for optimal balance
- **Location**: `public/images/`
- **Naming**: Use descriptive kebab-case names

### Finding Images

Free stock photo sources:
- [Unsplash](https://unsplash.com) - High-quality free images
- [Pexels](https://pexels.com) - Free stock photos
- [Pixabay](https://pixabay.com) - Free images and videos

### Optimizing Images

\`\`\`bash
# Using ImageMagick
convert original.jpg -resize 1200x600^ -gravity center -extent 1200x600 -quality 85 optimized.jpg

# Using sharp (Node.js)
npx sharp-cli resize 1200 600 --fit cover --quality 85 input.jpg -o output.jpg
\`\`\`

## Customization

### Styling

The design uses:
- **Fonts**: Lora (serif) for body, Lato (sans-serif) for headings
- **Colors**: Warm off-white background (#FDFDFB), brown tones (#5C554F, #403D39)
- **Background**: Subtle checkered pattern
- **Design Tokens**: Defined in `app/globals.css`

### Modifying Colors

Edit `app/globals.css`:
\`\`\`css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  /* ... more tokens ... */
}
\`\`\`

### Changing Fonts

Edit `app/layout.tsx`:
\`\`\`typescript
import { Cute_Font as YourFont, Cute_Font as AnotherFont } from 'next/font/google'

const yourFont = YourFont({ subsets: ['latin'] })
\`\`\`

## Technology Stack

- **Framework**: Next.js 16
- **React**: 19.2
- **TypeScript**: 5
- **Styling**: Tailwind CSS 4
- **UI Components**: shadcn/ui with Radix UI
- **Icons**: Lucide React
- **Analytics**: Vercel Analytics
- **Deployment**: Cloudflare Pages / Vercel

## Performance

### Optimizations

- Static site generation for instant page loads
- Image optimization with Next.js Image component
- Automatic code splitting
- CSS optimization with Tailwind CSS
- Global CDN distribution (Cloudflare/Vercel)

### Lighthouse Scores

Target scores:
- Performance: 95+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

## Development

### Available Scripts

\`\`\`bash
# Development server
pnpm dev

# Production build
pnpm build

# Start production server
pnpm start

# Lint code
pnpm lint

# Deploy to Cloudflare Pages
pnpm pages:deploy
\`\`\`

### Project Configuration

- `next.config.mjs` - Next.js configuration
- `tsconfig.json` - TypeScript configuration
- `app/globals.css` - Global styles and design tokens
- `components.json` - shadcn/ui configuration
- `wrangler.toml` - Cloudflare configuration

## Monitoring

### Analytics

The project includes Vercel Analytics. For Cloudflare Analytics:

1. Enable Web Analytics in Cloudflare dashboard
2. Add beacon script to `app/layout.tsx`

### Performance Monitoring

\`\`\`bash
# Analyze bundle size
pnpm build

# Check for unused dependencies
npx depcheck

# Audit dependencies
pnpm audit
\`\`\`

## Backup

### Content Backup

\`\`\`bash
# Backup articles
cp data/articles.json backups/articles-$(date +%Y%m%d).json

# Backup images
tar -czf backups/images-$(date +%Y%m%d).tar.gz public/images/
\`\`\`

### Git Backup

Your entire site is version-controlled:
\`\`\`bash
# View history
git log --oneline

# Restore previous version
git checkout <commit-hash>
\`\`\`

## Troubleshooting

### Common Issues

**Build Errors**
\`\`\`bash
# Clear cache and rebuild
rm -rf .next out node_modules
pnpm install
pnpm build
\`\`\`

**TypeScript Errors**
\`\`\`bash
# Check for errors
pnpm run lint

# The build ignores TypeScript errors by default
# See next.config.mjs
\`\`\`

**Images Not Loading**
- Ensure images are in `public/images/`
- Check image filenames match articles.json
- Verify image format (JPEG, PNG, WebP)

**Deployment Issues**
- Check build logs in deployment platform
- Verify build output directory is `out`
- Ensure all dependencies are in package.json

## Migration

### From Flask Version

The repository includes both Next.js and Flask versions:

- **Next.js**: Modern, static site (recommended)
- **Flask**: Traditional server-side rendering

Both use the same `data/articles.json` format, so content is compatible.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This blog application is a personal project showcasing engineering, aviation, and technology perspectives from an African viewpoint.

## Support

For deployment help:
- See [CLOUDFLARE_DEPLOYMENT.md](./CLOUDFLARE_DEPLOYMENT.md) for Cloudflare Pages
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for traditional hosting
- Check Next.js documentation at [nextjs.org](https://nextjs.org)
- Visit Cloudflare Pages docs at [developers.cloudflare.com/pages](https://developers.cloudflare.com/pages)

---

**Live Site**: Deploy to see your blog live on Cloudflare Pages or Vercel

**Author**: Daudi - Engineering, Aviation, and Technology from an African Perspective
