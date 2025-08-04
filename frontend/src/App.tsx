import React, { useState, useEffect } from 'react';
import RemoveRepositoryButton from './components/RemoveRepositoryButton';

// Define TypeScript interfaces
interface CacheFile {
  path: string;
  size: number;
  size_formatted: string;
  last_accessed: string | null;
  folder: string;
}

interface CacheStats {
  size: number;
  size_formatted: string;
  folders: number;
  files: number;
  last_updated: string;
}

interface DownloadProgress {
  status: string;
  progress: number;
  repo_id: string;
  filename: string;
  start_time: string;
  error?: string;
  end_time?: string;
  file_path?: string;
}

const App: React.FC = () => {
  const [cacheStats, setCacheStats] = useState<CacheStats | null>(null);
  const [cacheFiles, setCacheFiles] = useState<CacheFile[]>([]);
  const [downloads, setDownloads] = useState<{[key: string]: DownloadProgress}>({});
  const [repoId, setRepoId] = useState('');
  const [filename, setFilename] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch cache stats and files
  const fetchCacheData = async () => {
    try {
      const response = await fetch('/api/cache/stats');
      const stats = await response.json();
      setCacheStats(stats);
      
      const filesResponse = await fetch('/api/cache/files');
      const files = await filesResponse.json();
      setCacheFiles(files.files);
    } catch (error) {
      console.error('Error fetching cache data:', error);
    }
  };

  // Start a new download
  const startDownload = async () => {
    if (!repoId || !filename) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/cache/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repo_id: repoId,
          filename: filename
        })
      });
      
      const result = await response.json();
      if (result.download_id) {
        // Start polling for progress
        pollDownloadProgress(result.download_id);
      }
    } catch (error) {
      console.error('Error starting download:', error);
    } finally {
      setLoading(false);
    }
  };

  // Poll for download progress
  const pollDownloadProgress = (downloadId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`/api/cache/download/${downloadId}/progress`);
        const progress = await response.json();
        
        setDownloads(prev => ({
          ...prev,
          [downloadId]: progress
        }));
        
        // Stop polling when download is complete or failed
        if (progress.status === 'completed' || progress.status === 'failed' || progress.status === 'cancelled') {
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Error polling download progress:', error);
        clearInterval(interval);
      }
    }, 1000); // Poll every second
  };

  // Clear cache
  const clearCache = async () => {
    try {
      const response = await fetch('/api/cache/clear', {
        method: 'POST'
      });
      const result = await response.json();
      console.log('Cache cleared:', result.message);
      // Refresh data after clearing
      fetchCacheData();
    } catch (error) {
      console.error('Error clearing cache:', error);
    }
  };

  // Handle successful repository removal
  const handleRemoveSuccess = () => {
    // Refresh the data to reflect the removal
    fetchCacheData();
  };

  // Initial load
  useEffect(() => {
    fetchCacheData();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Hugging Face CLI Cache Manager</h1>
      
      {/* Stats Section */}
      <div className="bg-white shadow rounded-lg p-4 mb-4">
        <h2 className="text-xl font-semibold mb-2">Cache Statistics</h2>
        {cacheStats ? (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-blue-100 p-4 rounded">
              <p className="text-sm font-medium text-gray-600">Size</p>
              <p className="text-2xl font-bold">{cacheStats.size_formatted}</p>
            </div>
            <div className="bg-green-100 p-4 rounded">
              <p className="text-sm font-medium text-gray-600">Folders</p>
              <p className="text-2xl font-bold">{cacheStats.folders}</p>
            </div>
            <div className="bg-yellow-100 p-4 rounded">
              <p className="text-sm font-medium text-gray-600">Files</p>
              <p className="text-2xl font-bold">{cacheStats.files}</p>
            </div>
            <div className="bg-purple-100 p-4 rounded">
              <p className="text-sm font-medium text-gray-600">Last Updated</p>
              <p className="text-2xl font-bold">{new Date(cacheStats.last_updated).toLocaleString()}</p>
            </div>
          </div>
        ) : (
          <p>Loading cache stats...</p>
        )}
      </div>
      
      {/* Download Section */}
      <div className="bg-white shadow rounded-lg p-4 mb-4">
        <h2 className="text-xl font-semibold mb-2">Download Model</h2>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="repoId">
            Repository ID
          </label>
          <input
            id="repoId"
            type="text"
            value={repoId}
            onChange={(e) => setRepoId(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., lysandre/arxiv-nlp"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="filename">
            Filename
          </label>
          <input
            id="filename"
            type="text"
            value={filename}
            onChange={(e) => setFilename(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., config.json"
          />
        </div>
        <button
          onClick={startDownload}
          disabled={loading || !repoId || !filename}
          className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 ${loading || !repoId || !filename ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {loading ? 'Downloading...' : 'Start Download'}
        </button>
      </div>
      
      {/* Downloads Section */}
      <div className="bg-white shadow rounded-lg p-4 mb-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Active Downloads</h2>
          <button
            onClick={clearCache}
            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Clear Cache
          </button>
        </div>
        
        {Object.keys(downloads).length > 0 ? (
          <div className="space-y-4">
            {Object.entries(downloads).map(([id, download]) => (
              <div key={id} className="border rounded p-4">
                <div className="flex justify-between mb-2">
                  <span className="font-medium">{download.repo_id}/{download.filename}</span>
                  <span className="text-sm">{download.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className={`h-2.5 rounded-full ${download.status === 'completed' ? 'bg-green-500' : 
                      download.status === 'failed' ? 'bg-red-500' : 
                      download.status === 'cancelled' ? 'bg-yellow-500' : 'bg-blue-500'
                    }`} 
                    style={{ width: `${download.progress}%` }}
                  ></div>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  Status: {download.status}
                  {download.error && <span className="text-red-500 ml-2">Error: {download.error}</span>}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No active downloads</p>
        )}
      </div>
      
      {/* Files Section */}
      <div className="bg-white shadow rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-2">Cached Files ({cacheFiles.length})</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Accessed</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {cacheFiles.map((file, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{file.path}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{file.size_formatted}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {file.last_accessed ? new Date(file.last_accessed).toLocaleString() : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <RemoveRepositoryButton repository={file} onRemoveSuccess={handleRemoveSuccess} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default App;