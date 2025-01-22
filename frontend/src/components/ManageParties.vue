<template>
  <div class="manage-parties-page">
    <header class="hero">
      <h1>Manage Parties</h1>
      <p>Assemble your adventurers and prepare for the unknown!</p>
    </header>

    <form @submit.prevent="createParty" class="party-form">
      <div class="form-row">
        <label for="party-name">Party Name</label>
        <input
          id="party-name"
          v-model="newParty.name"
          placeholder="Enter party name"
          required
        />
      </div>
      <div class="form-row">
        <label>Select Players</label>
        <div v-for="player in players" :key="player.id" class="player-checkbox">
          <input
            type="checkbox"
            :value="player.id"
            v-model="newParty.playerIds"
          />
          <span>{{ player.name }}</span>
        </div>
      </div>
      <button type="submit">Create Party</button>
    </form>

    <div class="party-list">
      <h2>Existing Parties</h2>
      <ul>
        <li v-for="party in parties" :key="party.id">
          <strong>{{ party.name }}</strong>
          <div>
            <button @click="startEdit(party)">Edit</button>
            <button @click="deleteParty(party.id)">Delete</button>
          </div>
          <ul>
            <li v-if="party.players.length === 0">No players in this party</li>
            <li v-for="player in party.players" :key="player.id">
              {{ player.name }}
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <div v-if="editingParty" class="edit-party-form">
      <h3>Edit Party: {{ editingParty.name }}</h3>
      <form @submit.prevent="savePartyChanges">
        <input v-model="editingParty.name" placeholder="Party Name" required />
        <div v-for="player in players" :key="player.id" class="player-checkbox">
          <input
            type="checkbox"
            :value="player.id"
            v-model="editingParty.playerIds"
          />
          <span>{{ player.name }}</span>
        </div>
        <button type="submit">Save Changes</button>
        <button @click="cancelEdit">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "ManageParties",
  setup() {
    const players = ref([]);
    const parties = ref([]);
    const newParty = ref({ name: "", playerIds: [] });
    const editingParty = ref(null);

    const fetchPlayers = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/players`
      );
      players.value = await response.json();
      console.log("Players loaded:", players.value); // Debugging output
    };

    const fetchParties = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/parties`
      );
      const data = await response.json();
      parties.value = data.map((party) => ({
        ...party,
        players: party.players || [],
      }));
    };

    const createParty = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}http://localhost:5000/api/parties`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(newParty.value),
        }
      );
      const createdParty = await response.json();
      parties.value.push(createdParty);
      newParty.value = { name: "", playerIds: [] };
    };

    const deleteParty = async (partyId) => {
      await fetch(`${process.env.VUE_APP_API_URL}/api/parties/${partyId}`, {
        method: "DELETE",
      });
      parties.value = parties.value.filter((p) => p.id !== partyId);
    };

    const startEdit = (party) => {
      editingParty.value = {
        ...party,
        playerIds: party.players.map((player) => player.id),
      };
    };

    const savePartyChanges = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/parties/${editingParty.value.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(editingParty.value),
        }
      );
      const updatedParty = await response.json();
      const index = parties.value.findIndex((p) => p.id === updatedParty.id);
      parties.value[index] = updatedParty;
      editingParty.value = null;
    };

    const cancelEdit = () => {
      editingParty.value = null;
    };

    onMounted(() => {
      fetchPlayers();
      fetchParties();
    });

    return {
      players,
      parties,
      newParty,
      editingParty,
      createParty,
      deleteParty,
      startEdit,
      savePartyChanges,
      cancelEdit,
    };
  },
};
</script>

<style>
.manage-parties-page {
  text-align: center;
  font-family: "Georgia", serif;
  color: #fff;
  /* background: url("@/assets/fantasy-background.jpg") no-repeat center center fixed; */
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

.party-form {
  margin: 20px auto;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
}

.form-row {
  margin-bottom: 15px;
}

.player-checkbox {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.player-checkbox span {
  margin-left: 8px;
  font-size: 1rem;
  color: #000;
}

.party-list ul {
  list-style: none;
  padding: 0;
}

.party-list li {
  background-color: rgba(0, 0, 0, 0.6);
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
