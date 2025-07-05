import React from 'react';

const ThreadInfo = ({ threadId }) => {
    if (!threadId) return null;

    return (
        <div className="mt-6 p-4 bg-green-100 text-green-800 rounded-md font-mono border border-green-300">
            <strong>Thread ID:</strong> {threadId}
        </div>
    );
};

export default ThreadInfo;
