<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
    <!-- Navigation -->
    <nav class="relative z-50 py-6 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-r from-blue-400 to-purple-500 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-xl">O</span>
          </div>
          <span class="text-white font-bold text-xl">OnCallM</span>
        </div>
        <div class="hidden md:flex items-center space-x-8">
          <a href="#features" class="text-gray-300 hover:text-white transition-colors">Features</a>
          <a href="#how-it-works" class="text-gray-300 hover:text-white transition-colors">How It Works</a>
          <a href="#benefits" class="text-gray-300 hover:text-white transition-colors">Benefits</a>
          <button class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all transform hover:scale-105">
            Get Started
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto text-center">
        <div class="max-w-4xl mx-auto">
          <h1 class="text-5xl md:text-7xl font-bold text-white mb-8 leading-tight">
            AI-Powered
            <span class="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              Kubernetes
            </span>
            Alert Analysis
          </h1>
          <p class="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed">
            Reduce MTTR by 80% with intelligent root cause detection. 
            OnCallM analyzes your Kubernetes alerts and provides actionable insights in seconds.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button class="w-full sm:w-auto bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-all transform hover:scale-105 shadow-2xl">
              Start Free Analysis
            </button>
            <button class="w-full sm:w-auto border-2 border-gray-400 text-gray-300 px-8 py-4 rounded-lg text-lg font-semibold hover:border-white hover:text-white transition-all">
              View Demo
            </button>
          </div>
        </div>
        
        <!-- Stats -->
        <div class="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div class="text-center">
            <div class="text-4xl font-bold text-white mb-2">80%</div>
            <div class="text-gray-300">Faster Resolution</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold text-white mb-2">24/7</div>
            <div class="text-gray-300">AI Monitoring</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold text-white mb-2">∞</div>
            <div class="text-gray-300">Alert Processing</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Intelligent Alert Analysis
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            OnCallM leverages advanced AI to understand your Kubernetes environment and provide intelligent insights.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-2xl hover:shadow-xl transition-all transform hover:-translate-y-2">
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-4">Smart Root Cause Analysis</h3>
            <p class="text-gray-600">
              AI analyzes logs, metrics, and cluster state to identify the root cause of alerts automatically.
            </p>
          </div>

          <div class="bg-gradient-to-br from-purple-50 to-pink-100 p-8 rounded-2xl hover:shadow-xl transition-all transform hover:-translate-y-2">
            <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-4">Lightning Fast Response</h3>
            <p class="text-gray-600">
              Get detailed analysis reports in seconds, not minutes. Reduce your mean time to resolution dramatically.
            </p>
          </div>

          <div class="bg-gradient-to-br from-green-50 to-emerald-100 p-8 rounded-2xl hover:shadow-xl transition-all transform hover:-translate-y-2">
            <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-4">Kubernetes Native</h3>
            <p class="text-gray-600">
              Built specifically for Kubernetes environments with deep understanding of K8s resources and patterns.
            </p>
          </div>

          <div class="bg-gradient-to-br from-orange-50 to-red-100 p-8 rounded-2xl hover:shadow-xl transition-all transform hover:-translate-y-2">
            <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-600 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-4">Actionable Recommendations</h3>
            <p class="text-gray-600">
              Get specific, actionable steps to resolve issues, not just notifications about problems.
            </p>
          </div>

          <div class="bg-gradient-to-br from-cyan-50 to-blue-100 p-8 rounded-2xl hover:shadow-xl transition-all transform hover:-translate-y-2">
            <div class="w-12 h-12 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-4">Easy Integration</h3>
            <p class="text-gray-600">
              Simple webhook integration with AlertManager. Deploy once and start getting intelligent insights immediately.
            </p>
          </div>

          <div class="bg-gradient-to-br from-indigo-50 to-purple-100 p-8 rounded-2xl hover:shadow-xl transition-all transform hover:-translate-y-2">
            <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 00-2 2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-4">Rich Analytics</h3>
            <p class="text-gray-600">
              Comprehensive analysis reports with visual insights, trends, and historical context for better decision making.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            How OnCallM Works
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Simple integration, powerful analysis, actionable results.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div class="text-center">
            <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <span class="text-white font-bold text-2xl">1</span>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Alert Integration</h3>
            <p class="text-gray-600 text-lg">
              Connect OnCallM to your AlertManager with a simple webhook configuration. No complex setup required.
            </p>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <span class="text-white font-bold text-2xl">2</span>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">AI Analysis</h3>
            <p class="text-gray-600 text-lg">
              Our AI analyzes alert context, logs, metrics, and cluster state to understand the root cause of issues.
            </p>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <span class="text-white font-bold text-2xl">3</span>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Actionable Insights</h3>
            <p class="text-gray-600 text-lg">
              Receive detailed analysis reports with specific recommendations to resolve issues quickly and effectively.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits Section -->
    <section id="benefits" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div>
            <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-8">
              Transform Your On-Call Experience
            </h2>
            <div class="space-y-6">
              <div class="flex items-start space-x-4">
                <div class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center mt-1">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-bold text-gray-900 mb-2">Reduce Alert Fatigue</h3>
                  <p class="text-gray-600">Stop drowning in alerts. Get intelligent summaries and prioritized action items.</p>
                </div>
              </div>
              
              <div class="flex items-start space-x-4">
                <div class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center mt-1">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-bold text-gray-900 mb-2">Faster Issue Resolution</h3>
                  <p class="text-gray-600">AI-powered root cause analysis helps you fix problems faster than ever before.</p>
                </div>
              </div>
              
              <div class="flex items-start space-x-4">
                <div class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center mt-1">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-bold text-gray-900 mb-2">Better Sleep</h3>
                  <p class="text-gray-600">Confident resolution means less stress and better work-life balance for your team.</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl p-8 text-white">
            <h3 class="text-3xl font-bold mb-8">Ready to Get Started?</h3>
            <p class="text-xl mb-8 opacity-90">
              Join forward-thinking DevOps teams using OnCallM to revolutionize their incident response.
            </p>
            <button class="w-full bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105">
              Start Your Free Trial
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 px-4 sm:px-6 lg:px-8 bg-gray-900">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="flex items-center space-x-3 mb-6 md:mb-0">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-400 to-purple-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">O</span>
            </div>
            <span class="text-white font-bold text-xl">OnCallM</span>
          </div>
          <div class="text-gray-400 text-center md:text-right">
            <p>&copy; 2024 OnCallM. All rights reserved.</p>
            <p class="mt-2">Built with ❤️ for DevOps teams everywhere.</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    // Add smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }
}
</script> 