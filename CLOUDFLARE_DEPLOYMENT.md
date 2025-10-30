# Cloudflare Pages Deployment Guide

This guide will help you deploy Daudi's Perspective blog to Cloudflare Pages.

## Prerequisites

- Cloudflare account (free tier works)
- GitHub account
- Git installed locally
- Node.js 22+ installed

## Deployment Methods

### Method 1: Direct Git Integration (Recommended)

This method automatically deploys your site whenever you push to your repository.

#### Step 1: Push to GitHub

\`\`\`bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for Cloudflare Pages deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/daudis-perspective.git

# Push to GitHub
git push -u origin main
\`\`\`

#### Step 2: Connect to Cloudflare Pages

1. **Log in to Cloudflare Dashboard**
   - Go to https://dash.cloudflare.com
   - Navigate to "Workers & Pages"

2. **Create New Pages Project**
   - Click "Create application"
   - Select "Pages"
   - Click "Connect to Git"

3. **Connect Your Repository**
   - Authorize Cloudflare to access your GitHub account
   - Select your repository: `daudis-perspective`
   - Click "Begin setup"

4. **Configure Build Settings**
   \`\`\`
   Project name: daudis-perspective
   Production branch: main
   Framework preset: Next.js (Static HTML Export)
   Build command: npm run build
   Build output directory: out
   Root directory: / (leave empty)
   Node version: 22
   \`\`\`

5. **Environment Variables** (if needed)
   - Click "Add variable" if you have any environment variables
   - For this static blog, none are required

6. **Deploy**
   - Click "Save and Deploy"
   - Wait 2-5 minutes for the build to complete

#### Step 3: Access Your Site

Once deployed, you'll get a URL like:
\`\`\`
https://daudis-perspective.pages.dev
\`\`\`

### Method 2: Wrangler CLI Deployment

For direct deployment without Git integration.

#### Step 1: Install Wrangler

\`\`\`bash
# Install Wrangler globally
npm install -g wrangler

# Or use pnpm
pnpm add -g wrangler
\`\`\`

#### Step 2: Authenticate

\`\`\`bash
# Login to Cloudflare
wrangler login
\`\`\`

This will open a browser window for authentication.

#### Step 3: Build Your Project

\`\`\`bash
# Install dependencies
npm install

# Build the project
npm run build
\`\`\`

#### Step 4: Deploy

\`\`\`bash
# Deploy to Cloudflare Pages (first time)
wrangler pages deploy out --project-name=daudis-perspective

# For subsequent deployments
npm run build && wrangler pages deploy out --project-name=daudis-perspective
\`\`\`

## Custom Domain Setup

### Step 1: Add Custom Domain

1. In Cloudflare Pages dashboard, go to your project
2. Click "Custom domains" tab
3. Click "Set up a custom domain"
4. Enter your domain (e.g., `daudisperspective.com`)

### Step 2: Configure DNS

If your domain is already on Cloudflare:
- DNS records will be automatically configured
- SSL certificate will be automatically provisioned

If your domain is elsewhere:
1. Add a CNAME record pointing to your Pages URL
2. Wait for DNS propagation (up to 24 hours)

### Step 3: Verify

- Visit your custom domain
- Ensure HTTPS is working (automatic with Cloudflare)

## Continuous Deployment

With Git integration, every push to your main branch automatically triggers a deployment:

\`\`\`bash
# Make changes to your blog
git add .
git commit -m "Add new article"
git push origin main

# Cloudflare automatically builds and deploys
\`\`\`

### Preview Deployments

Every pull request gets its own preview URL:
- Create a branch: `git checkout -b new-feature`
- Push changes: `git push origin new-feature`
- Create PR on GitHub
- Get unique preview URL in PR comments

## Managing Articles

### Adding New Articles

1. **Edit articles.json**
   \`\`\`bash
   # Edit the data file
   nano data/articles.json
   \`\`\`

2. **Add Article Entry**
   \`\`\`json
   {
     "id": "new-article-slug",
     "title": "Your Article Title",
     "category": "Engineering",
     "date": "2025-01-30",
     "image": "new-article.jpg",
     "content": [
       "First paragraph...",
       "Second paragraph..."
     ]
   }
   \`\`\`

3. **Add Article Image**
   \`\`\`bash
   # Add image to public/images/
   cp ~/Downloads/new-article.jpg public/images/
   \`\`\`

4. **Commit and Deploy**
   \`\`\`bash
   git add data/articles.json public/images/new-article.jpg
   git commit -m "Add new article: Your Article Title"
   git push origin main
   \`\`\`

5. **Automatic Deployment**
   - Cloudflare automatically builds and deploys
   - Live in 2-5 minutes

## Performance Optimization

Cloudflare Pages automatically provides:

### Global CDN
- Content served from 300+ locations worldwide
- Automatic edge caching
- Sub-50ms response times globally

### Automatic Optimizations
- Brotli compression
- HTTP/3 support
- Minification of HTML, CSS, JS

## Monitoring and Analytics

### Built-in Analytics

Cloudflare Pages provides:
- Page views and unique visitors
- Geographic distribution
- Performance metrics
- Bandwidth usage

Access analytics in your Cloudflare Pages dashboard under the "Analytics" tab.

## Troubleshooting

### Build Failures

**Issue**: Build fails with "Command not found: pnpm"

**Solution**: The build command is set to `npm run build` which should work by default.

**Issue**: Build fails with TypeScript errors

**Solution**: The config has `ignoreBuildErrors: true`, but you can fix errors locally:
\`\`\`bash
npm run lint
\`\`\`

**Issue**: Build output directory not found

**Solution**: Ensure the build output directory is set to `out` in Cloudflare Pages settings.

### Deployment Issues

**Issue**: Site shows 404 errors

**Solution**: 
1. Verify build output directory is set to `out`
2. Check that `output: 'export'` is in next.config.mjs
3. Review build logs for errors

**Issue**: Images not loading

**Solution**: Ensure images are in `public/images/` directory and referenced correctly.

**Issue**: Styles not applying

**Solution**: Check that globals.css is imported in app/layout.tsx

## Security

Cloudflare Pages automatically provides:

- **DDoS Protection**: Automatic mitigation
- **SSL/TLS**: Free SSL certificates with auto-renewal
- **Bot Protection**: Automatic bot detection

## Costs

### Free Tier Includes:
- Unlimited bandwidth
- Unlimited requests
- 500 builds per month
- 1 build at a time
- 20,000 files per deployment

For a personal blog, the free tier is more than sufficient.

## Rollback

### Rollback to Previous Deployment

1. Go to Cloudflare Pages dashboard
2. Click "Deployments" tab
3. Find the previous successful deployment
4. Click "..." menu
5. Select "Rollback to this deployment"

### Rollback via Git

\`\`\`bash
# Revert to previous commit
git revert HEAD
git push origin main
\`\`\`

## Support and Resources

### Documentation
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Next.js on Cloudflare](https://developers.cloudflare.com/pages/framework-guides/nextjs/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)

### Community
- [Cloudflare Community](https://community.cloudflare.com/)
- [Cloudflare Discord](https://discord.gg/cloudflaredev)

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Cloudflare Pages project created
- [ ] Build settings configured correctly (build command: `npm run build`, output: `out`)
- [ ] First deployment successful
- [ ] Site accessible via .pages.dev URL
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] Analytics enabled
- [ ] First article published
- [ ] Performance verified

Congratulations! Your blog is now live on Cloudflare Pages with global CDN distribution and automatic deployments.
