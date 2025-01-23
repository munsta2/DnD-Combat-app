<template>
  <div class="combat-tracking-page">
    <!-- Header -->
    <header class="header">
      <h1>Combat Tracking</h1>
      <p>Manage combatants, track turns, and apply damage.</p>
    </header>

    <div class="combat-ui">
      <!-- Encounter Selection -->
      <div class="encounter-selection">
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

      <!-- Roll Initiative for Monsters -->
      <div
        class="roll-initiative"
        v-if="combatants.length > 0 && !initiativesSet"
      >
        <h2>Roll Initiatives for Monsters</h2>
        <button @click="rollMonsterInitiatives">
          Roll Monster Initiatives
        </button>
      </div>

      <!-- Initiative Input -->
      <div
        class="initiative-input"
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
              :disabled="combatant.type === 'monster'"
              Disable
              input
              for
              monsters
            />
            />
          </li>
        </ul>
        <button @click="setInitiatives">Set Initiatives</button>
      </div>

      <!-- Damage Application -->
      <div
        class="damage-application"
        v-if="combatants.length > 0 && initiativesSet"
      >
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

      <!-- Next Turn Button -->
      <div class="next-turn" v-if="combatants.length > 0 && initiativesSet">
        <button @click="nextTurn">Next Turn</button>
      </div>

      <!-- Combatants List -->
      <div
        class="combatants-list"
        v-if="combatants.length > 0 && initiativesSet"
      >
        <h2>Combatants</h2>
        <ul>
          <li
            v-for="(combatant, index) in combatants"
            :key="combatant.id"
            :class="{ active: index === currentTurnIndex }"
          >
            <strong>{{ combatant.name }}</strong> - HP: {{ combatant.hp }}/{{
              combatant.maxHp
            }}
            | AC: {{ combatant.ac }} | Initiative: {{ combatant.initiative }}
          </li>
        </ul>
      </div>

      <!-- Stat Block -->
      <div class="stat-block" v-if="activeCombatant && initiativesSet">
        <h2>Statblock</h2>
        <p><strong>Name:</strong> {{ activeCombatant.name }}</p>
        <p>
          <strong>HP:</strong> {{ activeCombatant.hp }}/{{
            activeCombatant.maxHp
          }}
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
      encounters: [], // List of encounters
      selectedEncounter: null, // Currently selected encounter
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
      // Fetch list of encounters
      fetch("http://127.0.0.1:5000/api/encounters") // Replace with your API endpoint
        .then((response) => response.json())
        .then((data) => {
          this.encounters = data;
        })
        .catch((error) => {
          console.error("Error fetching encounters:", error);
        });
    },
    loadEncounter() {
      // Start combat for the selected encounter
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
            initiative: 0, // Initialize initiative to 0
          }));
          this.currentTurnIndex = 0; // Reset turn index
        })
        .catch((error) => {
          console.error("Error loading encounter:", error);
        });
    },
    rollMonsterInitiatives() {
      // Automatically roll initiative for monsters
      this.combatants.forEach((combatant) => {
        if (combatant.type === "monster") {
          console.log(combatant);
          const dexMod = Math.floor((combatant.dex - 10) / 2); // Calculate Dexterity modifier
          combatant.initiative = Math.floor(Math.random() * 20) + 1 + dexMod;
        }
      });
    },
    setInitiatives() {
      // Sort combatants by initiative (highest to lowest)
      this.combatants.sort((a, b) => b.initiative - a.initiative);
      this.initiativesSet = true;
    },
    applyDamage() {
      if (!this.selectedCombatant || !this.damageAmount) {
        alert("Please select a combatant and enter damage.");
        return;
      }
      // Update the combatant's HP locally
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
  },
  mounted() {
    this.fetchEncounters(); // Load encounters on page load
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
