<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const message = ref("");

    onMounted(async () => {
      try {
        const response = await fetch("http://localhost:5000/api/hello");
        const data = await response.json();
        message.value = data.message; // Set the fetched message
      } catch (error) {
        console.error("Error fetching data from Flask:", error);
      }
    });

    return { message };
  },
};
</script>
