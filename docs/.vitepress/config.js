module.exports = {
  title: 'OncaLLM Documentation',
  description: 'AI-Powered Kubernetes Alert Analysis Documentation',
  
  // Output directory for GitHub Pages
  outDir: '../dist',
  
  // GitHub Pages deployment - repository name
  base: '/oncallm/',
  
  // Ignore dead links for now (temporary)
  ignoreDeadLinks: true,
  
  head: [
    ['link', { rel: 'icon', href: '/oncallm/favicon.svg' }],
    ['meta', { property: 'og:title', content: 'OncaLLM - AI-Powered Kubernetes Alert Analysis' }],
    ['meta', { property: 'og:description', content: 'Reduce MTTR by 80% with intelligent root cause detection. OncaLLM analyzes your Kubernetes alerts and provides actionable insights in seconds.' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    ['meta', { name: 'twitter:title', content: 'OncaLLM - AI-Powered Kubernetes Alert Analysis' }],
    ['meta', { name: 'twitter:description', content: 'Reduce MTTR by 80% with intelligent root cause detection' }]
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'OncaLLM',
    
    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Deployment', link: '/deployment/prerequisites' },
      { text: 'Configuration', link: '/configuration/environment' },
      { text: 'API', link: '/api/webhook' },
      { 
        text: 'Links',
        items: [
          { text: 'GitHub Repository', link: 'https://github.com/mmdaz/oncallm' },
          { text: 'Enterprise Contact', link: 'mailto:mohammad.azhdari.22@gmail.com' }
        ]
      }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/getting-started' },
            { text: 'How It Works', link: '/guide/how-it-works' },
            { text: 'Features', link: '/guide/features' }
          ]
        }
      ],
      '/deployment/': [
        {
          text: 'Deployment',
          items: [
            { text: 'Prerequisites', link: '/deployment/prerequisites' },
            { text: 'Quick Start', link: '/deployment/quick-start' }
          ]
        }
      ],
      '/configuration/': [
        {
          text: 'Configuration',
          items: [
            { text: 'Environment Variables', link: '/configuration/environment' },
            { text: 'AlertManager Setup', link: '/configuration/alertmanager' },
            { text: 'Resource Limits', link: '/configuration/resources' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API Reference',
          items: [
            { text: 'Webhook Endpoint', link: '/api/webhook' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/mmdaz/oncallm' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2025 OncaLLM Team'
    },

    editLink: {
      pattern: 'https://github.com/mmdaz/oncallm/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },

    search: {
      provider: 'local'
    },

    lastUpdated: {
      text: 'Updated at',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium'
      }
    }
  },

  markdown: {
    lineNumbers: true
  }
} 