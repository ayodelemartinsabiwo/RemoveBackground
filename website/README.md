# Background Remover Website

Professional marketing website for the Background Remover Windows desktop application.

## 📁 Files

- `index.html` - Main landing page with hero, features, download, and documentation sections
- `style.css` - Modern, responsive CSS with orange theme and smooth animations
- `script.js` - Interactive functionality including FAQ accordion, smooth scroll, and animations
- `README.md` - This file

## 🎨 Features

### Design
- **Modern UI/UX** - Clean, professional design with orange gradient theme
- **Fully Responsive** - Works perfectly on desktop, tablet, and mobile devices
- **Smooth Animations** - Scroll-triggered animations and hover effects
- **Accessible** - Semantic HTML and keyboard navigation support

### Sections
1. **Hero Section** - Eye-catching introduction with CTA buttons
2. **Features Grid** - Six key features with icons and descriptions
3. **How It Works** - Three-step process visualization
4. **Download Section** - Prominent download CTA with system requirements
5. **Documentation** - Quick links to guides and resources
6. **FAQ Accordion** - Common questions with expandable answers
7. **Footer** - Links, legal info, and credits

### Interactive Elements
- Mobile-friendly navigation menu
- FAQ accordion functionality
- Smooth scroll to sections
- Animated stats and counters
- Context menu preview demo
- Download button with alerts

## 🚀 Setup & Deployment

### Local Testing

1. **Open Locally**
   ```bash
   # Simply open index.html in your browser
   open index.html  # macOS
   start index.html  # Windows
   xdg-open index.html  # Linux
   ```

2. **Local Server (Recommended)**
   ```bash
   # Python 3
   python -m http.server 8000

   # Python 2
   python -m SimpleHTTPServer 8000

   # Node.js (if you have http-server installed)
   npx http-server
   ```

   Then visit: `http://localhost:8000`

### Deployment Options

#### GitHub Pages (Free)

1. **Push to GitHub**
   ```bash
   git add website/
   git commit -m "Add website for Background Remover"
   git push origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings > Pages
   - Source: Deploy from branch `main`
   - Folder: Select `/website` or move files to root
   - Save and wait for deployment

3. **Custom Domain (Optional)**
   - Add `CNAME` file with your domain
   - Configure DNS settings

#### Netlify (Free)

1. **Drag & Drop Deploy**
   - Go to [netlify.com](https://netlify.com)
   - Drag the `website/` folder to Netlify Drop
   - Get instant URL

2. **Continuous Deployment**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli

   # Deploy
   cd website/
   netlify deploy --prod
   ```

#### Vercel (Free)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd website/
vercel --prod
```

#### Traditional Web Hosting

1. **FTP Upload**
   - Upload all files in `website/` folder
   - Ensure `index.html` is in root directory
   - Set file permissions if needed

2. **cPanel/File Manager**
   - Log into hosting control panel
   - Navigate to `public_html/` or `www/`
   - Upload website files
   - Test the URL

## 🔧 Customization

### Update Download Link

Edit `index.html` line ~388:

```html
<button class="btn btn-primary btn-large" onclick="window.location.href='YOUR_DOWNLOAD_URL'">
```

Or edit `script.js` `handleDownload()` function.

### Change Colors

Edit CSS variables in `style.css`:

```css
:root {
    --primary-color: #ff6b35;     /* Main orange color */
    --primary-dark: #e85a28;      /* Darker orange */
    --primary-light: #ff8555;     /* Lighter orange */
    /* ... more colors ... */
}
```

### Add Analytics

Add Google Analytics in `index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Add Screenshots

1. Create an `images/` folder
2. Add screenshot images
3. Update `demo-img-placeholder` in HTML:

```html
<img src="images/before.jpg" alt="Before" />
```

### Update Content

All content is in `index.html`. Search for sections by ID:
- `#features` - Features section
- `#how-it-works` - Process steps
- `#download` - Download section
- `#documentation` - Docs cards
- FAQ section

## 📱 Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🎯 SEO Optimization

The website includes:
- Semantic HTML5 structure
- Meta descriptions and keywords
- Open Graph tags (add for social sharing)
- Fast loading with optimized CSS/JS
- Mobile-friendly responsive design

### Add Open Graph Tags

Add to `<head>` section:

```html
<meta property="og:title" content="Background Remover - AI-Powered">
<meta property="og:description" content="Professional Windows desktop application for removing backgrounds">
<meta property="og:image" content="URL_TO_PREVIEW_IMAGE">
<meta property="og:url" content="YOUR_WEBSITE_URL">
<meta name="twitter:card" content="summary_large_image">
```

## 📊 Performance

- **Fast Load Time**: Minimal dependencies, optimized CSS/JS
- **Lighthouse Score**: Aim for 90+ in all categories
- **No External Dependencies**: No jQuery, Bootstrap, or heavy frameworks
- **Lazy Loading**: Images and animations load on demand

## 🛠 Development

### File Structure
```
website/
├── index.html      # Main HTML file
├── style.css       # All styles
├── script.js       # All JavaScript
├── README.md       # This file
└── images/         # (Create this for screenshots)
```

### Best Practices

1. **Test Responsiveness**
   - Test on multiple screen sizes
   - Use browser DevTools responsive mode
   - Test on real devices

2. **Validate Code**
   - HTML: [validator.w3.org](https://validator.w3.org/)
   - CSS: [jigsaw.w3.org/css-validator](https://jigsaw.w3.org/css-validator/)

3. **Optimize Performance**
   - Compress images (use WebP format)
   - Minify CSS/JS for production
   - Enable gzip compression on server

### Build for Production

**Minify CSS** (using online tools or CLI):
```bash
# Using clean-css-cli
npm install -g clean-css-cli
cleancss -o style.min.css style.css
```

**Minify JavaScript**:
```bash
# Using terser
npm install -g terser
terser script.js -o script.min.js
```

Update `index.html` to use minified versions:
```html
<link rel="stylesheet" href="style.min.css">
<script src="script.min.js"></script>
```

## 📝 TODO

- [ ] Add actual download link when installer is built
- [ ] Add screenshot images in hero demo section
- [ ] Create and add favicon.ico
- [ ] Add GitHub Releases integration
- [ ] Create installation guide page
- [ ] Add usage examples with real screenshots
- [ ] Implement download statistics
- [ ] Add testimonials/reviews section

## 🤝 Contributing

To improve the website:

1. Test on different browsers/devices
2. Suggest improvements via GitHub issues
3. Submit pull requests with enhancements
4. Report bugs or broken links

## 📄 License

This website is part of the Background Remover project. See main LICENSE.txt for details.

## 💡 Tips

- **Update regularly**: Keep download links and version info current
- **Monitor analytics**: Track which sections get most engagement
- **Test CTAs**: Experiment with button text and placement
- **Add social proof**: Include user testimonials or download counts
- **Create video demo**: Add YouTube video for better engagement

---

**Built with ❤️ for Background Remover**
