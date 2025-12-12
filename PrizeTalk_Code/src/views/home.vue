<template>
  <div class="page-container">
    <div class="page-header">
      <h1>Welcome to PrizeTalk!</h1>
      <p class="subtitle">
        ~Jazz Hands~ Explore awards, see what others are thinking, and make discussion groups!
      </p>
    </div>

    <div class="welcome-card">
      <HelloWorld 
        msg="How Does This Work?"
        @greet="handleGreet"
      />

      <div class="instructions">
        <h2>What have we done:</h2>
        <ul>
          <li>Make a set of users using Signup</li>
          <li>Once logged-in, search through all the awards in separate tabs</li>
          <li>Create global posts in the community page with tags you can look up</li>
          <li>React using Like, Dislike, or comment on yours and other's posts</li>
          <li>Make your own group for group-only member posts</li>
          <li>Make member comments and react here too, only visible by other members</li>
          <li>If you made the group, you can delete the group. Also, if you are an Admin, you can delete any comment or post</li>
        </ul>
      </div>

      <div class="gif-container">
        <img src="../assets/low-poly-spinning.png" alt="Low-poly spinning fish GIF" />
      </div>

      <div class="demo-output" v-if="greetMessage">
        {{ greetMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HelloWorld from '../components/HelloWorld.vue'

const greetMessage = ref('')

const handleGreet = (payload) => {
  greetMessage.value = payload
}
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-header h1 {
  font-size: 2rem;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
  animation: slideDown 0.6s ease;
}

.subtitle {
  color: var(--color-text-muted);
  font-size: 1rem;
  animation: slideDown 0.6s ease;
}

.welcome-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  animation: fadeIn 0.5s ease;
}

.instructions {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--color-background);
  border: 1px dashed var(--color-border);
  border-radius: 8px;
}

.instructions h2 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.instructions ul {
  list-style: none;
  padding-left: 0;
}

.instructions li {
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.gif-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1.5rem 0;
}

.gif-container img {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  animation: fadeIn 0.5s ease;
}

.demo-output {
  margin-top: 1rem;
  font-weight: 600;
  color: var(--color-button-bg);
  font-size: 1rem;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
  .welcome-card {
    padding: 1.5rem;
  }
  
  .page-header h1 {
    font-size: 1.75rem;
  }
  
  .instructions h2 {
    font-size: 1rem;
  }
}
</style>
