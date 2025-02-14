<template>
  <div class="monster-statblocks-page">
    <header>
      <h1>Monster Statblocks</h1>
    </header>

    <div class="statblock-list">
      <div
        v-for="(monster, index) in monsters"
        :key="index"
        class="stat-block section"
      >
        <h3>{{ monster.name }}</h3>
        <p>{{ monster.size }} {{ monster.type }}, {{ monster.alignment }}</p>
        <p><strong>Armor Class:</strong> {{ monster.ac }}</p>
        <p><strong>Hit Points:</strong> {{ monster.hp }}</p>
        <p><strong>Speed:</strong> {{ monster.speed }}</p>

        <div class="abilities">
          <p>
            <strong>STR:</strong> {{ monster.stats.str }} <br />({{
              formatModifier(monster.stats.str)
            }})
          </p>
          <p>
            <strong>DEX:</strong> {{ monster.stats.dex }} <br />({{
              formatModifier(monster.stats.dex)
            }})
          </p>
          <p>
            <strong>CON:</strong> {{ monster.stats.con }} <br />({{
              formatModifier(monster.stats.con)
            }})
          </p>
          <p>
            <strong>INT:</strong> {{ monster.stats.int }} <br />({{
              formatModifier(monster.stats.int)
            }})
          </p>
          <p>
            <strong>WIS:</strong> {{ monster.stats.wis }} <br />({{
              formatModifier(monster.stats.wis)
            }})
          </p>
          <p>
            <strong>CHA:</strong> {{ monster.stats.cha }} <br />({{
              formatModifier(monster.stats.cha)
            }})
          </p>
        </div>

        <div class="divider"></div>

        <div class="details">
          <p>
            <strong>Damage Vulnerabilities:</strong>
            {{ monster.damageVulnerabilities || "None" }}
          </p>
          <p><strong>Senses:</strong> {{ monster.senses }}</p>
          <p><strong>Languages:</strong> {{ monster.languages }}</p>
          <p>
            <strong>Challenge:</strong> {{ monster.cr }} ({{ monster.exp }} XP)
          </p>
        </div>

        <div v-if="monster.actions" class="actions">
          <h4>Actions</h4>
          <div v-html="formatText(monster.actions)"></div>
        </div>

        <div v-if="monster.legendaryActions" class="actions">
          <h4>Legendary Actions</h4>
          <div v-html="formatText(monster.legendaryActions)"></div>
        </div>

        <div v-if="monster.traits" class="actions">
          <h4>Traits</h4>
          <div v-html="formatText(monster.traits)"></div>
        </div>

        <div v-if="monster.reactions" class="actions">
          <h4>Reactions</h4>
          <div v-html="formatText(monster.reactions)"></div>
        </div>
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
    // Retrieve the monster statblocks from localStorage with a slight delay to avoid timing issues
    setTimeout(() => {
      const monsterData = localStorage.getItem("monsterStatblocks");
      if (monsterData) {
        this.monsters = JSON.parse(monsterData);
      } else {
        console.error("No monster statblocks found in localStorage.");
      }
    }, 300);
  },
  methods: {
    formatModifier(stat) {
      const modifier = Math.floor((stat - 10) / 2);
      return modifier >= 0 ? `+${modifier}` : modifier.toString();
    },
    formatText(text) {
      // Convert plain text into HTML with line breaks
      return text.replace(/\n/g, "<br>");
    },
  },
};
</script>

<style scoped>
.monster-statblocks-page {
  padding: 20px;
  font-family: "Georgia", serif;
  background: url("@/assets/fantasy-3756975_1280.jpg") no-repeat center center
    fixed;
  background-size: cover;
  min-height: 100vh;
  color: #2c2c2c;
}

/* Updated layout to allow multiple statblocks to align side-by-side */
.statblock-list {
  display: flex;
  flex-wrap: wrap; /* Allows wrapping onto new lines */
  justify-content: center; /* Centers items when fewer than max per row */
  gap: 20px; /* Adds spacing between items */
}

/* Ensures statblocks fit within the grid */
.stat-block {
  width: calc(
    50% - 20px
  ); /* Each statblock takes 50% of the row minus spacing */
  max-width: 500px; /* Prevents them from becoming too wide */
  min-width: 300px; /* Prevents them from becoming too small */
  padding: 15px;
  border: 2px solid #7a4214;
  border-radius: 10px;
  background-color: #fdf6e3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Adjust to full width on smaller screens */
@media (max-width: 700px) {
  .stat-block {
    width: 100%; /* Stack full-width on smaller screens */
  }
}

.stat-block h3 {
  font-size: 1.8em;
  color: #7a4214;
  text-align: center;
  text-transform: uppercase;
  border-bottom: 2px solid #b68973;
  padding-bottom: 5px;
  margin-bottom: 10px;
}

.stat-block p {
  margin: 5px 0;
}

.stat-block h4 {
  font-size: 1.4em;
  color: #7a4214;
  text-transform: uppercase;
  text-align: left;
  border-bottom: 1px solid #b68973;
  padding-bottom: 5px;
  margin-bottom: 10px;
}

.abilities {
  display: flex;
  justify-content: space-between;
  text-align: center;
  margin-bottom: 10px;
}

.details {
  background-color: #fdfaf5;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #d7c4a1;
  margin-top: 10px;
}

.details p {
  font-size: 0.95em;
  margin: 5px 0;
}

.divider {
  height: 2px;
  background-color: #b68973;
  margin: 15px 0;
}

.actions {
  margin-top: 10px;
  background-color: #fdfaf5;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #d7c4a1;
}

.actions div {
  margin: 5px 0;
  font-size: 1em;
  color: #2c2c2c;
}

.stat-block strong {
  font-weight: bold;
  color: #7a4214;
}
</style>
