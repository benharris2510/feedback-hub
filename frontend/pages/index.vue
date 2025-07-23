<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative overflow-hidden py-20 lg:py-32">
      <!-- Background Elements -->
      <div class="absolute inset-0">
        <div class="absolute top-0 left-1/4 w-72 h-72 bg-violet-500/10 rounded-full blur-3xl"></div>
        <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
        <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-violet-500/5 to-purple-500/5 rounded-full blur-3xl"></div>
      </div>
      
      <div class="relative max-w-7xl mx-auto px-6 text-center">
        <div class="inline-flex items-center px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-300 text-sm font-medium mb-8">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
          New: Real-time feedback analytics
        </div>
        
        <h1 class="text-5xl lg:text-7xl font-bold mb-8 leading-tight">
          <span class="text-gradient">Feedback that</span><br>
          <span class="text-slate-100">drives growth</span>
        </h1>
        
        <p class="text-xl text-slate-400 mb-12 max-w-3xl mx-auto leading-relaxed">
          Transform customer insights into product success. Our modern platform helps you collect, 
          analyze, and act on feedback with the speed your business demands.
        </p>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
          <NuxtLink to="/register" class="btn btn-primary btn-lg group">
            Get Started Free
            <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </svg>
          </NuxtLink>
          
          <NuxtLink to="/feedback" class="btn btn-secondary btn-lg">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            View Demo
          </NuxtLink>
        </div>
        
        <!-- Stats -->
        <div class="flex flex-wrap justify-center gap-8 text-center">
          <div class="px-4">
            <div class="text-3xl font-bold text-gradient">10k+</div>
            <div class="text-sm text-slate-400">Feedback collected</div>
          </div>
          <div class="px-4">
            <div class="text-3xl font-bold text-gradient">99.9%</div>
            <div class="text-sm text-slate-400">Uptime</div>
          </div>
          <div class="px-4">
            <div class="text-3xl font-bold text-gradient">24/7</div>
            <div class="text-sm text-slate-400">Support</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 lg:py-32">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center mb-20">
          <h2 class="text-4xl lg:text-5xl font-bold mb-6">
            <span class="text-gradient">Everything you need</span><br>
            <span class="text-slate-100">to succeed</span>
          </h2>
          <p class="text-xl text-slate-400 max-w-3xl mx-auto">
            Built for modern teams who move fast and ship better products through customer-driven insights.
          </p>
        </div>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="card card-hover group">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a2 2 0 01-2-2v-1M15 8V6a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2h2m8-8V6a2 2 0 00-2-2H9a2 2 0 00-2 2v2m8 4V8a2 2 0 00-2-2H9a2 2 0 00-2 2v8a2 2 0 002 2h6l4 4v-4z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-100 mb-4">Community Forums</h3>
            <p class="text-slate-400 leading-relaxed">
              Foster engagement with threaded discussions, voting, and real-time notifications.
            </p>
          </div>
          
          <!-- Feature 2 -->
          <div class="card card-hover group">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-100 mb-4">Smart Feedback</h3>
            <p class="text-slate-400 leading-relaxed">
              AI-powered categorization and sentiment analysis for actionable insights.
            </p>
          </div>
          
          <!-- Feature 3 -->
          <div class="card card-hover group">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-100 mb-4">Developer API</h3>
            <p class="text-slate-400 leading-relaxed">
              Integrate seamlessly with REST APIs, webhooks, and extensive documentation.
            </p>
          </div>
          
          <!-- Feature 4 -->
          <div class="card card-hover group">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-100 mb-4">Advanced Analytics</h3>
            <p class="text-slate-400 leading-relaxed">
              Track trends, measure satisfaction, and make data-driven product decisions.
            </p>
          </div>
          
          <!-- Feature 5 -->
          <div class="card card-hover group">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-100 mb-4">Enterprise Security</h3>
            <p class="text-slate-400 leading-relaxed">
              SOC 2 compliant with advanced permissions and audit logging.
            </p>
          </div>
          
          <!-- Feature 6 -->
          <div class="card card-hover group">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2M7 4h10l-1 14H8L7 4zM9 9v6M15 9v6"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-100 mb-4">Multi-Platform</h3>
            <p class="text-slate-400 leading-relaxed">
              Works everywhere - web, mobile, desktop, and embedded widgets.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 lg:py-32">
      <div class="max-w-4xl mx-auto px-6 text-center">
        <div class="card glass-strong p-12">
          <h2 class="text-4xl lg:text-5xl font-bold mb-6">
            <span class="text-gradient">Ready to transform</span><br>
            <span class="text-slate-100">your feedback game?</span>
          </h2>
          <p class="text-xl text-slate-400 mb-10 max-w-2xl mx-auto">
            Join thousands of teams already building better products with customer insights.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <NuxtLink to="/register" class="btn btn-primary btn-lg">
              Start Free Trial
              <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
            </NuxtLink>
            
            <NuxtLink to="/forums" class="btn btn-ghost btn-lg">
              View Live Demo
            </NuxtLink>
          </div>
          
          <p class="text-sm text-slate-500 mt-6">
            No credit card required • 14-day free trial • Cancel anytime
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'Feedback Hub - Transform Customer Insights Into Product Success',
  meta: [
    { name: 'description', content: 'Modern feedback platform built for fast-moving teams. Collect, analyze, and act on customer feedback with AI-powered insights and developer-friendly APIs.' }
  ]
})
</script>