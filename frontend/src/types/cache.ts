export interface CacheFile {
  path: string;
  size: number;
  size_formatted: string;
  last_accessed: string | null;
  folder: string;
}

export interface CacheStats {
  size: number;
  size_formatted: string;
  folders: number;
  files: number;
  last_updated: string;
}

export interface DownloadProgress {
  status: string;
  progress: number;
  repo_id: string;
  filename: string;
  start_time: string;
  error?: string;
  end_time?: string;
  file_path?: string;
}