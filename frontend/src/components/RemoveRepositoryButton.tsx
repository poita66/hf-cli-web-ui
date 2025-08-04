import React, { useState } from 'react';

interface CacheFile {
  path: string;
  size: number;
  size_formatted: string;
  last_accessed: string | null;
  folder: string;
}

interface RemoveRepositoryProps {
  repository: CacheFile;
  onRemoveSuccess: () => void;
}

const RemoveRepositoryButton: React.FC<RemoveRepositoryProps> = ({ repository, onRemoveSuccess }) => {
  const [isRemoving, setIsRemoving] = useState(false);

  const handleRemove = async () => {
    if (!window.confirm(`Are you sure you want to remove this repository?\n${repository.path}`)) {
      return;
    }

    setIsRemoving(true);
    try {
      const response = await fetch(`/api/cache/remove/${encodeURIComponent(repository.path)}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        console.log(`Repository ${repository.path} removed successfully`);
        onRemoveSuccess();
      } else {
        const error = await response.json();
        alert(`Error removing repository: ${error.error}`);
      }
    } catch (error) {
      console.error('Error removing repository:', error);
      alert('Error removing repository');
    } finally {
      setIsRemoving(false);
    }
  };

  return (
    <button
      onClick={handleRemove}
      disabled={isRemoving}
      className={`ml-2 px-3 py-1 text-sm rounded ${isRemoving ? 'bg-gray-400' : 'bg-red-500 hover:bg-red-700'} text-white`}
    >
      {isRemoving ? 'Removing...' : 'Remove'}
    </button>
  );
};

export default RemoveRepositoryButton;