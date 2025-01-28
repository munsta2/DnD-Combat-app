<template>
  <div class="combat-tracking">
    <header class="hero">
      <h1>Combat Tracking</h1>
      <p>
        Manage combatants, track turns, apply damage, and dynamically manage
        combatants.
      </p>
      <router-link to="/" class="home-button">Home</router-link>
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

      <!-- Action Buttons (Roll Initiative, Next Turn, End Combat) -->
      <div class="action-section section">
        <h3>Combat Actions</h3>
        <button @click="rollMonsterInitiatives">
          Roll Monster Initiatives
        </button>
        <button @click="nextTurn">Next Turn</button>
        <button @click="endCombat" class="end-combat">End Combat</button>
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
            :class="[
              { active: index === currentTurnIndex },
              { dead: combatant.hp === 0 },
            ]"
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

      <!-- Stat Block Section -->
      <div class="stat-block section" v-if="activeCombatant && statBlock">
        <h3>{{ statBlock.name }}</h3>
        <p>
          {{ statBlock.size }} {{ statBlock.type }}, {{ statBlock.alignment }}
        </p>
        <p><strong>Armor Class:</strong> {{ statBlock.ac }}</p>
        <p><strong>Hit Points:</strong> {{ statBlock.hp }}</p>
        <p><strong>Speed:</strong> {{ statBlock.speed }}</p>

        <div class="abilities">
          <p>
            <strong>STR:</strong> {{ statBlock.stats.str }} <br />({{
              formatModifier(statBlock.stats.str)
            }})
          </p>
          <p>
            <strong>DEX:</strong> {{ statBlock.stats.dex }} <br />({{
              formatModifier(statBlock.stats.dex)
            }})
          </p>
          <p>
            <strong>CON:</strong> {{ statBlock.stats.con }} <br />({{
              formatModifier(statBlock.stats.con)
            }})
          </p>
          <p>
            <strong>INT:</strong> {{ statBlock.stats.int }} <br />({{
              formatModifier(statBlock.stats.int)
            }})
          </p>
          <p>
            <strong>WIS:</strong> {{ statBlock.stats.wis }} <br />({{
              formatModifier(statBlock.stats.wis)
            }})
          </p>
          <p>
            <strong>CHA:</strong> {{ statBlock.stats.cha }} <br />({{
              formatModifier(statBlock.stats.cha)
            }})
          </p>
        </div>

        <div class="divider"></div>

        <div class="details">
          <p>
            <strong>Damage Vulnerabilities:</strong>
            {{ statBlock.damageVulnerabilities || "None" }}
          </p>
          <p><strong>Senses:</strong> {{ statBlock.senses }}</p>
          <p><strong>Languages:</strong> {{ statBlock.languages }}</p>
          <p>
            <strong>Challenge:</strong> {{ statBlock.cr }} ({{ statBlock.exp }}
            XP)
          </p>
        </div>

        <div v-if="statBlock.actions" class="actions">
          <h4>Actions</h4>
          <div v-html="statBlock.actions"></div>
        </div>

        <div v-if="statBlock.legendaryActions" class="actions">
          <h4>Legendary Actions</h4>
          <div v-html="statBlock.legendaryActions"></div>
        </div>

        <div v-if="statBlock.traits" class="actions">
          <h4>Traits</h4>
          <div v-html="statBlock.traits"></div>
        </div>

        <div v-if="statBlock.reactions" class="actions">
          <h4>Reactions</h4>
          <div v-html="statBlock.reactions"></div>
        </div>
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
      statBlock: null,
    };
  },
  computed: {
    activeCombatant() {
      return this.combatants[this.currentTurnIndex] || null;
    },
    diceRollTotal() {
      return this.diceRollResult.reduce((total, roll) => total + roll, 0);
    },
  },
  methods: {
    formatModifier(stat) {
      const modifier = Math.floor((stat - 10) / 2);
      return modifier > 0 ? `+${modifier}` : modifier.toString();
    },
    fetchStatBlock(combatant) {
      console.log("I am being called");
      if (combatant.type === "monster") {
        fetch(`${process.env.VUE_APP_API_URL}/api/monsters/${combatant.dbId}`)
          .then((response) => response.json())
          .then((data) => {
            this.statBlock = data;
            console.log(data);
          })
          .catch((error) => {
            console.error("Error fetching stat block:", error);
          });
      } else {
        this.statBlock = null; // Clear stat block for non-monster combatants
      }
    },
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
    calculateDexMod(dex) {
      return Math.floor((dex - 10) / 2);
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
          this.combatants = data.turn_order.map((combatant, index) => {
            if (combatant.type === "monster") {
              monsterCount += 1; // Increment monster count
              console.log(combatant);
              return {
                ...combatant,
                id: `${combatant.id}-${index}`, // Unique frontend ID
                dbId: combatant.id, // Set dbId to the monster's database id
                displayName: `${combatant.name} ${monsterCount}`,
                initiative: combatant.initiative || 0,
              };
            } else {
              // Players keep their original name
              return {
                ...combatant,
                id: `player-${index}`,
                displayName: combatant.name,
                initiative: 0,
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
          const dexMod = Math.floor(((combatant.dex || 10) - 10) / 2);
          console.log(dexMod, combatant.dex);
          combatant.initiative = Math.floor(Math.random() * 20) + 1 + dexMod;
        }
      });
      this.combatants.sort((a, b) => b.initiative - a.initiative);
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
          // id: `${this.selectedMonster.id}`,
          id: `${this.selectedMonster.id}-${Date.now()}`, //front end id
          dbId: this.selectedMonster.id, // backend id
          name: this.selectedMonster.name,
          type: "monster",
          hp: this.selectedMonster.hp,
          maxHp: this.selectedMonster.hp,
          ac: this.selectedMonster.ac,
          dex: this.selectedMonster.stats.dex,
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
      console.log("this is who I am doing damage to,", combatant.name);
      if (combatant) {
        combatant.hp = Math.max(0, combatant.hp - this.damageAmount);
        this.damageAmount = null;
      }
    },
    nextTurn() {
      this.currentTurnIndex =
        (this.currentTurnIndex + 1) % this.combatants.length;
      this.fetchStatBlock(this.activeCombatant); // Update stat block on turn change
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
    updateInitiative(index, newInitiative) {
      const combatant = this.combatants[index];
      console.log(combatant.initiative, newInitiative);
      // if (combatant.initiative === newInitiative) return; // Skip if no change

      // Update initiative for the combatant
      combatant.initiative = newInitiative;

      // Preserve the current active combatant's ID
      const activeCombatantId = this.combatants[this.currentTurnIndex]?.id;

      // Sort the combatants array by initiative
      this.combatants = [...this.combatants].sort(
        (a, b) => b.initiative - a.initiative
      );
      // Update the currentTurnIndex to match the active combatant's new position
      const newIndex = this.combatants.findIndex(
        (combatant) => combatant.id === activeCombatantId
      );
      this.currentTurnIndex = newIndex !== -1 ? newIndex : 0;
    },
  },
  watch: {
    activeCombatant: {
      handler(newValue) {
        if (newValue && newValue.type === "monster") {
          this.fetchStatBlock(newValue);
        } else {
          this.statBlock = null; // Clear the stat block for non-monster turns
        }
      },
      immediate: true, // Run immediately on component load
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

.stat-block {
  background-color: #fdf6e3; /* Light parchment background */
  color: #2c2c2c; /* Dark text color for readability */
  padding: 20px;
  border-radius: 10px;
  border: 2px solid #b68973; /* Slightly darker parchment border */
  font-family: "Georgia", serif;
  margin: 20px auto;
  max-width: 600px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.stat-block h3 {
  font-size: 1.8em;
  color: #7a4214; /* Deep brown for headers */
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
  margin-top: 20px;
  font-size: 1.4em;
  color: #7a4214;
  text-transform: uppercase;
  text-align: left;
  border-bottom: 1px solid #b68973;
  padding-bottom: 5px;
}

.stat-block .abilities {
  display: flex;
  justify-content: space-between;
  text-align: center;
  margin-bottom: 10px;
}

.stat-block .abilities p {
  flex: 1;
  font-size: 1.1em;
  margin: 0;
}

.stat-block .details {
  background-color: #fdfaf5;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #d7c4a1;
  margin-top: 10px;
}

.stat-block .details p {
  font-size: 0.95em;
  margin: 5px 0;
}

.stat-block .divider {
  height: 2px;
  background-color: #b68973;
  margin: 15px 0;
}

.stat-block .actions {
  margin-top: 10px;
  background-color: #fdfaf5;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #d7c4a1;
}

.stat-block .actions h4 {
  margin-bottom: 5px;
  font-size: 1.3em;
}

.stat-block .actions div {
  margin: 5px 0;
  font-size: 1em;
  color: #2c2c2c;
}

.stat-block strong {
  font-weight: bold;
  color: #7a4214;
}
.home-button {
  display: inline-block;
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #00ff9d;
  color: white;
  text-decoration: none;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease;
}

.home-button:hover {
  background-color: #0056b3;
}

.styled-list li.dead {
  background-color: rgba(
    255,
    0,
    0,
    0.5
  ); /* Red background for dead combatants */
  color: #fff; /* White text for better contrast */
  font-weight: bold;
  text-decoration: line-through; /* Optional: visually strike through their name */
}

.styled-list li.dead input {
  text-decoration: line-through; /* Strike through input text if you want */
}
</style>
