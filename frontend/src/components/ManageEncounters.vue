<template>
  <div class="encounter-builder">
    <header class="hero">
      <h1>Encounter Builder</h1>
      <p>Create, customize, and save your encounters for epic battles!</p>
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
        <div class="monster-statblock" v-if="selectedMonster">
          <h3>{{ selectedMonster.name }}</h3>
          <p>
            {{ selectedMonster.size }} {{ selectedMonster.type }},
            {{ selectedMonster.alignment }}
          </p>
          <p><strong>Armor Class:</strong> {{ selectedMonster.ac }}</p>
          <p><strong>Hit Points:</strong> {{ selectedMonster.hp }}</p>
          <p><strong>Speed:</strong> {{ selectedMonster.speed }}</p>
          <h4>Abilities</h4>
          <p><strong>STR:</strong> {{ selectedMonster.stats?.str || "N/A" }}</p>
          <p><strong>DEX:</strong> {{ selectedMonster.stats?.dex || "N/A" }}</p>
          <p><strong>CON:</strong> {{ selectedMonster.stats?.con || "N/A" }}</p>
          <p><strong>INT:</strong> {{ selectedMonster.stats?.int || "N/A" }}</p>
          <p><strong>WIS:</strong> {{ selectedMonster.stats?.wis || "N/A" }}</p>
          <p><strong>CHA:</strong> {{ selectedMonster.stats?.cha || "N/A" }}</p>
          <h4>Actions</h4>
          <div v-html="selectedMonster.actions"></div>
          <button @click="addMonsterToEncounter">Add Monster</button>
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
        <button @click="saveEncounter">Save Encounter</button>
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
  },
  methods: {
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
    selectParty(party) {
      if (this.selectedParty?.id === party.id) {
        // Deselect the current party
        this.selectedParty = null;

        // Remove party players from selectedPlayers
        const partyPlayerIds = party.players.map((player) => player.id);
        this.selectedPlayers = this.selectedPlayers.filter(
          (player) => !partyPlayerIds.includes(player.id)
        );

        this.encounter.party_id = null;
        this.encounter.player_ids = this.selectedPlayers.map(
          (player) => player.id
        );
      } else {
        // Select a new party
        this.selectedParty = party;

        // Add party players to selectedPlayers if not already selected
        const newPlayers = party.players.filter(
          (player) =>
            !this.selectedPlayers.some(
              (selectedPlayer) => selectedPlayer.id === player.id
            )
        );
        this.selectedPlayers = [...this.selectedPlayers, ...newPlayers];

        this.encounter.party_id = party.id;
        this.encounter.player_ids = this.selectedPlayers.map(
          (player) => player.id
        );
      }
    },
    togglePlayer(player) {
      if (this.selectedPlayers.some((p) => p.id === player.id)) {
        // Remove player
        this.selectedPlayers = this.selectedPlayers.filter(
          (p) => p.id !== player.id
        );
      } else {
        // Add player
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
      } else {
        alert("Failed to save encounter.");
      }
    },
  },
  mounted() {
    this.fetchData();
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
</style>
