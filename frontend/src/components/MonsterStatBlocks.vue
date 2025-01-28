<template>
  <div class="monster-statblocks-page">
    <header>
      <h1>Monster Statblocks</h1>
    </header>
    <div class="statblock-list">
      <div v-for="(monster, index) in monsters" :key="index" class="statblock">
        <h2>{{ monster.name }}</h2>
        <p><strong>Size:</strong> {{ monster.size }}</p>
        <p><strong>Type:</strong> {{ monster.type }}</p>
        <p><strong>Alignment:</strong> {{ monster.alignment }}</p>
        <p><strong>Armor Class:</strong> {{ monster.ac }}</p>
        <p><strong>Hit Points:</strong> {{ monster.hp }}</p>
        <p><strong>Speed:</strong> {{ monster.speed }}</p>
        <p>
          <strong>Stats:</strong>
          STR: {{ monster.stats.str }}, DEX: {{ monster.stats.dex }}, CON:
          {{ monster.stats.con }}, INT: {{ monster.stats.int }}, WIS:
          {{ monster.stats.wis }}, CHA: {{ monster.stats.cha }}
        </p>
        <p><strong>Traits:</strong> {{ monster.traits }}</p>
        <p><strong>Actions:</strong> {{ monster.actions }}</p>
        <!-- Add more details as needed -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MonsterStatblocks",
  data() {
    return {
      monsters: [],
    };
  },
  mounted() {
    // Retrieve the monster statblocks from localStorage
    const monsterData = localStorage.getItem("monsterStatblocks");
    if (monsterData) {
      this.monsters = JSON.parse(monsterData);
    } else {
      console.error("No monster statblocks found in localStorage.");
    }
  },
};
</script>

<style>
.monster-statblocks-page {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.statblock-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.statblock {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>
