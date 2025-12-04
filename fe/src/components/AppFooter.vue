<template>
  <footer class="bg-slate-900 text-gray-400 border-t border-slate-800 mt-12">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <div class="grid md:grid-cols-4 gap-8 mb-8">
        <div>
          <h3 class="text-white font-bold mb-4">About</h3>
          <p class="text-sm leading-relaxed">
            A transparent digital diploma system powered by blockchain technology.
          </p>
        </div>
        <div>
          <h3 class="text-white font-bold mb-4">Quick Links</h3>
          <ul class="text-sm space-y-2">
            <li><router-link to="/explorer" class="hover:text-blue-400">Explorer</router-link></li>
            <li><router-link to="/verify" class="hover:text-blue-400">Verify Diploma</router-link></li>
            <li><a href="#" class="hover:text-blue-400">Documentation</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-white font-bold mb-4">Resources</h3>
          <ul class="text-sm space-y-2">
            <li><a href="#" class="hover:text-blue-400">FAQ</a></li>
            <li><a href="#" class="hover:text-blue-400">Support</a></li>
            <li><a href="#" class="hover:text-blue-400">Blog</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-white font-bold mb-4">Legal</h3>
          <ul class="text-sm space-y-2">
            <li><a href="#" class="hover:text-blue-400">Privacy</a></li>
            <li><a href="#" class="hover:text-blue-400">Terms</a></li>
            <li><a href="#" class="hover:text-blue-400">Security</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-slate-800 pt-8 text-sm text-center">
        <p>&copy; 2025 Blockchain Diploma System. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script>
