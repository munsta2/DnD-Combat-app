import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./components/HomePage.vue";
import ManagePlayers from "./components/ManagePlayers.vue";
import ManageParties from "./components/ManageParties.vue";
import ManageMonsters from "./components/ManageMonsters.vue";

// Define your routes
const routes = [
  { path: "/", component: HomePage },
  { path: "/players", component: ManagePlayers },
  { path: "/parties", component: ManageParties },
  { path: "/monsters", component: ManageMonsters },
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Create the Vue app instance
const app = createApp(App);

// Use the router in the app
app.use(router);

// Mount the app to the DOM
app.mount("#app");
