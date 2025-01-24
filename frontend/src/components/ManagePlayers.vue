<template>
  <div class="manage-players">
    <header class="hero">
      <h1>Manage Players</h1>
      <p>Add, update, and manage players for your adventures.</p>
      <router-link to="/" class="home-button">Home</router-link>
    </header>

    <div class="content">
      <!-- Player Form -->
      <div class="player-form section">
        <h3>{{ editMode ? "Update Player" : "Add Player" }}</h3>
        <form @submit.prevent="addOrUpdatePlayer">
          <div class="form-row">
            <label for="name">Player Name</label>
            <input
              id="name"
              v-model="newPlayer.name"
              placeholder="Enter player name"
              required
            />
          </div>
          <div class="form-row">
            <label for="level">Level</label>
            <input
              id="level"
              v-model.number="newPlayer.level"
              type="number"
              min="1"
              max="20"
              placeholder="Enter level"
              required
            />
          </div>
          <div class="form-row">
            <label for="ac">Armor Class</label>
            <input
              id="ac"
              v-model.number="newPlayer.ac"
              type="number"
              min="1"
              placeholder="Enter AC"
              required
            />
          </div>
          <div class="form-row">
            <label for="initiativeModifier">Initiative Modifier</label>
            <input
              id="initiativeModifier"
              v-model.number="newPlayer.initiativeModifier"
              type="number"
              placeholder="Enter initiative modifier"
              required
            />
          </div>
          <button type="submit">
            {{ editMode ? "Update Player" : "Add Player" }}
          </button>
        </form>
      </div>

      <!-- Player List -->
      <div class="player-list section">
        <h3>Current Players</h3>
        <ul class="styled-list">
          <li v-for="player in players" :key="player.id">
            <div class="player-info">
              <span><strong>Name:</strong> {{ player.name }}</span>
              <span><strong>Level:</strong> {{ player.level }}</span>
              <span><strong>AC:</strong> {{ player.ac }}</span>
              <span>
                <strong>Initiative:</strong> {{ player.initiativeModifier }}
              </span>
            </div>
            <div class="player-actions">
              <button @click="editPlayer(player)">Edit</button>
              <button class="delete-button" @click="removePlayer(player.id)">
                Delete
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script scoped>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "ManagePlayers",
  setup() {
    const players = ref([]);
    const newPlayer = ref({
      name: "",
      level: 1,
      ac: 10,
      initiativeModifier: 0,
    });
    const editMode = ref(false);
    const currentPlayerId = ref(null);
    const router = useRouter();

    const fetchPlayers = async () => {
      const response = await fetch(
        `${process.env.VUE_APP_API_URL}/api/players`
      );
      players.value = await response.json();
    };

    const addOrUpdatePlayer = async () => {
      const url = editMode.value
        ? `${process.env.VUE_APP_API_URL}/api/players/${currentPlayerId.value}`
        : `${process.env.VUE_APP_API_URL}/api/players`;
      const method = editMode.value ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newPlayer.value),
      });

      const updatedPlayer = await response.json();

      if (editMode.value) {
        const index = players.value.findIndex(
          (p) => p.id === currentPlayerId.value
        );
        players.value[index] = updatedPlayer;
        editMode.value = false;
        currentPlayerId.value = null;
      } else {
        players.value.push(updatedPlayer);
      }

      newPlayer.value = { name: "", level: 1, ac: 10, initiativeModifier: 0 };
    };

    const editPlayer = (player) => {
      newPlayer.value = { ...player };
      editMode.value = true;
      currentPlayerId.value = player.id;
    };

    const removePlayer = async (id) => {
      try {
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/api/players/${id}`,
          {
            method: "DELETE",
          }
        );

        if (response.ok) {
          players.value = players.value.filter((p) => p.id !== id);
          alert("Player deleted and removed from any associated encounters.");
        } else {
          const error = await response.json();
          console.error("Error deleting player:", error);
          alert(`Failed to delete player: ${error.error || "Unknown error"}`);
        }
      } catch (error) {
        console.error("Error deleting player:", error);
        alert("An error occurred while deleting the player.");
      }
    };

    onMounted(fetchPlayers);

    return {
      players,
      newPlayer,
      editMode,
      addOrUpdatePlayer,
      editPlayer,
      removePlayer,
      router,
    };
  },
};
</script>

<style>
.manage-players {
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

.player-info span {
  display: block;
}

.player-actions button {
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
</style>
