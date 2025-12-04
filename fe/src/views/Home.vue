<attachment id="src/views/Home.vue" folderPath="/home/albert/Documents/code/kripto/Certify/fe/src/views">
<content>
<template>
  <div class="home">
    <h1>Welcome to the Home Page</h1>
    <p>This is the main view of the application.</p>
    <HelloWorld />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import HelloWorld from '../components/HelloWorld.vue';

export default defineComponent({
  name: 'Home',
  components: {
    HelloWorld,
  },
});
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>
</content>
</attachment>