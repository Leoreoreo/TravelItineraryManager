// useStore.js
import { create } from "zustand";

const useAuthStore = create((set) => ({
  uid: null,
  username: null,
  trait: "",
  bod: "",
  setUser: (uid, username, trait, bod) => set({ uid, username, trait, bod }),
  setTrait: (trait) => set({ trait }),
  setBOD: (bod) => set({ bod }),

  clearUser: () => set({ uid: null, username: null }),
}));

export default useAuthStore;
