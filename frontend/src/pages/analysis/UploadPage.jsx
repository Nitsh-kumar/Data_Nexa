import { AppLayout } from '../../components/layout/AppLayout';
import { FileUploader } from '../../components/upload/FileUploader';
import { UploadProgress } from '../../components/upload/UploadProgress';
import { useUpload } from '../../hooks/useUpload';

export const UploadPage = () => {
  const { uploadProgress, uploadStatus } = useUpload();

  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-semibold text-text-primary">Upload dataset</h1>
          <p className="text-text-secondary">
            CSV, Excel, and Parquet files up to 2 GB are supported. Data never leaves your VPC.
          </p>
        </div>
        <FileUploader />
        <UploadProgress value={uploadProgress} status={uploadStatus} />
      </div>
    </AppLayout>
  );
};

