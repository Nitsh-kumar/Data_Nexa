import { create } from 'zustand';
import { datasetService } from '../services/datasetService';

const initialState = {
  currentFile: null,
  uploadProgress: 0,
  uploadStatus: 'idle', // idle, uploading, success, error
  dataset: null,
  selectedGoal: null,
  error: null,
};

export const uploadStore = create((set, get) => ({
  ...initialState,
  setFile: (file) => set({ currentFile: file, uploadStatus: 'idle', error: null }),
  setGoal: (goal) => set({ selectedGoal: goal }),
  uploadFile: async () => {
    const { currentFile, selectedGoal } = get();
    if (!currentFile) throw new Error('No file selected');
    const formData = new FormData();
    formData.append('file', currentFile);
    if (selectedGoal) {
      formData.append('goal_type', selectedGoal);
    }
    try {
      set({ uploadStatus: 'uploading', uploadProgress: 0, error: null });
      const dataset = await datasetService.upload(formData);
      set({ dataset, uploadStatus: 'success', uploadProgress: 100 });
      return dataset;
    } catch (error) {
      set({
        uploadStatus: 'error',
        error: error.message || 'Upload failed',
      });
      throw error;
    }
  },
  reset: () => set({ ...initialState }),
}));

