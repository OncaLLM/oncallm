# OncaLLM Landing Page

A modern, responsive Vue 3 landing page for OncaLLM - AI-Powered Kubernetes Alert Analysis tool.

![OncaLLM Banner](https://via.placeholder.com/800x400/3B82F6/FFFFFF?text=OncaLLM+-+AI-Powered+Kubernetes+Alert+Analysis)

## 🚀 Features

- **Modern Vue 3** with Composition API
- **Lightning Fast** - Built with Vite for optimal performance
- **SEO Optimized** - Complete meta tags, Open Graph, and structured data
- **Responsive Design** - Works perfectly on all devices
- **WindiCSS** - Utility-first CSS framework for rapid styling
- **Smooth Animations** - Beautiful hover effects and transitions
- **Professional Design** - Clean, modern, and engaging UI

## 🛠️ Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **WindiCSS** - On-demand atomic CSS framework
- **Inter Font** - Modern, readable typography
- **SVG Icons** - Scalable vector graphics for crisp visuals

## 📦 Installation

1. **Clone or navigate to the landing page directory:**
   ```bash
   cd landing-page
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## 🚦 Development

Start the development server with hot reload:

```bash
npm run dev
```

The landing page will be available at `http://localhost:5173`

## 🏗️ Build for Production

Create an optimized production build:

```bash
npm run build
```

The built files will be in the `dist/` directory.

## 👀 Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

## 📁 Project Structure

```
landing-page/
├── public/
│   └── favicon.svg          # OncaLLM favicon
├── src/
│   ├── App.vue              # Main landing page component
│   └── main.js              # Vue app entry point
├── index.html               # HTML template with SEO meta tags
├── package.json             # Dependencies and scripts
├── vite.config.js           # Vite configuration
├── windi.config.js          # WindiCSS configuration
└── README.md                # This file
```

## 🎨 Design Features

### Hero Section
- **Eye-catching gradient background** from slate to indigo
- **Large, bold typography** with gradient text effects
- **Compelling value proposition** with key statistics
- **Clear call-to-action buttons** for user engagement

### Features Section
- **Six key features** with beautiful gradient cards
- **Hover animations** for interactive experience
- **SVG icons** for each feature
- **Benefits-focused content** highlighting OncaLLM's value

### How It Works
- **Three-step process** explanation
- **Numbered circles** with gradient backgrounds
- **Clear, concise descriptions** of each step

### Benefits Section
- **Split layout** with benefits list and CTA card
- **Checkmark icons** for visual reinforcement
- **Gradient CTA card** for conversion focus

## 🔍 SEO Optimization

The landing page includes comprehensive SEO optimization:

- **Meta tags** for title, description, and keywords
- **Open Graph tags** for social media sharing
- **Twitter Card tags** for Twitter sharing
- **Structured data (JSON-LD)** for search engines
- **Semantic HTML** structure
- **Fast loading times** with Vite optimization

## 📱 Responsive Design

- **Mobile-first approach** with responsive breakpoints
- **Flexible grid layouts** using CSS Grid and Flexbox
- **Touch-friendly buttons** and interactive elements
- **Optimized typography** for all screen sizes

## 🎯 Performance

- **Vite optimization** for fast development and builds
- **WindiCSS purging** removes unused CSS
- **Modern JavaScript** with tree-shaking
- **Optimized images** and SVG icons
- **Font optimization** with Google Fonts preconnect

## 🚀 Deployment Options

### Static Hosting (Recommended)
The built landing page is a static site that can be deployed to:

- **Vercel** - `vercel --prod`
- **Netlify** - Drag and drop `dist/` folder
- **GitHub Pages** - Upload `dist/` contents
- **AWS S3** - Upload to S3 bucket with static hosting
- **Cloudflare Pages** - Connect repository for auto-deployment

### CDN Integration
For optimal performance, serve the built assets through a CDN:

- **Cloudflare**
- **AWS CloudFront**
- **Google Cloud CDN**

## 🔧 Customization

### Colors
Modify the gradient colors in `windi.config.js` and `App.vue`:

```javascript
// Primary gradient: blue to purple
from-blue-500 to-purple-600

// Secondary gradients: customize in App.vue
from-slate-900 via-blue-900 to-indigo-900
```

### Content
Update the content in `src/App.vue`:
- Hero section text and statistics
- Feature descriptions and benefits
- Call-to-action text and links

### Styling
WindiCSS utilities can be modified in `windi.config.js`:
- Custom animations
- Typography settings
- Spacing and sizing

## 📝 Content Strategy

The landing page content focuses on:

1. **Problem-Solution Fit** - Addresses alert fatigue and slow resolution
2. **Value Proposition** - 80% faster resolution with AI analysis
3. **Technical Benefits** - Kubernetes-native, easy integration
4. **Social Proof** - Professional design builds trust
5. **Clear CTAs** - Multiple conversion opportunities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or support:
- Open an issue in the repository
- Contact the OncaLLM team
- Check the main project documentation

---

**Built with ❤️ for DevOps teams everywhere** 