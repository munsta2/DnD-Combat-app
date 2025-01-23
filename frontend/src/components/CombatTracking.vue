<template>
  <div class="combat-tracking">
    <header class="hero">
      <h1>Combat Tracking</h1>
      <p>
        Manage combatants, track turns, apply damage, and dynamically manage
        combatants.
      </p>
    </header>

    <div class="content">
      <!-- Encounter Selection -->
      <div class="encounter-selection section">
        <h3>Select Encounter</h3>
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
      <div class="add-monster section">
        <h3>Add Monster</h3>
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

      <!-- Dice Roll Section -->
      <div class="dice-roll-section section">
        <h3>Roll Dice</h3>
        <div class="dice-controls">
          <label for="dice-count">Number of Dice:</label>
          <input
            id="dice-count"
            type="number"
            v-model.number="numberOfDice"
            min="1"
            style="width: 50px; margin-left: 10px"
          />
        </div>
        <div class="dice-buttons">
          <button
            v-for="sides in [4, 6, 8, 10, 12]"
            :key="sides"
            @click="rollDice(sides)"
          >
            🎲 D{{ sides }}
          </button>
        </div>
        <div v-if="diceRollResult.length > 0" class="dice-roll-result">
          <p>
            You rolled:
            <span v-for="(roll, index) in diceRollResult" :key="index">
              [{{ roll }}]{{ index < diceRollResult.length - 1 ? "," : "" }}
            </span>
          </p>
          <p><strong>Total:</strong> {{ diceRollTotal }}</p>
        </div>
      </div>

      <!-- Combatants Section -->
      <div class="combatants-section section">
        <h3>Combatants</h3>
        <ul class="styled-list">
          <li
            v-for="(combatant, index) in combatants"
            :key="combatant.id"
            :class="{ active: index === currentTurnIndex }"
          >
            <input
              type="text"
              v-model="combatant.displayName"
              @input="updateDisplayName"
              style="width: 150px"
            />
            - HP: {{ combatant.hp }}/{{ combatant.maxHp }} | AC:
            {{ combatant.ac }} | Initiative:
            <input
              type="number"
              v-model.number="combatant.initiative"
              @change="updateInitiative(index, combatant.initiative)"
              style="width: 50px"
            />
          </li>
        </ul>
      </div>

      <!-- Apply Damage Section -->
      <div class="apply-damage section">
        <h3>Apply Damage</h3>
        <label for="combatant-select">Select Combatant:</label>
        <select id="combatant-select" v-model="selectedCombatant">
          <option
            v-for="combatant in combatants"
            :key="combatant.id"
            :value="combatant.id"
          >
            {{ combatant.displayName }}
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

      <!-- Next Turn and End Combat -->
      <div class="action-buttons section">
        <button @click="nextTurn">Next Turn</button>
        <button @click="endCombat" class="end-combat">End Combat</button>
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
      numberOfDice: 1,
      diceRollResult: [],
    };
  },
  computed: {
    activeCombatant() {
      return this.combatants[this.currentTurnIndex];
    },
    diceRollTotal() {
      return this.diceRollResult.reduce((total, roll) => total + roll, 0);
    },
  },
  methods: {
    fetchEncounters() {
      fetch(`${process.env.VUE_APP_API_URL}/api/encounters`)
        .then((response) => response.json())
        .then((data) => {
          this.encounters = data;
        })
        .catch((error) => {
          console.error("Error fetching encounters:", error);
        });
    },
    rollDice(sides) {
      this.diceRollResult = [];
      for (let i = 0; i < this.numberOfDice; i++) {
        this.diceRollResult.push(Math.floor(Math.random() * sides) + 1);
      }
    },

    fetchAvailableMonsters() {
      fetch(`${process.env.VUE_APP_API_URL}/api/monsters`)
        .then((response) => response.json())
        .then((data) => {
          this.availableMonsters = data;
        })
        .catch((error) => {
          console.error("Error fetching monsters:", error);
        });
    },
    loadEncounter() {
      fetch(`${process.env.VUE_APP_API_URL}/api/combat/start`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ encounter_id: this.selectedEncounter }),
      })
        .then((response) => response.json())
        .then((data) => {
          let monsterCount = 0; // Counter to assign unique numbers to monsters

          // Assign displayName and count existing monsters
          this.combatants = data.turn_order.map((combatant) => {
            if (combatant.type === "monster") {
              monsterCount += 1; // Increment monster count
              return {
                ...combatant,
                displayName: `${combatant.name} ${monsterCount}`,
                initiative: combatant.initiative || 0,
              };
            } else {
              // Players keep their original name
              return {
                ...combatant,
                displayName: combatant.name,
                initiative: combatant.initiative || 0,
              };
            }
          });

          this.monsterCounter = monsterCount; // Set monster counter for future additions
          this.currentTurnIndex = 0; // Reset turn order index
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
    assignMonsterNumbers() {
      let monsterIndex = 1;
      this.combatants.forEach((combatant) => {
        if (combatant.type === "monster") {
          combatant.alias = `${combatant.name} ${monsterIndex}`;
          monsterIndex++;
        } else {
          combatant.alias = combatant.name; // Keep players' names unchanged
        }
      });
    },
    addMonster() {
      if (this.selectedMonster) {
        this.monsterCounter += 1; // Increment the monster counter
        const newMonster = {
          id: `${this.selectedMonster.id}-${Date.now()}`,
          name: this.selectedMonster.name,
          type: "monster",
          hp: this.selectedMonster.hp,
          maxHp: this.selectedMonster.hp,
          ac: this.selectedMonster.ac,
          dex: this.selectedMonster.dex || 10,
          initiative: 0,
          displayName: `${this.selectedMonster.name} ${this.monsterCounter}`, // Assign new suffix
        };
        this.combatants.push(newMonster); // Add the new monster
      }
    },

    updateMonsterAlias(index, alias) {
      this.combatants[index].alias = alias;
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

      const activeCombatantId = this.combatants[this.currentTurnIndex]?.id;

      this.combatants.sort((a, b) => b.initiative - a.initiative);

      const newIndex = this.combatants.findIndex(
        (combatant) => combatant.id === activeCombatantId
      );

      this.currentTurnIndex = newIndex !== -1 ? newIndex : 0;
    },
  },
  mounted() {
    this.fetchEncounters();
    this.fetchAvailableMonsters();
  },
};
</script>

<style>
.combat-tracking {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: "Georgia", serif;
  background: url("@/assets/fantasy-3756975_1280.jpg") no-repeat center center
    fixed;
  background-size: cover;
  min-height: 100vh;
  color: #fff;
  padding: 20px;
}

.content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
  gap: 20px;
}

.section {
  background-color: rgba(0, 0, 0, 0.8);
  padding: 20px;
  border-radius: 10px;
  flex: 1 1 45%;
  margin: 10px;
}

.styled-list {
  list-style: none;
  padding: 0;
}

.styled-list li {
  background-color: rgba(255, 255, 255, 0.1);
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.styled-list li.active {
  background-color: rgba(0, 128, 255, 0.5);
}

.end-combat {
  background-color: #ff4d4d;
  color: white;
}

.end-combat:hover {
  background-color: #e63939;
}

.dice-roll-section .dice-buttons button {
  margin-right: 10px;
}

.dice-roll-result {
  margin-top: 10px;
  font-size: 1.2em;
  color: #007bff;
  font-weight: bold;
}
</style>
