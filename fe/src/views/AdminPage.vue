<template>
  <section class="py-20 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <router-link to="/" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8">
          <span>←</span> Back
        </router-link>
      <h1 class="text-3xl font-bold text-center mb-12">
        Admin Dashboard
      </h1>

      <div class="grid md:grid-cols-2 gap-6">
        <!-- Student Management -->
        <div class="bg-background border border-border rounded-xl p-8 hover:border-accent/50 transition">
          <h3 class="text-xl font-semibold mb-2">Student Management</h3>
          <p class="text-muted-foreground text-sm mb-6">
            Manage students and issued certificates
          </p>

          <router-link
            to="/admin/students"
            class="block px-4 py-2 bg-accent text-accent-foreground rounded-lg text-center font-medium hover:bg-accent/90 transition"
          >
            Go to Students
          </router-link>
        </div>

        <!-- Issuer Registrations -->
        <div class="bg-background border border-border rounded-xl p-8 hover:border-accent/50 transition">
          <h3 class="text-xl font-semibold mb-2">Issuer Registrations</h3>
          <p class="text-muted-foreground text-sm mb-6">
            Review and approve issuer registration requests
          </p>

          <router-link
            to="/admin/issuer-registrations"
            class="block px-4 py-2 bg-accent text-accent-foreground rounded-lg text-center font-medium hover:bg-accent/90 transition"
          >
            Manage Issuers
          </router-link>
        </div>
        <!-- Issue Diploma -->
        <div class="bg-background border border-border rounded-xl p-8 hover:border-accent/50 transition">
          <h3 class="text-xl font-semibold mb-2">Issue New Diploma</h3>
          <p class="text-muted-foreground text-sm mb-6">
            Create and issue a new digital diploma certificate
          </p>

          <router-link
            to="/admin/issue"
            class="block px-4 py-2 bg-accent text-accent-foreground rounded-lg text-center font-medium hover:bg-accent/90 transition"
          >
          Issue New Diploma
          </router-link>
        </div>
        <!-- Revoke Diploma -->
        <div class="bg-background border border-border rounded-xl p-8 hover:border-accent/50 transition">
          <h3 class="text-xl font-semibold mb-2">Revoke Diploma</h3>
          <p class="text-muted-foreground text-sm mb-6">
            Revoke or invalidate an issued diploma certificate
          </p>

          <router-link
            to="/admin/issue"
            class="block px-4 py-2 bg-accent text-accent-foreground rounded-lg text-center font-medium hover:bg-accent/90 transition"
          >
          Revoke Diploma
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>
