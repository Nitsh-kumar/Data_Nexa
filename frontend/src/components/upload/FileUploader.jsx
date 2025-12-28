import { useRef } from 'react';
import { Button } from '../ui/button';
import { useUpload } from '../../hooks/useUpload';
import { Progress } from '../ui/progress';

export const FileUploader = () => {
  const fileInputRef = useRef(null);
  const { currentFile, uploadStatus, uploadProgress, setFile, uploadFile } = useUpload();

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  const handleUpload = async () => {
    try {
      await uploadFile();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="space-y-4 rounded-2xl border border-dashed border-primary-200 bg-white p-6 text-center">
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept=".csv,.xlsx,.xls,.parquet"
        onChange={handleFileSelect}
      />
      <p className="text-sm text-text-secondary">
        Drag & drop your dataset here or click to browse.
      </p>
      <div className="flex justify-center gap-3">
        <Button variant="secondary" onClick={() => fileInputRef.current?.click()}>
          Choose File
        </Button>
        <Button disabled={!currentFile || uploadStatus === 'uploading'} onClick={handleUpload}>
          Upload
        </Button>
      </div>
      {currentFile && (
        <div className="text-sm text-text-primary">
          Selected: <span className="font-medium">{currentFile.name}</span>
        </div>
      )}
      {uploadStatus !== 'idle' && (
        <div className="space-y-2">
          <Progress value={uploadProgress} />
          <p className="text-xs text-text-secondary">Status: {uploadStatus}</p>
        </div>
      )}
    </div>
  );
};

