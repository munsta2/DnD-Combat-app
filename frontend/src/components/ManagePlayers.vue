<template>
  <div class="manage-players">
    <h1>Manage Players</h1>

    <form class="player-form" @submit.prevent="addOrUpdatePlayer">
      <div class="form-row">
        <label for="name">Player Name</label>
        <input
          id="name"
          v-model="newPlayer.name"
          placeholder="Player Name"
          required
        />
      </div>
      <div class="form-row">
        <label for="level">Level</label>
        <input
          id="level"
          v-model.number="newPlayer.level"
          type="number"
          placeholder="Level"
          required
        />
      </div>
      <div class="form-row">
        <label for="ac">Armor Class</label>
        <input
          id="ac"
          v-model.number="newPlayer.ac"
          type="number"
          placeholder="Armor Class"
          required
        />
      </div>
      <div class="form-row">
        <label for="initiativeModifier">Initiative Modifier</label>
        <input
          id="initiativeModifier"
          v-model.number="newPlayer.initiativeModifier"
          type="number"
          placeholder="Initiative Modifier"
          required
        />
      </div>
      <button type="submit">
        {{ editMode ? "Update Player" : "Add Player" }}
      </button>
    </form>

    <div class="player-list">
      <h2>Current Players</h2>
      <ul>
        <li v-for="player in players" :key="player.id">
          <span>{{ player.name }}</span>
          <span>Level: {{ player.level }}</span>
          <span>AC: {{ player.ac }}</span>
          <span>Initiative: {{ player.initiativeModifier }}</span>
          <button @click="editPlayer(player)">Edit</button>
          <button @click="removePlayer(player.id)">Delete</button>
        </li>
      </ul>
    </div>

    <button class="home-button" @click="goHome">Go to Home</button>
  </div>
</template>

<script>
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
      await fetch(`${process.env.VUE_APP_API_URL}/api/players/${id}`, {
        method: "DELETE",
      });
      players.value = players.value.filter((p) => p.id !== id);
    };

    const goHome = () => {
      router.push("/");
    };

    onMounted(fetchPlayers);

    return {
      players,
      newPlayer,
      editMode,
      addOrUpdatePlayer,
      editPlayer,
      removePlayer,
      goHome,
    };
  },
};
</script>

<style>
.manage-players {
  padding: 20px;
}

.player-form {
  margin-bottom: 20px;
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 5px;
  background: #f9f9f9;
}

.form-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 15px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 5px;
}

button:hover {
  background-color: #0056b3;
}

.player-list {
  margin-top: 20px;
}

.player-list h2 {
  margin-bottom: 10px;
}

.player-list ul {
  list-style-type: none;
  padding: 0;
}

.player-list li {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.player-list li span {
  margin-right: 15px;
}

.home-button {
  margin-top: 20px;
  padding: 10px 15px;
  font-size: 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.home-button:hover {
  background-color: #218838;
}
</style>
