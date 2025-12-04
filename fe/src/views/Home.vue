<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-slate-900 to-slate-800 text-white py-20">
      <div class="max-w-6xl mx-auto px-4 text-center">
        <h1 class="text-5xl font-bold mb-6">Blockchain Diploma System</h1>
        <p class="text-xl text-slate-200 mb-8 max-w-2xl mx-auto">
          Transparent, secure, and immutable digital diploma issuance and verification powered by blockchain technology
        </p>
        <div class="flex justify-center gap-4 flex-wrap">
          <router-link
            to="/explorer"
            class="px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition"
          >
            Explore Transactions
          </router-link>
          <router-link
            to="/verify"
            class="px-8 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition"
          >
            Verify Diploma
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-gray-900 mb-12 text-center">Key Features</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-white rounded-lg shadow p-6">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span class="text-xl">🔐</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Secure Issuance</h3>
            <p class="text-gray-600">ECDSA signatures and SHA-256 hashing ensure diploma authenticity</p>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span class="text-xl">⛓️</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Immutable Ledger</h3>
            <p class="text-gray-600">Hash chain ensures transactions cannot be modified after creation</p>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span class="text-xl">👤</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Privacy Focused</h3>
            <p class="text-gray-600">Off-chain storage with AES encryption protects student data</p>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span class="text-xl">🔍</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Easy Verification</h3>
            <p class="text-gray-600">Anyone can verify diploma authenticity without special tools</p>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span class="text-xl">📋</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Revocation Support</h3>
            <p class="text-gray-600">Institutions can revoke diplomas when needed with full audit trail</p>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span class="text-xl">🔗</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Public Explorer</h3>
            <p class="text-gray-600">Transparent transaction history accessible to all stakeholders</p>
          </div>
        </div>
      </div>
    </section>

    <!-- User Roles Section -->
    <section class="py-16 bg-white">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-gray-900 mb-12 text-center">System Roles</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="border border-gray-200 rounded-lg p-8 text-center hover:shadow-lg transition">
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Institution Admin</h3>
            <p class="text-gray-600 mb-4">Universities and educational institutions</p>
            <ul class="text-left text-sm text-gray-700 space-y-2 mb-6">
              <li>✓ Issue new diplomas</li>
              <li>✓ Revoke diplomas</li>
              <li>✓ Manage diploma records</li>
            </ul>
            <router-link
              to="/admin/issue"
              class="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Go to Admin
            </router-link>
          </div>
          <div class="border border-gray-200 rounded-lg p-8 text-center hover:shadow-lg transition">
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Verifier</h3>
            <p class="text-gray-600 mb-4">Employers and verification services</p>
            <ul class="text-left text-sm text-gray-700 space-y-2 mb-6">
              <li>✓ Verify diploma authenticity</li>
              <li>✓ Check revocation status</li>
              <li>✓ View transaction history</li>
            </ul>
            <router-link
              to="/verify"
              class="inline-block px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Verify Now
            </router-link>
          </div>
          <div class="border border-gray-200 rounded-lg p-8 text-center hover:shadow-lg transition">
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Student</h3>
            <p class="text-gray-600 mb-4">Diploma recipients</p>
            <ul class="text-left text-sm text-gray-700 space-y-2 mb-6">
              <li>✓ View own diplomas</li>
              <li>✓ Access via secure link</li>
              <li>✓ Download certificate</li>
            </ul>
            <router-link
              to="/login"
              class="inline-block px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
            >
              Connect Wallet
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-blue-600 text-white py-16">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-4">Get Started Today</h2>
        <p class="text-xl mb-8">Join the revolution in digital diploma verification</p>
        <router-link
          to="/login"
          class="inline-block px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition"
        >
          Connect Your Wallet
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
</script>
