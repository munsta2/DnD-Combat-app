<template>
  <div class="homepage">
    <header class="hero">
      <h1>D&D Combat Manager</h1>
      <p>Streamline your adventure, focus on the story.</p>
    </header>

    <div class="actions">
      <button @click="$router.push('/players')">Manage Players</button>
      <button @click="$router.push('/parties')">Manage Parties</button>
      <button @click="$router.push('/monsters')">Manage Monsters</button>
      <button @click="$router.push('/encounters')">Manage Encounter</button>
      <button @click="$router.push('/combat')">Manage Combat</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style>
.homepage {
  text-align: center;
  font-family: "Georgia", serif;
  color: #333;
  background: url("@/assets/fantasy-3756975_1280.jpg") no-repeat center center
    fixed;
  background-size: cover;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.hero {
  background-color: rgba(0, 0, 0, 0.6);
  padding: 20px;
  border-radius: 10px;
  color: #fff;
}

.hero h1 {
  font-size: 3em;
  margin: 0;
}

.hero p {
  font-size: 1.5em;
  margin-top: 10px;
}

.actions {
  margin-top: 30px;
}

button {
  margin: 10px;
  padding: 15px 30px;
  font-size: 1.2em;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
