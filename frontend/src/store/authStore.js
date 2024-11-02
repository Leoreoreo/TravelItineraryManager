// useStore.js
import { create } from "zustand";

const useAuthStore = create((set) => ({
  uid: null,
  username: null,
  setUser: (uid, username) => set({ uid, username }),
  clearUser: () => set({ uid: null, username: null }),
}));

export default useAuthStore;
