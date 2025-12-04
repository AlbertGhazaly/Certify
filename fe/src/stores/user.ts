import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
    const role = ref('');
    const username = ref('');
    const publicKeyX = ref('');
    const publicKeyY = ref('');

    function setUser(user) {
        role.value = user.role;
        username.value = user.username;
        publicKeyX.value = user.publicKeyX;
        publicKeyY.value = user.publicKeyY;
    }

    function clearUser() {
        role.value = '';
        username.value = '';
        publicKeyX.value = '';
        publicKeyY.value = '';
    }

    return { role, username, publicKeyX, publicKeyY, setUser, clearUser };
});