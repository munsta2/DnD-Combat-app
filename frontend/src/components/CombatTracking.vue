<template>
  <div class="combat-tracking-page">
    <!-- Header -->
    <header class="header">
      <h1>Combat Tracking</h1>
      <p>Manage combatants, track turns, apply damage, and dynamically manage combatants.</p>
    </header>

    <div class="combat-ui">
      <!-- Encounter Selection -->
      <div class="encounter-selection card">
        <h2>Select Encounter</h2>
        <select v-model="selectedEncounter" @change="loadEncounter">
          <option value="" disabled selected>Select an encounter</option>
          <option
            v-for="encounter in encounters"
            :key="encounter.id"
            :value="encounter.id"
          >
            {{ encounter.name }}
          </option>
        </select>
      </div>

      <!-- Add Monster Section -->
      <div class="add-monster card">
        <h2>Add Monster</h2>
        <select v-model="selectedMonster">
          <option value="" disabled selected>Select a monster</option>
          <option
            v-for="monster in availableMonsters"
            :key="monster.id"
            :value="monster"
          >
            {{ monster.name }}
          </option>
        </select>
        <button @click="addMonster">Add Monster</button>
      </div>

      <!-- Roll Initiative for Monsters -->
      <div
        class="roll-initiative card"
        v-if="combatants.length > 0 && !initiativesSet"
      >
        <h2>Roll Initiatives for Monsters</h2>
        <button @click="rollMonsterInitiatives">
          Roll Monster Initiatives
        </button>
      </div>

      <!-- Initiative Input -->
      <div
        class="initiative-input card"
        v-if="combatants.length > 0 && !initiativesSet"
      >
        <h2>Set Initiative</h2>
        <ul>
          <li v-for="combatant in combatants" :key="combatant.id">
            <strong>{{ combatant.name }}</strong>
            <input
              type="number"
              v-model.number="combatant.initiative"
              placeholder="Enter Initiative"
            />
          </li>
        </ul>
        <button @click="setInitiatives">Set Initiatives</button>
      </div>

      <!-- Combatants List -->
      <div
        class="combatants-list card"
        v-if="combatants.length > 0 && initiativesSet"
      >
        <h2>Combatants</h2>
        <ul>
          <li
            v-for="(combatant, index) in combatants"
            :key="combatant.id"
            :class="{ active: index === currentTurnIndex }"
          >
            <strong>{{ combatant.name }}</strong> - HP: {{ combatant.hp }}/
            {{ combatant.maxHp }}
            | AC: {{ combatant.ac }} |
            Initiative:
            <input
              type="number"
              v-model.number="combatant.initiative"
              @change="updateInitiative(index, combatant.initiative)"
              style="width: 50px;"
            />
          </li>
        </ul>
      </div>

      <!-- Apply Damage Section -->
      <div class="apply-damage card" v-if="combatants.length > 0 && initiativesSet">
        <h2>Apply Damage</h2>
        <label for="combatant-select">Select Combatant:</label>
        <select id="combatant-select" v-model="selectedCombatant">
          <option
            v-for="combatant in combatants"
            :key="combatant.id"
            :value="combatant.id"
          >
            {{ combatant.name }}
          </option>
        </select>
        <label for="damage-input">Damage:</label>
        <input
          id="damage-input"
          v-model.number="damageAmount"
          type="number"
          placeholder="Enter damage"
        />
        <button @click="applyDamage">Apply</button>
      </div>

      <!-- Next Turn and End Combat Buttons -->
      <div class="action-buttons card" v-if="combatants.length > 0 && initiativesSet">
        <button @click="nextTurn">Next Turn</button>
        <button @click="endCombat" class="end-combat">End Combat</button>
      </div>

      <!-- Stat Block -->
      <div class="stat-block card" v-if="activeCombatant && initiativesSet">
        <h2>Statblock</h2>
        <p><strong>Name:</strong> {{ activeCombatant.name }}</p>
        <p>
          <strong>HP:</strong> {{ activeCombatant.hp }}/
          {{ activeCombatant.maxHp }}
        </p>
        <p><strong>AC:</strong> {{ activeCombatant.ac }}</p>
        <p><strong>Type:</strong> {{ activeCombatant.type }}</p>
        <p><strong>Initiative:</strong> {{ activeCombatant.initiative }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      encounters: [],
      availableMonsters: [],
      selectedEncounter: null,
      selectedMonster: null,
      combatants: [],
      currentTurnIndex: 0,
      selectedCombatant: null,
      damageAmount: 0,
      initiativesSet: false,
    };
  },
  computed: {
    activeCombatant() {
      return this.combatants[this.currentTurnIndex];
    },
  },
  methods: {
    fetchEncounters() {
      fetch("http://127.0.0.1:5000/api/encounters")
        .then((response) => response.json())
        .then((data) => {
          this.encounters = data;
        })
        .catch((error) => {
          console.error("Error fetching encounters:", error);
        });
    },
    fetchAvailableMonsters() {
      fetch("http://127.0.0.1:5000/api/monsters")
        .then((response) => response.json())
        .then((data) => {
          this.availableMonsters = data;
        })
        .catch((error) => {
          console.error("Error fetching monsters:", error);
        });
    },
    loadEncounter() {
      fetch("http://127.0.0.1:5000/api/combat/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ encounter_id: this.selectedEncounter }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.combatants = data.turn_order.map((combatant) => ({
            ...combatant,
            initiative: 0,
          }));
          this.currentTurnIndex = 0;
        })
        .catch((error) => {
          console.error("Error loading encounter:", error);
        });
    },
    rollMonsterInitiatives() {
      this.combatants.forEach((combatant) => {
        if (combatant.type === "monster") {
          const dexMod = Math.floor((combatant.dex || 10 - 10) / 2);
          combatant.initiative = Math.floor(Math.random() * 20) + 1 + dexMod;
        }
      });
    },
    setInitiatives() {
      this.combatants.sort((a, b) => b.initiative - a.initiative);
      this.initiativesSet = true;
    },
    addMonster() {
      if (this.selectedMonster) {
        const newMonster = {
          id: `${this.selectedMonster.id}-${Date.now()}`,
          name: this.selectedMonster.name,
          type: "monster",
          hp: this.selectedMonster.hp,
          maxHp: this.selectedMonster.hp,
          ac: this.selectedMonster.ac,
          dex: this.selectedMonster.dex || 10,
          initiative: 0,
        };
        this.combatants.push(newMonster);
      }
    },
    applyDamage() {
      if (!this.selectedCombatant || !this.damageAmount) {
        alert("Please select a combatant and enter damage.");
        return;
      }
      const combatant = this.combatants.find(
        (c) => c.id === this.selectedCombatant
      );
      if (combatant) {
        combatant.hp = Math.max(0, combatant.hp - this.damageAmount);
      }
    },
    nextTurn() {
      this.currentTurnIndex =
        (this.currentTurnIndex + 1) % this.combatants.length;
    },
    endCombat() {
      this.selectedEncounter = null;
      this.selectedMonster = null;
      this.combatants = [];
      this.currentTurnIndex = 0;
      this.selectedCombatant = null;
      this.damageAmount = 0;
      this.initiativesSet = false;
    },
    updateInitiative(index, initiative) {
      this.combatants[index].initiative = initiative;
      this.combatants.sort((a, b) => b.initiative - a.initiative);
      this.currentTurnIndex = 0;
    },
  },
  mounted() {
    this.fetchEncounters();
    this.fetchAvailableMonsters();
  },
};
</script>








<style>
.end-combat {
  background-color: #ff4d4d;
  color: white;
}

.end-combat:hover {
  background-color: #e63939;
}

.combat-tracking-page {
  font-family: Arial, sans-serif;
  background: #f9f9f9;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.combat-ui {
  display: grid;
  grid-template-columns: 1fr 2fr 2fr;
  gap: 20px;
}

.card {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

input,
select {
  width: 100%;
  margin: 5px 0;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.combatants-list ul {
  list-style: none;
  padding: 0;
}

.combatants-list li {
  padding: 5px;
  border-bottom: 1px solid #ddd;
}

.combatants-list li.active {
  background: #e0ffe0;
  font-weight: bold;
}
</style>
