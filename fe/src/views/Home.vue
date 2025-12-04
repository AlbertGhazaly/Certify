<template>
  <div class="min-h-screen bg-background">
    <!-- Navigation
    <nav class="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-gradient-to-br from-accent via-accent to-primary rounded-lg"></div>
          <span class="font-bold text-lg text-foreground hidden sm:inline">DigitalDiploma</span>
        </div>
        <router-link to="/login" class="px-4 py-2 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent/90 transition">
          Get Started
        </router-link>
      </div>
    </nav> -->

    <!-- Hero Section -->
    <section class="pt-32 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-background via-background to-card">
      <div class="max-w-4xl mx-auto text-center">
        <p class="text-accent text-sm font-semibold mb-4">Blockchain Diploma System</p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-foreground mb-6 leading-tight">
          Digital Diplomas,<br class="hidden sm:block" /><span class="bg-gradient-to-r from-accent via-primary to-accent bg-clip-text text-transparent">Forever Verified</span>
        </h1>
        <p class="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
          Transparent, secure, and immutable diploma verification powered by blockchain technology. Trusted by institutions worldwide.
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <router-link to="/explorer" class="w-full sm:w-auto px-8 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 transition">
            Explore System
          </router-link>
          <router-link to="/verify" class="w-full sm:w-auto px-8 py-3 bg-card border border-border text-foreground rounded-lg font-semibold hover:bg-secondary transition">
            Verify Diploma
          </router-link>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-6xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-card border border-border rounded-lg p-4 text-center">
          <p class="text-2xl sm:text-3xl font-bold text-accent-foreground">10K+</p>
          <p class="text-sm text-muted-foreground mt-1">Diplomas Verified</p>
        </div>
        <div class="bg-card border border-border rounded-lg p-4 text-center">
          <p class="text-2xl sm:text-3xl font-bold texttext-accent-foreground">500+</p>
          <p class="text-sm text-muted-foreground mt-1">Institutions</p>
        </div>
        <div class="bg-card border border-border rounded-lg p-4 text-center">
          <p class="text-2xl sm:text-3xl font-bold text-accent-foreground">99.9%</p>
          <p class="text-sm text-muted-foreground mt-1">Uptime</p>
        </div>
        <div class="bg-card border border-border rounded-lg p-4 text-center">
          <p class="text-2xl sm:text-3xl font-bold text-accent-foreground">24/7</p>
          <p class="text-sm text-muted-foreground mt-1">Support</p>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl sm:text-4xl font-bold text-center mb-12 text-foreground">Key Features</h2>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-card border border-border rounded-xl p-6 hover:border-accent/50 transition">
            <div class="w-12 h-12 bg-gradient-to-br from-accent/20 to-primary/20 rounded-lg flex items-center justify-center mb-4">
              <span class="text-2xl">🔐</span>
            </div>
            <h3 class="text-lg font-semibold text-foreground mb-2">Secure Issuance</h3>
            <p class="text-muted-foreground">ECDSA signatures and SHA-256 hashing ensure diploma authenticity</p>
          </div>
          <div class="bg-card border border-border rounded-xl p-6 hover:border-accent/50 transition">
            <div class="w-12 h-12 bg-gradient-to-br from-accent/20 to-primary/20 rounded-lg flex items-center justify-center mb-4">
              <span class="text-2xl">⛓️</span>
            </div>
            <h3 class="text-lg font-semibold text-foreground mb-2">Immutable Ledger</h3>
            <p class="text-muted-foreground">Hash chain ensures transactions cannot be modified after creation</p>
          </div>
          <div class="bg-card border border-border rounded-xl p-6 hover:border-accent/50 transition">
            <div class="w-12 h-12 bg-gradient-to-br from-accent/20 to-primary/20 rounded-lg flex items-center justify-center mb-4">
              <span class="text-2xl">👤</span>
            </div>
            <h3 class="text-lg font-semibold text-foreground mb-2">Privacy Focused</h3>
            <p class="text-muted-foreground">Off-chain storage with AES encryption protects student data</p>
          </div>
          <div class="bg-card border border-border rounded-xl p-6 hover:border-accent/50 transition">
            <div class="w-12 h-12 bg-gradient-to-br from-accent/20 to-primary/20 rounded-lg flex items-center justify-center mb-4">
              <span class="text-2xl">🔍</span>
            </div>
            <h3 class="text-lg font-semibold text-foreground mb-2">Easy Verification</h3>
            <p class="text-muted-foreground">Anyone can verify diploma authenticity without special tools</p>
          </div>
          <div class="bg-card border border-border rounded-xl p-6 hover:border-accent/50 transition">
            <div class="w-12 h-12 bg-gradient-to-br from-accent/20 to-primary/20 rounded-lg flex items-center justify-center mb-4">
              <span class="text-2xl">📋</span>
            </div>
            <h3 class="text-lg font-semibold text-foreground mb-2">Revocation Support</h3>
            <p class="text-muted-foreground">Institutions can revoke diplomas when needed with full audit trail</p>
          </div>
          <div class="bg-card border border-border rounded-xl p-6 hover:border-accent/50 transition">
            <div class="w-12 h-12 bg-gradient-to-br from-accent/20 to-primary/20 rounded-lg flex items-center justify-center mb-4">
              <span class="text-2xl">🔗</span>
            </div>
            <h3 class="text-lg font-semibold text-foreground mb-2">Public Explorer</h3>
            <p class="text-muted-foreground">Transparent transaction history accessible to all stakeholders</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Roles Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-card/50">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl sm:text-4xl font-bold text-center mb-12 text-foreground">System Roles</h2>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-background border border-border rounded-xl p-8 hover:border-accent/50 transition">
            <h3 class="text-xl font-semibold text-foreground mb-2">Institution Admin</h3>
            <p class="text-muted-foreground text-sm mb-4">Universities and educational institutions</p>
            <ul class="text-sm text-muted-foreground space-y-2 mb-6">
              <li class="flex gap-2"><span class="text-accent">✓</span> Issue new diplomas</li>
              <li class="flex gap-2"><span class="text-accent">✓</span> Revoke diplomas</li>
              <li class="flex gap-2"><span class="text-accent">✓</span> Manage records</li>
            </ul>
            <router-link to="/admin/issue" class="block px-4 py-2 bg-accent text-accent-foreground rounded-lg text-center font-medium hover:bg-accent/90 transition">
              Go to Admin
            </router-link>
          </div>
          <div class="bg-background border border-border rounded-xl p-8 hover:border-accent/50 transition">
            <h3 class="text-xl font-semibold text-foreground mb-2">Verifier</h3>
            <p class="text-muted-foreground text-sm mb-4">Employers and verification services</p>
            <ul class="text-sm text-muted-foreground space-y-2 mb-6">
              <li class="flex gap-2"><span class="text-accent">✓</span> Verify authenticity</li>
              <li class="flex gap-2"><span class="text-accent">✓</span> Check status</li>
              <li class="flex gap-2"><span class="text-accent">✓</span> View history</li>
            </ul>
            <router-link to="/verify" class="block px-4 py-2 bg-accent text-accent-foreground rounded-lg text-center font-medium hover:bg-accent/90 transition">
              Verify Now
            </router-link>
          </div>
          <div class="bg-background border border-border rounded-xl p-8 hover:border-accent/50 transition">
            <h3 class="text-xl font-semibold text-foreground mb-2">Student</h3>
            <p class="text-muted-foreground text-sm mb-4">Diploma recipients</p>
            <ul class="text-sm text-muted-foreground space-y-2 mb-6">
              <li class="flex gap-2"><span class="text-accent">✓</span> View own diplomas</li>
              <li class="flex gap-2"><span class="text-accent">✓</span> Access via link</li>
              <li class="flex gap-2"><span class="text-accent">✓</span> Download cert</li>
            </ul>
            <router-link to="/login" class="block px-4 py-2 bg-accent text-accent-foreground rounded-lg text-center font-medium hover:bg-accent/90 transition">
              Connect Wallet
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-accent/20 via-primary/20 to-accent/20">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl sm:text-4xl font-bold mb-4 text-foreground">Ready to Get Started?</h2>
        <p class="text-lg text-muted-foreground mb-8">Join thousands of institutions securing education credentials</p>
        <router-link to="/login" class="inline-block px-8 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 transition">
          Connect Your Wallet
        </router-link>
      </div>
    </section>
  </div>
</template>


<script setup lang="ts">
</script>
