/**
 * Collection of formatting helpers to keep UI components tidy.
 */
export const formatDate = (dateString) => {
  if (!dateString) return '—';
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(dateString));
};

export const formatNumber = (value) => {
  if (value === null || value === undefined) return '—';
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 1,
  }).format(value);
};

export const formatBytes = (bytes = 0, decimals = 1) => {
  if (!bytes) return '0 B';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / k ** i).toFixed(dm))} ${sizes[i]}`;
};

