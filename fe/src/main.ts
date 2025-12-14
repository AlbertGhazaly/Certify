import { createApp } from "vue"
import { createPinia } from "pinia"
import App from "./App.vue"
import router from "./router"
import "./style.css"
import { useAuthStore } from "./stores/authStore"

const app = createApp(App)

app.use(createPinia())

const authStore = useAuthStore()
authStore.init()

app.use(router)
app.mount("#app")
