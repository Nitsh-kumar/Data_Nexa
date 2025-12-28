import { useMemo } from 'react';
import { uploadStore } from '../store/uploadStore';

/**
 * Upload hook exposes the current file, status, and helper actions so components
 * like FileUploader stay declarative.
 */
export function useUpload() {
  const state = uploadStore((storeState) => storeState);

  return useMemo(
    () => ({
      currentFile: state.currentFile,
      uploadProgress: state.uploadProgress,
      uploadStatus: state.uploadStatus,
      dataset: state.dataset,
      selectedGoal: state.selectedGoal,
      error: state.error,
      setFile: state.setFile,
      setGoal: state.setGoal,
      uploadFile: state.uploadFile,
      reset: state.reset,
    }),
    [state],
  );
}

