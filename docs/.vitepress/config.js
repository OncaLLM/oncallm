module.exports = {
  title: 'OncaLLM Documentation',
  description: 'AI-Powered Kubernetes Alert Analysis Documentation',
  
  // Output directory relative to this config file  
  outDir: '../landing-page/dist',
  
  // GitHub Pages deployment - main site at /oncallm/
  base: process.env.NODE_ENV === 'production' ? '/oncallm/' : '/',
  
  // Ignore dead links for now (temporary)
  ignoreDeadLinks: true,
  
  head: [
    ['link', { rel: 'icon', href: '/oncallm/docs/favicon.svg' }],
    ['meta', { property: 'og:title', content: 'OncaLLM Documentation' }],
    ['meta', { property: 'og:description', content: 'AI-Powered Kubernetes Alert Analysis Documentation' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    ['meta', { name: 'twitter:title', content: 'OncaLLM Documentation' }],
    ['meta', { name: 'twitter:description', content: 'AI-Powered Kubernetes Alert Analysis Documentation' }]
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
          { text: 'GitHub Repository', link: 'https://github.com/OncaLLM/oncallm' },
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
            { text: 'Quick Start', link: '/deployment/quick-start' },
            { text: 'Helm Installation', link: '/deployment/helm' },
            { text: 'Docker Installation', link: '/deployment/docker' },
            { text: 'Configuration', link: '/deployment/configuration' }
          ]
        }
      ],
      '/configuration/': [
        {
          text: 'Configuration',
          items: [
            { text: 'Environment Variables', link: '/configuration/environment' },
            { text: 'AlertManager Setup', link: '/configuration/alertmanager' },
            { text: 'OpenAI Configuration', link: '/configuration/openai' },
            { text: 'Resource Limits', link: '/configuration/resources' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API Reference',
          items: [
            { text: 'Webhook Endpoint', link: '/api/webhook' },
            { text: 'Health Endpoints', link: '/api/health' },
            { text: 'Reports API', link: '/api/reports' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/OncaLLM/oncallm' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024 OncaLLM Team'
    },

    editLink: {
      pattern: 'https://github.com/OncaLLM/oncallm/edit/main/docs/:path',
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