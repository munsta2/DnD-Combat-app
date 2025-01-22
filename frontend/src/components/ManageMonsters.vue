<template>
  <div class="manage-monsters-page">
    <header class="hero">
      <h1>Manage Monsters</h1>
      <p>Add, edit, or delete monsters to populate your encounters!</p>
      <button class="home-button" @click="goHome">Go to Home</button>
    </header>

    <div class="content">
      <form @submit.prevent="createMonster" class="monster-form">
        <h3>Add New Monster</h3>
        <div class="form-row">
          <label for="monster-name">Name</label>
          <input
            id="monster-name"
            v-model="newMonster.name"
            placeholder="Monster name"
            required
          />
        </div>
        <div class="form-row">
          <label for="monster-size">Size</label>
          <select id="monster-size" v-model="newMonster.size" required>
            <option value="Tiny">Tiny</option>
            <option value="Small">Small</option>
            <option value="Medium">Medium</option>
            <option value="Large">Large</option>
            <option value="Huge">Huge</option>
            <option value="Gargantuan">Gargantuan</option>
          </select>
        </div>
        <div class="form-row">
          <label for="monster-type">Type</label>
          <input
            id="monster-type"
            v-model="newMonster.type"
            placeholder="Type (e.g., Beast)"
          />
        </div>
        <div class="form-row">
          <label for="monster-alignment">Alignment</label>
          <select
            id="monster-alignment"
            v-model="newMonster.alignment"
            required
          >
            <option value="Lawful Good">Lawful Good</option>
            <option value="Neutral Good">Neutral Good</option>
            <option value="Chaotic Good">Chaotic Good</option>
            <option value="Lawful Neutral">Lawful Neutral</option>
            <option value="Neutral">Neutral</option>
            <option value="Chaotic Neutral">Chaotic Neutral</option>
            <option value="Lawful Evil">Lawful Evil</option>
            <option value="Neutral Evil">Neutral Evil</option>
            <option value="Chaotic Evil">Chaotic Evil</option>
          </select>
        </div>
        <div class="form-row">
          <label for="monster-hp">Hit Points</label>
          <input
            id="monster-hp"
            v-model="newMonster.hp"
            type="number"
            placeholder="HP"
            required
          />
        </div>
        <div class="form-row">
          <label for="monster-ac">Armor Class</label>
          <input
            id="monster-ac"
            v-model="newMonster.ac"
            type="number"
            placeholder="AC"
            required
          />
        </div>
        <div class="form-row">
          <label for="monster-speed">Speed</label>
          <input
            id="monster-speed"
            v-model="newMonster.speed"
            placeholder="Speed (e.g., 30 ft., fly 60 ft.)"
          />
        </div>
        <div class="form-row">
          <label for="monster-stats">Stats</label>
          <div class="stats-group">
            <div>
              <label for="monster-str">STR</label>
              <input
                id="monster-str"
                v-model="newMonster.stats.str"
                type="number"
                placeholder="0"
              />
            </div>
            <div>
              <label for="monster-dex">DEX</label>
              <input
                id="monster-dex"
                v-model="newMonster.stats.dex"
                type="number"
                placeholder="0"
              />
            </div>
            <div>
              <label for="monster-con">CON</label>
              <input
                id="monster-con"
                v-model="newMonster.stats.con"
                type="number"
                placeholder="0"
              />
            </div>
            <div>
              <label for="monster-int">INT</label>
              <input
                id="monster-int"
                v-model="newMonster.stats.int"
                type="number"
                placeholder="0"
              />
            </div>
            <div>
              <label for="monster-wis">WIS</label>
              <input
                id="monster-wis"
                v-model="newMonster.stats.wis"
                type="number"
                placeholder="0"
              />
            </div>
            <div>
              <label for="monster-cha">CHA</label>
              <input
                id="monster-cha"
                v-model="newMonster.stats.cha"
                type="number"
                placeholder="0"
              />
            </div>
          </div>
        </div>
        <div class="form-row">
          <label for="monster-languages">Languages</label>
          <input
            id="monster-languages"
            v-model="newMonster.languages"
            placeholder="Enter languages (e.g., Common, Draconic)"
          />
        </div>
        <div class="form-row">
          <label for="monster-vulnerabilities">Damage Vulnerabilities</label>
          <input
            id="monster-vulnerabilities"
            v-model="newMonster.damageVulnerabilities"
            placeholder="Enter vulnerabilities (e.g., fire, cold)"
          />
        </div>
        <div class="form-row">
          <label for="monster-senses">Senses</label>
          <input
            id="monster-senses"
            v-model="newMonster.senses"
            placeholder="Enter senses (e.g., Passive perception 10)"
          />
        </div>
        <div class="form-row">
          <label for="monster-cr">Challenge Rating (CR)</label>
          <input
            id="monster-cr"
            v-model="newMonster.cr"
            placeholder="e.g., 1/4, 1, 2"
          />
        </div>
        <div class="form-row">
          <label for="monster-xp">XP</label>
          <input
            id="monster-xp"
            v-model="newMonster.exp"
            type="number"
            placeholder="Enter XP value (e.g., 50)"
          />
        </div>
        <div class="form-row">
          <label for="monster-actions">Actions</label>
          <textarea
            id="monster-actions"
            v-model="newMonster.actions"
            placeholder="Describe the monster's actions"
          ></textarea>
        </div>
        <div class="form-row">
          <label for="monster-legendary-actions">Legendary Actions</label>
          <textarea
            id="monster-legendary-actions"
            v-model="newMonster.legendaryActions"
            placeholder="Describe legendary actions"
          ></textarea>
        </div>
        <div class="form-row">
          <label for="monster-traits">Traits</label>
          <textarea
            id="monster-traits"
            v-model="newMonster.traits"
            placeholder="Describe special traits"
          ></textarea>
        </div>
        <div class="form-row">
          <label for="monster-reactions">Reactions</label>
          <textarea
            id="monster-reactions"
            v-model="newMonster.reactions"
            placeholder="Describe reactions"
          ></textarea>
        </div>
        <button type="submit">Add Monster</button>
      </form>

      <div class="monster-list">
        <h3>Existing Monsters</h3>
        <input
          type="text"
          v-model="searchTerm"
          placeholder="Search monsters..."
          class="search-bar"
        />
        <ul>
          <li
            v-for="monster in filteredMonsters"
            :key="monster.id"
            @click="selectMonster(monster)"
          >
            {{ monster.name }}
          </li>
        </ul>
        <div v-if="selectedMonster" class="monster-details">
          <div class="statblock">
            <!-- Monster Name -->
            <h2>{{ selectedMonster.name }}</h2>
            <p class="subtitle">
              {{ selectedMonster.size }} {{ selectedMonster.type }},
              {{ selectedMonster.alignment }}
            </p>

            <!-- Armor Class, Hit Points, Speed -->
            <div class="statblock-header">
              <p><strong>Armor Class:</strong> {{ selectedMonster.ac }}</p>
              <p><strong>Hit Points:</strong> {{ selectedMonster.hp }}</p>
              <p><strong>Speed:</strong> {{ selectedMonster.speed }}</p>
            </div>

            <!-- Stats -->
            <div class="stats">
              <p><strong>STR:</strong> {{ selectedMonster.stats.str }}</p>
              <p><strong>DEX:</strong> {{ selectedMonster.stats.dex }}</p>
              <p><strong>CON:</strong> {{ selectedMonster.stats.con }}</p>
              <p><strong>INT:</strong> {{ selectedMonster.stats.int }}</p>
              <p><strong>WIS:</strong> {{ selectedMonster.stats.wis }}</p>
              <p><strong>CHA:</strong> {{ selectedMonster.stats.cha }}</p>
            </div>

            <!-- Details -->
            <div class="details">
              <p>
                <strong>Damage Vulnerabilities:</strong>
                {{ selectedMonster.damageVulnerabilities || "None" }}
              </p>
              <p><strong>Senses:</strong> {{ selectedMonster.senses }}</p>
              <p><strong>Languages:</strong> {{ selectedMonster.languages }}</p>
              <p>
                <strong>Challenge:</strong> {{ selectedMonster.cr }} ({{
                  selectedMonster.exp
                }}
                XP)
              </p>
            </div>

            <!-- Actions -->
            <div class="abilities">
              <h3>Actions</h3>
              <div v-html="selectedMonster.actions"></div>
            </div>

            <!-- Legendary Actions -->
            <div class="abilities" v-if="selectedMonster.legendaryActions">
              <h3>Legendary Actions</h3>
              <div v-html="selectedMonster.legendaryActions"></div>
            </div>

            <!-- Traits -->
            <div class="abilities" v-if="selectedMonster.traits">
              <h3>Traits</h3>
              <div v-html="selectedMonster.traits"></div>
            </div>

            <!-- Reactions -->
            <div class="abilities" v-if="selectedMonster.reactions">
              <h3>Reactions</h3>
              <div v-html="selectedMonster.reactions"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
export default {
  name: "ManageMonsters",
  setup() {
    const router = useRouter();
    const monsters = ref([]);
    const newMonster = ref({
      name: "",
      size: "",
      type: "",
      alignment: "",
      hp: 0,
      ac: 0,
      speed: "",
      stats: { str: 0, dex: 0, con: 0, int: 0, wis: 0, cha: 0 },
      actions: "",
      legendaryActions: "",
      traits: "",
      reactions: "",
      languages: "",
      damageVulnerabilities: "",
      senses: "",
      cr: "",
      exp: 0,
    });
    const searchTerm = ref("");
    const selectedMonster = ref(null);

    const goHome = () => {
      router.push("/");
    };

    const filteredMonsters = computed(() => {
      return monsters.value.filter((monster) => {
        const monsterName = monster?.name || ""; // Default to empty string if undefined
        const search = searchTerm.value || ""; // Default to empty string if undefined
        return monsterName.toLowerCase().includes(search.toLowerCase());
      });
    });

    const fetchMonsters = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/monsters`
      );
      monsters.value = await response.json();
    };

    const createMonster = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/monsters`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(newMonster.value),
        }
      );
      if (!response.ok) {
        // Handle non-2xx responses (e.g., 400 or 500 errors)
        const errorDetails = await response.json();
        console.error("Failed to add monster:", errorDetails);
        alert(
          `Failed to add monster: ${errorDetails.error || "Unknown error"}`
        );
        return;
      }
      const createdMonster = await response.json();
      alert("Monster added successfully!");
      monsters.value.push(createdMonster);
      newMonster.value = {
        name: "",
        size: "",
        type: "",
        alignment: "",
        hp: 0,
        ac: 0,
        speed: "",
        stats: { str: 0, dex: 0, con: 0, int: 0, wis: 0, cha: 0 },
        actions: "",
        legendaryActions: "",
        traits: "",
        reactions: "",
        languages: "",
        damageVulnerabilities: "",
        senses: "",
        cr: "",
        exp: 0,
      };
    };

    const deleteMonster = async (monsterId) => {
      await fetch(`${process.env.VUE_APP_API_URL}/api/monsters/${monsterId}`, {
        method: "DELETE",
      });
      monsters.value = monsters.value.filter((m) => m.id !== monsterId);
      selectedMonster.value = null;
    };

    const selectMonster = (monster) => {
      selectedMonster.value = monster;
    };

    const startEdit = (monster) => {
      alert(`Edit functionality is not implemented yet for ${monster.name}`);
    };

    onMounted(() => {
      fetchMonsters();
    });

    return {
      monsters,
      newMonster,
      searchTerm,
      selectedMonster,
      filteredMonsters,
      createMonster,
      deleteMonster,
      selectMonster,
      startEdit,
      goHome,
    };
  },
};
</script>

<style>
.manage-monsters-page {
  text-align: center;
  font-family: "Georgia", serif;
  color: #fff;
  background: url("@/assets/fantasy-3756975_1280.jpg") no-repeat center center
    fixed;
  background-size: cover;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 20px;
}

.hero {
  background-color: rgba(0, 0, 0, 0.6);
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.content {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: flex-start;
}

.monster-form {
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 20px;
  border-radius: 10px;
  max-width: 450px;
  flex: 1;
}

.monster-list {
  flex: 2;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 20px;
  border-radius: 10px;
}

.monster-details {
  position: relative;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 10px;
}

.action-buttons button {
  padding: 10px;
  font-size: 1em;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.action-buttons button:hover {
  background-color: #b22b36;
}

.form-row {
  margin-bottom: 15px;
  text-align: left;
}

.form-row label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #fff;
}

.stats-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.stats-group label {
  font-weight: bold;
  margin-right: 5px;
}

.stats-group input {
  width: 50px;
  text-align: center;
}

.search-bar {
  margin: 10px auto;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 80%;
}

.monster-list ul {
  list-style: none;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 8px;
  padding: 10px;
  color: white;
}

.monster-list ul li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ccc;
}

.monster-list ul li:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.statblock {
  font-family: "Georgia", serif;
  background-color: #fdf5e6;
  border: 2px solid #8b4513;
  border-radius: 8px;
  padding: 20px;
  max-width: 500px;
  margin: 20px auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  color: #333;
  position: relative;
}

.statblock h2 {
  font-size: 1.8em;
  margin: 0;
  text-align: center;
  color: #8b4513;
  border-bottom: 2px solid #8b0000; /* Redline under the title */
  padding-bottom: 10px;
}

.statblock .subtitle {
  text-align: center;
  font-style: italic;
  color: #555;
  margin-bottom: 10px;
}

.statblock-header,
.stats,
.details,
.abilities {
  padding: 10px 0;
  border-top: 2px solid #8b0000; /* Redline between sections */
  margin-top: 10px;
}

.statblock-header {
  display: flex;
  justify-content: space-between;
  font-size: 1em;
}

.stats {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 5px;
  text-align: center;
}

.stats p {
  margin: 0;
  font-size: 0.9em;
}

.details p,
.abilities p {
  font-size: 0.9em;
  margin: 5px 0;
}

.abilities h3 {
  font-size: 1.2em;
  margin: 10px 0 5px;
  color: #8b4513;
}

hr {
  border: none;
  border-top: 2px solid #8b0000; /* Redline for horizontal rules */
  margin: 10px 0;
}

button {
  margin: 5px;
  padding: 10px 20px;
  font-size: 1em;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

button {
  margin: 5px;
  padding: 10px 20px;
  font-size: 1em;
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
