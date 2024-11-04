// useTripStore.js
import { create } from "zustand";
import config from "../config";

const useTripStore = create((set) => ({
  // Initial state
  trips: [],
  loading: false,
  error: null,

  // Actions
  fetchTrips: async (uid) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(
        `${config.backendUrl}/fetch_all_trip?uid=${uid}`
      );
      const data = await response.json();
      if (!response.ok) {
        set({ error: data.message, loading: false });
        throw new Error("Failed to fetch trips");
      }
      
      set({ trips: data.trips, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  addTrip: async (uid, title, startDate, endDate) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`${config.backendUrl}/addtrip`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ uid, title, startDate, endDate }),
      });
      if (!response.ok) {
        throw new Error("Failed to add trip");
      }
      const data = await response.json();
      set((state) => ({ trips: [...state.trips, data.trip], loading: false }));
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  clearTrips: () => set({ trips: [] }),
}));

export default useTripStore;
