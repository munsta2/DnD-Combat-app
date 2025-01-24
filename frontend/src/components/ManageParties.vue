<template>
  <div class="manage-parties-page">
    <header class="hero">
      <h1>Manage Parties</h1>
      <p>Assemble your adventurers and prepare for the unknown!</p>
      <router-link to="/" class="home-button">Home</router-link>
    </header>

    <div class="content">
      <!-- Party Creation Form -->
      <div class="party-form section">
        <h3>{{ editingParty ? "Edit Party" : "Create a New Party" }}</h3>
        <form
          @submit.prevent="editingParty ? savePartyChanges() : createParty()"
        >
          <div class="form-row">
            <label for="party-name">Party Name</label>
            <input
              id="party-name"
              v-model="partyForm.name"
              placeholder="Enter party name"
              required
            />
          </div>
          <div class="form-row">
            <label>Select Players</label>
            <div
              v-for="player in players"
              :key="player.id"
              class="player-checkbox"
            >
              <input
                type="checkbox"
                :value="player.id"
                v-model="partyForm.playerIds"
              />
              <span>{{ player.name }}</span>
            </div>
          </div>
          <button type="submit">
            {{ editingParty ? "Save Changes" : "Create Party" }}
          </button>
          <button v-if="editingParty" @click="cancelEdit" class="cancel-button">
            Cancel
          </button>
        </form>
      </div>

      <!-- Party List -->
      <div class="party-list section">
        <h3>Existing Parties</h3>
        <ul class="styled-list">
          <li v-for="party in parties" :key="party.id">
            <div class="party-details">
              <strong>{{ party.name }}</strong>
              <ul>
                <li v-if="party.players.length === 0">
                  No players in this party
                </li>
                <li v-for="player in party.players" :key="player.id">
                  {{ player.name }}
                </li>
              </ul>
            </div>
            <div class="party-actions">
              <button @click="startEdit(party)">Edit</button>
              <button class="delete-button" @click="deleteParty(party.id)">
                Delete
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from "vue";

export default {
  name: "ManageParties",
  setup() {
    const players = ref([]);
    const parties = ref([]);
    const editingParty = ref(null);
    const partyForm = reactive({ name: "", playerIds: [] });

    const fetchPlayers = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/players`
      );
      players.value = await response.json();
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

    const resetForm = () => {
      partyForm.name = "";
      partyForm.playerIds = [];
    };

    const createParty = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/parties`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(partyForm),
        }
      );
      const createdParty = await response.json();
      parties.value.push(createdParty);
      resetForm();
    };

    const deleteParty = async (partyId) => {
      await fetch(`${process.env.VUE_APP_API_URL}/api/parties/${partyId}`, {
        method: "DELETE",
      });
      parties.value = parties.value.filter((p) => p.id !== partyId);
    };

    const startEdit = (party) => {
      editingParty.value = party;
      partyForm.name = party.name;
      partyForm.playerIds = party.players.map((player) => player.id);
    };

    const savePartyChanges = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/parties/${editingParty.value.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(partyForm),
        }
      );
      const updatedParty = await response.json();
      const index = parties.value.findIndex((p) => p.id === updatedParty.id);
      parties.value[index] = updatedParty;
      editingParty.value = null;
      resetForm();
    };

    const cancelEdit = () => {
      editingParty.value = null;
      resetForm();
    };

    onMounted(() => {
      fetchPlayers();
      fetchParties();
    });

    return {
      players,
      parties,
      editingParty,
      partyForm,
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
}

.styled-list {
  list-style: none;
  padding: 0;
}

.styled-list li {
  background-color: rgba(255, 255, 255, 0.1);
  margin: 10px 0;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.party-details {
  text-align: left;
}

.party-details ul {
  list-style: none;
  padding: 0;
}

.party-actions button {
  margin-right: 10px;
}

button {
  padding: 10px 15px;
  font-size: 14px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.delete-button {
  background-color: #dc3545;
}

.delete-button:hover {
  background-color: #b02a37;
}

.cancel-button {
  background-color: #6c757d;
}

.cancel-button:hover {
  background-color: #565e64;
}
</style>
