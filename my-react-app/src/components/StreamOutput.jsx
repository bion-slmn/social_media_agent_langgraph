import React from 'react';

const StreamOutput = ({ process, streamedData }) => {
    if (!process) return null;

    return (
        <div className="mt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Stream Response: {process}</h3>
            <div className="bg-gray-100 border border-gray-300 p-4 rounded-md h-64 overflow-y-auto font-mono text-sm whitespace-pre-wrap">
                {streamedData}
            </div>
        </div>
    );
};

export default StreamOutput;
