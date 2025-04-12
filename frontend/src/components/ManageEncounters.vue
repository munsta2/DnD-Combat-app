<template>
  <div class="encounter-builder">
    <header class="hero">
      <h1>Encounter Builder</h1>
      <p>Create, customize, and save your encounters for epic battles!</p>
      <router-link to="/" class="home-button">Home</router-link>
    </header>

    <div class="content">
      <!-- Party Selection -->
      <div class="party-selection">
        <h3>Select Party</h3>
        <h4>Parties</h4>
        <ul class="styled-list">
          <li
            v-for="party in parties"
            :key="party.id"
            @click="selectParty(party)"
            :class="{ selected: selectedParty?.id === party.id }"
          >
            {{ party.name }}
          </li>
        </ul>
        <h4>Individual Players</h4>
        <ul class="styled-list">
          <li
            v-for="player in players"
            :key="player.id"
            @click="togglePlayer(player)"
            :class="{ selected: selectedPlayers.includes(player) }"
          >
            {{ player.name }}
          </li>
        </ul>

        <!-- Monster Statblock -->

        <div class="stat-block section" v-if="selectedMonster">
          <button @click="addMonsterToEncounter">Add Monster</button>
          <h3>{{ selectedMonster.name }}</h3>
          <p>
            {{ selectedMonster.size }} {{ selectedMonster.type }},
            {{ selectedMonster.alignment }}
          </p>
          <p><strong>Armor Class:</strong> {{ selectedMonster.ac }}</p>
          <p><strong>Hit Points:</strong> {{ selectedMonster.hp }}</p>
          <p><strong>Speed:</strong> {{ selectedMonster.speed }}</p>

          <div class="abilities">
            <p>
              <strong>STR:</strong> {{ selectedMonster.stats.str }} ({{
                formatModifier(selectedMonster.stats.str)
              }})
            </p>
            <p>
              <strong>DEX:</strong> {{ selectedMonster.stats.dex }} ({{
                formatModifier(selectedMonster.stats.dex)
              }})
            </p>
            <p>
              <strong>CON:</strong> {{ selectedMonster.stats.con }} ({{
                formatModifier(selectedMonster.stats.con)
              }})
            </p>
            <p>
              <strong>INT:</strong> {{ selectedMonster.stats.int }} ({{
                formatModifier(selectedMonster.stats.int)
              }})
            </p>
            <p>
              <strong>WIS:</strong> {{ selectedMonster.stats.wis }} ({{
                formatModifier(selectedMonster.stats.wis)
              }})
            </p>
            <p>
              <strong>CHA:</strong> {{ selectedMonster.stats.cha }} ({{
                formatModifier(selectedMonster.stats.cha)
              }})
            </p>
          </div>

          <div class="divider"></div>

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

          <div v-if="selectedMonster.actions" class="actions">
            <h4>Actions</h4>
            <div v-html="selectedMonster.actions"></div>
          </div>

          <div v-if="selectedMonster.legendaryActions" class="actions">
            <h4>Legendary Actions</h4>
            <div v-html="selectedMonster.legendaryActions"></div>
          </div>

          <div v-if="selectedMonster.traits" class="actions">
            <h4>Traits</h4>
            <div v-html="selectedMonster.traits"></div>
          </div>

          <div v-if="selectedMonster.reactions" class="actions">
            <h4>Reactions</h4>
            <div v-html="selectedMonster.reactions"></div>
          </div>
        </div>
      </div>

      <!-- Encounter Summary -->
      <div class="encounter-summary">
        <h3>Encounter Summary</h3>
        <div class="form-row">
          <label for="encounter-name">Encounter Name:</label>
          <input
            id="encounter-name"
            v-model="encounter.name"
            placeholder="Enter encounter name"
          />
        </div>
        <div>
          <h4>Party:</h4>
          <p>{{ selectedParty?.name || "No party selected" }}</p>
          <ul class="styled-list">
            <li v-for="player in selectedPlayers" :key="player.id">
              {{ player.name }}
            </li>
          </ul>
        </div>
        <div>
          <h4>Monsters:</h4>
          <ul class="styled-list">
            <li v-for="monster in encounter.monsters" :key="monster.id">
              <div class="monster-box">
                <span>{{ monster.name }}</span>
                <input
                  type="text"
                  v-model="monster.alias"
                  placeholder="Set alias (optional)"
                  class="alias-input"
                />
                <button @click="removeMonster(monster)">Remove</button>
              </div>
            </li>
          </ul>
        </div>
        <div class="difficulty-box">
          <h4>Encounter Difficulty</h4>
          <p>{{ encounterDifficulty }}</p>
        </div>
        <button @click="saveEncounter">Save Encounter</button>
        <div class="encounter-management section">
          <h3>Existing Encounters</h3>
          <ul class="styled-list">
            <li v-for="encounter in encounters" :key="encounter.id">
              <span>{{ encounter.name }}</span>
              <button
                @click="deleteEncounter(encounter.id)"
                class="delete-button"
              >
                Delete
              </button>
            </li>
          </ul>
        </div>
      </div>

      <!-- Monster Selection -->
      <div class="monster-selection">
        <h3>Select Monsters</h3>
        <input
          type="text"
          v-model="monsterSearch"
          placeholder="Search Monsters..."
          class="search-bar"
        />
        <ul class="styled-list">
          <li
            v-for="monster in filteredMonsters"
            :key="monster.id"
            @click="selectMonster(monster)"
          >
            {{ monster.name }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      encounters: [],
      parties: [],
      players: [],
      monsters: [],
      selectedParty: null,
      selectedPlayers: [],
      encounter: {
        name: "",
        player_ids: [],
        monsters: [],
      },
      selectedMonster: null,
      monsterSearch: "",
    };
  },
  computed: {
    filteredMonsters() {
      return this.monsters.filter((monster) =>
        monster.name.toLowerCase().includes(this.monsterSearch.toLowerCase())
      );
    },
    encounterDifficulty() {
      const xpThresholds = {
        1: { easy: 25, medium: 50, hard: 75, deadly: 100 },
        2: { easy: 50, medium: 100, hard: 150, deadly: 200 },
        3: { easy: 75, medium: 150, hard: 225, deadly: 400 },
        4: { easy: 125, medium: 250, hard: 375, deadly: 500 },
        5: { easy: 250, medium: 500, hard: 750, deadly: 1100 },
      };

      let partyThresholds = { easy: 0, medium: 0, hard: 0, deadly: 0 };
      this.selectedPlayers.forEach((player) => {
        const level = player.level;
        // // console.log("Processing Player:", player);
        if (xpThresholds[level]) {
          partyThresholds.easy += xpThresholds[level].easy;
          partyThresholds.medium += xpThresholds[level].medium;
          partyThresholds.hard += xpThresholds[level].hard;
          partyThresholds.deadly += xpThresholds[level].deadly;
        }
      });
      // console.log("party: ", partyThresholds);
      // console.log(this.encounter.monsters);
      const totalMonsterXP = this.encounter.monsters.reduce(
        (sum, monster) => sum + monster.exp,
        0
      );
      // console.log("monsters: ", totalMonsterXP);
      const monsterCount = this.encounter.monsters.length;
      let multiplier = 1;
      if (monsterCount === 2) multiplier = 1.5;
      else if (monsterCount >= 3 && monsterCount <= 6) multiplier = 2;
      else if (monsterCount >= 7 && monsterCount <= 10) multiplier = 2.5;
      else if (monsterCount >= 11 && monsterCount <= 14) multiplier = 3;
      else if (monsterCount >= 15) multiplier = 4;

      const adjustedXP = totalMonsterXP * multiplier;
      // console.log("audjetedxp: ", adjustedXP);
      // for (let difficulty in partyThresholds) {
      //   console.log(`${difficulty}: ${partyThresholds[difficulty]}`);
      // }

      if (
        adjustedXP == 0 ||
        (partyThresholds.deadly == 0 &&
          partyThresholds.hard == 0 &&
          partyThresholds.medium == 0 &&
          partyThresholds.easy == 0)
      )
        return "n/a";

      if (adjustedXP >= partyThresholds.deadly) return "Deadly";
      if (adjustedXP >= partyThresholds.hard) return "Hard";
      if (adjustedXP >= partyThresholds.medium) return "Medium";
      if (adjustedXP >= partyThresholds.easy) return "Easy";
      return "Trivial";
    },
  },
  methods: {
    async fetchEncounters() {
      try {
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/api/encounters`
        );
        if (response.ok) {
          this.encounters = await response.json();
        } else {
          console.error("Failed to fetch encounters.");
        }
      } catch (error) {
        console.error("Error fetching encounters:", error);
      }
    },

    async deleteEncounter(encounterId) {
      const confirmed = confirm(
        "Are you sure you want to delete this encounter?"
      );
      if (!confirmed) return;

      try {
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/api/encounters/${encounterId}`,
          {
            method: "DELETE",
          }
        );

        if (response.ok) {
          alert("Encounter deleted successfully!");
          // Optionally remove the encounter from the UI (if you're listing encounters here)
          this.encounters = this.encounters.filter(
            (encounter) => encounter.id !== encounterId
          );
        } else {
          alert("Failed to delete the encounter.");
        }
      } catch (error) {
        console.error("Error deleting encounter:", error);
        alert("An error occurred while deleting the encounter.");
      }
    },

    async fetchData() {
      const partyResponse = await fetch(
        `${process.env.VUE_APP_API_URL}/api/parties`
      );
      this.parties = await partyResponse.json();

      const playerResponse = await fetch(
        `${process.env.VUE_APP_API_URL}/api/players`
      );
      this.players = await playerResponse.json();

      const monsterResponse = await fetch(
        `${process.env.VUE_APP_API_URL}/api/monsters`
      );
      this.monsters = await monsterResponse.json();
    },
    formatModifier(stat) {
      const modifier = Math.floor((stat - 10) / 2);
      return modifier > 0 ? `+${modifier}` : modifier.toString();
    },
    selectParty(party) {
      // console.log("Selected Party:", party);
      if (this.selectedParty?.id === party.id) {
        // Deselect the party
        this.selectedParty = null;
        const partyPlayerIds = party.players.map((player) => player.id);
        this.selectedPlayers = this.selectedPlayers.filter(
          (player) => !partyPlayerIds.includes(player.id)
        );
        this.encounter.party_id = null;
        this.encounter.player_ids = [
          ...this.selectedPlayers.map((player) => player.id),
        ];
      } else {
        // Select a new party
        this.selectedParty = party;
        const newPlayers = party.players.filter(
          (player) =>
            !this.selectedPlayers.some(
              (selectedPlayer) => selectedPlayer.id === player.id
            )
        );
        // Replace selectedPlayers with a new array
        this.selectedPlayers = [...this.selectedPlayers, ...newPlayers];
        this.encounter.party_id = party.id;
        this.encounter.player_ids = [
          ...this.selectedPlayers.map((player) => player.id),
        ];
      }
      // console.log(
      //   "Selected Players after party selection:",
      //   this.selectedPlayers
      // );
    },

    togglePlayer(player) {
      if (this.selectedPlayers.some((p) => p.id === player.id)) {
        this.selectedPlayers = this.selectedPlayers.filter(
          (p) => p.id !== player.id
        );
      } else {
        this.selectedPlayers.push(player);
      }
      this.encounter.party_id = this.selectedParty
        ? this.selectedParty.id
        : null;
      this.encounter.player_ids = this.selectedPlayers.map((p) => p.id);
    },
    selectMonster(monster) {
      this.selectedMonster = monster;
    },
    addMonsterToEncounter() {
      if (this.selectedMonster) {
        this.encounter.monsters.push({
          id: this.selectedMonster.id,
          name: this.selectedMonster.name,
          exp: this.selectedMonster.exp,
          alias: "",
        });
        this.selectedMonster = null;
      }
    },
    removeMonster(monster) {
      this.encounter.monsters = this.encounter.monsters.filter(
        (m) => m.id !== monster.id
      );
    },
    async saveEncounter() {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/encounters`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.encounter),
        }
      );
      if (response.ok) {
        alert("Encounter saved successfully!");
        await this.fetchEncounters();
      } else {
        alert("Failed to save encounter.");
      }
    },
  },
  mounted() {
    this.fetchData();
    this.fetchEncounters();
  },
};
</script>

<style>
.encounter-builder {
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
  width: 100%;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.party-selection,
.encounter-summary,
.monster-selection,
.monster-statblock {
  background-color: rgba(0, 0, 0, 0.8);
  padding: 20px;
  border-radius: 10px;
  flex: 1;
}

.styled-list li {
  background-color: rgba(255, 255, 255, 0.1);
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.styled-list li.selected {
  background-color: rgba(0, 128, 255, 0.5);
}

.monster-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  margin: 5px 0;
  border-radius: 5px;
}

.difficulty-box {
  margin-top: 20px;
  background-color: rgba(255, 255, 0, 0.1);
  padding: 10px;
  border: 1px solid rgba(255, 255, 0, 0.8);
  border-radius: 5px;
  text-align: center;
  color: #fff;
}
</style>
