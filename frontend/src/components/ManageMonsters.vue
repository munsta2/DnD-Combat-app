<template>
  <div class="manage-monsters-page">
    <header class="hero">
      <h1>Manage Monsters</h1>
      <p>Add, edit, or delete monsters to populate your encounters!</p>
    </header>

    <form @submit.prevent="createMonster" class="monster-form">
      <h3>Add New Monster</h3>
      <div class="form-row">
        <label for="monster-name">Name</label>
        <input
          id="monster-name"
          v-model="newMonster.name"
          placeholder="Monster name"
          required
        />
      </div>
      <div class="form-row">
        <label for="monster-size">Size</label>
        <input
          id="monster-size"
          v-model="newMonster.size"
          placeholder="Size (e.g., Large)"
        />
      </div>
      <div class="form-row">
        <label for="monster-type">Type</label>
        <input
          id="monster-type"
          v-model="newMonster.type"
          placeholder="Type (e.g., Beast)"
        />
      </div>
      <div class="form-row">
        <label for="monster-alignment">Alignment</label>
        <input
          id="monster-alignment"
          v-model="newMonster.alignment"
          placeholder="Alignment (e.g., Chaotic Evil)"
        />
      </div>
      <div class="form-row">
        <label for="monster-hp">Hit Points</label>
        <input
          id="monster-hp"
          v-model="newMonster.hp"
          type="number"
          placeholder="HP"
          required
        />
      </div>
      <div class="form-row">
        <label for="monster-ac">Armor Class</label>
        <input
          id="monster-ac"
          v-model="newMonster.ac"
          type="number"
          placeholder="AC"
          required
        />
      </div>
      <div class="form-row">
        <label for="monster-speed">Speed</label>
        <input
          id="monster-speed"
          v-model="newMonster.speed"
          placeholder="Speed (e.g., 30 ft., fly 60 ft.)"
        />
      </div>
      <div class="form-row">
        <label for="monster-stats">Stats (STR, DEX, CON, INT, WIS, CHA)</label>
        <input
          id="monster-str"
          v-model="newMonster.stats.str"
          type="number"
          placeholder="STR"
        />
        <input
          id="monster-dex"
          v-model="newMonster.stats.dex"
          type="number"
          placeholder="DEX"
        />
        <input
          id="monster-con"
          v-model="newMonster.stats.con"
          type="number"
          placeholder="CON"
        />
        <input
          id="monster-int"
          v-model="newMonster.stats.int"
          type="number"
          placeholder="INT"
        />
        <input
          id="monster-wis"
          v-model="newMonster.stats.wis"
          type="number"
          placeholder="WIS"
        />
        <input
          id="monster-cha"
          v-model="newMonster.stats.cha"
          type="number"
          placeholder="CHA"
        />
      </div>
      <div class="form-row">
        <label for="monster-actions">Actions</label>
        <textarea
          id="monster-actions"
          v-model="newMonster.actions"
          placeholder="Describe the monster's actions"
        ></textarea>
      </div>
      <div class="form-row">
        <label for="monster-legendary-actions">Legendary Actions</label>
        <textarea
          id="monster-legendary-actions"
          v-model="newMonster.legendaryActions"
          placeholder="Describe legendary actions"
        ></textarea>
      </div>
      <div class="form-row">
        <label for="monster-traits">Traits</label>
        <textarea
          id="monster-traits"
          v-model="newMonster.traits"
          placeholder="Describe special traits"
        ></textarea>
      </div>
      <div class="form-row">
        <label for="monster-reactions">Reactions</label>
        <textarea
          id="monster-reactions"
          v-model="newMonster.reactions"
          placeholder="Describe reactions"
        ></textarea>
      </div>
      <button type="submit">Add Monster</button>
    </form>

    <div class="monster-list">
      <h2>Existing Monsters</h2>
      <ul>
        <li v-for="monster in monsters" :key="monster.id">
          <strong>{{ monster.name }}</strong>
          <p>{{ monster.size }} {{ monster.type }}, {{ monster.alignment }}</p>
          <p>
            HP: {{ monster.hp }}, AC: {{ monster.ac }}, Speed:
            {{ monster.speed }}
          </p>
          <p>
            Stats: STR: {{ monster.stats.str }}, DEX: {{ monster.stats.dex }},
            CON: {{ monster.stats.con }}, INT: {{ monster.stats.int }}, WIS:
            {{ monster.stats.wis }}, CHA: {{ monster.stats.cha }}
          </p>
          <p>Actions: {{ monster.actions }}</p>
          <p>Legendary Actions: {{ monster.legendaryActions }}</p>
          <p>Traits: {{ monster.traits }}</p>
          <p>Reactions: {{ monster.reactions }}</p>
          <div>
            <button @click="startEdit(monster)">Edit</button>
            <button @click="deleteMonster(monster.id)">Delete</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "ManageMonsters",
  setup() {
    const monsters = ref([]);
    const newMonster = ref({
      name: "",
      size: "",
      type: "",
      alignment: "",
      hp: 0,
      ac: 0,
      speed: "",
      stats: { str: 0, dex: 0, con: 0, int: 0, wis: 0, cha: 0 },
      actions: "",
      legendaryActions: "",
      traits: "",
      reactions: "",
    });
    const editingMonster = ref(null);

    const fetchMonsters = async () => {
      const response = await fetch("http://localhost:5000/api/monsters");
      monsters.value = await response.json();
    };

    const createMonster = async () => {
      const response = await fetch("http://localhost:5000/api/monsters", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newMonster.value),
      });
      const createdMonster = await response.json();
      monsters.value.push(createdMonster);
      newMonster.value = {
        name: "",
        size: "",
        type: "",
        alignment: "",
        hp: 0,
        ac: 0,
        speed: "",
        stats: { str: 0, dex: 0, con: 0, int: 0, wis: 0, cha: 0 },
        actions: "",
        legendaryActions: "",
        traits: "",
        reactions: "",
      };
    };

    const deleteMonster = async (monsterId) => {
      await fetch(`http://localhost:5000/api/monsters/${monsterId}`, {
        method: "DELETE",
      });
      monsters.value = monsters.value.filter((m) => m.id !== monsterId);
    };

    const startEdit = (monster) => {
      editingMonster.value = { ...monster };
    };

    const saveMonsterChanges = async () => {
      const response = await fetch(
        `http://localhost:5000/api/monsters/${editingMonster.value.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(editingMonster.value),
        }
      );
      const updatedMonster = await response.json();
      const index = monsters.value.findIndex((m) => m.id === updatedMonster.id);
      monsters.value[index] = updatedMonster;
      editingMonster.value = null;
    };

    const cancelEdit = () => {
      editingMonster.value = null;
    };

    onMounted(() => {
      fetchMonsters();
    });

    return {
      monsters,
      newMonster,
      editingMonster,
      createMonster,
      deleteMonster,
      startEdit,
      saveMonsterChanges,
      cancelEdit,
    };
  },
};
</script>

<style>
.manage-monsters-page {
  text-align: center;
  font-family: "Georgia", serif;
  color: #fff;
  background: url("@/assets/fantasy-3756975_1280.jpg") no-repeat center center
    fixed;
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

.monster-form {
  margin: 20px auto;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
}

.form-row {
  margin-bottom: 15px;
}

.monster-list ul {
  list-style: none;
  padding: 0;
}

.monster-list li {
  background-color: rgba(0, 0, 0, 0.6);
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
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
